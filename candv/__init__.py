# -*- coding: utf-8 -*-
"""
This module provides ready-to-use classes for constructing custom constants.
"""
from candv.base import (Constant as SimpleConstant,
    ConstantsContainer as _BaseContainer)


class VerboseMixin(object):
    """
    Provides support of verbose names and help texts. Must be placed at the
    left side of non-mixin base classes due to Python's MRO. Arguments must be
    passed as kwargs.

    :argument str verbose_name: optional verbose name
    :argument str help_text: optional description

    **Example**::

        class Foo(object):

            def __init__(self, arg1, arg2, kwarg1=None):
                pass


        class Bar(VerboseMixin, Foo):

            def __init__(self, arg1, arg2, verbose_name=None, help_text=None, kwarg1=None):
                super(Bar, self).__init__(arg1, arg2, verbose_name=verbose_name, help_text=help_text, kwarg1=kwarg1)

    """
    def __init__(self, *args, **kwargs):
        self.verbose_name = kwargs.pop('verbose_name', None)
        self.help_text = kwargs.pop('help_text', None)
        super(VerboseMixin, self).__init__(*args, **kwargs)

    def merge_into_group(self, group):
        """
        Redefines :meth:`~candv.base.Constant.merge_into_group` and adds
        ``verbose_name`` and ``help_text`` attributes to the target group.
        """
        super(VerboseMixin, self).merge_into_group(group)
        group.verbose_name = self.verbose_name
        group.help_text = self.help_text


class VerboseConstant(VerboseMixin, SimpleConstant):
    """
    Constant with optional verbose name and optional description.

    :argument str verbose_name: optional verbose name of the constant
    :argument str help_text: optional description of the constant

    :ivar str verbose_name: verbose name of the constant. Default: ``None``
    :ivar str help_text: verbose description of the constant. Default: ``None``
    """
    def __init__(self, verbose_name=None, help_text=None):
        super(VerboseConstant, self).__init__(verbose_name=verbose_name,
                                              help_text=help_text)


class Constants(_BaseContainer):
    """
    Simple container for any :class:`~candv.base.Constant` or it's subclass.
    This container can be used as enumeration.

    **Example**::

        >>> from candv import Constants, SimpleConstant
        >>> class USER_ROLES(Constants):
        ...     ADMIN = SimpleConstant()
        ...     ANONYMOUS = SimpleConstant()
        ...
        >>> USER_ROLES.ADMIN
        <constant 'USER_ROLES.ADMIN'>
        >>> USER_ROLES.get_by_name('ANONYMOUS')
        <constant 'USER_ROLES.ANONYMOUS'>
    """
    #: Set :class:`~candv.base.Constant` as top-level class for this container.
    #: See :attr:`~candv.base.ConstantsContainer.constant_class`.
    constant_class = SimpleConstant


class ValueConstant(SimpleConstant):
    """
    Extended version of :class:`SimpleConstant` which provides support for
    storing values of constants.

    :argument value: a value to attach to constant

    :ivar value: constant's value
    """
    def __init__(self, value):
        super(ValueConstant, self).__init__()
        self.value = value

    def merge_into_group(self, group):
        """
        Redefines :meth:`~candv.base.Constant.merge_into_group` and adds
        ``value`` attribute to the target group.
        """
        super(ValueConstant, self).merge_into_group(group)
        group.value = self.value


class VerboseValueConstant(VerboseMixin, ValueConstant):
    """
    A constant which can have both verbose name, help text and a value.

    :argument value: a value to attach to the constant
    :argument str verbose_name: optional verbose name of the constant
    :argument str help_text: optional description of the constant

    :ivar value: constant's value
    :ivar str verbose_name: verbose name of the constant. Default: ``None``
    :ivar str help_text: verbose description of the constant. Default: ``None``
    """
    def __init__(self, value, verbose_name=None, help_text=None):
        super(VerboseValueConstant, self).__init__(value,
                                                   verbose_name=verbose_name,
                                                   help_text=help_text)


class Values(_BaseContainer):
    """
    Constants container which supports getting and filtering constants by their
    values, listing values of all constants in container.
    """
    #: Set :class:`ValueConstant` as top-level class for this container.
    #: See :attr:`~candv.base.ConstantsContainer.constant_class`.
    constant_class = ValueConstant

    @classmethod
    def get_by_value(cls, value):
        """
        Get constant by its value.

        :param value: value of the constant to look for
        :returns: first found constant with given value
        :raises ValueError: if no constant in container has given value
        """
        for constant in cls.iterconstants():
            if constant.value == value:
                return constant
        raise ValueError("Value '{0}' is not present in '{1}'".format(
                         value, cls.__name__))

    @classmethod
    def filter_by_value(cls, value):
        """
        Get all constants which have given value.

        :param value: value of the constants to look for
        :returns: list of all found constants with given value
        """
        constants = []
        for constant in cls.iterconstants():
            if constant.value == value:
                constants.append(constant)
        return constants

    @classmethod
    def values(cls):
        """
        List values of all constants in the order they were defined.

        :returns: :class:`list` of values

        **Example**::

            >>> from candv import Values, ValueConstant
            >>> class FOO(Values):
            ...     TWO = ValueConstant(2)
            ...     ONE = ValueConstant(1)
            ...     SOME = ValueConstant("some string")
            ...
            >>> FOO.values()
            [2, 1, 'some string']
        """
        return [x.value for x in cls.iterconstants()]

    @classmethod
    def itervalues(cls):
        """
        Same as :meth:`values` but returns an interator.
        """
        for constant in cls.iterconstants():
            yield constant.value


class Choices(_BaseContainer):
    """
    Container of instances of :class:`VerboseConstant` and it's subclasses.

    Provides support for building `Django-compatible <https://docs.djangoproject.com/en/1.6/ref/models/fields/#choices>`_
    choices.
    """
    #: Set :class:`VerboseConstant` as top-level class for this container.
    #: See :attr:`~candv.base.ConstantsContainer.constant_class`.
    constant_class = VerboseConstant

    @classmethod
    def choices(cls):
        """
        Get a tuple of tuples representing constant's name and its verbose name.

        :returns: a tuple of constant's names and their verbose names in order
                  they were defined.

        **Example**::

            >>> from candv import Choices, VerboseConstant
            >>> class FOO(Choices):
            ...     ONE = VerboseConstant("first", help_text="first choice")
            ...     FOUR = VerboseConstant("fourth")
            ...     THREE = VerboseConstant("third")
            ...
            >>> FOO.choices()
            (('ONE', 'first'), ('FOUR', 'fourth'), ('THREE', 'third'))
            >>> FOO.get_by_name('ONE').help_text
            'first choice'
        """
        return tuple((name, x.verbose_name) for name, x in cls.items())
