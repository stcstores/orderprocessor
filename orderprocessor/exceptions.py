from termcolor import cprint


class ProcessOrdersError(Exception):
    def __init__(self, arg):
        self.message = self.make_message(arg)
        self.print_message = self.make_print_error(arg)
        super().__init__(self, self.message)

    def make_message(self, arg):
        raise NotImplemented

    def make_print_error(self, arg):
        return self.message

    def print_error(self):
        cprint(self.print_message, 'red', attrs=['bold'])


class OrderNumberNotFound(ProcessOrdersError):
    def make_message(self, order_number):
        return 'Order Number {} not found.'.format(order_number)


class OrderGUIDNotFound(ProcessOrdersError):
    def make_message(self, order_GUID):
        return 'Order GUID {} not found.'.format(order_GUID)

    def make_print_error(self, order_GUID):
        return 'ERROR finding Order ID.'


class OrderAlreadyProcessed(ProcessOrdersError):
    def make_message(self, order_number):
        return 'Order Number {} already processed.'.format(
            order_number)

    def make_print_error(self, order_number):
        return 'Order {} already processed'.format(order_number)


class OrderDataNotFound(ProcessOrdersError):
    def make_message(self, order_number):
        return "Order data for order {} not found".format(order_number)

    def make_print_error(self, order_number):
        return 'ERROR downloading order data for order {}'.format(order_number)


class LinnworksAPIUnavailable(ProcessOrdersError):
    message = 'linnworks.net API Unavailable.'

    def make_message(self):
        return self.message
