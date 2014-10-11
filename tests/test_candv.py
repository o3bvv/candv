# -*- coding: utf-8 -*-
import unittest

from candv import (
    Constants, SimpleConstant, VerboseConstant,
    Values, ValueConstant, VerboseValueConstant,
)


class VerboseConstantTestCase(unittest.TestCase):

    def _create_constant(self, *args, **kwargs):

        class FOO(Constants):
            CONSTANT = VerboseConstant(*args, **kwargs)

        return FOO.CONSTANT

    def test_no_args(self):
        constant = self._create_constant()
        self.assertEquals(constant.name, 'CONSTANT')
        self.assertEquals(constant.full_name, 'FOO.CONSTANT')
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
        self.assertEquals(constant.full_name, 'FOO.CONSTANT')
        self.assertEquals(constant.verbose_name, "foo")
        self.assertEquals(constant.help_text, "just test constant")


class ConstantsTestCase(unittest.TestCase):

    def test_one_constant_class(self):

        class FOO(Constants):
            two = SimpleConstant()
            one = SimpleConstant()

        self.assertEquals(
            [x.name for x in FOO.iterconstants()],
            ['two', 'one', ]
        )

    def test_one_constant_name(self):

        class FOO(Constants):
            one = SimpleConstant()
            one = SimpleConstant()

        self.assertEquals(
            [x.name for x in FOO.iterconstants()],
            ['one', ]
        )

    def test_mixed_constant_classes(self):

        class FOO(Constants):
            two = VerboseConstant("2", "just two")
            one = SimpleConstant()
            four = ValueConstant(4)
            three = VerboseValueConstant(3, "three", "just three")

        self.assertEquals(
            [x.name for x in FOO.iterconstants()],
            ['two', 'one', 'four', 'three', ]
        )


class ValuesTestCase(unittest.TestCase):

    def test_get_by_value(self):

        class FOO(Values):
            ONE = ValueConstant(1)
            TWO = ValueConstant(2)
            ONE_DUB = ValueConstant(1)

        self.assertEquals(FOO.get_by_value(1), FOO.ONE)
        self.assertEquals(FOO.get_by_value(2), FOO.get_by_name('TWO'))

        with self.assertRaises(ValueError) as cm:
            FOO.get_by_value(3)
        self.assertEqual(
            cm.exception.message,
            "Constant with value \"3\" is not present in "
            "\"<constants container 'FOO'>\""
        )

    def test_filter_by_value(self):

        class FOO(Values):
            ONE = ValueConstant(1)
            TWO = ValueConstant(2)
            ONE_DUB2 = ValueConstant(1)
            THREE = ValueConstant(3)
            ONE_DUB1 = ValueConstant(1)

        self.assertEquals(
            [x.name for x in FOO.filter_by_value(1)],
            ['ONE', 'ONE_DUB2', 'ONE_DUB1', ]
        )

    def test_values(self):

        class FOO(Values):
            ONE = ValueConstant(1)
            FOUR = ValueConstant(4)
            THREE = ValueConstant(3)

        self.assertEquals(
            FOO.values(),
            [1, 4, 3, ]
        )

    def test_itervalues(self):

        class FOO(Values):
            ONE = ValueConstant(1)
            FOUR = ValueConstant(4)
            THREE = ValueConstant(3)

        self.assertEquals(
            list(FOO.itervalues()),
            [1, 4, 3, ]
        )


class GrouppingTestCase(unittest.TestCase):

    def test_verbose_group(self):

        class FOO(Constants):
            A = SimpleConstant()
            B = VerboseConstant(
                verbose_name="Constant B",
                help_text="Just a group with verbose name"
            ).to_group(
                group_class=Constants,
                C=SimpleConstant(),
                D=SimpleConstant(),
            )

        self.assertEquals(FOO.B.verbose_name, "Constant B")
        self.assertEquals(FOO.B.help_text, "Just a group with verbose name")
        self.assertEquals(
            FOO.B.names(),
            ['C', 'D', ]
        )

    def test_valuable_group(self):

        class FOO(Constants):
            A = SimpleConstant()
            B = ValueConstant(10).to_group(
                group_class=Constants,
                C=SimpleConstant(),
                D=SimpleConstant(),
            )

        self.assertEquals(FOO.B.value, 10)
        self.assertEquals(
            FOO.B.names(),
            ['C', 'D', ]
        )

    def test_valuable_verbose_group(self):

        class FOO(Constants):
            A = SimpleConstant()
            B = VerboseValueConstant(
                value=10,
                verbose_name="Constant B",
                help_text="Just a group with verbose name"
            ).to_group(
                group_class=Constants,
                C=SimpleConstant(),
                D=SimpleConstant(),
            )

        self.assertEquals(FOO.B.value, 10)
        self.assertEquals(FOO.B.verbose_name, "Constant B")
        self.assertEquals(FOO.B.help_text, "Just a group with verbose name")
        self.assertEquals(
            FOO.B.names(),
            ['C', 'D', ]
        )
