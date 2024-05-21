"""
Author: Kexin Chen
"""

import unittest
import requests


class TestAPIEndpoints(unittest.TestCase):
    BASE_URL = "http://127.0.0.1:9090"

    def test_search_by_index(self):
        response = requests.get(f"{self.BASE_URL}/search")
        self.assertEqual(response.status_code, 200)

    def test_put(self):
        response = requests.put(f"{self.BASE_URL}/put", json={})
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
