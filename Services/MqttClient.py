import uuid
import paho.mqtt.client as mqtt
import json
import Entities.Module as mod

class MQTTClient:
    def __init__(self,masterHub, username=None, password=None,id=None):
        self.id=id
        self.MasterHub = masterHub
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        if username and password:
            self.client.username_pw_set(username, password)

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code " + str(rc))
        self.subscribe(f"hub/{self.id}/#")

    def on_message(self, client, userdata, msg):
        print(msg.topic + " " + str(msg.payload))
        payload = json.loads(msg.payload.decode('utf-8'))
        payload_type = None
        if "header" in payload and "type" in payload["header"]:
            payload_type = payload["header"]["type"]
        if msg.topic == f"hub/{self.id}/module/discover" and payload_type == "request":
            data = self.MasterHub.GetUnpairedModules()
            self.client.publish(msg.topic,data)
        elif msg.topic == f"hub/{self.id}/module/pair" and payload_type == "request":
            dummyModule = mod.Module("dummy", "dummy")
            dummyModule.MacAddress = payload["body"]["macAddress"]
            dummyModule.Name = payload["body"]["name"]
            self.MasterHub.updateModuleList(dummyModule,True)
        elif msg.topic == f"hub/{self.id}/module/delete" and payload_type == "request":
            moduleId = payload["body"]["id"]
            self.MasterHub.DeleteModuleCallback(moduleId)
            
        
        # Handle incoming messages

    def connect(self, broker_address, port=1883):
        self.client.connect(broker_address, port, 60)
        self.client.loop_start()

    def publish(self, topic, payload):
        self.client.publish(topic, payload)

    def subscribe(self, topic):
        self.client.subscribe(topic)

    def disconnect(self):
        self.client.loop_stop()
        self.client.disconnect()

