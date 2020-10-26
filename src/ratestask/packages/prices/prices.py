""" Module for prices.

    Module has implementation details, business functionalities and informations for prices.
"""
from src.ratestask.helper.helper import helper
from src.ratestask.api.service.service import service
from src.ratestask.packages.prices.prices_proto import ProtoPrices
from psycopg2 import DatabaseError, extras
import json


class Prices(ProtoPrices):
    """ Prices Class.

        Class contains the core implementation details, functionalities and informations for prices.
    """

    def average_rates(self, query_recursion, query_rates):
        """ Get average prices.

            Get average prices for each day on a route between port codes origin and destination.

            Parameters:
            - query_recursion: recursion query,
              type: query,
              required: true,
              description: query for recursion
            - query_rates: rates query,
              type: query,
              required: true,
              description: query for average rates

            Returns:
             status: status of the request-response cycle.
             message: list of average prices.
        """
        connection_pool_message = None
        connection_pool_status = None
        try:
            result = None
            status = None
            message = None
            get_url = helper.get_url("database")
            url = get_url["message"]

            create_connection_pool = helper.create_connection_pool(url)
            connection_pool_status = create_connection_pool["status"]
            connection_pool_message = create_connection_pool["message"]

            get_connection_object = helper.get_connection_object(
                connection_pool_message)
            connection_object_status = get_connection_object["status"]
            connection_object_messsage = get_connection_object["message"]

            if(connection_object_status == "success"):
                create_connection_cursor = helper.create_connection_cursor(
                    connection_object_messsage)
                cursor = create_connection_cursor["message"]

                cursor.execute(
                    f"""
                   {query_recursion}
                   {query_rates}""")
                result = cursor.fetchall()
                helper.close_connection_cursor(cursor)
            helper.release_connection_object(
                connection_pool_message, connection_object_messsage)
            if(result[0][0] != None):
                status = "success"
                message = json.dumps(result[0][0])
            else:
                status = "success"
                message = "No records found for provided details"
            return {"status": status, "message": message}
        except (BaseException, DatabaseError) as error:
            return {"status": "error", "message": f"""Encountered Error for checking average prices:{error}"""}
        finally:
            if (connection_pool_status == "success"):
                helper.close_connection_pool(connection_pool_message)

    def generate_price_payload(self, date_range, origin, destination, price):
        """ Generate payload.

            Generate payload containing details of required fields for price.

            Parameters:
            - date_range: date range,
              type: string,
              required: true,
              description: list of date range.
            - origin: origin code,
              type: string,
              required: true,
              description: Information of origin code.
            - destination: destination code,
              type: string,
              required: true,
              description: Information of destination code.
            - price: price,
              type: string,
              required: true,
              description: Information of price.

            Returns:
             status: status of the request-response cycle.
             message: payload having required fields and values.
        """
        try:
            result = []
            [result.append((origin, destination, i, price))
             for i in date_range]
            return {"status": "success", "message": result}
        except BaseException as error:
            return {"status": "error", "message": f"""Encountered Error for generating price payload:{error}"""}

    def upload_price(self, payload):
        """Upload price.

           Function to upload price.

          Parameters:
           - payload: payload data, 
             type: list,
             required: true,
             description: list structured with required fields and data for uploading.

          Returns:
           status: status of the request-response cycle.
           message: Information of success or error.
        """
        connection_pool_message = None
        connection_pool_status = None
        try:
            status = None
            message = None
            get_url = helper.get_url("database")
            url = get_url["message"]

            create_connection_pool = helper.create_connection_pool(url)
            connection_pool_status = create_connection_pool["status"]
            connection_pool_message = create_connection_pool["message"]

            get_connection_object = helper.get_connection_object(
                connection_pool_message)
            connection_object_status = get_connection_object["status"]
            connection_object_message = get_connection_object["message"]

            generate_query_uploadprice = helper.generate_query_uploadprice()
            query_upload_price = generate_query_uploadprice["message"]

            if(connection_object_status == "success"):
                create_connection_cursor = helper.create_connection_cursor(
                    connection_object_message)
                cursor = create_connection_cursor["message"]

                extras.execute_values(
                    cursor, query_upload_price, payload)
                result = cursor.fetchall()
                if(len(result) == len(payload)):
                    connection_object_message.commit()
                    status = "success"
                    message = "Data uploaded successfully"
                else:
                    connection_object_message.rollback()
                    status = "error"
                    message = "Not all rows were inserted, rollbacked updates"
                helper.close_connection_cursor(cursor)
            helper.release_connection_object(
                connection_pool_message, connection_object_message)
            return {"status": status, "message": message}
        except BaseException as error:
            return {"status": "error", "message": f"""Encountered Error for uploading price:{error}"""}
        finally:
            if (connection_pool_status == "success"):
                helper.close_connection_pool(connection_pool_message)

    def get_price(self, price, currency):
        """Get price.

           Function to fetch price in USD.

          Parameters:
           - price: price type, 
             type: integer,
             required: true,
             description: Indicates price.
           - currency: currency type,
             default: USD, 
             type: string,
             required: true,
             description: Indicates different currency type.

          Returns:
           status: status of the request-response cycle.
           message: price in USD.
        """
        try:
            price_usd = None
            if(currency == 'USD'):
                price_usd = price
            elif(currency == None):
                price_usd = price
            else:
                exchange_rate = service.openexchangerates_service(currency)
                price_usd = helper.connvert_to_USD(
                    price, exchange_rate["message"])
            return {"status": "success", "message": price_usd["message"]}
        except BaseException as error:
            return {"status": "error", "message": f"""Encountered Error for fetching price:{error}"""}


prices = Prices()
