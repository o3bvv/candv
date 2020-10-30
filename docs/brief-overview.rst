.. _brief-overview:

Brief Overview
==============

The most basic definition of :ref:`simple constants <usage_simple_constants>`:

.. code-block:: python
  :linenos:

  from candv import Constants
  from candv import SimpleConstant


  class TEAM(Constants):
    RED  = SimpleConstant()
    BLUE = SimpleConstant()


And usage:

.. code-block:: python
  :linenos:
  :lineno-start: 8

  TEAM.RED                 # <constant 'TEAM.RED'>
  TEAM['RED']              # <constant 'TEAM.RED'>
  TEAM.get('RED')          # <constant 'TEAM.RED'>
  TEAM.get('GREEN')        # None
  TEAM.RED.name            # 'RED'
  TEAM.RED.full_name       # 'TEAM.RED'
  TEAM.RED.to_primitive()  # {'name': 'RED'}
  TEAM.RED.container       # <constants container 'TEAM'>

  TEAM                     # <constants container 'TEAM'>
  TEAM.name                # 'TEAM'
  TEAM.full_name           # 'TEAM'
  len(TEAM)                # 2
  TEAM.has_name('RED')     # True

  TEAM.names()             # ['RED', 'BLUE']
  TEAM.iternames()         # <odict_iterator object at 0x7f451013e0e0>

  TEAM.constants()         # [<constant 'TEAM.RED'>, <constant 'TEAM.BLUE'>]
  TEAM.iterconstants()     # <odict_iterator object at 0x7f45100f3450>

  TEAM.items()             # [('RED', <constant 'TEAM.RED'>), ('BLUE', <constant 'TEAM.BLUE'>)]
  TEAM.iteritems()         # <odict_iterator object at 0x7f451013bdb0>

  TEAM.to_primitive()      # {'name': 'TEAM', 'items': [{'name': 'RED'}, {'name': 'BLUE'}]}


Using :ref:`with values <usage_valued_constants>`:

.. code-block:: python
  :linenos:

  from candv import Values
  from candv import ValueConstant


  class TEAM(Values):
    RED  = ValueConstant(1)
    BLUE = ValueConstant(2)


  TEAM.values()            # [1, 2]
  TEAM.itervalues()        # <map object at 0x7f450ffdb1c0>

  TEAM.get_by_value(1)     # <constant 'TEAM.RED'>
  TEAM.filter_by_value(1)  # [<constant 'TEAM.RED'>]

  TEAM.RED.value           # 1
  TEAM.RED.to_primitive()  # {'name': 'RED', 'value': 1}


Using :ref:`with human-readable names <usage_verbose_constants>`:

.. code-block:: python
  :linenos:

  from candv import Constants
  from candv import VerboseConstant


  class Countries(Constants):
    au = VerboseConstant("Australia")
    uk = VerboseConstant("United Kingdom")
    us = VerboseConstant("United States")


  Countries.au.name            # 'au'
  Countries.au.verbose_name    # 'Australia'
  Countries.au.help_text       # None
  Countries.au.to_primitive()  # {'name': 'au', 'verbose_name': 'Australia', 'help_text': None}


With values and names:

.. code-block:: python
  :linenos:

  from candv import Values
  from candv import VerboseValueConstant


  class SkillLevel(Values):
    rki = VerboseValueConstant(0, "rookie")
    avg = VerboseValueConstant(1, "average")
    vtn = VerboseValueConstant(2, "veteran")
    ace = VerboseValueConstant(3, "ace")


  SkillLevel.avg.value           #  1
  SkillLevel.avg.name            # 'avg'
  SkillLevel.avg.full_name       # 'SkillLevel.avg'
  SkillLevel.avg.verbose_name    # 'average'
  SkillLevel.avg.help_text       # None
  SkillLevel.avg.to_primitive()  # {'name': 'avg', 'value': 1, 'verbose_name': 'average', 'help_text': None}


Plays well with verboselib_ or, say, `Django translation strings`_:

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


Supports :ref:`custom methods <customization>`:

.. code-block:: python
  :linenos:

  from candv import Constants
  from candv import SimpleConstant


  class SupportedLanguages(Constants):
    en = SimpleConstant()
    ru = SimpleConstant()

    @classmethod
    def get_default(cls):
      return cls.en


  SupportedLanguages.get_default()  # <constant 'SupportedLanguages.en'>


And :ref:`custom types of constants <customization>`:

.. code-block:: python
  :linenos:

  from candv import Constants
  from candv import SimpleConstant
  from candv import with_constant_class


  class MissionStatus(SimpleConstant):
    ...


  class MissionStatuses(with_constant_class(MissionStatus), Constants):
    not_loaded = MissionStatus()
    loaded     = MissionStatus()
    playing    = MissionStatus()


It's also possible to define :ref:`hierarchies <hierarchies>`:

.. code-block:: python
  :linenos:

  from candv import Constants
  from candv import SimpleConstant


  class STATUS(Constants):
    SUCCESS = SimpleConstant()
    ERROR   = SimpleConstant().to_group(Constants,

      INVALID   = SimpleConstant(),
      NOT_FOUND = SimpleConstant(),
      INTERNAL  = SimpleConstant(),
    )


  STATUS.names()                   # ['SUCCESS', 'ERROR']
  STATUS.ERROR                     # <constants group 'STATUS.ERROR'>
  STATUS.ERROR.full_name           # 'STATUS.ERROR'
  STATUS.ERROR.INTERNAL            # <constant 'STATUS.ERROR.INTERNAL'>
  STATUS.ERROR.INTERNAL.full_name  # 'STATUS.ERROR.INTERNAL'
  STATUS.ERROR.names()             # ['INVALID', 'NOT_FOUND', 'INTERNAL']


.. _verboselib: https://github.com/oblalex/verboselib
.. _Django translation strings: https://docs.djangoproject.com/en/3.1/topics/i18n/translation/
