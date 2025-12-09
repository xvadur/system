#!/usr/bin/env python3
"""
Finálna analýza dominantných tém v promptoch podľa mesiacov.
Identifikuje top 3 témy pomocou kľúčových slov a fráz špecifických pre témy.
"""

import json
import re
from pathlib import Path
from collections import Counter, defaultdict
from datetime import datetime

# Cesty k dátam
PROMPTS_SPLIT_DIR = Path("data/prompts/prompts_split")
PROMPTS_LOG_PATH = Path("xvadur/data/prompts_log.jsonl")

# Kľúčové slová pre rôzne témy (slovenčina + angličtina)
TOPIC_KEYWORDS = {
    'ai_technologie': ['ai', 'chatgpt', 'openai', 'llm', 'prompt', 'prompty', 'api', 'model', 'agent', 'automatizacia', 'n8n', 'workflow'],
    'psychologia_jung': ['jung', 'shadow', 'tien', 'archetyp', 'self', 'individuacia', 'nevedomie', 'red book'],
    'nabozenstvo_filozofia': ['boh', 'krestanstvo', 'biblia', 'genesis', 'nabozenstvo', 'modlitba', 'viera', 'sparta', 'egypt', 'civilizacia'],
    'zdravotnictvo': ['lekar', 'sestra', 'nemocnica', 'pacient', 'zdravotnictvo', 'medicina', 'urgent', 'oddelenie'],
    'biznis_projekty': ['newsletter', 'mladichlekarov', 'strategia', 'biznis', 'peniaze', 'monetizacia', 'projekt', 'firma'],
    'osobny_rozvoj': ['trauma', 'rodicia', 'mama', 'otec', 'detstvo', 'identita', 'sebareflexia', 'transformacia'],
    'depresia_frustracia': ['depresia', 'frustracia', 'odpor', 'strateny', 'neviem', 'tazko', 'piči', 'zlyhavanie'],
    'automatizacia_kod': ['automatizacia', 'code', 'script', 'git', 'github', 'pr', 'commit', 'workflow', 'qa'],
    'workspace_systemy': ['workspace', 'cursor', 'obsidian', 'mcp', 'savegame', 'loadgame', 'log', 'session'],
}

# Stop words
STOP_WORDS = {
    'a', 'aj', 'ako', 'aký', 'aká', 'aké', 'ale', 'alebo', 'ani', 'áno', 'avšak',
    'bol', 'bola', 'bolo', 'boli', 'bude', 'budem', 'budeš', 'budeme', 'by', 'byť',
    'cez', 'čo', 'do', 'dokonca', 'ešte', 'ho', 'i', 'ich', 'je', 'k', 'keď',
    'ktorý', 'ktorá', 'ktoré', 'ktorí', 'ktorú', 'ktorom', 'ktorým', 'ktorých',
    'lebo', 'ma', 'mi', 'na', 'nie', 'o', 'od', 'po', 'pre', 'pri', 'sa', 'so',
    'som', 'sú', 'tak', 'to', 'tu', 'už', 'v', 'vo', 'za', 'že',
    'ked', 'ktory', 'ktore', 'teraz', 'mam', 'sme', 'tam', 'mal', 'aby', 'toto',
    'neviem', 'chcem', 'pretoze', 'potom', 'toho', 'cize', 'mama', 'vsetko',
}


def extract_topic_keywords(text: str) -> dict:
    """Extrahuje kľúčové slová pre rôzne témy z textu."""
    if not text:
        return {}
    
    text_lower = text.lower()
    topic_scores = defaultdict(int)
    
    # Pre každú tému nájde kľúčové slová
    for topic, keywords in TOPIC_KEYWORDS.items():
        for keyword in keywords:
            # Hľadá presné slovo (nie súčasť iného slova)
            pattern = r'\b' + re.escape(keyword) + r'\b'
            matches = len(re.findall(pattern, text_lower))
            topic_scores[topic] += matches
    
    return topic_scores


