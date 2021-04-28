import sys
from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import random

from testFlask import *

from flask import Response
import json


app = Flask(__name__)
CORS(app)
counter = 0
print(os.environ)


@app.route("/index", methods=['GET'])
def index():
    return jsonify({
        'title': "Welcome to Electron - Vue - Python stack !",
        'description': 'This content came from the api backend in python using the flask framework'
        })


@app.route('/increment')
def increment():
    global counter
    counter += 1
    return jsonify({'counter': counter})

# init
testObj = testFlask()
print(testObj.handle)
num = 0
val = 0

@app.route("/pressure", methods=['GET', 'POST'])
def echarts():
    if request.method == 'POST':
        typeCode = request.get_json()['typeCode'];
        print(typeCode)
        if(typeCode == 0) : #typecode == 0 : control switch
            sta = request.get_json()['status']
            if sta == True :
                print("switch on, open device")
                """ global testObj """
                testObj.open()
                print(testObj.handle)
            else:
                print("switch off, close device")
                """ global testObj """
                testObj.close()
        
        elif(typeCode == 1) : #typeCode == 1 : control pressure channel
            num = request.get_json()['num']
            val = request.get_json()['val']
            print(num, val)
            testObj.set(num, val)

    elif request.method == 'GET':
        return jsonify(testObj.read())

    return 'echarts'

@app.route("/resistence", methods=['GET'])
def test():
    d = {'val1' : 0, 'val2' : 0}
    d['val1'] = random.randint(-1e6, 1e6)
    d['val2'] = random.randint(-1e6, 1e6)
    return jsonify(d)

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000)