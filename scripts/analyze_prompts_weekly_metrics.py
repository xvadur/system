#!/usr/bin/env python3
"""
Analýza metrík promptov podľa týždňov.
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


def calculate_weekly_metrics(prompts: list) -> dict:
    """Vypočíta metriky pre každý týždeň (ISO týždeň)."""
    weekly_data = defaultdict(lambda: {
        "prompts": [],
        "word_counts": [],
        "sentence_counts": [],
        "dates": set(),
    })
    
    for prompt in prompts:
        date = prompt["date"]
        # ISO týždeň: (rok, týždeň, deň)
        iso_week = date.isocalendar()
        week_key = f"{iso_week[0]}-W{iso_week[1]:02d}"
        
        text = prompt["text"]
        word_count = prompt["word_count"]
        sentence_count = count_sentences(text)
        
        weekly_data[week_key]["prompts"].append(prompt)
        weekly_data[week_key]["word_counts"].append(word_count)
        weekly_data[week_key]["sentence_counts"].append(sentence_count)
        weekly_data[week_key]["dates"].add(date.date())
    
    # Vypočíta finálne metriky
    metrics = {}
    for week_key, data in weekly_data.items():
        year, week_num = week_key.split("-W")
        year = int(year)
        week_num = int(week_num)
        
        # Nájdi prvý a posledný deň týždňa
        dates = sorted(data["dates"])
        first_date = dates[0] if dates else None
        last_date = dates[-1] if dates else None
        
        # Display name
        if first_date and last_date:
            if first_date.month == last_date.month:
                display_name = f"W{week_num} {year} ({first_date.strftime('%d')}-{last_date.strftime('%d.%m')})"
            else:
                display_name = f"W{week_num} {year} ({first_date.strftime('%d.%m')}-{last_date.strftime('%d.%m')})"
        else:
            display_name = f"W{week_num} {year}"
        
        total_prompts = len(data["prompts"])
        total_words = sum(data["word_counts"])
        total_sentences = sum(data["sentence_counts"])
        median_sentences = median(data["sentence_counts"]) if data["sentence_counts"] else 0
        active_days = len(data["dates"])
        avg_words_per_prompt = total_words / total_prompts if total_prompts > 0 else 0
        
        metrics[week_key] = {
            "display_name": display_name,
            "week_key": week_key,
            "total_prompts": total_prompts,
            "total_words": total_words,
            "total_sentences": total_sentences,
            "median_sentences": round(median_sentences, 1),
            "active_days": active_days,
            "avg_words_per_prompt": round(avg_words_per_prompt, 1),
            "first_date": first_date,
            "last_date": last_date,
        }
    
    return metrics


def calculate_trends(metrics: dict) -> dict:
    """Vypočíta trendy (zmeny oproti predchádzajúcemu týždňu)."""
    sorted_weeks = sorted(metrics.keys())
    trends = {}
    
    for i, week_key in enumerate(sorted_weeks):
        if i == 0:
            trends[week_key] = {
                "prompts_change": None,
                "words_change": None,
                "sentences_change": None,
            }
        else:
            prev_week_key = sorted_weeks[i - 1]
            prev_metrics = metrics[prev_week_key]
            curr_metrics = metrics[week_key]
            
            prompts_change = curr_metrics["total_prompts"] - prev_metrics["total_prompts"]
            words_change = curr_metrics["total_words"] - prev_metrics["total_words"]
            sentences_change = curr_metrics["total_sentences"] - prev_metrics["total_sentences"]
            
            trends[week_key] = {
                "prompts_change": prompts_change,
                "words_change": words_change,
                "sentences_change": sentences_change,
            }
    
    return trends


def main():
    """Hlavná funkcia."""
    print("📊 Analýza metrík promptov podľa týždňov...")
    print()
    
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
    print()
    
    # Vypočíta metriky
    print("🔢 Vypočítavam metriky podľa týždňov...")
    metrics = calculate_weekly_metrics(all_prompts)
    trends = calculate_trends(metrics)
    
    # Zobraz výsledky
    print("\n📈 Výsledky podľa týždňov:")
    print("-" * 100)
    
    # Zoradiť podľa týždňa
    sorted_weeks = sorted(metrics.keys())
    
    for week_key in sorted_weeks:
        m = metrics[week_key]
        t = trends[week_key]
        
        print(f"\n{m['display_name']}:")
        print(f"  - Počet promptov: {m['total_prompts']}", end="")
        if t["prompts_change"] is not None:
            change_str = f"+{t['prompts_change']}" if t['prompts_change'] >= 0 else str(t['prompts_change'])
            print(f" ({change_str})", end="")
        print()
        print(f"  - Celkový word count: {m['total_words']:,}")
        print(f"  - Priemerný word count na prompt: {m['avg_words_per_prompt']}")
        print(f"  - Celkový počet viet: {m['total_sentences']:,}")
        print(f"  - Median počtu viet: {m['median_sentences']}")
        print(f"  - Aktívnych dní: {m['active_days']}")
    
    # Vytvor markdown tabuľku
    print("\n" + "=" * 100)
    print("📋 Markdown tabuľka:")
    print("=" * 100)
    print()
    print("| Týždeň | Počet Promptov | Word Count | Priem. Words/Prompt | Počet Viet | Median Viet | Aktívnych Dní |")
    print("|--------|---------------|------------|---------------------|------------|-------------|---------------|")
    
    for week_key in sorted_weeks:
        m = metrics[week_key]
        print(f"| {m['display_name']} | {m['total_prompts']} | {m['total_words']:,} | {m['avg_words_per_prompt']} | {m['total_sentences']:,} | {m['median_sentences']} | {m['active_days']} |")
    
    # Štatistiky
    print("\n" + "=" * 100)
    print("📊 Celkové štatistiky:")
    print("=" * 100)
    total_prompts = sum(m["total_prompts"] for m in metrics.values())
    total_words = sum(m["total_words"] for m in metrics.values())
    total_sentences = sum(m["total_sentences"] for m in metrics.values())
    avg_prompts_per_week = total_prompts / len(metrics) if metrics else 0
    avg_words_per_week = total_words / len(metrics) if metrics else 0
    
    print(f"Celkom týždňov: {len(metrics)}")
    print(f"Celkom promptov: {total_prompts}")
    print(f"Celkom slov: {total_words:,}")
    print(f"Celkom viet: {total_sentences:,}")
    print(f"Priemer promptov za týždeň: {avg_prompts_per_week:.1f}")
    print(f"Priemer slov za týždeň: {avg_words_per_week:,.0f}")
    
    return metrics


if __name__ == "__main__":
    main()


