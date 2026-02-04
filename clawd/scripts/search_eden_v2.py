import os.path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import json

TOKEN_PATH = '/Users/_xvadur/clawd/xvadur_os_token.json'
SCOPES = ['https://www.googleapis.com/auth/gmail.modify', 'https://www.googleapis.com/auth/calendar']

def search_eden_suite():
    creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
    service = build('gmail', 'v1', credentials=creds)
    
    query = "from:'EDEN SUITE' OR 'EDEN SUITE' OR 'edensuite'"
    results = service.users().messages().list(userId='me', q=query, maxResults=10).execute()
    messages = results.get('messages', [])
    
    output = []
    for msg in messages:
        m = service.users().messages().get(userId='me', id=msg['id']).execute()
        output.append({"from": m.get('payload', {}).get('headers', []), "snippet": m.get('snippet')})
    
    return output

if __name__ == '__main__':
    print(json.dumps(search_eden_suite(), indent=2))
