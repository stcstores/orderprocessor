import os

import argparse
from termcolor import cprint
import colorama

from weights_db import WeightsDB
import pylinnworks

from . exceptions import OrderNumberNotFound
from . exceptions import OrderGUIDNotFound
from . exceptions import OrderDataNotFound
from . exceptions import OrderAlreadyProcessed
from . exceptions import LinnworksAPIUnavailable
from . functions import get_order, process_weight


def process_orders(api_session, weights=False):
    colorama.init()
    if weights is True:
        cprint('Processing orders with weights', 'green')
        weight_database = WeightsDB().update_db
        completed_items = WeightsDB().completed_db.get_stock_ids()
    else:
        cprint('Processing orders without weights', 'red')

    while True:
        order = None
        order_number = input('Order Number > ')
        if order_number.lower() == 'c':
            os.system('cls')
            continue
        if order_number.lower() == 'exit':
            return 0
        try:
            order = get_order(api_session, order_number)
        except OrderNumberNotFound as e:
            e.print_error()
            continue
        except OrderGUIDNotFound as e:
            e.print_error()
            continue
        except OrderDataNotFound as e:
            e.print_error()
            continue
        except OrderAlreadyProcessed as e:
            e.print_error()
            continue
        customer_name = order.customer_name
        cprint(customer_name, 'yellow', attrs=['bold'])
        if order.invoice_printed is not True:
            cprint('Order Not Printed! {} for {}'.format(
                order_number, customer_name), 'red', attrs=['bold'])
        if input('Process?') != '':
            cprint('Order Not Processed {} for {}'.format(
                order_number, customer_name), 'red')
            continue
        if weights is True:
            process_weight(weight_database, order, completed_items)
        process_success = order.process()
        if process_success is False:
            cprint('Error: {} for {} may not be processed'.format(
                order_number, customer_name), 'red', attrs=['bold'])
        else:
            cprint('{} Processed for {}'.format(
                order_number, customer_name), 'green', 'on_white')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--weights", dest='weights', action='store_true')
    parser.add_argument("--no-weights", dest='weights', action='store_false')
    parser.set_defaults(weights=True)
    args = parser.parse_args()
    try:
        api_session = pylinnworks.LinnworksAPISession()
    except:
        raise LinnworksAPIUnavailable(None)
    process_orders(api_session, weights=args.weights)
