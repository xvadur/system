import os.path
import json
import argparse
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from datetime import datetime

TOKEN_PATH = '/Users/_xvadur/clawd/xvadur_os_token.json'
SCOPES = ['https://www.googleapis.com/auth/gmail.modify', 'https://www.googleapis.com/auth/calendar']

def debug_events(calendar_id):
    if not os.path.exists(TOKEN_PATH):
        return "ERROR: Token file not found."
    
    creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
    service = build('calendar', 'v3', credentials=creds)
    
    # Check events for today and next 14 days
    now = datetime.utcnow().isoformat() + 'Z'
    events_result = service.events().list(calendarId=calendar_id, timeMin=now,
                                        maxResults=10, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])
    return [{"summary": e.get('summary'), "start": e.get('start'), "id": e.get('id')} for e in events]

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--id', required=True)
    args = parser.parse_args()
    result = debug_events(args.id)
    print(json.dumps(result, indent=2, ensure_ascii=False))
