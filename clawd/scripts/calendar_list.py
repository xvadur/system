import os.path
import json
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

TOKEN_PATH = '/Users/_xvadur/clawd/xvadur_os_token.json'
SCOPES = ['https://www.googleapis.com/auth/gmail.modify', 'https://www.googleapis.com/auth/calendar']

def list_calendars():
    if not os.path.exists(TOKEN_PATH):
        return "ERROR: Token file not found."
    
    creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
    service = build('calendar', 'v3', credentials=creds)
    
    calendar_list = service.calendarList().list().execute()
    return [{"summary": c.get('summary'), "id": c.get('id')} for c in calendar_list.get('items', [])]

if __name__ == '__main__':
    result = list_calendars()
    print(json.dumps(result, indent=2, ensure_ascii=False))
