import os

import report_manager
import receipt_reader
import report_translator

import json

def get_conf():
    f = open('conf.json')
    conf = json.load(f)
    return conf

def generate_reports(conf, downloaded_receipts):
    report_paths = []
    for receipt_image in downloaded_receipts:
        report_path = receipt_reader.generate_report.generate_report(receipt_image, conf['is-comma-decimal'],
                                                                     conf['report-output-dir'])
        report_paths.append(report_path)
    return report_paths

def translate_reports(conf, translated_reports):
    translated_paths = []
    for report_path in translated_reports:
        translated_report_path = report_translator.translate_report.translate_and_save(report_path,
                                                                                       conf['translation']['src'],
                                                                                       conf['translation']['dest'],
                                                                                conf['translated-report-output-dir'])
        translated_paths.append(translated_report_path)
    return translated_paths


if __name__ == '__main__':
    config = get_conf()
    downloaded_receipt_images = report_manager.download_receipt_images.download_receipts(config['receipt-download-dir'])
    generated_report_paths = generate_reports(config, downloaded_receipt_images)
    translated_report_paths = translate_reports(config, generated_report_paths)
    print(generated_report_paths)
