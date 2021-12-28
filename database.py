from typing import Union
import os
from table import Table
import jsonpickle
import Pyro5.api

PathLike = Union[str, bytes, os.PathLike]

@Pyro5.api.expose
class Database:
    def __init__(self):
        self.tables = {}
    
    def get_table(self, name):
        return self.tables[name]

    def get_tables(self):
        return str(self.tables)

    def as_dict(self):
        return {name: str(table) for name, table in self.tables.items()}

    def append_table(self, table: Table, name: str) -> None:
        self.tables.update({name: table})

    def remove_table(self, name: str) -> None:
        self.tables.pop(name)
    
    def save(self, path: PathLike):
        with open(path, 'w') as file:
            file.write(jsonpickle.encode(self))

    @staticmethod
    def from_file(path: PathLike):
        with open(path, 'r') as file:
            return jsonpickle.decode(file.read())