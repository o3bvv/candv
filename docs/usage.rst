Usage
=====

The main idea is that ``constants`` are *instances* of
:class:`~candv.base.Constant` class (or its subclasses) and they are stored
inside *subclasses* of :class:`~candv.base.ConstantsContainer` class which are
called ``containers``.

Every constant has its own name which is equal to the name of container's
attribure they are assigned to. Every container is a singleton, i.e. you just
need to define container's class and use it. You are not permitted to create
instances of containers. This is unnecessary. Containers have class methods
for accessing constants in different ways.

Constants remember the order they were defined inside container.

Constants may have custom attributes and methods. Containers may have custom
class methods. :doc:`See customization docs<customization>`.

Constants may be converted into groups of constants providing ability to create
different constant hierarchies (:ref:`see Hierarchies <hierarchies>`).


.. _usage_simple_constants:

Simple constants
----------------

Simple constants are really simple. They look like `enumerations in Python 3.4 <https://docs.python.org/3/library/enum.html>`_::

    >>> from candv import SimpleConstant, Constants
    >>> class STATUS(Constants):
    ...     SUCCESS = SimpleConstant()
    ...     FAILURE = SimpleConstant()
    ...

And they can be used just like enumerations.

Here ``STATUS`` is a subclass of :class:`candv.Constants`. The latter can
contain any instances of :class:`candv.SimpleConstant` class or its subclasses.

.. note::

    ``candv.SimpleConstant`` and ``candv.Constants`` are aliases for
    :class:`candv.base.Constant` and :class:`candv.base.ConstantsContainer`
    respectively.

``STATUS`` is a container::

    >>> STATUS
    <constants container 'STATUS'>

All containers have the following attributes::

    >>> STATUS.name
    'STATUS'
    >>> STATUS.full_name
    'STATUS'

They have an API which is similar to the API of Python's :class:`dict` (in the
mater of accessing its members):

::

    >>> len(STATUS)
    2
    >>> 'SUCCESS' in STATUS
    True
    >>> STATUS.has_name('PENDING')
    False
    >>> STATUS.names()
    ['SUCCESS', 'FAILURE']
    >>> STATUS.constants()
    [<constant 'STATUS.SUCCESS'>, <constant 'STATUS.FAILURE'>]
    >>> STATUS.items()
    [('SUCCESS', <constant 'STATUS.SUCCESS'>), ('FAILURE', <constant 'STATUS.FAILURE'>)]
    >>> STATUS['FAILURE']
    <constant 'STATUS.FAILURE'>
    >>> STATUS.get('XXX', 999)
    999

.. note::

    Since 1.1.2 you can list constants and get the same result by calling
    :meth:`~candv.base.ConstantsContainer.values` and
    :meth:`~candv.base.ConstantsContainer.itervalues` also. Take into account,
    those methods are overridden in :class:`~candv.Values` (see section below).

Also, you can access constants directly::

    >>> STATUS.SUCCESS
    <constant 'STATUS.SUCCESS'>

And access its attributes::

    >>> STATUS.SUCCESS.name
    'SUCCESS'
    >>> STATUS.SUCCESS.full_name
    'STATUS.SUCCESS'
    >>> STATUS.SUCCESS.container
    <constants container 'STATUS'>


.. _usage_valued_constants:

Constants with values
---------------------

Constants with values behave like simple constants, except they can have any
object attached to them as a value. It's something like an ordered dictionary::

    >>> from candv import ValueConstant, Values
    >>> class TEAMS(Values):
    ...     NONE = ValueConstant('#EEE')
    ...     RED = ValueConstant('#F00')
    ...     BLUE = ValueConstant('#00F')
    ...

Here ``TEAMS`` is a subclass of :class:`~candv.Values`, which is a more
specialized container than :class:`~candv.Constants`. As you may guessed,
:class:`~candv.ValueConstant` is a more specialized constant class than
``SimpleConstant`` and its instances have own values.

.. note::

    ``Values`` and its subclasses treat as constants only instances of ``ValueConstant`` or its sublasses::

        >>> class UNBOUND_CONSTANTS(Values):
        ...     FOO = SimpleConstant()
        ...     BAR = SimpleConstant()
        ...

    Here ``UNBOUND_CONSTANTS`` container contains 2 instances of
    ``SimpleConstant``, which is more gerenal then ``ValueConstant``. It's not an
    error, but those 2 constants will be invisible for the container::

        >>> UNBOUND_CONSTANTS.constants()
        []
        >>> UNBOUND_CONSTANTS.FOO
        <constant '__UNBOUND__.FOO'>

