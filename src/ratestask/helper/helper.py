""" Module for assist API.

    Module has implementation details, functionalities and informations for assisting APIs.
"""

from psycopg2 import pool, DatabaseError
import yaml
from datetime import timedelta, date, datetime
from cerberus import Validator


class Helper:
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
            raise error

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
            raise error

    def close_connection_pool(self, connection_pool):
        """Close Connection Pool

           Function for closing existing database connection pool.

           Parameters:
            - connection_pool: connection pool,
              required: true,
              description: Inforamtion of existing connection pool.

           Returns:
            status: status of the request-response cycle.
            message: Information of closed connection pool.
        """
        try:
            close_pool = connection_pool.closeall()
            return {"status": "success", "message": close_pool}
        except(BaseException, DatabaseError) as error:
            raise error

    def get_connection_object(self, connection_pool):
        try:
            get_connection = connection_pool.getconn()
            return {"status": "success", "message": get_connection}
        except(BaseException, DatabaseError) as error:
            raise error

    def release_connection_object(self, connection_pool, connection_object):
        try:
            release = connection_pool.putconn(connection_object)
            return {"status": "success", "message": release}
        except(BaseException, DatabaseError) as error:
            raise error

    def create_connection_cursor(self, connection_object):
        try:
            cursor = connection_object.cursor()
            return {"status": "success", "message": cursor}
        except(BaseException, DatabaseError) as error:
            raise error

    def close_connection_cursor(self, connection_cursor):
        try:
            cursor_close = connection_cursor.close()
            return {"status": "success", "message": cursor_close}
        except(BaseException, DatabaseError) as error:
            raise error

    def generate_query_recursion(self, slug):
        try:
            message = f"""WITH RECURSIVE a AS (SELECT slug, parent_slug, 1:: integer recursion_level FROM public.regions WHERE slug ='{slug}' UNION ALL SELECT d.slug, d.parent_slug, a.recursion_level + 1 FROM public.regions d JOIN a ON a.slug = d.parent_slug)"""
            return {"status": "success", "message": message}
        except BaseException as error:
            raise error

    def generate_query_rates(self, date_from, date_to, origin, destination):
        try:
            message = f"""SELECT json_agg(json_build_object('day', day, 'average_price', price)) as result FROM(SELECT day, AVG(price) price FROM public.prices WHERE DAY BETWEEN '{date_from}' AND '{date_to}' AND orig_code in (select code from public.ports where code='{origin}' or parent_slug in (select slug from a)) AND dest_code in (select code from public.ports where code='{destination}' or parent_slug in (select slug from a)) GROUP BY DAY ORDER BY DAY ASC) as sub"""
            return{"status": "success", "message": message}
        except BaseException as error:
            raise error

    def generate_query_ratesnull(self, date_from, date_to, origin, destination):
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
            raise error

    def generate_query_portcheck(self):
        try:
            message = f"""SELECT json_agg(json_build_object('code',code)) as result from public.ports where code in %s"""
            return {"status": "success", "message": message}
        except BaseException as error:
            raise error

    def generate_query_uploadprice(self):
        try:
            message = f"""insert into public.prices (orig_code, dest_code, day, price) values %s RETURNING price"""
            return {"status": "success", "message": message}
        except BaseException as error:
            raise error

    def get_date_range(self, start_date, end_date):
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
            raise error

    def connvert_to_USD(self, price, exchange_rate):
        try:
            price_USD = price/exchange_rate
            price_roundoff = round(price_USD)
            return {"status": "success", "message": price_roundoff}
        except BaseException as error:
            raise error

    def validate_params(self, date_from, date_to, origin, destination):
        try:
            schema = {'date_from': {'required': True, 'type': 'string', 'minlength': 10, 'maxlength': 10, "regex": "^\d{4}\-(0[1-9]|1[012])\-(0[1-9]|[12][0-9]|3[01])$"},
                      'date_to': {'required': True, 'type': 'string', 'minlength': 10, 'maxlength': 10, "regex": "^\d{4}\-(0[1-9]|1[012])\-(0[1-9]|[12][0-9]|3[01])$"},
                      'origin': {'required': True, 'type': 'string'},
                      'destination': {'required': True, 'type': 'string'}}
            payload = {
                'date_from': date_from,
                'date_to': date_to,
                'origin': origin,
                'destination': destination}

            check_data = Validator(schema)
            test = check_data.validate(payload)
            if(test):
                return {"status": "success", "message": "valid"}
            else:
                return {"status": "error", "message": check_data.errors}
        except BaseException as error:
            raise error

    def validate_equality_check(self, origin, destination):
        try:
            if (origin == destination):
                return {"status": "error",
                        "message": "origin and destination cannot be same"}
            else:
                return {"status": "success", "message": "valid"}
        except BaseException as error:
            raise error

    def validate_ports_types(self, origin, result):
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
            raise error


helper = Helper()
