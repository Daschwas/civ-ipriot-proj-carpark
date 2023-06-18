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

MQTT_CLIENT_NAME = "duck-down" # must be unique
MQTT_SUBSCRIBE_TOPIC = "test/ducks" # main topic: test, subtopic: ducks
MQTT_PUBLISH_TOPIC = "test/geese"

# instantiate an MQTT Client
client = mqtt.Client(MQTT_CLIENT_NAME)

# connect to the server/broker
client.connect(MQTT_HOST, MQTT_PORT, MQTT_KEEP_ALIVE)

# subscribe to the topic
client.subscribe(MQTT_SUBSCRIBE_TOPIC)

def on_message_callback(client, userdata, message):
    msg = message
    msg_data = str(msg.payload.decode("UTF-8")) # decode the message payload into UTF-* characters
    data = json.loads(msg_data)

    temp = data['temp']
    if temp<22:
        message_text = "Too cold"
    elif temp>23:
        message_text = "too hot"
    else:
        message_text: "perrrrfect"

    #have to have space after

    out_data = { "message": message_text}
    data_as_json = json.dumps(out_data)
    output = f"{out_data}"

    client.publish(MQTT_PUBLISH_TOPIC, data_as_json)



# listen for messages - call the 'callback' when one is received
client.on_message = on_message_callback
print(f"{MQTT_CLIENT_NAME} is listening on port {MQTT_PORT} for messages with the topic {MQTT_SUBSCRIBE_TOPIC}")
client.loop_forever()