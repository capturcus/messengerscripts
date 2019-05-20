#!/usr/bin/python3
import json

with open("../antonimarmolada_wybgplc-xa/message.json") as f:
    content = json.loads(f.read())

for m in content['messages']:
    print(m['content'].encode('latin-1').decode('utf-8'))