import random
import threading
import time
import paho.mqtt.client as mqtt
from WindowedDisplay import WindowedDisplay
from config_parser import parse_config

MQTT_HOST = "127.0.0.1"
MQTT_PORT = 1883
MQTT_KEEP_ALIVE = 300

MQTT_CLIENT_NAME = "car-on"
MQTT_TOPIC = "display"


class CarParkDisplay:
    FIELDS = ['Available bays', 'Temperature', 'At']

    def __init__(self):
        self.window = WindowedDisplay('Moondalup', CarParkDisplay.FIELDS)
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

        field_values = dict(zip(CarParkDisplay.FIELDS, [
            str(self.spaces),
            f'{self.temperature}℃',
            self.time
        ]))
        print(f'{self.spaces, self.temperature}')
        self.window.update(field_values)

    def check_updates(self):
        display_config = parse_config("config.toml")
        client = mqtt.Client(client_id=MQTT_CLIENT_NAME)
        client.on_connect = self.on_connect
        client.on_message = self.on_message

        client.connect(MQTT_HOST, MQTT_PORT, MQTT_KEEP_ALIVE)

        client.loop_start()
        self.spaces = int(display_config['MOO']['total_spaces'])
        while True:
            self.temp = int(random.gauss(24, 6))
            field_values = dict(zip(CarParkDisplay.FIELDS, [
                f'{self.spaces}',
                f'{self.temp}℃',
                time.strftime("%H:%M:%S")]))
            self.window.update(field_values)
            time.sleep(5)


if __name__ == '__main__':
    CarParkDisplay()
