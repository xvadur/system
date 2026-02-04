import os.path
import json
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

TOKEN_PATH = '/Users/_xvadur/clawd/xvadur_os_token.json'
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

def list_recent_emails():
    if not os.path.exists(TOKEN_PATH):
        return "ERROR: Token file not found."
    
    creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
    service = build('gmail', 'v1', credentials=creds)
    
    # Získame posledných 5 správ
    results = service.users().messages().list(userId='me', maxResults=5, q="label:INBOX").execute()
    messages = results.get('messages', [])
    
    if not messages:
        return "Žiadne správy v doručenej pošte."
    
    output = []
    for msg in messages:
        txt = service.users().messages().get(userId='me', id=msg['id']).execute()
        payload = txt.get('payload')
        headers = payload.get('headers')
        
        subject = "Bez predmetu"
        sender = "Neznámy"
        for h in headers:
            if h['name'] == 'Subject':
                subject = h['value']
            if h['name'] == 'From':
                sender = h['value']
        
        output.append({"from": sender, "subject": subject})
    
    return output

if __name__ == '__main__':
    print(json.dumps(list_recent_emails(), indent=2, ensure_ascii=False))
