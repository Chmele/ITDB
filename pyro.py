import os

from fields import IntegerField
from table import Table
os.environ['PYRO_SERIALIZER'] = 'pickle'

from dbms import DBMS
import Pyro5.api
from database import Database

@Pyro5.api.expose
class RemoteDBMS(DBMS):
    def __init__(self):
        self.databases = {}

    def create_database(self, name: str) -> Database:
        print('invoked')
        d = Database()
        self.databases.update({name: d})
        # return daemon.register(d)

    @Pyro5.api.expose
    def get_database(self, name: str) -> Database:
        print('invoked')
        return daemon.register(self.databases[name])



daemon = Pyro5.api.Daemon()
d = RemoteDBMS()
d.create_database('test')
d.databases['test'].append_table(Table((IntegerField('id'),)), 'test')
d.databases['test'].tables['test'].add_row([112])
uri = daemon.register(d)
print("Ready. Object uri =", uri)       # print the uri so we can use it in the client later
daemon.requestLoop()