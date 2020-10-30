Usage
=====

The concept behind ``candv`` is that constants are grouped together into containers.

Those containers are special classes having constants as class attributes. All containers are created by subclassing :class:`~candv.Constants`. Containers cannot be instantiated.

In their turn, constants are special objects, which are instances of :class:`~candv.SimpleConstant` or of its derivatives.

As containers are classes and constants are instances of classes, they can and actually have own methods and attributes.

It is possible to add custom functionality simply by subclassing :class:`~candv.Constants` and :class:`~candv.SimpleConstant` respectively.

In addition to the basic constants and basic containers, ``candv`` also provides extended ones like :class:`~candv.VerboseConstant`, :class:`~candv.ValueConstant`, :class:`~candv.Values`, etc.


.. _usage_simple_constants:

Simple constants
----------------

Simple constants are really simple. They do not have any particular values attached and resemble :class:`enum.Enum` used with :class:`enum.auto`:

.. code-block:: python
  :linenos:

  from candv import Constants
  from candv import SimpleConstant


  class STATUS(Constants):
    SUCCESS = SimpleConstant()
    FAILURE = SimpleConstant()


Here, ``STATUS`` is a subclass of :class:`~candv.Constants`. It acts as a container:

.. code-block:: python
  :linenos:
  :lineno-start: 8

  >>> STATUS
  <constants container 'STATUS'>


All containers have the following attributes:

* ``name``
* ``full_name``


By default they are equal to the name of the class itself:

.. code-block:: python
  :linenos:
  :lineno-start: 10

  >>> STATUS.name
  'STATUS'

  >>> STATUS.full_name
  'STATUS'


.. note::

  If there is a reason on the Earth to define custom names, it can be done:

  .. code-block:: python

    class STATUS(Constants):
      name = "foo"
      full_name = f"package.{name}"

      SUCCESS = SimpleConstant()
      FAILURE = SimpleConstant()


The same attributes are available to all constants as well:

.. code-block:: python
  :linenos:
  :lineno-start: 15

  >>> STATUS.SUCCESS.name
  'SUCCESS'

  >>> STATUS.SUCCESS.full_name
  'STATUS.SUCCESS'


As can be seen from the above, names of constants are equal to the names of container's attributes. And full names combine names of constants with full names of their containers. Custom values are not allowed.

Next, all containers have a member-access API similar to the API of Python's :class:`dict`:

.. code-block:: python
  :linenos:
  :lineno-start: 20

  >>> STATUS.names()
  ['SUCCESS', 'FAILURE']

  >>> STATUS.iternames()
  <odict_iterator object at 0x7f289fa6e680>

  >>> STATUS.constants()
  [<constant 'STATUS.SUCCESS'>, <constant 'STATUS.FAILURE'>]

  >>> STATUS.iterconstants()
  <odict_iterator object at 0x7f289fa6ecc0>

  >>> STATUS.items()
  [('SUCCESS', <constant 'STATUS.SUCCESS'>), ('FAILURE', <constant 'STATUS.FAILURE'>)]

  >>> STATUS.iteritems()
  <odict_iterator object at 0x7f289fa1e360>

  >>> list(STATUS)
  ['SUCCESS', 'FAILURE']

  >>> len(STATUS)
  2

  >>> STATUS['SUCCESS']
  <constant 'STATUS.SUCCESS'>

  >>> 'SUCCESS' in STATUS
  True

  >>> STATUS.has_name('PENDING')
  False

  >>> STATUS.get('XXX')
  None

  >>> STATUS.get('XXX', default=999)
  999


.. note::

  Since 1.1.2 it is possible to list constants and get the same result by calling :meth:`~candv.Constants.values` and
  :meth:`~candv.Constants.itervalues`:

  .. code-block:: python

    >>> STATUS.values()
    [<constant 'STATUS.SUCCESS'>, <constant 'STATUS.FAILURE'>]

    >>> STATUS.itervalues()
    <odict_iterator object at 0x7f289fa17b30>

  These methods are overridden in :class:`~candv.Values` (see the section below).


In addition to the item-access, containers also provide a dot-access for their constants:

