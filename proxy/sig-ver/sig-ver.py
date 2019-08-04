
import base64
import json
import time
import urllib.parse


from CryptoUtil import *

prefix=""
#prefix="../nfd-entry/"

def sigver():


    # poll, waiting for the semaphore to release
    with open(prefix+"shared/sig-ver.sem","r") as f:
        while 1:
            f.seek(0)
            tmp = f.read()
            try:
                if int(tmp) == 0:
                    break;
            except:
                print("...")

            time.sleep(0.1)

    with open(prefix+"shared/sig-ver.sem","w") as f:
        f.write("1")

    # read in the info written by the nfd-entry
    d = []
    with open(prefix+"shared/data.first.txt","r") as f:
        for line in f.readlines():
            d.append(line)

    # read in the user info, including their keys
    with open(prefix+"shared/system-info.json") as f:
        user_data = json.load(f)


    # \r is added somewhere along the line, that
    # and newlines need to be stripped
    user_name = d[1].rstrip()
    sig = d[-1]
    sig = urllib.parse.unquote(sig)
    sig = base64.b64decode(sig)

    # decode and load the public key to verify user signature
    user_pub_key = user_data[user_name]['pub_key']
    user_pub_key = base64.b64decode(user_pub_key)
    user_pub_key = load_pub_key(user_pub_key)

    try:
        user_pub_key.verify(sig,bytes(user_name,'utf-8'))
        print("[*] Sig verification was succesfull. Moving to sym-dec")
        # now that we know the sig is good, let the sym decrypt
        # know they can decrypt and request the data

        with open(prefix+"shared/sym-dec.sem","w") as f:
            f.write("0")
    except:
        with open(prefix+"shared/final.sem","w") as f:
            f.write("0")

        print("[!] Invalid signature. Alerting producer to return a Fail")



    #time.sleep(1)


while(1):
    sigver()



