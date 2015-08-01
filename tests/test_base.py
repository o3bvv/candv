# -*- coding: utf-8 -*-

import os
import sys
import unittest

from candv.base import Constant, ConstantsContainer, with_constant_class


class ConstantsContainerTestCase(unittest.TestCase):

    def test_container_instantiation(self):

        with self.assertRaises(TypeError) as cm:
            ConstantsContainer()

        self.assertEqual(
            cm.exception.args[0],
            "\"<constants container 'ConstantsContainer'>\" cannot be "
            "instantiated, because constant containers are not designed for "
            "that."
        )

    def _get_container(self):

        class FOO(ConstantsContainer):
            CONSTANT2 = Constant()
            CONSTANT3 = Constant()
            CONSTANT1 = Constant()

        return FOO

    def test_name(self):
        FOO = self._get_container()
        self.assertEqual(FOO.name, 'FOO')

    def test_full_name(self):
        FOO = self._get_container()
        self.assertEqual(FOO.full_name, 'FOO')

    def test_repr(self):
        FOO = self._get_container()
        self.assertEqual(repr(FOO), "<constants container 'FOO'>")

    def test_names(self):
        FOO = self._get_container()
        self.assertEqual(
            FOO.names(),
            ['CONSTANT2', 'CONSTANT3', 'CONSTANT1', ]
        )

    def test_iternames(self):
        FOO = self._get_container()
        self.assertEqual(
            list(FOO.iternames()),
            ['CONSTANT2', 'CONSTANT3', 'CONSTANT1', ]
        )

    def test_values(self):
        FOO = self._get_container()
        self.assertEqual(
            FOO.values(),
            [FOO.CONSTANT2, FOO.CONSTANT3, FOO.CONSTANT1, ]
        )

    def test_itervalues(self):
        FOO = self._get_container()
        self.assertEqual(
            list(FOO.itervalues()),
            [FOO.CONSTANT2, FOO.CONSTANT3, FOO.CONSTANT1, ]
        )

    def test_constants(self):
        FOO = self._get_container()
        self.assertEqual(
            FOO.constants(),
            [FOO.CONSTANT2, FOO.CONSTANT3, FOO.CONSTANT1, ]
        )

    def test_iterconstants(self):
        FOO = self._get_container()
        self.assertEqual(
            list(FOO.iterconstants()),
            [FOO.CONSTANT2, FOO.CONSTANT3, FOO.CONSTANT1, ]
        )

    def test_items(self):
        FOO = self._get_container()
        self.assertEqual(
            FOO.items(),
            [
                ('CONSTANT2', FOO.CONSTANT2),
                ('CONSTANT3', FOO.CONSTANT3),
                ('CONSTANT1', FOO.CONSTANT1),
            ]
        )

    def test_iteritems(self):
        FOO = self._get_container()
        self.assertEqual(
            list(FOO.iteritems()),
            [
                ('CONSTANT2', FOO.CONSTANT2),
                ('CONSTANT3', FOO.CONSTANT3),
                ('CONSTANT1', FOO.CONSTANT1),
            ]
        )

    def test_iter(self):
        FOO = self._get_container()
        for x, y in zip(FOO, FOO.iternames()):
            self.assertEqual(x, y)

    def test_len(self):
        FOO = self._get_container()
        self.assertEqual(len(FOO), 3)

    def test_contains(self):
        FOO = self._get_container()
        self.assertTrue('CONSTANT2' in FOO)
        self.assertFalse('CONSTANT_X' in FOO)

    def test_has_name(self):
        FOO = self._get_container()
        self.assertTrue(FOO.has_name('CONSTANT2'))
        self.assertFalse(FOO.has_name('CONSTANT_X'))

    def test_get_item(self):
        FOO = self._get_container()
        self.assertEqual(FOO['CONSTANT2'], FOO.CONSTANT2)

        with self.assertRaises(KeyError) as cm:
            FOO['CONSTANT_X']
        self.assertEqual(
            cm.exception.args[0],
            "Constant \"CONSTANT_X\" is not present in "
            "\"<constants container 'FOO'>\""
        )

    def test_get(self):
        FOO = self._get_container()
        self.assertEqual(FOO.get('CONSTANT2'), FOO.CONSTANT2)
        self.assertEqual(FOO.get('CONSTANT_X'), None)

    def test_invalid_constant_class(self):

        with self.assertRaises(TypeError) as cm:

            class FOO(ConstantsContainer):
                constant_class = int

        self.assertEqual(
            cm.exception.args[0],
            "\"{0}\" which is used as \"constant_class\" for "
            "\"<constants container 'FOO'>\" must be derived from "
            "\"<class 'candv.base.Constant'>\".".format(repr(int))
        )

    def test_reuse_of_constant(self):

        with self.assertRaises(ValueError) as cm:

            class A(ConstantsContainer):
                FOO = Constant()
                BAR = Constant()

            class B(ConstantsContainer):
                FOO = Constant()
                BAR = A.BAR

        self.assertEqual(
            cm.exception.args[0],
            "Cannot use \"<constant 'A.BAR'>\" as value for the attribute "
            "\"BAR\" for \"<constants container 'B'>\", because "
            "\"<constant 'A.BAR'>\" already belongs to "
            "\"<constants container 'A'>\"."
        )

    def test_constant_class_mixin_factory(self):

        class SomeConstant(Constant):
            pass

        class FOO(with_constant_class(SomeConstant), ConstantsContainer):
            A = SomeConstant()
            B = SomeConstant()
            C = Constant()

        self.assertEqual(FOO.constant_class, SomeConstant)
        self.assertEqual(FOO.constants(), [FOO.A, FOO.B, ])

    def test_to_primitive(self):

        class FOO(ConstantsContainer):
            ONE = Constant()
            TWO = Constant()
            TREE = Constant()

        self.assertEqual(
            FOO.to_primitive(),
            {
                'name': 'FOO',
                'items': [
                    {'name': 'ONE', },
                    {'name': 'TWO', },
                    {'name': 'TREE', },
                ]
            }
        )


