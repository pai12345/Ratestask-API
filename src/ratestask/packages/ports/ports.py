from src.ratestask.helper.helper import helper
from psycopg2 import DatabaseError


class Ports:
    def check_ports(self, origin, destination):
        connection_pool = None
        connection_pool_status = None
        validate_result = None
        try:
            _, url = helper.get_database_url("database")
            connection_pool_status, connection_pool = helper.create_connection_pool(
                url)
            connection_object_status, connection_object = helper.get_connection_object(
                connection_pool)
            _, query_check_ports = helper.generate_query_portcheck()

            if(connection_object_status):
                _, cursor = helper.create_connection_cursor(
                    connection_object)
                cursor.execute(query_check_ports, [(origin, destination)])
                result = cursor.fetchone()
                _, validate_result = helper.validate_ports_types(
                    origin, result)
                helper.close_connection_cursor(cursor)
            helper.release_connection_object(
                connection_pool, connection_object)
            return validate_result
        except (BaseException, DatabaseError) as error:
            raise error
        finally:
            if (connection_pool_status == "success"):
                helper.close_connection_pool(connection_pool)


ports = Ports()
