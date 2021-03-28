import paho.mqtt.client as mqtt
from time import time
import ssl
import logging

class AWSMqttHandler:

    def on_connect(self,client, userdata, flags, rc):
        if rc==0:
            logging.debug("connected ok")
            for message in self.messagebuffer:
                self.client.publish(self.devicename+"/"+subtopic,message,1)
            self.messagebuffer[:]=[]


        
    def on_publish(self, mqttc, obj, mid):
        logging.debug("mid: "+str(mid))

    def on_log(self, mqttc, obj, level, string):
        logging.info(string)
    
    def __init__(self,devicename="HW01",ca_path = "./creds/root-ca.pem",cert_path = "./creds/certificate.pem.crt",priv_key_path = "./creds/private.pem.key",awshost = "a18s3lp9ll2h3-ats.iot.eu-central-1.amazonaws.com"):
        self.last_pub_req=None
        self.messagebuffer=[]
        self.devicename = devicename
        self.client=mqtt.Client(devicename)
        self.client.on_publish = self.on_publish
        self.client.on_log = self.on_log
        self.client.on_connect =self.on_connect
        self.client.tls_set(ca_path, certfile=cert_path, keyfile=priv_key_path, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)
        try:
            self.client.connect(awshost, 8883,10)
        except:
            print("connection failed")
            exit(1)
        
        print("connection succeded")
        self.client.loop_start()

    def pub(self,subtopic="ip",message=""):
        self.last_pub_req=message
        logging.info("publishing to aws...")
        try:
            self.client.publish("balluff/"+self.devicename+"/"+subtopic,message,1)
        except:
            self.messagebuffer.append(message)


