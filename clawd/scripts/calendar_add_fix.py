import os.path
import json
import argparse
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from datetime import datetime

TOKEN_PATH = '/Users/_xvadur/clawd/xvadur_os_token.json'
SCOPES = ['https://www.googleapis.com/auth/gmail.modify', 'https://www.googleapis.com/auth/calendar']

def add_event(summary, start_time, end_time, calendar_id='primary'):
    if not os.path.exists(TOKEN_PATH):
        print("ERROR: Token file not found.")
        return
    
    creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
    service = build('calendar', 'v3', credentials=creds)
    
    event = {
        'summary': summary,
        'start': {'dateTime': start_time, 'timeZone': 'Europe/Bratislava'},
        'end': {'dateTime': end_time, 'timeZone': 'Europe/Bratislava'},
    }
    
    try:
        created_event = service.events().insert(calendarId=calendar_id, body=event).execute()
        print(f"Event created in {calendar_id}: {created_event.get('htmlLink')}")
    except Exception as e:
        print(f"FAILED for {calendar_id}: {e}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--summary', required=True)
    parser.add_argument('--start', required=True)
    parser.add_argument('--end', required=True)
    parser.add_argument('--calendar', default='primary')
    args = parser.parse_args()
    
    add_event(args.summary, args.start, args.end, args.calendar)
