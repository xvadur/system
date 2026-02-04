import os.path
import json
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import base64

TOKEN_PATH = '/Users/_xvadur/clawd/xvadur_os_token.json'
SCOPES = ['https://www.googleapis.com/auth/gmail.modify', 'https://www.googleapis.com/auth/calendar']

def search_tickets():
    creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
    service = build('gmail', 'v1', credentials=creds)
    
    # Search for Cinemax or Pan Prstenov
    query = "Cinemax OR 'Pán prsteňov' OR 'Pan prstenov'"
    results = service.users().messages().list(userId='me', q=query, maxResults=5).execute()
    messages = results.get('messages', [])
    
    if not messages:
        return "No tickets found."
    
    output = []
    for msg in messages:
        m = service.users().messages().get(userId='me', id=msg['id']).execute()
        snippet = m.get('snippet')
        subject = next((h['value'] for h in m['payload']['headers'] if h['name'] == 'Subject'), "No Subject")
        
        # Get body for more details
        parts = m.get('payload', {}).get('parts', [])
        body = ""
        for part in parts:
            if part['mimeType'] == 'text/plain':
                body = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
        
        output.append({
            "id": msg['id'],
            "subject": subject,
            "snippet": snippet,
            "body": body
        })
    
    return output

if __name__ == '__main__':
    print(json.dumps(search_tickets(), indent=2, ensure_ascii=False))
