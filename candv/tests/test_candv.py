# -*- coding: utf-8 -*-
import unittest

from candv import (Constants, SimpleConstant, VerboseConstant, Values,
    ValueConstant, VerboseValueConstant, )


class VerboseConstantTestCase(unittest.TestCase):

    def _create_constant(self, *args, **kwargs):

        class FOO(Constants):
            CONSTANT = VerboseConstant(*args, **kwargs)

        return FOO.CONSTANT

    def test_no_args(self):
        constant = self._create_constant()
        self.assertEquals(constant.name, 'CONSTANT')
        self.assertIsNone(constant.verbose_name)
        self.assertIsNone(constant.help_text)

    def test_versose_name(self):
        constant = VerboseConstant(verbose_name="foo")
        self.assertEquals(constant.verbose_name, "foo")

    def test_help_text(self):
        constant = VerboseConstant(help_text="just test constant")
        self.assertEquals(constant.help_text, "just test constant")

    def test_all_args(self):
        constant = self._create_constant("foo", "just test constant")
        self.assertEquals(constant.name, 'CONSTANT')
        self.assertEquals(constant.verbose_name, "foo")
        self.assertEquals(constant.help_text, "just test constant")


class ConstantsTestCase(unittest.TestCase):

    def test_one_constant_class(self):

        class FOO(Constants):
            two = SimpleConstant()
            one = SimpleConstant()

        names = [x.name for x in FOO.iterconstants()]
        self.assertEquals(names, ['two', 'one', ])

    def test_one_constant_name(self):

        class FOO(Constants):
            one = SimpleConstant()
            one = SimpleConstant()

        names = [x.name for x in FOO.iterconstants()]
        self.assertEquals(names, ['one', ])

    def test_mixed_constant_classes(self):

        class FOO(Constants):
            two = VerboseConstant("2", "just two")
            one = SimpleConstant()
            four = ValueConstant(4)
            three = VerboseValueConstant(3, "three", "just three")

        names = [x.name for x in FOO.iterconstants()]
        self.assertEquals(names, ['two', 'one', 'four', 'three', ])

    def test_invalid_container(self):

        def define_classes():
            class FOO(Constants):
                one = SimpleConstant()

            class BAR(Constants):
                one = FOO.one

        self.assertRaises(ValueError, define_classes)


class ValuesTestCase(unittest.TestCase):

    def test_get_by_value(self):

        class FOO(Values):
            ONE = ValueConstant(1)
            TWO = ValueConstant(2)
            ONE_DUB1 = ValueConstant(1)

        self.assertEquals(FOO.get_by_value(1), FOO.ONE)
        self.assertEquals(FOO.get_by_value(2), FOO.get_by_name('TWO'))
        self.assertRaises(ValueError, FOO.get_by_value, 3)

    def test_filter_by_value(self):

        class FOO(Values):
            ONE = ValueConstant(1)
            TWO = ValueConstant(2)
            ONE_DUB2 = ValueConstant(1)
            THREE = ValueConstant(3)
            ONE_DUB1 = ValueConstant(1)

        names = [x.name for x in FOO.filter_by_value(1)]
        self.assertEquals(names, ['ONE', 'ONE_DUB2', 'ONE_DUB1', ])

    def test_values(self):

        class FOO(Values):
            ONE = ValueConstant(1)
            FOUR = ValueConstant(4)
            THREE = ValueConstant(3)

        self.assertEquals(FOO.values(), [1, 4, 3, ])

    def test_itervalues(self):

        class FOO(Values):
            ONE = ValueConstant(1)
            FOUR = ValueConstant(4)
            THREE = ValueConstant(3)

        self.assertEquals(list(FOO.itervalues()), [1, 4, 3, ])
