
from flask import Flask, request, jsonify
import requests
import base64



from CryptoUtil import *


app = Flask(__name__)

@app.route('/sign',methods=['POST'])
def hello_word():

    data = request.form['data']
    key = request.form['key']

    key = base64.b64decode(key)
    key = load_priv_key(key)


    sig = key.sign(bytes(data,'utf-8'))

    return base64.b64encode(sig).decode('ascii')


if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port=8080)
