# -*- coding: utf-8 -*-
import unittest

from candv.base import Constant, ConstantsContainer


class ConstantsContainerTestCase(unittest.TestCase):

    def test_container_instantiation(self):

        with self.assertRaises(TypeError) as cm:
            ConstantsContainer()

        self.assertEqual(
            cm.exception.args[0],
            "\"<constants container 'ConstantsContainer'>\" cannot be "
            "instantiated, because constant containers are not designed for "
            "this."
        )

    def _get_container(self):

        class FOO(ConstantsContainer):
            CONSTANT2 = Constant()
            CONSTANT3 = Constant()
            CONSTANT1 = Constant()

        return FOO

    def test_group_name(self):
        FOO = self._get_container()
        self.assertEquals(FOO.name, 'FOO')

    def test_group_full_name(self):
        FOO = self._get_container()
        self.assertEquals(FOO.full_name, 'FOO')

    def test_group_repr(self):
        FOO = self._get_container()
        self.assertEquals(repr(FOO), "<constants container 'FOO'>")

    def test_names(self):
        FOO = self._get_container()
        self.assertEquals(
            FOO.names(),
            ['CONSTANT2', 'CONSTANT3', 'CONSTANT1', ]
        )

    def test_iternames(self):
        FOO = self._get_container()
        self.assertEquals(
            list(FOO.iternames()),
            ['CONSTANT2', 'CONSTANT3', 'CONSTANT1', ]
        )

    def test_constants(self):
        FOO = self._get_container()
        self.assertEquals(
            FOO.constants(),
            [FOO.CONSTANT2, FOO.CONSTANT3, FOO.CONSTANT1, ]
        )

    def test_iterconstants(self):
        FOO = self._get_container()
        self.assertEquals(
            list(FOO.iterconstants()),
            [FOO.CONSTANT2, FOO.CONSTANT3, FOO.CONSTANT1, ]
        )

    def test_items(self):
        FOO = self._get_container()
        self.assertEquals(
            FOO.items(),
            [
                ('CONSTANT2', FOO.CONSTANT2),
                ('CONSTANT3', FOO.CONSTANT3),
                ('CONSTANT1', FOO.CONSTANT1),
            ]
        )

    def test_iteritems(self):
        FOO = self._get_container()
        self.assertEquals(
            list(FOO.iteritems()),
            [
                ('CONSTANT2', FOO.CONSTANT2),
                ('CONSTANT3', FOO.CONSTANT3),
                ('CONSTANT1', FOO.CONSTANT1),
            ]
        )

    def test_contains(self):
        FOO = self._get_container()
        self.assertTrue(FOO.contains('CONSTANT2'))
        self.assertFalse(FOO.contains('CONSTANT_X'))

    def test_get_by_name(self):
        FOO = self._get_container()

        self.assertEquals(
            FOO.get_by_name('CONSTANT2'),
            FOO.CONSTANT2
        )

        with self.assertRaises(KeyError) as cm:
            FOO.get_by_name('CONSTANT_X')
        self.assertEqual(
            cm.exception.args[0],
            "Constant \"CONSTANT_X\" is not present in "
            "\"<constants container 'FOO'>\""
        )

    def test_invalid_constant_class(self):

        with self.assertRaises(TypeError) as cm:

            class FOO(ConstantsContainer):
                constant_class = int

        self.assertEqual(
            cm.exception.args[0],
            "\"<type 'int'>\" which is used as \"constant_class\" for "
            "\"<constants container 'FOO'>\" must be derived from "
            "\"<class 'candv.base.Constant'>\"."
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


class ConstantTestCase(unittest.TestCase):

    def test_creation_counter(self):
        value = Constant._creation_counter
        Constant()
        self.assertEquals(Constant._creation_counter, value + 1)

    def test_name(self):

        class FOO(ConstantsContainer):
            CONSTANT = Constant()

        self.assertEquals(FOO.CONSTANT.name, 'CONSTANT')

    def test_full_name(self):

        class FOO(ConstantsContainer):
            CONSTANT = Constant()

        self.assertEquals(FOO.CONSTANT.full_name, 'FOO.CONSTANT')

    def test_repr(self):

        class FOO(ConstantsContainer):
            CONSTANT = Constant()

        self.assertEquals(repr(FOO.CONSTANT), "<constant 'FOO.CONSTANT'>")

    def test_container(self):
        constant = Constant()
        self.assertIsNone(constant.container)

        class FOO(ConstantsContainer):
            CONSTANT = Constant()

        self.assertEquals(FOO.CONSTANT.container, FOO)


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

    def test_container_names(self):
        FOO = self._get_group()
        self.assertEquals(
            FOO.names(),
            ['A', 'B', ]
        )

    def test_get_by_name_from_container(self):
        FOO = self._get_group()
        self.assertEquals(
            FOO.get_by_name('B'),
            FOO.B
        )

    def test_group_name(self):
        FOO = self._get_group()
        self.assertEquals(FOO.B.name, 'B')

    def test_group_full_name(self):
        FOO = self._get_group()
        self.assertEquals(FOO.B.full_name, 'FOO.B')

    def test_group_repr(self):
        FOO = self._get_group()
        self.assertEquals(
            repr(FOO.B),
            "<constants group 'FOO.B'>"
        )

    def test_group_container(self):
        FOO = self._get_group()
        self.assertEquals(FOO.B.container, FOO)

    def test_group_as_container(self):
        FOO = self._get_group()
        self.assertEquals(FOO.B.B2.container, FOO.B)

    def test_group_names(self):
        FOO = self._get_group()
        self.assertEquals(
            FOO.B.names(),
            ['B2', 'B0', 'B1', ]
        )

    def test_get_by_name_from_group(self):
        FOO = self._get_group()
        self.assertEquals(
            FOO.B.get_by_name('B0'),
            FOO.B.B0
        )

    def test_group_member_full_name(self):
        FOO = self._get_group()
        self.assertEquals(FOO.B.B2.full_name, 'FOO.B.B2')

    def test_invalid_group(self):
        with self.assertRaises(TypeError) as cm:

            class FOO(ConstantsContainer):
                A = Constant().to_group(
                    group_class=ConstantsContainer,
                    B=Constant(),
                    C=1)

        self.assertEqual(
            cm.exception.args[0],
            "\"1\" cannot be a member of a group. Only instances of "
            "\"<class 'candv.base.Constant'>\" or other groups can be."
        )