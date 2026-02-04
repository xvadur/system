import os.path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import json

TOKEN_PATH = '/Users/_xvadur/clawd/xvadur_os_token.json'
SCOPES = ['https://www.googleapis.com/auth/gmail.modify', 'https://www.googleapis.com/auth/calendar']

def find_eden_link():
    if not os.path.exists(TOKEN_PATH):
        return "ERROR: Token file not found."
    
    creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
    service = build('gmail', 'v1', credentials=creds)
    
    # Search for Eden or Chris Lee or Execution
    query = "Eden OR 'Chris Lee' OR 'Execution Sprint' OR 'Elite Sprint'"
    results = service.users().messages().list(userId='me', q=query, maxResults=10).execute()
    messages = results.get('messages', [])
    
    if not messages:
        return "No relevant emails found."
    
    output = []
    for msg in messages:
        m = service.users().messages().get(userId='me', id=msg['id']).execute()
        headers = m.get('payload', {}).get('headers', [])
        subject = next((h['value'] for h in headers if h['name'] == 'Subject'), "No Subject")
        sender = next((h['value'] for h in headers if h['name'] == 'From'), "Unknown")
        output.append({"from": sender, "subject": subject, "snippet": m.get('snippet')})
    
    return output

if __name__ == '__main__':
    print(json.dumps(find_eden_link(), indent=2))
