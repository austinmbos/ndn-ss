"""
Simple sign test
Reads in a json file, then signs the data in
each field of the json
"""
import random
import string
import json
import base64
import sys
import time


from CryptoUtil import *



##############################################################
##############################################################
def run_sign(filename,logfile):
    """ signed with ed25519
    """
    
    data = {}

    with open(filename,"r") as f:
        data = json.load(f)

    priv_key = gen_priv_key()

    start = time.time_ns()
    for x in data:
        priv_key.sign(bytes(x,'utf-8'))

    end = time.time_ns()
    with open(logfile,"w") as f:
        f.write("Length: " + str(len(data)) + "\n")
        f.write("time (seconds): " + str( round( (end-start) / 1e9 , 5)) + "\n")



        
##############################################################

if __name__ == "__main__":
    """ when this is run in docker, a volume should be attached,
        So when finished running, the volume shoud be available under
        /var/lib/docker/volumes/{name}/_data

        When run on host, data is available right in this dir
    """
    ext = ""

    if len(sys.argv) > 1:

        if sys.argv[1] == "--docker":
            ext += ".docker.log"

    else:
        ext += ".log"

    # can run multiple tests here
    # first number is content size
    # second number is how long the list is
    run_sign("data/10000-1000-list_of_data.json","results/sign-10000-1000"+ext)
    run_sign("data/10000-100-list_of_data.json","results/sign-10000-100"+ext);
    run_sign("data/10000-10-list_of_data.json","results/sign-10000-10"+ext);




