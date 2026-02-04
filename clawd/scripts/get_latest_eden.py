import os.path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import json

TOKEN_PATH = '/Users/_xvadur/clawd/xvadur_os_token.json'
SCOPES = ['https://www.googleapis.com/auth/gmail.modify', 'https://www.googleapis.com/auth/calendar']

def get_latest_eden():
    creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
    service = build('gmail', 'v1', credentials=creds)
    
    query = "Eden"
    results = service.users().messages().list(userId='me', q=query, maxResults=5).execute()
    messages = results.get('messages', [])
    
    output = []
    for msg in messages:
        m = service.users().messages().get(userId='me', id=msg['id']).execute()
        output.append({"subject": next((h['value'] for h in m['payload']['headers'] if h['name'] == 'Subject'), "No Subject"), "snippet": m.get('snippet')})
    
    return output

if __name__ == '__main__':
    print(json.dumps(get_latest_eden(), indent=2))
