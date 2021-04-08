import paho.mqtt.client as mqtt
from time import time
import ssl
import logging
import json
from persistqueue import Queue




class AWSMqttHandler:

    def on_connect(self,client, userdata, flags, rc):
        logging.debug("connected ok")
        while self.messagebuffer.qsize():
            payload = json.loads(self.messagebuffer.get())
            self.client.publish(payload.topic,payload.message,1)
            self.messagebuffer.task_done()

    def on_publish(self, mqttc, obj, mid):
        logging.debug("mid: "+str(mid))

    
    def __init__(self,devicename,awshost,ca_path = "./creds/root-ca.pem",cert_path = "./creds/certificate.pem.crt",priv_key_path = "./creds/private.pem.key",queuedict="../data"):
        self.last_pub_req=None
        self.messagebuffer=Queue(queuedict)
        self.devicename = devicename
        self.client=mqtt.Client(devicename)
        self.client.on_publish = self.on_publish
        self.client.on_connect =self.on_connect
        self.client.tls_set(ca_path, certfile=cert_path, keyfile=priv_key_path, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)


        try:
            self.client.connect(awshost, 8883,60)
            logging.info("connection succeded")
            self.client.loop_start()
        except:
            logging.error("connection to aws failed")
            exit(1)
        


    def pub(self,subtopic="ip",message=""):
        self.last_pub_req=message
        logging.info("publishing to aws...")
        try:
            self.client.publish(self.devicename+"/"+subtopic,message,1)
        except:
            payload=json.dumps({
                'topic':self.devicename+"/"+subtopic,
                'message':message
            })
            self.messagebuffer.put(payload)


