#! env/Scripts/python.exe -i

import os

from tabler import Tabler
from weights_db import WeightsDB


class UserExit(Exception):
    pass


class Main():
    @classmethod
    def get_commands(cls):
        cls.commands = {
            'ni': cls.next_item,
            'av': cls.average,
            'ci': cls.change_index,
            'rw': cls.remove_weight,
            'aw': cls.add_weight,
            'c': cls.complete}

    @classmethod
    def main(cls):
        cls.get_commands()
        cls.weights_db = WeightsDB()
        cls.inventory_lookup = cls.get_inventory_data()
        cls.update()
        cls.get_items()
        if len(cls.invalid_items) > 0:
            cls.stock_ids = list(cls.invalid_items.keys())
            cls.index = 0
            cls.get_item()
            while True:
                try:
                    cls.process_command(input('> '))
                except UserExit:
                    break
                cls.print_status()

    @classmethod
    def process_command(cls, input_string):
        tokens = input_string.split(' ')
        command = tokens[0].lower()
        args = tokens[1:]
        if command == 'exit':
            raise UserExit
        elif command in cls.commands:
            cls.commands[command](args)
        else:
            print("Command Not Found")

    @staticmethod
    def get_inventory_data():
        inventory_filename = os.path.expanduser(
                '~/desktop/linnadmin/download/linnworks_inventory.csv')
        inventory = Tabler(inventory_filename)
        inventory_data = {
            row['pkStockItemID']: {
                'stock_id': row['pkStockItemID'],
                'sku': row['SKU'],
                'title': row['ItemTitle'],
                'weight': row['Weight']} for row in inventory}
        return inventory_data

    @classmethod
    def get_item(cls, args=None):
        cls.stock_id = cls.stock_ids[cls.index]
        cls.weights = cls.invalid_items[cls.stock_id]
        cls.item_data = cls.inventory_lookup[cls.stock_id]
        cls.title = cls.item_data['title']
        cls.sku = cls.item_data['sku']
        cls.print_status()

    @classmethod
    def print_status(cls):
        print(cls.stock_id)
        print('{}: {}'.format(cls.sku, cls.title[:50]))
        print(cls.weights)

    @classmethod
    def next_item(cls, args=None):
        if cls.index < len(cls.invalid_items) - 1:
            cls.index += 1
            cls.get_item()
        else:
            print('DONE')
            cls.update()

    @classmethod
    def remove_weight(cls, weights):
        for weight in [int(w) for w in weights]:
            cls.weights_db.update_db.remove_weight(cls.stock_id, weight)
            cls.weights = cls.weights_db.update_db.get_weight_list(
                cls.stock_id)
            cls.invalid_items[cls.stock_id] = cls.weights

    @classmethod
    def add_weight(cls, weights):
        for weight in [int(w) for w in weights]:
            cls.weights_db.update_db.add_weight(cls.stock_id, weight)
            cls.weights = cls.weights_db.update_db.get_weight_list(
                cls.stock_id)
            cls.invalid_items[cls.stock_id] = cls.weights

    @classmethod
    def update(cls, args=None):
        update_count = cls.weights_db.update()
        print("Updated {}".format(update_count))

    @classmethod
    def get_items(cls, args=None):
        cls.invalid_items = cls.weights_db.get_invalid_weight_lists()
        print("{} invalid items to fix".format(len(cls.invalid_items)))

    @classmethod
    def change_index(cls, i):
        cls.index = int(i[0])
        cls.get_item()

    @classmethod
    def complete(cls, weights):
        weight = int(weights[0])
        cls.weights_db.complete_item(cls.stock_id, weight)

    @classmethod
    def average(cls, args=None):
        return int(sum(cls.weights) / len(cls.weights))

if __name__ == "__main__":
    Main.main()
