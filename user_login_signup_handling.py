"""
Module Name: user_login_signup_handling
Description: This module provides classes for handling user data and plant data.

Classes:
- UserDataHandler: Abstract base class for handling user data.
- EmailValidator: Class for validating user email.
- SignUp: Class for signing up a new user.
- PlantDataHandler: Abstract base class for handling plant data.
- CheckExistenceOfPlants: Class for checking the existence of plants for a user.
- RegisterPlant: Class for registering a new plant for a user.

Dependencies:
- datetime: Module for working with dates and times.
- re: Module for regular expressions.
- abc: Module for abstract base classes.
- db_request_handling: Module for handling database requests.
- flask_app.app: Module for accessing plant data and watering frequency.

Exceptions:
- NotImplementedError: Exception raised when the abstract method called before implementation
- Exception: Exception raised when there is an error in fetching or writing queries into the database.
"""
import datetime
import re
from abc import ABC, abstractmethod

from db_request_handling import SQLDataHandler
from flask_app.app import get_plant_data, get_watering_frequency


class UserDataHandler(ABC):
    """
    Abstract base class for handling user data.

    Attributes:
    - current_user_name (str): The current user's name.
    - sql_request (SQLDataHandler): Instance of the SQLDataHandler class for handling SQL queries.

    Methods:
    - execute_query(): Abstract method for executing a query.
    """

    def __init__(self, current_user_name):
        """
        Initialize UserDataHandler.

        Args:
            current_user_name (str): The current user's name.
        """
        self.user = current_user_name
        self.sql_request = SQLDataHandler()

    @abstractmethod
    def execute_query(self):
        """
        Execute a query.

        Raises:
            NotImplementedError: This function has not been implemented yet.
        """
        raise NotImplementedError("This function has not been implemented yet.")
        pass


class EmailValidator(UserDataHandler):
    """
    Class for validating user email.

    Methods:
    - execute_query(): Execute a query to retrieve the user's email.
    - validate_email(): Validate the user's email.
    """

    def execute_query(self):
        """
        Execute a query to retrieve the user's email.

        Returns:
            tuple: A tuple containing the user's email and a success message.

        Raises:
            DBRequestError: Error retrieving email.

        Returns:
            tuple or None: A tuple containing the user's email or None.

         Raises:
             NotImplementedError: This function has not been implemented yet.
         """
        self.sql_request.query = f"SELECT email FROM user_credentials WHERE username = '{self.user}'"
        return self.sql_request.db_get_record()

    def validate_email(self):
        """
          Validate the user's email.

          Returns:
              tuple or None: A tuple containing the user's email and a success message,
                             or None with an error message.
          """
        try:
            email, = self.execute_query()
            return email, "Username accepted."
        except Exception as e:
            # print('Error retrieving email:', e)
            return None, "We don't recognize you 0.0"


class SignUp(UserDataHandler):
    """
    Class for signing up a new user.

    Inherits UserDataHandler class.

    Methods:
    - execute_query(): Execute a query to insert user credentials into the database.
    """

    def execute_query(self):
        """
        Execute a query to insert user credentials into the database.

        Prompts the user to provide an email and validates it.

        Raises:
            NotImplementedError: This function has not been implemented yet.
        """
        email = input("You seem to be new here. Please provide you email to sign up: ")

        while True:
            if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                print("Please provide a valid email address: ")
            else:
                break

        insert_query = f"INSERT INTO user_credentials (username, email) VALUES ('{self.user}', '{email}');"
        self.sql_request.query = insert_query
        self.sql_request.db_set_record()


class PlantDataHandler(ABC):
    """
    Abstract base class for handling plant data.

    Attributes:
    - current_user_name (str): The current user's name.
    - sql_request (SQLDataHandler): Instance of the SQLDataHandler class for handling SQL queries.

    Methods:
    - execute_query(): Abstract method for executing a query.
    """

    def __init__(self, current_user_name):
        """
        Initialize PlantDataHandler.

        Args:
            current_user_name (str): The current user's name.
        """
        self.user = current_user_name
        self.sql_request = SQLDataHandler()

    @abstractmethod
    def execute_query(self):
        """
         Execute a query.

         Raises:
             NotImplementedError: This function has not been implemented yet.
         """
        raise NotImplementedError("This function has not been implemented yet.")
        pass


