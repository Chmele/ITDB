from os import path
from typing import Any


class Field:
    def __init__(self, name: str):
        self.name = name

    def compatible(self, other):
        return self.__class__ == other.__class__


class IntegerField(Field):
    def validate_value(self, value: Any):
        return isinstance(value, int)


class FloatField(Field):
    def validate_value(self, value: Any):
        return isinstance(value, float)


class StringField(Field):
    def validate_value(self, value: Any):
        return isinstance(value, str)


class CharField(StringField):
    def validate_value(self, value: Any):
        return isinstance(value, str) and len(value) == 1


class PngField(StringField):
    def validate_value(self, value: Any):
        return isinstance(value, str) and path.isfile(value)


class FloatIntervalField(Field):
    def validate_value(self, value: Any):
        return isinstance(value, tuple) and len(tuple) == 2 and\
            isinstance(value[0], float) and isinstance(value[1], float)