import unittest
from unittest.mock import patch
from datetime import timedelta
from app import app, get_plant_data, get_watering_frequency

class FlaskAppTests(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_index(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<h1>Welcome to the API Test</h1>', response.data)

    @patch('requests.get')
    def test_get_plant_data_with_direct_match(self, mock_get):
        mock_response = {
            "data": [
                {
                    "common_name": "Rose",
                    "scientific_name": ["Rosa"],
                    "other_name": None,
                    "watering": "Frequent"
                }
            ]
        }
        mock_get.return_value.json.return_value = mock_response
        plant_data = get_plant_data("Rose")
        self.assertEqual(plant_data["common_name"], "Rose")
        self.assertEqual(plant_data["watering"], "Frequent")

    @patch('requests.get')
    def test_get_plant_data_with_close_matches(self, mock_get):
        mock_response = {
            "data": [
                {
                    "common_name": "Sunflower",
                    "scientific_name": ["Helianthus"],
                    "other_name": None,
                    "watering": "Average"
                },
                {
                    "common_name": "Rose",
                    "scientific_name": ["Rosa"],
                    "other_name": None,
                    "watering": "Frequent"
                }
            ]
        }
        mock_get.return_value.json.return_value = mock_response
        plant_data = get_plant_data("Sunflwr")
        self.assertIsInstance(plant_data, list)
        self.assertEqual(len(plant_data), 1)
        self.assertEqual(plant_data[0]["common_name"], "Sunflower")
        self.assertEqual(plant_data[0]["original_name"], "Sunflwr")
        self.assertEqual(plant_data[0]["watering"], "Average")

    def test_get_watering_frequency(self):
        self.assertEqual(get_watering_frequency("Frequent"), 2)
        self.assertEqual(get_watering_frequency("Average"), 7)
        self.assertEqual(get_watering_frequency("Minimum"), 28)
        self.assertEqual(get_watering_frequency("None"), "never")
        self.assertEqual(get_watering_frequency("Unknown"), "unknown")
        
    def test_get_plant_data_with_no_match(self):
        plant_name = "InvalidPlant"
        response = self.app.get(f'/result?plant_name={plant_name}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'No plant details found', response.data)
        self.assertNotIn(b'Plant Name:', response.data)
        self.assertNotIn(b'Watering Frequency:', response.data)

    def test_get_plant_data_missing_parameter(self):
        response = self.app.get('/result')
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Missing parameter', response.data)

if __name__ == '__main__':
    unittest.main()
