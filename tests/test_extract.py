import unittest
import json
from backend.extract.extract import get_accidents, get_weather, format_date, get_weather_data

class TestExtractFunctions(unittest.TestCase):
    def test_get_accidents(self):
        response = get_accidents()
        response_dict = json.loads(response)
        
        self.assertEqual(response_dict['status_code'], 200)
        self.assertTrue(len(response_dict['message']) > 0)

    def test_get_weather(self):
        response = get_weather()
        response_dict = json.loads(response)
        
        self.assertEqual(response_dict['status_code'], 200)
        self.assertTrue(len(response_dict['message']) > 0)
    
    def test_format_date(self):
        date_str = "2023-01-01"
        formatted_date = format_date(date_str)
        
        self.assertEqual(formatted_date, "20230101")

    def test_get_weather_data(self):
        response = get_weather_data(2023, 12)
        
        self.assertTrue(len(response) > 0)