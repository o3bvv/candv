.. _dive-in:

Dive in
=======

How often do you need to define names which can be treated as constants?
How about grouping them into something integral? What about giving names and
descriptions for your constants? Attaching values to them? Do you need to find
constants by their names or values? What about combining groups of constants
into an hierarchy? And finally, how do you imagine documenting process of this
all?


Simple example
--------------

Well, if you have ever asked yourself one of these questions, this library may
answer you. Just look::

    >>> from candv import Constants, SimpleConstant
    >>> class BAR(Constants):
    ...     """
    ...     This is an example container of named constants.
    ...     """
    ...     ONE = SimpleConstant()
    ...     TWO = SimpleConstant()
    ...     NINE = SimpleConstant()
    ...

Let's see some stuff. What's ``BAR``?

::

    >>> BAR
    <constants container 'BAR'>
    >>> BAR.name
    'BAR'
    >>> BAR.full_name
    'BAR'

What constants does it have? What's their order?

::

    >>> BAR.names()
    ['ONE', 'TWO', 'NINE']

What are those constants?

::

    >>> BAR.constants()
    [<constant 'BAR.ONE'>, <constant 'BAR.TWO'>, <constant 'BAR.NINE'>]
    >>> BAR.items()
    [('ONE', <constant 'BAR.ONE'>), ('TWO', <constant 'BAR.TWO'>), ('NINE', <constant 'BAR.NINE'>)]

How much constants are there in the container?

::

    >>> len(BAR)
    3

Does ``BAR`` have a constant named ``ONE``?

::

    >>> BAR.has_name('ONE')
    True
    >>> 'ONE' in BAR
    True

How to get a constant by name?

::

    >>> BAR['TWO']
    <constant 'BAR.TWO'>

How to get a constant by name with fallback to default value?

::

    >>> BAR.get('XXX', default=123)
    123

How to access a single constant?

::

    >>> BAR.ONE
    <constant 'BAR.ONE'>

What attributes does it have?

::

    >>> BAR.ONE.name
    'ONE'
    >>> BAR.ONE.full_name
    'BAR.ONE'
    >>> BAR.ONE.container
    <constants container 'BAR'>


.. _complex-example:

Complex example
---------------

Was it too simple for you? Watchout:

.. code-block:: python

    >>> from candv import (
    ...     Constants, Values, SimpleConstant, VerboseConstant, ValueConstant,
    ...     VerboseValueConstant,
    ... )
    >>> class FOO(Constants):
    ...     """
    ...     Example container of constants which shows the diversity of the library.
    ...     """
    ...     #: just a named constant
    ...     ONE = SimpleConstant()
    ...     #: named constant with verbose name
    ...     BAR = VerboseConstant("bar constant")
    ...     #: named constant with verbose name and description
    ...     BAZ = VerboseConstant(verbose_name="baz constant",
    ...                           help_text="description of baz constant")
    ...     #: named constant with value
    ...     QUX = ValueConstant(4)
    ...     #: another named constant with another value (list)
    ...     SOME = ValueConstant(['1', 4, True])
    ...     #: yet another named constant with another value, verbose name and description
    ...     SOME_VERBOSE = VerboseValueConstant("some value",
    ...                                         "some string",
    ...                                         "this is just some string")
    ...     #: named group of constants with values
    ...     GROUP = SimpleConstant().to_group(Values,
    ...         SIX=ValueConstant(6),
    ...         SEVEN=ValueConstant("S373N"),
    ...     )
    ...     #: subgroup with name, value and verbose name
    ...     MEGAGROUP = VerboseValueConstant(
    ...         value=100500,
    ...         verbose_name="megagroup"
    ...     ).to_group(Values,
    ...         HEY=ValueConstant(1),
    ...         #: group inside another group. How deep can you go?
    ...         YAY=ValueConstant(2).to_group(Constants,
    ...             OK=SimpleConstant(),
    ...             ERROR=SimpleConstant(),
    ...         ),
    ...     )

Whew! This looks like a big mess, but it shows all tasty things in one place.
If you need something simple, you can have it.

Let's try to investigate this example.

At first, what do we have?