.. code-block:: python
  :linenos:
  :lineno-start: 58

  >>> STATUS.SUCCESS
  <constant 'STATUS.SUCCESS'>


Finally, every constant has access to own containers via the ``container`` attribute:

.. code-block:: python
  :linenos:
  :lineno-start: 60

  >>> STATUS.SUCCESS.container
  <constants container 'STATUS'>


.. _usage_valued_constants:

Constants with values
---------------------

Constants with values are created via :class:`~candv.ValueConstant` and can have arbitrary values attached to them.

Such constants have to be contained by derivatives of :class:`~candv.Values` class. This enables additional functionality like inverse lookups, i.e. lookups of constants by their values.

.. code-block:: python
  :linenos:

  from candv import ValueConstant
  from candv import Values


  class TEAMS(Values):
    NONE = ValueConstant('#EEE')
    RED  = ValueConstant('#F00')
    BLUE = ValueConstant('#00F')


Here, ``TEAMS`` is a subclass of :class:`~candv.Values`, which is a specialized version of :class:`~candv.Constants`. And :class:`~candv.ValueConstant` is a specialized version of :class:`~candv.SimpleConstant`:

.. code-block:: python
  :linenos:
  :lineno-start: 9

  >>> Values.mro()
  [<constants container 'Values'>, <constants container 'Constants'>, <class 'object'>]

  >>> ValueConstant.mro()
  [<class 'candv.ext.ValueConstant'>, <class 'candv.core.SimpleConstant'>, <class 'object'>]


So, ``TEAMS`` has all of the attributes and methods described above. Its :meth:`~candv.Values.values` method returns actual values of its constants:

.. code-block:: python
  :linenos:
  :lineno-start: 14

  >>> TEAMS.values()
  ['#EEE', '#F00', '#00F']

  >>> TEAMS.itervalues()
  <map object at 0x7f289fa54ac0>


Values of constants themselves are also accessible:

.. code-block:: python
  :linenos:
  :lineno-start: 19

  >>> TEAMS.RED.value
  '#F00'


In addition to the previously mentioned ``get()`` method, :class:`~candv.Values` provides :meth:`~candv.Values.get_by_value` method:

.. code-block:: python
  :linenos:
  :lineno-start: 21

  >>> TEAMS.get_by_value('#F00')
  <constant 'TEAMS.RED'>


It is allowed for constants to have multiple constants with same values. However, in such case the :meth:`~candv.Values.get_by_value` method will return the first matching constant considering the order constants are defined:

.. code-block:: python
  :linenos:

  class FOO(Values):
    ATTR1     = ValueConstant('one')
    ATTR2     = ValueConstant('two')
    ATTR1_DUB = ValueConstant('one')


.. code-block:: python
  :linenos:
  :lineno-start: 5

  >>> FOO.get_by_value('one')
  <constant 'FOO.ATTR1'>


If there is a real need to have multiple constants with same values, it's possible to get all of them by their value using :meth:`~candv.Values.filter_by_value` method:

.. code-block:: python
  :linenos:
  :lineno-start: 7

  >>> FOO.filter_by_value('one')
  [<constant 'FOO.ATTR1'>, <constant 'FOO.ATTR1_DUB'>]


.. _usage_verbose_constants:

Verbose constants
-----------------

Verbose constants are special constants with human-readable names and help messages.

They can be useful when there's a need to present constants as possible choices to a user.

Usually, this is achieved by defining each constant literal as a separate global variable, followed by construction of a lookup dictionary or tuple:

.. code-block:: python
  :linenos:

  COUNTRY_AU = 'au'
  COUNTRY_UK = 'uk'
  COUNTRY_US = 'us'

  COUNTRIES_NAMES = (
    (COUNTRY_AU, "Australia"),
    (COUNTRY_UK, "United States"),
    (COUNTRY_US, "United Kingdom"),
  )


This is hard to use and to maintain already. And its very common for names to come with descriptions or help texts, which means additional complexity.

In the contrast, it's possible to use :class:`~candv.VerboseConstant` to keep definitions coupled and concise:

