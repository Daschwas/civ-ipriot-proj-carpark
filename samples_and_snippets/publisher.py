import json
import time
from random import randrange, uniform
from datetime import datetime

import paho.mqtt.client as mqtt

from paho.mqtt.client import MQTTMessage

# import paho mqtt client, aliased as mqtt

MQTT_HOST = 'localhost' # replace localhost with the name of the computer that MQTT is running on
MQTT_PORT = 1883  # default MQTT port
MQTT_KEEP_ALIVE = 300 # seconds - this keeps the connection "open"

MQTT_CLIENT_NAME = "duck-off" # must be unique
MQTT_TOPIC = "test/ducks" # main topic: test, subtopic: ducks

# instantiate an MQTT Client
client = mqtt.Client(MQTT_CLIENT_NAME)

# connect to the server/broker
client.connect(MQTT_HOST, MQTT_PORT, MQTT_KEEP_ALIVE)

print(f"Sending message to MQTT broker {MQTT_HOST} on port {MQTT_PORT}")
print(f"with the topic {MQTT_TOPIC}")

message_to_send = "Hello..."

while True:
    time.sleep(5)
    temperature = uniform(20, 25)
    now = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ+0800")
    print(f"Temperature is {temperature} at {now}")

    message_data = {"client" : MQTT_CLIENT_NAME,
                    "temp": temperature,
                     "datetime": now
                    }
    #convert the dictionary to JSON format
    message_to_send = json.dumps(message_data)
    client.publish(MQTT_TOPIC, message_to_send)
