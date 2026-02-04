import sqlite3
import os
import json
import re
from datetime import datetime, timedelta

DB_PATH = os.path.expanduser("~/Library/Messages/chat.db")
LOG_FILE = "/Users/_xvadur/clawd/memory/daily_logs.json"

def clean_binary(data):
    try:
        # Hľadáme text medzi SLSP a dátumom
        raw = data.decode('utf-16', errors='ignore')
        match = re.search(r"(SLSP.*?)\d{2}\.\d{2}\.\d{4}", raw)
        if match:
            return match.group(0).replace('\x00', '')
        return None
    except:
        return None

def sync_expenses():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Hľadáme správy za posledných 24 hodín
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d 00:00:00")
    
    query = """
    SELECT attributedBody, datetime(date/1000000000 + 978307200, 'unixepoch', 'localtime') as date
    FROM message 
    JOIN handle ON message.handle_id = handle.ROWID 
    WHERE handle.id LIKE '%SLSP%'
    AND datetime(message.date/1000000000 + 978307200, 'unixepoch', 'localtime') > ?
    ORDER BY message.date DESC;
    """
    
    cursor.execute(query, (yesterday,))
    rows = cursor.fetchall()
    conn.close()

    new_expenses = []
    for row in rows:
        body, date = row
        clean_text = clean_binary(body)
        
        if clean_text:
            # Extrakcia sumy
            suma_match = re.search(r"Suma:\s*([\d,]+\s*EUR)", clean_text)
            suma = suma_match.group(1) if suma_match else "Neznáma"
            
            # Extrakcia obchodníka (zjednodušene)
            parts = clean_text.split('\n')
            merchant = parts[-2] if len(parts) > 1 else "Neznámy"

            new_expenses.append({
                "timestamp": date,
                "activity": f"Expense: {merchant}",
                "category": "SURVIVAL",
                "energy": 5,
                "note": clean_text.strip(),
                "xp": 5,
                "amount": suma
            })

    # Uloženie do daily_logs.json
    if new_expenses:
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, "r") as f:
                logs = json.load(f)
        else:
            logs = []
        
        # Pridáme len tie, ktoré tam ešte nie sú (podľa timestampu)
        existing_timestamps = [l.get("timestamp") for l in logs]
        added_count = 0
        for e in new_expenses:
            if e["timestamp"] not in existing_timestamps:
                logs.append(e)
                added_count += 1
        
        with open(LOG_FILE, "w", encoding="utf-8") as f:
            json.dump(logs, f, indent=2, ensure_ascii=False)
        
        print(f"Synchronizovaných {added_count} nových výdavkov.")

if __name__ == "__main__":
    sync_expenses()
