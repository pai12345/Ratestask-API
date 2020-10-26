""" Module for Abstract Class: Prices.

    Module has semantic contract for Prices Class.
"""
from abc import ABC, abstractmethod


class ProtoPrices(ABC):
    """ Abstract Class for Prices Class

        Class contains the core implementation details, functionalities and informations for prices.
    """
    @abstractmethod
    def average_rates(self):
        """ Sematic contract for average_rates.

            Get average prices for each day on a route between port codes origin and destination.
        """
        pass

    @abstractmethod
    def generate_price_payload(self):
        """ Sematic contract for generate_price_payload.

            Generate payload containing details of required fields for price.
        """
        pass

    @abstractmethod
    def upload_price(self):
        """ Sematic contract for upload_price.

            Function to upload price.
        """
        pass

    @abstractmethod
    def get_price(self):
        """ Sematic contract for get_price.

            Function to fetch price in USD.
        """
        pass
