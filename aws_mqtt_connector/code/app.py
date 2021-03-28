from flask import Flask
import logging
from flask_mqtt import Mqtt
from aws_mqtt import AWSMqttHandler
import json
import datetime
import requests

app = Flask(__name__)
app.config['MQTT_CLIENT_ID'] = 'AWSClient1'
app.config['MQTT_CLEAN_SESSION'] = False
app.config['MQTT_BROKER_URL'] = 'mqtt_broker'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_REFRESH_TIME'] = 0.2  # refresh time in seconds
mqtt = Mqtt(app)
mqtt.subscribe("balluff/#")
aws_mqtt=AWSMqttHandler()

@mqtt.on_log()
def handle_logging(client, userdata, level, buf):
    print(level, buf)

@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    msg = json.dumps({
        'payload':str(message.payload.decode('utf-8')),
        'timestamp_iso': datetime.datetime.utcnow().isoformat()
    })
    aws_mqtt.pub(message.topic,msg)


@app.route("/hi")
def hi():
    return json.dumps({
        'connected aws client':str(aws_mqtt.client),
        'connected mqtt client':str(mqtt),
        'last message':aws_mqtt.last_pub_req,
        'aws publish buffer':aws_mqtt.messagebuffer

    })








