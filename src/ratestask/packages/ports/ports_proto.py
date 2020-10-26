""" Module for Abstract Class: Ports.

    Module has semantic contract for Ports Class.
"""
from abc import ABC, abstractmethod


class ProtoPorts(ABC):
    """ Abstract Class for Ports Class

        Class contains the core implementation details, functionalities and informations for ports.
    """
    @abstractmethod
    def check_ports(self):
        """Semantic contract for check_ports.

           Function for checking ports for origin and destination.
        """
        pass
