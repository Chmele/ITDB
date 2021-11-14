import os
os.environ['PYRO_SERIALIZER'] = 'pickle'

from dbms import DBMS
import Pyro5.api
from database import Database


# @Pyro5.api.expose
# class GreetingMaker(object):
#     def get_fortune(self, name):
#         return "Hello, {0}. Here is your fortune message:\n" \
#                "Behold the warranty -- the bold print giveth and the fine print taketh away.".format(name)


# daemon = Pyro5.api.Daemon()             # make a Pyro daemon
# uri = daemon.register(GreetingMaker)    # register the greeting maker as a Pyro object

# print("Ready. Object uri =", uri)       # print the uri so we can use it in the client later
# daemon.requestLoop()                    # start the event loop of the server to wait for calls

@Pyro5.api.expose
class RemoteDBMS(DBMS):
    def __init__(self):
        self.databases = {}

    def create_database(self, name: str) -> Database:
        print('invoked')
        d = Database()
        self.databases.update({name: d})
        return daemon.register(d)

    @Pyro5.api.expose
    def get_database(self, name: str) -> Database:
        print('invoked')
        return daemon.register(self.databases[name])



daemon = Pyro5.api.Daemon()             # make a Pyro daemon
d = RemoteDBMS()
d.create_database('test')
uri = daemon.register(d)       # register the greeting maker as a Pyro object

print("Ready. Object uri =", uri)       # print the uri so we can use it in the client later
daemon.requestLoop()    