import requests
import base64
import json

from CryptoUtil import *


priv_key = gen_priv_key()
priv_key_bytes = get_priv_bytes(priv_key)
encoded_priv_key = base64.b64encode(priv_key_bytes).decode('ascii')

d = "hello there"

data = {'data':d,'key':encoded_priv_key}

r = requests.post(url="http://localhost:8080/sign",data=data)

data = r.text

sig = base64.b64decode(r.text)

