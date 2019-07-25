
from flask import Flask, request, jsonify
import requests
import base64



app = Flask(__name__)

@app.route('/sign',methods=['POST'])
def hello_word():

    return "hello there"


if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port=8080)
