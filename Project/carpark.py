from datetime import datetime
import random

import mqtt_device
from paho.mqtt.client import MQTTMessage


class CarPark(mqtt_device.MqttDevice):
    """Creates a carpark object to store the state of cars in the lot"""

    def __init__(self, config):
        super().__init__(config['broker'])
        carpark_name = config['broker']['location']
        print(f" Carpark at {carpark_name} is ready")
        self.total_spaces = int(config['MOO']['total_spaces'])
        self.total_cars = int(config['MOO']['total_cars'])
        self.client.on_message = self.on_message
        self.client.subscribe('car/sensor')
        self.client.loop_forever()

    @property
    def available_spaces(self):
        available = self.total_spaces - self.total_cars
        if available > self.total_spaces:
            available = self.total_spaces
        elif self.total_cars > self.total_spaces:
            available = 0
        return available

    def temperature(self):
        mean = 24
        std_dev = 6
        temperature = int(random.gauss(mean, std_dev))
        return temperature

    def _publish_event(self):
        readable_time = datetime.now().strftime('%H:%M:%S')
        available_spaces = self.available_spaces
        temperature = self.temperature()
        print(f"TIME: {readable_time}, " +
              f"SPACES: {available_spaces}, " +
              f"TEMP: {temperature}")
        message = (f"TIME: {readable_time}, " +
                   f"SPACES: {available_spaces}, " +
                   f"TEMP: {temperature}")
        self.client.publish('display', message)

    def on_car_entry(self):
        self.total_cars += 1
        self._publish_event()

    def on_car_exit(self):
        self.total_cars -= 1
        self._publish_event()

    def on_message(self, client, userdata, msg: MQTTMessage):
        payload = msg.payload.decode()
        if 'exit' in payload:
            print("exit payload received")
            self.on_car_exit()
        else:
            print("entry payload received")
            self.on_car_entry()


if __name__ == '__main__':
    from config_parser import parse_config

    config = parse_config("config.toml")
    CarPark(config)
    print("Carpark initialized")
