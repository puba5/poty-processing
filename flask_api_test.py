import json

with open('./pyflask/example_return.json') as json_file:
    json_data = json.load(json_file)

print(json_data["timestampes"][0])