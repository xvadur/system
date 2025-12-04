#!/usr/bin/env python3
"""
Analýza rozdielov medzi Kortex backupom a historickými promptmi.
"""

import json
from pathlib import Path
from collections import defaultdict

workspace_root = Path(__file__).parent.parent

print('🔍 ANALÝZA: ČO JE V KORTEX BACKUPE, ČO NIE JE V HISTORICKÝCH?\n')

# Načítame dátumy z historických promptov
historical_dates = set()
historical_texts = set()

historical_dir = workspace_root / 'data/prompts/prompts_split'
for day_dir in historical_dir.glob('*'):
    if not day_dir.is_dir():
        continue
    for json_file in day_dir.glob('*.json'):
        try:
            with open(json_file, 'r') as f:
                data = json.load(f)
                date = data.get('date', '')
                text = data.get('text', '')[:200]
                if date:
                    historical_dates.add(date)
                if text:
                    historical_texts.add(text.lower().strip()[:100])
        except:
            pass

print(f'📊 Historické prompty:')
print(f'   {len(historical_dates)} unikátnych dátumov')
print(f'   {len(historical_texts)} unikátnych textov\n')

# Načítame z Kortex backupu
kortex_dates = set()
kortex_texts = set()
kortex_date_counts = defaultdict(int)

kortex_file = workspace_root / 'xvadur/data/kortex_guaranteed/user_prompts_guaranteed.jsonl'
if kortex_file.exists():
    with open(kortex_file, 'r') as f:
        for line in f:
            try:
                data = json.loads(line)
                date_created = data.get('date_created', '')
                text = data.get('extracted_text', '')[:200]
                
                if date_created:
                    date_only = date_created[:10]
                    kortex_dates.add(date_only)
                    kortex_date_counts[date_only] += 1
                
                if text:
                    kortex_texts.add(text.lower().strip()[:100])
            except:
                pass

print(f'📊 Kortex backup:')
print(f'   {len(kortex_dates)} unikátnych dátumov')
print(f'   {len(kortex_texts)} unikátnych textov\n')

# Porovnanie
dates_only_in_kortex = kortex_dates - historical_dates
texts_only_in_kortex = kortex_texts - historical_texts
texts_in_both = kortex_texts & historical_dates

print(f'📅 Rozdiel v dátumoch:')
print(f'   Dátumy len v Kortex backupe: {len(dates_only_in_kortex)}')
print(f'   Dátumy v oboch: {len(kortex_dates & historical_dates)}\n')

if dates_only_in_kortex:
    print(f'   Príklady dátumov len v Kortex backupe:')
    for date in sorted(list(dates_only_in_kortex))[:10]:
        count = kortex_date_counts.get(date, 0)
        print(f'     {date}: {count} promptov')

print(f'\n📝 Rozdiel v textoch:')
print(f'   Texty len v Kortex backupe: {len(texts_only_in_kortex)}')
print(f'   Texty v oboch: {len(kortex_texts & historical_texts)}')
print(f'   Pokrytie: {len(kortex_texts & historical_texts) / len(kortex_texts) * 100:.1f}% textov z Kortex backupu je aj v historických\n')

# Analyzujeme typy promptov v Kortex backupe
print('📊 ŠTATISTIKY KORTEX BACKUP PROMPTOV:\n')

lengths = []
word_counts = []
has_code = 0
has_links = 0
very_short = 0
short = 0
medium = 0
long = 0

if kortex_file.exists():
    with open(kortex_file, 'r') as f:
        for line in f:
            try:
                data = json.loads(line)
                text = data.get('extracted_text', '')
                word_count = data.get('word_count', len(text.split()))
                
                lengths.append(len(text))
                word_counts.append(word_count)
                
                if '```' in text or 'def ' in text or 'function ' in text:
                    has_code += 1
                
                if 'http' in text or 'www.' in text:
                    has_links += 1
                
                if word_count < 50:
                    very_short += 1
                elif word_count < 200:
                    short += 1
                elif word_count < 500:
                    medium += 1
                else:
                    long += 1
            except:
                pass

print(f'   Celkom: {len(word_counts)} promptov')
if word_counts:
    print(f'   Priemerná dĺžka: {sum(lengths) / len(lengths):.0f} znakov')
    print(f'   Priemerný počet slov: {sum(word_counts) / len(word_counts):.1f} slov\n')
    
    print(f'📏 Rozdelenie podľa dĺžky:')
    print(f'   Veľmi krátke (< 50 slov): {very_short} ({very_short/len(word_counts)*100:.1f}%)')
    print(f'   Krátke (50-200 slov): {short} ({short/len(word_counts)*100:.1f}%)')
    print(f'   Stredné (200-500 slov): {medium} ({medium/len(word_counts)*100:.1f}%)')
    print(f'   Dlhé (500+ slov): {long} ({long/len(word_counts)*100:.1f}%)\n')
    
    print(f'🔧 Obsah:')
    print(f'   S kódom: {has_code} ({has_code/len(word_counts)*100:.1f}%)')
    print(f'   S linkami: {has_links} ({has_links/len(word_counts)*100:.1f}%)')

