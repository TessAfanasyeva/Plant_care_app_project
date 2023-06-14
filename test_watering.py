import unittest
from unittest import mock
from unittest.mock import MagicMock, patch
from datetime import date, timedelta
from your_module import calculate_next_watering_date

from watering_logic import *


class TestPlantStateObserver(unittest.TestCase):
    def test_init_with_wrong_type(self):
        plant = "not a plant"
        with self.assertRaises(TypeError):
            observer = PlantStateObserver(plant)

    def test_update_not_implemented(self):
        plant = MagicMock(spec=Plant)
        observer = PlantStateObserver(plant)
        with self.assertRaises(NotImplementedError):
            observer.update()


class TestPlantWateringObserver(unittest.TestCase):
    def setUp(self):
        self.fake_plant = MagicMock(spec=Plant)
        self.observer = PlantWateringObserver(self.fake_plant)

    def test_init(self):
        self.assertIsInstance(self.observer, Thread)
        self.assertIsInstance(self.observer, PlantStateObserver)
        self.assertEqual(self.observer.plant, self.fake_plant)

    def test_update(self):  # Need this one
        pass


class TestHousePlant(unittest.TestCase):
    def setUp(self):
        self.plant_name = "test plant"
        self.plant = HousePlant(self.plant_name)

    def test_init(self):
        self.assertEqual(self.plant.plant_name, self.plant_name)
        self.assertTrue(self.plant.needs_water)
        self.assertIsNone(self.plant.last_watered)
        self.assertEqual(self.plant._observers, [])

    def test_register_observer(self):
        observer = MagicMock(spec=PlantStateObserver)
        self.plant.register_observer(observer)
        self.assertIn(observer, self.plant._observers)

    def test_unregister_observer(self):
        observer = MagicMock(spec=PlantStateObserver)
        self.plant.register_observer(observer)
        self.plant.unregister_observer(observer)
        self.assertNotIn(observer, self.plant._observers)

    def test_notify_observers(self):
        observer1 = MagicMock(spec=PlantStateObserver)
        observer2 = MagicMock(spec=PlantStateObserver)
        self.plant.register_observer(observer1)
        self.plant.register_observer(observer2)
        self.plant.notify_observers()
        observer1.update.assert_called_once()
        observer2.update.assert_called_once()

    def test_update_needs_water(self):
        self.plant.notify_observers = MagicMock()
        self.plant.update_needs_water()
        self.assertFalse(self.plant.needs_water)
        self.plant.notify_observers.assert_called_once()

    def test_observer_type(self):
        self.assertIsInstance(self.observer, PlantStateObserver)

    def test_observer_update_method(self):
        with self.assertRaises(NotImplementedError):
            self.observer.update()

    def test_observer_plant_attribute(self):
        self.assertEqual(self.observer.plant, self.plant)

    def test_plant_type(self):
        self.assertIsInstance(self.plant, Plant)

    def test_plant_needs_water(self):
        self.assertTrue(self.plant.needs_water)

    def test_plant_last_watered(self):
        self.assertIsNone(self.plant.last_watered)

    def test_plant_register_observer(self):
        self.assertEqual(len(self.plant._observers), 1)

    def test_houseplant_type(self):
        houseplant = HousePlant("test_houseplant")
        self.assertIsInstance(houseplant, Plant)
        self.assertIsInstance(houseplant, HousePlant)


class PlantWateringUpdater(unittest.TestCase):
    def test_houseplant_update_needs_water(self):
        houseplant = HousePlant("test_houseplant")
        with mock.patch.object(houseplant, "notify_observers") as mock_notify:
            houseplant.update_needs_water()
            self.assertFalse(houseplant.needs_water)
            mock_notify.assert_called_once()

    def test_watering_updater_calculate_next_watering_date(
            self):  # cant mke this one to work TypeError: getattr(): attribute name must be string
        plant = HousePlant("test_houseplant")
        watering_updater = PlantWateringUpdater(plant)
        watering_frequency = datetime.timedelta(days=7)
        plant.last_watered = datetime.date.today() - watering_frequency
        with patch.object(SQLDataGetter, 'get_watering_frequency', return_value=watering_frequency):
            next_watering_date = watering_updater.calculate_next_watering_date()
        expected_next_watering_date = plant.last_watered + watering_frequency
        self.assertEqual(next_watering_date, expected_next_watering_date)

    def test_watering_updater_calculate_next_watering_date_no_frequency(
            self):  # cant mke this one to work TypeError: getattr(): attribute name must be string
        plant = HousePlant("test_houseplant")
        watering_updater = PlantWateringUpdater(plant)
        SQLDataGetter.get_watering_frequency = mock.MagicMock(return_value=None)
        next_watering_date = watering_updater.calculate_next_watering_date()
        self.assertIsNone(next_watering_date)

    def test_watering_updater_calculate_next_watering_date_no_last_watered(
            self):  # cant mke this one to work TypeError: getattr(): attribute name must be string
        plant = HousePlant("test_houseplant")
        watering_updater = PlantWateringUpdater(plant)
        SQLDataGetter.get_watering_frequency = mock.MagicMock(return_value=datetime.timedelta(days=7))
        next_watering_date = watering_updater.calculate_next_watering_date()
        self.assertIsNone(next_watering_date)
