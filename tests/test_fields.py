import unittest
from fields import *


class TestFields(unittest.TestCase):
    def test_integer_validator(self):
        integer = IntegerField('id')
        self.assertTrue(integer.validate_value(1))
        self.assertTrue(integer.validate_value(1221))
        self.assertFalse(integer.validate_value('1'))


