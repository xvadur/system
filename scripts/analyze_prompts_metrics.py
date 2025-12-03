#!/usr/bin/env python3
"""
Analýza metrík promptov podľa mesiacov.
Vypočíta: počet promptov, word count, počet viet, median viet.
"""

import json
import re
from pathlib import Path
from collections import defaultdict
from statistics import median
from datetime import datetime

# Cesty k dátam
PROMPTS_SPLIT_DIR = Path("data/prompts/prompts_split")
PROMPTS_LOG_PATH = Path("xvadur/data/prompts_log.jsonl")


def count_words(text: str) -> int:
    """Počíta počet slov v texte."""
    if not text:
        return 0
    # Odstráni whitespace a rozdelí na slová
    words = re.findall(r'\b\w+\b', text)
    return len(words)


def count_sentences(text: str) -> int:
    """Počíta počet viet v texte."""
    if not text:
        return 0
    # Rozdelí na vety podľa interpunkcie
    sentences = re.split(r'[.!?]+', text)
    # Filtruje prázdne vety
    sentences = [s.strip() for s in sentences if s.strip()]
    return len(sentences)


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
                
                # Validácia
                if not data.get("text"):
                    continue
                
                # Extrahuj dátum
                date_str = data.get("date", day_dir.name)
                try:
                    date = datetime.strptime(date_str, "%Y-%m-%d")
                except:
                    continue
                
                text = data.get("text", "")
                word_count = data.get("word_count", count_words(text))
                
                prompts.append({
                    "date": date,
                    "text": text,
                    "word_count": word_count,
                })
            except Exception as e:
                print(f"⚠️  Chyba pri načítaní {json_file}: {e}")
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
                    
                    # Len user prompty
                    if data.get("role") != "user":
                        continue
                    
                    # Extrahuj dátum
                    timestamp_str = data.get("timestamp", "")
                    try:
                        # Podporuje rôzne formáty timestampov
                        if '+' in timestamp_str or timestamp_str.endswith('Z'):
                            # ISO format s timezone
                            date = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
                        else:
                            date = datetime.fromisoformat(timestamp_str)
                    except:
                        continue
                    
                    text = data.get("content", "")
                    word_count = count_words(text)
                    
                    prompts.append({
                        "date": date,
                        "text": text,
                        "word_count": word_count,
                    })
                except Exception as e:
                    print(f"⚠️  Chyba pri parsovaní riadku: {e}")
                    continue
    except Exception as e:
        print(f"⚠️  Chyba pri načítaní {PROMPTS_LOG_PATH}: {e}")
    
    return prompts


def calculate_monthly_metrics(prompts: list) -> dict:
    """Vypočíta metriky pre každý mesiac."""
    monthly_data = defaultdict(lambda: {
        "prompts": [],
        "word_counts": [],
        "sentence_counts": [],
    })
    
    for prompt in prompts:
        date = prompt["date"]
        month_key = f"{date.year}-{date.month:02d}"
        
        text = prompt["text"]
        word_count = prompt["word_count"]
        sentence_count = count_sentences(text)
        
        monthly_data[month_key]["prompts"].append(prompt)
        monthly_data[month_key]["word_counts"].append(word_count)
        monthly_data[month_key]["sentence_counts"].append(sentence_count)
    
    # Vypočíta finálne metriky
    metrics = {}
    for month_key, data in monthly_data.items():
        year, month = month_key.split("-")
        year = int(year)
        month = int(month)
        
        # Slovenské názvy mesiacov
        month_names = {
            1: "Január", 2: "Február", 3: "Marec", 4: "Apríl",
            5: "Máj", 6: "Jún", 7: "Júl", 8: "August",
            9: "September", 10: "Október", 11: "November", 12: "December"
        }
        
        month_name = month_names.get(month, f"Mesiac {month}")
        display_name = f"{month_name} {year}"
        
        total_prompts = len(data["prompts"])
        total_words = sum(data["word_counts"])
        total_sentences = sum(data["sentence_counts"])
        median_sentences = median(data["sentence_counts"]) if data["sentence_counts"] else 0
        
        metrics[month_key] = {
            "display_name": display_name,
            "total_prompts": total_prompts,
            "total_words": total_words,
            "total_sentences": total_sentences,
            "median_sentences": round(median_sentences, 1),
        }
    
    return metrics


def main():
    """Hlavná funkcia."""
    print("📊 Analýza metrík promptov...")
    
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
    
    # Vypočíta metriky
    print("🔢 Vypočítavam metriky...")
    metrics = calculate_monthly_metrics(all_prompts)
    
    # Zobraz výsledky
    print("\n📈 Výsledky podľa mesiacov:")
    print("-" * 80)
    
    # Zoradiť podľa dátumu
    sorted_months = sorted(metrics.keys())
    
    for month_key in sorted_months:
        m = metrics[month_key]
        print(f"{m['display_name']}:")
        print(f"  - Počet promptov: {m['total_prompts']}")
        print(f"  - Celkový word count: {m['total_words']:,}")
        print(f"  - Celkový počet viet: {m['total_sentences']:,}")
        print(f"  - Median počtu viet: {m['median_sentences']}")
        print()
    
    # Vytvor markdown tabuľku
    print("\n📋 Markdown tabuľka:")
    print("-" * 80)
    print("| Mesiac | Počet Promptov | Word Count | Počet Viet | Median Viet |")
    print("|--------|---------------|------------|------------|-------------|")
    
    for month_key in sorted_months:
        m = metrics[month_key]
        print(f"| {m['display_name']} | {m['total_prompts']} | {m['total_words']:,} | {m['total_sentences']:,} | {m['median_sentences']} |")
    
    return metrics


if __name__ == "__main__":
    main()

