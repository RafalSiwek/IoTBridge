from flask import Flask
import logging
import paho.mqtt.client as mqtt
from aws_mqtt import AWSMqttHandler
import json
import datetime
import requests
import os
import base64


app = Flask(__name__)

DEVICE_NAME=os.environ.get('DEVICE_NAME')
MQTT_CLIENT_ID = "aws_mqtt_handler"+DEVICE_NAME

PRIV_KEY_STRING=str(os.environ.get('PRIV_KEY'))
CERT_PEM_STRING=str(os.environ.get('CERT_PEM'))
ROOT_CA_STRING=str(os.environ.get('ROOT_CA'))
AWS_HOST_STRING=str(os.environ.get('ENDPOINT'))

MQTT_BROKER_URL = 'mqtt_broker'
MQTT_CLEAN_SESSION = False
MQTT_BROKER_PORT = 1883
MQTT_KEEP_ALIVE_DURATION = 10

CA_PATH = "./creds/root-ca.pem"
CERT_PATH = "./creds/certificate.pem.crt"
PRIV_KEY_PATH = "./creds/private.pem.key"

if CERT_PEM_STRING is not None:
    f_pem_cert = open(CERT_PATH,"w")
    f_pem_cert.write(CERT_PEM_STRING)
    f_pem_cert.close()
else:
    logging.log("Env variable CERT_PEM not set")
    exit(1)

if PRIV_KEY_STRING is not None:
    f_priv_key = open(PRIV_KEY_PATH,"w")
    f_priv_key.write(PRIV_KEY_STRING)
    f_priv_key.close()   
else:
    logging.log("Env variable PRIV_KEY not set")
    exit(1)

if ROOT_CA_STRING is not None:
    f_root_ca = open(CA_PATH,"w")
    f_root_ca.write(ROOT_CA_STRING)
    f_root_ca.close()
else:
    logging.log("Env variable ROOT_CA not set")
    exit(1)

if AWS_HOST_STRING is None:
    logging.log("Env variable ENDPOINT not set")
    exit(1)

aws_mqtt=AWSMqttHandler(DEVICE_NAME,AWS_HOST_STRING)



def handle_connection(client, userdata, flags, rc):
    logging.debug("connected ok")
    logging.debug([client,userdata,flags,rc])



def handle_mqtt_message(client, userdata, message):
    try:
        msg = json.loads(message.payload.decode('utf-8'))
        msg['send_timestamp']= datetime.datetime.utcnow().isoformat()
    except TypeError as e:
        msg = {
            'data':message.payload.decode('utf-8'),
            'send_timestamp':datetime.datetime.utcnow().isoformat()
            }
    
    aws_mqtt.pub(message.topic,json.dumps(msg))
    #mqttc.publish("test",json.dumps(msg),2)


mqttc = mqtt.Client(MQTT_CLIENT_ID,MQTT_CLEAN_SESSION)
mqttc.on_message = handle_mqtt_message
mqttc.on_connect = handle_connection


try:
    mqttc.connect(MQTT_BROKER_URL, MQTT_BROKER_PORT,MQTT_KEEP_ALIVE_DURATION)
    logging.debug("Connection success")
    mqttc.subscribe("balluff/#",2)
    mqttc.loop_start()
except:
    logging.debug("internall connection failed")
    logging.error("Not able to connect to mqtt internal broker")
    exit(1)




@app.route("/hi")
def hi():
    return json.dumps({
        'connected aws client':str(aws_mqtt.client),
        'connected mqtt client':str(mqtt),
        'last message':aws_mqtt.last_pub_req,
        'aws publish buffer':aws_mqtt.messagebuffer.qsize()

    })








