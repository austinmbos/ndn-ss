import json

with open("100-10-signed_data.json","r") as f:
    x = json.load(f)


y = x['data_list']

for i in y:
    print(i['data'])
