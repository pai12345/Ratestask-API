from requests import get
import json
from src.ratestask.helper.helper import helper


class Service:
    def openexchangerates_service(self, currency):
        try:
            _, base_url = helper.get_database_url('openexchangerates')
            response = get(f"""{base_url}&symbols={currency}""", json={
                           "key": "value"})
            response_to_json = json.loads(response.content.decode(
                'utf8').replace("'", '"'))
            currency_rate = [response_to_json['rates'][i]
                             for i in response_to_json['rates']]
            return currency_rate[0]
        except BaseException as error:
            raise error


service = Service()
