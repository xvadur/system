import os.path
import json
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from datetime import datetime, timedelta

TOKEN_PATH = '/Users/_xvadur/clawd/xvadur_os_token.json'
SCOPES = ['https://www.googleapis.com/auth/gmail.modify', 'https://www.googleapis.com/auth/calendar']

def get_karol_calendar_events():
    if not os.path.exists(TOKEN_PATH):
        return "ERROR: Token file not found."
    
    creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
    service = build('calendar', 'v3', credentials=creds)
    
    # Target specific secondary calendar 'Karol'
    karol_calendar_id = 'e7e36755df9e6a9ab2950dcbc1f77d9fa0dabd3ccf03597f8bc9324f4a32a668@group.calendar.google.com'
    
    # 30 days ago
    time_min = (datetime.now() - timedelta(days=30)).astimezone().isoformat()
    
    events_result = service.events().list(calendarId=karol_calendar_id, 
                                              timeMin=time_min,
                                              singleEvents=True,
                                              orderBy='startTime').execute()
    events = events_result.get('items', [])
    
    output = []
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        output.append({
            "summary": event.get('summary'),
            "start": start,
            "id": event.get('id')
        })
    
    return output

if __name__ == '__main__':
    result = get_karol_calendar_events()
    print(json.dumps(result, indent=2, ensure_ascii=False))
