from flask import Flask
import logging
from flask_mqtt import Mqtt
import json
import datetime
import os
import asyncio
import requests

device_ip=os.environ.get('MASTER_IP')
if device_ip is None:
    raise SystemExit("Setup MASTER_IP envirnoment variable ...")


app = Flask(__name__)
app.config['MQTT_CLIENT_ID'] = device_ip
app.config['MQTT_CLEAN_SESSION'] = True
app.config['MQTT_BROKER_URL'] = 'mqtt_broker'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_REFRESH_TIME'] = 0.2  # refresh time in seconds
mqtt = Mqtt(app)
global run
run = False

@app.route('/start')
def start():
    run = True
    return 'Start IoT connector for device IP '+device_ip

@app.route('/stop')
def stop():
    run = False
    return 'Stop IoT connector for device IP '+device_ip

@mqtt.on_log()
def handle_logging(client, userdata, level, buf):
    print(level, buf)











