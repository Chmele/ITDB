import requests
import json

requests.post('http://127.0.0.1:5000/test/test', data = {'table': json.dumps((1, 'new row'))})