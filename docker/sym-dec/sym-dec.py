
from flask import Flask, request, jsonify
import requests
import base64




from CryptoUtil import *


app = Flask(__name__)

@app.route('/encrypt',methods=['POST'])
def hello_word():

    data = request.form['data']
    key = request.form['key']

    key = base64.b64decode(key)


    iv, ct, tag = sym_encrypt(key,data)
    iv = base64.b64encode(iv).decode('ascii')
    ct = base64.b64encode(ct).decode('ascii')
    tag = base64.b64encode(tag).decode('ascii')

    to_return = {'iv':iv,'ct':ct,'tag':tag}

    return jsonify(to_return)


if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0")
