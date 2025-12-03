#!/usr/bin/env python3
"""
Analýza dominantných tém v promptoch podľa mesiacov.
Identifikuje top 3 témy pre každý mesiac pomocou kľúčových slov a fráz.
"""

import json
import re
from pathlib import Path
from collections import Counter, defaultdict
from datetime import datetime

# Cesty k dátam
PROMPTS_SPLIT_DIR = Path("data/prompts/prompts_split")
PROMPTS_LOG_PATH = Path("xvadur/data/prompts_log.jsonl")

# Stop words (slovenčina + angličtina)
STOP_WORDS = {
    'a', 'áno', 'ani', 'ale', 'aj', 'ako', 'aký', 'aká', 'aké', 'akú', 'akom', 'akým',
    'alebo', 'alebo', 'ani', 'avšak', 'áno', 'áno',
    'bol', 'bola', 'bolo', 'boli', 'bol', 'bude', 'budem', 'budeš', 'bude', 'budeme',
    'by', 'byť', 'byť', 'byť', 'byť',
    'cez', 'čo', 'čo', 'čo', 'čo', 'čo', 'čo', 'čo', 'čo', 'čo', 'čo', 'čo',
    'do', 'dokonca', 'dokonca', 'dokonca', 'dokonca', 'dokonca', 'dokonca',
    'ešte', 'ešte', 'ešte', 'ešte', 'ešte', 'ešte', 'ešte', 'ešte', 'ešte',
    'ho', 'ho', 'ho', 'ho', 'ho', 'ho', 'ho', 'ho', 'ho', 'ho', 'ho', 'ho',
    'i', 'ich', 'ich', 'ich', 'ich', 'ich', 'ich', 'ich', 'ich', 'ich', 'ich',
    'je', 'je', 'je', 'je', 'je', 'je', 'je', 'je', 'je', 'je', 'je', 'je',
    'k', 'k', 'k', 'k', 'k', 'k', 'k', 'k', 'k', 'k', 'k', 'k',
    'keď', 'keď', 'keď', 'keď', 'keď', 'keď', 'keď', 'keď', 'keď', 'keď',
    'ktorý', 'ktorá', 'ktoré', 'ktorí', 'ktorú', 'ktorom', 'ktorým', 'ktorých',
    'lebo', 'lebo', 'lebo', 'lebo', 'lebo', 'lebo', 'lebo', 'lebo', 'lebo',
    'ma', 'ma', 'ma', 'ma', 'ma', 'ma', 'ma', 'ma', 'ma', 'ma', 'ma', 'ma',
    'mi', 'mi', 'mi', 'mi', 'mi', 'mi', 'mi', 'mi', 'mi', 'mi', 'mi', 'mi',
    'na', 'na', 'na', 'na', 'na', 'na', 'na', 'na', 'na', 'na', 'na', 'na',
    'nie', 'nie', 'nie', 'nie', 'nie', 'nie', 'nie', 'nie', 'nie', 'nie',
    'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o',
    'od', 'od', 'od', 'od', 'od', 'od', 'od', 'od', 'od', 'od', 'od', 'od',
    'po', 'po', 'po', 'po', 'po', 'po', 'po', 'po', 'po', 'po', 'po', 'po',
    'pre', 'pre', 'pre', 'pre', 'pre', 'pre', 'pre', 'pre', 'pre', 'pre',
    'pri', 'pri', 'pri', 'pri', 'pri', 'pri', 'pri', 'pri', 'pri', 'pri',
    'sa', 'sa', 'sa', 'sa', 'sa', 'sa', 'sa', 'sa', 'sa', 'sa', 'sa', 'sa',
    'so', 'so', 'so', 'so', 'so', 'so', 'so', 'so', 'so', 'so', 'so', 'so',
    'som', 'som', 'som', 'som', 'som', 'som', 'som', 'som', 'som', 'som',
    'sú', 'sú', 'sú', 'sú', 'sú', 'sú', 'sú', 'sú', 'sú', 'sú', 'sú', 'sú',
    'tak', 'tak', 'tak', 'tak', 'tak', 'tak', 'tak', 'tak', 'tak', 'tak',
    'to', 'to', 'to', 'to', 'to', 'to', 'to', 'to', 'to', 'to', 'to', 'to',
    'tu', 'tu', 'tu', 'tu', 'tu', 'tu', 'tu', 'tu', 'tu', 'tu', 'tu', 'tu',
    'už', 'už', 'už', 'už', 'už', 'už', 'už', 'už', 'už', 'už', 'už', 'už',
    'v', 'v', 'v', 'v', 'v', 'v', 'v', 'v', 'v', 'v', 'v', 'v',
    'vo', 'vo', 'vo', 'vo', 'vo', 'vo', 'vo', 'vo', 'vo', 'vo', 'vo', 'vo',
    'za', 'za', 'za', 'za', 'za', 'za', 'za', 'za', 'za', 'za', 'za', 'za',
    'že', 'že', 'že', 'že', 'že', 'že', 'že', 'že', 'že', 'že', 'že', 'že',
    'a', 'an', 'the', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
    'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing',
    'will', 'would', 'could', 'should', 'may', 'might', 'must',
    'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they',
    'me', 'him', 'her', 'us', 'them', 'my', 'your', 'his', 'her', 'its', 'our', 'their',
    'what', 'which', 'who', 'whom', 'whose', 'where', 'when', 'why', 'how',
    'and', 'or', 'but', 'if', 'because', 'as', 'while', 'until', 'for', 'to', 'of', 'in', 'on', 'at', 'by', 'with', 'from', 'up', 'about', 'into', 'through', 'during', 'including', 'against', 'among', 'throughout', 'despite', 'towards', 'upon', 'concerning', 'to', 'of', 'in', 'for', 'on', 'with', 'at', 'by', 'from', 'up', 'about', 'into', 'through', 'during', 'including', 'against', 'among', 'throughout', 'despite', 'towards', 'upon', 'concerning'
}

