import requests
import re
import json
import time
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os
AIRTABLE_PAT = os.environ.get("AIRTABLE_PAT", "")
BASE_ID = "appiQMfbNFuUNbt0s"
TABLE_NAME = "zubary"

# Keywords for dental professional names in Slovakia/Czechia
NAME_REGEX = r'(?:MUDr\.|MDDr\.|Dr\.)\s+([A-Z][a-zčšžýáíéöü]+(?:\s+[A-Z][a-zčšžýáíéöü]+)+)'

def get_airtable_records():
    url = f"https://api.airtable.com/v0/{BASE_ID}/{TABLE_NAME}"
    headers = {"Authorization": f"Bearer {AIRTABLE_PAT}"}
    all_records = []
    offset = None
    while True:
        params = {"maxRecords": 50} # Start with 50 for quality check
        if offset: params["offset"] = offset
        response = requests.get(url, headers=headers, params=params)
        data = response.json()
        all_records.extend(data.get("records", []))
        offset = data.get("offset")
        if not offset or len(all_records) >= 50: break
    return all_records

def scrape_owner_name(site_url):
    if not site_url or not site_url.startswith('http'): return None
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'}
    
    try:
        # Check Home and Contact/About
        urls_to_check = [site_url]
        home_resp = requests.get(site_url, timeout=10, headers=headers)
        if home_resp.status_code == 200:
            soup = BeautifulSoup(home_resp.text, 'html.parser')
            for a in soup.find_all('a', href=True):
                if any(k in a['href'].lower() for k in ['kontakt', 'o-nas', 'tím', 'team', 'lekari']):
                    urls_to_check.append(urljoin(site_url, a['href']))
        
        for url in list(set(urls_to_check))[:3]:
            r = requests.get(url, timeout=8, headers=headers)
            if r.status_code != 200: continue
            
            # Simple regex search for Medical titles
            found = re.findall(NAME_REGEX, r.text)
            if found:
                # Return the full title + name
                # findall returns the group, so we reconstruct
                match = re.search(r'((?:MUDr\.|MDDr\.|Dr\.)\s+[A-Z][a-zčšžýáíéöü]+(?:\s+[A-Z][a-zčšžýáíéöü]+)+)', r.text)
                if match: return match.group(0)
                
    except: pass
    return None

def update_airtable(record_id, name):
    url = f"https://api.airtable.com/v0/{BASE_ID}/{TABLE_NAME}"
    headers = {"Authorization": f"Bearer {AIRTABLE_PAT}", "Content-Type": "application/json"}
    payload = {"records": [{"id": record_id, "fields": {"owner_info": name}}]}
    requests.patch(url, headers=headers, json=payload)

def main():
    print("Fetching 50 records for Name Enrichment...")
    records = get_airtable_records()
    
    count = 0
    for rec in records:
        fields = rec.get("fields", {})
        website = fields.get("website")
        if website and not fields.get("owner_info"):
            print(f"Scraping {website} for owner...")
            name = scrape_owner_name(website)
            if name:
                print(f"  Found: {name}")
                update_airtable(rec["id"], name)
                count += 1
            else:
                print("  No name found.")
            time.sleep(0.5)
            
    print(f"Enrichment done. Added {count} names.")

if __name__ == "__main__":
    main()
