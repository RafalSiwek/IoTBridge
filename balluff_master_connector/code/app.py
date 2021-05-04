from flask import Flask
import logging
import json
import os
import requests
import paho.mqtt.client as mqtt
from persistqueue import Queue
from time import sleep
import datetime


app = Flask(__name__)

name=os.environ.get('DEVICE_NAME')
device_ip=os.environ.get('MASTER_IP')
app = Flask(__name__)
MQTT_CLIENT_ID = 'balluff_master:'+device_ip
MQTT_BROKER_URL = 'mqtt_broker'
MQTT_CLEAN_SESSION = False
MQTT_BROKER_PORT = 1883
MQTT_KEEP_ALIVE_DURATION = 10
Process_URL="http://"+device_ip+"/dprop.jsn"
Status_URL="http://"+device_ip+"/index.jsn"

messagebuffer=Queue("../data")

def publish(topic,message):
    try:
        mqttc.publish(topic,message,2)
    except:
        payload=json.loads({
            'topic':topic,
            'message':message
        })
        messagebuffer.put(payload)


def handle_connection(client, userdata, flags, rc):
    logging.debug("connected ok")
    logging.debug([client,userdata,flags,rc])
    while messagebuffer.qsize():
        payload = json.loads(messagebuffer.get())
        mqttc.publish(payload.topic,payload.message,2)
        messagebuffer.task_done()


mqttc = mqtt.Client(MQTT_CLIENT_ID,MQTT_CLEAN_SESSION)
try:
    mqttc.connect(MQTT_BROKER_URL, MQTT_BROKER_PORT,MQTT_KEEP_ALIVE_DURATION)
    logging.info("Connection success")
    mqttc.loop_start()
except:
    logging.info("internall connection failed")
    exit(1)



def make_get_req(URL):
    for i in range(5):
        try:
            r = requests.get(URL,timeout=2)
            msg = json.dumps({
                'data':r.json(),
                'receive_time':datetime.datetime.utcnow().isoformat()
            })
            return msg
        except requests.exceptions.Timeout:
            logging.info(f'timeout, retrying ....')
        except requests.exceptions.ConnectionError:
            logging.info(f'timeout, retrying ....')
    msg = json.dumps({
        'data':"Master connection timeout",
        'receive_timestamp':datetime.datetime.utcnow().isoformat()
    })
    return msg

iter = 0

while True:
    logging.info(messagebuffer.qsize())
    publish("balluff/"+name+"/IO-Link_Process_Data",make_get_req(Process_URL))
    if iter >=5:
        publish("balluff/"+name+"/Master_Status_Data",make_get_req(Status_URL))
        publish("balluff/"+name+"/IO-Link_Process_Data",make_get_req(Process_URL))
        iter = 0
    iter +=1
    sleep(0.4)







