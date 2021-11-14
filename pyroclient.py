import Pyro5.api

uri = 'PYRO:obj_16a6c481be094671b504137c9d025e43@localhost:60420'
dbms = Pyro5.api.Proxy(uri)
db = Pyro5.api.Proxy(dbms.create_database('testDB'))