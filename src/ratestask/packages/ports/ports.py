""" Module for Ports.

    Module has implementation details, business functionalities and informations for ports.
"""
from src.ratestask.helper.helper import helper
from psycopg2 import DatabaseError
from src.ratestask.packages.ports.ports_proto import ProtoPorts


class Ports(ProtoPorts):
    """ Ports Class

        Class contains the core implementation details, functionalities and informations for ports.
    """

    def check_ports(self, origin, destination):
        """Fetch URL

           Function for checking ports for origin and destination.

           Parameters:
            - origin: origin code,
              type: string,
              required: true,
              description: Inforamtion for origin code.
            - destination: destination code,
              type: string,
              required: true,
              description: Inforamtion for destination code.

           Returns:
             status: status of the request-response cycle.
             message: Information of success or failure.
        """
        connection_pool = None
        connection_pool_status = None

        try:
            status = None
            message = None
            validate_result = None
            get_url = helper.get_url("database")
            url = get_url["message"]

            create_connection_pool = helper.create_connection_pool(
                url)
            connection_pool_status = create_connection_pool["status"]
            connection_pool = create_connection_pool["message"]

            if(connection_pool_status == "success"):
                get_connection_object = helper.get_connection_object(
                    connection_pool)
                connection_object_status = get_connection_object["status"]
                connection_object = get_connection_object["message"]

                if(connection_object_status == "success"):
                    create_connection_cursor = helper.create_connection_cursor(
                        connection_object)
                    cursor_status = create_connection_cursor["status"]
                    cursor = create_connection_cursor["message"]

                    if(cursor_status == "success"):
                        generate_query_portcheck = helper.generate_query_portcheck()
                        query_check_ports = generate_query_portcheck["message"]

                        cursor.execute(query_check_ports, [
                                       (origin, destination)])
                        result = cursor.fetchone()
                        validate_ports_types = helper.validate_ports_types(
                            origin, result)
                        validate_result = validate_ports_types["message"]
                        helper.close_connection_cursor(cursor)
                        helper.release_connection_object(
                            connection_pool, connection_object)
                        status = "success"
                        message = validate_result
                    else:
                        status = "error"
                        message = cursor
                else:
                    status = "error"
                    message = connection_object
            else:
                status = "error"
                message = connection_pool
            return {"status": status, "message": message}
        except (BaseException, DatabaseError) as error:
            return {"status": "error", "message": f"""Encountered Error for checking ports for origin and destination: {error}"""}
        finally:
            if (connection_pool_status == "success"):
                helper.close_connection_pool(connection_pool)


ports = Ports()
