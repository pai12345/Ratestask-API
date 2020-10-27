""" Module for HTTP Services.

    Contains implementation details, functionalities and informations of HTTP library and services.
"""
from requests import get
import json
from src.ratestask.helper.helper import helper
from src.ratestask.api.service.service_proto import ProtoService


class Service(ProtoService):
    def openexchangerates_service(self, currency):
        """API for currency conversion.

           Simple, accurate and transparent exchange rates and currency conversion data API.

          Parameters:
           - currency: currency type,
             default: USD, 
             type: string,
             required: true,
             description: Indicates different currency type.

          Returns:
           status: status of the request-response cycle.
           message: Information of currency exchange rates.
        """
        try:
            base_url = helper.get_url('openexchangerates')
            response = get(f"""{base_url["message"]}&symbols={currency}""", json={
                           "key": "value"})
            response_to_json = json.loads(response.content.decode(
                'utf8').replace("'", '"'))
            currency_rate = [response_to_json['rates'][i]
                             for i in response_to_json['rates']]
            return {"status": "success", "message": currency_rate[0]}
        except BaseException as error:
            return {"status": "error", "message": f"""Encountered Error for openexchangerates API service: Conversion for '{currency}' failed"""}


service = Service()
