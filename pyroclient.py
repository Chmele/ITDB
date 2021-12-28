import Pyro5.api
import os
os.environ['PYRO_SERIALIZER'] = 'pickle'

uri = 'PYRO:obj_42caa510e90747e58214a1dc13195c0f@localhost:50292'
dbms = Pyro5.api.Proxy(uri)
# db = Pyro5.api.Proxy(dbms.get_database('test'))