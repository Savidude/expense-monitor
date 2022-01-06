import json
import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

def get_conf():
    f = open('gdrive_conf.json')
    conf = json.load(f)
    return conf

def authenticate(conf):
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', conf['scopes'])
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secrets.json', conf['scopes'])
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

def get_drive_service(creds):
    try:
        service = build('drive', 'v3', credentials=creds)
    except HttpError as error:
        print(f'An error occurred: {error}')
        service = None
    return service
