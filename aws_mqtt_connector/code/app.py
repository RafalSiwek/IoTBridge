from flask import Flask
import logging
import paho.mqtt.client as mqtt
from aws_mqtt import AWSMqttHandler
import json
import datetime
import requests

app = Flask(__name__)
MQTT_CLIENT_ID = "aws_mqtt_handler"
MQTT_BROKER_URL = 'mqtt_broker'
MQTT_CLEAN_SESSION = False
MQTT_BROKER_PORT = 1883
MQTT_KEEP_ALIVE_DURATION = 10


aws_mqtt=AWSMqttHandler()

def handle_connection(client, userdata, flags, rc):
    logging.debug("connected ok")
    logging.debug([client,userdata,flags,rc])


def handle_logging(client, userdata, level, buf):
    print(level, buf)

def handle_mqtt_message(client, userdata, message):
    msg = json.dumps({
        'payload':str(message.payload.decode('utf-8')),
        'timestamp_iso': datetime.datetime.utcnow().isoformat()
    })
    aws_mqtt.pub(message.topic,msg)


mqttc = mqtt.Client(MQTT_CLIENT_ID,MQTT_CLEAN_SESSION)
mqttc.on_message = handle_mqtt_message
mqttc.enable_logger()
mqttc.on_log = handle_logging
mqttc.on_connect = handle_connection

try:
    mqttc.connect(MQTT_BROKER_URL, MQTT_BROKER_PORT,MQTT_KEEP_ALIVE_DURATION)
except:
    logging.debug("internall connection failed")
    exit(1)

logging.debug("Connection success")
mqttc.subscribe("balluff/#",2)
mqttc.loop_start()

@app.route("/hi")
def hi():
    return json.dumps({
        'connected aws client':str(aws_mqtt.client),
        'connected mqtt client':str(mqtt),
        'last message':aws_mqtt.last_pub_req,
        'aws publish buffer':aws_mqtt.messagebuffer

    })








