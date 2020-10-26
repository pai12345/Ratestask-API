""" Module for Abstract Class: Helper.

    Module has semantic contract for Helper Class.
"""
from abc import ABC, abstractmethod


class ProtoHelper(ABC):
    """ Abstract Class for Helper Class

        Class contains the core implementation details, functionalities and informations for assisting classes and methods.
    """
    @abstractmethod
    def get_url(self):
        """Semantic contract for get_url.

           Function for fetching URL for database or openexchangerates API.
        """
        pass

    @abstractmethod
    def create_connection_pool(self):
        """Semantic contract for create_connection_pool.

           Function for creating database connection pool.
        """
        pass

    @abstractmethod
    def close_connection_pool(self):
        """Semantic contract for close_connection_pool.

           Function for closing existing database connection pool.
        """
        pass

    @abstractmethod
    def get_connection_object(self):
        """Semantic contract for get_connection_object.

           Function for fetching connection from pool.
        """
        pass

    @abstractmethod
    def release_connection_object(self):
        """Semantic contract for release_connection_object.

           Function for releasing existing connection from pool.
        """
        pass

    @abstractmethod
    def create_connection_cursor(self):
        """Semantic contract for create_connection_cursor.

           Function for creating new cursor object.
        """
        pass

    @abstractmethod
    def close_connection_cursor(self):
        """Semantic contract for close_connection_cursor.

           Function for closing existing cursor object.
        """
        pass

    @abstractmethod
    def generate_query_recursion(self):
        """Semantic contract for generate_query_recursion.

           Function for generating query for recursion.
        """
        pass

    @abstractmethod
    def generate_query_rates(self):
        """Semantic contract for generate_query_rates.

           Function for generating query returning a list with the average prices for each day on a route between port codes origin and destination.
        """
        pass

    @abstractmethod
    def generate_query_ratesnull(self):
        """Semantic contract for generate_query_ratesnull.

           Function for generating query for returning an empty value(JSON null) for days on which there are less than 3 prices in total.
        """
        pass

    @abstractmethod
    def generate_query_portcheck(self):
        """Semantic contract for generate_query_portcheck.

           Function for generating query for port check.
        """
        pass

    @abstractmethod
    def generate_query_uploadprice(self):
        """Semantic contract for generate_query_uploadprice.

           Function for generating query on upload price.
        """
        pass

    @abstractmethod
    def get_date_range(self):
        """Semantic contract for get_date_range.

           Function for fetching date range.
        """
        pass

    @abstractmethod
    def connvert_to_USD(self):
        """Semantic contract for connvert_to_USD.

           Function for converting existing currency type to USD.
        """
        pass

    @abstractmethod
    def validate_params(self):
        """Semantic contract for validate_params.

           Function for validateing request url parameters and request payload.
        """
        pass

    @abstractmethod
    def validate_equality_check(self):
        """Semantic contract for validate_equality_check.

           Function for checking equality for origin and destination.
        """
        pass

    @abstractmethod
    def validate_ports_types(self):
        """Semantic contract for validate_ports_types.

           Function for checking equality for origin and destination.
        """
        pass

    @abstractmethod
    def precheck_parameters(self):
        """Semantic contract for precheck_parameters.

           Function for pre-checking all payload parameters.
        """
        pass

    @abstractmethod
    def check_sqlinjection(self):
        """Semantic contract for check_sqlinjection.

           Function for checking all parameters for sql injection.
        """
        pass
