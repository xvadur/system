#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Rozdelí conversations_clean_backup.jsonl podľa mesiacov.
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from collections import Counter

INPUT_FILE = Path("development/data/conversations_clean_backup.jsonl")
OUTPUT_DIR = Path("development/data/conversations_by_month")

def parse_jsonl_objects(file_path):
    """
    Parsuje JSONL súbor s multi-line JSON objektmi.
    
    Používame regex na rozdelenie súboru podľa patternu '}\n{' alebo '}\n\n{'
    (objekt končí, ďalší začína na novom riadku).
    """
    import re
    
    records = []
    
    # Načítať celý súbor (je to veľký, ale zvládneme to)
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Rozdeliť podľa patternu: '}' nasledovaný whitespace a '\n' a whitespace a '{'
    # Toto identifikuje miesta, kde jeden objekt končí a ďalší začína
    parts = re.split(r'\}\s*\n\s*\{', content)
    
    print(f"  Nájdených {len(parts)} častí (očakávaných ~1,822 objektov)")
    
    # Prvý objekt - pridať začiatočnú '{' (ak nie je už v prvej časti)
    for i, part in enumerate(parts):
        obj_num = i + 1
        if obj_num % 500 == 0:
            print(f"  Spracovaných {obj_num:,}/{len(parts)} objektov...", flush=True)
        
        try:
            # Prvý objekt - začíná s '{'
            if i == 0:
                obj_text = part.rstrip()
                # Odstrániť trailing comma ak existuje pred parsovaním
                obj_text = obj_text.rstrip().rstrip(',')
                # Ak už nezačína s '{', pridať ho
                if not obj_text.startswith('{'):
                    obj_text = '{' + obj_text
            # Posledný objekt - končí s '}'
            elif i == len(parts) - 1:
                obj_text = part.rstrip()
                # Ak už nekončí s '}', pridať ho
                if not obj_text.endswith('}'):
                    obj_text = obj_text + '}'
            # Stredné objekty - oba '{' a '}' musia byť pridané
            else:
                obj_text = '{' + part.rstrip() + '}'
            
            # Odstrániť trailing comma ak existuje
            obj_text = obj_text.rstrip().rstrip(',')
            
            # Parsovať JSON
            record = json.loads(obj_text)
            records.append(record)
            
        except json.JSONDecodeError as e:
            # Ak parsovanie zlyhá, lognúť a preskočiť (len prvých pár chýb)
            if len(records) < 10:
                print(f"  ⚠️  Chyba pri parsovaní objektu {obj_num}: {e}")
                print(f"      Dĺžka textu: {len(obj_text)} znakov")
                print(f"      Prvých 100 znakov: {obj_text[:100]}")
            continue
    
    return records


def extract_date_from_record(record):
    """Extrahuje dátum z záznamu."""
    date_str = None
    
    if 'user_prompt' in record and isinstance(record['user_prompt'], dict):
        if 'date_created' in record['user_prompt']:
            date_str = record['user_prompt']['date_created']
    
    if not date_str and 'timestamp' in record:
        date_str = record['timestamp']
    
    return date_str


def split_by_months():
    """Rozdelí súbor podľa mesiacov."""
    print("="*60)
    print("🔍 ANALÝZA A ROZDELENIE conversations_clean_backup.jsonl")
    print("="*60)
    
    if not INPUT_FILE.exists():
        print(f"❌ Súbor neexistuje: {INPUT_FILE}")
        sys.exit(1)
    
    print("\n📖 Načítavam súbor... (môže to trvať)")
    records = parse_jsonl_objects(INPUT_FILE)
    total_records = len(records)
    print(f"✅ Načítaných {total_records:,} záznamov\n")
    
    if total_records == 0:
        print("❌ Žiadne záznamy na spracovanie")
        sys.exit(1)
    
    # Analýza dátumov
    print("📅 Analyzujem dátumy...")
    months = Counter()
    valid_dates = 0
    invalid_dates = 0
    date_range = {'min': None, 'max': None}
    
    for i, record in enumerate(records):
        if (i + 1) % 500 == 0:
            print(f"  Spracovaných {i+1:,}/{total_records:,} záznamov...", flush=True)
        
        date_str = extract_date_from_record(record)
        
        if date_str:
            try:
                date_str_clean = date_str.replace('Z', '+00:00')
                dt = datetime.fromisoformat(date_str_clean)
                
                month_key = f"{dt.year}-{dt.month:02d}"
                months[month_key] += 1
                valid_dates += 1
                
                if date_range['min'] is None or dt < date_range['min']:
                    date_range['min'] = dt
                if date_range['max'] is None or dt > date_range['max']:
                    date_range['max'] = dt
                    
            except Exception:
                invalid_dates += 1
        else:
            invalid_dates += 1
    
    print(f"\n📊 ŠTATISTIKY")
    print(f"  Celkový počet záznamov: {total_records:,}")
    print(f"  Valid dátumov: {valid_dates:,}")
    print(f"  Invalid dátumov: {invalid_dates:,}")
    
    if date_range['min'] and date_range['max']:
        print(f"\n  Rozsah dátumov:")
        print(f"    Od: {date_range['min'].strftime('%Y-%m-%d')}")
        print(f"    Do: {date_range['max'].strftime('%Y-%m-%d')}")
        print(f"    Rozsah: {(date_range['max'] - date_range['min']).days} dní")
    
    print(f"\n  Rozdelenie podľa mesiacov:")
    for month in sorted(months.keys()):
        count = months[month]
        percentage = (count / valid_dates * 100) if valid_dates > 0 else 0
        print(f"    {month}: {count:,} konverzácií ({percentage:.1f}%)")
    
    # Rozdelenie podľa mesiacov
    print(f"\n✂️  ROZDELUJEM PODĽA MESIACOV...")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    month_files = {}
    month_counts = Counter()
    
    for i, record in enumerate(records):
        if (i + 1) % 500 == 0:
            print(f"  Spracovaných {i+1:,}/{total_records:,} záznamov...", flush=True)
        
        date_str = extract_date_from_record(record)
        
        if date_str:
            try:
                date_str_clean = date_str.replace('Z', '+00:00')
                dt = datetime.fromisoformat(date_str_clean)
                month_key = f"{dt.year}-{dt.month:02d}"
                
                # Otvorenie súboru pre mesiac
                if month_key not in month_files:
                    output_file = OUTPUT_DIR / f"conversations_{month_key}.jsonl"
                    month_files[month_key] = open(output_file, 'w', encoding='utf-8')
                    month_counts[month_key] = 0
                
                # Zápis ako JSONL (jeden objekt na riadok)
                month_files[month_key].write(json.dumps(record, ensure_ascii=False) + '\n')
                month_counts[month_key] += 1
                
            except Exception:
                pass
    
    # Zatvorenie súborov
    for file_handle in month_files.values():
        file_handle.close()
    
    print(f"\n✅ ROZDELENIE DOKONČENÉ!")
    print(f"\n📁 VÝSLEDKY:")
    for month in sorted(month_counts.keys()):
        count = month_counts[month]
        file_path = OUTPUT_DIR / f"conversations_{month}.jsonl"
        if file_path.exists():
            file_size = file_path.stat().st_size / (1024 * 1024)  # MB
            print(f"  {month}: {count:,} konverzácií ({file_size:.1f} MB) -> {file_path.name}")
        else:
            print(f"  {month}: {count:,} konverzácií -> {file_path.name} (CHYBÁ!)")
    
    print(f"\n✅ Všetky súbory sú v: {OUTPUT_DIR}")


if __name__ == "__main__":
    split_by_months()

