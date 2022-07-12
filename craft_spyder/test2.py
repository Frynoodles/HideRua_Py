import json
with open('test2.text', 'r', encoding='utf-8') as f:
    data = json.loads(f.read())

print(data)
print('==')
print(type(data))
print('==')

