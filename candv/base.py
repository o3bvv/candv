# -*- coding: utf-8 -*-
"""
This module defines base constant and base container for constants. All other
stuff must be derived from them.

Each container has :attr:`~ConstantsContainer.constant_class` attribute. It
specifies class of constants which will be defined within contaner.
"""
import six

from collections import OrderedDict


def _constant_repr(full_name):
    return "<constant '{0}'>".format(full_name)


class _LazyConstantsGroup(object):

    def __init__(self, constant, group_class, **group_members):
        for name, obj in group_members.items():
            if not isinstance(obj, (Constant, _LazyConstantsGroup)):
                raise TypeError("{0} cannot be a member of a constants group"
                                .format(obj.__class__))
        self.constant = constant
        self.group_class = group_class
        self.group_members = group_members

    def _evaluate(self, parent, name):
        group_class, self.group_class = self.group_class, None
        group_members, self.group_members = self.group_members, None

        cls_name = "{0}.{1}".format(parent.__name__, name)
        group_repr = _constant_repr(cls_name)

        group_members.update({
            '__new__': object.__new__, # Remove singleton protection
            '__repr__': lambda self: group_repr,
            '__name__': name,
            'name': name,
        })

        cls = type(cls_name, (group_class, ), group_members)
        group = cls()
        self.constant._merge_into_group(group)
        return group


class Constant(object):
    """
    Base class for all constants.

    :ivar str name: constant's name. Is set up automatically and equals to the
                    name of container's attribute
    """

    # Tracks each time a Constant instance is created. Used to retain order.
    _creation_counter = 0

    def __init__(self):
        self.name = None
        self._repr = ''
        self._container = None

        # Increase the creation counter, and save our local copy.
        self._creation_counter = Constant._creation_counter
        Constant._creation_counter += 1

    def _post_init(self, container, name):
        """
        Called automatically by container after container's class construction.
        """
        self.name = name
        self._repr = _constant_repr("{0}.{1}".format(container.__name__, name))
        self._container = container

    def to_group(self, group_class, **group_members):
        return _LazyConstantsGroup(self, group_class, **group_members)

    def _merge_into_group(self, group):
        """
        Called automatically by container after group construction.
        """
        group._creation_counter = self._creation_counter

    def __repr__(self):
        """
        Return text identifying both which constant this is and which
        collection it belongs to.
        """
        return self._repr


class _ConstantsContainerMeta(type):
    """
    Metaclass for creating constants container classes.
    """
    def __new__(self, class_name, bases, attributes):
        cls = super(_ConstantsContainerMeta, self).__new__(
            self, class_name, bases, attributes)

        constant_class = getattr(cls, 'constant_class', None)

        if constant_class is None:
            return cls
        elif not issubclass(constant_class, Constant):
            raise TypeError(
                "Constant class {0} must be derived from {1}".format(
                 constant_class.__name__, Constant.__name__))

        constants = []
        for name, obj in list(six.iteritems(attributes)):
            if isinstance(obj, _LazyConstantsGroup):
                new_obj = obj._evaluate(cls, name)
                del obj.constant
                setattr(cls, name, new_obj)
                constants.append((name, new_obj))
            elif isinstance(obj, constant_class):
                if obj._container is not None:
                    raise ValueError(
                        "Cannot use {0} as the value of an attribute {1} on {2}"
                        .format(obj, name, cls.__name__))
                obj._post_init(cls, name)
                constants.append((name, obj))

        constants.sort(key=lambda name_obj: name_obj[1]._creation_counter)
        cls._constants = OrderedDict(constants)
        return cls


@six.add_metaclass(_ConstantsContainerMeta)
class ConstantsContainer(object):
    """
    Base class for creating constants containers. Each constant defined within
    container will remember it's creation order. See an example in
    :meth:`iterconstants`.

    :cvar constant_class: stores a class of constants which can be stored by
                          container. This attribute **MUST** be set up manually
                          when you define a new container type. Otherwise
                          container will not be initialized. Default: ``None``
    :raises TypeError: if you try to create an instance of container.
                       Containers are singletons and they cannot be
                       instantiated. Their attributes must be used directly.
    """

    #: Holds a class of constants which can be stored by container
    constant_class = None

    def __new__(cls):
        """
        Classes representing constants containers are not intended to be
        instantiated.

        The class object itself is used directly.
        """
        raise TypeError("'{0}' may not be instantiated".format(cls.__name__))

    @classmethod
    def contains(cls, item):
        return item in cls.names()

    @classmethod
    def names(cls):
        return list(cls.internames())

    @classmethod
    def internames(cls):
        return six.iterkeys(cls._constants)

    @classmethod
    def constants(cls):
        return list(cls.iterconstants())

    @classmethod
    def iterconstants(cls):
        """
        Get generator for iterating all constants in container.

        :returns: a generator for iterating container's constants. Constants
                  will appear in the order they were defined.
        :rtype: :class:`generator`

        **Example**::

            >>> from candv.base import Constant, ConstantsContainer
            >>> class FOO(ConstantsContainer):
            ...     constant_class = Constant
            ...     foo = Constant()
            ...     bar = Constant()
            ...
            >>> [x.name for x in FOO.iterconstants()]
            ['foo', 'bar']
        """
        return six.itervalues(cls._constants)

    @classmethod
    def items(cls):
        return list(cls.iteritems())

    @classmethod
    def iteritems(cls):
        return six.iteritems(cls._constants)

    @classmethod
    def get_by_name(cls, name):
        """
        Try to get constant by it's name.

        :param str name: name of constant to search for

        :returns: a constant
        :rtype: a class specified by :attr:`constant_class` which is :class:`Constant` or it's subclass

        :raises KeyError: if constant name ``name`` is not present in
                          container

        **Example**::

            >>> from candv.base import Constant, ConstantsContainer
            >>> class FOO(ConstantsContainer):
            ...     constant_class = Constant
            ...     foo = Constant()
            ...     bar = Constant()
            ...
            >>> FOO.get_by_name('foo')
            <constant 'FOO.foo'>
        """
        try:
            return cls._constants[name]
        except KeyError:
            raise KeyError("Constant with name '{0}' is not present in '{1}'"
                           .format(name, cls.__name__))
