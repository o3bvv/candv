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
    Base class for all constants.

    :argument str help_text: optional verbose description of the constant

    :ivar str name: constant's name. Is set up automatically and equals to the
                    name of container's attribute
    :ivar str help_text: optional verbose description of the constant.
                         Default: ``None``
    """

    # Tracks each time a Constant instance is created. Used to retain order.
    _creation_counter = 0

    def __init__(self, help_text=None):
        self.help_text = help_text

        # Container which this constant belongs to. Is set up automatically by
        # container.
        self._container = None

        # Name by which constant can be accessed from containter. Is set up
        # automatically by container.
        self._name = None

        # Increase the creation counter, and save our local copy.
        self._creation_counter = Constant._creation_counter
        Constant._creation_counter += 1

    def _post_init(self, container, constant_name):
        """
        Called automatically by container after container's class construction.
        """
        self._container = container
        self.name = constant_name

    def __repr__(self):
        """
        Return text identifying both which constant this is and which
        collection it belongs to.
        """
        return "<constant '{0}.{1}'>".format(self._container.__name__,
                                             self.name)


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

        def verify_object(obj):
            """
            Check if constant does not belong to other containers.
            """
            if obj._container is None:
                return obj
            else:
                raise ValueError(
                    "Cannot use {0} as the value of an attribute on {1}"
                    .format(obj, cls.__name__))

        # Get sorted list of container's constants with their names
        constants = [
            (name, verify_object(obj), )
            for name, obj in list(six.iteritems(attributes))
            if isinstance(obj, constant_class)
        ]
        constants.sort(key=lambda x: x[1]._creation_counter)

        # Finish initialization of constants and store them in internal buffer
        cls._constants = OrderedDict()
        for (name, obj) in constants:
            obj._post_init(container=cls, constant_name=name)
            cls._constants[name] = obj

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
    def iterconstants(cls):
        """
        Get generator for iterating all constants in container.

        :returns: a generator for iterating container's constants. Constants
                  will appear in the order they were defined.
        :rtype: :class:`generator`

        :raises AttributeError: if :attr:`constant_class` was not specified

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
    def find_by_name(cls, name):
        """
        Try to get constant by it's name.

        :param str name: name of constant to search for

        :returns: a constant
        :rtype: a class specified by :attr:`constant_class` which is :class:`Constant` or it's subclass

        :raises KeyError: if constant name ``name`` is not present in
                          container
        :raises AttributeError: if :attr:`constant_class` was not specified

        **Example**::

            >>> from candv.base import Constant, ConstantsContainer
            >>> class FOO(ConstantsContainer):
            ...     constant_class = Constant
            ...     foo = Constant()
            ...     bar = Constant()
            ...
            >>> FOO.find_by_name('foo')
            <constant 'FOO.foo'>
        """
        try:
            return cls._constants[name]
        except KeyError:
            raise KeyError("Constant with name '{0}' is not present in '{1}'"
                           .format(name, cls.__name__))
