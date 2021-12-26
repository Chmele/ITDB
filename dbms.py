from database import Database


class DBMS:
    def __init__(self):
        self.databases = {}

    def create_database(self, name: str) -> Database:
        self.databases.update({name: Database()})
        return self.databases[name]

    def get_database(self, name: str) -> Database:
        return self.databases[name]

    def delete_database(self, name: str) -> None:
        self.databases.pop(name)

    def get_or_create_database(self, name: str) -> Database:
        try:
            return self.get_database(name)
        except KeyError:
            return self.create_database(name)
