import random
import threading
import time
import tkinter as tk
from typing import Iterable
from WindowedDisplay import WindowedDisplay
import paho.mqtt.client as mqtt
from config_parser import parse_config

MQTT_HOST = "127.0.0.1"  # replace localhost with the name of the computer that MQTT is running on
MQTT_PORT = 1883  # default MQTT port
MQTT_KEEP_ALIVE = 300  # seconds - this keeps the connection "open"

MQTT_CLIENT_NAME = "car-on"  # must be unique
MQTT_TOPIC = "car/sensor"  # main topic: test, subtopic: ducks


class CarParkDisplay:
    """Provides a simple display of the car park status. This is a skeleton only. The class is designed to be customizable without requiring an understanding of tkinter or threading."""

    # determines what fields appear in the UI
    fields = ['Available bays', 'Temperature', 'At']

    def __init__(self):
        self.data = self.load_data()
        self.window = WindowedDisplay(
            'Moondalup', CarParkDisplay.fields)

        updater = threading.Thread(target=self.check_updates)
        updater.daemon = True
        updater.start()
        self.window.show()

    def load_data(self):
        config = parse_config("config.toml")
        return {
            'total_spaces': config.get("MOO", {}).get("total_spaces", 0),
            'total_cars': config.get("MOO", {}).get("total_cars", 0)
        }

    def on_connect(self, client, userdata, flags, rc):
        print(f"{MQTT_CLIENT_NAME} is listening on port {MQTT_PORT} for messages with the topic {MQTT_TOPIC}")
        client.subscribe(MQTT_TOPIC)

    def on_message(self, client, userdata, msg):
        payload = msg.payload.decode()
        if payload == "entry":
            self.data['total_cars'] += 1
            print(f"Car entered. Total cars: {self.data['total_cars']}")
        elif payload == "exit":
            self.data['total_cars'] -= 1
            print(f"Car exited. Total cars: {self.data['total_cars']}")

        available_bays = self.data['total_spaces'] - self.data['total_cars']
        print(f"Total spaces: {self.data['total_spaces']}")
        print(f"Available bays: {available_bays}")
        field_values = dict(zip(CarParkDisplay.fields, [
            str(available_bays),
            f'{random.randint(0, 45):02d}℃',
            time.strftime("%H:%M:%S")
        ]))
        self.window.update(field_values)

    def check_updates(self):
        client = mqtt.Client(client_id=MQTT_CLIENT_NAME)

        client.on_connect = self.on_connect
        client.on_message = self.on_message

        client.connect(MQTT_HOST, MQTT_PORT, MQTT_KEEP_ALIVE)

        client.loop_start()

        while True:
            temperature = int(random.gauss(24, 6))

            field_values = dict(zip(CarParkDisplay.fields, [
                str(self.data['total_spaces'] - self.data['total_cars']),
                f'{temperature:02d}°C',
                time.strftime("%H:%M:%S")
            ]))
            self.window.update(field_values)

            # Sleep for 10 seconds
            time.sleep(10)


if __name__ == '__main__':
    CarParkDisplay()
