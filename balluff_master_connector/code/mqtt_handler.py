import paho.mqtt.client as mqtt

class MQTTClient:
    def on_connect(self, mqttc, obj, flags, rc):
        print("rc: "+str(rc))

    def on_message(self, mqttc, obj, msg):
        print(msg.topic+" "+str(msg.qos)+" "+str(msg.payload))

    def on_publish(self, mqttc, obj, mid):
        print("mid: "+str(mid))

    def on_subscribe(self, mqttc, obj, mid, granted_qos):
        self.client.on_message = on_message
        print("Subscribed: "+str(mid)+" "+str(granted_qos))


    def on_log(self, mqttc, obj, level, string):
        print(string)

    def __init__(self,devicename="HW01",brokeraddress="mqtt_broker"):
        self.devicename = devicename
        self.client=mqtt.Client(devicename)
        self.client.on_connect = self.on_connect
        self.bokeraddress=brokeraddress
        self.client.connect(self.bokeraddress, 1883)
        

    def run(self):
        self.client.subscribe("$SYS/#")
        self.client.loop_start()

    def stop(self):
        self.client.loop_stop()
    
    def pub(self,message="NaN"):
        self.client.publish("$SYS/"+self.devicename,message)


