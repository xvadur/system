#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Analyzuje conversations_clean_backup.jsonl a rozdelí ho podľa mesiacov.
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from collections import Counter, defaultdict

# Cesta k súboru
INPUT_FILE = Path("development/data/conversations_clean_backup.jsonl")
OUTPUT_DIR = Path("development/data/conversations_by_month")

def analyze_structure():
    """Analyzuje štruktúru súboru - prvý a posledný záznam."""
    print("="*60)
    print("📊 ANALÝZA ŠTRUKTÚRY")
    print("="*60)
    
    # Načítanie súboru - skúsime ako multi-line JSON alebo JSONL
    try:
        # Skúsime najprv ako JSONL (jeden JSON na riadok)
        with open(INPUT_FILE, 'r', encoding='utf-8') as f:
            # Prvý riadok
            first_line = f.readline().strip()
            if first_line and first_line.startswith('{'):
                try:
                    first_data = json.loads(first_line)
                    print("\n=== PRVÝ ZÁZNAM (JSONL formát) ===")
                    print(f"Kľúče: {list(first_data.keys())}")
                    if 'user_prompt' in first_data:
                        print(f"User prompt kľúče: {list(first_data['user_prompt'].keys())}")
                    if 'ai_response' in first_data:
                        print(f"AI response kľúče: {list(first_data['ai_response'].keys())}")
                except json.JSONDecodeError:
                    print("\n⚠️  Prvý riadok nie je validný JSON - súbor môže byť multi-line JSON")
            else:
                print("\n⚠️  Súbor nezačína s '{' - môže byť multi-line JSON")
    except Exception as e:
        print(f"\n❌ Chyba pri čítaní súboru: {e}")


def parse_jsonl_multiline(file_path):
    """Parsuje JSONL súbor, ktorý môže mať multi-line JSON objekty."""
    records = []
    current_obj_lines = []
    brace_count = 0
    line_num = 0
    
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line_num += 1
            stripped = line.strip()
            
            # Preskočiť úplne prázdne riadky
            if not stripped:
                continue
            
            current_obj_lines.append(line)
            
            # Počítaj zátvorky (iba v neprázdnom riadku)
            brace_count += stripped.count('{') - stripped.count('}')
            
            # Ak sme našli uzatvorený objekt (brace_count == 0 a máme nejaký obsah)
            if brace_count == 0 and current_obj_lines:
                try:
                    obj_text = ''.join(current_obj_lines)
                    record = json.loads(obj_text)
                    records.append(record)
                    current_obj_lines = []
                except json.JSONDecodeError as e:
                    # Ak je to len čiastočný objekt, pokračuj
                    if brace_count == 0:
                        # Skúsme to ako kompletný objekt - ak zlyhá, pokračuj
                        pass
                    # Preskočiť len ak máme kompletný objekt, ale je neplatný
                    if len(current_obj_lines) > 10:  # Ak máme dosť riadkov, skúsme to
                        try:
                            # Možno je to problém s trailing comma alebo podobne
                            obj_text = ''.join(current_obj_lines)
                            # Skúsme odstrániť trailing comma
                            obj_text = obj_text.rstrip().rstrip(',')
                            record = json.loads(obj_text)
                            records.append(record)
                            current_obj_lines = []
                        except:
                            # Ak stále zlyhá, reset
                            current_obj_lines = []
                            brace_count = 0
                            continue
    
    # Ak zostali nejaké riadky na konci, skúsme ich načítať
    if current_obj_lines and brace_count == 0:
        try:
            obj_text = ''.join(current_obj_lines)
            obj_text = obj_text.rstrip().rstrip(',')
            record = json.loads(obj_text)
            records.append(record)
        except:
            pass
    
    return records


def extract_date_from_record(record):
    """Extrahuje dátum z záznamu."""
    # Skús rôzne možné kľúče pre dátum
    date_str = None
    
    if 'user_prompt' in record:
        if 'date_created' in record['user_prompt']:
            date_str = record['user_prompt']['date_created']
        elif 'timestamp' in record['user_prompt']:
            date_str = record['user_prompt']['timestamp']
    
    if not date_str and 'timestamp' in record:
        date_str = record['timestamp']
    
    if not date_str and 'date' in record:
        date_str = record['date']
    
    if not date_str and 'date_created' in record:
        date_str = record['date_created']
    
    return date_str


