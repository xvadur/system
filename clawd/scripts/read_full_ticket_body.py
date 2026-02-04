import os.path
import json
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import base64
import re

TOKEN_PATH = '/Users/_xvadur/clawd/xvadur_os_token.json'
SCOPES = ['https://www.googleapis.com/auth/gmail.modify', 'https://www.googleapis.com/auth/calendar']

def get_email_body(msg_id):
    creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
    service = build('gmail', 'v1', credentials=creds)
    message = service.users().messages().get(userId='me', id=msg_id, format='full').execute()
    
    parts = message.get('payload', {}).get('parts', [])
    body = ""
    for part in parts:
        if part['mimeType'] == 'text/plain':
            body = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
            break
        elif part['mimeType'] == 'text/html':
             # some emails only have html. If text/plain exists, we use it.
             body = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
    
    if not body and not parts:
        # Message might not be multipart
        body_data = message.get('payload', {}).get('body', {}).get('data', '')
        if body_data:
            body = base64.urlsafe_b64decode(body_data).decode('utf-8')

    return body

if __name__ == '__main__':
    ids = ['19c0657322f49654', '19c0654c86887363', '19c065372e6ca4e4']
    for mid in ids:
        print(f"--- ID: {mid} ---")
        full_body = get_email_body(mid)
        # Search for dates like 30.01.2026 or similar patterns
        print(full_body)