.. code-block:: python
  :linenos:

  from candv import Constants
  from candv import VerboseConstant


  class Countries(Constants):
    au = VerboseConstant("Australia")
    uk = VerboseConstant("United Kingdom")
    us = VerboseConstant(
      verbose_name="United States",
      help_text="optional description",
    )


Verbose constants are derived from :class:`~candv.SimpleConstant` in their nature:

.. code-block:: python
  :linenos:
  :lineno-start: 12

  >>> VerboseConstant.mro()
  [<class 'candv.ext.VerboseConstant'>, <class 'candv.ext.VerboseMixin'>, <class 'candv.core.SimpleConstant'>, <class 'object'>]

And in addition to the basic attributes of :class:`~candv.SimpleConstant`, instances of :class:`~candv.VerboseConstant` have extra optional attributes:

* ``verbose_name``
* ``help_text``

.. code-block:: python
  :linenos:
  :lineno-start: 14

  >>> Countries.au.name
  'au'

  >>> Countries.au.verbose_name
  'Australia'

  >>> Countries.au.help_text
  None

  >>> Countries.us.help_text
  'optional description'


Attributes of verbose constants can be lazy translations, for example, provided by verboselib_ or, say, `Django translation strings`_:

.. code-block:: python
  :linenos:

  from candv import Constants
  from candv import VerboseConstant

  from verboselib import Translations


  translations = Translations(
    domain="the_app",
    locale_dir_path="locale",
  )
  _ = translations.gettext_lazy


  class UnitType(Constants):
    aircraft = VerboseConstant(_("aircraft"))
    ship     = VerboseConstant(_("ship"))
    train    = VerboseConstant(_("train"))
    vehicle  = VerboseConstant(_("vehicle"))


.. _usage_verbose_constants_with_values:

Verbose constants with values
-----------------------------

Another type of constants supported by ``candv`` out of the box are verbose constants with values.

Intuitively, the constant class which allows that is :class:`~candv.VerboseValueConstant`:

Obviously, it needs to be contained by :class:`~candv.Values` or by its derivatives:

.. code-block:: python
  :linenos:

  from candv import Values
  from candv import VerboseValueConstant


  class SkillLevel(Values):
    rki = VerboseValueConstant(0, "rookie")
    avg = VerboseValueConstant(1, "average")
    vtn = VerboseValueConstant(2, "veteran")
    ace = VerboseValueConstant(3, "ace")


Here, constants have attributes of both :class:`~candv.ValueConstant` and :class:`~candv.VerboseConstant`:

.. code-block:: python
  :linenos:
  :lineno-start: 10

  >>> VerboseValueConstant.mro()
  [<class 'candv.ext.VerboseValueConstant'>, <class 'candv.ext.VerboseMixin'>, <class 'candv.ext.ValueConstant'>, <class 'candv.core.SimpleConstant'>, <class 'object'>]

  >>> SkillLevel.avg.name
  'avg'

  >>> SkillLevel.avg.full_name
  'SkillLevel.avg'

  >>> SkillLevel.avg.value
  1


.. _hierarchies:

Hierarchies
-----------

``candv`` library supports an exotic feature of constants hierarchies. This enables creation of subconstants:

.. code-block:: python
  :linenos:

  from candv import Constants
  from candv import SimpleConstant


  class TREE(Constants):
    LEFT = SimpleConstant().to_group(Constants,
      LEFT  = SimpleConstant(),
      RIGHT = SimpleConstant(),
    )
    RIGHT = SimpleConstant().to_group(Constants,
      LEFT  = SimpleConstant(),
      RIGHT = SimpleConstant(),
    )


Here, the key point is :meth:`~candv.SimpleConstant.to_group` method. It turns a constant into a ``group``, which is both a constant and a container.

As for the arguments, the :meth:`~candv.SimpleConstant.to_group` method accepts a class that will be used to construct new container and  instances of constants passed as keywords.

Groups can be created from any constant and any container can be used to store subconstants.

.. code-block:: python
  :linenos:
  :lineno-start: 14

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


Serialization
-------------

There are several ways to serialize ``candv`` constants:

