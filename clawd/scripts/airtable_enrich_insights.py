import requests
import json
import time
import os
import re
from bs4 import BeautifulSoup
AIRTABLE_PAT = os.environ.get("AIRTABLE_PAT", "")
BASE_ID = "appiQMfbNFuUNbt0s"
TABLE_NAME = "zubary"
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY", "")

def get_airtable_records():
    url = f"https://api.airtable.com/v0/{BASE_ID}/{TABLE_NAME}"
    headers = {"Authorization": f"Bearer {AIRTABLE_PAT}"}
    params = {"maxRecords": 20, "view": "Grid view"} # Start small for quality check
    response = requests.get(url, headers=headers, params=params)
    return response.json().get("records", [])

def scrape_site_text(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        r = requests.get(url, timeout=10, headers=headers)
        soup = BeautifulSoup(r.text, 'html.parser')
        # Extract title and first few paragraphs
        text = f"Title: {soup.title.string if soup.title else 'No Title'}\n"
        paragraphs = soup.find_all('p')
        text += "\n".join([p.get_text() for p in paragraphs[:5]])
        return text[:1500] # Limit to avoid token waste
    except:
        return ""

def generate_insight(clinic_name, website_text):
    prompt = f"""
Ako AI Architekt XVADUR (bývalý sanitár s 10-ročnou praxou), analyzuj tento úryvok z webu zubnej kliniky {clinic_name}.
Nájdi jeden konkrétny detail alebo slabinu v ich procese objednávania/komunikácie (napr. chýbajúci online kalendár, nutnosť volať len v určité hodiny, staromódny prístup).
Vytvor jednu krátku, údernú vetu v slovenčine, ktorú použiješ ako 'hook' v emaile. 
Veta musí začínať "Všimol som si, že..." a musí pôsobiť ako postreh experta, nie ako predajca.

Web text:
{website_text}

Insight (iba jedna veta):"""

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "google/gemini-2.0-flash-lite-preview-02-05:free",
        "messages": [{"role": "user", "content": prompt}]
    }
    
    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
        return response.json()['choices'][0]['message']['content'].strip().replace('"', '')
    except:
        return "Všimol som si vaše zameranie na modernú stomatológiu, ale proces objednávania sa zdá byť stále viazaný na obmedzené ordinačné hodiny."

def update_airtable(record_id, insight):
    url = f"https://api.airtable.com/v0/{BASE_ID}/{TABLE_NAME}"
    headers = {"Authorization": f"Bearer {AIRTABLE_PAT}", "Content-Type": "application/json"}
    payload = {"records": [{"id": record_id, "fields": {"custom_insight": insight}}]}
    requests.patch(url, headers=headers, json=payload)

def main():
    print("Zahajujem High-Level Enrichment pre XVADUR OS...")
    records = get_airtable_records()
    
    for rec in records:
        fields = rec.get("fields", {})
        website = fields.get("website")
        if website and not fields.get("custom_insight"):
            print(f"Analyzujem {fields.get('title')}...")
            site_text = scrape_site_text(website)
            if site_text:
                insight = generate_insight(fields.get('title'), site_text)
                print(f"  Generated Insight: {insight}")
                update_airtable(rec["id"], insight)
            time.sleep(1) # Safety delay
    
    print("Done. Insights uploaded to Airtable.")

if __name__ == "__main__":
    main()
