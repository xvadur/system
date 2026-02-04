import os.path
import json
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

TOKEN_PATH = '/Users/_xvadur/clawd/xvadur_os_token.json'
SCOPES = ['https://www.googleapis.com/auth/gmail.modify', 'https://www.googleapis.com/auth/calendar']

def scan_inbox(limit=100):
    if not os.path.exists(TOKEN_PATH):
        return "ERROR: Token file not found."
    
    creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
    service = build('gmail', 'v1', credentials=creds)
    
    # Získame ID správ z doručenej pošty
    results = service.users().messages().list(userId='me', maxResults=limit, q="label:INBOX").execute()
    messages = results.get('messages', [])
    
    if not messages:
        return "Inbox je prázdny."
    
    scan_results = []
    for msg in messages:
        m = service.users().messages().get(userId='me', id=msg['id'], format='metadata', metadataHeaders=['From', 'Subject']).execute()
        headers = m.get('payload', {}).get('headers', [])
        
        subject = "Bez predmetu"
        sender = "Neznámy"
        for h in headers:
            if h['name'] == 'Subject': subject = h['value']
            if h['name'] == 'From': sender = h['value']
        
        scan_results.append({
            "id": msg['id'],
            "from": sender,
            "subject": subject,
            "snippet": m.get('snippet')
        })
    
    return scan_results

if __name__ == '__main__':
    data = scan_inbox()
    # Uložíme surový sken pre Jarvisovu analýzu
    with open('/Users/_xvadur/clawd/memory/gmail_discovery_raw.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Sken dokončený. Spracovaných {len(data)} mailov.")
