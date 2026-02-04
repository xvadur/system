import os.path
import base64
import json
import requests
import time
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from email.message import EmailMessage
AIRTABLE_PAT = os.environ.get("AIRTABLE_PAT", "")
BASE_ID = "appiQMfbNFuUNbt0s"
TABLE_NAME = "zubary"
TOKEN_PATH = '/Users/_xvadur/clawd/xvadur_os_token.json'
# Replace with your actual Loom/Video link
VIDEO_LINK = "https://www.loom.com/share/dab0ca16ccf64a23b18b7bff950a6c8e" 

def get_leads():
    url = f"https://api.airtable.com/v0/{BASE_ID}/{TABLE_NAME}"
    headers = {"Authorization": f"Bearer {AIRTABLE_PAT}"}
    params = {"view": "Grid view"}
    response = requests.get(url, headers=headers, params=params)
    records = response.json().get("records", [])
    return [r['fields'] for r in records if 'email' in r['fields']]

def create_draft(service, lead):
    email_address = lead.get('email')
    clinic_name = lead.get('title', 'vašu kliniku')
    owner = lead.get('owner_info', 'Dobrý deň')
    
    # Chris Lee Strategy: Tier A (Direct Value) or Tier B (Permission)
    # Using Tier B style: "Quick check + Permission for video"
    
    subject = f"Rýchla otázka - {clinic_name}"
    
    body = f"""Dobrý deň {owner if owner != 'Dobrý deň' else ''},

píšem vám krátku poznámku k zmeškaným dopytom v {clinic_name}.

Zaujímalo ma, ako riešite objednávanie u stomatológov v Bratislave a všimol som si u vás malý logistický únik, ktorý zvyčajne stojí kliniky desiatky pacientov mesačne.

Natočil som k tomu 60-sekundové video: {VIDEO_LINK}

Ak ste otvorení krátkemu rozhovoru o tom, ako u vás tento únik opraviť za 7 dní, odpíšte ÁNO a pošlem vám link na kalendár.

S pozdravom,

Adam Xvadur
XVADUR OS | AI Architekt pre zdravotníctvo"""

    message = EmailMessage()
    message.set_content(body)
    message['To'] = email_address
    message['Subject'] = subject

    # encoded message
    encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    create_message = {
        'message': {
            'raw': encoded_message
        }
    }
    
    try:
        service.users().drafts().create(userId="me", body=create_message).execute()
        return True
    except Exception as e:
        print(f"Error creating draft for {email_address}: {e}")
        return False

def main():
    creds = Credentials.from_authorized_user_file(TOKEN_PATH, ['https://www.googleapis.com/auth/gmail.modify'])
    service = build('gmail', 'v1', credentials=creds)
    
    print("Načítavam leady...")
    leads = get_leads()
    print(f"Nájdených {len(leads)} leadov s emailom.")
    
    count = 0
    # Process top 15 as requested for test
    for lead in leads[:15]:
        if create_draft(service, lead):
            print(f"√ Draft vytvorený pre: {lead.get('email')}")
            count += 1
        time.sleep(0.5)
        
    print(f"Hotovo. Celkovo vytvorených {count} draftov v Gmaile.")

if __name__ == '__main__':
    main()
