""" Module for assist API.

    Module has implementation details, functionalities and informations for assisting classes and methods.
"""
from psycopg2 import pool, DatabaseError
import yaml
from datetime import timedelta, datetime
from cerberus import Validator
from src.ratestask.helper.helper_proto import ProtoHelper


class Helper(ProtoHelper):
    """ Helper Class

        Class contains the core implementation details, functionalities and informations for assisting APIs.
    """

    def get_url(self, type):
        """Fetch URL

           Function for fetching URL for database or openexchangerates API.

           Parameters:
            - type: type of information,
              type: string,
              required: true,
              description: Inforamtion for generating URL.

           Returns:
             status: status of the request-response cycle.
             message: URL Address.
        """
        result = None
        try:
            with open("src/ratestask/config/config.yml") as file:
                config_data = yaml.load(file, Loader=yaml.FullLoader)
                if(type == "database"):
                    result = f"""{config_data['database']['type']}://{config_data['database']['user']}:{config_data['database']['password']}@{config_data['database']['address']}:{config_data['database']['port']}/{config_data['database']['name']}"""
                elif(type == "openexchangerates"):
                    result = f"""https://{config_data['openexchangerates']['address']}?app_id={config_data['openexchangerates']['app_id']}"""
                else:
                    result = None
                return {"status": "success", "message": result}
        except BaseException as error:
            return {"status": "error", "message": f"""Encountered Error while fetching URL:{error}"""}

    def create_connection_pool(self, url):
        """Create Connection Pool

           Function for creating database connection pool.

           Parameters:
            - url: url address,
              type: string,
              required: true,
              description: Inforamtion for generating connection pool.

           Returns:
             status: status of the request-response cycle.
             message: new pool of connection.
        """
        try:
            create_pool = pool.SimpleConnectionPool(
                1, 20, url)
            return {"status": "success", "message": create_pool}
        except(BaseException, DatabaseError) as error:
            return {"status": "error", "message": f"""Encountered Error while creating connection pool:{error}"""}

    def close_connection_pool(self, connection_pool):
        """Close Connection Pool

           Function for closing existing database connection pool.

           Parameters:
            - connection_pool: connection pool,
              required: true,
              description: Inforamtion of existing connection pool.

           Returns:
             status: status of the request-response cycle.
             message: close exisitng connection pool.
        """
        try:
            close_pool = connection_pool.closeall()
            return {"status": "success", "message": close_pool}
        except(BaseException, DatabaseError) as error:
            return {"status": "error", "message": f"""Encountered Error while closing connection pool:{error}"""}

    def get_connection_object(self, connection_pool):
        """Get Connection

           Function for fetching connection from pool.

           Parameters:
            - connection_pool: connection pool,
              required: true,
              description: Inforamtion of existing connection pool.

           Returns:
             status: status of the request-response cycle.
             message: a new connection object from connection pool.
        """
        try:
            get_connection = connection_pool.getconn()
            return {"status": "success", "message": get_connection}
        except(BaseException, DatabaseError) as error:
            return {"status": "error", "message": f"""Encountered Error while fetching connection object from pool:{error}"""}

    def release_connection_object(self, connection_pool, connection_object):
        """Release connection.

           Function for releasing existing connection from pool.

           Parameters:
            - connection_object: connection from connection pool,
              type: string,
              required: true,
              description: contains connection from connection pool.

           Returns:
             status: status of the request-response cycle.
             message: release existing connection object to pool.
        """
        try:
            release = connection_pool.putconn(connection_object)
            return {"status": "success", "message": release}
        except(BaseException, DatabaseError) as error:
            return {"status": "error", "message": f"""Encountered Error while releasing connection object to pool:{error}"""}

    def create_connection_cursor(self, connection_object):
        """Create cursor.

           Function for creating new cursor object.

           Parameters:
            - connection_object: connection from pool,
              type: string,
              required: true,
              description: contains connection from pool.

           Returns:
             status: status of the request-response cycle.
             message: new cursor object.
        """
        try:
            cursor = connection_object.cursor()
            return {"status": "success", "message": cursor}
        except(BaseException, DatabaseError) as error:
            return {"status": "error", "message": f"""Encountered Error while creating cursor object:{error}"""}

    def close_connection_cursor(self, connection_cursor):
        """Close cursor.

           Function for closing existing cursor object.

           Parameters:
            - connection_cursor: cursor for psycopg2,
              type: string,
              required: true,
              description: contains cursor object for psycopg2.

           Returns:
            status: status of the request-response cycle.
            message: close existing cursor object.
        """
        try:
            cursor_close = connection_cursor.close()
            return {"status": "success", "message": cursor_close}
        except(BaseException, DatabaseError) as error:
            return {"status": "error", "message": f"""Encountered Error while closing cursor object:{error}"""}

    def generate_query_recursion(self, slug):
        """Query for recursion.

           Function for generating query for recursion.

           Parameters:
            - slug: destination code,
              type: string,
              required: true,
              description: contains destination code.

           Returns:
            status: status of the request-response cycle.
            message: query for recursion.
        """
        try:
            message = f"""WITH RECURSIVE a AS (SELECT slug, parent_slug, 1:: integer recursion_level FROM public.regions WHERE slug ='{slug}' UNION ALL SELECT d.slug, d.parent_slug, a.recursion_level + 1 FROM public.regions d JOIN a ON a.slug = d.parent_slug)"""
            return {"status": "success", "message": message}
        except BaseException as error:
            return {"status": "error", "message": f"""Encountered Error while generating recursion query:{error}"""}

    def generate_query_rates(self, date_from, date_to, origin, destination):
        """Query for rates API.

           Function for generating query returning a list with the average prices for each day on a route between port codes origin and destination.

           Parameters:
            - date_from: begin date,
              type: string,
              required: true,
              description: contains begin date.
            - date_to: end date,
              type: string,
              required: true,
              description: contains end date.
            - origin: origin code,
              type: string,
              required: true,
              description: contains origin code.
            - destination: destination code,
              type: string,
              required: true,
              description: contains destination code.

           Returns:
            status: status of the request-response cycle.
            message: query for rates.
        """
        try:
            message = f"""SELECT json_agg(json_build_object('day', day, 'average_price', price)) as result FROM(SELECT day, AVG(price) price FROM public.prices WHERE DAY BETWEEN '{date_from}' AND '{date_to}' AND orig_code in (select code from public.ports where code='{origin}' or parent_slug in (select slug from a)) AND dest_code in (select code from public.ports where code='{destination}' or parent_slug in (select slug from a)) GROUP BY DAY ORDER BY DAY ASC) as sub"""
            return{"status": "success", "message": message}
        except BaseException as error:
            return {"status": "error", "message": f"""Encountered Error while generating query for rates:{error}"""}

    def generate_query_ratesnull(self, date_from, date_to, origin, destination):
        """Query for rates_null API.

           Function for generating query for returning an empty value(JSON null) for days on which there are less than 3 prices in total.

           Parameters:
            - date_from: begin date,
              type: string,
              required: true,
              description: contains begin date.
            - date_to: end date,
              type: string,
              required: true,
              description: contains end date.
            - origin: origin code,
              type: string,
              required: true,
              description: contains origin code.
            - destination: destination code,
              type: string,
              required: true,
              description: contains destination code.

           Returns:
            status: status of the request-response cycle.
            message: query for rates.
        """
        try:
            message = f"""
SELECT json_agg(json_build_object('day', day, 'average_price', average_price)) as result FROM(SELECT day,
case
	 when Count(price) < 3 then null
	 else avg(price)
end as average_price
FROM public.prices
WHERE
DAY BETWEEN '{date_from}' AND '{date_to}'
AND orig_code in (select code from public.ports where code='{origin}' or parent_slug in (select slug from a))
AND dest_code in (select code from public.ports where code='{destination}' or parent_slug in (select slug from a))
GROUP BY DAY
ORDER BY DAY ASC) as sub
"""
            return {"status": "success", "message": message}
        except BaseException as error:
            return {"status": "error", "message": f"""Encountered Error while generating query for rates_null:{error}"""}

    def generate_query_portcheck(self):
        """Query for port check.

           Function for generating query for port check.

           Returns:
            status: status of the request-response cycle.
            message: query for port check.
        """
        try:
            message = f"""SELECT json_agg(json_build_object('code', code)) as result from public.ports where code in %s"""
            return {"status": "success", "message": message}
        except BaseException as error:
            return {"status": "error", "message": f"""Encountered Error while generating query for portcheck:{error}"""}

    def generate_query_uploadprice(self):
        """Query for upload price.

           Function for generating query on upload price.

           Returns:
            status: status of the request-response cycle.
            message: query of upload price
        """
        try:
            message = f"""insert into public.prices(orig_code, dest_code, day, price) values % s RETURNING price"""
            return {"status": "success", "message": message}
        except BaseException as error:
            return {"status": "error", "message": f"""Encountered Error while generating query for uploading prices:{error}"""}

    def get_date_range(self, start_date, end_date):
        """Get date range.

           Function for fetching date range.

           Parameters:
            - start_date: begin date,
              type: string,
              required: true,
              description: contains begin date.
            - exchange_rate: end date,
              type: string,
              required: true,
              description: contains end date.

           Returns:
            status: status of the request-response cycle.
            message: contains date ranges
        """
        try:
            Dats = list()
            start = datetime.strptime(start_date, '%Y-%m-%d')
            end = datetime.strptime(end_date, '%Y-%m-%d')
            step = timedelta(days=1)
            while start <= end:
                Dats.append(start.strftime("%Y-%m-%d"))
                start += step
            return {"status": "success", "message": Dats}
        except BaseException as error:
            return {"status": "error", "message": f"""Encountered Error while fetching date range:{error}"""}

    def connvert_to_USD(self, price, exchange_rate):
        """Convert currency to USD.

           Function for converting existing currency type to USD.

           Parameters:
            - price: price,
              type: integer,
              required: true,
              description: Information on price.
            - exchange_rate: exchange rate,
              type: integer,
              required: true,
              description: Information of currency exchange rate.

           Returns:
            status: status of the request-response cycle.
            message: rounded-off price in USD.
        """
        try:
            price_USD = price/exchange_rate
            price_roundoff = round(price_USD)
            return {"status": "success", "message": price_roundoff}
        except BaseException as error:
            return {"status": "error", "message": f"""Encountered Error while computing price to USD:{error}"""}

    def validate_params(self, payload, category):
        """Validates url params and payload.

           Function for validateing request url parameters and request payload.

           Parameters:
            - payload: request data,
              type: dictionary,
              required: true,
              description: contains request payload as a dictionary.
            - category: information,
              type: string,
              required: true,
              description: Inforamtion for validation category.

           Returns:
            status: status of the request-response cycle.
            message: contains success or error messages.
        """
        try:
            schema = None
            status = None
            message = None
            if(category == "price"):
                schema = {'date_from': {'required': True, 'type': 'string', 'minlength': 10, 'maxlength': 10, "regex": "^\d{4}\-(0[1-9]|1[012])\-(0[1-9]|[12][0-9]|3[01])$"},
                          'date_to': {'required': True, 'type': 'string', 'minlength': 10, 'maxlength': 10, "regex": "^\d{4}\-(0[1-9]|1[012])\-(0[1-9]|[12][0-9]|3[01])$"},
                          'origin': {'required': True, 'type': 'string'},
                          'destination': {'required': True, 'type': 'string'},
                          'price': {'required': True, 'type': 'integer'},
                          'currency': {'type': 'string'}}
            elif(category == "rates"):
                schema = {'date_from': {'required': True, 'type': 'string', 'minlength': 10, 'maxlength': 10, "regex": "^\d{4}\-(0[1-9]|1[012])\-(0[1-9]|[12][0-9]|3[01])$"},
                          'date_to': {'required': True, 'type': 'string', 'minlength': 10, 'maxlength': 10, "regex": "^\d{4}\-(0[1-9]|1[012])\-(0[1-9]|[12][0-9]|3[01])$"},
                          'origin': {'required': True, 'type': 'string'},
                          'destination': {'required': True, 'type': 'string'}}
            else:
                return {"status": "error", "message": "Invalid parameters passed for Validation"}

            check_data = Validator(schema)
            test = check_data.validate(payload)
            if(test == True):
                if(payload["date_from"] > payload["date_to"]):
                    status = "error"
                    message = "date_from cannot be greater than date_to."
                elif(payload["date_from"] == payload["date_to"]):
                    status = "error"
                    message = "date_from cannot be equal to date_to."
                else:
                    status = "success"
                    message = "valid"
            else:
                status = "error"
                message = check_data.errors
            return {"status": status, "message": message}
        except BaseException as error:
            return {"status": "error", "message": f"""Encountered Error while validating parameters:{error}"""}

    def validate_equality_check(self, origin, destination):
        """Equality Check.

           Function for checking equality for origin and destination.

           Parameters:
            - origin: origin code,
              type: string,
              required: true,
              description: contains origin code.
            - destination: destination code,
              type: string,
              required: true,
              description: contains destination code.

           Returns:
            status: status of the request-response cycle.
            message: contains success or error messages.
        """
        try:
            status = None
            message = None
            if (origin == destination):
                status = "error"
                message = "origin and destination cannot be same."
            else:
                status = "success"
                message = "valid"
            return {"status": status, "message": message}
        except BaseException as error:
            return {"status": "error", "message": f"""Encountered Error while validating equality check:{error}"""}

    def validate_ports_types(self, origin, result):
        """Validate ports.

           Function for checking equality for origin and destination.

           Parameters:
            - origin: origin code,
              type: string,
              required: true,
              description: contains origin code.
            - result: result,
              type: string,
              required: true,
              description: database query results of ports for origin and destination.

           Returns:
            status: status of the request-response cycle.
            message: contains success or error messages.
        """
        status = None
        message = None
        try:
            if(len(result[0]) > 1):
                status = "success"
                message = "origin and destination codes found"
            elif(len(result[0]) == 1):
                codes = [i['code'] for i in result[0]]
                if(origin in codes):
                    status = "error"
                    message = "origin code found, destination code does not exist"
                else:
                    status = "error"
                    message = "destination code found, origin code does not exist"
            else:
                status = "error"
                message = "No origin and destination codes present"
            return {"status": status, "message": message}
        except BaseException as error:
            return {"status": "error", "message": f"""Encountered Error while validating port types:{error}"""}

    def precheck_parameters(self, payload):
        """Precheck all parameters.

           Function for pre-checking all payload parameters.

           Parameters:
            - payload: payload data,
              type: dictionary,
              required: true,
              description: contains key-value pairs.

           Returns:
            status: status of the request-response cycle.
            message: contains success or error messages.
        """
        try:
            status = None
            message = None
            if(len(payload) == 4):
                accept = ["date_from", "date_to", "origin", "destination"]
                check = [i for i in payload]
                if(accept == check):
                    status = "success"
                    message = "valid"
                else:
                    status = "error"
                    message = "Invalid, allowed parameters are date_from, date_to, origin and destination."
            else:
                status = "error"
                message = "Invalid URL parameters"
            return {"status": status, "message": message}
        except BaseException as error:
            return {"status": "error", "message": f"""Encountered Error while prechecking parameters:{error}"""}

    def check_sqlinjection(self, payload):
        """check for SQL injections.

           Function for checking all parameters for sql injection.

           Parameters:
            - payload: payload data,
              type: dictionary,
              required: true,
              description: contains key-value pairs.

           Returns:
            status: status of the request-response cycle.
            message: contains success or error messages.
        """
        try:
            status = None
            message = None
            blacklist = ["DROP", "TRUNCATE", "ALTER",
                         "DELETE", "INSERT", "UPDATE", "CREATE"]
            data = [payload[i] for i in payload]
            validate = [True if i in blacklist else False for i in data]
            check = True in validate
            if(check):
                status = "error"
                message = "Invalid parameters present"
            else:
                status = "success"
                message = "valid"
            return {"status": status, "message": message}
        except BaseException as error:
            return {"status": "error", "message": f"""Encountered Error while validating for SQL injection:{error}"""}


helper = Helper()
