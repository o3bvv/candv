# -*- coding: utf-8 -*-
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
    constant_class = SimpleConstant


class ValueConstant(SimpleConstant):

    def __init__(self, value):
        super(ValueConstant, self).__init__()
        self.value = value

    def merge_into_group(self, group):
        super(ValueConstant, self).merge_into_group(group)
        group.value = self.value


class VerboseValueConstant(VerboseMixin, ValueConstant):

    def __init__(self, value, verbose_name=None, help_text=None):
        super(VerboseValueConstant, self).__init__(value,
                                                   verbose_name=verbose_name,
                                                   help_text=help_text)


class Values(_BaseContainer):

    constant_class = ValueConstant

    @classmethod
    def get_by_value(cls, value):
        for constant in cls.iterconstants():
            if constant.value == value:
                return constant
        raise ValueError("Value '{0}' is not present in '{1}'".format(
                         value, cls.__name__))

    @classmethod
    def filter_by_value(cls, value):
        constants = []
        for constant in cls.iterconstants():
            if constant.value == value:
                constants.append(constant)
        return constants

    @classmethod
    def values(cls):
        return [x.value for x in cls.iterconstants()]

    @classmethod
    def itervalues(cls):
        for constant in cls.iterconstants():
            yield constant.value


class Choices(_BaseContainer):

    constant_class = VerboseConstant

    @classmethod
    def choices(cls):
        return tuple((name, x.verbose_name) for name, x in cls.items())
