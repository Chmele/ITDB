from fields import *
from collections.abc import Sequence


class Table:
    def __init__(self, fields: "list[Field]"):
        self.fields = fields
        self.rows = []

    def validate_row(self, row: Sequence):
        if len(row) != len(self.fields):
            return False
        return all(field.validate_value(value) for value, field in zip(row, self.fields))

    def add_row(self, row: Sequence):
        if self.validate_row(row):
            self.rows.append(list(row))

    def get_row(self, index: int):
        return self.rows[index]