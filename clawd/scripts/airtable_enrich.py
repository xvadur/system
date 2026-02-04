import requests
import re
import json
import time
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import os
AIRTABLE_PAT = os.environ.get("AIRTABLE_PAT", "")
BASE_ID = "appiQMfbNFuUNbt0s"
TABLE_NAME = "hotely"

EMAIL_REGEX = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'

def get_airtable_records():
    url = f"https://api.airtable.com/v0/{BASE_ID}/{TABLE_NAME}"
    headers = {"Authorization": f"Bearer {AIRTABLE_PAT}"}
    all_records = []
    offset = None
    
    while True:
        params = {}
        if offset:
            params["offset"] = offset
        
        response = requests.get(url, headers=headers, params=params)
        data = response.json()
        all_records.extend(data.get("records", []))
        
        offset = data.get("offset")
        if not offset:
            break
        time.sleep(0.2) # Rate limit
    
    return all_records

def find_email_on_page(url):
    try:
        response = requests.get(url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
        if response.status_code != 200:
            return None
        
        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.get_text()
        emails = re.findall(EMAIL_REGEX, text)
        
        # Look in mailto links
        for a in soup.find_all('a', href=True):
            if a['href'].startswith('mailto:'):
                emails.append(a['href'].replace('mailto:', '').split('?')[0])
        
        # Clean and filter
        valid_emails = []
        for e in emails:
            e = e.strip().lower()
            if e and not e.endswith(('.png', '.jpg', '.jpeg', '.gif', '.svg')) and '@' in e:
                valid_emails.append(e)
        
        return list(set(valid_emails))[0] if valid_emails else None
    except:
        return None

def scrape_clinic(site_url):
    if not site_url or not site_url.startswith('http'):
        return None
        
    email = find_email_on_page(site_url)
    if email:
        return email
        
    # If not found on home page, try contact page
    try:
        response = requests.get(site_url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(response.text, 'html.parser')
        contact_links = []
        for a in soup.find_all('a', href=True):
            href = a['href'].lower()
            if 'kontakt' in href or 'contact' in href:
                contact_links.append(urljoin(site_url, a['href']))
        
        for link in list(set(contact_links))[:3]: # Limit to first 3 contact links
            email = find_email_on_page(link)
            if email:
                return email
    except:
        pass
        
    return None

def update_airtable_batch(updates):
    url = f"https://api.airtable.com/v0/{BASE_ID}/{TABLE_NAME}"
    headers = {
        "Authorization": f"Bearer {AIRTABLE_PAT}",
        "Content-Type": "application/json"
    }
    
    # Process in chunks of 10
    for i in range(0, len(updates), 10):
        chunk = updates[i:i+10]
        payload = {"records": chunk}
        response = requests.patch(url, headers=headers, json=payload)
        if response.status_code != 200:
            print(f"Error updating batch: {response.text}")
        time.sleep(0.5)

def main():
    print("Fetching records...")
    records = get_airtable_records()
    print(f"Found {len(records)} records.")
    
    updates = []
    count = 0
    
    for i, rec in enumerate(records):
        fields = rec.get("fields", {})
        website = fields.get("website")
        existing_email = fields.get("email")
        
        if website and not existing_email:
            print(f"[{i+1}/{len(records)}] Scraping {website}...")
            email = scrape_clinic(website)
            if email:
                print(f"  Found: {email}")
                updates.append({
                    "id": rec["id"],
                    "fields": {"email": email}
                })
                count += 1
            else:
                print("  No email found.")
            
            # Periodically update to avoid data loss if interrupted
            if len(updates) >= 10:
                print(f"Updating batch of {len(updates)} records...")
                update_airtable_batch(updates)
                updates = []
        
    if updates:
        print(f"Updating final batch of {len(updates)} records...")
        update_airtable_batch(updates)
        
    print(f"Done! Updated {count} records with emails.")

if __name__ == "__main__":
    main()
