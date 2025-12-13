#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Analyzuje časové vzorce v konverzáciách:
- Heatmapa aktivity (hodiny x dni v týždni)
- Medzery medzi konverzáciami
- Časové závislosti a trendy
"""

import json
import sys
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict, Counter
from typing import Dict, List, Tuple
import statistics

try:
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    import seaborn as sns
    import numpy as np
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False
    print("⚠️  matplotlib/seaborn nie je nainštalovaný - vytvorím len textový report")

CONVERSATIONS_DIR = Path("development/data/conversations_by_month")
OUTPUT_DIR = Path("development/data/analysis")
OUTPUT_REPORT = OUTPUT_DIR / "conversations_temporal_analysis.md"


def load_conversations(conversations_dir: Path) -> List[Dict]:
    """Načíta všetky konverzácie."""
    records = []
    
    monthly_files = sorted(conversations_dir.glob("conversations_*.jsonl"))
    
    for monthly_file in monthly_files:
        with open(monthly_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    record = json.loads(line)
                    records.append(record)
                except json.JSONDecodeError:
                    continue
    
    return records


def extract_datetime(record: Dict) -> datetime:
    """Extrahuje datetime z záznamu."""
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


def analyze_temporal_patterns(records: List[Dict]) -> Dict:
    """Analyzuje časové vzorce."""
    print("📊 Analyzujem časové vzorce...")
    
    datetimes = []
    
    for record in records:
        dt = extract_datetime(record)
        if dt:
            datetimes.append((dt, record))
    
    # Zoradiť podľa času
    datetimes.sort(key=lambda x: x[0])
    
    # Aktivita podľa hodiny dňa
    hourly_activity = Counter()
    # Aktivita podľa dňa v týždni (0 = pondelok, 6 = nedeľa)
    weekday_activity = Counter()
    # Aktivita podľa dňa v mesiaci
    day_of_month_activity = Counter()
    # Kombinovaná heatmapa: hodina x deň v týždni
    hour_weekday_heatmap = defaultdict(lambda: defaultdict(int))
    
    # Medzery medzi konverzáciami
    time_gaps_minutes = []
    time_gaps_hours = []
    time_gaps_days = []
    
    # Dĺžky textov podľa času
    hourly_word_counts = defaultdict(list)
    weekday_word_counts = defaultdict(list)
    
    # Sledovanie konverzácií v rámci session
    session_gaps = defaultdict(list)  # session_id -> [gaps v minútach]
    
    prev_dt = None
    prev_session = None
    
    for dt, record in datetimes:
        # Hodinová aktivita
        hour = dt.hour
        hourly_activity[hour] += 1
        
        # Deň v týždni (0 = pondelok, 6 = nedeľa)
        weekday = dt.weekday()
        weekday_activity[weekday] += 1
        
        # Deň v mesiaci
        day_of_month = dt.day
        day_of_month_activity[day_of_month] += 1
        
        # Heatmapa
        hour_weekday_heatmap[weekday][hour] += 1
        
        # Dĺžka textu
        user_text = record.get("user_prompt", {}).get("extracted_text", "")
        word_count = len(user_text.split())
        hourly_word_counts[hour].append(word_count)
        weekday_word_counts[weekday].append(word_count)
        
        # Medzery medzi konverzáciami
        if prev_dt:
            gap = dt - prev_dt
            gap_minutes = gap.total_seconds() / 60
            gap_hours = gap.total_seconds() / 3600
            gap_days = gap.days
            
            time_gaps_minutes.append(gap_minutes)
            time_gaps_hours.append(gap_hours)
            if gap_days > 0:
                time_gaps_days.append(gap_days)
            
            # Gaps v rámci session
            current_session = record.get("session", "")
            if current_session and current_session == prev_session:
                session_gaps[current_session].append(gap_minutes)
        
        prev_dt = dt
        prev_session = record.get("session", "")
    
    # Štatistiky gaps
    gap_stats = {}
    if time_gaps_minutes:
        gap_stats = {
            'median_minutes': statistics.median(time_gaps_minutes),
            'mean_minutes': statistics.mean(time_gaps_minutes),
            'median_hours': statistics.median(time_gaps_hours),
            'mean_hours': statistics.mean(time_gaps_hours),
            'median_days': statistics.median(time_gaps_days) if time_gaps_days else 0,
            'mean_days': statistics.mean(time_gaps_days) if time_gaps_days else 0,
            'min_gap_minutes': min(time_gaps_minutes),
            'max_gap_minutes': max(time_gaps_minutes),
            'p95_minutes': sorted(time_gaps_minutes)[int(len(time_gaps_minutes) * 0.95)] if len(time_gaps_minutes) > 20 else max(time_gaps_minutes),
        }
    
    # Priemerné počty slov podľa hodiny/dňa
    hourly_avg_words = {h: statistics.mean(word_counts) if word_counts else 0 
                        for h, word_counts in hourly_word_counts.items()}
    weekday_avg_words = {d: statistics.mean(word_counts) if word_counts else 0 
                         for d, word_counts in weekday_word_counts.items()}
    
    # Session gaps štatistiky
    session_gap_stats = {}
    for session, gaps in session_gaps.items():
        if gaps:
            session_gap_stats[session] = {
                'median': statistics.median(gaps),
                'mean': statistics.mean(gaps),
                'count': len(gaps)
            }
    
    return {
        'total_conversations': len(datetimes),
        'date_range': {
            'start': datetimes[0][0] if datetimes else None,
            'end': datetimes[-1][0] if datetimes else None
        },
        'hourly_activity': hourly_activity,
        'weekday_activity': weekday_activity,
        'day_of_month_activity': day_of_month_activity,
        'hour_weekday_heatmap': hour_weekday_heatmap,
        'time_gaps': {
            'minutes': time_gaps_minutes,
            'hours': time_gaps_hours,
            'days': time_gaps_days,
            'stats': gap_stats
        },
        'hourly_word_counts': hourly_avg_words,
        'weekday_word_counts': weekday_avg_words,
        'session_gaps': session_gap_stats,
        'datetimes': datetimes
    }


def create_heatmap(data: Dict, output_dir: Path):
    """Vytvorí heatmapu aktivity."""
    if not HAS_MATPLOTLIB:
        print("⚠️  matplotlib nie je dostupný - preskakujem vytvorenie heatmapy")
        return
    
    print("\n🎨 Vytváram heatmapu...")
    
    # Pripraviť dáta pre heatmapu (deň v týždni x hodina)
    weekday_names = ['Pondelok', 'Utorok', 'Streda', 'Štvrtok', 'Piatok', 'Sobota', 'Nedeľa']
    hours = list(range(24))
    
    heatmap_data = np.zeros((7, 24))
    
    for weekday in range(7):
        for hour in range(24):
            heatmap_data[weekday, hour] = data['hour_weekday_heatmap'][weekday].get(hour, 0)
    
    # Vytvorenie heatmapy
    plt.figure(figsize=(14, 8))
    sns.heatmap(heatmap_data, 
                xticklabels=hours,
                yticklabels=weekday_names,
                cmap='YlOrRd',
                annot=False,
                fmt='.0f',
                cbar_kws={'label': 'Počet konverzácií'})
    
    plt.title('Aktivita podľa dňa v týždni a hodiny dňa', fontsize=16, pad=20)
    plt.xlabel('Hodina dňa', fontsize=12)
    plt.ylabel('Deň v týždni', fontsize=12)
    plt.tight_layout()
    
    heatmap_path = output_dir / "activity_heatmap.png"
    plt.savefig(heatmap_path, dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"✅ Heatmapa uložená: {heatmap_path}")


def create_time_series(data: Dict, output_dir: Path):
    """Vytvorí časový graf aktivity."""
    if not HAS_MATPLOTLIB:
        return
    
    print("📈 Vytváram časový graf...")
    
    # Zoskupiť podľa dní
    daily_counts = defaultdict(int)
    for dt, _ in data['datetimes']:
        day_key = dt.date()
        daily_counts[day_key] += 1
    
    dates = sorted(daily_counts.keys())
    counts = [daily_counts[d] for d in dates]
    
    plt.figure(figsize=(16, 6))
    plt.plot(dates, counts, linewidth=1.5, alpha=0.7)
    plt.fill_between(dates, counts, alpha=0.3)
    plt.title('Počet konverzácií podľa dní', fontsize=16)
    plt.xlabel('Dátum', fontsize=12)
    plt.ylabel('Počet konverzácií', fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.gcf().autofmt_xdate()
    
    time_series_path = output_dir / "activity_timeline.png"
    plt.savefig(time_series_path, dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"✅ Časový graf uložený: {time_series_path}")


def create_gaps_distribution(data: Dict, output_dir: Path):
    """Vytvorí graf distribúcie medzier."""
    if not HAS_MATPLOTLIB:
        return
    
    print("⏱️  Vytváram graf distribúcie medzier...")
    
    gaps_minutes = data['time_gaps']['minutes']
    
    # Filtrovať extrémne veľké gaps (viac ako 7 dní) pre lepšie zobrazenie
    filtered_gaps = [g for g in gaps_minutes if g <= 7 * 24 * 60]
    
    plt.figure(figsize=(14, 6))
    
    # Histogram
    plt.subplot(1, 2, 1)
    plt.hist(filtered_gaps, bins=100, edgecolor='black', alpha=0.7)
    plt.xlabel('Medzera (minúty)', fontsize=12)
    plt.ylabel('Počet', fontsize=12)
    plt.title('Distribúcia medzier medzi konverzáciami', fontsize=14)
    plt.yscale('log')
    plt.grid(True, alpha=0.3)
    
    # Box plot (pre medzery kratšie ako 24 hodín)
    short_gaps = [g for g in gaps_minutes if g <= 24 * 60]
    plt.subplot(1, 2, 2)
    plt.boxplot(short_gaps, vert=True)
    plt.ylabel('Medzera (minúty)', fontsize=12)
    plt.title('Medzery ≤ 24 hodín (box plot)', fontsize=14)
    plt.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    
    gaps_path = output_dir / "time_gaps_distribution.png"
    plt.savefig(gaps_path, dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"✅ Graf distribúcie uložený: {gaps_path}")


def generate_report(data: Dict, output_file: Path, output_dir: Path) -> str:
    """Generuje Markdown report."""
    report = []
    
    report.append("# Časová Analýza Konverzácií\n")
    report.append(f"**Dátum analýzy:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    report.append(f"**Celkový počet konverzácií:** {data['total_conversations']:,}\n")
    
    # Dátumový rozsah
    if data['date_range']['start']:
        start = data['date_range']['start']
        end = data['date_range']['end']
        report.append(f"\n## 📅 Dátumový Rozsah\n")
        report.append(f"- **Od:** {start.strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"- **Do:** {end.strftime('%Y-%m-%d %H:%M:%S')}")
        days = (end - start).days
        report.append(f"- **Rozsah:** {days} dní\n")
    
    # Heatmapa
    report.append(f"\n## 🗓️ Heatmapa Aktivity\n")
    report.append("![Activity Heatmap](activity_heatmap.png)\n")
    report.append("*Aktivita podľa dňa v týždni a hodiny dňa*\n")
    
    # Top hodiny
    report.append(f"\n### Top 10 Najaktívnejších Hodín\n")
    report.append("| Hodina | Počet konverzácií |")
    report.append("|--------|-------------------|")
    for hour, count in data['hourly_activity'].most_common(10):
        report.append(f"| {hour:02d}:00 | {count:,} |")
    
    # Top dni v týždni
    weekday_names = ['Pondelok', 'Utorok', 'Streda', 'Štvrtok', 'Piatok', 'Sobota', 'Nedeľa']
    report.append(f"\n### Aktivita Podľa Dňa v Týždni\n")
    report.append("| Deň | Počet konverzácií |")
    report.append("|-----|-------------------|")
    for weekday in range(7):
        count = data['weekday_activity'].get(weekday, 0)
        report.append(f"| {weekday_names[weekday]} | {count:,} |")
    
    # Priemerné počty slov
    report.append(f"\n## 📝 Dĺžka Textov Podľa Času\n")
    
    report.append(f"\n### Priemerný Počet Slov Podľa Hodiny\n")
    report.append("| Hodina | Priemerný počet slov |")
    report.append("|--------|---------------------|")
    for hour in range(24):
        avg_words = data['hourly_word_counts'].get(hour, 0)
        if avg_words > 0:
            report.append(f"| {hour:02d}:00 | {avg_words:.0f} |")
    
    report.append(f"\n### Priemerný Počet Slov Podľa Dňa v Týždni\n")
    report.append("| Deň | Priemerný počet slov |")
    report.append("|-----|---------------------|")
    for weekday in range(7):
        avg_words = data['weekday_word_counts'].get(weekday, 0)
        if avg_words > 0:
            report.append(f"| {weekday_names[weekday]} | {avg_words:.0f} |")
    
    # Časový graf
    report.append(f"\n## 📈 Časový Vývoj Aktivity\n")
    report.append("![Activity Timeline](activity_timeline.png)\n")
    
    # Medzery medzi konverzáciami
    report.append(f"\n## ⏱️ Medzery Medzi Konverzáciami\n")
    
    gap_stats = data['time_gaps']['stats']
    if gap_stats:
        report.append("![Time Gaps Distribution](time_gaps_distribution.png)\n")
        report.append("\n### Štatistiky Medzier\n")
        report.append(f"- **Medián medzery:** {gap_stats['median_minutes']:.1f} minút ({gap_stats['median_hours']:.2f} hodín)")
        report.append(f"- **Priemerná medzera:** {gap_stats['mean_minutes']:.1f} minút ({gap_stats['mean_hours']:.2f} hodín)")
        report.append(f"- **Minimálna medzera:** {gap_stats['min_gap_minutes']:.1f} minút")
        report.append(f"- **Maximálna medzera:** {gap_stats['max_gap_minutes']:.1f} minút ({gap_stats['max_gap_minutes']/60:.1f} hodín, {gap_stats['max_gap_minutes']/(60*24):.1f} dní)")
        report.append(f"- **P95 medzera:** {gap_stats['p95_minutes']:.1f} minút ({gap_stats['p95_minutes']/60:.2f} hodín)")
        
        if gap_stats.get('median_days', 0) > 0:
            report.append(f"- **Medián medzery (dni):** {gap_stats['median_days']:.1f} dní")
            report.append(f"- **Priemerná medzera (dni):** {gap_stats['mean_days']:.1f} dní")
    
    # Interpretácia
    report.append(f"\n## 💡 Interpretácia\n")
    
    # Najaktívnejšia hodina
    top_hour, top_hour_count = data['hourly_activity'].most_common(1)[0]
    report.append(f"- **Najaktívnejšia hodina:** {top_hour:02d}:00 ({top_hour_count} konverzácií)")
    
    # Najaktívnejší deň
    top_weekday_idx, top_weekday_count = max(data['weekday_activity'].items(), key=lambda x: x[1])
    report.append(f"- **Najaktívnejší deň v týždni:** {weekday_names[top_weekday_idx]} ({top_weekday_count} konverzácií)")
    
    # Priemerná medzera
    if gap_stats:
        median_hours = gap_stats['median_hours']
        if median_hours < 1:
            report.append(f"- **Priemerná medzera:** {median_hours*60:.0f} minút - aktívne písanie")
        elif median_hours < 24:
            report.append(f"- **Priemerná medzera:** {median_hours:.1f} hodín - pravidelné písanie")
        else:
            report.append(f"- **Priemerná medzera:** {median_hours/24:.1f} dní - občasné písanie")
    
    return "\n".join(report)


def main():
    """Hlavná funkcia"""
    print("="*60)
    print("📊 ČASOVÁ ANALÝZA KONVERZÁCIÍ")
    print("="*60)
    print()
    
    # Načítanie dát
    print("📖 Načítavam konverzácie...")
    records = load_conversations(CONVERSATIONS_DIR)
    print(f"✅ Načítaných {len(records):,} konverzácií\n")
    
    if not records:
        print("❌ Žiadne dáta na analýzu")
        sys.exit(1)
    
    # Analýza
    data = analyze_temporal_patterns(records)
    
    # Vytvorenie vizualizácií
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    if HAS_MATPLOTLIB:
        create_heatmap(data, OUTPUT_DIR)
        create_time_series(data, OUTPUT_DIR)
        create_gaps_distribution(data, OUTPUT_DIR)
    
    # Generovanie reportu
    print("\n📝 Generujem report...")
    report = generate_report(data, OUTPUT_REPORT, OUTPUT_DIR)
    
    # Uloženie
    with open(OUTPUT_REPORT, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"✅ Report uložený: {OUTPUT_REPORT}")
    print(f"\n{'='*60}")
    print("✅ ANALÝZA DOKONČENÁ")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()

