candv: Constants & Values
=========================

|pypi_package| |python_versions| |license|

|unix_build| |windows_build| |codebeat| |codacy| |scrutinizer|


``candv`` allows to create complex enum-like constants.

In contrast to other methods of defining constants, ``candv`` helps to organize and to document classes of constants.

This is done by providing iteration and lookup facilities for containers of constants.

Additionally, ``candv`` provides an ability to attach human-readable names, descriptions, arbitrary values, and methods to constants.

Inspired by `Constants from Twisted`_ and `Form Fields from Django`_.


Contents
========

.. toctree::
  :maxdepth: 2
  :numbered:

  brief-overview
  installation
  usage
  customization


Changelog
=========

* `1.4.0`_ (Oct 30, 2020)

  API changes: public API is not changed, however, the following internal changes are introduced:

  #. ``candv.base`` is moved to ``candv.core``.
  #. Package-level definitions in ``candv`` are moved to ``candv.ext``.
  #. ``candv.version`` module is added.
  #. Package-specific exceptions are defined in ``candv.exceptions``. Work as before, but now exceptions can be caught more precisely if needed.
  #. ``candv.SimpleConstant`` is a direct reference to ``candv.core.SimpleConstant`` now. Previously it was an alias to ``candv.base.Constant``.
  #. ``candv.Constants`` is a direct reference to ``candv.core.Constants`` now. Previously it was an alias to ``candv.base.ConstantsContainer``.

  Python support:

  * Support of all Python versions below ``3.7`` is dropped.

  Other:

  #. All external dependencies are removed.
  #. The license is switched from ``LGPLv3`` to ``MIT``.
  #. The documentation is reworked to be more explanatory and concise.


* `1.3.1`_ (Aug 1, 2015)

  * Comparison of constants is fixed: now it is based on constant's ``full_name`` attribute (`issue #11`_).


* `1.3.0`_ (Dec 31, 2014)

  * ``to_primitive()`` method is implemented. This can be used for serialization, for example, into JSON (`issue #1`_). See :ref:`usage <usage_to_primitives>` and :ref:`customization <customization_to_primitives>` for more info.


* `1.2.0`_ (Oct 11, 2014)

  #. Core classes are significantly refactored.
  #. ``constant_class`` now uses ``candv.SimpleConstant`` as the default value (instead of ``None``, see :ref:`customization` for more info).
  #. Support of groups is reimplemented: now they are classes just as other constants containers (previously groups were instances of patched containers). So, groups automatically gain all of those attributes and methods which usual containers have.
  #. Constant's ``container`` attribute is public now. Groups of constants have it too (see :ref:`hierarchies`).
  #. API of containers is made really close to API of Python's :class:`dict` (:ref:`see usage <usage_simple_constants>` for more info):

     * ``__getitem__``, ``__contains__``, ``__len__`` and ``__iter__`` magic methods are implemented.
     * ``contains`` method is renamed to ``has_name``.
     * ``get_by_name`` method is removed in favor of ``__getitem__`` method.
     * ``get`` method with support of default value is introduced.

  #. All objects (containers, groups and constants) have ``name`` and ``full_name`` attributes now. This may be useful if names of constants are used as key values (e.g. for Redis).
  #. Also, all objects have good ``repr`` now.
  #. Mixin factory ``candv.with_constant_class()`` is introduced. It may help to define containers in a more compact way.
  #. A potential bug of uninitialized unbounded constants is fixed. Unbounded constant is an instance of a class which differs from container's ``constant_class`` or its subclasses. This is unnatural case, but if this is really needed, it will not break now.
  #. Exception messages are more informative now.
  #. Tests are moved out the package.
  #. Introductory documentation is improved. Other docs are updated too.


* `1.1.2`_ (Jul 6, 2014)

  * ``values`` and ``itervalues`` attributes are added to ``Constants``.


* `1.1.1`_ (Jun 21, 2014)

  * switch license from ``GPLv2`` to ``LGPLv3``.


* `1.1.0`_ (Jun 21, 2014)

  #. ``Choices`` container is moved to `django-candv-choices`_ library.
  #. Docs are updated and typos are fixed.
  #. Utils are stripped from requirements.


* `1.0.0`_ (Apr 15, 2014)

  * Initial version.


Sources
=======

Feel free to explore, fork or contribute: https://github.com/oblalex/candv


API
===

.. toctree::
  :maxdepth: 2

  candv


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


.. |unix_build| image:: http://img.shields.io/travis/oblalex/candv.svg?branch=master&style=flat
   :target: https://travis-ci.org/oblalex/candv

.. |windows_build| image:: https://ci.appveyor.com/api/projects/status/9ll29jta8sqtve91/branch/master?svg=true
    :target: https://ci.appveyor.com/project/oblalex/candv/branch/master
    :alt: Build status of the master branch on Windows

.. |pypi_package| image:: https://img.shields.io/pypi/v/candv
   :target: http://badge.fury.io/py/candv/
   :alt: Version of PyPI package

.. |python_versions| image:: https://img.shields.io/badge/Python-3.7+-brightgreen.svg
   :alt: Supported versions of Python

.. |license| image:: https://img.shields.io/badge/license-MIT-blue.svg
   :target: https://github.com/oblalex/candv/blob/master/LICENSE
   :alt: MIT license

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
.. _django-candv-choices: https://github.com/oblalex/django-candv-choices

.. _issue #1: https://github.com/oblalex/candv/issues/1
.. _issue #11: https://github.com/oblalex/candv/issues/11

.. _1.4.0: https://github.com/oblalex/candv/compare/v1.3.1...v1.4.0
.. _1.3.1: https://github.com/oblalex/candv/compare/v1.3.0...v1.3.1
.. _1.3.0: https://github.com/oblalex/candv/compare/v1.2.0...v1.3.0
.. _1.2.0: https://github.com/oblalex/candv/compare/v1.1.2...v1.2.0
.. _1.1.2: https://github.com/oblalex/candv/compare/v1.1.1...v1.1.2
.. _1.1.1: https://github.com/oblalex/candv/compare/v1.1.0...v1.1.1
.. _1.1.0: https://github.com/oblalex/candv/compare/v1.0.0...v1.1.0
.. _1.0.0: https://github.com/oblalex/candv/releases/tag/v1.0.0
