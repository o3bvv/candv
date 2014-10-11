# -*- coding: utf-8 -*-
"""
This module defines base constant and base container for constants. All other
stuff must be derived from them.

Each container has :attr:`~ConstantsContainer.constant_class` attribute. It
specifies class of constants which will be defined within contaner.
"""
import six

from collections import OrderedDict


class Constant(object):
    """
    Base class for all constants. Can be merged into a container instance.

    :ivar str name: constant's name. Is set up automatically and is equal to
                    the name of container's attribute
    """

    # Tracks each time a Constant instance is created. Used to retain order.
    _creation_counter = 0

    def __init__(self):
        self.name = None
        self.container = None

        # Increase the creation counter, and save our local copy.
        self._creation_counter = Constant._creation_counter
        Constant._creation_counter += 1

    def _post_init(self, container, name):
        """
        Called automatically by container after container's class construction.
        """
        self.name = name
        self.container = container

    def to_group(self, group_class, **group_members):
        """
        Convert a constant into a constants group.

        :param class group_class: a class of group container which will be
                                  created
        :param group_members: unpacked dict which defines group members.

        :returns: a lazy constants group which will be evaluated by container.
                  During group evaluation :meth:`merge_into_group` will be
                  called.

        **Example**::

            from candv import Constants, SimpleConstant

            class FOO(Constants):
                A = SimpleConstant()
                B = SimpleConstant().to_group(
                    group_class=Constants,
                    B2=SimpleConstant(),
                    B0=SimpleConstant(),
                    B1=SimpleConstant(),
            )
        """
        return _LazyConstantsGroup(self, group_class, **group_members)

    def merge_into_group(self, group):
        """
        Called automatically by container after group construction.

        .. note::

            Redefine this method in all derived classes. Attach all custom
            attributes and methods to the group here.

        :param group: an instance of :class:`ConstantsContainer` or it's
                      subclass this constant will be merged into

        :returns: ``None``
        """
        group._creation_counter = self._creation_counter

    @property
    def full_name(self):
        return "{0}.{1}".format(self.container.full_name, self.name)

    def __repr__(self):
        """
        Return text identifying both which constant this is and which
        collection it belongs to.
        """
        return "<constant '{0}'>".format(self.full_name)


def _evaluate_constants(obj, attributes):
    constants = []
    for name, the_object in six.iteritems(attributes):
        if isinstance(the_object, _LazyConstantsGroup):
            group = the_object._evaluate(obj, name)
            setattr(obj, name, group)
            constants.append((name, group))
        elif isinstance(the_object, obj.constant_class):
            if the_object.container is not None:
                raise ValueError(
                    'Cannot use "{0}" as value for the attribute '
                    '"{1}" for "{2}", because "{0}" already belongs '
                    'to "{3}".'
                    .format(the_object, name, obj, the_object.container)
                )
            the_object._post_init(obj, name)
            constants.append((name, the_object))

    constants.sort(key=lambda x: x[1]._creation_counter)
    obj._constants.update(OrderedDict(constants))


class _LazyConstantsGroup(object):

    def __init__(self, constant, group_class, **group_members):
        for name, obj in group_members.items():
            if not isinstance(obj, (Constant, _LazyConstantsGroup)):
                raise TypeError(
                    "\"{0}\" cannot be a member of a group. Only instances of "
                    "\"{1}\" or other groups can be."
                    .format(obj, Constant)
                )
        self.constant = constant
        self.group_class = group_class
        self.group_members = group_members

    def _evaluate(self, parent, name):
        full_name = "{0}.{1}".format(parent.full_name, name)
        __repr__ = lambda x: "<constants group '{0}'>".format(full_name)
        attributes = {
            '__name__': name,
            '__new__': object.__new__,  # Remove singleton protection
            '__repr__': classmethod(__repr__),
            'name': name,
            'container': parent,
            'full_name': full_name,
            '_constants_eveluation': False,
        }
        attributes.update(self.group_members)

        cls = type(full_name, (self.group_class, ), attributes)

        group = cls()
        _evaluate_constants(group, self.group_members)

        self.constant.merge_into_group(group)

        del self.constant
        del self.group_class
        del self.group_members

        return group


class _ConstantsContainerMeta(type):
    """
    Metaclass for creating constants container classes.
    """
    def __new__(self, class_name, bases, attributes):
        constants_eveluation = attributes.pop('_constants_eveluation', True)

        cls = (
            super(_ConstantsContainerMeta, self)
            .__new__(self, class_name, bases, attributes)
        )
        # Create '_constants' as class attribute, so we can use class methods
        # in future
        cls._constants = OrderedDict()

        constant_class = getattr(cls, 'constant_class', None)
        if not issubclass(constant_class, Constant):
            raise TypeError(
                "\"{0}\" which is used as \"constant_class\" for \"{1}\" must "
                "be derived from \"{2}\"."
                .format(constant_class, cls, Constant)
            )
        # We may skip evaluation to manually specify a container object for
        # constants
        if constants_eveluation:
            _evaluate_constants(cls, attributes)
        return cls

    @property
    def name(self):
        return self.__name__

    full_name = name

    def __repr__(self):
        return "<constants container '{0}'>".format(self.name)


