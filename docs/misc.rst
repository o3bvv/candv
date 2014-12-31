Misc
====

This chapter covers miscellaneous things which are not related to the library
usage.


Tests
^^^^^

See the output of tests execution at `Travis CI`_.

If you need to run tests locally, you need to have `nose`_ installed. Then
just run

::

    $ nosetests

to run all tests inside the project.

Visit `Coveralls`_ to see the tests coverage online.

If you need to see coverage locally, install `coverage`_ additionally. Then
run::

    $ coverage run `which nosetests` --nocapture && coverage report -m


Building docs
^^^^^^^^^^^^^

If you need to have a local copy of these docs, you will need to install
`Sphinx`_ and `make`_. Then::

    $ cd docs
    $ make html

This will render docs in ``HTML`` format to ``docs/_build/html`` directory.

To see all available output formats, run::

    $ make help


.. _Travis CI: https://travis-ci.org/oblalex/candv
.. _nose: https://nose.readthedocs.org/en/latest/
.. _Coveralls: https://coveralls.io/r/oblalex/candv?branch=master
.. _coverage: http://nedbatchelder.com/code/coverage/
.. _Sphinx: http://sphinx-doc.org/
.. _make: http://www.gnu.org/software/make/
