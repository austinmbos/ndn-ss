
from pyndn import Name, Interest, Face
from pyndn.security import KeyChain
from pyndn.util import Blob

import time
import base64
import json
import copy
import sys
import threading
import signal
import statistics as stat

from CryptoUtil import *


quit_flag = 0
collected_values=[]
mean_throughput = 0


# collecting is done here, gather data now
def sig_handler(sig,frame):
    print("[!] Recieved SIGINT")
    global quit_flag
    quit_flag = 1
    mean_throughput = stat.mean(collected_values)
    print("mean throughput: " + str(round(mean_throughput,3)))
    with open("thru-put.dat","a") as f:
        f.write(str(mean_throughput)+"\n")
    sys.exit(0);


class Consumer(object):
    def __init__(self,isGood):
        self.status = 1
        self.count = 1
        self.data_count = 1
        self.data_rate = 0.03
        self.face = Face()
        self.isGood = isGood

        # load user keys
        with open("shared/system-info.json") as f:
            self.data = json.load(f)

        self.sym_key = base64.b64decode(self.data['austin']['sym_key'])
        self.name = None
        self.req_name = ""
        self.priv_key = ""

        print("Finished initializing consumer")


    def buildName(self):
        self.name = Name("/ndn-ss/austin")
        self.req_name = "/example/test"+str(self.count)
        self.count = self.count + 1
        iv,ct,tag = sym_encrypt(self.sym_key,self.req_name)
        self.name.append(base64.b64encode(iv).decode('ascii'))
        self.name.append(base64.b64encode(ct).decode('ascii'))
        self.name.append(base64.b64encode(tag).decode('ascii'))

        self.priv_key = load_priv_key(base64.b64decode(self.data['austin']['priv_key']))
        if self.isGood == True:
            sig=base64.b64encode(self.priv_key.sign(bytes("austin",'utf-8'))).decode('ascii')
        if self.isGood == False:
            sig=base64.b64encode(self.priv_key.sign(bytes("abstin",'utf-8'))).decode('ascii')
        
        self.name.append(sig)



    def sendInterest(self):
        self.buildName()
        self.face.expressInterest(self.name,self.onData,self.onTimeout)
        self.status = 1
        #print("Sending Interest: "+str(self.count))


    def sendInterest_mod(self):
        i = Interest()
        i.setMustBeFresh(True)
        i.setInterestLifetimeMilliseconds(5000)
        self.buildName()
        self.face.expressInterest(self.name,i,self.onData,self.onTimeout)
        self.status = 1
        #print("[MOD] Sending Interest: "+str(self.count))


    def onData(self,interest,data):
        #print("Got Data packet"+str(data.getContent()))
        self.data_count = self.data_count + 1
        #self.status = 0
        #self.sendInterest_mod()
        #self.sendInterest()
        

    def onTimeout(self,interest):
        print("\n\n\n\nTimeout...")
        print("Need to reduce rate...")
        quit_flag = 1


    # meant to be threaded
    def proc_E(self):
        while self.status == 1:
            if quit_flag == 1:
                quit()
            self.face.processEvents()
            time.sleep(0.2)
            

    def spamInterest(self):
        while 1:
            self.sendInterest()
            #self.sendInterest_mod()
            time.sleep(self.data_rate)
            if quit_flag == 1:
                quit()



    # meant to be threaded
    def getThroughput(self):
        global run_slow
        start = time.time()
        while 1:
            if quit_flag == 1:
                quit()
            # reset the timer and interest count
            s_count = self.count
            s_d_count = self.data_count
            end = time.time()
            status = end-start
            while status <= 1.0:
                end = time.time()
                status = end-start

            e_count = self.count
            e_d_count = self.data_count
            final_count = e_count - s_count 
            d_final_count = e_d_count - s_d_count 
            start = time.time()
            print("")
            print("====================================")
            print("throughput (interest) : " + str(final_count))
            print("throughput (data)     : " + str(d_final_count))
            print("time                  : " + str(round(status,3)))
            print("data rate (inverse)   : " + str(self.data_rate))
            print("====================================")
            

            collected_values.append(final_count)
            if run_slow == False: 

                # if we are receiving a data for every interest on time
                # increase the data_rate
                print(str(d_final_count) + "   " + str(final_count))
                if d_final_count >= final_count:
                    if self.data_rate >= 0.1:
                        self.data_rate = self.data_rate - 0.05
                    elif self.data_rate < 0.1 and self.data_rate > 0.05:
                        self.data_rate = self.data_rate - 0.01
                    elif self.data_rate <= 0.05 and self.data_rate > 0.001:
                        self.data_rate = self.data_rate - 0.001
                    else:
                        self.data_rate = self.data_rate - 0.0001

                if d_final_count <= final_count - 3:
                    self.data_rate = 0.03
                



if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("Enter good of bad")
        quit()

    run_slow = False
    if len(sys.argv) == 3:
        if sys.argv[2] == "--slow":
            run_slow = True

    if sys.argv[1] == "good":
        isGood = True
    if sys.argv[1] == "bad":
        isGood = False

    signal.signal(signal.SIGINT,sig_handler)

    print("Running client")
    consume = Consumer(isGood)
    consume.sendInterest()



    t_2 = threading.Thread(target=consume.getThroughput,args=[])
    t_2.start()

    # thread to not block when processing events,
    # only want to call processEvents once, and send many many interests
    t_1 = threading.Thread(target=consume.proc_E,args=[])
    t_1.start()


    consume.spamInterest()

        
