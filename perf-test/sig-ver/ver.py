"""
Read in a json that contains signed data
and the corresponding keys
just verify the signature
"""

import random
import string
import json
import base64
import sys
import time

from CryptoUtil import *



def run_ver(filename,logfile):

    with open(filename,"r") as f:
        file = json.load(f)

    pub_key = base64.b64decode(file['pub_key'])
    pub_key = load_pub_key(pub_key)

    start = time.time_ns()
    for x in file['data_list']:
        data = bytes(x['data'],"utf-8")
        sig = base64.b64decode(x['sig'])

        try:
            status = pub_key.verify(sig,data)
        except:
            print("INVALID SIGNATURE: check for errors, there should not\n")
            print("be invalid signatures for this test")

    end = time.time_ns()

    with open(logfile,"w") as f:
        f.write("Length: " + str(len(data)) + "\n")
        f.write("time (seconds): " + str( round( (end-start) / 1e9 , 5)) + "\n")




    return 1




if __name__ == "__main__":


    ext = ""

    if len(sys.argv) > 1:

        if sys.argv[1] == "--docker":
            ext += ".docker.log"

    else:
        ext += ".log"


    run_ver("data/10000-1000-signed_data.json","results/sig-ver-10000-1000"+ext)