* Using :mod:`pickle`.
* Converting to a primitive and then to a JSON or similar.


Pickling
~~~~~~~~

Usually, pickling should be avoided. However, there are situations, when it cannot be avoided, e.g., when passing data to and from subprocesses, etc. If pickled objects really can be trusted, they are good to go.

``candv`` constants are ``pickle``-able. For example, there's a definition of ``STATUS`` in a ``constants.py`` module:

.. code-block:: python
  :linenos:

  # constants.py
  from candv import Constants
  from candv import SimpleConstant


  class STATUS(Constants):
    SUCCESS = SimpleConstant()
    FAILURE = SimpleConstant()


One process can create a variable and pickle it into a file:

.. code-block:: python
  :linenos:

  import pickle

  from constants import STATUS


  status = STATUS.SUCCESS

  with open('foo.pkl', 'wb') as f:
    pickle.dump(status, f)


And another process can restore the value:

.. code-block:: python
  :linenos:

  import pickle

  with open('foo.pkl', 'rb') as f:
    status = pickle.load(f)


.. code-block:: python
  :linenos:
  :lineno-start: 5

  >>> status
  <constant 'STATUS.SUCCESS'>


.. _usage_to_primitives:

Converting to primitives
~~~~~~~~~~~~~~~~~~~~~~~~

.. versionadded:: 1.3.0

Constants and containers can be converted into Python primitives for further serialization, for example, into JSONs.

This is done via ``to_primitive()`` method.

For example, for simple constants defined previously:

.. code-block:: python

  >>> STATUS.to_primitive()
  {'name': 'STATUS', 'items': [{'name': 'SUCCESS'}, {'name': 'FAILURE'}]}

  >>> STATUS.SUCCESS.to_primitive()
  {'name': 'SUCCESS'}


Same for constants with values:

.. code-block:: python

  >>> TEAMS.RED.to_primitive()
  {'name': 'RED', 'value': '#F00'}

.. note::

  Actual values of constants are out of scope of this library.

  Any value can be used as a value of constants, but converting values into primitives is almost up to the user.

  If a given value is a ``callable`` (e.g., it's a lazy translation string), ``candv`` will call it to get it's value.

  If it has ``to_primitive(*args, **kwargs)`` method, again, ``candv`` will call it.

  If it has ``isoformat()`` method (it's a ``date``, ``time``, etc.), ``candv`` will call it either.

  Everything else is expected to be a primitive by itself. Otherwise, it's recommended to implement :ref:`a custom constant class <customization>` with :ref:`custom conversion to primitives <customization_to_primitives>`.


For verbose constants:

.. code-block:: python

  >>> Countries.au.to_primitive()
  {'name': 'au', 'verbose_name': 'Australia', 'help_text': None}


For verbose constants with values:

.. code-block:: python

  >>> SkillLevel.ace.to_primitive()
  {'name': 'ace', 'value': 3, 'verbose_name': 'ace', 'help_text': None}


And for hierarchies:

.. code-block:: python

  >>> TREE.to_primitive()
  {'name': 'TREE', 'items': [{'name': 'LEFT', 'items': [{'name': 'LEFT'}, {'name': 'RIGHT'}]}, {'name':   'RIGHT', 'items': [{'name': 'LEFT'}, {'name': 'RIGHT'}]}]}

  >>> TREE.LEFT.to_primitive()
  {'name': 'LEFT', 'items': [{'name': 'LEFT'}, {'name': 'RIGHT'}]}

  >>> TREE.LEFT.LEFT.to_primitive()
  {'name': 'LEFT'}


Using with django
-----------------

It's possible to use verbose constants and verbose constants with values as ``choices`` in ``djnago`` models. See `django-candv-choices`_ details.

Additionally, see `django-rf-candv-choices`_ for using as ``choices`` in ``django-rest-framework``.


.. _verboselib: https://github.com/oblalex/verboselib
.. _Django translation strings: https://docs.djangoproject.com/en/3.1/topics/i18n/translation/
.. _django-candv-choices: https://github.com/oblalex/django-candv-choices
.. _django-rf-candv-choices: https://github.com/oblalex/django-rf-candv-choices
