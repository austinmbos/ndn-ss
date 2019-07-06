"""
symmetric key encryption test
read in list of data in json format,
then encrypt each data field
"""

import sys
import time
import json

from CryptoUtil import *

def run_enc(filename,logfile):
    key = create_sym_key()

    with open(filename,"r") as f:
        data = json.load(f)

    start = time.time_ns()
    for x in data:
        sym_encrypt(key,x)

    end = time.time_ns()

    with open(logfile,"w") as f:
        f.write("Length: " + str(len(data)) + "\n")
        f.write("time (seconds): " +  str(round( (end-start) / 1e9,5)) + "\n")
    


if __name__ == "__main__":

    ext = ""

    if len(sys.argv) > 1:
        if sys.argv[1] == "--docker":
            ext += ".docker.log"

    else:
        ext += ".log"


    run_enc("data/10000-1000-list_of_data.json","results/sym-enc-10000-1000"+ext)
    run_enc("data/10000-100-list_of_data.json","results/sym-enc-10000-100"+ext)
    run_enc("data/10000-10-list_of_data.json","results/sym-enc-10000-10"+ext)
