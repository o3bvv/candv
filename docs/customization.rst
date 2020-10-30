.. _customization:

Customization
=============

It is possible to create custom classes of constant and of containers if standard functionality is not enough.


Custom definitions
------------------

There are several reasons why one would need to create a custom class of constants. For example:

* A need to vividly define a type of constants tracked by a certain container.
* A need to add extra methods to constants.
* A need to add extra attributes to constants.


Custom constants can be created simply by subclassing one of existing classes of constants, e.g.:

.. code-block:: python
  :linenos:

  from candv import SimpleConstant

  class SupportedLanguage(SimpleConstant):
    ...


Here, ``SupportedLanguage`` is quite ready to be used, e.g.:

.. code-block:: python
  :linenos:
  :lineno-start: 5

  from candv import Constants


  class SupportedLanguages(Constants):
    en = SupportedLanguage()
    fr = SupportedLanguage()


Despite ``SupportedLanguages`` is a valid container, it does not enforce which constants are its valid members. For example, it's still possible to use other constants:

.. code-block:: python
  :linenos:
  :lineno-start: 11

  class SupportedLanguages(Constants):
    en = SupportedLanguage()
    fr = SupportedLanguage()

    xx = SimpleConstant()


Here, all constants will be visible to the container:

.. code-block:: python
  :linenos:
  :lineno-start: 16

  >>> SupportedLanguages.names()
  ['en', 'fr', 'xx']


If a container has methods relying on custom attributes of its members, such behavior might become troublesome.

One should specify ``constant_class`` attribute in order to explicitly define constants supported by a container. So, a bit more correct definition would be:

.. code-block:: python
  :linenos:
  :lineno-start: 18
  :emphasize-lines: 2

  class SupportedLanguages(Constants):
    constant_class = SupportedLanguage

    en = SupportedLanguage()
    fr = SupportedLanguage()


As a result, any constants except ``SupportedLanguage`` and its derivatives will be ignored:

.. code-block:: python
  :linenos:
  :lineno-start: 23

  class SupportedLanguages(Constants):
    constant_class = SupportedLanguage

    en = SupportedLanguage()
    fr = SupportedLanguage()

    xx = SimpleConstant()


.. code-block:: python
  :linenos:
  :lineno-start: 30

  >>> SupportedLanguages.names()
  ['en', 'fr']


As definitions of the ``constant_class`` attribute may clutter definitions of classes, it's possible to lift them out of class bodies using a helper :meth:`~candv.with_constant_class`:

.. code-block:: python
  :linenos:
  :lineno-start: 32
  :emphasize-lines: 4

  from candv import with_constant_class


  class SupportedLanguages(with_constant_class(SupportedLanguage), Constants):
    en = SupportedLanguage()
    fr = SupportedLanguage()


Of course, it's possible to add custom methods and attributes to both constants and containers.

For example, the following constants allow formatting and parsing of operations having opcodes:

.. code-block:: python
  :linenos:
  :emphasize-lines: 8-11,18-23

  from candv import ValueConstant
  from candv import Values
  from candv import with_constant_class


  class Opcode(ValueConstant):

    def compose(self, *args):
      chunks = [self.value, ]
      chunks.extend(args)
      return '/'.join(map(str, chunks))


  class OPERATIONS(with_constant_class(Opcode), Values):
    REQ = Opcode(100)
    ACK = Opcode(200)

    @classmethod
    def decompose(cls, value):
      chunks = value.split('/')
      opcode = int(chunks.pop(0))
      constant = cls.get_by_value(opcode)
      return constant, chunks


Example usage of such constants is defined as follows.

.. code-block:: python
  :linenos:
  :lineno-start: 24

  >>> OPERATIONS.ACK.compose(1, 2, 'foo')
  '200/1/2/foo'

  >>> OPERATIONS.decompose('200/1/2/foo')
  (<constant 'OPERATIONS.ACK'>, ['1', '2', 'foo'])


The point here is to show that it is possible to add arbitrary attributes and logic to constants if really needed.


