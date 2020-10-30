import pickle
import sys
import unittest

from collections.abc import Iterable
from collections.abc import Iterator

from pathlib import Path

from candv.core import Constants
from candv.core import SimpleConstant
from candv.core import with_constant_class

from candv.exceptions import CandvConstantAlreadyBoundError
from candv.exceptions import CandvContainerMisusedError
from candv.exceptions import CandvInvalidConstantClass
from candv.exceptions import CandvInvalidGroupMemberError
from candv.exceptions import CandvMissingConstantError


class ConstantsTestCase(unittest.TestCase):

  def test_container_instantiation(self):

    with self.assertRaises(CandvContainerMisusedError) as cm:
      Constants()

    self.assertEqual(
      cm.exception.args[0],
      (
        "\"<constants container 'Constants'>\" cannot be instantiated: "
        "constant containers are not designed for that"
      ),
    )

  def test_name(self):

    class FOO(Constants):
      ...

    self.assertEqual(FOO.name, "FOO")

  def test_full_name(self):

    class FOO(Constants):
      ...

    self.assertEqual(FOO.full_name, "FOO")

  def test_repr(self):

    class FOO(Constants):
      ...

    self.assertEqual(repr(FOO), "<constants container 'FOO'>")

  def test_names(self):

    class FOO(Constants):
      CONSTANT_2 = SimpleConstant()
      CONSTANT_3 = SimpleConstant()
      CONSTANT_1 = SimpleConstant()

    names = FOO.names()

    self.assertIsInstance(names, list)
    self.assertEqual(
      names,
      [
        "CONSTANT_2",
        "CONSTANT_3",
        "CONSTANT_1",
      ],
    )

  def test_iternames(self):

    class FOO(Constants):
      CONSTANT_2 = SimpleConstant()
      CONSTANT_3 = SimpleConstant()
      CONSTANT_1 = SimpleConstant()

    names = FOO.iternames()

    self.assertIsInstance(names, Iterator)
    self.assertEqual(
      list(names),
      [
        "CONSTANT_2",
        "CONSTANT_3",
        "CONSTANT_1",
      ],
    )

  def test_values(self):

    class FOO(Constants):
      CONSTANT_2 = SimpleConstant()
      CONSTANT_3 = SimpleConstant()
      CONSTANT_1 = SimpleConstant()

    values = FOO.values()

    self.assertIsInstance(values, list)
    self.assertEqual(
      values,
      [
        FOO.CONSTANT_2,
        FOO.CONSTANT_3,
        FOO.CONSTANT_1,
      ],
    )

  def test_itervalues(self):

    class FOO(Constants):
      CONSTANT_2 = SimpleConstant()
      CONSTANT_3 = SimpleConstant()
      CONSTANT_1 = SimpleConstant()

    values = FOO.itervalues()

    self.assertIsInstance(values, Iterator)
    self.assertEqual(
      list(values),
      [
        FOO.CONSTANT_2,
        FOO.CONSTANT_3,
        FOO.CONSTANT_1,
      ],
    )

  def test_constants(self):
    class FOO(Constants):
      CONSTANT_2 = SimpleConstant()
      CONSTANT_3 = SimpleConstant()
      CONSTANT_1 = SimpleConstant()

    constants = FOO.constants()

    self.assertIsInstance(constants, list)
    self.assertEqual(
      constants,
      [
        FOO.CONSTANT_2,
        FOO.CONSTANT_3,
        FOO.CONSTANT_1,
      ],
    )

  def test_iterconstants(self):

    class FOO(Constants):
      CONSTANT_2 = SimpleConstant()
      CONSTANT_3 = SimpleConstant()
      CONSTANT_1 = SimpleConstant()

    constants = FOO.iterconstants()

    self.assertIsInstance(constants, Iterator)
    self.assertEqual(
      list(constants),
      [
        FOO.CONSTANT_2,
        FOO.CONSTANT_3,
        FOO.CONSTANT_1,
      ],
    )

  def test_items(self):

    class FOO(Constants):
      CONSTANT_2 = SimpleConstant()
      CONSTANT_3 = SimpleConstant()
      CONSTANT_1 = SimpleConstant()

    items = FOO.items()

    self.assertIsInstance(items, list)
    self.assertEqual(
      items,
      [
        ("CONSTANT_2", FOO.CONSTANT_2),
        ("CONSTANT_3", FOO.CONSTANT_3),
        ("CONSTANT_1", FOO.CONSTANT_1),
      ],
    )

  def test_iteritems(self):

    class FOO(Constants):
      CONSTANT_2 = SimpleConstant()
      CONSTANT_3 = SimpleConstant()
      CONSTANT_1 = SimpleConstant()

    items = FOO.iteritems()

    self.assertIsInstance(items, Iterator)
    self.assertEqual(
      list(items),
      [
        ("CONSTANT_2", FOO.CONSTANT_2),
        ("CONSTANT_3", FOO.CONSTANT_3),
        ("CONSTANT_1", FOO.CONSTANT_1),
      ],
    )

  def test_iter(self):

    class FOO(Constants):
      CONSTANT_2 = SimpleConstant()
      CONSTANT_3 = SimpleConstant()
      CONSTANT_1 = SimpleConstant()

    self.assertIsInstance(FOO, Iterable)
    self.assertEqual(
      list(FOO),
      [
        "CONSTANT_2",
        "CONSTANT_3",
        "CONSTANT_1",
      ],
    )

  def test_len(self):

    class FOO(Constants):
      CONSTANT_2 = SimpleConstant()
      CONSTANT_3 = SimpleConstant()
      CONSTANT_1 = SimpleConstant()

    self.assertEqual(len(FOO), 3)

  def test_contains(self):

    class FOO(Constants):
      CONSTANT_1 = SimpleConstant()

    self.assertTrue("CONSTANT_1" in FOO)
    self.assertFalse("CONSTANT_X" in FOO)

  def test_has_name(self):

    class FOO(Constants):
      CONSTANT_1 = SimpleConstant()

    self.assertTrue(FOO.has_name("CONSTANT_1"))
    self.assertFalse(FOO.has_name("CONSTANT_X"))

  def test_get_item(self):

    class FOO(Constants):
      CONSTANT_1 = SimpleConstant()

    self.assertEqual(FOO["CONSTANT_1"], FOO.CONSTANT_1)

  def test_get_item_missing(self):

    class FOO(Constants):
      CONSTANT_1 = SimpleConstant()

    with self.assertRaises(CandvMissingConstantError) as cm:
      FOO["CONSTANT_X"]

    self.assertEqual(
      cm.exception.args[0],
      (
        "constant \"CONSTANT_X\" is not present in "
        "\"<constants container 'FOO'>\""
      ),
    )

  def test_get(self):

    class FOO(Constants):
      CONSTANT_1 = SimpleConstant()

    self.assertEqual(FOO.get("CONSTANT_1"), FOO.CONSTANT_1)
    self.assertEqual(FOO.get("CONSTANT_X"), None)

  def test_invalid_constant_class(self):

    with self.assertRaises(CandvInvalidConstantClass) as cm:

      class FOO(Constants):
        constant_class = int

    self.assertEqual(
      cm.exception.args[0],
      (
        f"invalid \"constant_class\" for \"<constants container 'FOO'>\": "
        f"must be derived from \"<class 'candv.core.SimpleConstant'>\", "
        f"but got \"{repr(int)}\""
      ),
    )

  def test_reuse_of_constant(self):

    with self.assertRaises(CandvConstantAlreadyBoundError) as cm:

      class FOO(Constants):
        CONSTANT_1 = SimpleConstant()

      class BAR(Constants):
        CONSTANT_1 = FOO.CONSTANT_1

    self.assertEqual(
      cm.exception.args[0],
      (
        "cannot use \"<constant 'FOO.CONSTANT_1'>\" as value for \"CONSTANT_1\" "
        "attribute of \"<constants container 'BAR'>\" container: already bound "
        "to \"<constants container 'FOO'>\""
      ),
    )

  def test_duplicates(self):

    class FOO(Constants):
      CONSTANT_1 = SimpleConstant()
      CONSTANT_1 = SimpleConstant()

    self.assertEqual(
      list(FOO),
      ["CONSTANT_1", ],
    )

  def test_mixed_constant_classes(self):

    class CustomConstant(SimpleConstant):
      pass

    class FOO(Constants):
      CONSTANT_1 = SimpleConstant()
      CONSTANT_2 = CustomConstant()

    self.assertEqual(
      list(FOO),
      [
        "CONSTANT_1",
        "CONSTANT_2",
      ],
    )

  def test_constant_class(self):

    class CustomConstant(SimpleConstant):
      pass

    class FOO(Constants):
      constant_class = CustomConstant

      CONSTANT_1 = CustomConstant()
      CONSTANT_2 = CustomConstant()
      CONSTANT_X = SimpleConstant()  # more generic, hence insivible

    self.assertEqual(
      list(FOO),
      [
        "CONSTANT_1",
        "CONSTANT_2",
      ],
    )

  def test_unbound_constant(self):

    class CustomConstant(SimpleConstant):
      pass

    class FOO(Constants):
      constant_class = CustomConstant

      CONSTANT_1 = SimpleConstant()  # more generic, not owned

    self.assertEqual(
      FOO.CONSTANT_1.name,
      "CONSTANT_1",
    )
    self.assertEqual(
      FOO.CONSTANT_1.full_name,
      "__UNBOUND__.CONSTANT_1",
    )
    self.assertEqual(
      repr(FOO.CONSTANT_1),
      "<constant '__UNBOUND__.CONSTANT_1'>",
    )

  def test_to_primitive(self):

    class FOO(Constants):
      CONSTANT_2 = SimpleConstant()
      CONSTANT_3 = SimpleConstant()
      CONSTANT_1 = SimpleConstant()

    self.assertEqual(
      FOO.to_primitive(),
      {
        'name': "FOO",
        'items': [
          {'name': "CONSTANT_2", },
          {'name': "CONSTANT_3", },
          {'name': "CONSTANT_1", },
        ],
      },
    )

  def test_different_imports(self):
    sys.path.insert(0, str(Path(__file__).absolute().parent / "package"))

    from .package.subpackage.constants import CONSTANTS
    from subpackage.constants import CONSTANTS as SUBCONSTANTS

    self.assertNotEqual(CONSTANTS.__module__, SUBCONSTANTS.__module__)
    self.assertEqual(CONSTANTS.PRIMARY, SUBCONSTANTS.PRIMARY)

  def test_picking(self):
    from .package.subpackage.constants import CONSTANTS

    restored = pickle.loads(pickle.dumps(CONSTANTS))
    self.assertEqual(CONSTANTS, restored)