So, ``TEAMS`` is just another container::

    >>> TEAMS
    <constants container 'TEAMS'>

It has extra methods for working with valued constants. For example, you can
list all values::

    >>> TEAMS.values()
    ['#EEE', '#F00', '#00F']

.. note::

    Since 1.1.2 methods :meth:`~candv.Values.values` and
    :meth:`~candv.Values.itervalues` from :class:`~candv.Values` override
    methods :meth:`~candv.base.ConstantsContainer.values` and
    :meth:`~candv.base.ConstantsContainer.itervalues` from
    :class:`~candv.base.ConstantsContainer` accordingly.

And you can get a constant by its value::

    >>> TEAMS.get_by_value('#F00')
    <constant 'TEAMS.RED'>


If you have different constants with equal values, it's OK anyway::

    >>> class FOO(Values):
    ...     ATTR1 = ValueConstant('one')
    ...     ATTRX = ValueConstant('x')
    ...     ATTR2 = ValueConstant('two')
    ...     ATTR1_DUB = ValueConstant('one')
    ...

Here ``FOO.ATTR1`` and ``FOO.ATTR1_DUB`` have identical values. In this case
method :meth:`~candv.Values.get_by_value` will return first constant with given
value::

    >>> FOO.get_by_value('one')
    <constant 'FOO.ATTR1'>

If you need to get all constants with same value, use
:meth:`~candv.Values.filter_by_value` method instead::

    >>> FOO.filter_by_value('one')
    [<constant 'FOO.ATTR1'>, <constant 'FOO.ATTR1_DUB'>]

And of course, you can access values of constants:

    >>> TEAMS.RED.value
    '#F00'

.. todo::


.. _usage_verbose_constants:

Verbose constants
-----------------

How often do you do things like below?

    >>> TYPE_FOO = 'foo'
    >>> TYPE_BAR = 'bar'
    >>> TYPES = (
    ...     (TYPE_FOO, "Some foo constant"),
    ...     (TYPE_BAR, "Some bar constant"),
    ... )

This is usually done to add verbose names to constants which you can use
somewhere, e.g in HTML template:

.. code-block:: jinja

    <select>
    {% for code, name in TYPES %}
      <option value='{{ code }}'>{{ name }}</option>
    {% endfor %}
    </select>

Okay. How about adding help text? Extend tuples? Or maybe create some
``TYPES_DESCRIPTIONS`` tuple? How far can you go and how ugly can you make it?
Well, spare yourself from headache and use verbose constants
:class:`~candv.VerboseConstant` and :class:`~candv.VerboseValueConstant`::

    >>> from candv import VerboseConstant, Constants
    >>> class TYPES(Constants):
    ...     FOO = VerboseConstant("Some foo constant", "help")
    ...     BAR = VerboseConstant(verbose_name="Some bar constant",
    ...                           help_text="some help")

Here you can access ``verbose_name`` and ``help_text`` attributes of
constants::

    >>> TYPES.FOO.verbose_name
    'Some foo constant'
    >>> TYPES.FOO.help_text
    'help'

Now you can rewrite your code:

.. code-block:: jinja

    <select>
    {% for constant in TYPES.constants() %}
      <option value='{{ constant.name }}' title='{{ constant.help_text }}'>
        {{ constant.verbose_name }}
      </option>
    {% endfor %}
    </select>

Same thing with values, just use ``VerboseValueConstant``::

    >>> from candv import VerboseValueConstant, Values
    >>> class TYPES(Values):
    ...     FOO = VerboseValueConstant('foo', "Some foo constant", "help")
    ...     BAR = VerboseValueConstant('bar', verbose_name="Some bar constant",
    ...                                       help_text="some help")
    ...
    >>> TYPES.FOO.value
    'foo'
    >>> TYPES.FOO.verbose_name
    'Some foo constant'
    >>> TYPES.FOO.help_text
    'help'

Our sample HTML block will look almost the same and will use ``value``
attribute:

.. code-block:: jinja

    <select>
    {% for constant in TYPES.constants() %}
      <option value='{{ constant.value }}' title='{{ constant.help_text }}'>
        {{ constant.verbose_name }}
      </option>
    {% endfor %}
    </select>


