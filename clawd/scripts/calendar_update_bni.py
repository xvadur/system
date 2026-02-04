import os.path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from datetime import datetime, timedelta

TOKEN_PATH = '/Users/_xvadur/clawd/xvadur_os_token.json'
SCOPES = ['https://www.googleapis.com/auth/gmail.modify', 'https://www.googleapis.com/auth/calendar']

def update_bni_event():
    creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
    service = build('calendar', 'v3', credentials=creds)
    
    # Range for today
    now = datetime.now()
    start_of_day = now.replace(hour=0, minute=0, second=0).astimezone().isoformat()
    end_of_day = now.replace(hour=23, minute=59, second=59).astimezone().isoformat()
    
    # Search for BNI in primary calendar
    events_result = service.events().list(calendarId='primary', timeMin=start_of_day, timeMax=end_of_day, q='BNI').execute()
    events = events_result.get('items', [])
    
    if not events:
        return "No BNI event found in primary calendar."
    
    # Update the first matching event found
    event = events[0]
    existing_desc = event.get('description', '')
    new_desc = (existing_desc + "\n\nNote: Mám odtiaľ 2 leady.").strip()
    
    event['description'] = new_desc
    updated_event = service.events().update(calendarId='primary', eventId=event['id'], body=event).execute()
    return f"Updated BNI event: {updated_event.get('summary')} - {updated_event.get('htmlLink')}"

if __name__ == '__main__':
    print(update_bni_event())
