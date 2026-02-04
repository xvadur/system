import os.path
import json
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

TOKEN_PATH = '/Users/_xvadur/clawd/xvadur_os_token.json'
SCOPES = ['https://www.googleapis.com/auth/gmail.modify', 'https://www.googleapis.com/auth/calendar']

LABELS = [
    'XV_LEADS', 
    'XV_BNI', 
    'XV_URGENT', 
    'XV_CONSUMPTION', 
    'XV_SOCIAL', 
    'XV_LOGISTICS', 
    'XV_PROMO'
]

def create_labels():
    creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
    service = build('gmail', 'v1', credentials=creds)
    
    # Získame existujúce labely
    results = service.users().labels().list(userId='me').execute()
    existing_names = [label['name'] for label in results.get('labels', [])]
    
    created = []
    for label_name in LABELS:
        if label_name not in existing_names:
            label_obj = {
                'name': label_name,
                'labelListVisibility': 'labelShow',
                'messageListVisibility': 'show'
            }
            service.users().labels().create(userId='me', body=label_obj).execute()
            created.append(label_name)
    
    return created

if __name__ == '__main__':
    res = create_labels()
    print(f"Vytvorené nové labely: {res}")
