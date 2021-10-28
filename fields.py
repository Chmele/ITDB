from typing import Any

class Field:
    def __init__(self, name: str):
        self.name = name

    def compatible(self, other):
        return self.__class__ == other.__class__

class IntegerField(Field):
    def validate_value(self, value: Any):
        return isinstance(value, int)