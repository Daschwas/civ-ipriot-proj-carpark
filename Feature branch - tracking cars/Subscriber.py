import paho.mqtt.client as mqtt

MQTT_HOST = "127.0.0.1" # replace localhost with the name of the computer that MQTT is running on
MQTT_PORT = 1883  # default MQTT port
MQTT_KEEP_ALIVE = 300 # seconds - this keeps the connection "open"

MQTT_CLIENT_NAME = "car-out" # must be unique
MQTT_TOPIC = "car/sensor" # main topic: test, subtopic: ducks
def on_connect(client, userdata, flags, rc):
    print(f"{MQTT_CLIENT_NAME} is listening on port {MQTT_PORT} for messages with the topic {MQTT_TOPIC}")
    # Subscribe to the topic
    client.subscribe("car/sensor")

def on_message(client, userdata, msg):
    print(f"Received message: {msg.payload.decode()}")

def main():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect("127.0.0.1", 1883, 60)

    client.loop_forever()

if __name__ == '__main__':
    main()
