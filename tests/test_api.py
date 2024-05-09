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

    def test_getweather(self):
        """Test the getweather function endpoint"""
        response = requests.get(f"{self.BASE_URL}/getweather")
        self.assertEqual(response.status_code, 200)
        self.assertIn("count", response.json())

    def test_searchweather(self):
        """Test the searchweather function endpoint"""
        response = requests.get(f"{self.BASE_URL}/searchweather/20240301/20240311")
        self.assertEqual(response.status_code, 200)
        self.assertIn("data", response.json())

    def test_getaccidents(self):
        """Test the getaccidents function endpoint"""
        response = requests.get(f"{self.BASE_URL}/getaccidents")
        self.assertEqual(response.status_code, 200)
        self.assertIn("accidents", response.json())

    def test_storeweather(self):
        """Test the storeweather function endpoint"""
        # Assuming POST method is used and it requires some data
        data = {"temperature": 22, "date": "20240301"}
        response = requests.post(f"{self.BASE_URL}/storeweather", json=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("status", response.json())

    def test_getlocations(self):
        """Test the getlocations function endpoint"""
        response = requests.get(f"{self.BASE_URL}/getlocations")
        self.assertEqual(response.status_code, 200)
        self.assertIn("locations", response.json())

    def test_getroadcondition(self):
        """Test the getroadcondition function endpoint"""
        response = requests.get(f"{self.BASE_URL}/getroadcondition")
        self.assertEqual(response.status_code, 200)
        self.assertIn("condition", response.json())

    def test_search_by_index(self):
        """Test the search function endpoint for a specific index"""
        for i in self.indexes:
            response = requests.get(f"{self.BASE_URL}/search/{i}")
            self.assertEqual(response.status_code, 200)
            self.assertIn("response", response.json())


if __name__ == "__main__":
    unittest.main()
