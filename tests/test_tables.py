import unittest
from table import Table
from fields import *


class TestTables(unittest.TestCase):
    def setUp(self) -> None:
        self.t = Table([
            IntegerField('id'),
            IntegerField('something'),
        ])

    def test_field_validation(self):
        t = self.t
        self.assertTrue(t.validate_row([1, 1]))
        self.assertTrue(t.validate_row([1, 1211221]))
        self.assertFalse(t.validate_row(['1', 1]))

    def test_row_appending(self):
        t = self.t
        t.add_row([1,1])
        self.assertEqual(t.rows, [[1, 1]])
        t.add_row(['1', 1])
        self.assertEqual(t.rows, [[1, 1]])
