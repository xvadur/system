import sqlite3
import os
import re
from datetime import datetime, timedelta

DB_PATH = os.path.expanduser("~/Library/Messages/chat.db")
KAROL_ACC = "SK8309000000000175233180"

def audit_karol_net():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    thirty_days_ago = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d %H:%M:%S")
    
    # We scan all messages to find both IN and OUT transfers involving Karol's account
    query = """
    SELECT attributedBody, datetime(date/1000000000 + 978307200, 'unixepoch', 'localtime') as date
    FROM message 
    WHERE datetime(message.date/1000000000 + 978307200, 'unixepoch', 'localtime') > ?
    ORDER BY message.date DESC;
    """
    
    cursor.execute(query, (thirty_days_ago,))
    rows = cursor.fetchall()
    conn.close()

    incoming = []
    outgoing = []

    for row in rows:
        body, date = row
        if not body: continue
        try:
            # Decode blob
            raw_text = body.decode('latin-1', errors='ignore')
            clean = "".join(i for i in raw_text if 31 < ord(i) < 127 or i in "\n\r\t")
            
            # 1. Check for incoming from Karol
            if "Prijata" in clean and KAROL_ACC in clean:
                suma_match = re.search(r"Suma:\s*([\d,]+)", clean)
                if suma_match:
                    amount = float(suma_match.group(1).replace(',', '.'))
                    incoming.append({"date": date, "amount": amount})
            
            # 2. Check for outgoing TO Karol
            # Standard SLSP SMS for outgoing: "Realizovana SEPA platba... Protiucet: [ACC] ... Suma: [AMT]"
            if "Realizovana" in clean and KAROL_ACC in clean:
                suma_match = re.search(r"Suma:\s*([\d,]+)", clean)
                if suma_match:
                    amount = float(suma_match.group(1).replace(',', '.'))
                    outgoing.append({"date": date, "amount": amount})
                    
        except:
            continue

    return incoming, outgoing

if __name__ == '__main__':
    inc, out = audit_karol_net()
    total_in = sum(i['amount'] for i in inc)
    total_out = sum(o['amount'] for i in out)
    
    print(f"--- KAROL NET AUDIT (Last 30 Days) ---")
    print(f"INCOMING (To Adam):")
    for i in inc:
        print(f"  [+] {i['date']}: {i['amount']} EUR")
    
    print(f"\nOUTGOING (To Karol):")
    for o in out:
        print(f"  [-] {o['date']}: {o['amount']} EUR")
        
    print(f"--------------------------------------")
    print(f"TOTAL RECEIVED:  {total_in:.2f} EUR")
    print(f"TOTAL RETURNED:  {total_out:.2f} EUR")
    print(f"NET INCOME:      {total_in - total_out:.2f} EUR")
