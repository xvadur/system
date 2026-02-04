import requests
import re
import json
import time
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os
AIRTABLE_PAT = os.environ.get("AIRTABLE_PAT", "")
BASE_ID = "appiQMfbNFuUNbt0s"
TABLE_NAME = "hotely"

# Improved email regex to catch obfuscated ones
EMAIL_REGEX = r'[a-zA-Z0-9_.+-]+(?:\s*\[at\]\s*|\s*@\s*)[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'

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
        time.sleep(0.2)
    
    return all_records

def clean_email(email):
    # Standardize
    e = email.lower().strip()
    e = e.replace(' [at] ', '@').replace('[at]', '@').replace(' (at) ', '@').replace('(at)', '@')
    e = re.sub(r'\s+', '', e)
    # Filter out common junk
    if e.endswith(('.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp')):
        return None
    if '@' not in e:
        return None
    return e

def extract_emails_from_html(soup, html_text):
    emails = []
    # 1. Standard regex from text
    found = re.findall(EMAIL_REGEX, html_text, re.IGNORECASE)
    emails.extend([clean_email(e) for e in found if clean_email(e)])
    
    # 2. mailto links
    for a in soup.find_all('a', href=True):
        if a['href'].lower().startswith('mailto:'):
            e = a['href'][7:].split('?')[0]
            cleaned = clean_email(e)
            if cleaned:
                emails.append(cleaned)
                
    return list(set(emails))

def scrape_site(site_url):
    if not site_url or not site_url.startswith('http'):
        return None
    
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
    
    try:
        # Load home page
        resp = requests.get(site_url, timeout=15, headers=headers)
        if resp.status_code != 200:
            return None
        
        soup = BeautifulSoup(resp.text, 'html.parser')
        emails = extract_emails_from_html(soup, resp.text)
        
        if emails:
            # Prefer non-generic if possible but return first
            return emails[0]
            
        # Discover contact/about pages
        links_to_crawl = []
        for a in soup.find_all('a', href=True):
            href = a['href'].lower()
            text = a.get_text().lower()
            # Look for contact keywords in URL or Link Text
            if any(k in href or k in text for k in ['kontakt', 'contact', 'about', 'o-nas', 'impressum', 'vop', 'gdPR', 'legal', 'podmienky']):
                links_to_crawl.append(urljoin(site_url, a['href']))
        
        # Unique and prioritized
        links_to_crawl = list(set(links_to_crawl))
        
        for link in links_to_crawl[:8]: # Check up to 8 discovered pages
            try:
                r = requests.get(link, timeout=10, headers=headers)
                s = BeautifulSoup(r.text, 'html.parser')
                e_list = extract_emails_from_html(s, r.text)
                if e_list:
                    return e_list[0]
            except:
                continue
                
    except Exception as e:
        print(f"  Error on {site_url}: {e}")
        
    return None

def update_airtable_batch(updates):
    url = f"https://api.airtable.com/v0/{BASE_ID}/{TABLE_NAME}"
    headers = {"Authorization": f"Bearer {AIRTABLE_PAT}", "Content-Type": "application/json"}
    for i in range(0, len(updates), 10):
        chunk = {"records": updates[i:i+10]}
        requests.patch(url, headers=headers, json=chunk)
        time.sleep(0.3)

def main():
    print("Fetching records...")
    records = get_airtable_records()
    print(f"Analyzing {len(records)} records.")
    
    updates = []
    count = 0
    
    for i, rec in enumerate(records):
        fields = rec.get("fields", {})
        website = fields.get("website")
        email_field = fields.get("email")
        
        # Force re-scan if user wants, or skip only if already has email
        if website and not email_field:
            print(f"[{i+1}/{len(records)}] Deep-scanning {website}...")
            email = scrape_site(website)
            if email:
                print(f"  √ Found: {email}")
                updates.append({"id": rec["id"], "fields": {"email": email}})
                count += 1
            else:
                print("  × No email found.")
            
            if len(updates) >= 5:
                update_airtable_batch(updates)
                updates = []
        
    if updates:
        update_airtable_batch(updates)
        
    print(f"Done. Newly discovered emails: {count}")

if __name__ == "__main__":
    main()
