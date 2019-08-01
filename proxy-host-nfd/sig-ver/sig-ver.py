import base64
import json
import time
import urllib.parse
from pyndn import Face,Name,Interest,Data
from pyndn.security import KeyChain
from CryptoUtil import *


class Counter:
    def __init__(self,keyChain,certName):
        self.rec = 1
        self.keyChain = keyChain
        self.certName = certName

    def onInterest(self,prefix,interest,face,interestFilterId,filter):
        print("[*] Got interest")
        self.rec = 0
        data = Data(interest.getName())
        content = "hello"
        data.setContent(content)
        #self.keyChain.sign(data,self.certName)
        face.putData(data)
        print("! finished in onInterest")

    def onRegisterFailed(self):
        print("Fail..")



def main():

    face = Face()
    keyChain = KeyChain()
    face.setCommandSigningInfo(keyChain,keyChain.getDefaultCertificateName())

    prefix = Name("/test")

    counter = Counter(keyChain,keyChain.getDefaultCertificateName())
    face.registerPrefix(prefix,counter.onInterest,counter.onRegisterFailed)

    while counter.rec == 1:
        face.processEvents()
        time.sleep(0.5)

    face.shutdown()


main()

