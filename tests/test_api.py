"""
Author: Kexin Chen
"""

import unittest
import requests


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
