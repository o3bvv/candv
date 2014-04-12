# -*- coding: utf-8 -*-
from candv.base import (Constant as SimpleConstant,
    ConstantsContainer as _BaseContainer)


class VerboseConstant(SimpleConstant):
    """
    Constant with optional verbose name and optional description.

    :argument str verbose_name: optional verbose name of the constant
    :argument str help_text: optional description of the constant

    :ivar str verbose_name: verbose name of the constant. Default: ``None``
    :ivar str help_text: verbose description of the constant. Default: ``None``
    """
    def __init__(self, verbose_name=None, help_text=None):
        super(VerboseConstant, self).__init__()
        self.verbose_name = verbose_name
        self.help_text = help_text


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
        >>> USER_ROLES.find_by_name('ANONYMOUS')
        <constant 'USER_ROLES.ANONYMOUS'>
    """
    constant_class = SimpleConstant
