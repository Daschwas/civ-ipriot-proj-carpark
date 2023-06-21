import toml
import mqtt_device
import time


class Display(mqtt_device.MqttDevice):
    """Displays the number of cars and the temperature"""

    def __init__(self, config):
        super().__init__(config['broker'])
        self.client.on_message = self.on_message
        self.client.subscribe('display')
        self.client.loop_forever()

    def display(self, *args):
        print('*' * 20)
        for val in args:
            print(val)
            time.sleep(1)

        print('*' * 20)

    def on_message(self, client, userdata, msg):
        data = msg.payload.decode()
        self.display(*data.split(','))
        available_spaces, temperature, time = data.split(',')
        self.display(available_spaces, temperature, time)


if __name__ == '__main__':
    config_file = 'config.toml'
    with open(config_file, 'r+') as file:
        config = toml.load(file)
    print("Config file read!")

    display = Display(config)
