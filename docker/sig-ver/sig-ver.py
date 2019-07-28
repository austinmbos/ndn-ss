
import base64
import json


from CryptoUtil import *



def sigver():

    d = []
    with open("data.first.txt","r") as f:
        for line in f.readlines():
            d.append(line)

    with open("system-info.json") as f:
        user_data = json.load(f)


    user_name = d[1].rstrip()
    sig = d[-1]
    sig = sig[0:-4]
    sig = base64.b64decode(sig)
    sig = sig[0:-2]
    

    user_pub_key = user_data[user_name]['pub_key']
    user_pub_key = base64.b64decode(user_pub_key)
    user_pub_key = load_pub_key(user_pub_key)

    user_pub_key.verify(sig,bytes(user_name,'utf-8'))




sigver()
