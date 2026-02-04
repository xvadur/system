import os.path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from datetime import datetime, timedelta

TOKEN_PATH = '/Users/_xvadur/clawd/xvadur_os_token.json'
SCOPES = ['https://www.googleapis.com/auth/gmail.modify', 'https://www.googleapis.com/auth/calendar']
CALENDAR_ID = 'e7e36755df9e6a9ab2950dcbc1f77d9fa0dabd3ccf03597f8bc9324f4a32a668@group.calendar.google.com'

def update_emergency_event():
    creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
    service = build('calendar', 'v3', credentials=creds)
    
    # Range of today
    now = datetime.now()
    start_of_day = now.replace(hour=0, minute=0, second=0).astimezone().isoformat()
    
    events_result = service.events().list(calendarId=CALENDAR_ID, timeMin=start_of_day, q='emergency').execute()
    events = events_result.get('items', [])
    
    if not events:
        return "No emergency event found."
    
    # Get the latest one
    event = events[-1]
    event['description'] = (event.get('description', '') + "\n\nStatus: Ukončené o 01:31. Prijaté 30 EUR.").strip()
    event['end'] = {'dateTime': now.astimezone().isoformat()}
    
    updated_event = service.events().update(calendarId=CALENDAR_ID, eventId=event['id'], body=event).execute()
    return f"Event updated: {updated_event.get('htmlLink')}"

if __name__ == '__main__':
    print(update_emergency_event())
