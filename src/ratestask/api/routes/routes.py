""" Module for API routes.

    Module has API implementation details, paths, business functionalities and informations.
"""

from flask import Blueprint, request, Response
from src.ratestask.packages.prices.prices import prices
from src.ratestask.packages.ports.ports import ports
from src.ratestask.packages.prices.prices import helper

router = Blueprint('/', __name__)


@router.route('/rates', methods=['GET'])
def rates():
    """API for fetching average prices.

       API returns a list with the average prices for each day on a route between port codes origin and destination.

      Parameters:
      - date_from: begin date,
        type: string,
        required: true,
        description: Indicated the begin date.
      - date_to: to date,
        type: string,
        required: true,
        description: Indicated the end date.
      - origin: origin code,
        type: string,
        required: true,
        description: Indicated origin code accepting either port codes or region slugs.
      - destination: destination code,
        type: string,
        required: true,
        description: Indicates destination code accepting either port codes or region slugs.

       Returns:
        list: average prices for each day.
    """
    try:
        precheck_parameters = helper.precheck_parameters(
            request.args.to_dict())
        precheck_status = precheck_parameters["status"]
        precheck_message = precheck_parameters["message"]

        if(precheck_status == "success"):
            date_from = request.args.get('date_from', type=str)
            date_to = request.args.get('date_to', type=str)
            origin = request.args.get('origin', type=str)
            destination = request.args.get('destination', type=str)

            payload = {
                "date_from": date_from,
                "date_to": date_to,
                "origin": origin,
                "destination": destination
            }

            validate_params = helper.validate_params(payload, "rates")
            check_url_params_status = validate_params["status"]
            check_url_params = validate_params["message"]

            if(check_url_params_status == "success"):
                date_from = date_from.strip()
                date_to = date_to.strip()
                origin = origin.strip()
                destination = destination.strip()

                check_sqlinjection = helper.check_sqlinjection(payload)
                check_sqlinjection_status = check_sqlinjection["status"]
                check_sqlinjection_message = check_sqlinjection["message"]

                if(check_sqlinjection_status == "success"):
                    validate_equality_check = helper.validate_equality_check(
                        origin, destination)
                    check_equality_status = validate_equality_check["status"]
                    check_equality_check = validate_equality_check["message"]

                    if(check_equality_status == "success"):
                        generate_query_recursion = helper.generate_query_recursion(
                            origin, destination)
                        query_recursion = generate_query_recursion["message"]

                        generate_query_rates = helper.generate_query_rates(
                            date_from, date_to, origin, destination)
                        query_rates_null = generate_query_rates["message"]

                        average_rates = prices.average_rates(
                            query_recursion, query_rates_null)

                        return Response(average_rates["message"], status=200)
                    else:
                        return Response(check_equality_check, status=400)
                else:
                    return Response(f"""{check_sqlinjection_message}""", status=400)
            else:
                return Response(f"""{check_url_params}""", status=400)
        else:
            return Response(f"""{precheck_message}""", status=400)
    except BaseException as error:
        return {"status": "error", "message": f"""Encountered Error for API endpoint /rates: {error}"""}


@router.route('/rates_null', methods=['GET'])
def rates_null():
    """API for fetching average prices.

       API endpoint return an empty value (JSON null) for days on which there are less than 3 prices in total.

      Parameters:
       - date_from: begin date,
         type: string,
         required: true,
         description: Indicated the begin date.
       - date_to: to date,
         type: string,
         required: true,
         description: Indicated the end date.
       - origin: origin code,
         type: string,
         required: true,
         description: Indicated origin code accepting either port codes or region slugs.
       - destination: destination code,
         type: string,
         required: true,
         description: Indicates destination code accepting either port codes or region slugs.

       Returns:
        list: average prices for each day.
    """
    try:
        precheck_parameters = helper.precheck_parameters(
            request.args.to_dict())
        precheck_status = precheck_parameters["status"]
        precheck_message = precheck_parameters["message"]

        if(precheck_status == "success"):
            date_from = request.args.get('date_from', type=str)
            date_to = request.args.get('date_to', type=str)
            origin = request.args.get('origin', type=str)
            destination = request.args.get('destination', type=str)

            payload = {
                "date_from": date_from,
                "date_to": date_to,
                "origin": origin,
                "destination": destination
            }

            check_url = helper.validate_params(payload, "rates")
            check_url_params_status = check_url["status"]
            check_url_params = check_url["message"]

            if(check_url_params_status == "success"):
                date_from = date_from.strip()
                date_to = date_to.strip()
                origin = origin.strip()
                destination = destination.strip()

                check_sqlinjection = helper.check_sqlinjection(payload)
                check_sqlinjection_status = check_sqlinjection["status"]
                check_sqlinjection_message = check_sqlinjection["message"]

                if(check_sqlinjection_status == "success"):
                    validate_equality_check = helper.validate_equality_check(
                        origin, destination)
                    check_equality_check_status = validate_equality_check["status"]
                    check_equality_check = validate_equality_check["message"]

                    if(check_equality_check_status == "success"):
                        generate_query_recursion = helper.generate_query_recursion(
                            origin, destination)
                        query_recursion = generate_query_recursion["message"]

                        generate_query_ratesnull = helper.generate_query_ratesnull(
                            date_from, date_to, origin, destination)
                        query_rates_null = generate_query_ratesnull["message"]

                        average_rates = prices.average_rates(
                            query_recursion, query_rates_null)

                        return Response(average_rates["message"], status=200)
                    else:
                        return Response(check_equality_check, status=400)
                else:
                    return Response(check_sqlinjection_message, status=400)
            else:
                return Response(f"""{check_url_params}""", status=400)
        else:
            return Response(f"""{precheck_message}""", status=400)
    except BaseException as error:
        return {"status": "error", "message": f"""Encountered Error for API endpoint /rates_null: {error}"""}


