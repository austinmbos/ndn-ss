
from flask import Flask, request, jsonify
import requests
import base64



from CryptoUtil import *


app = Flask(__name__)

@app.route('/verify',methods=['POST'])
def hello_word():

    sig = request.form['sig']
    sig = base64.b64decode(sig)
    pub_key = request.form['pub_key']
    pub_key = base64.b64decode(pub_key)
    pub_key = load_pub_key(pub_key)
    data = request.form['data']

    try:
        pub_key.verify(sig,bytes(data,'utf-8'))
        status = "GOOD"
    except:
        status = "BAD"


    return status


if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port=8090)
