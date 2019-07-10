
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
##############################################################
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

##############################################################
##############################################################
def run_enc(filename,logfile):
    key = create_sym_key()

    with open(filename,"r") as f:
        data = json.load(f)


    with open(logfile,"w") as f:
        sym_encrypt(key,"a") # why is the first one so slow
        for x in data:
            start = time.time_ns()
            sym_encrypt(key,x)
            end = time.time_ns()
            f.write(str( (end-start) ) + "\n")


    """
    with open(logfile,"w") as f:
        f.write("Length: " + str(len(data)) + "\n")
        f.write("time (seconds): " +  str(round( (end-start) / 1e9,5)) + "\n")
    """
    

##############################################################
##############################################################
if __name__ == "__main__":
    """
    Run all the test
    1. For convience, run all tests on bare metal, then
        docker build the image, this copies bare metal results into
        results/ then run the docker image, and all results should be
        in one spot for later
    """

    # Check if running in docker
    # make sure to pass --docker flag to the Docker file CMD argument
    ext = ""
    if len(sys.argv) > 1:
        if sys.argv[1] == "--docker":
            ext += ".docker.log"
    else:
        ext += ".log"


    # can run multiple tests here
    # first number is content size
    # second number is how long the list is
    #run_sign("data/10000-1000-list_of_data.json","results/sign-10000-1000"+ext)
    #run_sign("data/10000-100-list_of_data.json","results/sign-10000-100"+ext);
    #run_sign("data/10000-10-list_of_data.json","results/sign-10000-10"+ext);

    #run_ver("data/10000-1000-signed_data.json","results/sig-ver-10000-1000"+ext)

    run_enc("data/10-10-list_of_data.json","results/sym-enc-10-10"+ext)
    #run_enc("data/10000-100-list_of_data.json","results/sym-enc-10000-100"+ext)
    #run_enc("data/10000-10-list_of_data.json","results/sym-enc-10000-10"+ext)











