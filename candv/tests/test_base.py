# -*- coding: utf-8 -*-
import unittest

from candv.base import Constant, ConstantsContainer


class ConstantsContainerTestCase(unittest.TestCase):

    def test_singleton(self):

        def create_instance():
            ConstantsContainer()

        self.assertRaises(TypeError, create_instance)

    def test_iterconstants(self):

        class FOO(ConstantsContainer):
            constant_class = Constant

            CONSTANT2 = Constant()
            CONSTANT3 = Constant()
            CONSTANT1 = Constant()

        names = [x.name for x in FOO.iterconstants()]
        self.assertEquals(names, ['CONSTANT2', 'CONSTANT3', 'CONSTANT1', ])

    def test_iterconstants_with_no_class(self):
        self.assertRaises(AttributeError, ConstantsContainer.iterconstants)

    def test_find_by_name(self):

        class FOO(ConstantsContainer):
            constant_class = Constant

            CONSTANT2 = Constant()
            CONSTANT1 = Constant()

        self.assertEquals(FOO.find_by_name('CONSTANT2'), FOO.CONSTANT2)
        self.assertRaises(KeyError, FOO.find_by_name, 'CONSTANT_X')

    def test_find_by_name_with_no_class(self):
        self.assertRaises(AttributeError,
                          ConstantsContainer.find_by_name, 'CONSTANT_X')

    def test_invalid_constant_class(self):

        def define_class():
            class FOO(ConstantsContainer):
                constant_class = int

        self.assertRaises(TypeError, define_class)

    def test_invalid_container(self):

        def define_classes():

            class A(ConstantsContainer):
                constant_class = Constant

                FOO = Constant()
                BAR = Constant()

            class B(ConstantsContainer):
                constant_class = Constant

                FOO = Constant()
                BAR = A.BAR

        self.assertRaises(ValueError, define_classes)


class ConstantTestCase(unittest.TestCase):

    def test_creation_counter(self):
        value = Constant._creation_counter
        Constant()
        self.assertEquals(Constant._creation_counter, value + 1)

    def test_container(self):

        constant = Constant()
        self.assertIsNone(constant._container)

        class FOO(ConstantsContainer):
            constant_class = Constant
            CONSTANT = Constant()

        self.assertEquals(FOO.CONSTANT._container, FOO)

    def test_name(self):

        class FOO(ConstantsContainer):
            constant_class = Constant
            CONSTANT = Constant()

        self.assertEquals(FOO.CONSTANT.name, 'CONSTANT')

    def test_repr(self):

        class FOO(ConstantsContainer):
            constant_class = Constant
            CONSTANT = Constant()

        self.assertEquals(repr(FOO.CONSTANT), "<constant 'FOO.CONSTANT'>")
