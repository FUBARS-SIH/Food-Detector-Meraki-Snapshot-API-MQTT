import paho.mqtt.client as mqtt
import json

client = mqtt.Client()
broker, topic = 'mqtt.eclipse.org', "food_detection"

def  on_connect(client, userData, flags, rc):
    if rc == 0:
        print("Connected to the broker. OK")
        client.subscribe(topic)
    else:
        print(f"Bad connection returned code {rc}")

def  on_log(client, userData, level, buf):
    print(f"[LOG] {buf}")

def on_disconnect(client, userData, flags, rc=0):
    client.loop_stop()
    print(f"Disconnected result code {str(rc)}")

def on_message(client, userData, msg):
    topic = msg.topic
    msg = json.loads(msg.payload.decode("utf-8","ignore"))
    print(f"[MSG from topic:{topic}]\n{msg}")

client.on_connect = on_connect
# client.on_log = on_log
client.on_disconnect = on_disconnect
client.on_message = on_message

print("Connecting to the broker")
client.connect(broker,1883,60)
client.loop_forever()