def analyze_dates():
    """Analyzuje dátumy v súbore."""
    print("\n" + "="*60)
    print("📅 ANALÝZA DÁTUMOV")
    print("="*60)
    print("  Načítavam súbor... (môže to trvať)")
    
    # Parsovanie multi-line JSON
    records = parse_jsonl_multiline(INPUT_FILE)
    total_records = len(records)
    print(f"  ✅ Načítaných {total_records:,} záznamov\n")
    
    months = Counter()
    years = Counter()
    valid_dates = 0
    invalid_dates = 0
    sample_dates = []
    date_range = {'min': None, 'max': None}
    
    for record_num, data in enumerate(records, 1):
        if record_num % 5000 == 0:
            print(f"  Spracovaných {record_num:,}/{total_records:,} záznamov...", flush=True)
        
        date_str = extract_date_from_record(data)
        
        if date_str:
            try:
                # Normalizácia dátumového formátu
                date_str_clean = date_str.replace('Z', '+00:00')
                dt = datetime.fromisoformat(date_str_clean)
                
                month_key = f"{dt.year}-{dt.month:02d}"
                months[month_key] += 1
                years[dt.year] += 1
                valid_dates += 1
                
                # Vzorka dátumov
                if len(sample_dates) < 10:
                    sample_dates.append((record_num, date_str, month_key))
                
                # Rozsah dátumov
                if date_range['min'] is None or dt < date_range['min']:
                    date_range['min'] = dt
                if date_range['max'] is None or dt > date_range['max']:
                    date_range['max'] = dt
                    
            except Exception as e:
                invalid_dates += 1
                if invalid_dates <= 5:
                    print(f"  ⚠️  Chyba pri parsovaní dátumu v zázname {record_num}: {date_str} - {e}")
        else:
            invalid_dates += 1
            if invalid_dates <= 5:
                print(f"  ⚠️  Chýba dátum v zázname {record_num}")
    
    print(f"\n=== ŠTATISTIKY ===")
    print(f"Celkový počet záznamov: {total_records:,}")
    print(f"Valid dátumov: {valid_dates:,}")
    print(f"Invalid dátumov: {invalid_dates:,}")
    
    if date_range['min'] and date_range['max']:
        print(f"\nRozsah dátumov:")
        print(f"  Od: {date_range['min'].isoformat()}")
        print(f"  Do: {date_range['max'].isoformat()}")
        print(f"  Rozsah: {(date_range['max'] - date_range['min']).days} dní")
    
    print(f"\n=== VZORKA DÁTUMOV ===")
    for line_num, date_str, month in sample_dates:
        print(f"  Riadok {line_num}: {date_str} -> {month}")
    
    print(f"\n=== ROZDELENIE PODĽA MESIACOV ===")
    for month in sorted(months.keys()):
        count = months[month]
        percentage = (count / valid_dates * 100) if valid_dates > 0 else 0
        print(f"  {month}: {count:,} konverzácií ({percentage:.1f}%)")
    
    print(f"\n=== ROZDELENIE PODĽA ROKOV ===")
    for year in sorted(years.keys()):
        count = years[year]
        percentage = (count / valid_dates * 100) if valid_dates > 0 else 0
        print(f"  {year}: {count:,} konverzácií ({percentage:.1f}%)")
    
    return months, date_range


def split_by_months(months):
    """Rozdelí súbor podľa mesiacov."""
    print("\n" + "="*60)
    print("✂️  ROZDELENIE PODĽA MESIACOV")
    print("="*60)
    print("  Načítavam súbor... (môže to trvať)")
    
    # Parsovanie multi-line JSON
    records = parse_jsonl_multiline(INPUT_FILE)
    total_records = len(records)
    print(f"  ✅ Načítaných {total_records:,} záznamov\n")
    
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # Zostavenie month writers
    month_files = {}
    month_counts = Counter()
    
    for record_num, data in enumerate(records, 1):
        if record_num % 5000 == 0:
            print(f"  Spracovaných {record_num:,}/{total_records:,} záznamov...", flush=True)
        
        date_str = extract_date_from_record(data)
        
        if date_str:
            try:
                date_str_clean = date_str.replace('Z', '+00:00')
                dt = datetime.fromisoformat(date_str_clean)
                month_key = f"{dt.year}-{dt.month:02d}"
                
                # Otvorenie/získanie súboru pre mesiac
                if month_key not in month_files:
                    output_file = OUTPUT_DIR / f"conversations_{month_key}.jsonl"
                    month_files[month_key] = open(output_file, 'w', encoding='utf-8')
                    month_counts[month_key] = 0
                
                # Zápis do príslušného súboru (jeden JSON objekt na riadok)
                month_files[month_key].write(json.dumps(data, ensure_ascii=False) + '\n')
                month_counts[month_key] += 1
                
            except Exception:
                pass
    
    # Zatvorenie súborov
    for file_handle in month_files.values():
        file_handle.close()
    
    print(f"\n✅ Rozdelenie dokončené!")
    print(f"\n=== VÝSLEDKY ===")
    for month in sorted(month_counts.keys()):
        count = month_counts[month]
        file_path = OUTPUT_DIR / f"conversations_{month}.jsonl"
        file_size = file_path.stat().st_size / (1024 * 1024)  # MB
        print(f"  {month}: {count:,} konverzácií ({file_size:.1f} MB) -> {file_path.name}")
    
    return month_counts


def main():
    """Hlavná funkcia"""
    print("="*60)
    print("🔍 ANALÝZA conversations_clean_backup.jsonl")
    print("="*60)
    
    if not INPUT_FILE.exists():
        print(f"❌ Súbor neexistuje: {INPUT_FILE}")
        sys.exit(1)
    
    # 1. Analýza štruktúry
    analyze_structure()
    
    # 2. Analýza dátumov
    months, date_range = analyze_dates()
    
    # 3. Rozdelenie podľa mesiacov
    if months:
        # Automatické rozdelenie (pre skriptovanie)
        print("\n🚀 Automatické rozdelenie podľa mesiacov...")
        month_counts = split_by_months(months)
        print(f"\n✅ Hotovo! Súbory sú v: {OUTPUT_DIR}")
    else:
        print("\n⚠️  Neboli nájdené žiadne dátumy - nemôžem rozdeliť súbor.")


if __name__ == "__main__":
    main()

