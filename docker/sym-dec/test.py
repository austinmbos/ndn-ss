import requests
import base64
import json

from CryptoUtil import *


o_key = create_sym_key()
key = base64.b64encode(o_key).decode('ascii')


data = {'data':"hello there",'key':key}

r = requests.post(url="http://localhost:5000/encrypt",data=data)

data = json.loads(r.text)

print("ciphertext: " + data['ct'])

iv = base64.b64decode(data['iv'])
iv = base64.b64decode(data['iv'])
ct = base64.b64decode(data['ct'])
tag = base64.b64decode(data['tag'])

plaintext = sym_decrypt(o_key,iv,ct,tag)
print("plaintext: " + plaintext.decode('ascii'))

