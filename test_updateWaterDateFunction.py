import unittest
from datetime import date, timedelta
from your_module import calculate_next_watering_date

class TestCalculateNextWateringDate(unittest.TestCase):
    def test_next_watering_date_exists(self):
        # Plant with valid last_watered date and watering frequency
        plant1 = {
            "last_watered": date(2023, 1, 29),
            "watering_frequency": 7
        }
        expected1 = date(2023, 2, 5)
        result1 = calculate_next_watering_date(plant1)
        self.assertEqual(result1, expected1)

        # Plant with last_watered date set to today and watering frequency
        plant2 = {
            "last_watered": date.today(),
            "watering_frequency": 7
        }
        expected2 = date.today() + timedelta(days=7)
        result2 = calculate_next_watering_date(plant2)
        self.assertEqual(result2, expected2)

    def test_next_watering_date_not_set(self):
        # Plant with watering frequency set, but last_watered date not set
        plant3 = {
            "last_watered": None,
            "watering_frequency": 7
        }
        expected3 = None
        result3 = calculate_next_watering_date(plant3)
        self.assertEqual(result3, expected3)

        # Plant with last_watered date set, but watering frequency not set
        plant4 = {
            "last_watered": date(2023, 1, 29),
            "watering_frequency": None
        }
        expected4 = None
        result4 = calculate_next_watering_date(plant4)
        self.assertEqual(result4, expected4)

        # Plant with both last_watered date and watering frequency not set
        plant5 = {
            "last_watered": None,
            "watering_frequency": None
        }
        expected5 = None
        result5 = calculate_next_watering_date(plant5)
        self.assertEqual(result5, expected5)

if __name__ == "__main__":
    unittest.main()