Adding verbosity
----------------

If custom constants need to have human-friendly attributes provided by :class:`~candv.VerboseConstant`, they can be added by :class:`~candv.VerboseMixin`:

.. code-block:: python
  :linenos:

  from candv import SimpleConstant
  from candv import VerboseMixin


  class CustomConstant(VerboseMixin, SimpleConstant):

      def __init__(self, arg1, agr2, verbose_name=None, help_text=None):
        super().__init__(
          verbose_name=verbose_name,
          help_text=help_text,
        )
        self.arg1 = arg1
        self.arg2 = arg2

.. note::

  Here, ``verbose_name`` and ``help_text`` attributes must be passed as keyword arguments during ``super().__init__()`` call.


.. _customization_to_primitives:

Custom conversion to primitives
-------------------------------

Custom constants which have complex attributes may need to define custom logic for converting their attributes into primitives. This is primarily needed for serialization, say, into JSON.

One has to override ``to_primitive()`` method to define custom conversion logic. For example:

.. code-block:: python
  :linenos:
  :emphasize-lines: 15-21

  from fractions import Fraction
  from pprint import pprint

  from candv import Constants
  from candv import SimpleConstant
  from candv import with_constant_class


  class FractionConstant(SimpleConstant):

    def __init__(self, value):
      super().__init__()
      self.value = value

    def to_primitive(self, context=None):
      primitive = super().to_primitive(context)
      primitive.update({
        'numerator':   self.value.numerator,
        'denominator': self.value.denominator
      })
      return primitive


  class Fractions(with_constant_class(FractionConstant), Constants):
    one_half  = FractionConstant(Fraction(1, 2))
    one_third = FractionConstant(Fraction(1, 3))

.. code-block:: python
  :linenos:
  :lineno-start: 26

  >>> Fractions.one_half.to_primitive()
  {'name': 'one_half', 'numerator': 1, 'denominator': 2}

  >>> pprint(Fractions.to_primitive())
  {'items': [{'denominator': 2, 'name': 'one_half', 'numerator': 1},
             {'denominator': 3, 'name': 'one_third', 'numerator': 1}],
   'name': 'Fractions'}


The plot in a nutshell:

  #. Define ``to_primitive()`` method which accepts an optional ``context`` argument.
  #. Call parent's method and get a primitive.
  #. Update that primitive with custom data which may depend on the context.
  #. Return the updated primitive.


The same can be applied to :ref:`custom constant containers <custom_containers>`
as well.


Hierarchies
-----------

Hierarchies are made by creating groups from constants objects. Since groups are created dynamically, original attributes and methods of constants have to be supplied to groups.

This can be done by overriding :meth:`~candv.SimpleConstant.merge_into_group` method. For example:

.. code-block:: python
  :linenos:
  :emphasize-lines: 13-15

  from candv import Values
  from candv import ValueConstant


  class Opcode(ValueConstant):

    # custom method that also needs to be available in groups
    def compose(self, *args):
      chunks = [self.value, ]
      chunks.extend(args)
      return '/'.join(map(str, chunks))

    def merge_into_group(self, group):
      super().merge_into_group(group)
      group.compose = self.compose


.. code-block:: python
  :linenos:
  :lineno-start: 16

  class FOO(Values):
    BAR = Opcode(300).to_group(Values,
      BAZ = Opcode(301),
    )


.. code-block:: python
  :linenos:
  :lineno-start: 20

  >>> FOO.BAR.compose(1, 2, 3)
  '300/1/2/3'

  >>> FOO.BAR.BAZ.compose(5, 6)
  '301/5/6'

Here, the overridden method :meth:`~candv.SimpleConstant.merge_into_group` calls the original method of the
base class and adds a new ``compose`` attribute to the group.

In this simple case the attribute is a reference to the ``compose()`` method of the custom ``Opcode`` class.

.. warning::

  Attaching methods of existing objects to another objects can be not a good idea.

  Consider using method factories or at least lambdas.
