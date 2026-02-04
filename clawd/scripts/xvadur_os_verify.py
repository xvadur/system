import os.path
import json
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from datetime import datetime

TOKEN_PATH = '/Users/_xvadur/clawd/xvadur_os_token.json'
SCOPES = ['https://www.googleapis.com/auth/gmail.modify', 'https://www.googleapis.com/auth/calendar']

def check_status():
    if not os.path.exists(TOKEN_PATH):
        return "TOKEN_NOT_FOUND"
    
    creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
    
    # Check Calendar events
    calendar_service = build('calendar', 'v3', credentials=creds)
    now = datetime.utcnow().isoformat() + 'Z'
    events_result = calendar_service.events().list(calendarId='primary', timeMin=now,
                                              maxResults=5, singleEvents=True,
                                              orderBy='startTime').execute()
    events = events_result.get('items', [])
    
    return events

if __name__ == '__main__':
    result = check_status()
    print(json.dumps(result, indent=2, ensure_ascii=False))
