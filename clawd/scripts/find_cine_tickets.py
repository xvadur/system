import os.path
import json
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

TOKEN_PATH = '/Users/_xvadur/clawd/xvadur_os_token.json'
SCOPES = ['https://www.googleapis.com/auth/gmail.modify', 'https://www.googleapis.com/auth/calendar']

def find_specific_tickets():
    creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
    service = build('gmail', 'v1', credentials=creds)
    
    # Rozšírené vyhľadávanie pre lístky
    query = "vstupenka OR ticket OR cinemax OR 'pan prstenov' after:2026/01/20"
    results = service.users().messages().list(userId='me', q=query, maxResults=10).execute()
    messages = results.get('messages', [])
    
    if not messages:
        return "Nenašli sa žiadne čerstvé lístky."
    
    output = []
    for msg in messages:
        m = service.users().messages().get(userId='me', id=msg['id'], format='full').execute()
        headers = m.get('payload', {}).get('headers', [])
        subject = next((h['value'] for h in headers if h['name'] == 'Subject'), "Bez predmetu")
        output.append({"id": msg['id'], "subject": subject, "snippet": m.get('snippet')})
    
    return output

if __name__ == '__main__':
    print(json.dumps(find_specific_tickets(), indent=2, ensure_ascii=False))
