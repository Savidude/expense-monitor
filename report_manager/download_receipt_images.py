import argparse
import os
import io
import shutil
import json

from . import google_services
from googleapiclient.http import MediaIoBaseDownload

import report_manager

def get_images_in_dir(service, dir_id):
    page_token = None
    files = []
    while True:
        response = service.files().list(q="'{dir_id}' in parents".format(dir_id=dir_id),
                                        spaces='drive',
                                        fields='nextPageToken, files(id, name)',
                                        pageToken=page_token).execute()
        files.extend(response.get('files', []))
        page_token = response.get('nextPageToken', None)
        if page_token is None:
            break
    return files

def download_images(service, drive_images, download_dir):
    downloaded_image_files = os.listdir(download_dir)
    downloaded_images = []
    for image in drive_images:
        if image.get('name') not in downloaded_image_files:
            download_image(service, image.get('id'), image.get('name'), download_dir)
            downloaded_images.append(os.path.join(download_dir, image.get('name')))
    return downloaded_images

def download_image(service, image_id, image_name, download_dir):
    request = service.files().get_media(fileId=image_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    try:
        while done is False:
            status, done = downloader.next_chunk()
            print("Downloading file %s: %d%%." % (image_name, int(status.progress() * 100)))

        fh.seek(0)

        with open(os.path.join(download_dir, image_name), 'wb') as f:
            shutil.copyfileobj(fh, f)
    except:
        print("Something went wrong.")

def download_receipts(download_dir):
    gdrive_conf = google_services.get_conf()
    drive_creds = google_services.authenticate(gdrive_conf)
    drive_service = google_services.get_drive_service(drive_creds)
    images_in_dir = get_images_in_dir(drive_service, gdrive_conf['receipt_dir_id'])
    downloaded_images = download_images(drive_service, images_in_dir, download_dir)
    return downloaded_images

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("-d", "--directory", required=True, help="Path receipts should be downloaded into")
    args = vars(ap.parse_args())

    download_receipts(args["directory"])
