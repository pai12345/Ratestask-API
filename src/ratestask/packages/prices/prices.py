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
                exchange_rate = service.openexchangerates_service(currency)
                price_usd = helper.connvert_to_USD(
                    price, exchange_rate["message"])
            return {"status": "success", "message": price_usd["message"]}
        except BaseException as error:
            raise error


prices = Prices()
