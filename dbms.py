from database import Database


class DBMS:
    def __init__(self):
        self.databases = {}

    def create_database(self, name: str) -> Database:
        d = Database
        self.databases.update({name: d})
        return d

    def get_database(self, name: str) -> Database:
        return self.databases[name]