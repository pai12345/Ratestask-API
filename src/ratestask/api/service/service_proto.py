""" Module for Abstract Class: Service.

    Module has semantic contract for Service Class.
"""
from abc import ABC, abstractmethod


class ProtoService(ABC):
    """ Abstract Class for Service Class.

        Class contains the core implementation details, functionalities and informations for assisting classes and methods.
    """

    @abstractmethod
    def openexchangerates_service(self):
        """Semantic contract for openexchangerates_service.

           Simple, accurate and transparent exchange rates and currency conversion data API.
        """
        pass
