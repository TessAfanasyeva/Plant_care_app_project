"""
Module: main

This module contains the main logic of the plant watering reminder application. It prompts the user for their name, validates their email, checks if the plant exists in the database, retrieves information about the plant using GPT, prompts for watering status, and updates the plant's watering information.

Dependencies:
- datetime
- gpt_plant_info.get_fun_fact
- user_login_signup_handling.EmailValidator
- user_login_signup_handling.SignUp
- user_login_signup_handling.CheckExistenceOfPlants
- watering_logic.PlantWateringUpdater

Functions:
- get_current_user_name(): Prompts the user for their name and returns it.
- validate_email(current_user_name): Validates the email of the current user.
- check_plant_existence(current_user_name, plant_name): Checks if the provided plant exists for the current user in the database.
- gpt_information_getter(current_user_name, plant_name): Retrieves information about the plant using GPT.
- prompt_watering_status(): Prompts the user for the watering status of the plant.
- main(): Main function that orchestrates the flow of the application.

"""
import datetime

from gpt_plant_info import get_fun_fact
from user_login_signup_handling import EmailValidator, SignUp, CheckExistenceOfPlants
from watering_logic import PlantWateringUpdater


def get_current_user_name():
    """
    Prompts the user for their name and returns it.

    Returns:
        str: The name of the current user.
    """
    while True:
        current_user_name = input("Welcome! What is your name? ")
        current_user_name = current_user_name.strip()
        if current_user_name:
            return current_user_name
        else:
            print("Invalid input. Please enter your name.")


def validate_email(current_user_name):
    """
    Validates the email of the current user.

    Args:
        current_user_name (str): The name of the current user.

    Returns:
        None
    """
    email_check = EmailValidator(current_user_name)
    email, welcome_message = email_check.validate_email()
    if not email:
        new_sign_up = SignUp(current_user_name)
        new_sign_up.execute_query()


def check_plant_existence(current_user_name, plant_name):
    """
    Checks if the provided plant exists for the current user in the database.

    Args:
        current_user_name (str): The name of the current user.
        plant_name (str): The name of the plant.

    Returns:
        tuple: A tuple containing a boolean indicating if the plant exists and the plant ID. Promts user to register the plant.
    """
    does_plant_exist = CheckExistenceOfPlants(current_user_name, plant_name)
    plant_id = does_plant_exist.get_plant_id()

    if plant_id is None:
        user_input = input(
            "Unfortunately, you don't have this plant yet. Would you like to register it? (y/n) ").lower()
        if user_input not in ["y", "yes", "ye", "ya", 'okay']:
            return False, None
        else:
            does_plant_exist.register_plant()
            plant_id = does_plant_exist.get_plant_id()
    return True, plant_id


def gpt_information_getter(current_user_name, plant_name):
    """
    Retrieves information about the plant using GPT.

    Args:
        current_user_name (str): The name of the current user.
        plant_name (str): The name of the plant.

    Returns:
        str: The information about the plant generated by GPT.
    """
    print("GPT is generating information about your plant! Thank you for waiting... \n")
    does_plant_exist = CheckExistenceOfPlants(current_user_name, plant_name)
    try:
        plant_species = does_plant_exist.get_plant_species()
        gpt_information = get_fun_fact(plant_species)
        return gpt_information
    except Exception as e:
        print("Error retrieving gpt-written fun fact:", e)
        return None


def prompt_watering_status():
    """
    Prompts the user for the watering status of the plant.

    Returns:
        bool: True if the plant was watered today, False otherwise.
    """
    while True:
        did_you_water_today = input("Did you water your plant today? (y/n) ").lower()
        if did_you_water_today in ["y", "yes", "ye", "ya", 'okay']:
            return True
        elif did_you_water_today in ["n", "no"]:
            return False
        else:
            print("Invalid input. Please enter 'y' or 'n'.")


def main():
    """
    Main function that orchestrates the flow of the application.

    Returns:
        None
    """
    current_user_name = get_current_user_name()
    validate_email(current_user_name)

    while True:
        plant_name = input("What is the name of the plant you would like to log? ").lower().capitalize()
        exit_code, plant_id = check_plant_existence(current_user_name, plant_name)
        if not exit_code:
            break

        if plant_id is None:
            print(
                "We are using an unpaid version of the plant API for this exercise, and thus, our species list is limited."
                "We apologise for the inconvenience caused. Please, pick another plant species. "
                "May we suggest an orchid, an easy-to-grow friend that adds a tropical touch to your home? ")
        else:
            print(gpt_information_getter(current_user_name, plant_name))
            did_you_water_today = prompt_watering_status()
            if did_you_water_today:
                last_watered = datetime.date.today()
                my_plant = PlantWateringUpdater(plant_id=plant_id, last_watered=last_watered)
            else:
                while True:
                    last_watered = input("When did you last water your plant? (yyyy-mm-dd): ")
                    try:
                        last_watered = datetime.datetime.strptime(last_watered, '%Y-%m-%d').date()
                        my_plant = PlantWateringUpdater(plant_id=plant_id, last_watered=last_watered)
                        break
                    except ValueError:
                        print("Invalid date format. Please enter the date in yyyy-mm-dd format.")

            my_plant.update_plant()

            user_has_another_plant = input("Do you have another plant? (y/n) ")
            if user_has_another_plant.lower() not in ["y", "ye", "ya", "yes", "sure", "okay"]:
                break


if __name__ == "__main__":
    main()
