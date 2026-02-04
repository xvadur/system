import os.path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

TOKEN_PATH = '/Users/_xvadur/clawd/xvadur_os_token.json'
SCOPES = ['https://www.googleapis.com/auth/gmail.modify', 'https://www.googleapis.com/auth/calendar']

def count_labeled_messages():
    creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
    service = build('gmail', 'v1', credentials=creds)
    
    results = service.users().labels().list(userId='me').execute()
    labels = results.get('labels', [])
    
    xv_labels = [l for l in labels if l['name'].startswith('XV_')]
    
    print("XVADUR Label Status:")
    for label in xv_labels:
        l_info = service.users().labels().get(userId='me', id=label['id']).execute()
        total = l_info.get('messagesTotal', 0)
        unread = l_info.get('messagesUnread', 0)
        print(f"{label['name']}: Total={total}, Unread={unread}")

if __name__ == '__main__':
    count_labeled_messages()
