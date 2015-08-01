# -*- coding: utf-8 -*-
"""
This module defines base constant and base container for constants. All other
stuff must be derived from them.

Each container has :attr:`~ConstantsContainer.constant_class` attribute. It
specifies class of constants which will be defined within contaner.
"""

import six
import types

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

    def _post_init(self, name, container=None):
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
        prefix = self.container.full_name if self.container else "__UNBOUND__"
        return "{0}.{1}".format(prefix, self.name)

    def to_primitive(self, context=None):
        """
        .. versionadded:: 1.3.0
        """
        return {'name': self.name, }

    def __repr__(self):
        """
        Return text identifying both which constant this is and which
        collection it belongs to.
        """
        return "<constant '{0}'>".format(self.full_name)

    def __hash__(self):
        """
        .. versionadded:: 1.3.1
        """
        return hash(self.full_name)

    def __eq__(self, other):
        """
        .. versionadded:: 1.3.1
        """
        return (isinstance(other, Constant)
                and (self.full_name == other.full_name))

    def __ne__(self, other):
        """
        .. versionadded:: 1.3.1
        """
        return not (self == other)


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
        self.group_members.update({
            'name': name,
            'full_name': full_name,
            'container': parent,
            '__repr': "<constants group '{0}'>".format(full_name),
        })
        group = type(full_name, (self.group_class, ), self.group_members)
        self.constant.merge_into_group(group)

        to_primitive = self._get_to_primitive(self.constant, group)
        group.to_primitive = types.MethodType(to_primitive, group)

        del self.constant
        del self.group_class
        del self.group_members

        return group

    @staticmethod
    def _get_to_primitive(group, constant):

        group_primitive = group.to_primitive
        constant_primitive = constant.to_primitive

        def to_primitive(self, context=None):
            primitive = group_primitive(context)
            primitive.update(constant_primitive(context))
            return primitive

        return to_primitive


class _ConstantsContainerMeta(type):
    """
    Metaclass for creating constants container classes.
    """
    def __new__(self, class_name, bases, attributes):
        if not 'name' in attributes:
            attributes['name'] = class_name
        if not 'full_name' in attributes:
            attributes['full_name'] = class_name

        __repr = attributes.pop(
            '__repr',
            "<constants container '{0}'>".format(attributes['name'])
        )
        cls = (
            super(_ConstantsContainerMeta, self)
            .__new__(self, class_name, bases, attributes)
        )
        cls.__repr = __repr

        constant_class = getattr(cls, 'constant_class', None)
        if not issubclass(constant_class, Constant):
            raise TypeError(
                "\"{0}\" which is used as \"constant_class\" for \"{1}\" must "
                "be derived from \"{2}\"."
                .format(constant_class, cls, Constant)
            )

        constants = []
        for name, the_object in six.iteritems(attributes):
            if isinstance(the_object, _LazyConstantsGroup):
                group = the_object._evaluate(cls, name)
                setattr(cls, name, group)
                constants.append((name, group))
            elif isinstance(the_object, cls.constant_class):
                if the_object.container is not None:
                    raise ValueError(
                        'Cannot use "{0}" as value for the attribute '
                        '"{1}" for "{2}", because "{0}" already belongs '
                        'to "{3}".'
                        .format(the_object, name, cls, the_object.container)
                    )
                the_object._post_init(name, cls)
                constants.append((name, the_object))
            elif isinstance(the_object, Constant):
                the_object._post_init(name)
        constants.sort(key=lambda x: x[1]._creation_counter)
        cls._constants = OrderedDict(constants)

        return cls

    def __repr__(self):
        return self.__repr

    def __getitem__(self, name):
        """
        Try to get constant by it's name.

        :param str name: name of constant to search for

        :returns: a constant
        :rtype: an instance of :class:`Constant` or it's subclass

        :raises KeyError: if constant name ``name`` is not present in
                          container

        **Example**::

            >>> from candv import Constants, SimpleConstant
            >>> class FOO(Constants):
            ...     foo = SimpleConstant()
            ...     bar = SimpleConstant()
            ...
            >>> FOO['foo']
            <constant 'FOO.foo'>
        """
        try:
            return self._constants[name]
        except KeyError:
            raise KeyError(
                "Constant \"{0}\" is not present in \"{1}\""
                .format(name, self)
            )

    def __contains__(self, name):
        return name in self._constants

    def __len__(self):
        return len(self._constants)

    def __iter__(self):
        return self.iternames()

    def get(self, name, default=None):
        """
        Try to get constant by it's name or fallback to default.

        :param str name: name of constant to search for
        :param default: an object returned by default if constant with a given
                        name is not present in the container

        :returns: a constant or a default value
        :rtype: an instance of :class:`Constant` or it's subclass, or `default`
                value

        **Example**::

            >>> from candv import Constants, SimpleConstant
            >>> class FOO(Constants):
            ...     foo = SimpleConstant()
            ...     bar = SimpleConstant()
            ...
            >>> FOO.get('foo')
            <constant 'FOO.foo'>
            >>> FOO.get('xxx')
            >>>
            >>> FOO.get('xxx', default=123)
            123
        """
        return self[name] if name in self else default

    def has_name(self, name):
        """
        Check if container has a constant with a given name.

        :param str name: a constant's name to check

        :returns: ``True`` if given name belongs to container,
                  ``False`` otherwise
        :rtype: :class:`bool`
        """
        return name in self

    def names(self):
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
        return list(self.iternames())

    def iternames(self):
        """
        Same as :meth:`names` but returns an interator.
        """
        return six.iterkeys(self._constants)

    def constants(self):
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
        return list(self.iterconstants())

    def iterconstants(self):
        """
        Same as :meth:`constants` but returns an interator.
        """
        return six.itervalues(self._constants)

    def items(self):
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
        return list(self.iteritems())

    def iteritems(self):
        """
        Same as :meth:`items` but returns an interator.
        """
        return six.iteritems(self._constants)

    #: .. versionadded:: 1.1.2
    #:
    #: Alias for :meth:`constants`.
    #: Added for consistency with dictionaries. Use :class:`~candv.Values` and
    #: :meth:`~candv.Values.values` if you need to have constants with real
    #: values.
    values = constants

    #: .. versionadded:: 1.1.2
    #:
    #: Alias for :meth:`iterconstants`.
    #: Added for consistency with dictionaries. Use :class:`~candv.Values` and
    #: :meth:`~candv.Values.itervalues` if you need to have constants with real
    #: values.
    itervalues = iterconstants

    def to_primitive(self, context=None):
        """
        .. versionadded:: 1.3.0
        """
        return {
            'name': self.name,
            'items': [x.to_primitive(context) for x in self.iterconstants()]
        }


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
            "not designed for that."
            .format(cls)
        )


def with_constant_class(the_class):
    """
    A mixin factory which allows to set constant class for constants container
    outside container itself. This may help to create more readable container
    definition, e.g.:

        >>> from candv import Constants, SimpleConstant, with_constant_class
        >>>
        >>> class SomeConstant(SimpleConstant):
        ...     pass
        ...
        >>> class FOO(with_constant_class(SomeConstant), Constants):
        ...     A = SomeConstant()
        ...     B = SomeConstant()
        ...
        >>> FOO.constant_class
        <class '__main__.SomeConstant'>
    """
    class ConstantContainerMixin(object):
        constant_class = the_class

    return ConstantContainerMixin
