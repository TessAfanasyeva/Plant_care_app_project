import unittest
from unittest.mock import Mock, patch
from datetime import date
from your_module import PlantWateringUpdater

class TestPlantWateringUpdater(unittest.TestCase):
    def setUp(self):
        self.plant_id = 1
        self.plant = Mock()
        self.sql_request = Mock()
        self.plant.update_needs_water = Mock()
        self.updater = PlantWateringUpdater(self.plant_id)
        self.updater.plant = self.plant
        self.updater.sql_request = self.sql_request

    def test_update_plant_watered_today(self):
        self.updater.last_watered = date.today()
        self.updater.calculate_next_watering_date = Mock(return_value=date.today() + timedelta(days=7))

        with patch("builtins.print") as mocked_print:
            self.updater.update_plant()

        mocked_print.assert_called_once_with("Watering your plant... Your plant was watered today.")
        self.sql_request.update_db.assert_called_once_with(date.today().strftime("%m-%d-%Y"))
        self.plant.notify_observers.assert_called_once_with(
            plant_id=self.plant_id,
            next_watering_date=date.today() + timedelta(days=7).strftime("%m-%d-%Y")
        )
        self.plant.update_needs_water.assert_called_once()

    def test_update_plant_next_watering_date_in_future(self):
        self.updater.last_watered = date.today() - timedelta(days=2)
        self.updater.calculate_next_watering_date = Mock(return_value=date.today() + timedelta(days=7))

        with patch("builtins.print") as mocked_print:
            self.updater.update_plant()

        mocked_print.assert_called_once_with(f"The next watering date for your plant is {date.today() + timedelta(days=7)}.")
        self.sql_request.update_db.assert_called_once_with((date.today() + timedelta(days=7)).strftime("%m-%d-%Y"))
        self.plant.notify_observers.assert_called_once_with(
            plant_id=self.plant_id,
            next_watering_date=date.today() + timedelta(days=7).strftime("%m-%d-%Y")
        )
        self.plant.update_needs_water.assert_called_once()

    def test_update_plant_next_watering_date_in_past(self):
        self.updater.last_watered = date.today() - timedelta(days=10)
        self.updater.calculate_next_watering_date = Mock(return_value=date.today() - timedelta(days=3))

        with patch("builtins.print") as mocked_print:
            self.updater.update_plant()

        mocked_print.assert_called_once_with(
            f"The watering date for your plant was {date.today() - timedelta(days=3)}. Watering your plant... "
            f"The next watering date is {date.today() - timedelta(days=3)}."
        )
        self.sql_request.update_db.assert_called_once_with((date.today() - timedelta(days=3)).strftime("%m-%d-%Y"))
        self.plant.notify_observers.assert_called_once_with(
            plant_id=self.plant_id,
            next_watering_date=date.today() - timedelta(days=3).strftime("%m-%d-%Y")
        )
        self.plant.update_needs_water.assert_called_once()

if __name__ == "__main__":
    unittest.main()

