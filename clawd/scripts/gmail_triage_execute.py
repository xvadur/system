import os.path
import json
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

TOKEN_PATH = '/Users/_xvadur/clawd/xvadur_os_token.json'
SCOPES = ['https://www.googleapis.com/auth/gmail.modify', 'https://www.googleapis.com/auth/calendar']

# Definícia logiky triáže (odosielatelia/kľúčové slová)
RULES = {
    'XV_BNI': ['bni-slovensko.sk', 'support@bni'],
    'XV_URGENT': ['calendly.com', 'autovignet.eu', 'google.com', 'noreply@skool.com'],
    'XV_CONSUMPTION': ['medium.com', 'beehiiv.com', 'dennikn.sk', 'itnetwork.cz', 'substack.com'],
    'XV_SOCIAL': ['linkedin.com', 'facebookmail.com', 'instagram.com'],
    'XV_LOGISTICS': ['revolut.com', 'shopify.com', 'gls-slovakia.sk', 'packeta.sk', 'dpd.sk'],
    'XV_PROMO': ['smarty.sk', 'totosport.sk', 'lidl.sk', 'newsletter']
}

def execute_triage(limit=100):
    creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
    service = build('gmail', 'v1', credentials=creds)
    
    # 1. Získanie ID labelov, aby sme mohli používať ich mená
    labels_res = service.users().labels().list(userId='me').execute()
    label_map = {l['name']: l['id'] for l in labels_res.get('labels', [])}
    
    # 2. Získanie správ z Inboxu
    results = service.users().messages().list(userId='me', maxResults=limit, q="label:INBOX").execute()
    messages = results.get('messages', [])
    
    if not messages:
        print("Inbox je prázdny.")
        return

    print(f"Začínam triáž {len(messages)} mailov...")
    
    for msg in messages:
        m = service.users().messages().get(userId='me', id=msg['id'], format='metadata', metadataHeaders=['From', 'Subject']).execute()
        headers = m.get('payload', {}).get('headers', [])
        sender = next((h['value'].lower() for h in headers if h['name'] == 'From'), "")
        
        target_label = None
        for category, triggers in RULES.items():
            if any(trigger in sender for trigger in triggers):
                target_label = category
                break
        
        if target_label and target_label in label_map:
            # Ak sme našli kategóriu, pridáme label a ODOBERIEME Inbox (Archivujeme)
            body = {
                'addLabelIds': [label_map[target_label]],
                'removeLabelIds': ['INBOX']
            }
            service.users().messages().modify(userId='me', id=msg['id'], body=body).execute()
            print(f"Otagované: {sender} -> {target_label}")

if __name__ == '__main__':
    execute_triage(limit=500)
