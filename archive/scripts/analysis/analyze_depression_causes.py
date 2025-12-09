#!/usr/bin/env python3
"""
Detailná analýza príčin "depresie" v promptoch.
Rozlišuje medzi skutočnou depresiou, frustráciou z práce a neistotou.
"""

import json
import re
from pathlib import Path
from collections import defaultdict, Counter
from datetime import datetime

PROMPTS_SPLIT_DIR = Path("data/prompts/prompts_split")
PROMPTS_LOG_PATH = Path("xvadur/data/prompts_log.jsonl")

# Kategórie kľúčových slov
UNCERTAINTY_KEYWORDS = ['neviem', 'neviem co', 'neviem ako', 'neviem ci', 'neviem preco', 'neviem kde', 
                        'neviem kedy', 'neviem ktory', 'neviem ktore', 'neviem ktora', 'neviem ktoreho',
                        'neviem ktoremu', 'neviem ktoreho', 'neviem ktoremu', 'neviem ktoreho',
                        'neviem ci', 'neviem preco', 'neviem kde', 'neviem kedy']

FRUSTRATION_KEYWORDS = ['frustracia', 'odpor', 'nefunguje', 'nemozem', 'nedokazem', 'nechcem', 
                        'tazko', 'piči', 'zlyhavanie', 'zlyhal', 'nerad', 'averzia', 'chytam averziu',
                        'cely den je v piči', 'nič som neurobil', 'nefunguje', 'nefunguje to']

DEPRESSION_KEYWORDS = ['depresia', 'smutok', 'bolest', 'beznadej', 'beznadejny', 'strateny', 'sam', 
                       'opusteny', 'osamelost', 'osamelost', 'trapenie', 'utrpenie', 'bolest',
                       'som strateny', 'som sam', 'som opusteny', 'citem sa zle', 'citem sa strateny']

def categorize_prompt(text: str) -> dict:
    """Kategorizuje prompt podľa typu depresie/frustrácie."""
    text_lower = text.lower()
    
    categories = {
        'uncertainty': 0,
        'frustration': 0,
        'depression': 0
    }
    
    # Neistota
    for keyword in UNCERTAINTY_KEYWORDS:
        pattern = r'\b' + re.escape(keyword) + r'\b'
        matches = len(re.findall(pattern, text_lower))
        categories['uncertainty'] += matches
    
    # Frustrácia
    for keyword in FRUSTRATION_KEYWORDS:
        pattern = r'\b' + re.escape(keyword) + r'\b'
        matches = len(re.findall(pattern, text_lower))
        categories['frustration'] += matches
    
    # Depresia
    for keyword in DEPRESSION_KEYWORDS:
        pattern = r'\b' + re.escape(keyword) + r'\b'
        matches = len(re.findall(pattern, text_lower))
        categories['depression'] += matches
    
    # Určí dominantnú kategóriu
    max_category = max(categories.items(), key=lambda x: x[1])
    dominant = max_category[0] if max_category[1] > 0 else None
    
    return {
        'categories': categories,
        'dominant': dominant,
        'total_score': sum(categories.values())
    }

def analyze_prompts(prompts: list) -> dict:
    """Analyzuje prompty a kategorizuje ich."""
    categorized = {
        'uncertainty': [],
        'frustration': [],
        'depression': [],
        'mixed': []
    }
    
    for prompt in prompts:
        text = prompt.get("text", "")
        analysis = categorize_prompt(text)
        
        if analysis['total_score'] == 0:
            continue
        
        prompt_data = {
            'date': prompt.get("date"),
            'text': text,
            'analysis': analysis
        }
        
        # Kategorizuje
        if analysis['dominant']:
            if analysis['categories'][analysis['dominant']] >= 2:
                categorized[analysis['dominant']].append(prompt_data)
            else:
                categorized['mixed'].append(prompt_data)
    
    return categorized

def load_historical_prompts() -> list:
    """Načíta všetky historické prompty."""
    prompts = []
    
    for day_dir in sorted(PROMPTS_SPLIT_DIR.glob("*")):
        if not day_dir.is_dir():
            continue
        
        for json_file in sorted(day_dir.glob("*.json")):
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                if not data.get("text"):
                    continue
                
                date_str = data.get("date", day_dir.name)
                try:
                    date = datetime.strptime(date_str, "%Y-%m-%d")
                except:
                    continue
                
                prompts.append({
                    "date": date,
                    "text": data.get("text", ""),
                })
            except:
                continue
    
    return prompts