.. _hierarchies:

Hierarchies
-----------

**candv** library supports direct attaching of a group of constants to another
constant to create hierarchies. A group can be created from any constant and
any container can be used to store children. You may already saw this in the
:ref:`introduction chapter <complex-example>`, but let's examine simple
example::

    >>> from candv import Constants, SimpleConstant
    >>> class TREE(Constants):
    ...     LEFT = SimpleConstant().to_group(Constants,
    ...         LEFT=SimpleConstant(),
    ...         RIGHT=SimpleConstant(),
    ...     )
    ...     RIGHT = SimpleConstant().to_group(Constants,
    ...         LEFT=SimpleConstant(),
    ...         RIGHT=SimpleConstant(),
    ...     )
    ...

Here the key point is :meth:`~candv.base.Constant.to_group` method which is
avaivable for every constant. It accepts class that will be used to construct
new container and any number of constant instances passed as keywords. You can
access any group as any usual constant and use it as any usual container at the
same time::

    >>> TREE.LEFT
    <constants group 'TREE.LEFT'>
    >>> TREE.LEFT.name
    'LEFT'
    >>> TREE.LEFT.full_name
    'TREE.LEFT'
    >>> TREE.LEFT.constant_class
    <class 'candv.base.Constant'>
    >>> TREE.LEFT.names()
    ['LEFT', 'RIGHT']
    >>> TREE.LEFT.LEFT
    <constant 'TREE.LEFT.LEFT'>
    >>> TREE.LEFT.LEFT.full_name
    'TREE.LEFT.LEFT'
    >>> TREE.LEFT.LEFT.container
    <constants group 'TREE.LEFT'>


.. _usage_exporting:

Exporting
---------

.. versionadded:: 1.2.1

You can convert constants and containers into Python primitives for further
serialization, for example, into JSON.

Use ``to_primitive()`` method of constants and containers to do that.

Simple constants
~~~~~~~~~~~~~~~~

Let's see how it works with :ref:`simple constants <usage_simple_constants>`::

    >>> STATUS.SUCCESS.to_primitive()
    {'name': 'SUCCESS'}
    >>> STATUS.to_primitive()
    {'items': [{'name': 'SUCCESS'}, {'name': 'FAILURE'}], 'name': 'STATUS'}

By default ``to_primitive()`` returns a :class:`dict` which contains at least
a ``name``. In addition, containers have :class:`list` of their ``items``.

Verbose constants
~~~~~~~~~~~~~~~~~

:ref:`Verbose constants <usage_verbose_constants>` work same way::

    >>> TYPES.FOO.to_primitive()
    {'help_text': 'help', 'verbose_name': 'Some foo constant', 'name': 'FOO'}

Valued constants
~~~~~~~~~~~~~~~~

You can do that with :ref:`valued constants <usage_valued_constants>` as well::

    >>> TEAMS.RED.to_primitive()
    {'name': 'RED', 'value': '#F00'}

.. note::

    Remember: values of constants are out of scope of this library.

    You can use anything as value of your constants, but converting values into
    primitives is almost up to you.

    If your value is ``callable``, ``candv`` will call it to get it's value.
    If your value has ``isoformat()`` method (``date``, ``time``, etc.),
    ``candv`` will call it either. Everything else is supposed to be a
    primitive.

    It is unlikely that you will use something complex, but if you will, than
    it's strongly recommended to implement
    :ref:`a custom constant class <customization>` with
    :ref:`custom support of exporting <customization_exporting>`.

Hierarchies
~~~~~~~~~~~

Hierarchies can be converted to primitives also::

    >>> class FOO(Constants):
    ...     A = SimpleConstant()
    ...     B = VerboseValueConstant(
    ...         value=10,
    ...         verbose_name="Constant B",
    ...         help_text="Just a group with verbose name"
    ...     ).to_group(
    ...         group_class=Constants,
    ...         C=SimpleConstant(),
    ...         D=SimpleConstant(),
    ...     )
    ...
    >>> from pprint import pprint
    >>> pprint(FOO.B.to_primitive())
        {'help_text': 'Just a group with verbose name',
         'items': [{'name': 'C'}, {'name': 'D'}],
         'name': 'B',
         'value': 10,
         'verbose_name': 'Constant B'}

As you can see, result is a mix of constant and container.
