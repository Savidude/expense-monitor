import argparse
import json

ap = argparse.ArgumentParser()
ap.add_argument("-r", "--report", required = True, help = "Path to the report")
args = vars(ap.parse_args())

def get_report(path):
    f = open(path)
    data = json.load(f)
    return data

def calculate_price_total(report):
    items = report['items']
    total = 0
    for item in items:
        total += item['price']
    return total

def get_report_summary(report):
    summary = "Date: {date}\n" \
              "Subject: {subject}\n" \
              "Total: {total}"\
        .format(date=report['date'], subject=report['subject'], total=calculate_price_total(report))
    return summary

report_data = get_report(args["report"])
report_summary = get_report_summary(report_data)
print(report_summary)
