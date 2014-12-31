# -*- coding: utf-8 -*-

import unittest

from datetime import date
from candv import (
    Constants, SimpleConstant, VerboseConstant, Values, ValueConstant,
    VerboseValueConstant,
)


class VerboseConstantTestCase(unittest.TestCase):

    def _create_constant(self, *args, **kwargs):

        class FOO(Constants):
            CONSTANT = VerboseConstant(*args, **kwargs)

        return FOO.CONSTANT

    def test_no_args(self):
        constant = self._create_constant()
        self.assertEqual(constant.name, 'CONSTANT')
        self.assertEqual(constant.full_name, 'FOO.CONSTANT')
        self.assertIsNone(constant.verbose_name)
        self.assertIsNone(constant.help_text)

    def test_versose_name(self):
        constant = VerboseConstant(verbose_name="foo")
        self.assertEqual(constant.verbose_name, "foo")

    def test_help_text(self):
        constant = VerboseConstant(help_text="just test constant")
        self.assertEqual(constant.help_text, "just test constant")

    def test_all_args(self):
        constant = self._create_constant("foo", "just test constant")
        self.assertEqual(constant.name, 'CONSTANT')
        self.assertEqual(constant.full_name, 'FOO.CONSTANT')
        self.assertEqual(constant.verbose_name, "foo")
        self.assertEqual(constant.help_text, "just test constant")

    def test_to_primitive(self):
        constant = self._create_constant()
        self.assertEqual(
            constant.to_primitive(),
            {
                'name': 'CONSTANT',
                'verbose_name': None,
                'help_text': None,
            }
        )

        constant = self._create_constant("Constant", "A test constant")
        self.assertEqual(
            constant.to_primitive(),
            {
                'name': 'CONSTANT',
                'verbose_name': "Constant",
                'help_text': "A test constant",
            }
        )


class ConstantsTestCase(unittest.TestCase):

    def test_one_constant_class(self):

        class FOO(Constants):
            two = SimpleConstant()
            one = SimpleConstant()

        self.assertEqual(
            [x.name for x in FOO.iterconstants()],
            ['two', 'one', ]
        )

    def test_one_constant_name(self):

        class FOO(Constants):
            one = SimpleConstant()
            one = SimpleConstant()

        self.assertEqual([x.name for x in FOO.iterconstants()], ['one', ])

    def test_mixed_constant_classes(self):

        class FOO(Constants):
            two = VerboseConstant("2", "just two")
            one = SimpleConstant()
            four = ValueConstant(4)
            three = VerboseValueConstant(3, "three", "just three")

        self.assertEqual(
            [x.name for x in FOO.iterconstants()],
            ['two', 'one', 'four', 'three', ]
        )

    def test_mixed_constant_classes_less_generic(self):

        class FOO(Values):
            two = VerboseConstant("2", "just two")
            one = SimpleConstant()
            four = ValueConstant(4)
            three = VerboseValueConstant(3, "three", "just three")

        self.assertEqual(
            [x.name for x in FOO.iterconstants()],
            ['four', 'three', ]
        )

    def test_unbound_constant(self):

        class FOO(Values):
            one = SimpleConstant()
            two = ValueConstant(2)

        self.assertEqual([x.name for x in FOO.iterconstants()], ['two', ])
        self.assertEqual(FOO.one.name, 'one')
        self.assertEqual(FOO.one.full_name, '__UNBOUND__.one')
        self.assertEqual(repr(FOO.one), "<constant '__UNBOUND__.one'>")


class ValuesTestCase(unittest.TestCase):

    def test_get_by_value(self):

        class FOO(Values):
            ONE = ValueConstant(1)
            TWO = ValueConstant(2)
            ONE_DUB = ValueConstant(1)

        self.assertEqual(FOO.get_by_value(1), FOO.ONE)
        self.assertEqual(FOO.get_by_value(2), FOO.get('TWO'))

        with self.assertRaises(ValueError) as cm:
            FOO.get_by_value(3)

        self.assertEqual(
            cm.exception.args[0],
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

        self.assertEqual(
            [x.name for x in FOO.filter_by_value(1)],
            ['ONE', 'ONE_DUB2', 'ONE_DUB1', ]
        )

    def test_values(self):

        class FOO(Values):
            ONE = ValueConstant(1)
            FOUR = ValueConstant(4)
            THREE = ValueConstant(3)

        self.assertEqual(FOO.values(), [1, 4, 3, ])

    def test_itervalues(self):

        class FOO(Values):
            ONE = ValueConstant(1)
            FOUR = ValueConstant(4)
            THREE = ValueConstant(3)

        self.assertEqual(list(FOO.itervalues()), [1, 4, 3, ])

    def test_to_primitive(self):

        class FOO(Values):
            ONE = ValueConstant(1)
            TWO = ValueConstant(lambda: 2)
            DATE = ValueConstant(date(1999, 12, 31))

        self.assertEqual(
            FOO.ONE.to_primitive(),
            {'name': 'ONE', 'value': 1, }
        )
        self.assertEqual(
            FOO.TWO.to_primitive(),
            {'name': 'TWO', 'value': 2, }
        )
        self.assertEqual(
            FOO.DATE.to_primitive(),
            {'name': 'DATE', 'value': '1999-12-31', }
        )
        self.assertEqual(
            FOO.to_primitive(),
            {
                'name': 'FOO',
                'items': [
                    {'name': 'ONE', 'value': 1, },
                    {'name': 'TWO', 'value': 2, },
                    {'name': 'DATE', 'value': '1999-12-31', },
                ]
            }
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

        self.assertEqual(FOO.B.verbose_name, "Constant B")
        self.assertEqual(FOO.B.help_text, "Just a group with verbose name")
        self.assertEqual(FOO.B.names(), ['C', 'D', ])
        self.assertEqual(
            FOO.to_primitive(),
            {
                'name': "FOO",
                'items': [
                    {'name': "A", },
                    {
                        'name': "B",
                        'verbose_name': "Constant B",
                        'help_text': "Just a group with verbose name",
                        'items': [
                            {'name': "C", },
                            {'name': "D", },
                        ],
                    },
                ]
            }
        )

    def test_valuable_group(self):

        class FOO(Constants):
            A = SimpleConstant()
            B = ValueConstant(10).to_group(
                group_class=Constants,
                C=SimpleConstant(),
                D=SimpleConstant(),
            )

        self.assertEqual(FOO.B.value, 10)
        self.assertEqual(FOO.B.names(), ['C', 'D', ])
        self.assertEqual(
            FOO.to_primitive(),
            {
                'name': "FOO",
                'items': [
                    {'name': "A", },
                    {
                        'name': "B",
                        'value': 10,
                        'items': [
                            {'name': "C", },
                            {'name': "D", },
                        ],
                    },
                ]
            }
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

        self.assertEqual(FOO.B.value, 10)
        self.assertEqual(FOO.B.verbose_name, "Constant B")
        self.assertEqual(FOO.B.help_text, "Just a group with verbose name")
        self.assertEqual(FOO.B.names(), ['C', 'D', ])
        self.assertEqual(
            FOO.to_primitive(),
            {
                'name': "FOO",
                'items': [
                    {'name': "A", },
                    {
                        'name': "B",
                        'verbose_name': "Constant B",
                        'help_text': "Just a group with verbose name",
                        'value': 10,
                        'items': [
                            {'name': "C", },
                            {'name': "D", },
                        ],
                    },
                ]
            }
        )
