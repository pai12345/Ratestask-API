from src.ratestask.helper.helper import helper
from src.ratestask.api.service.service import service
from psycopg2 import DatabaseError, extras
import json


class Prices:
    def average_rates(self, query_recursion, query_rates):
        connection_pool_message = None
        connection_pool_status = None
        status = None
        message = None
        result = None
        try:
            _, url_message = helper.get_database_url("database")

            connection_pool_status, connection_pool_message = helper.create_connection_pool(
                url_message)

            connection_object_status, connection_object_messsage = helper.get_connection_object(
                connection_pool_message)

            if(connection_object_status == "success"):
                _, cursor = helper.create_connection_cursor(
                    connection_object_messsage)
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
            raise error
        finally:
            if (connection_pool_status == "success"):
                helper.close_connection_pool(connection_pool_message)

    def generate_price_payload(self, dats, origin, destination, price):
        try:
            result = []
            [result.append((origin, destination, i, price)) for i in dats]
            return {"status": "success", "message": result}
        except BaseException as error:
            raise error

    def upload_price(self, payload):
        connection_pool_message = None
        connection_pool_status = None
        status = None
        message = None
        try:
            _, url_message = helper.get_database_url("database")
            connection_pool_status, connection_pool_message = helper.create_connection_pool(
                url_message)

            connection_object_status, connection_object_message = helper.get_connection_object(
                connection_pool_message)

            _, query_upload_price = helper.generate_query_uploadprice()

            if(connection_object_status == "success"):
                _, cursor = helper.create_connection_cursor(
                    connection_object_message)
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
            raise error
        finally:
            if (connection_pool_status == "success"):
                helper.close_connection_pool(connection_pool_message)

    def get_price(self, price, currency):
        try:
            price_usd = None
            if(currency == 'USD'):
                price_usd = price
            elif(currency == None):
                price_usd = price
            else:
                _, exchange_rate = service.openexchangerates_service(currency)
                _, price_usd = helper.connvert_to_USD(
                    price, exchange_rate)
            return {"status": "success", "message": price_usd}
        except BaseException as error:
            raise error


prices = Prices()
