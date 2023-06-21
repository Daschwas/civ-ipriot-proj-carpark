import unittest
from config_parser import parse_config


class TestConfigParsing(unittest.TestCase):
    def test_parse_config_has_correct_location_and_spaces(self):
        test_config = parse_config("config.toml")
        self.assertEqual(test_config['MOO']['name'], "Moondalup City Square Parking")
        self.assertEqual(test_config['MOO']['total_spaces'], 192)
