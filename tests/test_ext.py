import operator
import unittest

from collections.abc import Iterator

from datetime import date

from dataclasses import dataclass

from candv.core import Constants
from candv.core import SimpleConstant

from candv.exceptions import CandvValueNotFoundError

from candv.ext import VerboseConstant
from candv.ext import Values
from candv.ext import ValueConstant
from candv.ext import VerboseValueConstant


class VerboseConstantTestCase(unittest.TestCase):

  def test_no_args(self):

    class FOO(Constants):
      CONSTANT = VerboseConstant()

    self.assertEqual(FOO.CONSTANT.name, "CONSTANT")
    self.assertEqual(FOO.CONSTANT.full_name, "FOO.CONSTANT")
    self.assertIsNone(FOO.CONSTANT.verbose_name)
    self.assertIsNone(FOO.CONSTANT.help_text)

  def test_versose_name(self):
    constant = VerboseConstant(verbose_name="foo")
    self.assertEqual(constant.verbose_name, "foo")

  def test_help_text(self):
    constant = VerboseConstant(help_text="just test constant")
    self.assertEqual(constant.help_text, "just test constant")

  def test_all_args(self):

    class FOO(Constants):
      CONSTANT = VerboseConstant("foo", "just test constant")

    self.assertEqual(FOO.CONSTANT.name, "CONSTANT")
    self.assertEqual(FOO.CONSTANT.full_name, "FOO.CONSTANT")
    self.assertEqual(FOO.CONSTANT.verbose_name, "foo")
    self.assertEqual(FOO.CONSTANT.help_text, "just test constant")

  def test_to_primitive_no_args(self):

    class FOO(Constants):
      CONSTANT = VerboseConstant()

    self.assertEqual(
      FOO.CONSTANT.to_primitive(),
      {
        'name': "CONSTANT",
        'verbose_name': None,
        'help_text': None,
      }
    )

  def test_to_primitive_all_args(self):

    class FOO(Constants):
      CONSTANT = VerboseConstant("Constant", "A test constant")

    self.assertEqual(
      FOO.CONSTANT.to_primitive(),
      {
        'name': "CONSTANT",
        'verbose_name': "Constant",
        'help_text': "A test constant",
      }
    )

  def test_group(self):

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
    self.assertEqual(FOO.B.names(), ["C", "D", ])
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
        ],
      },
    )


class ValuesTestCase(unittest.TestCase):

  def test_get_by_value(self):

    class FOO(Values):
      ONE = ValueConstant(1)
      TWO = ValueConstant(2)

    self.assertEqual(FOO.get_by_value(2), FOO.TWO)

  def test_get_by_value_missing(self):

    class FOO(Values):
      ONE = ValueConstant(1)

    with self.assertRaises(CandvValueNotFoundError) as cm:
      FOO.get_by_value(2)

    self.assertEqual(
      cm.exception.args[0],
      "constant with value \"2\" is not present in "
      "\"<constants container 'FOO'>\""
    )

  def test_get_by_value_with_duplicates(self):

    class FOO(Values):
      ONE = ValueConstant(1)
      TWO = ValueConstant(2)
      TWO_DUB = ValueConstant(1)

    self.assertEqual(FOO.get_by_value(2), FOO.TWO)

  def test_filter_by_value(self):

    class FOO(Values):
      ONE = ValueConstant(1)
      TWO = ValueConstant(2)
      ONE_DUB2 = ValueConstant(1)
      THREE = ValueConstant(3)
      ONE_DUB1 = ValueConstant(1)

    constants = FOO.filter_by_value(1)
    self.assertIsInstance(constants, list)
    self.assertEqual(
      list(map(operator.attrgetter("name"), constants)),
      [
        "ONE",
        "ONE_DUB2",
        "ONE_DUB1",
      ],
    )

  def test_values(self):

    class FOO(Values):
      ONE = ValueConstant(1)
      THREE = ValueConstant(3)
      TWO = ValueConstant(2)

    values = FOO.values()

    self.assertIsInstance(values, list)
    self.assertEqual(values, [1, 3, 2, ])

  def test_itervalues(self):

    class FOO(Values):
      ONE = ValueConstant(1)
      THREE = ValueConstant(3)
      TWO = ValueConstant(2)

    values = FOO.itervalues()

    self.assertIsInstance(values, Iterator)
    self.assertEqual(list(values), [1, 3, 2, ])

  def test_to_primitive_scalar(self):

    class FOO(Values):
      ONE = ValueConstant(1)

    self.assertEqual(
      FOO.ONE.to_primitive(),
      {
        'name': "ONE",
        'value': 1,
      },
    )

  def test_to_primitive_callable(self):

    class FOO(Values):
      ONE = ValueConstant(lambda: 1)

    self.assertEqual(
      FOO.ONE.to_primitive(),
      {
        'name': "ONE",
        'value': 1,
      },
    )

  def test_to_primitive_custom(self):

    @dataclass
    class Point2D:
      x: int
      y: int

      def to_primitive(self, context=None):
        return f"{self.x}:{self.y}"

    class FOO(Values):
      POS = ValueConstant(Point2D(10, 20))

    self.assertEqual(
      FOO.POS.to_primitive(),
      {
        'name': "POS",
        'value': "10:20",
      },
    )

  def test_to_primitive_date(self):

    class FOO(Values):
      DATE = ValueConstant(date(1999, 12, 31))

    self.assertEqual(
      FOO.DATE.to_primitive(),
      {
        'name': "DATE",
        'value': "1999-12-31",
      },
    )

  def test_group(self):

    class FOO(Constants):
      A = SimpleConstant()
      B = ValueConstant(10).to_group(
        group_class=Constants,
        C=SimpleConstant(),
        D=SimpleConstant(),
      )

    self.assertEqual(FOO.B.value, 10)
    self.assertEqual(FOO.B.names(), ["C", "D", ])
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
        ],
      },
    )


class VerboseValueConstantTestCase(unittest.TestCase):

  def test_group(self):

    class FOO(Constants):
      A = SimpleConstant()
      B = VerboseValueConstant(
        value=10,
        verbose_name="Constant B",
        help_text="A group with verbose name and value"
      ).to_group(
        group_class=Constants,
        C=SimpleConstant(),
        D=SimpleConstant(),
      )

    self.assertEqual(FOO.B.value, 10)
    self.assertEqual(FOO.B.verbose_name, "Constant B")
    self.assertEqual(FOO.B.help_text, "A group with verbose name and value")
    self.assertEqual(FOO.B.names(), ["C", "D", ])
    self.assertEqual(
      FOO.to_primitive(),
      {
        'name': "FOO",
        'items': [
          {'name': "A", },
          {
            'name': "B",
            'verbose_name': "Constant B",
            'help_text': "A group with verbose name and value",
            'value': 10,
            'items': [
                {'name': "C", },
                {'name': "D", },
            ],
          },
        ],
      },
    )
