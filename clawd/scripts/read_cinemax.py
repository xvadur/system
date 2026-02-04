import os.path
import json
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import base64
from datetime import datetime

TOKEN_PATH = '/Users/_xvadur/clawd/xvadur_os_token.json'
SCOPES = ['https://www.googleapis.com/auth/gmail.modify', 'https://www.googleapis.com/auth/calendar']

def get_cinemax_details():
    creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
    service = build('gmail', 'v1', credentials=creds)
    
    # Search for exactly the sender we saw earlier
    query = "from:vstupenka@cine-max.sk"
    results = service.users().messages().list(userId='me', q=query, maxResults=5).execute()
    messages = results.get('messages', [])
    
    if not messages:
        return "Nenašli sa žiadne lístky od Cinemax."
    
    details = []
    for msg in messages:
        m = service.users().messages().get(userId='me', id=msg['id']).execute()
        snippet = m.get('snippet')
        
        # Check snippet for dates/times
        details.append({
            "id": msg['id'],
            "snippet": snippet
        })
    
    return details

if __name__ == '__main__':
    res = get_cinemax_details()
    print(json.dumps(res, indent=2, ensure_ascii=False))
