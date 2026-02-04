import os.path
import json
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

TOKEN_PATH = '/Users/_xvadur/clawd/xvadur_os_token.json'
CREDS_PATH = '/Users/_xvadur/clawd/xvadur_gmail_creds.json'
# Unified scopes for Gmail and Calendar
SCOPES = [
    'https://www.googleapis.com/auth/gmail.modify',
    'https://www.googleapis.com/auth/calendar'
]

def setup_xvadur_os():
    creds = None
    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDS_PATH, SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open(TOKEN_PATH, 'w') as token:
            token.write(creds.to_json())

    # Verify Gmail
    gmail_service = build('gmail', 'v1', credentials=creds)
    gmail_results = gmail_service.users().labels().list(userId='me').execute()
    
    # Verify Calendar
    calendar_service = build('calendar', 'v3', credentials=creds)
    calendar_list = calendar_service.calendarList().list().execute()
    
    print(f"Success. Connected to Gmail ({len(gmail_results.get('labels', []))} labels) and Calendar ({len(calendar_list.get('items', []))} calendars).")

if __name__ == '__main__':
    setup_xvadur_os()
