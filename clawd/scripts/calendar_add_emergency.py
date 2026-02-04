import os.path
import json
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from datetime import datetime, timedelta

TOKEN_PATH = '/Users/_xvadur/clawd/xvadur_os_token.json'
SCOPES = ['https://www.googleapis.com/auth/gmail.modify', 'https://www.googleapis.com/auth/calendar']
CALENDAR_ID = 'e7e36755df9e6a9ab2950dcbc1f77d9fa0dabd3ccf03597f8bc9324f4a32a668@group.calendar.google.com'

def add_emergency_visit():
    creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
    service = build('calendar', 'v3', credentials=creds)
    
    now = datetime.now()
    end_time = now + timedelta(hours=1)
    
    event = {
      'summary': 'karol (emergency)',
      'description': 'Akútna návšteva - kontrola nefrostómií, prevencia hydronefrózy.',
      'start': {
        'dateTime': now.astimezone().isoformat(),
      },
      'end': {
        'dateTime': end_time.astimezone().isoformat(),
      },
    }
    
    event = service.events().insert(calendarId=CALENDAR_ID, body=event).execute()
    return event.get('htmlLink')

if __name__ == '__main__':
    link = add_emergency_visit()
    print(f"Emergency visit added: {link}")
