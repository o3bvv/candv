Customization
=============

If all you've seen before is not enough for you, then you can create your own
constants and containers for them. Let's see some examples.

Custom constants
^^^^^^^^^^^^^^^^

Imagine you need to create some constant class. For example, you need to define
some operation codes and have ability to create come commands with arguments::

    >>> from candv import ValueConstant
    >>> class Opcode(ValueConstant):
    ...     def compose(self, *args):
    ...         chunks = [self.value, ]
    ...         chunks.extend(args)
    ...         return '/'.join(map(str, chunks))
    ...

So, just a class with a method. Nothing special. You can use it right now::

    >>> from candv import Constants
    >>> class OPERATIONS(Constants):
    ...     REQ = Opcode(100)
    ...     ACK = Opcode(200)
    ...
    >>> OPERATIONS.REQ.compose(1, 9, 3, 2, 0)
    '100/1/9/3/2/0'

Providing groups support
^^^^^^^^^^^^^^^^^^^^^^^^

Well, everything looks fine. But what about creating a group from our new
constants? First, let's create some::

    >>> class FOO(Constants):
    ...     BAR = Opcode(300).to_group(Constants,
    ...         BAZ = Opcode(301),
    ...     )

And now let's check it:

    >>> FOO.BAR.compose(1, 2, 3)
    Traceback (most recent call last):
      File "<input>", line 1, in <module>
    AttributeError: 'FOO.BAR' object has no attribute 'compose'
    >>> FOO.BAR.BAZ.compose(4, 5, 6)
    '301/4/5/6'

Oops! Our newborn group does not have a ``compose`` method. Don't give up!
We will add it easily, but in a special manner. Let's redefine our ``Opcode``
class::

    >>> class Opcode(ValueConstant):
    ...     def compose(self, *args):
    ...         chunks = [self.value, ]
    ...         chunks.extend(args)
    ...         return '/'.join(map(str, chunks))
    ...     def merge_into_group(self, group):
    ...         super(Opcode, self).merge_into_group(group)
    ...         group.compose = self.compose
    ...
    >>> class FOO(Constants):
    ...     BAR = Opcode(300).to_group(Constants,
    ...         BAZ = Opcode(301),
    ...     )
    ...
    >>> FOO.BAR.compose(1, 2, 3)
    '300/1/2/3'

Here the key point is ``merge_into_group`` method, which redefines
:meth:`candv.base.Constant.merge_into_group`. Firstly, it calls method of the
base class, so that internal mechanisms can be initialized. Then it sets a
new attribute ``compose`` which is a reference to ``compose`` method of our
``Opcode`` class.

.. note::

    Be careful with attaching methods of existing objects to another objects.
    Maybe it will be better for you to use some lambda or define somemethod
    within ``merge_into_group``.

Adding verbosity
^^^^^^^^^^^^^^^^

If you need to add verbosity to your constants, just use
:class:`~candv.VerboseMixin` mixin as the first base of your own class::

    >>> from candv import VerboseMixin, SimpleConstant
    >>> class SomeConstant(VerboseMixin, SimpleConstant):
    ...     def __init__(self, arg1, agr2, verbose_name=None, help_text=None):
    ...         super(SomeConstant, self).__init__(verbose_name=verbose_name,
    ...                                            help_text=help_text)
    ...         self.arg1 = arg1
    ...         self.arg2 = arg2
    ...

Here note, that during call of ``__init__`` method of the super class, you
pass ``verbose_name`` and ``help_text`` as keyword arguments.

Custom containers
^^^^^^^^^^^^^^^^^

To define own container, just derive new class from existing containers, e.g.
from :class:`~candv.Constants` or :class:`~candv.Values`::

    >>> class FOO(Values):
    ...     constant_class = Opcode
    ...     @classmethod
    ...     def compose_all(cls, *args):
    ...         return '!'.join(map(lambda x: x.compose(*args), cls.constants()))
    ...

Here ``constant_class`` attribute defines top-level class of constants.
Instances whose class is more general than ``constant_class`` will be invisible
to container (see :attr:`candv.base.ConstantsContainer.constant_class`). Our
new method ``compose_all`` just joins compositions of all its opcodes.

Now it's time to use new container::

    >>> class BAR(FOO):
    ...     REQ = Opcode(1)
    ...     ACK = Opcode(2)
    ...     @classmethod
    ...     def decompose(cls, value):
    ...         chunks = value.split('/')
    ...         opcode = int(chunks.pop(0))
    ...         constant = cls.get_by_value(opcode)
    ...         return constant, chunks

Here we add new method ``decompose`` which takes a string and decomposes it
into tuple of opcode constant and it's arguments. Let's test our conainer::

    >>> BAR.compose_all(1, 9, 30)
    '1/1/9/30!2/1/9/30'
    >>> BAR.decompose('1/100/200')
    (<constant 'BAR.REQ'>, ['100', '200'])

Seems to be OK.
