import os.path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from datetime import datetime

TOKEN_PATH = '/Users/_xvadur/clawd/xvadur_os_token.json'
SCOPES = ['https://www.googleapis.com/auth/gmail.modify', 'https://www.googleapis.com/auth/calendar']

def update_bni_all_calendars():
    creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
    service = build('calendar', 'v3', credentials=creds)
    
    now = datetime.now()
    start_of_day = now.replace(hour=0, minute=0, second=0).astimezone().isoformat()
    end_of_day = now.replace(hour=23, minute=59, second=59).astimezone().isoformat()
    
    cal_list = service.calendarList().list().execute().get('items', [])
    
    updated_any = False
    for cal in cal_list:
        cal_id = cal['id']
        events_result = service.events().list(calendarId=cal_id, timeMin=start_of_day, timeMax=end_of_day, q='BNI').execute()
        events = events_result.get('items', [])
        
        for event in events:
            existing_desc = event.get('description', '')
            new_desc = (existing_desc + "\n\nNote: Mám odtiaľ 2 leady.").strip()
            event['description'] = new_desc
            service.events().update(calendarId=cal_id, eventId=event['id'], body=event).execute()
            print(f"Updated event '{event.get('summary')}' in calendar '{cal.get('summary')}'")
            updated_any = True
            
    if not updated_any:
        print("No BNI event found in any calendar for today.")

if __name__ == '__main__':
    update_bni_all_calendars()