# Technické slová, ktoré chceme ignorovať
TECH_STOP_WORDS = {
    'subor', 'suboru', 'suborom', 'subore', 'suboroch', 'suborom',
    'súbor', 'súboru', 'súborom', 'súbore', 'súboroch', 'súborom',
    'json', 'jsonl', 'md', 'py', 'txt', 'csv', 'yaml', 'yml',
    'file', 'files', 'folder', 'folders', 'directory', 'directories',
    'path', 'paths', 'url', 'urls', 'link', 'links',
    'code', 'codes', 'script', 'scripts', 'function', 'functions',
    'variable', 'variables', 'parameter', 'parameters',
    'data', 'datum', 'date', 'time', 'timestamp',
    'create', 'created', 'update', 'updated', 'delete', 'deleted',
    'add', 'added', 'remove', 'removed', 'change', 'changed',
    'make', 'made', 'do', 'done', 'get', 'got', 'set', 'use', 'used',
    'need', 'needed', 'want', 'wanted', 'can', 'could', 'should',
    'will', 'would', 'may', 'might', 'must',
    'this', 'that', 'these', 'those',
    'one', 'two', 'three', 'first', 'second', 'third',
    'new', 'old', 'old', 'good', 'bad', 'big', 'small',
    'very', 'really', 'quite', 'just', 'only', 'also', 'even',
    'more', 'most', 'less', 'least', 'much', 'many', 'few',
    'some', 'any', 'all', 'each', 'every', 'both', 'either', 'neither',
    'other', 'another', 'same', 'different', 'such', 'same',
    'here', 'there', 'where', 'when', 'why', 'how',
    'now', 'then', 'today', 'yesterday', 'tomorrow',
    'yes', 'no', 'not', 'never', 'always', 'often', 'sometimes', 'usually',
    'well', 'better', 'best', 'worse', 'worst',
    'say', 'said', 'tell', 'told', 'ask', 'asked', 'answer', 'answered',
    'see', 'saw', 'look', 'looked', 'watch', 'watched',
    'know', 'knew', 'known', 'think', 'thought', 'thought',
    'come', 'came', 'go', 'went', 'gone', 'get', 'got', 'got',
    'give', 'gave', 'given', 'take', 'took', 'taken',
    'make', 'made', 'find', 'found', 'work', 'worked',
    'try', 'tried', 'use', 'used', 'call', 'called',
    'ask', 'asked', 'need', 'needed', 'want', 'wanted',
    'help', 'helped', 'show', 'showed', 'shown',
    'let', 'let', 'put', 'put', 'set', 'set',
    'run', 'ran', 'run', 'move', 'moved', 'turn', 'turned',
    'begin', 'began', 'begun', 'start', 'started', 'stop', 'stopped',
    'keep', 'kept', 'hold', 'held', 'bring', 'brought',
    'write', 'wrote', 'written', 'read', 'read', 'read',
    'hear', 'heard', 'listen', 'listened', 'speak', 'spoke', 'spoken',
    'say', 'said', 'tell', 'told', 'talk', 'talked',
    'meet', 'met', 'meet', 'leave', 'left', 'left',
    'feel', 'felt', 'felt', 'seem', 'seemed', 'appear', 'appeared',
    'become', 'became', 'become', 'grow', 'grew', 'grown',
    'build', 'built', 'built', 'buy', 'bought', 'bought',
    'send', 'sent', 'sent', 'pay', 'paid', 'paid',
    'cut', 'cut', 'cut', 'hit', 'hit', 'hit',
    'cost', 'cost', 'cost', 'hurt', 'hurt', 'hurt',
    'let', 'let', 'let', 'put', 'put', 'put',
    'set', 'set', 'set', 'shut', 'shut', 'shut',
    'spread', 'spread', 'spread', 'split', 'split', 'split',
    'strike', 'struck', 'struck', 'stuck', 'stuck', 'stuck',
    'sweep', 'swept', 'swept', 'swing', 'swung', 'swung',
    'teach', 'taught', 'taught', 'tear', 'tore', 'torn',
    'tell', 'told', 'told', 'think', 'thought', 'thought',
    'throw', 'threw', 'thrown', 'understand', 'understood', 'understood',
    'wake', 'woke', 'woken', 'wear', 'wore', 'worn',
    'win', 'won', 'won', 'wind', 'wound', 'wound',
    'write', 'wrote', 'written'
}