def load_current_prompts() -> list:
    """Načíta aktuálne prompty."""
    prompts = []
    
    if not PROMPTS_LOG_PATH.exists():
        return prompts
    
    try:
        with open(PROMPTS_LOG_PATH, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                
                try:
                    data = json.loads(line)
                    
                    if data.get("role") != "user":
                        continue
                    
                    timestamp_str = data.get("timestamp", "")
                    try:
                        if '+' in timestamp_str or timestamp_str.endswith('Z'):
                            date = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
                        else:
                            date = datetime.fromisoformat(timestamp_str)
                    except:
                        continue
                    
                    prompts.append({
                        "date": date,
                        "text": data.get("content", ""),
                    })
                except:
                    continue
    except:
        pass
    
    return prompts

def main():
    """Hlavná funkcia."""
    print("🔍 Detailná analýza príčin 'depresie' v promptoch...")
    
    # Načítaj prompty
    print("📖 Načítavam prompty...")
    historical_prompts = load_historical_prompts()
    current_prompts = load_current_prompts()
    all_prompts = historical_prompts + current_prompts
    print(f"✅ Načítaných {len(all_prompts)} promptov")
    
    # Analyzuj
    print("🔍 Kategorizujem prompty...")
    categorized = analyze_prompts(all_prompts)
    
    # Zobraz výsledky
    print("\n" + "="*80)
    print("📈 VÝSLEDKY KATEGORIZÁCIE")
    print("="*80)
    
    total = sum(len(v) for v in categorized.values())
    
    print(f"\n📊 Celkový počet kategorizovaných promptov: {total}")
    print(f"📊 Neistota (neviem, neviem ako, neviem co): {len(categorized['uncertainty'])} ({len(categorized['uncertainty'])/total*100:.1f}%)")
    print(f"📊 Frustrácia z práce/projektov (odpor, nefunguje, nemozem): {len(categorized['frustration'])} ({len(categorized['frustration'])/total*100:.1f}%)")
    print(f"📊 Skutočná depresia (smutok, strateny, sam, opusteny): {len(categorized['depression'])} ({len(categorized['depression'])/total*100:.1f}%)")
    print(f"📊 Zmiešané (viacero kategórií): {len(categorized['mixed'])} ({len(categorized['mixed'])/total*100:.1f}%)")
    
    # Príklady
    print("\n📝 Príklady promptov - NEISTOTA (neviem, neviem ako):")
    print("-" * 80)
    for i, prompt in enumerate(categorized['uncertainty'][:5], 1):
        preview = prompt['text'][:200] + "..." if len(prompt['text']) > 200 else prompt['text']
        print(f"\n{i}. {prompt['date'].strftime('%Y-%m-%d')}: {preview}")
    
    print("\n📝 Príklady promptov - FRUSTRÁCIA (odpor, nefunguje, nemozem):")
    print("-" * 80)
    for i, prompt in enumerate(categorized['frustration'][:5], 1):
        preview = prompt['text'][:200] + "..." if len(prompt['text']) > 200 else prompt['text']
        print(f"\n{i}. {prompt['date'].strftime('%Y-%m-%d')}: {preview}")
    
    print("\n📝 Príklady promptov - SKUTOČNÁ DEPRESIA (smutok, strateny, sam):")
    print("-" * 80)
    for i, prompt in enumerate(categorized['depression'][:5], 1):
        preview = prompt['text'][:200] + "..." if len(prompt['text']) > 200 else prompt['text']
        print(f"\n{i}. {prompt['date'].strftime('%Y-%m-%d')}: {preview}")
    
    # Rozdelenie podľa mesiacov
    print("\n📅 Rozdelenie podľa mesiacov:")
    monthly = defaultdict(lambda: {'uncertainty': 0, 'frustration': 0, 'depression': 0, 'mixed': 0})
    
    for category, prompts_list in categorized.items():
        for prompt in prompts_list:
            month_key = f"{prompt['date'].year}-{prompt['date'].month:02d}"
            monthly[month_key][category] += 1
    
    for month_key in sorted(monthly.keys()):
        data = monthly[month_key]
        total_month = sum(data.values())
        print(f"\n{month_key}:")
        print(f"  Neistota: {data['uncertainty']} ({data['uncertainty']/total_month*100:.1f}%)")
        print(f"  Frustrácia: {data['frustration']} ({data['frustration']/total_month*100:.1f}%)")
        print(f"  Depresia: {data['depression']} ({data['depression']/total_month*100:.1f}%)")
        print(f"  Zmiešané: {data['mixed']} ({data['mixed']/total_month*100:.1f}%)")
    
    return categorized

if __name__ == "__main__":
    main()

