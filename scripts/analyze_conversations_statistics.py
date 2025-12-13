#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Vytvorí detailné štatistiky z rozdelenej datasetu conversations_by_month.
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from collections import Counter, defaultdict
from typing import Dict, List

CONVERSATIONS_DIR = Path("development/data/conversations_by_month")
OUTPUT_FILE = Path("development/data/analysis/conversations_statistics.md")


def load_monthly_files(conversations_dir: Path) -> List[Dict]:
    """Načíta všetky konverzácie zo všetkých mesiacových súborov."""
    records = []
    
    if not conversations_dir.exists():
        print(f"❌ Adresár neexistuje: {conversations_dir}")
        return records
    
    monthly_files = sorted(conversations_dir.glob("conversations_*.jsonl"))
    
    if not monthly_files:
        print(f"⚠️  Nenašli sa žiadne mesiacové súbory")
        return records
    
    print(f"📖 Načítavam {len(monthly_files)} mesiacových súborov...")
    
    for monthly_file in monthly_files:
        file_records = 0
        with open(monthly_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    record = json.loads(line)
                    records.append(record)
                    file_records += 1
                except json.JSONDecodeError:
                    continue
        print(f"  ✅ {monthly_file.name}: {file_records:,} konverzácií")
    
    print(f"\n✅ Celkovo načítaných {len(records):,} konverzácií")
    return records


def extract_date(record: Dict) -> datetime:
    """Extrahuje dátum z záznamu."""
    date_str = None
    
    if 'user_prompt' in record and isinstance(record['user_prompt'], dict):
        if 'date_created' in record['user_prompt']:
            date_str = record['user_prompt']['date_created']
    
    if not date_str and 'timestamp' in record:
        date_str = record['timestamp']
    
    if date_str:
        try:
            date_str_clean = date_str.replace('Z', '+00:00')
            return datetime.fromisoformat(date_str_clean)
        except:
            pass
    
    return None


def analyze_statistics(records: List[Dict]) -> Dict:
    """Analyzuje štatistiky z konverzácií."""
    print("\n📊 Analyzujem štatistiky...")
    
    stats = {
        'total_conversations': len(records),
        'by_month': Counter(),
        'by_day': Counter(),
        'by_session': Counter(),
        'date_range': {'min': None, 'max': None},
        'text_lengths': {
            'user_prompts': [],
            'ai_responses': [],
            'total': []
        },
        'word_counts': {
            'user_prompts': [],
            'ai_responses': [],
            'total': []
        },
        'sessions_stats': defaultdict(lambda: {
            'count': 0,
            'dates': [],
            'total_words': 0
        }),
        'valid_dates': 0,
        'invalid_dates': 0,
        'empty_texts': 0
    }
    
    for i, record in enumerate(records):
        if (i + 1) % 500 == 0:
            print(f"  Spracovaných {i+1:,}/{len(records):,} konverzácií...", flush=True)
        
        # Dátum
        dt = extract_date(record)
        if dt:
            stats['valid_dates'] += 1
            month_key = f"{dt.year}-{dt.month:02d}"
            day_key = dt.strftime('%Y-%m-%d')
            stats['by_month'][month_key] += 1
            stats['by_day'][day_key] += 1
            
            if stats['date_range']['min'] is None or dt < stats['date_range']['min']:
                stats['date_range']['min'] = dt
            if stats['date_range']['max'] is None or dt > stats['date_range']['max']:
                stats['date_range']['max'] = dt
        else:
            stats['invalid_dates'] += 1
        
        # Texty
        user_text = record.get("user_prompt", {}).get("extracted_text", "")
        ai_text = record.get("ai_response", {}).get("extracted_text", "")
        
        if not user_text.strip() or not ai_text.strip():
            stats['empty_texts'] += 1
            continue
        
        # Dĺžky textov
        user_length = len(user_text)
        ai_length = len(ai_text)
        total_length = user_length + ai_length
        
        stats['text_lengths']['user_prompts'].append(user_length)
        stats['text_lengths']['ai_responses'].append(ai_length)
        stats['text_lengths']['total'].append(total_length)
        
        # Počty slov
        user_words = len(user_text.split())
        ai_words = len(ai_text.split())
        total_words = user_words + ai_words
        
        stats['word_counts']['user_prompts'].append(user_words)
        stats['word_counts']['ai_responses'].append(ai_words)
        stats['word_counts']['total'].append(total_words)
        
        # Sessions
        session = record.get("session", "")
        if session:
            stats['by_session'][session] += 1
            stats['sessions_stats'][session]['count'] += 1
            if dt:
                stats['sessions_stats'][session]['dates'].append(dt)
            stats['sessions_stats'][session]['total_words'] += total_words
    
    return stats


def calculate_percentiles(values: List[int]) -> Dict:
    """Vypočíta percentily zoznamu hodnôt."""
    if not values:
        return {}
    
    sorted_values = sorted(values)
    n = len(sorted_values)
    
    return {
        'min': sorted_values[0],
        'p25': sorted_values[int(n * 0.25)],
        'median': sorted_values[int(n * 0.5)],
        'p75': sorted_values[int(n * 0.75)],
        'p90': sorted_values[int(n * 0.90)],
        'p95': sorted_values[int(n * 0.95)],
        'p99': sorted_values[int(n * 0.99)] if n > 100 else sorted_values[-1],
        'max': sorted_values[-1],
        'mean': sum(values) / n
    }


def generate_report(stats: Dict) -> str:
    """Generuje Markdown report zo štatistík."""
    report = []
    report.append("# Štatistiky Konverzácií\n")
    report.append(f"**Dátum analýzy:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    report.append(f"**Celkový počet konverzácií:** {stats['total_conversations']:,}\n")
    
    # Dátumový rozsah
    if stats['date_range']['min'] and stats['date_range']['max']:
        report.append(f"\n## 📅 Dátumový Rozsah\n")
        report.append(f"- **Od:** {stats['date_range']['min'].strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"- **Do:** {stats['date_range']['max'].strftime('%Y-%m-%d %H:%M:%S')}")
        days = (stats['date_range']['max'] - stats['date_range']['min']).days
        report.append(f"- **Rozsah:** {days} dní ({days/30:.1f} mesiacov)")
        report.append(f"- **Valid dátumov:** {stats['valid_dates']:,} ({stats['valid_dates']/stats['total_conversations']*100:.1f}%)")
        report.append(f"- **Invalid dátumov:** {stats['invalid_dates']:,}")
    
    # Rozdelenie podľa mesiacov
    report.append(f"\n## 📊 Rozdelenie Podľa Mesiacov\n")
    report.append("| Mesiac | Počet konverzácií | Percentuálny podiel |")
    report.append("|--------|-------------------|---------------------|")
    total_valid = sum(stats['by_month'].values())
    for month in sorted(stats['by_month'].keys()):
        count = stats['by_month'][month]
        percentage = (count / total_valid * 100) if total_valid > 0 else 0
        report.append(f"| {month} | {count:,} | {percentage:.1f}% |")
    
    # Rozdelenie podľa dní (top 20)
    report.append(f"\n## 📅 Najaktívnejšie Dni (Top 20)\n")
    report.append("| Dátum | Počet konverzácií |")
    report.append("|-------|-------------------|")
    for day, count in stats['by_day'].most_common(20):
        report.append(f"| {day} | {count:,} |")
    
    # Sessions
    report.append(f"\n## 💬 Sessions\n")
    report.append(f"- **Celkový počet sessions:** {len(stats['by_session']):,}")
    report.append(f"- **Priemerný počet konverzácií na session:** {sum(stats['by_session'].values())/len(stats['by_session']):.1f}")
    
    # Top sessions
    report.append(f"\n### Top 10 Sessions (podľa počtu konverzácií)\n")
    report.append("| Session ID | Počet konverzácií | Rozsah dátumov | Celkový počet slov |")
    report.append("|------------|-------------------|----------------|---------------------|")
    for session, count in stats['by_session'].most_common(10):
        session_stats = stats['sessions_stats'][session]
        dates = session_stats['dates']
        if dates:
            date_range = f"{min(dates).strftime('%Y-%m-%d')} - {max(dates).strftime('%Y-%m-%d')}"
        else:
            date_range = "N/A"
        report.append(f"| `{session[:8]}...` | {count:,} | {date_range} | {session_stats['total_words']:,} |")
    
    # Textové štatistiky
    report.append(f"\n## 📝 Textové Štatistiky\n")
    
    # Dĺžky textov
    report.append(f"\n### Dĺžka Textov (znaky)\n")
    for text_type in ['user_prompts', 'ai_responses', 'total']:
        values = stats['text_lengths'][text_type]
        if values:
            percentiles = calculate_percentiles(values)
            type_name = {
                'user_prompts': 'User Prompts',
                'ai_responses': 'AI Responses',
                'total': 'Celkom (User + AI)'
            }[text_type]
            report.append(f"\n**{type_name}:**")
            report.append(f"- Priemer: {percentiles['mean']:,.0f} znakov")
            report.append(f"- Medián: {percentiles['median']:,} znakov")
            report.append(f"- Min: {percentiles['min']:,} znakov")
            report.append(f"- Max: {percentiles['max']:,} znakov")
            report.append(f"- P95: {percentiles['p95']:,} znakov")
    
    # Počty slov
    report.append(f"\n### Počet Slov\n")
    for text_type in ['user_prompts', 'ai_responses', 'total']:
        values = stats['word_counts'][text_type]
        if values:
            percentiles = calculate_percentiles(values)
            type_name = {
                'user_prompts': 'User Prompts',
                'ai_responses': 'AI Responses',
                'total': 'Celkom (User + AI)'
            }[text_type]
            report.append(f"\n**{type_name}:**")
            report.append(f"- Priemer: {percentiles['mean']:,.0f} slov")
            report.append(f"- Medián: {percentiles['median']:,} slov")
            report.append(f"- Min: {percentiles['min']:,} slov")
            report.append(f"- Max: {percentiles['max']:,} slov")
            report.append(f"- P95: {percentiles['p95']:,} slov")
    
    # Ratio AI/User
    if stats['word_counts']['user_prompts'] and stats['word_counts']['ai_responses']:
        avg_user_words = sum(stats['word_counts']['user_prompts']) / len(stats['word_counts']['user_prompts'])
        avg_ai_words = sum(stats['word_counts']['ai_responses']) / len(stats['word_counts']['ai_responses'])
        ratio = avg_ai_words / avg_user_words if avg_user_words > 0 else 0
        
        report.append(f"\n### AI/User Ratio\n")
        report.append(f"- Priemerný počet slov (User): {avg_user_words:,.0f}")
        report.append(f"- Priemerný počet slov (AI): {avg_ai_words:,.0f}")
        report.append(f"- **Ratio (AI/User): {ratio:.2f}x** (AI odpovede sú v priemere {ratio:.1f}x dlhšie)")
    
    # Problémy
    if stats['empty_texts'] > 0:
        report.append(f"\n## ⚠️ Problémy\n")
        report.append(f"- Konverzácie s prázdnymi textami: {stats['empty_texts']:,}")
    
    return "\n".join(report)


def main():
    """Hlavná funkcia"""
    print("="*60)
    print("📊 ANALÝZA ŠTATISTÍK KONVERZÁCIÍ")
    print("="*60)
    print()
    
    # Načítanie dát
    records = load_monthly_files(CONVERSATIONS_DIR)
    
    if not records:
        print("❌ Žiadne dáta na analýzu")
        sys.exit(1)
    
    # Analýza
    stats = analyze_statistics(records)
    
    # Generovanie reportu
    print("\n📝 Generujem report...")
    report = generate_report(stats)
    
    # Uloženie reportu
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"✅ Report uložený: {OUTPUT_FILE}")
    print(f"\n{'='*60}")
    print("📊 STRUČNÉ ZHRNUTIE")
    print(f"{'='*60}")
    print(f"Celkový počet konverzácií: {stats['total_conversations']:,}")
    print(f"Sessions: {len(stats['by_session']):,}")
    if stats['date_range']['min'] and stats['date_range']['max']:
        print(f"Dátumový rozsah: {stats['date_range']['min'].strftime('%Y-%m-%d')} - {stats['date_range']['max'].strftime('%Y-%m-%d')}")
    if stats['word_counts']['total']:
        avg_words = sum(stats['word_counts']['total']) / len(stats['word_counts']['total'])
        print(f"Priemerný počet slov na konverzáciu: {avg_words:,.0f}")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()


