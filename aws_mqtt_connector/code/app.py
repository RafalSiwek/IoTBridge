from flask import Flask
import logging
from flask_mqtt import Mqtt
from aws_mqtt import AWSMqttHandler
import json
import datetime
import requests

app = Flask(__name__)
app.config['MQTT_CLIENT_ID'] = 'aws_handler_mqtt'
app.config['MQTT_CLEAN_SESSION'] = True
app.config['MQTT_BROKER_URL'] = 'mqtt_broker'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_REFRESH_TIME'] = 0.2  # refresh time in seconds
mqtt = Mqtt(app)
mqtt.subscribe("#")
#mqtt.loop_start()

aws_mqtt=AWSMqttHandler()


@app.route('/hi')
def hi():
    logging.debug("Invoking HI...")
    mqtt.publish("hi",1)
    return 'Hey, I am doing some crazy-ass web-service shit!'

@app.route('/req')
def get_req():
    # api-endpoint 
    URL = "http://192.168.0.2/dprop.jsn"
    # sending get request and saving the response as response object 
    while True:
        try:
            r = requests.get(URL,timeout=10)
        except requests.exceptions.Timeout:
            print(f'timeout, retrying ....')
            continue
        except requests.exceptions.TooManyRedirects:
            return "Wrong url"
        except requests.exceptions.RequestException as e:
            print(e)
            raise SystemExit(e)
        break

    # extracting data in json format 
    data = r.json() 
    # printing the output 
    print(f'{data}')
    #return data
    return str(data)


@mqtt.on_log()
def handle_logging(client, userdata, level, buf):
    print(level, buf)

@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    msg = json.dumps({
        'payload':str(message.payload.decode('utf-8')),
        'timestamp_iso': datetime.datetime.utcnow().isoformat()
    })


    #mqtt.publish("elo",msg)
    aws_mqtt.pub(message.topic,msg)










