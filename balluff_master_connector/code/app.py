from flask import Flask
import logging
import json
import os
import requests
from flask_mqtt import Mqtt
from time import sleep


app = Flask(__name__)

while True:
    device_ip=os.environ.get('MASTER_IP')
    if device_ip is not None:
        app.config['MQTT_CLIENT_ID'] = device_ip
        app.config['MQTT_CLEAN_SESSION'] = False
        app.config['MQTT_BROKER_URL'] = 'mqtt_broker'
        app.config['MQTT_BROKER_PORT'] = 1883
        app.config['MQTT_REFRESH_TIME'] = 0.2  # refresh time in seconds
        mqtt = Mqtt(app)
        #raise SystemExit(device_ip)
        break
    else:
        raise SystemExit("Setup MASTER_IP envirnoment variable ...")
        device_ip=os.environ.get('MASTER_IP')

print("connection made")
Process_URL="http://"+device_ip+"/dprop.jsn"
Status_URL="http://"+device_ip+"/index.jsn"


def make_get_req(URL):
    for i in range(3):
        try:
            r = requests.get(URL,timeout=2)
            return str(r.json())
        except requests.exceptions.Timeout:
            logging.info(f'timeout, retrying ....')
        except requests.exceptions.ConnectionError:
            logging.info(f'timeout, retrying ....')
        return "Master connection timeout"

iter = 0

while True:
    mqtt.publish("balluff/"+device_ip+"/IO-Link_Process_Data",make_get_req(Process_URL),2)
    if iter >=5:
        mqtt.publish("balluff/"+device_ip+"/Master_Status_Data",make_get_req(Status_URL),2)
        mqtt.publish("balluff/"+device_ip+"/IO-Link_Process_Data",make_get_req(Process_URL),2)
        iter = 0
    iter +=1
    sleep(0.4)







