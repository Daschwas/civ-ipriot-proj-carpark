import paho.mqtt.client as mqtt
import time
from random import randrange, uniform
from datetime import datetime


MQTT_HOST = "127.0.0.1" # replace localhost with the name of the computer that MQTT is running on
MQTT_PORT = 1883  # default MQTT port
MQTT_KEEP_ALIVE = 300 # seconds - this keeps the connection "open"

MQTT_CLIENT_NAME = "car-off" # must be unique
MQTT_TOPIC = "car/sensor" # main topic: test, subtopic: ducks
def on_connect(client, userdata, flags, rc):


    client.subscribe("car/sensor")

def on_publish(client, userdata, mid):
    print(f"Sending message to MQTT broker {MQTT_HOST} on port {MQTT_PORT}")
    print(f"with the topic {MQTT_TOPIC}")

def main():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_publish = on_publish

    client.connect(MQTT_HOST, MQTT_PORT, MQTT_KEEP_ALIVE)

    client.publish("car/sensor", "Status Change")

    client.loop_forever()

if __name__ == '__main__':
    main()
