
import random
import string
import json
import base64
import sys
import time

from CryptoUtil import *

##############################################################
# 1
##############################################################
def run_sign(filename,logfile):
    """ signed with ed25519
    """
    
    data = {}

    with open(filename,"r") as f:
        data = json.load(f)

    priv_key = gen_priv_key()

    with open(logfile,"w") as f:

        for x in data:
            start = time.time_ns()
            priv_key.sign(bytes(x,'utf-8'))

            end = time.time_ns()
            f.write(str( (end-start) ) + "\n")

        
##############################################################
# 2
##############################################################
def run_ver(filename,logfile):

    with open(filename,"r") as f:
        file = json.load(f)

    pub_key = base64.b64decode(file['pub_key'])
    pub_key = load_pub_key(pub_key)

    with open(logfile,"w") as f:
        for x in file['data_list']:
            start = time.time_ns()
            data = bytes(x['data'],"utf-8")
            sig = base64.b64decode(x['sig'])

            try:
                status = pub_key.verify(sig,data)
            except:
                print("INVALID SIGNATURE: check for errors, there should not\n")
                print("be invalid signatures for this test")

            end = time.time_ns()
            f.write(str( (end-start) ) + "\n")



##############################################################
# 3
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


##############################################################
# 4
##############################################################
def run_rsa_enc(filename,logfile):
    priv_key = gen_rsa_priv_key()
    pub_key = priv_key.public_key()

    with open(filename,"r") as f:
        data = json.load(f)

    with open(logfile,"w") as f:
        rsa_enc(pub_key,"a")
        for x in data:
            start = time.time_ns()
            rsa_enc(pub_key,x)
            end = time.time_ns()
            f.write(str( (end-start) ) + "\n")



##############################################################
# 5
##############################################################
def run_rsa_dec(filename,logfile):
    priv_key = gen_rsa_priv_key()
    pub_key = priv_key.public_key()

    enc_data = []

    with open(filename,"r") as f:
        data = json.load(f)

    for x in data:
        enc_data.append(rsa_enc(pub_key,x))

    with open(logfile,"w") as f:
        rsa_dec(priv_key,enc_data[0])
        for x in enc_data:
            start = time.time_ns()
            rsa_dec(priv_key,x)
            end = time.time_ns()
            f.write(str( (end-start) ) + "\n")

    

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

    run_rsa_enc("data/10-1000-list_of_data.json","results/rsa-enc-10000-1000"+ext)
    run_rsa_enc("data/10-100-list_of_data.json","results/rsa-enc-10000-100"+ext)
    run_rsa_enc("data/10-10-list_of_data.json","results/rsa-enc-10000-10"+ext)

    run_rsa_dec("data/10-1000-list_of_data.json","results/rsa-dec-10000-1000"+ext)
    run_rsa_dec("data/10-100-list_of_data.json","results/rsa-dec-10000-100"+ext)
    run_rsa_dec("data/10-10-list_of_data.json","results/rsa-dec-10000-10"+ext)

    run_sign("data/10000-1000-list_of_data.json","results/sign-10000-1000"+ext)
    run_sign("data/10000-100-list_of_data.json","results/sign-10000-100"+ext);
    run_sign("data/10000-10-list_of_data.json","results/sign-10000-10"+ext);

    run_ver("data/10000-1000-signed_data.json","results/sig-ver-10000-1000"+ext)
    run_ver("data/10000-100-signed_data.json","results/sig-ver-10000-100"+ext)
    run_ver("data/10000-10-signed_data.json","results/sig-ver-10000-10"+ext)

    run_enc("data/10000-1000-list_of_data.json","results/sym-enc-10000-1000"+ext)
    run_enc("data/10000-100-list_of_data.json","results/sym-enc-10000-100"+ext)
    run_enc("data/10000-10-list_of_data.json","results/sym-enc-10000-10"+ext)











