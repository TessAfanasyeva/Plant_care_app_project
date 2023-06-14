"""
Module: db_request_handling

This module provides a class for handling SQL data operations.

Classes:
- SQLDataHandler: Handles database connections and performs SQL operations.

Dependencies:
- mysql.connector: Module to connect to SQL database.

Exceptions:
- DBConnectionError: Custom exception raised when there is an error in the database connection.

"""
import mysql.connector

from config import PASSWORD, HOST, USER


class DBConnectionError(Exception):
    pass


class SQLDataHandler:
    """
    SQLDataHandler class handles database connections and performs SQL operations.

    Attributes:
    - db_name (str): Name of the database.
    - query (str): SQL query to be executed.

    Methods:
    - db_connect(): Establishes a database connection.
    - db_set_record(): Executes the SQL query for inserting records into the database.
    - db_get_record(): Executes the SQL query for fetching a single record from the database.

    """

    def __init__(self, db_name="thirst_trap", query=None):
        """
        Initializes an instance of the SQLDataHandler class.

        Args:
        - db_name (str): Name of the database. Default is 'thirst_trap'.
        - query (str): SQL query to be executed. Default is None.

        """
        self.db_name = db_name
        self.query = query

    def db_connect(self):
        """
        Establishes a database connection.

        Returns:
        - cnx (mysql.connector.connection_cext.CMySQLConnection): Database connection object.

        """
        cnx = mysql.connector.connect(
            host=HOST,
            user=USER,
            password=PASSWORD,
            auth_plugin="mysql_native_password",
            database=self.db_name
        )
        return cnx

    def db_set_record(self):
        """
        Executes the SQL query for inserting records into the database.

        Raises:
        - DBConnectionError: If there is an error in the database connection.

        """
        try:
            db_connection = self.db_connect()
            cur = db_connection.cursor()
            if self.query is None:
                print("DB: Query is not specified.")
                return None
            cur.execute(self.query)
            db_connection.commit()
            print("DB: Query is inserted.")
            cur.close()
        except Exception as e:
            raise DBConnectionError("Failed to read data from DB.", e)
        finally:
            if db_connection:
                db_connection.close()

    def db_get_record(self):
        """
        Executes the SQL query for fetching a single record from the database.

        Returns:
        - record (tuple): Single record fetched from the database.

        Raises:
        - DBConnectionError: If there is an error in the database connection.

        """
        try:
            db_connection = self.db_connect()
            cur = db_connection.cursor()
            if self.query is None:
                print("DB: Query is not specified.")
                return None
            cur.execute(self.query)
            record, = cur.fetchall()
            cur.close()
        except Exception as e:
            raise DBConnectionError("Failed to read data from DB.", e)
        finally:
            if db_connection:
                db_connection.close()
        return record