def extract_meaningful_phrases(text: str, min_length: int = 4) -> list:
    """Extrahuje zmysluplné frázy (bigramy) z textu."""
    if not text:
        return []
    
    # Rozdelí na slová
    words = re.findall(r'\b\w+\b', text.lower())
    
    # Filtruje stop words a krátke slová
    meaningful_words = []
    for word in words:
        if (len(word) >= min_length and 
            word not in STOP_WORDS and
            not word.isdigit()):
            meaningful_words.append(word)
    
    # Vytvorí bigramy
    bigrams = []
    for i in range(len(meaningful_words) - 1):
        bigram = f"{meaningful_words[i]} {meaningful_words[i+1]}"
        bigrams.append(bigram)
    
    return bigrams


def identify_topics(texts: list, top_n: int = 3) -> list:
    """Identifikuje top témy na základe kľúčových slov a fráz."""
    all_topic_scores = defaultdict(int)
    all_bigrams = []
    
    for text in texts:
        # Pridá skóre pre témy
        topic_scores = extract_topic_keywords(text)
        for topic, score in topic_scores.items():
            all_topic_scores[topic] += score
        
        # Pridá bigramy
        bigrams = extract_meaningful_phrases(text)
        all_bigrams.extend(bigrams)
    
    # Počíta frekvencie bigramov
    bigram_freq = Counter(all_bigrams)
    
    # Kombinuje témy a bigramy
    results = []
    
    # Najprv témy (majú vyššiu váhu)
    for topic, score in sorted(all_topic_scores.items(), key=lambda x: x[1], reverse=True):
        if score >= 3:  # Minimálna frekvencia
            topic_name = topic.replace('_', ' ').title()
            results.append((topic_name, score * 2))
    
    # Potom top bigramy (ako fallback)
    for bigram, count in bigram_freq.most_common(10):
        if count >= 5:  # Minimálna frekvencia
            results.append((bigram, count))
    
    # Zoradiť a vrátiť top N
    results.sort(key=lambda x: x[1], reverse=True)
    return results[:top_n]


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


def analyze_monthly_topics(prompts: list) -> dict:
    """Analyzuje témy pre každý mesiac."""
    monthly_prompts = defaultdict(list)
    
    for prompt in prompts:
        date = prompt["date"]
        month_key = f"{date.year}-{date.month:02d}"
        monthly_prompts[month_key].append(prompt["text"])
    
    monthly_topics = {}
    
    for month_key, texts in monthly_prompts.items():
        # Identifikuje top 3 témy
        topics = identify_topics(texts, top_n=3)
        
        year, month = month_key.split("-")
        year = int(year)
        month = int(month)
        
        month_names = {
            1: "Január", 2: "Február", 3: "Marec", 4: "Apríl",
            5: "Máj", 6: "Jún", 7: "Júl", 8: "August",
            9: "September", 10: "Október", 11: "November", 12: "December"
        }
        
        month_name = month_names.get(month, f"Mesiac {month}")
        display_name = f"{month_name} {year}"
        
        monthly_topics[month_key] = {
            "display_name": display_name,
            "topics": topics,
        }
    
    return monthly_topics


def main():
    """Hlavná funkcia."""
    print("🔍 Analýza dominantných tém v promptoch (finálna verzia)...")
    
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
    
    # Analyzuj témy
    print("🔍 Analyzujem témy...")
    monthly_topics = analyze_monthly_topics(all_prompts)
    
    # Zobraz výsledky
    print("\n📈 Dominantné témy podľa mesiacov:")
    print("-" * 80)
    
    sorted_months = sorted(monthly_topics.keys())
    
    for month_key in sorted_months:
        data = monthly_topics[month_key]
        print(f"\n{data['display_name']}:")
        for i, (topic, score) in enumerate(data['topics'], 1):
            print(f"  {i}. {topic} (skóre: {score:.1f})")
    
    # Vytvor markdown formát
    print("\n📋 Markdown formát:")
    print("-" * 80)
    
    for month_key in sorted_months:
        data = monthly_topics[month_key]
        topics_str = " | ".join([f"{topic}" for topic, _ in data['topics']])
        print(f"| {data['display_name']} | {topics_str} |")
    
    return monthly_topics


if __name__ == "__main__":
    main()

