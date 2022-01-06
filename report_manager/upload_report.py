import argparse
import os

import google_services
from googleapiclient.http import MediaFileUpload

ap = argparse.ArgumentParser()
ap.add_argument("-r", "--report", required = True, help = "Path to report")
args = vars(ap.parse_args())

def remove_translation_from_name(file_path):
    filename = os.path.basename(file_path)
    return filename.replace('-translated', '')

def upload_report(service, upload_dir_id, file_path):
    file_metadata = {
        'name': remove_translation_from_name(file_path),
        'parents': [upload_dir_id]
    }
    media = MediaFileUpload(file_path, mimetype='application/json')
    file = service.files().create(body=file_metadata,
                                        media_body=media,
                                        fields='id').execute()
    print ('File ID: %s' % file.get('id'))


gdrive_conf = google_services.get_conf()
drive_creds = google_services.authenticate(gdrive_conf)
drive_service = google_services.get_drive_service(drive_creds)
upload_report(drive_service, gdrive_conf['report_dir_id'], args["report"])
