import os.path
import json
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/gmail.modify']
TOKEN_PATH = '/Users/_xvadur/clawd/gmail_token.json'
CREDS_PATH = '/Users/_xvadur/clawd/gmail_credentials.json'

def verify():
    creds = None
    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            return "TOKEN_MISSING"
            
    service = build('gmail', 'v1', credentials=creds)
    results = service.users().labels().list(userId='me').execute()
    return results.get('labels', [])

if __name__ == '__main__':
    result = verify()
    print(json.dumps(result))
