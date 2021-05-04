import requests
import json

URL='http://192.168.0.2/index.jsn'

r=requests.get(URL,timeout=2)
print(json.dumps(r.json()))