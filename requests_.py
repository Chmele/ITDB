import requests
import json

requests.post('http://127.0.0.1:5000/test/test', data = {'table': json.dumps((1, 'new row'))})
requests.post('http://127.0.0.1:5000/test/test/1', data = {"id":223,"name":"223"})