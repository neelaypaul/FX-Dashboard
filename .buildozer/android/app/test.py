import requests
import json
from datetime import datetime

with open('../Assets/latest.json', encoding='utf-8') as f:
    data = json.load(f)


print(data)

time = datetime.utcfromtimestamp(data['timestamp'])

print(time)

print(data['rates']['EUR']/data['rates']['EUR'])