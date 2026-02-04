import os.path
import json
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from datetime import datetime, timedelta

TOKEN_PATH = '/Users/_xvadur/clawd/xvadur_os_token.json'
SCOPES = ['https://www.googleapis.com/auth/gmail.modify', 'https://www.googleapis.com/auth/calendar']

def add_tickets():
    creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
    service = build('calendar', 'v3', credentials=creds)
    
    events = [
        {
            'summary': 'Kino: Pán prsteňov: Spoločenstvo Prsteňa',
            'location': 'KINO BORY MALL BRATISLAVA',
            'description': 'Sála E, Rad 6, Miesto 13. (Vstupenka v Gmaile)',
            'start': {'dateTime': '2026-01-30T19:00:00+01:00'},
            'end': {'dateTime': '2026-01-30T22:30:00+01:00'}
        },
        {
            'summary': 'Kino: Pán prsteňov: Dve veže',
            'location': 'KINO BORY MALL BRATISLAVA',
            'description': 'Sála E, Rad 5, Miesto 11. (Vstupenka v Gmaile)',
            'start': {'dateTime': '2026-01-31T19:00:00+01:00'},
            'end': {'dateTime': '2026-01-31T22:30:00+01:00'}
        },
        {
            'summary': 'Kino: Pán prsteňov: Návrat kráľa',
            'location': 'KINO BORY MALL BRATISLAVA',
            'description': 'Sála E, Rad 5, Miesto 10. (Vstupenka v Gmaile)',
            'start': {'dateTime': '2026-02-01T18:20:00+01:00'},
            'end': {'dateTime': '2026-02-01T21:50:00+01:00'}
        }
    ]

    links = []
    for e in events:
        event = service.events().insert(calendarId='primary', body=e).execute()
        links.append(event.get('htmlLink'))
    
    return links

if __name__ == '__main__':
    res = add_tickets()
    print(f"Lístky zapísané do kalendára: {len(res)} udalostí.")
