import receipt_scanner
import receipt_analyser

import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True, help = "Path to the image to be scanned")
ap.add_argument('--commaDecimal', dest='commaDecimal', action='store_true', default=False,
                help = "If the decimal point is represented by a comma")
ap.add_argument("-o", "--output", required = True, help = "Path to the output directory of the report")
args = vars(ap.parse_args())

is_comma_decimal = args["commaDecimal"]

receipt_text = receipt_scanner.read_receipt_from_image(args["image"])

items = receipt_analyser.get_items(receipt_text, is_comma_decimal)
item_data = receipt_analyser.get_item_data(items, is_comma_decimal)
receipt_analyser.generate_report(item_data, args["output"])