class CheckExistenceOfPlants(PlantDataHandler):
    """
    Class for checking the existence of plants for a user.

    Attributes:
    - current_user_name (str): The current user's name.
    - plant_name (str): The name of the plant to check.
    - registered_plant (RegisterPlant): Instance of the RegisterPlant class for registering a new plant.
    - plant_count (int): The count of plants for the user.
    - plant_name_user_input (str): The user-input plant name.

    Methods:
    - execute_query(): Executes a database query to check the existence of plants for the user.
    - register_plant(): Registers a new plant for the user.
    - get_plant_id(): Retrieves the ID of the plant for the user.
    - get_plant_species(): Retrieves the species of the plant for the user.
    """

    def __init__(self, current_user_name, plant_name):
        """
            Initialize CheckExistenceOfPlants.

            Args:
                current_user_name (str): The current user's name.
                plant_name (str): The name of the plant to check.
            """
        super().__init__(current_user_name)
        self.plant_name = plant_name
        self.registered_plant = None
        self.plant_count = None
        self.plant_name_user_input = None

    def execute_query(self):
        """
            Executes a database query to check the existence of plants for the user.

            Returns:
            - record (tuple): Single record fetched from the database.

            """
        self.sql_request.query = f"SELECT plant_id FROM user_credentials uc JOIN user_plants up ON uc.user_id = up.user_id WHERE username = '{self.user}';"
        return self.sql_request.db_get_record()

    def register_plant(self):
        """
        Registers a new plant for the user.

        Returns:
        - None in case of failure to register a plant.

        """
        self.registered_plant = RegisterPlant(self.user, self.plant_name)

        try:
            self.registered_plant.execute_query()
            print("Successfully registered your plant!")
        except Exception as e:
            print("Error registering your plant:", e)
            return None

    def get_plant_id(self):
        """
        Retrieves the ID of the plant for the user.

        Returns:
        - plant_id (int): The ID of the plant.

        """
        try:
            self.sql_request.query = f"SELECT up.plant_id FROM user_credentials uc JOIN user_plants up ON uc.user_id = up.user_id WHERE uc.username = '{self.user}' AND up.plant_nickname = '{self.plant_name}';"
            plant_id, = self.sql_request.db_get_record()
            return plant_id
        except Exception as e:
            # print("Error retrieving plant_id:", e)
            return None

    def get_plant_species(self):
        """
        Retrieves the species of the plant for the user.

        Returns:
        - plant_species (str): The species of the plant.

        """
        try:
            self.sql_request.query = f"SELECT up.plant_type FROM user_credentials uc JOIN user_plants up ON uc.user_id = up.user_id WHERE uc.username = '{self.user}' AND up.plant_nickname = '{self.plant_name}';"
            plant_species, = self.sql_request.db_get_record()
            return plant_species
        except Exception as e:
            # print("Error retrieving plant_species:", e)
            return None


class RegisterPlant(PlantDataHandler):
    """
      Class for registering a new plant for a user.

      Attributes:
      - current_user_name (str): The current user's name.
      - plant_name (str): The name of the plant to register.
      - user_id (None): Placeholder for storing the user ID (to be retrieved from the database).
      - date_last_watered (None): Placeholder for storing the date of the last watering (to be set as today's date).
      - watering_frequency (None): Placeholder for storing the watering frequency of the plant.
      - new_plant_species (None): Placeholder for storing the species of the new plant.

      Methods:
      - get_frequency(): Retrieves the watering frequency of the plant from user input and external plant data.
      - execute_query(): Executes a database query to register the new plant for the user.

      """

    def __init__(self, current_user_name, plant_name):
        """
        Initialize RegisterPlant.

        Args:
        - current_user_name (str): The current user's name.
        - plant_name (str): The name of the plant to register.

        """
        super().__init__(current_user_name)
        self.plant = plant_name
        self.user_id = None
        self.date_last_watered = None
        self.watering_frequency = None
        self.new_plant_species = None

    def get_frequency(self):
        """
        Retrieves the watering frequency of the plant from user input and external plant data.

        Returns:
        - frequency_description (str): The description of the watering frequency.

        """
        self.new_plant_species = input("What is your plant's species?")
        plant_data = get_plant_data(self.new_plant_species)

        if plant_data is not None and not isinstance(plant_data, list):
            plant_name = plant_data["common_name"]
            watering_frequency = plant_data["watering"]
            frequency_description = get_watering_frequency(watering_frequency)
            print(f"The watering frequency of {plant_name} is: {frequency_description}")
            return frequency_description
        else:
            print("No plant details found for the provided name.")
            return None

    def execute_query(self):
        """
           Executes a database query to register the new plant for the user.

           Returns:
           - None

           """
        self.watering_frequency = self.get_frequency()

        try:
            self.user_id = self.sql_request.query = f"SELECT user_id FROM user_credentials WHERE username = '{self.user}';"
            self.user_id, = self.sql_request.db_get_record()
        except Exception as e:
            # print("Error retrieving user_id:", e)
            return None

        self.date_last_watered = datetime.date.today()
        try:
            self.sql_request.query = f"INSERT INTO user_plants (plant_type, plant_nickname, user_id, watering_frequency, " \
                                     f"date_last_watered) VALUES ('{self.new_plant_species}', '{self.plant}', '{self.user_id}', " \
                                     f"'{self.watering_frequency}', '{self.date_last_watered}');"
            self.sql_request.db_set_record()
        except Exception as e:
            print("Error writing your plant information into the database:", e)
            return None
