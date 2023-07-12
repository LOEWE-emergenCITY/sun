#!/usr/bin/env python3
import json
import os
import random
import time
import socket
import sys
from paho.mqtt import client as mqtt_client

broker = '10.193.0.7'
port = 1883

def connect_mqtt(component):
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(component)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def publish(client, topic, msg):
    result = client.publish(topic, msg)
    # result: [0, 1]
    status = result[0]
    if status == 0:
        print(f"Send `{msg}` to topic `{topic}`")
    else:
        print(f"Failed to send message to topic {topic}")


if __name__ == '__main__':    

    if len(sys.argv) < 3:
        print("USAGE: %s <topic> <content>" % sys.argv[0])
        sys.exit(1)

    topic = sys.argv[1]
    content = sys.argv[2]
    client = connect_mqtt(socket.gethostname())
    
    publish(client, topic, content)
