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

    def test_search_by_index(self):
        for i in self.indexes:
            response = requests.get(f"{self.BASE_URL}/search/{i}")
            self.assertEqual(response.status_code, 200)

    def test_put(self):
        response = requests.put(f"{self.BASE_URL}/put/weather", json={})
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
