.. _customization:

Customization
=============

If all you've seen before is not enough for you, then you can create your own
constants and containers for them. Let's see some examples.


Custom constants
----------------

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

    >>> from candv import Values
    >>> class OPERATIONS(Values):
    ...     REQ = Opcode(100)
    ...     ACK = Opcode(200)
    ...
    >>> OPERATIONS.REQ.compose(1, 2, 3, 4, 5)
    '100/1/2/3/4/5'


Adding support of groups
------------------------

Well, everything looks fine. But what about creating a group from our new
constants?

.. note:: If you don't know what this means, see :ref:`hierarchies`.

So, firstly, let's create some constant::

    >>> class FOO(Values):
    ...     BAR = Opcode(300).to_group(Values,
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
    >>> class FOO(Values):
    ...     BAR = Opcode(300).to_group(Values,
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
    Maybe it will be better for you to use some *lambda* or to define some
    method within ``merge_into_group``.

.. _customization_exporting:

Adding support of exporting
---------------------------

If your constant stores some complex objects, then it's strongly recommended
to provide support of exporting for them (see :ref:`usage_exporting`).

Do do that, you need to define ``to_primitive()`` method for your class.
Example::

    >>> from fractions import Fraction
    >>> from pprint import pprint
    >>> from candv import SimpleConstant, Constants
    >>>
    >>> class FractionConstant(SimpleConstant):
    ...     def __init__(self, value):
    ...         super(FractionConstant, self).__init__()
    ...         self.value = value
    ...
    ...     def to_primitive(self, context=None):
    ...         primitive = super(FractionConstant, self).to_primitive(context)
    ...         primitive.update({
    ...                'numerator': self.value.numerator,
    ...                'denominator': self.value.denominator
    ...         })
    ...         return primitive
    ...
    >>> class Fractions(Constants):
    ...     one_half = FractionConstant(Fraction(1, 2))
    ...     one_third = FractionConstant(Fraction(1, 3))
    ...
    >>> Fractions.one_half.to_primitive()
    {'denominator': 2, 'numerator': 1, 'name': 'one_half'}
    >>> pprint(Fractions.to_primitive())
    {'items': [{'denominator': 2, 'name': 'one_half', 'numerator': 1},
               {'denominator': 3, 'name': 'one_third', 'numerator': 1}],
     'name': 'Fractions'}

.. note::

    This example is quite hypothetical and it's intended just to show
    implementation of custom ``to_primitive()`` method.

The plot in a nutshell:

    #. Define ``to_primitive()`` method which accepts ``context`` argument.
    #. Call parent's method and get primitive.
    #. Update that primitive with your data, which may depend on context.
    #. Return updated primitive.

Same can be applied to :ref:`custom constant containers <custom_containers>`
as well.


Adding verbosity
----------------

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

.. note::

    Here note, that during call of ``__init__`` method of the super class, you
    need to pass ``verbose_name`` and ``help_text`` as keyword arguments.


.. _custom_containers:

Custom containers
-----------------

To define own container, just derive new class from existing containers, e.g.
from :class:`~candv.Constants` or :class:`~candv.Values`::

    >>> class FOO(Values):
    ...     constant_class = Opcode
    ...
    ...     @classmethod
    ...     def compose_all(cls, *args):
    ...         return '!'.join(map(lambda x: x.compose(*args), cls.constants()))
    ...

Here ``constant_class`` attribute defines top-level class of constants.
Instances whose class is more general than ``constant_class`` will be invisible
to container (see :attr:`~candv.base.ConstantsContainer.constant_class`). Our
new method ``compose_all`` just joins compositions of all its opcodes.

.. note::

    Since *1.2.0* you can use :meth:`~candv.base.with_constant_class` mixin
    factory to make definitions of your containers more readable, e.g.::

        >>> from candv import with_constant_class
        >>> class FOO(with_constant_class(Opcode), Values):
        ...
        ...     @classmethod
        ...     def compose_all(cls, *args):
        ...         return '!'.join(map(lambda x: x.compose(*args), cls.constants()))
        ...

    This will produce the same class as above.

Now it's time to use new container::

    >>> class BAR(FOO):
    ...     REQ = Opcode(1)
    ...     ACK = Opcode(2)
    ...
    ...     @classmethod
    ...     def decompose(cls, value):
    ...         chunks = value.split('/')
    ...         opcode = int(chunks.pop(0))
    ...         constant = cls.get_by_value(opcode)
    ...         return constant, chunks

Here we add new method ``decompose`` which takes a string and decomposes it
into tuple of opcode constant and its arguments. Let's test our conainer::

    >>> BAR.compose_all(500, 600, 700)
    '1/500/600/700!2/500/600/700'
    >>> BAR.decompose('1/100/200')
    (<constant 'BAR.REQ'>, ['100', '200'])

Seems to be OK.
