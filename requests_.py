import requests
import json

requests.post('http://127.0.0.1:5000/test/test', data = {'data': json.dumps((1, 'new row'))})