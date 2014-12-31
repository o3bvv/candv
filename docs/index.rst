candv: Constants & Values
=========================

|Build Status| |Coverage Status| |PyPi package| |PyPi downloads| |License|

**candv** stands for `Constants & Values`. It is a little Python library which
provides an easy way for creating complex constants.


Contents
========

.. toctree::
   :maxdepth: 2
   :numbered:

   dive-in
   install
   usage
   customization
   misc


Changelog
=========

*You can click a version name to see a diff with the previous one.*

* `1.2.1`_ (Dec 31, 2014)

   #. Implement ``to_primitive()`` method, which can be used for
      serialization, for example, into JSON (`#1`_).
      See :ref:`usage<usage_exporting>` and
      :ref:`customization<customization_exporting>` for more info.

* `1.2.0`_ (Oct 11, 2014)

   #. Core classes were significantly refactored.
   #. ``constant_class`` uses :class:`~candv.base.Constant` as default value
      (instead of ``None``, see :ref:`custom_containers` for more info).
   #. Support of groups was reimplemented: now they are classes just as other
      constants containers (earlier groups were instances of patched
      containers). So, groups automatically gain all those attributes and
      methods which usual containers have.
   #. Constant's ``container`` attribute was made public. Groups of constants
      now have it too (see :ref:`hierarchies`).
   #. API of containers was made really close to API of Python's :class:`dict`
      (:ref:`see usage <usage_simple_constants>` for more info):

      * ``__getitem__``, ``__contains__``, ``__len__`` and ``__iter__`` magic
        methods were implemented;
      * ``contains`` method was renamed to ``has_name``;
      * ``get_by_name`` method was removed in favor of ``__getitem__`` method.
      * ``get`` method with support of default value was introduced.

   #. All objects (contaners, groups and constants) now have ``name`` and
      ``full_name`` attributes. This may be useful if you use names of
      constants as key values (e.g. for Redis).
   #. Also, all objects have good ``repr`` now.
   #. Mixin factory :meth:`~candv.base.with_constant_class` was introduced. It
      may help you to define more readable containers.
   #. A potential bug of uninitialized unbounded constants was fixed. Unbounded
      constant is an instance of a class which is differ from container's
      ``constant_class`` or its subclasses. This is unnatural case, but if you
      really need it, it will not break now.
   #. Exception messages are more informative now.
   #. Tests were moved out the package.
   #. :ref:`Introductory documentation <dive-in>` was improved. Other docs were
      updated too.

* `1.1.2`_ (Jul 6, 2014)

   * add ``values`` and ``itervalues`` attributes to ``ConstantsContainer``.

* `1.1.1`_ (Jun 21, 2014)

   * switch license from ``GPLv2`` to ``LGPLv3``.

* `1.1.0`_ (Jun 21, 2014)

   #. remove ``Choices`` container, move it to `django-candv-choices`_ library;
   #. update docs and fix typos;
   #. strip utils from requirements.

* `1.0.0`_ (Apr 15, 2014)
   Initial version.


Sources
=======

Feel free to explore, fork or contribute:

    https://github.com/oblalex/candv


Authors
=======

`Alexander Oblovatniy`_  (`@oblalex`_) created ``candv`` and
`these fine people`_ have contributed.


Modules
=======

.. toctree::
   :maxdepth: 2

   modules


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


.. |Build Status| image:: http://img.shields.io/travis/oblalex/candv.svg?branch=master&style=flat
   :target: https://travis-ci.org/oblalex/candv
.. |Coverage Status| image:: http://img.shields.io/coveralls/oblalex/candv.svg?branch=master&style=flat
   :target: https://coveralls.io/r/oblalex/candv?branch=master
.. |PyPi package| image:: http://img.shields.io/pypi/v/candv.svg?style=flat
   :target: http://badge.fury.io/py/candv/
.. |PyPi downloads| image:: http://img.shields.io/pypi/dm/candv.svg?style=flat
   :target: https://crate.io/packages/candv/
.. |License| image:: https://img.shields.io/badge/license-LGPLv3-brightgreen.svg?style=flat

.. _Alexander Oblovatniy: https://github.com/oblalex
.. _@oblalex: https://twitter.com/oblalex
.. _these fine people: https://github.com/oblalex/candv/contributors

.. _django-candv-choices: https://github.com/oblalex/django-candv-choices

.. _#1: https://github.com/oblalex/candv/issues/1

.. _1.2.1: https://github.com/oblalex/candv/compare/v1.2.0...v1.2.1
.. _1.2.0: https://github.com/oblalex/candv/compare/v1.1.2...v1.2.0
.. _1.1.2: https://github.com/oblalex/candv/compare/v1.1.1...v1.1.2
.. _1.1.1: https://github.com/oblalex/candv/compare/v1.1.0...v1.1.1
.. _1.1.0: https://github.com/oblalex/candv/compare/v1.0.0...v1.1.0
.. _1.0.0: https://github.com/oblalex/candv/releases/tag/v1.0.0
