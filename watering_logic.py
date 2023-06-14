"""
Module: Logic for calculation of the next watering date o the plant

This module provides classes for observing and managing the state of a plant.

Classes:
- PlantStateObserver: An abstract base class for objects that observe the state of a plant.
- PlanObserverNotifications: A class that observes a plant and sends email notifications with the next watering date.
- Plant: An abstract base class representing a plant.
- HousePlant: A subclass of Plant for a houseplant.
- PlantWateringUpdater: A class for updating and managing plant watering information.
- PlantDBConnection: Represents a connection to a thirst trap database.

Exceptions:
- DBConnectionError: Custom exception raised when there is an error in the database connection.
- TypeError: Raised when an invalid type is passed as an argument.

"""
import datetime
from abc import ABC, abstractmethod

import notifications
from db_request_handling import SQLDataHandler


class PlantStateObserver(ABC):
    """
    An abstract base class for objects that observe the state of a plant.

    Attributes:
        plant (Plant): The plant to be observed.

    Methods:
        update(): Abstract method to update the observer with the current state of the plant.
    """

    def __init__(self, plant):
        """
         Initializes a PlantStateObserver instance.

         Args:
             plant (Plant): The plant to be observed.

         Raises:
             TypeError: If the plant argument is not of type Plant.
         """
        if not isinstance(plant, Plant):
            raise TypeError("plant argument must be of type Plant")
        self.plant = plant
        self.plant.register_observer(self)

    @abstractmethod
    def update(self):
        """
             Abstract method to update the observer with the current state of the plant.
             Subclasses must implement this method.

        Raises:
            NotImplementedError: If the method is not implemented in a subclass.
        """
        raise NotImplementedError("This function has not been implemented yet.")
        pass


class PlanObserverNotifications(PlantStateObserver):
    """
    A class that observes a plant and call function that sends email notifications with the next watering date.

    Attributes:
        plant (Plant): The plant to be observed.

    Methods:
            def update(): Provides the next watering date in an email format and triggers email notification.
    """

    def __init__(self, plant, next_watering_date):
        super().__init__(plant)
        self.next_watering_date = next_watering_date

    def update(self, **kwargs):
        plant_id = kwargs.get('plant_id')
        next_watering_date = kwargs.get('next_watering_date')
        notifications.initiate_email(plant_id, next_watering_date)


class Plant(ABC):
    """
    Abstract base class representing a plant.

    Attributes:
        plant_id (int): The ID of the plant.
        needs_water (bool): Indicates if the plant needs watering.
        _observers (list): List of registered PlantStateObservers.

    Methods:
        __init__(plant_id): Initializes a Plant instance.
        update_needs_water(): Abstract method to update the needs_water attribute (to be implemented by subclasses).
        register_observer(observer): Registers a PlantStateObserver.
        unregister_observer(observer): Unregisters a PlantStateObserver.
        notify_observers(): Notifies all registered PlantStateObservers.
    """

    def __init__(self, plant_id):
        """
           Initializes a Plant instance.

           Args:
               plant_id (int): The ID of the plant.
        """
        self.plant_id = plant_id
        self.needs_water = True
        self._observers = []

    @abstractmethod
    def update_needs_water(self):
        """
        Abstract method to update the needs_water attribute.
            Subclasses must implement this method.

        Raises:
            NotImplementedError: If the method is not implemented in a subclass.
        """
        raise NotImplementedError("This function has not been implemented yet.")
        pass

    def register_observer(self, observer: PlantStateObserver):
        """
        Registers a PlantStateObserver.

        Args:
            observer (PlantStateObserver): The observer to register.
        """
        print("Plant: Appending PlantStateObservers... ")
        self._observers.append(observer)

    def unregister_observer(self, observer: PlantStateObserver):
        """
        Unregisters a PlantStateObserver.

        Args:
            observer (PlantStateObserver): The observer to unregister.
        """
        print("Plant: Removing PlantStateObservers... ")
        self._observers.remove(observer)

    def notify_observers(self, **kwargs):
        print("Plant: Notifying PlantStateObservers... ")
        for observer in self._observers:
            observer.update(**kwargs)


class HousePlant(Plant):
    """
    Subclass of Plant for a house plant.

    Attributes:
        See Plant class.

    Methods:
        update_needs_water(): Updates the needs_water attribute.
    """

    def update_needs_water(self):
        """
        This method toggles the value of the needs_water attribute, indicating whether the plant needs water or not.

        Raises:
            None
        """
        print("Plant: Updating status... ")
        self.needs_water = not self.needs_water


