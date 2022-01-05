import os
import re
from datetime import date
import string
import random
import json

PRICE_REGEX_EU = "(\d+,\d{1,2})"
PRICE_REGEX_GLOBAL = "(\d+\.\d{1,2})"

QUANTITY_REGEX = "(\d+(g|kg|KG|ml|l|kpl|KPL))"

def is_line_not_empty(line):
    if line and line.strip():
        return True
    return False

def is_item_in_line(line, is_comma_decimal):
    if is_line_not_empty(line):
        if is_comma_decimal:
            return re.search(PRICE_REGEX_EU, line)
        else:
            return re.search(PRICE_REGEX_GLOBAL, line)

def get_items(receipt_text, is_comma_decimal):
    items = []
    for line in receipt_text.splitlines():
        if is_item_in_line(line, is_comma_decimal):
            items.append(line)
    return items

class ReceiptItem:
    def __init__(self, item_str, is_comma_decimal):
        if is_comma_decimal:
            price_regex = PRICE_REGEX_EU
        else:
            price_regex = PRICE_REGEX_GLOBAL

        item_price = re.findall(price_regex, item_str)[0]
        description = item_str.split(item_price)[0]
        if is_comma_decimal:
            item_price = item_price.replace(",", ".")
        self.price = float(item_price)

        item_quantity = re.findall(QUANTITY_REGEX, description)
        if len(item_quantity) == 0:
            self.quantity = None
        else:
            self.quantity = item_quantity[0]

        if self.quantity is not None:
            self.name = description.split(self.quantity[0])[0]
        else:
            self.name = description

def get_item_data(items, is_comma_decimal):
    item_data = []
    for item in items:
        item_data.append(ReceiptItem(item, is_comma_decimal))
    return item_data

class ReceiptAnalysis:
    def __init__(self, item_data):
        self.id = self.generate_analysis_id()
        self.date = date.today().strftime("%d.%m.%Y")
        self.subject = ""

        items = []
        for item in item_data:
            quantity_data = item.quantity
            quantity = {}
            if quantity_data is not None:
                quantity['amount'] = float(quantity_data[0].replace(quantity_data[1], ""))
                quantity['unit'] = quantity_data[1].lower()
            else:
                quantity['amount'] = 1
                quantity['unit'] = "kpl"

            item_data = {'name': item.name, 'quantity': quantity, 'price': item.price}
            items.append(item_data)
        self.items = items

    @staticmethod
    def generate_analysis_id():
        today = date.today()
        d = today.strftime("%d%m%Y")
        return d + '-' + ''.join(random.choice(string.ascii_lowercase) for i in range(3))

    def to_json(self):
        analysis_data = {'id': self.id, 'date': self.date, 'subject': self.subject, 'items': self.items}
        return json.dumps(analysis_data, indent=4, separators=(',', ': '))

def generate_report(item_data, output_dir):
    analysis = ReceiptAnalysis(item_data)
    analysis_file_name = analysis.id + ".json"
    analysis_file_path = os.path.join(output_dir, analysis_file_name)

    analysis_file = open(analysis_file_path, "w")
    analysis_file.write(analysis.to_json())
    analysis_file.close()
