candv: Constants & Values
=========================

|pypi_package| |python_versions| |docs| |license|

|linux_build| |windows_build| |coverage| |codebeat| |codacy| |scrutinizer|


``candv`` allows to create complex enum-like constants.

In contrast to other methods of defining constants, ``candv`` helps to organize and to document classes of constants.

This is done by providing iteration and lookup facilities for containers of constants.

Additionally, ``candv`` provides an ability to attach human-readable names, descriptions, arbitrary values, and methods to constants.

Inspired by `Constants from Twisted`_ and `Form Fields from Django`_.


Installation
------------

Available as a `PyPI <https://pypi.python.org/pypi/candv>`_ package:

.. code-block:: bash

  pip install candv


Brief overview
--------------

The most basic definition of constants:

.. code-block:: python

  from candv import Constants
  from candv import SimpleConstant

  class TEAM(Constants):
    RED  = SimpleConstant()
    BLUE = SimpleConstant()


And usage:

.. code-block:: python

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


Using with values:

.. code-block:: python

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


Using with human-readable names:

.. code-block:: python

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


Supports custom methods:

.. code-block:: python

  from candv import Constants
  from candv import SimpleConstant

  class SupportedLanguages(Constants):
    en = SimpleConstant()
    ru = SimpleConstant()

    @classmethod
    def get_default(cls):
      return cls.en


  SupportedLanguages.get_default()  # <constant 'SupportedLanguages.en'>


And custom types of constants:

.. code-block:: python

  from candv import Constants
  from candv import SimpleConstant
  from candv import with_constant_class

  class MissionStatus(SimpleConstant):
    ...

  class MissionStatuses(with_constant_class(MissionStatus), Constants):
    not_loaded = MissionStatus()
    loaded     = MissionStatus()
    playing    = MissionStatus()


It's also possible to define hierarchies:

.. code-block:: python

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


More info
---------

Visit `the docs`_ for full information.

See `django-candv-choices`_ for using as ``choices`` in ``django``.

See `django-rf-candv-choices`_ for using as ``choices`` in ``django-rest-framework``.


.. |pypi_package| image:: https://img.shields.io/pypi/v/candv
   :target: http://badge.fury.io/py/candv/
   :alt: Version of PyPI package

.. |python_versions| image:: https://img.shields.io/badge/Python-3.7+-brightgreen.svg
   :alt: Supported versions of Python

.. |docs| image:: https://readthedocs.org/projects/candv/badge/?version=latest
   :target: docs_
   :alt: Documentation Status

.. |license| image:: https://img.shields.io/badge/license-MIT-blue.svg
   :target: https://github.com/oblalex/candv/blob/master/LICENSE
   :alt: MIT license

.. |linux_build| image:: http://img.shields.io/travis/oblalex/candv.svg?branch=master&style=flat
   :target: https://travis-ci.org/oblalex/candv

.. |windows_build| image:: https://ci.appveyor.com/api/projects/status/9ll29jta8sqtve91/branch/master?svg=true
   :target: https://ci.appveyor.com/project/oblalex/candv/branch/master
   :alt: Build status of the master branch on Windows

.. |coverage| image:: https://scrutinizer-ci.com/g/oblalex/candv/badges/coverage.png?b=master
   :target: https://scrutinizer-ci.com/g/oblalex/candv/?branch=master
   :alt: Code coverage

.. |codebeat| image:: https://codebeat.co/badges/270255bd-0a59-4f53-b91a-13bda8352bcf
   :target: https://codebeat.co/projects/github-com-oblalex-candv-master
   :alt: Code quality provided by «Codebeat»

.. |codacy| image:: https://app.codacy.com/project/badge/Grade/6cd7b783d9604e2195ab854733bdc806
   :target: https://www.codacy.com/gh/oblalex/candv/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=oblalex/candv&amp;utm_campaign=Badge_Grade
   :alt: Code quality provided by «Codacy»

.. |scrutinizer| image:: https://scrutinizer-ci.com/g/oblalex/candv/badges/quality-score.png?b=master
   :target: https://scrutinizer-ci.com/g/oblalex/candv/?branch=master
   :alt: Code quality provided by «Scrutinizer CI»


.. _Constants from Twisted: http://twistedmatrix.com/documents/current/core/howto/constants.html
.. _Form Fields from Django: https://docs.djangoproject.com/en/3.1/ref/forms/fields/
.. _the docs:
.. _docs: http://candv.readthedocs.org/en/latest/
.. _verboselib: https://github.com/oblalex/verboselib
.. _Django translation strings: https://docs.djangoproject.com/en/3.1/topics/i18n/translation/
.. _django-candv-choices: https://github.com/oblalex/django-candv-choices
.. _django-rf-candv-choices: https://github.com/oblalex/django-rf-candv-choices
