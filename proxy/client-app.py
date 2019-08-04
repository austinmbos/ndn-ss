"""
This is the client application
it is meant to be run on the host machine, and its request
goes through the ndn-ss microservice chains, where it will
be processed.


make sure a face is created to the docker container with NFD
nfdc face create udp://{ip:port}
nfdc route add /ndn-ss udp://{same ip: same port}
"""


from pyndn import Name, Interest, Face
from pyndn.security import KeyChain
from pyndn.util import Blob

import time
import base64
import json
import copy

import sys

from CryptoUtil import *

class Counter(object):
    def __init__(self):
        self.rec = 1
        print("init")

    def onData(self,interest,data):
        #self.rec = 0
        print("Got a packet")
        print(data.getContent())

    def onTimeout(self,interest):
        print("Timeout..")


def main():
    if len(sys.argv) < 2:
        print("usage: python3 client-app.py {good/bad}")
        quit()

    #Interest.setDefaultCanBePrefix(True)

    with open("shared/system-info.json") as f:
        user_data = json.load(f)

    face = Face()
    counter = Counter()

    name = Name("/ndn-ss/austin")
    req_name = "/example/test"
    sym_key = base64.b64decode(user_data['austin']['sym_key'])
    iv,ct,tag = sym_encrypt(sym_key,req_name)

    enc_req_name = base64.b64encode(iv).decode('ascii') 
    name.append(enc_req_name)
    enc_req_name = base64.b64encode(ct).decode('ascii') 
    name.append(enc_req_name)
    enc_req_name = base64.b64encode(tag).decode('ascii')
    name.append(enc_req_name)

    
    priv_key = user_data['austin']['priv_key']
    priv_key = base64.b64decode(priv_key)
    priv_key = load_priv_key(priv_key)

    sig =\
    base64.b64encode(priv_key.sign(bytes("austin",'utf-8'))).decode('ascii')
    
    bad_sig =\
    base64.b64encode(priv_key.sign(bytes("abstin",'utf-8'))).decode('ascii')

    i = Interest()
    i.setMustBeFresh(True)
    i.setInterestLifetimeMilliseconds(0)

    #face.expressInterest(name,counter.onData,counter.onTimeout)

    if sys.argv[1] == "good":
        name.append(sig)
        face.expressInterest(name,i,counter.onData,counter.onTimeout)
    elif sys.argv[1] == "bad":
        name.append(bad_sig)
        face.expressInterest(name,i,counter.onData,counter.onTimeout)
    else:
        print("c")
        

    while counter.rec == 1:

        face.processEvents()
        time.sleep(0.1)
        face.expressInterest(name,i,counter.onData,counter.onTimeout)



main()
        

