from flask import Flask
import logging
from flask_mqtt import Mqtt
import json
import datetime

app = Flask(__name__)
app.config['MQTT_CLIENT_ID'] = 'aws_handler_mqtt'
app.config['MQTT_CLEAN_SESSION'] = True
app.config['MQTT_BROKER_URL'] = 'mqtt_broker'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_REFRESH_TIME'] = 0.2  # refresh time in seconds
mqtt = Mqtt(app)
mqtt.subscribe("#")
#mqtt.loop_start()



@app.route('/hi')
def hi():
    logging.debug("Invoking HI...")
    mqtt.publish("hi",1)
    return 'Hey, I am doing some crazy-ass web-service shit!'

@mqtt.on_log()
def handle_logging(client, userdata, level, buf):
    print(level, buf)

@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    msg = json.dumps({
        'payload':str(message.payload.decode('utf-8')),
        'timestamp_iso': datetime.datetime.utcnow().isoformat()
    })










