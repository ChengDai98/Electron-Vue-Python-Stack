import sys
from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import random

import nidaqmx

from testFlask import *
from smacqDAQ import *
from niDAQ import *

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
""" testObj = testFlask()
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
                testObj.open()
                print(testObj.handle)
            else:
                print("switch off, close device")
                testObj.close()
        
        elif(typeCode == 1) : #typeCode == 1 : control pressure channel
            num = request.get_json()['num']
            val = request.get_json()['val']
            print(num, val)
            testObj.set(num, val)

    elif request.method == 'GET':
        return jsonify(testObj.read())

    return 'echarts' """

# init

testObj = SmacqController()
num = 0
val = 0

val_pakg = [0, 0]

@app.route("/pressure", methods=['GET', 'POST'])
def echarts():

    if request.method == 'POST':
        typeCode = request.get_json()['typeCode']
        print(typeCode)
        if(typeCode == 0) : #typecode == 0 : control switch
            sta = request.get_json()['status']
            if sta == True :
                print("switch on, open device")
                testObj.open_device_and_init_avgs()
                testObj.init_DA(0) #应该是传入的值
                testObj.start_read_pressure()
            else:
                print("switch off, close device")
                testObj.reset_DA()
                testObj.stop_process()
        
        elif(typeCode == 1) : #typeCode == 1 : control pressure channel
            val_pakg[0] = request.get_json()['num']
            val_pakg[1] = request.get_json()['val']
            print("post val and num:", val_pakg[0], val_pakg[1])
            testObj.set_pressure_channel(val_pakg[0])
            testObj.change_DA(val_pakg[0], val_pakg[1]) #unless these two avgs is not global var

    elif request.method == 'GET':
        data = []
        for i in range(0, 4):
            tmp = testObj.read_data()
            data.append(tmp)

        d = {'given': val_pakg[1], 'observed': data[3]}
        
        # print("request get val" , d)
        return jsonify(d)

    return 'echarts'

""" @app.route("/resistence", methods=['GET'])
def test():
    d = {'val1' : 0, 'val2' : 0}
    d['val1'] = random.randint(-1e6, 1e6)
    d['val2'] = random.randint(-1e6, 1e6)
    return jsonify(d) """


nitestOBJ = nidaqController()
@app.route("/resistence", methods=['GET', 'POST'])
def get_resist():
    if request.method == 'POST':
        code = request.get_json()['code']
        if code == 'ch0':
            pass
        elif code == 'c0':
            nitestOBJ.set_averaging(request.get_json()['val'])
        elif code == 'c1':
            nitestOBJ.set_frequency(request.get_json()['val'])
        elif code == 'c2':
            nitestOBJ.set_amplitude(request.get_json()['val'])
        elif code == 'c3':
            nitestOBJ.set_holding_voltage(request.get_json()['val'])
        elif code == 's0':
            if request.get_json()['val'] == 'Voltage Clamp':
                nitestOBJ.set_clamp_args(0)
            else:
                nitestOBJ.set_clamp_args(1)
        else:
            print("invalid input")

    if request.method == 'GET':
        nitestOBJ.gen_new_squarewave()
        return jsonify(nitestOBJ.get_data())

    return "resist"


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000)