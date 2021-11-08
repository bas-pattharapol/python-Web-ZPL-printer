# -*- coding: utf-8 -*-

import os ,sys
from platform import machine

from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask.sessions import NullSession
from PIL import Image

import io

from sbpl import *
from paho.mqtt import client as mqtt_client

import random
import time


import time 

broker = '10.11.1.1'
port = 1883

client_id = f'python-mqtt-{random.randint(0, 1000)}'
username = 'plc1'
password = 'plc@2021'


app = Flask('MyService')

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def publish(client,Material,Mat_Name,Code_Type,Barcode,Amount,topic):
    msg_count = '{"version":0.1,"Code":0,"index":' + Amount + ',"barcode":' + Barcode +',"code_type":"' +Code_Type+'"}'
   
    msg = f'{msg_count}'
    result = client.publish(topic, msg)

    status = result[0]
    if status == 0:
        print(f"Send `{msg}` to topic `{topic}`")
    else:
        print(f"Failed to send message to topic {topic}")

    time.sleep(1)

    msg_count1 = '{"version":0.1,"Code":3,"index":' + Amount + ',"barcode":' + Barcode +',"code_type":"' +Code_Type+'"}'
   
    msg1 = f'{msg_count1}'
    result1 = client.publish(topic, msg1)

    status1 = result1[0]
    if status1 == 0:
        print(f"Send `{msg}` to topic `{topic}`")
        count = 1
    else:
        print(f"Failed to send message to topic {topic}")
    count = 0
    # result: [0, 1]
    return count

def subscribe(client: mqtt_client,topic):
    def on_message(client, userdata, msg):
        d = json.loads(msg.payload)
        print("code : " + str(d["Code"]))

        if str(d["Code"]) == "5" :
            print("ok")
            client.disconnect()
            
    client.subscribe(topic)
    client.on_message = on_message
    
'''
def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client)

    #subscribe(client)
    #client.loop_forever()
'''

@app.route('/re', methods=["GET", "POST"])
def re():  
    if request.method == "POST":
        time.sleep(1)
        os.execl(sys.executable, 'python', __file__, *sys.argv[1:])
        
    
    return render_template("re.html") 

@app.route('/error', methods=["GET", "POST"])
def error():  
    if request.method == "POST":
        time.sleep(1)
        os.execl(sys.executable, 'python', __file__, *sys.argv[1:])
        
    
    return render_template("error.html") 
    

@app.route('/ok')
def ok():  
    return render_template("noPrinter.html")
    

def stop():
    import requests
    resp = requests.get('http://localhost:5001/shutdown')

@app.route('/index', methods=["GET", "POST"])
def test():

    if request.method == "POST":
        
        Material = request.form['Material']
        Mat_Name = request.form['Mat_Name']
        machineSec = request.form['machineSec']
        Barcode = request.form['Barcode']
        Amount = request.form['Amount']

        client = connect_mqtt()
        client.loop_start()
        hostasd = None

        if machineSec == "15":
            publish(client,Material,Mat_Name,"ean",Barcode,Amount,"/line/1/send")
            hostasd = "10.11.1.15"
        elif machineSec == "16":
            publish(client,Material,Mat_Name,"ean",Barcode,Amount,"/line/2/send")
            hostasd = "10.11.1.16"

        try:
            print(hostasd)
            client.loop_stop()

            json_str =[
                {"host":hostasd, "port": 9100, "communication": "SG412R_Status5"},
                [
                    {"set_label_size": [440, 158]},

                        {"shift_jis": 0},
                        {"rotate_270": 0},   
                        {"comment": "==Material Name=="},
                        {"pos": [157, 230], "expansion": [1530], "ttf_write": Material, "font": "AngsanaNew-Bold.ttf"},                                        
                        {"comment": "==Material Name=="},
                        {"pos": [133, 240], "expansion": [1530], "ttf_write": Mat_Name, "font": "AngsanaNew-Bold.ttf"},
                        {"comment": "==barcode=="},
                        {"pos": [105, 225], "jan_13": [Barcode, 2, 60]},   
                        {"comment": "== ID =="},
                        {"pos": [51, 235], "expansion": [1700], "ttf_write": "8 851989 96056 2", "font": "CmPrasanmit Bold.ttf"},                             
                        {"rotate_0": 0},          
                        {"print": int(Amount)}
                    ]
                ]
                
            comm = SG412R_Status5()
            gen = LabelGenerator()
            parser = JsonParser(gen)
            parser.parse(json_str)
            print(json_str)
            parser.post(comm)

                    
            client = connect_mqtt()
            if machineSec == "15":
                subscribe(client,"/line/1/receipt")
            elif machineSec == "16":
                subscribe(client,"/line/2/receipt")

            client.loop_forever()
            
            return redirect(url_for('re'))
        except:
            return redirect(url_for('error'))

        

    time.sleep(3)
    return render_template("test.html")

#-------------------- Country --------------------------------------
def start():
    app.run(host='0.0.0.0',debug=True,use_reloader=True, port=5000)

count = 0
slp = 1
if __name__ == "__main__":
    slp = 1
    
    start()
