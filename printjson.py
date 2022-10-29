import json

f = open('ruburdic.json', 'r', encoding='utf-8')
data = json.load(f)
print(data)