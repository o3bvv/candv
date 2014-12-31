# -*- coding: utf-8 -*-
"""
This module provides ready-to-use classes for constructing custom constants.
"""

import six

from .base import (
    Constant as SimpleConstant, ConstantsContainer as Constants,
    with_constant_class,
)


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

    def to_primitive(self, context=None):
        """
        .. versionadded:: 1.3.0
        """
        primitive = super(VerboseMixin, self).to_primitive(context)
        to_text = lambda x: six.text_type(x) if x is not None else x
        primitive.update({
            'verbose_name': to_text(self.verbose_name),
            'help_text': to_text(self.help_text),
        })
        return primitive


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

    def to_primitive(self, context=None):
        """
        .. versionadded:: 1.3.0
        """
        primitive = super(ValueConstant, self).to_primitive(context)
        value = self.value

        if hasattr(value, 'isoformat'):
            value = value.isoformat()
        elif callable(value):
            value = value()

        primitive['value'] = value
        return primitive


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


class Values(with_constant_class(ValueConstant), Constants):
    """
    Constants container which supports getting and filtering constants by their
    values, listing values of all constants in container.
    """

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
        raise ValueError(
            "Constant with value \"{0}\" is not present in \"{1}\""
            .format(value, cls)
        )

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

        .. note::

            Overrides :meth:`~candv.base.ConstantsContainer.values` since
            1.1.2.
        """
        return [x.value for x in cls.iterconstants()]

    @classmethod
    def itervalues(cls):
        """
        Same as :meth:`values` but returns an interator.

        .. note::

            Overrides :meth:`~candv.base.ConstantsContainer.itervalues` since
            1.1.2.
        """
        for constant in cls.iterconstants():
            yield constant.value
