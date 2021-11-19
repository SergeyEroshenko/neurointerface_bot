import requests
import json


uri = 'http://127.0.0.1:2336'

data = requests.get(uri + '/Spectrum').content
data = json.loads(data)

print(data.keys())
print(len(data['spectrum'][0]))
