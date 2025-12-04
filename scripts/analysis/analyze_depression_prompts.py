#!/usr/bin/env python3
"""
Analýza promptov kategórie "Depresia/Frustrácia".
Identifikuje konkrétne prompty a extrahuje príklady, aby sme zistili prečo.
"""

import json
import re
from pathlib import Path
from collections import defaultdict, Counter
from datetime import datetime

# Cesty k dátam
PROMPTS_SPLIT_DIR = Path("data/prompts/prompts_split")
PROMPTS_LOG_PATH = Path("xvadur/data/prompts_log.jsonl")

# Kľúčové slová pre depresiu/frustráciu
DEPRESSION_KEYWORDS = ['depresia', 'frustracia', 'odpor', 'strateny', 'neviem', 'tazko', 'piči', 'zlyhavanie', 
                       'nerad', 'averzia', 'odpor', 'trapenie', 'bolest', 'smutok', 'beznadej', 'beznadejny',
                       'zlyhavam', 'neviem', 'nemozem', 'nedokazem', 'nefunguje', 'nefunguje', 'zlyhal',
                       'rozdrapit', 'chytam averziu', 'cely den je v piči', 'nič som neurobil',
                       'som strateny', 'sam', 'opusteny', 'nechcem', 'neviem co', 'neviem ako']

def extract_depression_prompts(prompts: list) -> list:
    """Extrahuje prompty, ktoré obsahujú kľúčové slová pre depresiu/frustráciu."""
    depression_prompts = []
    
    for prompt in prompts:
        text = prompt.get("text", "").lower()
        
        # Skontroluje, či obsahuje kľúčové slová
        matches = []
        for keyword in DEPRESSION_KEYWORDS:
            pattern = r'\b' + re.escape(keyword) + r'\b'
            if re.search(pattern, text):
                matches.append(keyword)
        
        if matches:
            depression_prompts.append({
                "date": prompt.get("date"),
                "text": prompt.get("text", ""),
                "matches": matches,
                "match_count": len(matches)
            })
    
    return depression_prompts

def analyze_depression_patterns(depression_prompts: list) -> dict:
    """Analyzuje vzorce v depresných promptoch."""
    # Zoskupí podľa mesiacov
    monthly_prompts = defaultdict(list)
    
    for prompt in depression_prompts:
        date = prompt["date"]
        month_key = f"{date.year}-{date.month:02d}"
        monthly_prompts[month_key].append(prompt)
    
    # Počíta najčastejšie kľúčové slová
    all_matches = []
    for prompt in depression_prompts:
        all_matches.extend(prompt["matches"])
    
    keyword_freq = Counter(all_matches)
    
    # Extrahuje príklady promptov
    examples = []
    for prompt in sorted(depression_prompts, key=lambda x: x["match_count"], reverse=True)[:20]:
        text = prompt["text"]
        # Zobrazí prvých 300 znakov
        preview = text[:300] + "..." if len(text) > 300 else text
        examples.append({
            "date": prompt["date"].strftime("%Y-%m-%d"),
            "matches": prompt["matches"],
            "preview": preview
        })
    
    return {
        "total_count": len(depression_prompts),
        "monthly_distribution": {k: len(v) for k, v in monthly_prompts.items()},
        "keyword_frequency": dict(keyword_freq.most_common(20)),
        "examples": examples
    }

def load_historical_prompts() -> list:
    """Načíta všetky historické prompty z prompts_split."""
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
    """Načíta aktuálne prompty z prompts_log.jsonl."""
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
    print("🔍 Analýza promptov kategórie 'Depresia/Frustrácia'...")
    
    # Načítaj prompty
    print("📖 Načítavam historické prompty...")
    historical_prompts = load_historical_prompts()
    print(f"✅ Načítaných {len(historical_prompts)} historických promptov")
    
    print("📖 Načítavam aktuálne prompty...")
    current_prompts = load_current_prompts()
    print(f"✅ Načítaných {len(current_prompts)} aktuálnych promptov")
    
    # Spoj všetky prompty
    all_prompts = historical_prompts + current_prompts
    print(f"📊 Celkom {len(all_prompts)} promptov")
    
    # Extrahuj depresné prompty
    print("🔍 Hľadám prompty s kľúčovými slovami depresie/frustrácie...")
    depression_prompts = extract_depression_prompts(all_prompts)
    print(f"✅ Nájdených {len(depression_prompts)} promptov s depresnými/frustračnými znakmi")
    
    # Analyzuj vzorce
    print("📊 Analyzujem vzorce...")
    analysis = analyze_depression_patterns(depression_prompts)
    
    # Zobraz výsledky
    print("\n" + "="*80)
    print("📈 VÝSLEDKY ANALÝZY")
    print("="*80)
    
    print(f"\n📊 Celkový počet promptov s depresnými/frustračnými znakmi: {analysis['total_count']}")
    print(f"📊 Percento z celkového počtu: {analysis['total_count']/len(all_prompts)*100:.1f}%")
    
    print("\n📅 Rozdelenie podľa mesiacov:")
    for month_key in sorted(analysis['monthly_distribution'].keys()):
        count = analysis['monthly_distribution'][month_key]
        print(f"  {month_key}: {count} promptov")
    
    print("\n🔑 Najčastejšie kľúčové slová:")
    for keyword, count in list(analysis['keyword_frequency'].items())[:10]:
        print(f"  - '{keyword}': {count}x")
    
    print("\n📝 Príklady promptov (top 10):")
    print("-" * 80)
    for i, example in enumerate(analysis['examples'][:10], 1):
        print(f"\n{i}. Dátum: {example['date']}")
        print(f"   Kľúčové slová: {', '.join(example['matches'][:5])}")
        print(f"   Text: {example['preview']}")
    
    return analysis

if __name__ == "__main__":
    main()

