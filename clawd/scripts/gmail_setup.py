import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Ak upravíš tieto rozsahy (scopes), vymaž súbor token.json.
TOKEN_PATH = '/Users/_xvadur/clawd/gmail_token.json'
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

def setup_gmail():
    creds = None
    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                '/Users/_xvadur/clawd/gmail_credentials.json', SCOPES)
            creds = flow.run_local_server(port=8080)
        
        with open(TOKEN_PATH, 'w') as token:
            token.write(creds.to_json())

    service = build('gmail', 'v1', credentials=creds)
    results = service.users().labels().list(userId='me').execute()
    labels = results.get('labels', [])

    if not labels:
        print('Žiadne štítky nenájdené.')
    else:
        print('Pripojenie úspešné. Nájdené štítky v Gmaile:')
        for label in labels:
            print(label['name'])

if __name__ == '__main__':
    setup_gmail()