class ConstantClassMixinTestCase(unittest.TestCase):

  def test_constant_class_mixin_factory(self):

    class CustomConstant(SimpleConstant):
      pass

    class FOO(with_constant_class(CustomConstant), Constants):
      CONSTANT_1 = CustomConstant()
      CONSTANT_2 = CustomConstant()

    self.assertEqual(FOO.constant_class, CustomConstant)
    self.assertEqual(
      FOO.constants(),
      [
        FOO.CONSTANT_1,
        FOO.CONSTANT_2,
      ],
    )


class SimpleConstantTestCase(unittest.TestCase):

  def test_name(self):

    class FOO(Constants):
      CONSTANT = SimpleConstant()

    self.assertEqual(FOO.CONSTANT.name, "CONSTANT")

  def test_full_name(self):

    class FOO(Constants):
      CONSTANT = SimpleConstant()

    self.assertEqual(FOO.CONSTANT.full_name, "FOO.CONSTANT")

  def test_repr(self):

    class FOO(Constants):
      CONSTANT = SimpleConstant()

    self.assertEqual(repr(FOO.CONSTANT), "<constant 'FOO.CONSTANT'>")

  def test_container(self):

    class FOO(Constants):
      CONSTANT = SimpleConstant()

    self.assertEqual(FOO.CONSTANT.container, FOO)

  def test_to_primitive(self):

    class FOO(Constants):
      CONSTANT = SimpleConstant()

    self.assertEqual(
      FOO.CONSTANT.to_primitive(),
      {'name': "CONSTANT"},
    )


