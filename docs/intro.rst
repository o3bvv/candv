Introduction
============

How often do you need to define names which can be treated as constants?
How about grouping them into something integral? What about giving names and
descriptions for your constants? Attaching values to them? Do you need to find
constants by their names or values? What about combining groups of constants
into an hierarchy? And finally, how do you imagine documenting process of this
all?

Well, if you have ever asked yourself one of these questions, this library may
answer you. Just look::

    >>> class BAR(Constants):
    ...     ONE = SimpleConstant()
    ...     TWO = SimpleConstant()
    ...     NINE = SimpleConstant()
    ...
    >>> BAR.ONE
    <constant 'BAR.ONE'>
    >>> BAR.names()
    ['ONE', 'TWO', 'NINE']
    >>> BAR.constants()
    [<constant 'BAR.ONE'>, <constant 'BAR.TWO'>, <constant 'BAR.NINE'>]
    >>> BAR.items()
    [('ONE', <constant 'BAR.ONE'>), ('TWO', <constant 'BAR.TWO'>), ('NINE', <constant 'BAR.NINE'>)]
    >>> BAR.contains('NINE')
    True
    >>> BAR.get_by_name('TWO')
    <constant 'BAR.TWO'>
    >>> BAR.get_by_name('TWO').name
    'TWO'

Too simple for you? Watchout:

.. _complex-example:

.. code-block:: python

    >>> class FOO(Constants):
    ...     """
    ...     Some group of constants showing the diversity of the library.
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
    ...     #: another named constant with another value
    ...     SOME = ValueConstant(['1', 4, '2'])
    ...     #: yet another named constant with another value, verbose name and
    ...     #: description
    ...     SOME_VERBOSE = VerboseValueConstant("some value",
    ...                                         "some string",
    ...                                         "this is just some string")
    ...     #: subgroup with name
    ...     SUBGROUP = SimpleConstant().to_group(Values,
    ...         SIX=ValueConstant(6),
    ...         SEVEN=ValueConstant("S373N"),
    ...     )
    ...     #: subgroup with name, value and verbose name
    ...     MEGA_SUBGROUP = VerboseValueConstant(100500,
    ...                                          "mega subgroup").to_group(Values,
    ...         hey=ValueConstant(1),
    ...         #: subgroup inside another subgroup. How deep can you go?
    ...         yay=ValueConstant(2).to_group(Constants,
    ...             OK=SimpleConstant(),
    ...             ERROR=SimpleConstant(),
    ...         ),
    ...     )
    ...
    >>> FOO.names()
    ['ONE', 'BAR', 'BAZ', 'QUX', 'SOME', 'SOME_VERBOSE', 'SUBGROUP', 'MEGA_SUBGROUP']
    >>> FOO.BAR.verbose_name
    'bar constant'
    >>> FOO.BAZ.help_text
    'description of baz constant'
    >>> FOO.QUX.value
    4
    >>> FOO.SOME_VERBOSE.value, FOO.SOME_VERBOSE.verbose_name
    ('some value', 'some string')
    >>> FOO.SUBGROUP
    <constant 'FOO.SUBGROUP'>
    >>> FOO.SUBGROUP.names()
    ['SIX', 'SEVEN']
    >>> FOO.SUBGROUP.SIX.value
    6
    >>> FOO.SUBGROUP.get_by_value('S373N')
    <constant 'FOO.SUBGROUP.SEVEN'>
    >>> FOO.MEGA_SUBGROUP.value
    100500
    >>> FOO.MEGA_SUBGROUP.name
    'MEGA_SUBGROUP'
    >>> FOO.MEGA_SUBGROUP.verbose_name
    'mega subgroup'
    >>> FOO.MEGA_SUBGROUP.names()
    ['hey', 'yay']
    >>> FOO.MEGA_SUBGROUP.get_by_value(2).ERROR
    <constant 'FOO.MEGA_SUBGROUP.yay.ERROR'>

Okay, this is looks like a big mess, but it shows all-in-one. If you need
something simple, you can have it.
