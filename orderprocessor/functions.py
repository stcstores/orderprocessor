from termcolor import cprint
import pylinnworks

from . exceptions import OrderNumberNotFound
from . exceptions import OrderGUIDNotFound
from . exceptions import OrderDataNotFound
from . exceptions import OrderAlreadyProcessed


def get_order(api_session, order_number):
    try:
        order_guid = pylinnworks.get_order_id(api_session, order_number)
    except:
        raise OrderNumberNotFound(order_number)
    order_guid = pylinnworks.get_order_id(api_session, order_number)
    if order_guid is None:
        raise OrderGUIDNotFound(order_guid)
        cprint('Error: GUID for ' + order_number + ' not found', 'red')
    get_order_request = pylinnworks.api_requests.GetOrderInfo(
        api_session, order_guid)
    order_data = get_order_request.response_dict
    if order_data['dProcessedOn'] != '0001-01-01T00:00:00':
        raise OrderAlreadyProcessed(order_number)
    try:
        order = pylinnworks.orders.OpenOrder(
            api_session, load_order_id=order_guid)
    except:
        raise OrderDataNotFound(order_number)
    return order


def process_weight(weight_database, order, completed_items):
    if len(order.items) > 1 or order.items[0].quantity > 1:
        cprint('Weight Unusable', 'green')
        return
    item = order.items[0]
    if item.stock_id in completed_items:
        cprint('Weight Done', 'green')
        return
    item_weight = input('Weight: ')
    if item_weight.isdigit():
        item_weight = int(item_weight)
        if item_weight > 0 and item_weight < 9999:
            weight_database.add_weight(
                item.stock_id, item_weight)
            cprint('Added {}g to weights for {}'.format(
                item_weight, item.title), 'cyan')
