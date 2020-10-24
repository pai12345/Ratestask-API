from flask import Blueprint, request
from src.ratestask.packages.prices.prices import prices
from src.ratestask.packages.ports.ports import ports
from src.ratestask.packages.prices.prices import helper

router = Blueprint('/', __name__)


@router.route('/rates', methods=['GET'])
def rates():
    try:
        date_from = request.args.get('date_from', type=str)
        date_to = request.args.get('date_to', type=str)
        origin = request.args.get('origin', type=str)
        destination = request.args.get('destination', type=str)

        check_url_params_status, check_url_params = helper.validate_params(
            date_from, date_to, origin, destination)

        if(check_url_params_status == "success"):
            check_equality_status, check_equality_check = helper.validate_equality_check(
                origin, destination)

            if(check_equality_status == "success"):
                _, query_recursion = helper.generate_query_recursion(
                    destination)
                _, query_rates_null = helper.generate_query_rates(
                    date_from, date_to, origin, destination)
                _, average_rate = prices.average_rates(
                    query_recursion, query_rates_null)
                return average_rate
            else:
                return check_equality_check
        else:
            return check_url_params
    except BaseException as error:
        raise error


@router.route('/rates_null', methods=['GET'])
def rates_null():
    try:
        date_from = request.args.get('date_from', type=str)
        date_to = request.args.get('date_to', type=str)
        origin = request.args.get('origin', type=str)
        destination = request.args.get('destination', type=str)

        check_url_params_status, check_url_params = helper.validate_params(
            date_from, date_to, origin, destination)

        if(check_url_params_status == "success"):
            check_equality_check_status, check_equality_check = helper.validate_equality_check(
                origin, destination)

            if(check_equality_check_status == "success"):
                _, query_recursion = helper.generate_query_recursion(
                    destination)
                _, query_rates_null = helper.generate_query_ratesnull(
                    date_from, date_to, origin, destination)
                _, average_rate = prices.average_rates(
                    query_recursion, query_rates_null)
                return average_rate
            else:
                return check_equality_check
        else:
            return check_url_params
    except BaseException as error:
        raise error


@router.route('/price', methods=['POST'])
def price():
    try:
        price_usd = None
        date_from = request.json.get('date_from')
        date_to = request.json.get('date_to')
        origin = request.json.get('origin')
        destination = request.json.get('destination')
        price = request.json.get('price')
        currency = request.json.get('currency')

        check_url_params_status, check_url_params = helper.validate_params(
            date_from, date_to, origin, destination)

        if(check_url_params_status == "success"):
            check_equality_check_status, check_equality_check = helper.validate_equality_check(
                origin, destination)

            if(check_equality_check_status == "success"):
                check_ports_status, check_ports = ports.check_ports(
                    origin, destination)

                if(check_ports_status == "success"):
                    _, price_usd = prices.get_price(price, currency)

                    _, get_date_range = helper.get_date_range(
                        date_from, date_to)

                    _, get_pricing_payload = prices.generate_price_payload(
                        get_date_range, origin, destination, price_usd)

                    _, upload_price_database = prices.upload_price(
                        get_pricing_payload)
                    return upload_price_database
                else:
                    return check_ports
            else:
                return check_equality_check
        else:
            return check_url_params
    except BaseException as error:
        raise error
