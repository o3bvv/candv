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
class methods. See :doc:`customization docs<customization>`.

Constants may be converted into groups of constants providing ability to create
different constant hierarchies (see :ref:`hierarchies`).

Simple constants
^^^^^^^^^^^^^^^^

Simple constants are really simple. They look like `enumerations in Python 3.4 <https://docs.python.org/3/library/enum.html>`_::

    >>> from candv import SimpleConstant, Constants
    >>> class STATUS(Constants):
    ...     SUCCESS = SimpleConstant()
    ...     FAILURE = SimpleConstant()
    ...

And they can be used just like enumerations. Here ``STATUS`` is a subclass of
:class:`candv.Constants`. The latter can contain any instances of
:class:`~candv.base.Constant` class or its subclasses. ``SimpleConstant`` is
just an alias to :class:`candv.base.Constant`.

Access some constant::

    >>> STATUS.SUCCESS
    <constant 'STATUS.SUCCESS'>

Access its name::

    >>> STATUS.SUCCESS.name
    'SUCCESS'

List names of all constants in the container::

    >>> STATUS.names()
    ['SUCCESS', 'FAILURE']

List all constants in the container::

    >>> STATUS.constants()
    [<constant 'STATUS.SUCCESS'>, <constant 'STATUS.FAILURE'>]

Check whether the container has constant with a given name::

    >>> STATUS.contains('SUCCESS')
    True
    >>> STATUS.contains('XXX')
    False

Get constant by name or get a :class:`KeyError`::

    >>> STATUS.get_by_name('FAILURE')
    <constant 'STATUS.FAILURE'>
    >>> STATUS.get_by_name('XXX')
    Traceback (most recent call last):
      File "<input>", line 1, in <module>
      File "candv/base.py", line 316, in get_by_name
        .format(name, cls.__name__))
    KeyError: "Constant with name 'XXX' is not present in 'STATUS'"

Constants with values
^^^^^^^^^^^^^^^^^^^^^

Constants with values behave like simple constants, except they can have any
object attached to them as a value. It's something like an ordered dictionary::

    >>> from candv import ValueConstant, Values
    >>> class TEAMS(Values):
    ...     NONE = ValueConstant(0)
    ...     RED = ValueConstant(1)
    ...     BLUE = ValueConstant(2)
    ...

Here ``TEAMS`` is a subclass of :class:`~candv.Values`, which is a more
specialized container than :class:`~candv.Constants`. As you may guessed,
:class:`~candv.ValueConstant` is a more specialized constant class than
``SimpleConstant`` and its instances have own values. ``Values`` and its
subclasses treat as constants only instances of ``ValueConstant`` or its
sublasses::

    >>> class INVALID(Values):
    ...     FOO = SimpleConstant()
    ...     BAR = SimpleConstant()
    ...

Here ``INVALID`` contains 2 instances of ``SimpleConstant``, which is more
gerenal then ``ValueConstant``. It's not an error, but those 2 constants will
be invisible for the container::

    >>> INVALID.constants()
    []

Ok, let's get back to our ``TEAMS``. You can access values of constants:

    >>> TEAMS.RED.value
    1

Get constant by its value or get :class:`ValueError`::

    >>> TEAMS.get_by_value(2)
    <constant 'TEAMS.BLUE'>
    >>> TEAMS.get_by_value(-1)
    Traceback (most recent call last):
      File "<input>", line 1, in <module>
      File "candv/__init__.py", line 146, in get_by_value
        value, cls.__name__))
    ValueError: Value '-1' is not present in 'TEAMS'

List all values inside the container::

    >>> TEAMS.values()
    [0, 1, 2]

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

Verbose constants
^^^^^^^^^^^^^^^^^

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
    ...     foo = VerboseConstant("Some foo constant", "help")
    ...     bar = VerboseConstant(verbose_name="Some bar constant",
    ...                           help_text="some help")

Here you can access ``verbose_name`` and ``help_text`` as attributes of
constants::

    >>> TYPES.foo.verbose_name
    'Some foo constant'
    >>> TYPES.foo.help_text
    'help'

Now you can rewrite your code:

.. code-block:: jinja

    <select>
    {% for constant in TYPES.constants() %}
        <option value='{{ constant.name }}' title='{{ constant.help_text }}'>{{ constant.verbose_name }}</option>
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

Our sample HTML block will look almost the same, except ``value`` attribute:

.. code-block:: jinja

    <select>
    {% for constant in TYPES.constants() %}
        <option value='{{ constant.value }}' title='{{ constant.help_text }}'>{{ constant.verbose_name }}</option>
    {% endfor %}
    </select>

.. _hierarchies:

Hierarchies
^^^^^^^^^^^

**candv** library supports direct attaching of a group of constants to another
constant to create hierarchies. A group can be created from any constant and
any container can be used to store children. You may already saw this in
:ref:`introduction <complex-example>`, but let's examine simple example::

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

    >>> TREE.LEFT.LEFT
    <constant 'TREE.LEFT.LEFT'>
    >>> TREE.RIGHT.names()
    ['LEFT', 'RIGHT']
