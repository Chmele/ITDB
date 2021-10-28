from fields import *
from collections.abc import Sequence


class Table:
    def __init__(self, fields: "list[Field]", rows = []):
        self.fields = fields
        self.rows = rows

    def compatible(self, other: "Table") -> bool:
        if len(self.fields) != len(other.fields):
            return False
        return all(
            Field.compatible(field1, field2) 
            for field1, field2 
            in zip(self.fields, other.fields)
            )

    def __add__(self, other: "Table") -> "Table":
        assert Table.compatible(self, other)
        return Table(self.fields, rows = self.rows + other.rows)
    
    def __eq__(self, other: "Table") -> bool:
        return Table.compatible(self, other) and self.rows==other.rows

    def validate_row(self, row: Sequence):
        if len(row) != len(self.fields):
            return False
        return all(field.validate_value(value) for value, field in zip(row, self.fields))

    def add_row(self, row: Sequence):
        if self.validate_row(row):
            self.rows.append(list(row))

    def get_row(self, index: int):
        return self.rows[index]