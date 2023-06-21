import unittest
from unittest.mock import patch
from carpark import CarPark

class TestCarPark(unittest.TestCase):

    def setUp(self):
        self.patcher = patch('paho.mqtt.client.Client')
        self.mock_client_class = self.patcher.start()
        self.mock_client = self.mock_client_class.return_value
        self.mock_client.loop_start.return_value = None
        self.mock_client.loop_stop.return_value = None

        config = {
            'broker': {
                'broker': '127.0.0.1',
                'port': 1883,
                'topic-root': 'carpark',
                'topic-qualifier': 'controller',
                'name': 'parking-lot',
                'location': 'MOO',
                'sensor': 'sensor 1'
            },
            'MOO': {
                'name': 'Moondalup City Square Parking',
                'total_spaces': 192,
                'total_cars': 0
            },
            'sensor1': {
                'name': 'entry',
                'broker': '127.0.0.1',
                'port': 1883
            }
        }
        self.car_park = CarPark(config)

    def tearDown(self):
        # Stop the MQTT client patcher
        self.patcher.stop()

    def test_car_entry(self):
        self.car_park.total_spaces = 100
        self.car_park.total_cars = 90

        self.car_park.on_car_entry()

        self.assertEqual(self.car_park.total_cars, 91)
        self.assertEqual(self.car_park.total_spaces, 100)
        self.assertEqual(self.car_park.available_spaces, 9)
        print(self.car_park.available_spaces)

    def test_car_exit(self):
        self.car_park.total_spaces = 100
        self.car_park.total_cars = 70

        self.car_park.on_car_exit()

        self.assertEqual(self.car_park.total_cars, 69)
        self.assertEqual(self.car_park.total_spaces, 100)
        self.assertEqual(self.car_park.available_spaces, 31)
        print(self.car_park.available_spaces)

    def test_no_negative_spaces(self):
        self.car_park.total_spaces = 100
        self.car_park.total_cars = 100

        self.car_park.on_car_entry()

        self.assertEqual(self.car_park.total_cars, 100)
        self.assertEqual(self.car_park.total_spaces, 100)
        self.assertEqual(self.car_park.available_spaces, 0)

        self.car_park.on_car_exit()
        self.car_park.on_car_exit()

        self.assertEqual(self.car_park.total_cars, 98)
        self.assertEqual(self.car_park.total_spaces, 100)
        self.assertEqual(self.car_park.available_spaces, 2)
        print(self.car_park.available_spaces)

if __name__ == '__main__':
    unittest.main()