@six.add_metaclass(_ConstantsContainerMeta)
class ConstantsContainer(object):
    """
    Base class for creating constants containers. Each constant defined within
    container will remember it's creation order. See an example in
    :meth:`constants`.

    :cvar constant_class: stores a class of constants which can be stored by
                          container. This attribute **MUST** be set up manually
                          when you define a new container type. Otherwise
                          container will not be initialized. Default: ``None``
    :raises TypeError: if you try to create an instance of container.
                       Containers are singletons and they cannot be
                       instantiated. Their attributes must be used directly.
    """

    #: Defines a top-level class of constants which can be stored by container
    constant_class = Constant

    def __new__(cls):
        """
        Classes representing constants containers are not intended to be
        instantiated.

        The class object itself is used directly.
        """
        raise TypeError(
            "\"{0}\" cannot be instantiated, because constant containers are "
            "not designed for this."
            .format(cls)
        )

    @classmethod
    def contains(cls, name):
        """
        Check if container has a constant with a given name.

        :param str name: a constant's name to check

        :returns: ``True`` if given name belongs to container,
                  ``False`` otherwise
        :rtype: :class:`bool`
        """
        return name in cls.names()

    @classmethod
    def names(cls):
        """
        List all names of constants within container.

        :returns: a list of constant names in order constants were defined
        :rtype: :class:`list` of strings

        **Example**::

            >>> from candv import Constants, SimpleConstant
            >>> class FOO(Constants):
            ...     foo = SimpleConstant()
            ...     bar = SimpleConstant()
            ...
            >>> FOO.names()
            ['foo', 'bar']
        """
        return list(cls.iternames())

    @classmethod
    def iternames(cls):
        """
        Same as :meth:`names` but returns an interator.
        """
        return six.iterkeys(cls._constants)

    @classmethod
    def constants(cls):
        """
        List all constants in container.

        :returns: list of constants in order they were defined
        :rtype: :class:`list`

        **Example**::

            >>> from candv import Constants, SimpleConstant
            >>> class FOO(Constants):
            ...     foo = SimpleConstant()
            ...     bar = SimpleConstant()
            ...
            >>> [x.name for x in FOO.constants()]
            ['foo', 'bar']
        """
        return list(cls.iterconstants())

    #: *New since 1.1.2.*
    #:
    #: Alias for :meth:`constants`.
    #: Added for consistency with dictionaries. Use :class:`~candv.Values` and
    #: :meth:`~candv.Values.values` if you need to have constants with real
    #: values.
    values = constants

    @classmethod
    def iterconstants(cls):
        """
        Same as :meth:`constants` but returns an interator.
        """
        return six.itervalues(cls._constants)

    #: *New since 1.1.2.*
    #:
    #: Alias for :meth:`iterconstants`.
    #: Added for consistency with dictionaries. Use :class:`~candv.Values` and
    #: :meth:`~candv.Values.itervalues` if you need to have constants with real
    #: values.
    itervalues = iterconstants

    @classmethod
    def items(cls):
        """
        Get list of constants with their names.

        :returns: list of constants with their names in order they were
                  defined. Each element in list is a :class:`tuple` in format
                  ``(name, constant)``.
        :rtype: :class:`list`

        **Example**::

            >>> from candv import Constants, SimpleConstant
            >>> class FOO(Constants):
            ...     foo = SimpleConstant()
            ...     bar = SimpleConstant()
            ...
            >>> FOO.items()
            [('foo', <constant 'FOO.foo'>), ('bar', <constant 'FOO.bar'>)]
        """
        return list(cls.iteritems())

    @classmethod
    def iteritems(cls):
        """
        Same as :meth:`items` but returns an interator.
        """
        return six.iteritems(cls._constants)

    @classmethod
    def get_by_name(cls, name):
        """
        Try to get constant by it's name.

        :param str name: name of constant to search for

        :returns: a constant
        :rtype: a class specified by :attr:`constant_class` which is
                :class:`Constant` or it's subclass

        :raises KeyError: if constant name ``name`` is not present in
                          container

        **Example**::

            >>> from candv import Constants, SimpleConstant
            >>> class FOO(Constants):
            ...     foo = SimpleConstant()
            ...     bar = SimpleConstant()
            ...
            >>> FOO.get_by_name('foo')
            <constant 'FOO.foo'>
        """
        try:
            return cls._constants[name]
        except KeyError:
            raise KeyError(
                "Constant \"{0}\" is not present in \"{1}\""
                .format(name, cls)
            )
