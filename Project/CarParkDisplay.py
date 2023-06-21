import random
import threading
import time
from WindowedDisplay import WindowedDisplay
import paho.mqtt.client as mqtt

MQTT_HOST = "127.0.0.1"
MQTT_PORT = 1883
MQTT_KEEP_ALIVE = 300

MQTT_CLIENT_NAME = "car-on"
MQTT_TOPIC = "display"


class CarParkDisplay:
    fields = ['Available bays', 'Temperature', 'At']

    def __init__(self):
        self.window = WindowedDisplay('Moondalup', CarParkDisplay.fields)
        updater = threading.Thread(target=self.check_updates)
        updater.daemon = True
        updater.start()
        self.window.show()
        self.spaces = 0
        self.time = ""
        self.temperature = ""

    def on_connect(self, client, userdata, flags, rc):
        print(f"{MQTT_CLIENT_NAME} is listening on port {MQTT_PORT} for messages with the topic {MQTT_TOPIC}")

        client.subscribe(MQTT_TOPIC)

    def on_message(self, client, userdata, msg):

        payload = msg.payload.decode()
        print({payload})
        values = dict(value.split(': ') for value in payload.split(', '))

        self.spaces = values['SPACES']
        self.time = values['TIME']
        self.temperature = values['TEMP']

        field_values = dict(zip(CarParkDisplay.fields, [
            str(self.spaces),
            f'{self.temperature}℃',
            self.time
        ]))
        print(f'{self.spaces, self.temperature}')
        self.window.update(field_values)

    def check_updates(self):
        client = mqtt.Client(client_id=MQTT_CLIENT_NAME)
        client.on_connect = self.on_connect
        client.on_message = self.on_message

        client.connect(MQTT_HOST, MQTT_PORT, MQTT_KEEP_ALIVE)

        client.loop_start()
        self.spaces = "T.B.A."
        while True:
            self.temp = int(random.gauss(24, 6))
            field_values = dict(zip(CarParkDisplay.fields, [
                f'{self.spaces}',
                f'{self.temp}℃',
                time.strftime("%H:%M:%S")]))
            self.window.update(field_values)
            time.sleep(10)


if __name__ == '__main__':
    CarParkDisplay()
