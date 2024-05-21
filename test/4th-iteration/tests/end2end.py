"""
Author: Kexin Chen
"""

import unittest
import requests
import json
from backend.extract.extract import (
    get_accidents,
    get_weather,
    format_date,
    get_weather_data,
)


class TestExtractFunctions(unittest.TestCase):
    def test_get_accidents(self):
        response = get_accidents()
        response_dict = json.loads(response)

        self.assertEqual(response_dict["status_code"], 200)
        self.assertTrue(len(response_dict["message"]) > 0)

    def test_get_weather(self):
        response = get_weather()
        response_dict = json.loads(response)

        self.assertEqual(response_dict["status_code"], 200)
        self.assertTrue(len(response_dict["message"]) > 0)

    def test_format_date(self):
        date_str = "2023-01-01"
        formatted_date = format_date(date_str)
        self.assertEqual(formatted_date, "20230101")

    def test_get_weather_data(self):
        response = get_weather_data(2023, 12)
        self.assertTrue(len(response) > 0)


class TestAPIEndpoints(unittest.TestCase):
    BASE_URL = "http://127.0.0.1:9090"
    indexes = [
        "weather",
        "accidents",
        "roadcondition",
        "population",
        "accident_locations",
        "geoinfo",
    ]

    def test_searchweather(self):
        """Test the searchweather function endpoint"""
        response = requests.get(f"{self.BASE_URL}/searchweather/20240301/20240311")
        self.assertEqual(response.status_code, 200)
        self.assertIn("response", response.json())
        
        response = requests.post(f"{self.BASE_URL}/searchweather/20240301/20240311")
        self.assertEqual(response.status_code, 400)

    def test_search_by_index(self):
        """Test the search function endpoint for a specific index"""
        for i in self.indexes:
            response = requests.get(f"{self.BASE_URL}/search/{i}")
            self.assertEqual(response.status_code, 200)
            self.assertIn("response", response.json())

    def test_put(self):
        """Test the put function endpoint"""
        action = [
            {
                "_index": "weather",
                "_id": "20240301",
                "_source": {
                    "Date": "20240301",
                    "Rainfall (mm)": "0.0",
                    "Maximum temperature (°C)": "19.8",
                    "Minimum temperature (°C)": "15.9",
                },
            }
        ]
        response = requests.put(f"{self.BASE_URL}/put/weather", json=action)
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
