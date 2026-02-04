import sqlite3
import os
import re
from datetime import datetime, timedelta

DB_PATH = os.path.expanduser("~/Library/Messages/chat.db")

def parse_income():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    thirty_days_ago = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d %H:%M:%S")
    
    query = """
    SELECT attributedBody, datetime(date/1000000000 + 978307200, 'unixepoch', 'localtime') as date, handle.id
    FROM message 
    LEFT JOIN handle ON message.handle_id = handle.ROWID 
    WHERE datetime(message.date/1000000000 + 978307200, 'unixepoch', 'localtime') > ?
    ORDER BY message.date DESC;
    """
    
    cursor.execute(query, (thirty_days_ago,))
    rows = cursor.fetchall()
    conn.close()

    income_total = 0
    records = []

    for row in rows:
        body, date, handle_id = row
        if not body: continue
        try:
            # Try to see if it's in raw bytes first
            if b'Prijata' in body or b'Suma' in body:
                raw_text = body.decode('latin-1', errors='ignore')
                clean = "".join(i for i in raw_text if 31 < ord(i) < 127 or i in "\n\r\t")
                
                suma_match = re.search(r"Suma:\s*([\d,]+)", clean)
                acc_match = re.search(r"Protiucet:\s*([A-Z0-9]+)", clean)
                
                if suma_match:
                    amount = float(suma_match.group(1).replace(',', '.'))
                    acc = acc_match.group(1) if acc_match else "Unknown"
                    records.append({"date": date, "amount": amount, "account": acc})
                    income_total += amount
        except Exception as e:
            continue

    return records, income_total

if __name__ == '__main__':
    recs, total = parse_income()
    print(f"--- INCOME REPORT (Last 30 Days) ---")
    for r in recs:
        print(f"[{r['date']}] {r['amount']} EUR (From: {r['account']})")
    print(f"------------------------------------")
    print(f"TOTAL INCOME: {total} EUR")
