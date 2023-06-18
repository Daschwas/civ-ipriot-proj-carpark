""""Demonstrates a simple implementation of an 'event' listener that triggers
a publication via mqtt"""
import random

import toml

import mqtt_device


class Sensor(mqtt_device.MqttDevice):
    # TODO consider adding def__init__ into this class
    @property
    def temperature(self):
        """Returns the current temperature"""
        return random.randint(10, 35) 

    def on_detection(self, message):
        """Triggered when a detection occurs"""
        self.client.publish('sensor', message)

    def start_sensing(self):
        """ A blocking event loop that waits for detection events, in this
        case Enter presses"""
        while True:
            print("Press E when 🚗 entered!")
            print("Press X when 🚖 exited!")
            detection = input("E or X> ").upper()
            if detection == 'E':
                self.on_detection(f"entered, {self.temperature}")
            else:
                self.on_detection(f"exited, {self.temperature}")


if __name__ == '__main__':
    from config_parser import parse_config
    config1 = parse_config("config.toml")
    # consider moving MOO to a moo.toml and have above call that instead of config
    sensor1 = Sensor(config1)


    print("Sensor initialized")
    sensor1.start_sensing()

    sensor1.start_sensing()