class GrouppingTestCase(unittest.TestCase):

  def test_group_name(self):

    class FOO(Constants):
      G = SimpleConstant().to_group(group_class=Constants)

    self.assertEqual(FOO.G.name, "G")

  def test_group_full_name(self):

    class FOO(Constants):
      G = SimpleConstant().to_group(group_class=Constants)

    self.assertEqual(FOO.G.full_name, "FOO.G")

  def test_group_repr(self):

    class FOO(Constants):
      G = SimpleConstant().to_group(group_class=Constants)

    self.assertEqual(repr(FOO.G), "<constants group 'FOO.G'>")

  def test_group_names(self):

    class FOO(Constants):
      G = SimpleConstant().to_group(
        group_class=Constants,
        G_3=SimpleConstant(),
        G_1=SimpleConstant(),
        G_2=SimpleConstant(),
      )

    names = FOO.G.names()

    self.assertIsInstance(names, list)
    self.assertEqual(
      names,
      [
        "G_3",
        "G_1",
        "G_2",
      ],
    )

  def test_group_iternames(self):

    class FOO(Constants):
      G = SimpleConstant().to_group(
        group_class=Constants,
        G_3=SimpleConstant(),
        G_1=SimpleConstant(),
        G_2=SimpleConstant(),
      )

    names = FOO.G.iternames()

    self.assertIsInstance(names, Iterator)
    self.assertEqual(
      list(names),
      [
        "G_3",
        "G_1",
        "G_2",
      ],
    )

  def test_group_values(self):

    class FOO(Constants):
      G = SimpleConstant().to_group(
        group_class=Constants,
        G_3=SimpleConstant(),
        G_1=SimpleConstant(),
        G_2=SimpleConstant(),
      )

    values = FOO.G.values()

    self.assertIsInstance(values, list)
    self.assertEqual(
      values,
      [
        FOO.G.G_3,
        FOO.G.G_1,
        FOO.G.G_2,
      ],
    )

  def test_group_itervalues(self):

    class FOO(Constants):
      G = SimpleConstant().to_group(
        group_class=Constants,
        G_3=SimpleConstant(),
        G_1=SimpleConstant(),
        G_2=SimpleConstant(),
      )

    values = FOO.G.itervalues()

    self.assertIsInstance(values, Iterator)
    self.assertEqual(
      list(values),
      [
        FOO.G.G_3,
        FOO.G.G_1,
        FOO.G.G_2,
      ],
    )

  def test_group_constants(self):

    class FOO(Constants):
      G = SimpleConstant().to_group(
        group_class=Constants,
        G_3=SimpleConstant(),
        G_1=SimpleConstant(),
        G_2=SimpleConstant(),
      )

    constants = FOO.G.constants()

    self.assertIsInstance(constants, list)
    self.assertEqual(
      constants,
      [
        FOO.G.G_3,
        FOO.G.G_1,
        FOO.G.G_2,
      ],
    )

  def test_group_iterconstants(self):

    class FOO(Constants):
      G = SimpleConstant().to_group(
        group_class=Constants,
        G_3=SimpleConstant(),
        G_1=SimpleConstant(),
        G_2=SimpleConstant(),
      )

    constants = FOO.G.iterconstants()

    self.assertIsInstance(constants, Iterator)
    self.assertEqual(
      list(constants),
      [
        FOO.G.G_3,
        FOO.G.G_1,
        FOO.G.G_2,
      ],
    )

  def test_group_items(self):

    class FOO(Constants):
      G = SimpleConstant().to_group(
        group_class=Constants,
        G_3=SimpleConstant(),
        G_1=SimpleConstant(),
        G_2=SimpleConstant(),
      )

    items = FOO.G.items()

    self.assertIsInstance(items, list)
    self.assertEqual(
      items,
      [
        ("G_3", FOO.G.G_3),
        ("G_1", FOO.G.G_1),
        ("G_2", FOO.G.G_2),
      ]
    )

  def test_group_iteritems(self):

    class FOO(Constants):
      G = SimpleConstant().to_group(
        group_class=Constants,
        G_3=SimpleConstant(),
        G_1=SimpleConstant(),
        G_2=SimpleConstant(),
      )

    items = FOO.G.iteritems()

    self.assertIsInstance(items, Iterator)
    self.assertEqual(
      list(items),
      [
        ("G_3", FOO.G.G_3),
        ("G_1", FOO.G.G_1),
        ("G_2", FOO.G.G_2),
      ]
    )

  def test_group_iter(self):

    class FOO(Constants):
      G = SimpleConstant().to_group(
        group_class=Constants,
        G_3=SimpleConstant(),
        G_1=SimpleConstant(),
        G_2=SimpleConstant(),
      )

    self.assertIsInstance(FOO.G, Iterable)
    self.assertEqual(
      list(FOO.G),
      [
        "G_3",
        "G_1",
        "G_2",
      ]
    )

  def test_group_len(self):

    class FOO(Constants):
      G = SimpleConstant().to_group(
        group_class=Constants,
        G_3=SimpleConstant(),
        G_1=SimpleConstant(),
        G_2=SimpleConstant(),
      )

    self.assertEqual(len(FOO.G), 3)

  def test_group_contains(self):

    class FOO(Constants):
      G = SimpleConstant().to_group(
        group_class=Constants,
        G_1=SimpleConstant(),
      )

    self.assertTrue("G_1" in FOO.G)
    self.assertFalse("G_X" in FOO.G)

  def test_group_has_name(self):

    class FOO(Constants):
      G = SimpleConstant().to_group(
        group_class=Constants,
        G_1=SimpleConstant(),
      )

    self.assertTrue(FOO.G.has_name("G_1"))
    self.assertFalse(FOO.G.has_name("G_X"))

  def test_group_get_item(self):

    class FOO(Constants):
      G = SimpleConstant().to_group(
        group_class=Constants,
        G_1=SimpleConstant(),
      )

    self.assertEqual(FOO.G["G_1"], FOO.G.G_1)

  def test_group_get_item_missing(self):

    class FOO(Constants):
      G = SimpleConstant().to_group(
        group_class=Constants,
        G_1=SimpleConstant(),
      )

    with self.assertRaises(CandvMissingConstantError) as cm:
      FOO.G["G_X"]

    self.assertEqual(
      cm.exception.args[0],
      "constant \"G_X\" is not present in \"<constants group 'FOO.G'>\"",
    )

  def test_group_get(self):

    class FOO(Constants):
      G = SimpleConstant().to_group(
        group_class=Constants,
        G_1=SimpleConstant(),
      )

    self.assertEqual(FOO.G.get("G_1"), FOO.G.G_1)
    self.assertEqual(FOO.G.get("G_X"), None)

  def test_group_container(self):

    class FOO(Constants):
      G = SimpleConstant().to_group(
        group_class=Constants,
        G_1=SimpleConstant(),
      )

    self.assertEqual(FOO.G.container, FOO)

  def test_group_as_container(self):

    class FOO(Constants):
      G = SimpleConstant().to_group(
        group_class=Constants,
        G_1=SimpleConstant(),
      )

    self.assertEqual(FOO.G.G_1.container, FOO.G)

  def test_container_names(self):

    class FOO(Constants):
      A = SimpleConstant()
      G = SimpleConstant().to_group(
        group_class=Constants,
        G_1=SimpleConstant(),
      )

    self.assertEqual(FOO.names(), ["A", "G", ])

  def test_get_from_container(self):

    class FOO(Constants):
      G = SimpleConstant().to_group(
        group_class=Constants,
        G_1=SimpleConstant(),
      )

    self.assertEqual(FOO["G"], FOO.G)

  def test_group_member_full_name(self):

    class FOO(Constants):
      G = SimpleConstant().to_group(
        group_class=Constants,
        G_1=SimpleConstant(),
      )

    self.assertEqual(FOO.G.G_1.full_name, "FOO.G.G_1")

  def test_invalid_group(self):
    with self.assertRaises(CandvInvalidGroupMemberError) as cm:

      class FOO(Constants):
        G = SimpleConstant().to_group(
          group_class=Constants,
          G_1=SimpleConstant(),
          G_2=1,
        )

    self.assertEqual(
      cm.exception.args[0],
      (
        "invalid group member \"1\": only instances of "
        "\"<class 'candv.core.SimpleConstant'>\" or other groups are allowed"
      ),
    )

  def test_to_primitive(self):

    class FOO(Constants):
      A = SimpleConstant()
      G = SimpleConstant().to_group(
        group_class=Constants,
        G_3=SimpleConstant(),
        G_1=SimpleConstant(),
        G_2=SimpleConstant(),
      )

    self.assertEqual(
      FOO.to_primitive(),
      {
        'name': "FOO",
        'items': [
          {'name': "A", },
          {
            'name': "G",
            'items': [
              {'name': "G_3", },
              {'name': "G_1", },
              {'name': "G_2", },
            ],
          },
        ],
      },
    )
