import sqlite3
import os
import binascii
from datetime import datetime

# Cesta k databáze správ
DB_PATH = os.path.expanduser("~/Library/Messages/chat.db")

def get_slsp_messages():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Hľadáme správy od SLSP z dnešného dňa
        query = """
        SELECT 
            message.text, 
            message.attributedBody,
            datetime(message.date/1000000000 + 978307200, 'unixepoch', 'localtime') as date
        FROM message 
        JOIN handle ON message.handle_id = handle.ROWID 
        WHERE (handle.id LIKE '%SLSP%' OR message.text LIKE '%SLSP%')
        AND message.date/1000000000 + 978307200 > strftime('%s', '2026-01-28 00:00:00')
        ORDER BY message.date DESC;
        """
        
        cursor.execute(query)
        rows = cursor.fetchall()
        
        results = []
        for row in rows:
            text, body, date = row
            content = ""
            
            if text:
                content = text
            elif body:
                # Dekódovanie Apple "attributedBody" blobu
                # Toto je zjednodušený parser pre získanie textu z binárneho formátu
                try:
                    raw_data = body.decode('utf-16', errors='ignore')
                    # Hľadáme kľúčové slová SLSP a Suma v binárnych dátach
                    if "Suma:" in raw_data:
                        # Očistenie od binárneho bordelu vôkol
                        start_idx = raw_data.find("SLSP")
                        content = raw_data[start_idx:].split('\x00')[0]
                except:
                    content = "Nepodarilo sa dekódovať blob."
            
            if content:
                results.append({"date": date, "content": content})
        
        conn.close()
        return results
    except Exception as e:
        return [f"Error: {str(e)}"]

if __name__ == "__main__":
    messages = get_slsp_messages()
    if not messages:
        print("Dnes neboli nájdené žiadne správy od SLSP.")
    for msg in messages:
        print(f"[{msg['date']}] {msg['content']}")
