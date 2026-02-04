import os.path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from datetime import datetime

TOKEN_PATH = '/Users/_xvadur/clawd/xvadur_os_token.json'
SCOPES = ['https://www.googleapis.com/auth/gmail.modify', 'https://www.googleapis.com/auth/calendar']
CALENDAR_ID = 'e7e36755df9e6a9ab2950dcbc1f77d9fa0dabd3ccf03597f8bc9324f4a32a668@group.calendar.google.com'

def find_and_update():
    creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
    service = build('calendar', 'v3', credentials=creds)
    
    # Check last few hours
    now = datetime.now()
    events_result = service.events().list(calendarId=CALENDAR_ID, maxResults=10, orderBy='startTime', singleEvents=True).execute()
    events = events_result.get('items', [])
    
    for event in reversed(events):
        if 'karol' in event.get('summary', '').lower():
            event['description'] = (event.get('description', '') + f"\n\nStatus: Completed at {now.strftime('%H:%M')}. Received 30 EUR.").strip()
            event['end'] = {'dateTime': now.astimezone().isoformat()}
            service.events().update(calendarId=CALENDAR_ID, eventId=event['id'], body=event).execute()
            return f"Found and updated: {event.get('summary')}"
    return "No Karol event found."

if __name__ == '__main__':
    print(find_and_update())
