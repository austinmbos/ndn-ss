import requests
import base64
import json

from CryptoUtil import *

priv_key = gen_priv_key()
pub_key = priv_key.public_key()
pub_key = get_pub_bytes(pub_key)
pub_key = base64.b64encode(pub_key).decode('ascii')


d = "hello there"
sig = priv_key.sign(bytes(d,'utf-8'))
sig = base64.b64encode(sig).decode('ascii')


data = {'sig':sig,'data':d,'pub_key':pub_key}

r = requests.post(url="http://localhost:5111/verify",data=data)


print(r.text)



