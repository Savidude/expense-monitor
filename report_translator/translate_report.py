import argparse
import json
import os

from googletrans import Translator

def get_report(path):
    f = open(path)
    data = json.load(f)
    return data

def translate_report(report, src, dest):
    items = report['items']
    item_names = []
    for item in items:
        item_names.append(item['name'])

    translator = Translator()
    translated_names = translator.translate(item_names, src=src, dest=dest)
    for translation in translated_names:
        for item in items:
            if item['name'] == translation.origin:
                item['name'] = translation.text
                break
    return report

def save_report(report, out):
    report_file_name = report['id'] + "-translated.json"
    report_file_path = os.path.join(out, report_file_name)

    report_text = json.dumps(report, indent=4, separators=(',', ': '))

    report_file = open(report_file_path, "w")
    report_file.write(report_text)
    report_file.close()
    return report_file_path

def translate_and_save(report_file_path, src, dest, output_dir):
    report_data = get_report(report_file_path)
    translated_report = translate_report(report_data, src, dest)
    translated_report_path = save_report(translated_report, output_dir)
    print("Translated report {report} from {src} to {dest} at {translated_report}"
          .format(report=report_file_path, src=src, dest=dest, translated_report=translated_report_path))
    return translated_report_path

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("-s", "--src", required=True, help="Source language of translation")
    ap.add_argument("-d", "--dest", required=True, help="Destination language of translation")
    ap.add_argument("-r", "--report", required=True, help="Path to the original report")
    ap.add_argument("-o", "--output", required=True, help="Path to the output directory of the translated report")
    args = vars(ap.parse_args())

    translate_and_save(args["report"], args["src"], args["dest"], args["output"])