@router.route('/price', methods=['POST'])
def price():
    """API for uploding prices.

       API endpoint for uploading prices in USD for the given date range.

       Parameters:
       - date_from: begin date,
         type: string,
         required: true,
         description: Indicated the begin date.
       - date_to: to date,
         type: string,
         required: true,
         description: Indicated the end date.
       - origin: origin code,
         type: string,
         required: true,
         description: Indicated origin code accepting either port codes or region slugs.
       - destination: destination code,
         type: string,
         required: true,
         description: Indicated destination code accepting either port codes or region slugs.
       - price: price,
         currency: USD by default,
         type: string,
         required: true,
         description: Indicates the price.

       Returns:
        str: message for success or failure.
    """
    try:
        price_usd = None
        date_from = request.json.get('date_from')
        date_to = request.json.get('date_to')
        origin = request.json.get('origin')
        destination = request.json.get('destination')
        price = request.json.get('price')
        currency = request.json.get('currency')

        payload = {
            "date_from": date_from,
            "date_to": date_to,
            "origin": origin,
            "destination": destination,
            "price": price,
        }

        if(currency != None):
            payload["currency"] = currency

        validate_params = helper.validate_params(payload, "price")
        check_url_params_status = validate_params["status"]
        check_url_params = validate_params["message"]

        if(check_url_params_status == "success"):
            payload.pop("price")

            date_from = date_from.strip()
            date_to = date_to.strip()
            origin = origin.strip()
            destination = destination.strip()

            if(currency != None):
                currency = currency.strip()

            check_sqlinjection = helper.check_sqlinjection(payload)
            check_sqlinjection_status = check_sqlinjection["status"]
            check_sqlinjection_message = check_sqlinjection["message"]

            if(check_sqlinjection_status == "success"):
                validate_equality_check = helper.validate_equality_check(
                    origin, destination)
                check_equality_check_status = validate_equality_check["status"]
                check_equality_check = validate_equality_check["message"]

                if(check_equality_check_status == "success"):
                    check_ports_code = ports.check_ports(
                        origin, destination)
                    check_ports_status = check_ports_code["status"]
                    check_ports = check_ports_code["message"]

                    if(check_ports_status == "success"):
                        get_price = prices.get_price(price, currency)
                        price_usd_status = get_price["status"]
                        price_usd = get_price["message"]

                        if(price_usd_status == "success"):
                            get_range = helper.get_date_range(
                                date_from, date_to)
                            get_date_range = get_range["message"]

                            generate_price_payload = prices.generate_price_payload(
                                get_date_range, origin, destination, price_usd)
                            get_pricing_payload = generate_price_payload["message"]

                            upload_price_database = prices.upload_price(
                                get_pricing_payload)
                            upload_price_database_status = upload_price_database["status"]
                            upload_price_database_message = upload_price_database["message"]

                            if(upload_price_database_status == "success"):
                                return Response(upload_price_database_message, status=201)
                            else:
                                return Response(upload_price_database_message, status=400)
                        else:
                            return Response(price_usd, status=400)
                    else:
                        return Response(check_ports, status=400)
                else:
                    return Response(check_equality_check, status=400)
            else:
                return Response(check_sqlinjection_message, status=400)
        else:
            return Response(check_url_params, status=400)
    except BaseException as error:
        return {"status": "error", "message": f"""Encountered Error for API endpoint /prices: {error}"""}