class ConstantTestCase(unittest.TestCase):

    def test_creation_counter(self):
        value = Constant._creation_counter
        Constant()
        self.assertEqual(Constant._creation_counter, value + 1)

    def test_name(self):

        class FOO(ConstantsContainer):
            CONSTANT = Constant()

        self.assertEqual(FOO.CONSTANT.name, 'CONSTANT')

    def test_full_name(self):

        class FOO(ConstantsContainer):
            CONSTANT = Constant()

        self.assertEqual(FOO.CONSTANT.full_name, 'FOO.CONSTANT')

    def test_repr(self):

        class FOO(ConstantsContainer):
            CONSTANT = Constant()

        self.assertEqual(repr(FOO.CONSTANT), "<constant 'FOO.CONSTANT'>")

    def test_container(self):
        constant = Constant()
        self.assertIsNone(constant.container)

        class FOO(ConstantsContainer):
            CONSTANT = Constant()

        self.assertEqual(FOO.CONSTANT.container, FOO)

    def test_to_primitive(self):

        class FOO(ConstantsContainer):
            CONSTANT = Constant()

        self.assertEqual(FOO.CONSTANT.to_primitive(), {'name': 'CONSTANT'})


class GrouppingTestCase(unittest.TestCase):

    def _get_group(self):
        class FOO(ConstantsContainer):
            A = Constant()
            B = Constant().to_group(
                group_class=ConstantsContainer,
                B2=Constant(),
                B0=Constant(),
                B1=Constant(),
            )

        return FOO

    def test_group_name(self):
        FOO = self._get_group()
        self.assertEqual(FOO.B.name, 'B')

    def test_group_full_name(self):
        FOO = self._get_group()
        self.assertEqual(FOO.B.full_name, 'FOO.B')

    def test_group_repr(self):
        FOO = self._get_group()
        self.assertEqual(repr(FOO.B), "<constants group 'FOO.B'>")

    def test_group_names(self):
        FOO = self._get_group()
        self.assertEqual(
            FOO.B.names(),
            ['B2', 'B0', 'B1', ]
        )

    def test_group_iternames(self):
        FOO = self._get_group()
        self.assertEqual(
            list(FOO.B.iternames()),
            ['B2', 'B0', 'B1', ]
        )

    def test_group_values(self):
        FOO = self._get_group()
        self.assertEqual(
            FOO.B.values(),
            [FOO.B.B2, FOO.B.B0, FOO.B.B1, ]
        )

    def test_group_itervalues(self):
        FOO = self._get_group()
        self.assertEqual(
            list(FOO.B.itervalues()),
            [FOO.B.B2, FOO.B.B0, FOO.B.B1, ]
        )

    def test_group_constants(self):
        FOO = self._get_group()
        self.assertEqual(
            FOO.B.constants(),
            [FOO.B.B2, FOO.B.B0, FOO.B.B1, ]
        )

    def test_group_iterconstants(self):
        FOO = self._get_group()
        self.assertEqual(
            list(FOO.B.iterconstants()),
            [FOO.B.B2, FOO.B.B0, FOO.B.B1, ]
        )

    def test_group_items(self):
        FOO = self._get_group()
        self.assertEqual(
            FOO.B.items(),
            [
                ('B2', FOO.B.B2),
                ('B0', FOO.B.B0),
                ('B1', FOO.B.B1),
            ]
        )

    def test_group_iteritems(self):
        FOO = self._get_group()
        self.assertEqual(
            list(FOO.B.iteritems()),
            [
                ('B2', FOO.B.B2),
                ('B0', FOO.B.B0),
                ('B1', FOO.B.B1),
            ]
        )

    def test_group_iter(self):
        FOO = self._get_group()
        for x, y in zip(FOO.B, FOO.B.iternames()):
            self.assertEqual(x, y)

    def test_group_len(self):
        FOO = self._get_group()
        self.assertEqual(len(FOO.B), 3)

    def test_group_contains(self):
        FOO = self._get_group()
        self.assertTrue('B2' in FOO.B)
        self.assertFalse('B_X' in FOO.B)

    def test_group_has_name(self):
        FOO = self._get_group()
        self.assertTrue(FOO.B.has_name('B2'))
        self.assertFalse(FOO.B.has_name('B_X'))

    def test_group_get_item(self):
        FOO = self._get_group()
        self.assertEqual(FOO.B['B2'], FOO.B.B2)

        with self.assertRaises(KeyError) as cm:
            FOO.B['B_X']

        self.assertEqual(
            cm.exception.args[0],
            "Constant \"B_X\" is not present in "
            "\"<constants group 'FOO.B'>\""
        )

    def test_group_get(self):
        FOO = self._get_group()
        self.assertEqual(FOO.B.get('B2'), FOO.B.B2)
        self.assertEqual(FOO.B.get('B_X'), None)

    def test_group_container(self):
        FOO = self._get_group()
        self.assertEqual(FOO.B.container, FOO)

    def test_group_as_container(self):
        FOO = self._get_group()
        self.assertEqual(FOO.B.B2.container, FOO.B)

    def test_container_names(self):
        FOO = self._get_group()
        self.assertEqual(FOO.names(), ['A', 'B', ])

    def test_get_from_container(self):
        FOO = self._get_group()
        self.assertEqual(FOO['B'], FOO.B)

    def test_group_member_full_name(self):
        FOO = self._get_group()
        self.assertEqual(FOO.B.B2.full_name, 'FOO.B.B2')

    def test_invalid_group(self):
        with self.assertRaises(TypeError) as cm:

            class FOO(ConstantsContainer):
                A = Constant().to_group(
                    group_class=ConstantsContainer,
                    B=Constant(),
                    C=1
                )

        self.assertEqual(
            cm.exception.args[0],
            "\"1\" cannot be a member of a group. Only instances of "
            "\"<class 'candv.base.Constant'>\" or other groups can be."
        )

    def test_to_primitive(self):
        self.assertEqual(
            self._get_group().to_primitive(),
            {
                'name': 'FOO',
                'items': [
                    {'name': 'A', },
                    {
                        'name': 'B',
                        'items': [
                            {'name': 'B2', },
                            {'name': 'B0', },
                            {'name': 'B1', },
                        ]
                    },
                ]
            }
        )

    def test_comparison(self):
        sys.path.insert(
            0,
            os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                'package',
            )
        )
        from .package.subpackage.constants import CONSTANTS
        from subpackage.constants import CONSTANTS as SUBCONSTANTS

        self.assertNotEqual(CONSTANTS.__module__, SUBCONSTANTS.__module__)
        self.assertEqual(CONSTANTS.PRIMARY, SUBCONSTANTS.PRIMARY)
