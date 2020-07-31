from configparser import ConfigParser
from Meraki.utils import snapshot
from DetectionTools.ops import load_model, get_detected_classes
import numpy as np
import random
import paho.mqtt.client as mqtt
import json

config = ConfigParser()

config.read('config.ini')

serial, api_key, network_id, model_dir = (
	config.get('credentials','camera_serial'),
    config.get('credentials','api_key'),
    config.get('credentials','network_id'),
    config.get('model','model_dir')
)

if __name__ == '__main__':

    # load model
    print("Loading model...",end="\n")
    detect_fn = load_model(model_dir)
    print("Model has been loaded.",end="\n")

    #mqtt client
    client = mqtt.Client()

    def  on_connect(client, userData, flags, rc):
        if rc == 0:
            print("Connected to the broker. OK")
        else:
            print(f"Bad connection returned code {rc}")

    def  on_log(client, userData, level, buf):
        print(f"[LOG] {buf}")

    def on_disconnect(client, userData, flags, rc=0):
        client.loop_stop()
        client.disconnect()
        print(f"Disconnected result code {str(rc)}")
        
    client.on_connect = on_connect
    # client.on_log = on_log
    client.on_disconnect = on_disconnect

    broker = 'mqtt.eclipse.org'
    print("Connecting to the broker")
    client.connect(broker,1883,60)
    client.loop_start()

    #keeps fetching images
    while True:

        #fetch image    
        image_loc, timestamp = snapshot(network_id,serial, api_key)
        # print("Image Loaded\n")

        #detect images
        # print("Detecting Images\n")
        image_loc = random.choice(['/static/mid-day-meal-1.jpg','/static/mid-day-meal-2.jpeg','/static/mid-day-meal-3.jpg'])
        classes = get_detected_classes(detect_fn, image_loc, threshold=0.8)

        data = json.dumps({
            "ts": timestamp,
            "objects": classes
        })
        topic = "food_detection"
        client.publish(topic,payload=data)
        print(f"[SENT] {data}")
