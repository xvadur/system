import os.path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import json

TOKEN_PATH = '/Users/_xvadur/clawd/xvadur_os_token.json'
SCOPES = ['https://www.googleapis.com/auth/gmail.modify', 'https://www.googleapis.com/auth/calendar']

def search_eden_login():
    creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
    service = build('gmail', 'v1', credentials=creds)
    
    query = "Eden OR 'Eden Suite' OR 'edenai'"
    results = service.users().messages().list(userId='me', q=query, maxResults=20).execute()
    messages = results.get('messages', [])
    
    if not messages:
        return "No Eden emails found."
    
    output = []
    for msg in messages:
        m = service.users().messages().get(userId='me', id=msg['id']).execute()
        snippet = m.get('snippet')
        if "http" in snippet:
            output.append({"snippet": snippet})
    
    return output

if __name__ == '__main__':
    print(json.dumps(search_eden_login(), indent=2))
