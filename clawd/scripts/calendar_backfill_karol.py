import os.path
import json
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from datetime import datetime

TOKEN_PATH = '/Users/_xvadur/clawd/xvadur_os_token.json'
SCOPES = ['https://www.googleapis.com/auth/gmail.modify', 'https://www.googleapis.com/auth/calendar']
CALENDAR_ID = 'e7e36755df9e6a9ab2950dcbc1f77d9fa0dabd3ccf03597f8bc9324f4a32a668@group.calendar.google.com'

def add_missing_karol_visits(dates):
    if not os.path.exists(TOKEN_PATH):
        return "ERROR: Token file not found."
    
    creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
    service = build('calendar', 'v3', credentials=creds)
    
    created_events = []
    for date_str in dates:
        event = {
          'summary': 'karol',
          'start': {
            'date': date_str,
          },
          'end': {
            'date': date_str,
          },
        }
        ev = service.events().insert(calendarId=CALENDAR_ID, body=event).execute()
        created_events.append(date_str)
    
    return created_events

if __name__ == '__main__':
    # Dates identified from payments but missing in calendar
    missing_dates = [
        "2026-01-27",
        "2026-01-22",
        "2026-01-09",
        "2026-01-08",
        "2026-01-07",
        "2026-01-06",
        "2026-01-05",
        "2026-01-04",
        "2026-01-03",
        "2026-01-02",
        "2026-01-01"
    ]
    res = add_missing_karol_visits(missing_dates)
    print(f"Doplnené návštevy do kalendára: {res}")