::

    >>> FOO
    <constants container 'FOO'>
    >>> FOO.name
    'FOO'
    >>> FOO.full_name
    'FOO'

What's inside?

::

    >>> FOO.names()
    ['ONE', 'BAR', 'BAZ', 'QUX', 'SOME', 'SOME_VERBOSE', 'GROUP', 'MEGAGROUP']

What are all these things?

::

    >>> FOO.constants()
    [<constant 'FOO.ONE'>, <constant 'FOO.BAR'>, <constant 'FOO.BAZ'>, <constant 'FOO.QUX'>, <constant 'FOO.SOME'>, <constant 'FOO.SOME_VERBOSE'>, <constants group 'FOO.GROUP'>, <constants group 'FOO.MEGAGROUP'>]

Okay, we've seen :ref:`SimpleConstant <usage_simple_constants>` in action. What is :ref:`VerboseConstant <usage_verbose_constants>`?

::

    >>> FOO.BAZ
    <constant 'FOO.BAZ'>
    >>> FOO.BAZ.name
    'BAZ'
    >>> FOO.BAZ.full_name
    'FOO.BAZ'
    >>> FOO.BAZ.verbose_name
    'baz constant'
    >>> FOO.BAZ.help_text
    'description of baz constant'

Yes, verbose constants can carry name and description for humans.

What about :ref:`ValueConstant <usage_valued_constants>`?

::

    >>> FOO.QUX
    <constant 'FOO.QUX'>
    >>> FOO.QUX.name
    'QUX'
    >>> FOO.QUX.full_name
    'FOO.QUX'
    >>> FOO.QUX.value
    4

How about adding verbosity to values?

::

    >>> FOO.SOME_VERBOSE
    <constant 'FOO.SOME_VERBOSE'>
    >>> FOO.SOME_VERBOSE.value
    'some value'
    >>> FOO.SOME_VERBOSE.verbose_name
    'some string'
    >>> FOO.SOME_VERBOSE.help_text
    'this is just some string'

What is a group?

::

    >>> FOO.GROUP
    <constants group 'FOO.GROUP'>
    >>> FOO.GROUP.name
    'GROUP'
    >>> FOO.GROUP.full_name
    'FOO.GROUP'

It's a constant!

::

    >>> FOO.GROUP.constant_class
    <class 'candv.ValueConstant'>
    >>> FOO.GROUP.names()
    ['SIX', 'SEVEN']
    >>> FOO.GROUP.constants()
    [<constant 'FOO.GROUP.SIX'>, <constant 'FOO.GROUP.SEVEN'>]
    >>> FOO.GROUP.values()
    [6, 'S373N']
    >>> FOO.GROUP.get_by_value(6)
    <constant 'FOO.GROUP.SIX'>

And it's a container! Groups, like photons, have dual nature: they are both
constants and containers according to your needs.

Can we attach values and other stuff to groups? Surely!

::

    >>> FOO.MEGAGROUP.value
    100500
    >>> FOO.MEGAGROUP.verbose_name
    'megagroup'
    >>> FOO.MEGAGROUP.names()
    ['HEY', 'YAY']

Can groups contain nested groups? Yes, they can:

::

    >>> FOO.MEGAGROUP.YAY
    <constants group 'FOO.MEGAGROUP.YAY'>
    >>> FOO.MEGAGROUP.YAY.full_name
    'FOO.MEGAGROUP.YAY'
    >>> FOO.MEGAGROUP.YAY.names()
    ['OK', 'ERROR']

:ref:`Visit hierarchies section <hierarchies>` for more info about groups.

Any real examples?
------------------

Yeah. There are some real public examples.
`See some examples <https://github.com/IL2HorusTeam/il2fb-commons/tree/master/il2fb/commons>`_.

In most cases you will be satisfied with standard facilities of the libraries.
But you are not limited. You can :ref:`create your own <customization>`
containers and constants. Examples mentioned above also may help you with this.

And of course, instead of a thousand words you can
`dig around tests <https://github.com/oblalex/candv/tree/master/tests>`_.

.. note::

    By the way, verbose names taste more sweet if you use
    `verboselib <https://github.com/oblalex/verboselib>`_ for I18N (or any
    other suitable for you mechanism).