def normalize_word(word: str) -> str:
    """Normalizuje slovo (lowercase, odstráni diakritiku)."""
    word = word.lower()
    # Odstráni diakritiku (jednoduchá verzia)
    replacements = {
        'á': 'a', 'ä': 'a', 'č': 'c', 'ď': 'd', 'é': 'e', 'ě': 'e',
        'í': 'i', 'ľ': 'l', 'ĺ': 'l', 'ň': 'n', 'ó': 'o', 'ô': 'o',
        'ö': 'o', 'ř': 'r', 'š': 's', 'ť': 't', 'ú': 'u', 'ů': 'u',
        'ü': 'u', 'ý': 'y', 'ž': 'z'
    }
    for old, new in replacements.items():
        word = word.replace(old, new)
    return word


def extract_keywords(text: str, min_length: int = 3) -> list:
    """Extrahuje kľúčové slová z textu."""
    if not text:
        return []
    
    # Rozdelí na slová
    words = re.findall(r'\b\w+\b', text.lower())
    
    # Filtruje stop words a krátke slová
    keywords = []
    for word in words:
        normalized = normalize_word(word)
        if (len(word) >= min_length and 
            normalized not in STOP_WORDS and 
            normalized not in TECH_STOP_WORDS and
            not word.isdigit()):
            keywords.append(normalized)
    
    return keywords


def extract_bigrams(text: str) -> list:
    """Extrahuje bigramy (dvojice slov) z textu."""
    if not text:
        return []
    
    words = extract_keywords(text)
    bigrams = []
    
    for i in range(len(words) - 1):
        bigram = f"{words[i]} {words[i+1]}"
        bigrams.append(bigram)
    
    return bigrams


def identify_topics(keywords: list, bigrams: list, top_n: int = 3) -> list:
    """Identifikuje top témy na základe kľúčových slov a bigramov."""
    # Počíta frekvencie
    keyword_freq = Counter(keywords)
    bigram_freq = Counter(bigrams)
    
    # Kombinuje kľúčové slová a bigramy
    all_terms = []
    
    # Pridá bigramy (majú vyššiu váhu)
    for bigram, count in bigram_freq.most_common(top_n * 2):
        all_terms.append((bigram, count * 2))  # Bigramy majú 2x väčšiu váhu
    
    # Pridá kľúčové slová
    for keyword, count in keyword_freq.most_common(top_n * 3):
        # Ignoruje slová, ktoré sú už v bigramoch
        if keyword not in ' '.join([b[0] for b in all_terms]):
            all_terms.append((keyword, count))
    
    # Zoradiť podľa frekvencie
    all_terms.sort(key=lambda x: x[1], reverse=True)
    
    # Vráti top N tém
    topics = []
    seen_words = set()
    
    for term, count in all_terms:
        # Ignoruje duplikáty
        term_words = set(term.split())
        if not term_words.intersection(seen_words):
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
            except Exception as e:
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
        # Zlúči všetky texty pre mesiac
        all_text = ' '.join(texts)
        
        # Extrahuje kľúčové slová a bigramy
        keywords = extract_keywords(all_text)
        bigrams = extract_bigrams(all_text)
        
        # Identifikuje top 3 témy
        topics = identify_topics(keywords, bigrams, top_n=3)
        
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
    print("🔍 Analýza dominantných tém v promptoch...")
    
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
            print(f"  {i}. {topic} ({count}x)")
    
    # Vytvor markdown formát
    print("\n📋 Markdown formát:")
    print("-" * 80)
    
    for month_key in sorted_months:
        data = monthly_topics[month_key]
        topics_str = " | ".join([f"{topic} ({count}x)" for topic, count in data['topics']])
        print(f"| {data['display_name']} | {topics_str} |")
    
    return monthly_topics


if __name__ == "__main__":
    main()

