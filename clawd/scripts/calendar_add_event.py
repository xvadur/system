import os.path
import json
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from datetime import datetime

TOKEN_PATH = '/Users/_xvadur/clawd/xvadur_os_token.json'
SCOPES = ['https://www.googleapis.com/auth/gmail.modify', 'https://www.googleapis.com/auth/calendar']

def add_calendar_event():
    if not os.path.exists(TOKEN_PATH):
        return "ERROR: Token file not found."
    
    creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
    service = build('calendar', 'v3', credentials=creds)
    
    # Event details
    event = {
      'summary': 'Zakúpené Duolingo (English/Math/Chess)',
      'description': 'Začiatok 30-minútového ranného vzdelávacieho cyklu.',
      'start': {
        'date': datetime.now().strftime('%Y-%m-%d'),
      },
      'end': {
        'date': datetime.now().strftime('%Y-%m-%d'),
      },
    }

    event = service.events().insert(calendarId='primary', body=event).execute()
    return event.get('htmlLink')

if __name__ == '__main__':
    link = add_calendar_event()
    print(f"Event created: {link}")
