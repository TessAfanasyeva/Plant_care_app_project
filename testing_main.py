import unittest
from datetime import datetime, timedelta
from io import StringIO
from unittest.mock import patch, MagicMock
from main import (
    get_current_user_name,
    validate_email,
    check_plant_existence,
    gpt_information_getter,
    prompt_watering_status,
    main
)

class TestMainFunction(unittest.TestCase):
    @patch('main.get_current_user_name', return_value='lezlee_lowpez')
    @patch('main.validate_email')
    @patch('main.check_plant_existence', side_effect=[(True, 2), (False, None)])
    @patch('main.prompt_watering_status', return_value=True)
    @patch('main.PlantWateringUpdater')
    @patch('builtins.input', side_effect=['ginger lily', 'y', 'n'])
    def test_main_flow(self, mock_input, mock_plant_updater, mock_watering_status,
                       mock_check_plant_existence, mock_validate_email, mock_get_current_user_name):
        expected_output = "Welcome! What is your name? \n" \
                          "What is the name of the plant you would like to log? \n" \
                          "Do you have another plant? (y/n) \n"

        with patch('sys.stdout', new=StringIO()) as fake_output:
            main()

        mock_get_current_user_name.assert_called_once()
        mock_validate_email.assert_called_once_with('lezlee_lowpez')
        mock_check_plant_existence.assert_any_call('lezlee_lowpez', 'ginger lily')
        mock_check_plant_existence.assert_any_call('lezlee_lowpez', 'Orchid')
        mock_watering_status.assert_called_once()
        mock_plant_updater.assert_called_once_with(plant_id=2, last_watered='04-01-2023')

        self.assertEqual(fake_output.getvalue(), expected_output)

    def test_get_current_user_name(self):
        with patch('builtins.input', side_effect=["", "lezlee_lowpez"]):
            result = get_current_user_name()
            self.assertEqual(result, "lezlee_lowpez")

    @patch('user_login_signup_handling.SignUp.execute_query')
    def test_validate_email(self, mock_execute_query):
        validate_email("lezlee_lowpez")
        mock_execute_query.assert_called_once()

    @patch('user_login_signup_handling.CheckExistenceOfPlants.get_plant_id')
    def test_check_plant_existence(self, mock_get_plant_id):
        mock_check_existence = MagicMock()
        mock_check_existence.register_plant = MagicMock()
        mock_check_existence.get_plant_species.return_value = 'Ginger Lily'
        mock_get_plant_id.return_value = None

        with patch('builtins.input', return_value='y'):
            result = check_plant_existence('lezlee_lowpez', 'ginger lily')
            self.assertEqual(result, (True, mock_get_plant_id.return_value))
            mock_check_existence.register_plant.assert_called_once()

        with patch('builtins.input', return_value='n'):
            result = check_plant_existence('lezlee_lowpez', 'ginger lily')
            self.assertEqual(result, (False, None))

    @patch('builtins.input', side_effect=['y', 'n'])
    def test_prompt_watering_status(self, mock_input):
        result = prompt_watering_status()
        self.assertTrue(result)

        result = prompt_watering_status()
        self.assertFalse(result)

if __name__ == "__main__":
    unittest.main()
