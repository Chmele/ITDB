from typing import Union
import os
from table import Table
import jsonpickle

PathLike = Union[str, bytes, os.PathLike]

class Database:
    def __init__(self):
        self.tables = []

    def append_table(self, table: Table):
        self.tables.append(table)

    def remove_table(self, table: Table):
        self.tables.remove(table)
    
    def save(self, path: PathLike):
        with open(path, 'w') as file:
            file.write(jsonpickle.encode(self))

    @staticmethod
    def from_file(path: PathLike):
        with open(path, 'r') as file:
            return jsonpickle.decode(file.read())