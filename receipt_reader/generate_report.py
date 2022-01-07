from . import receipt_scanner
from . import receipt_analyser

import argparse

def generate_report(image_path, is_comma_decimal, output_dir):
    receipt_text = receipt_scanner.read_receipt_from_image(image_path)

    items = receipt_analyser.get_items(receipt_text, is_comma_decimal)
    item_data = receipt_analyser.get_item_data(items, is_comma_decimal)
    report_path = receipt_analyser.generate_report(item_data, output_dir)
    print("Generated report for {image} at {report_path}".format(image=image_path, report_path=report_path))
    return report_path

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", required=True, help="Path to the image to be scanned")
    ap.add_argument('--commaDecimal', dest='commaDecimal', action='store_true', default=False,
                    help="If the decimal point is represented by a comma")
    ap.add_argument("-o", "--output", required=True, help="Path to the output directory of the report")
    args = vars(ap.parse_args())

    generate_report(args["image"], args["commaDecimal"], args["output"])

