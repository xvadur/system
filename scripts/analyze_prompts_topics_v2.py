#!/usr/bin/env python3
"""
Analýza dominantných tém v promptoch podľa mesiacov - vylepšená verzia.
Identifikuje top 3 témy pomocou bigramov/trigramov a lepšieho filtrovania.
"""

import json
import re
from pathlib import Path
from collections import Counter, defaultdict
from datetime import datetime

# Cesty k dátam
PROMPTS_SPLIT_DIR = Path("data/prompts/prompts_split")
PROMPTS_LOG_PATH = Path("xvadur/data/prompts_log.jsonl")

# Rozšírené stop words (vrátane slovenských slov)
STOP_WORDS = {
    # Slovenské stop words
    'a', 'aj', 'ako', 'aký', 'aká', 'aké', 'akú', 'akom', 'akým', 'ale', 'alebo', 'ani',
    'áno', 'avšak', 'bol', 'bola', 'bolo', 'boli', 'bude', 'budem', 'budeš', 'budeme',
    'by', 'byť', 'cez', 'čo', 'do', 'dokonca', 'ešte', 'ho', 'i', 'ich', 'je', 'k',
    'keď', 'ktorý', 'ktorá', 'ktoré', 'ktorí', 'ktorú', 'ktorom', 'ktorým', 'ktorých',
    'lebo', 'ma', 'mi', 'na', 'nie', 'o', 'od', 'po', 'pre', 'pri', 'sa', 'so', 'som',
    'sú', 'tak', 'to', 'tu', 'už', 'v', 'vo', 'za', 'že',
    # Anglické stop words
    'a', 'an', 'the', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
    'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing',
    'will', 'would', 'could', 'should', 'may', 'might', 'must',
    'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they',
    'me', 'him', 'her', 'us', 'them', 'my', 'your', 'his', 'her', 'its', 'our', 'their',
    'what', 'which', 'who', 'whom', 'whose', 'where', 'when', 'why', 'how',
    'and', 'or', 'but', 'if', 'because', 'as', 'while', 'until', 'for', 'to', 'of', 'in',
    'on', 'at', 'by', 'with', 'from', 'up', 'about', 'into', 'through', 'during',
    # Časté slová, ktoré nie sú informatívne
    'ked', 'ktory', 'ktore', 'teraz', 'mam', 'sme', 'tam', 'mal', 'aby',
    'create', 'created', 'update', 'updated', 'delete', 'deleted',
    'add', 'added', 'remove', 'removed', 'change', 'changed',
    'make', 'made', 'do', 'done', 'get', 'got', 'set', 'use', 'used',
}


def extract_meaningful_words(text: str, min_length: int = 4) -> list:
    """Extrahuje zmysluplné slová z textu (dlhšie slová, nie stop words)."""
    if not text:
        return []
    
    # Rozdelí na slová
    words = re.findall(r'\b\w+\b', text.lower())
    
    # Filtruje
    meaningful = []
    for word in words:
        # Ignoruje krátke slová, stop words, čísla
        if (len(word) >= min_length and 
            word not in STOP_WORDS and
            not word.isdigit() and
            not re.match(r'^\d+$', word)):
            meaningful.append(word)
    
    return meaningful


def extract_phrases(text: str, n: int = 2) -> list:
    """Extrahuje n-gramy (frázy) z textu."""
    if not text:
        return []
    
    words = extract_meaningful_words(text, min_length=3)
    phrases = []
    
    for i in range(len(words) - n + 1):
        phrase = ' '.join(words[i:i+n])
        phrases.append(phrase)
    
    return phrases


def identify_topics(texts: list, top_n: int = 3) -> list:
    """Identifikuje top témy na základe bigramov a trigramov."""
    all_bigrams = []
    all_trigrams = []
    all_words = []
    
    for text in texts:
        all_bigrams.extend(extract_phrases(text, n=2))
        all_trigrams.extend(extract_phrases(text, n=3))
        all_words.extend(extract_meaningful_words(text, min_length=4))
    
    # Počíta frekvencie
    bigram_freq = Counter(all_bigrams)
    trigram_freq = Counter(all_trigrams)
    word_freq = Counter(all_words)
    
    # Kombinuje s váhami (trigramy > bigramy > slová)
    all_terms = []
    
    # Trigramy (najvyššia váha)
    for trigram, count in trigram_freq.most_common(20):
        if count >= 3:  # Minimálna frekvencia
            all_terms.append((trigram, count * 3))
    
    # Bigramy
    for bigram, count in bigram_freq.most_common(30):
        if count >= 5:  # Minimálna frekvencia
            # Ignoruje bigramy, ktoré sú súčasťou trigramov
            if not any(trigram in bigram or bigram in trigram for trigram, _ in all_terms[:10]):
                all_terms.append((bigram, count * 2))
    
    # Slová (len top, ako fallback)
    for word, count in word_freq.most_common(10):
        if count >= 10:  # Minimálna frekvencia
            all_terms.append((word, count))
    
    # Zoradiť podľa váhy
    all_terms.sort(key=lambda x: x[1], reverse=True)
    
    # Vráti top N tém
    topics = []
    seen_words = set()
    
    for term, count in all_terms:
        # Ignoruje duplikáty
        term_words = set(term.split())
        if not term_words.intersection(seen_words) or len(term_words) > 1:
            topics.append((term, count))
            seen_words.update(term_words)
            if len(topics) >= top_n:
                break
    
    return topics


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
    print("🔍 Analýza dominantných tém v promptoch (v2)...")
    
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
        for i, (topic, count) in enumerate(data['topics'], 1):
            print(f"  {i}. {topic} (váha: {count:.1f})")
    
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

