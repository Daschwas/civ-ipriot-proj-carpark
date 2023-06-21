""""Demonstrates a simple implementation of an 'event' listener that triggers
a publication via mqtt"""
import random
from config_parser import parse_config
import mqtt_device


class Sensor(mqtt_device.MqttDevice):
    def __init__(self, config):
        super().__init__(config['broker'])
        sensor_name = config['broker']['sensor']
        print(f"Sensor {sensor_name} is ready")

    @property #consider removing
    def temperature(self):
        """Returns the current temperature"""
        return random.randint(10, 35) 

    def on_detection(self, message):
        """Triggered when a detection occurs"""
        self.client.publish('car/sensor', message)

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
    sensor_config = parse_config('config.toml')
    sensor1 = Sensor(sensor_config)

    print("Sensor Name:", sensor1)
    print("Sensor initialized")
    sensor1.start_sensing()