class PlantWateringUpdater:
    """
    Class for updating and managing plant watering information.

    Attributes:
        plant (HousePlant): The plant instance to update.
        sql_request (PlantDBConnection): The database connection for plant-related queries.
        watering_frequency (int): The watering frequency in days.
        next_watering_date (datetime.datetime): The next watering date for the plant.
        last_watered (str): The last watered date in string format.

    Methods:
        __init__(plant_id, last_watered=None): Initializes a PlantWateringUpdater instance.
        calculate_next_watering_date(): Calculates the next date the plant needs to be watered.
        update_plant(): Updates the plant's watering needs and provides a message about the next watering date.
    """

    def __init__(self, plant_id, last_watered=None):
        """
              Initializes a PlantWateringUpdater instance.

              Args:
                  plant_id (int): The ID of the plant.
                  last_watered (str): Optional. The last watered date in string format. Defaults to None.
              """
        self.plant = HousePlant(plant_id)
        self.sql_request = PlantDBConnection(self.plant)
        self.watering_frequency = None
        self.next_watering_date = None
        self.last_watered = last_watered

    def calculate_next_watering_date(self):
        """
             Calculates the next date the plant needs to be watered.

             Returns:
                 datetime.datetime or None: The next date the plant needs to be watered, or None if the frequency is not set
                 or the last watering date is not set.
             """
        self.watering_frequency = datetime.timedelta(days=self.sql_request.get_watering_frequency())
        if self.watering_frequency is None:
            print("Watering frequency is not set.")
            return None

        if self.last_watered is None:
            last_watered_str = self.sql_request.get_last_watered()
            if last_watered_str == datetime.date.today().strftime("%m-%d-%Y"):
                self.last_watered = datetime.date.today()
            else:
                self.last_watered = datetime.datetime.strptime(last_watered_str, "%m-%d-%Y").date()
        if self.last_watered is None:
            print("Last watering date is not set.")
            return None

        self.next_watering_date = self.last_watered + self.watering_frequency
        return self.next_watering_date

    def update_plant(self):
        """
            Updates the plant's watering needs, provides a message notifying about the next watering date, and triggers email sending.

            Returns:
                None
            """
        self.next_watering_date = self.calculate_next_watering_date()
        today = datetime.date.today()

        if self.last_watered == today:
            print(f"Watering your plant... You plant was watered today.")
        elif self.next_watering_date > today:
            print(f"The next watering date for your plant is {self.next_watering_date}.")
        else:
            print(
                f"The watering date for your plant was {self.next_watering_date}. Watering your plant... "
                f"The next watering date is {self.next_watering_date}.")

        self.next_watering_date = self.next_watering_date.strftime("%m-%d-%Y")
        self.sql_request.update_db(self.next_watering_date)
        email_observer = PlanObserverNotifications(self.plant, self.next_watering_date)
        self.plant.notify_observers(plant_id=self.plant.plant_id, next_watering_date=self.next_watering_date)
        return self.plant.update_needs_water()


class PlantDBConnection:
    """
    Represents a connection to a thirst trap database.

    Attributes:
    - next_watering_date (str): The date of the next watering.
    - last_watered (str): The date when the plant was last watered.
    - watering_frequency (int): The frequency at which the plant should be watered.
    - plant_id (int): The unique identifier of the plant.
    - sql_request (SQLDataHandler): An instance of the SQLDataHandler class for executing SQL queries.
    """

    def __init__(self, plant):
        self.next_watering_date = None
        self.last_watered = None
        self.watering_frequency = None
        self.plant = plant
        self.sql_request = SQLDataHandler()

    def get_watering_frequency(self):
        """
        Retrieves the watering frequency for the plant from the database.

        Returns:
            int: The watering frequency in days.
        """
        print("PlantDBConnection: Retrieving watering frequency... ")
        self.sql_request.query = f"SELECT watering_frequency FROM user_plants WHERE plant_id = '{self.plant.plant_id}';"
        self.watering_frequency, = self.sql_request.db_get_record()
        return self.watering_frequency

    def get_last_watered(self):
        """
         Retrieves the last watered date for the plant from the database.

         Returns:
             str: The last watered date in string format.
         """
        print("PlantDBConnection: Retrieving last watered date... ")
        self.sql_request.query = f"SELECT date_last_watered FROM user_plants WHERE plant_id = '{self.plant.plant_id}';"
        self.last_watered, = self.sql_request.db_get_record()
        print(self.last_watered)
        return self.last_watered

    def update_db(self, next_watering_date):
        """
        Updates the database with the next watering date for the plant.

        Args:
            next_watering_date (str): The next watering date in string format.

        Returns:
            None
        """
        print("PlantDBConnection: Updating next watered date... ")
        self.sql_request.query = f" UPDATE user_plants SET date_last_watered = '{next_watering_date}' WHERE plant_id = '{self.plant.plant_id}';"
        self.sql_request.db_set_record()
