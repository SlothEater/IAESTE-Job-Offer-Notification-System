import os.path
import base64
import re

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from src.constants.paths import TELEGRAM_BOT_TOKEN_PATH

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


def verification_code() -> str:
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                TELEGRAM_BOT_TOKEN_PATH, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    # Call the Gmail API
    service = build('gmail', 'v1', credentials=creds)
    results = (service.users().messages().list(userId='me',
                                               labelIds=['INBOX'],
                                               q="is:unread").execute())
    messages = results.get('messages', [])

    for message in messages:
        msg = service.users().messages().get(userId='me',
                                             id=message['id']).execute()

        # Get the payload of the message
        payload = msg['payload']
        headers = payload.get("headers")
        parts = payload.get("parts")[0]
        data = parts['body']['data']
        byte_code = base64.urlsafe_b64decode(data)
        text = byte_code.decode("utf-8")

        return re.search(r'code is (\d{6})', text).group(1)
