#!/usr/bin/env python3
"""
Vytvorí grafy pre analýzu promptov:
1. Sentiment v priebehu času
2. Počet slov v priebehu času
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from collections import defaultdict
from typing import List, Dict

try:
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    from matplotlib import style
except ImportError:
    print("❌ Chyba: Potrebuješ nainštalovať matplotlib")
    print("   pip install matplotlib")
    sys.exit(1)

# Konfigurácia
INPUT_FILE = Path("data/prompts/prompts_nlp4sk.jsonl")
OUTPUT_DIR = Path("data/prompts/visualizations")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Nastavenie štýlu
plt.style.use('seaborn-v0_8-darkgrid')
fig_size = (14, 6)


def load_data() -> List[Dict]:
    """Načíta dáta z prompts_nlp4sk.jsonl."""
    data = []
    
    if not INPUT_FILE.exists():
        print(f"❌ Súbor {INPUT_FILE} neexistuje!")
        return data
    
    try:
        with open(INPUT_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    data.append(json.loads(line))
                except json.JSONDecodeError as e:
                    continue
    except Exception as e:
        print(f"❌ Chyba pri načítaní dát: {e}")
        return data
    
    print(f"✅ Načítaných {len(data)} promptov")
    return data


def prepare_sentiment_data(data: List[Dict]) -> Dict:
    """Pripraví dáta pre sentiment graf - agregácia podľa dátumu."""
    daily_sentiments = defaultdict(lambda: {'positive': 0, 'neutral': 0, 'negative': 0, 'total': 0})
    
    for item in data:
        date_str = item.get('date', '')
        sentiment = item.get('sentiment', 'neutral')
        
        if not date_str:
            continue
        
        try:
            # Parsuj dátum
            if isinstance(date_str, str):
                date = datetime.strptime(date_str, "%Y-%m-%d")
            else:
                continue
            
            # Agreguj sentimenty
            if sentiment in ['positive', 'neutral', 'negative']:
                daily_sentiments[date][sentiment] += 1
            daily_sentiments[date]['total'] += 1
            
        except Exception as e:
            continue
    
    # Zoraď podľa dátumu
    sorted_dates = sorted(daily_sentiments.keys())
    
    dates = []
    positive_counts = []
    neutral_counts = []
    negative_counts = []
    total_counts = []
    
    for date in sorted_dates:
        dates.append(date)
        counts = daily_sentiments[date]
        positive_counts.append(counts['positive'])
        neutral_counts.append(counts['neutral'])
        negative_counts.append(counts['negative'])
        total_counts.append(counts['total'])
    
    return {
        'dates': dates,
        'positive': positive_counts,
        'neutral': neutral_counts,
        'negative': negative_counts,
        'total': total_counts
    }


def prepare_word_count_data(data: List[Dict]) -> Dict:
    """Pripraví dáta pre word count graf - agregácia podľa dátumu."""
    daily_word_counts = defaultdict(lambda: {'words': [], 'count': 0})
    
    for item in data:
        date_str = item.get('date', '')
        word_count = item.get('word_count', 0)
        
        if not date_str or word_count == 0:
            continue
        
        try:
            # Parsuj dátum
            if isinstance(date_str, str):
                date = datetime.strptime(date_str, "%Y-%m-%d")
            else:
                continue
            
            daily_word_counts[date]['words'].append(word_count)
            daily_word_counts[date]['count'] += 1
            
        except Exception as e:
            continue
    
    # Zoraď podľa dátumu a vypočítaj priemery
    sorted_dates = sorted(daily_word_counts.keys())
    
    dates = []
    avg_word_counts = []
    total_word_counts = []
    prompt_counts = []
    
    for date in sorted_dates:
        dates.append(date)
        words = daily_word_counts[date]['words']
        if words:
            avg_word_counts.append(sum(words) / len(words))
            total_word_counts.append(sum(words))
        else:
            avg_word_counts.append(0)
            total_word_counts.append(0)
        prompt_counts.append(daily_word_counts[date]['count'])
    
    return {
        'dates': dates,
        'avg_words': avg_word_counts,
        'total_words': total_word_counts,
        'prompt_count': prompt_counts
    }


def create_sentiment_graph(sentiment_data: Dict):
    """Vytvorí graf sentimentu v priebehu času."""
    fig, ax = plt.subplots(figsize=fig_size)
    
    dates = sentiment_data['dates']
    
    # Stacked area chart pre sentimenty
    ax.fill_between(dates, 0, sentiment_data['positive'], 
                    label='Pozitívny', color='#2ecc71', alpha=0.7)
    ax.fill_between(dates, sentiment_data['positive'], 
                    [p + n for p, n in zip(sentiment_data['positive'], sentiment_data['neutral'])],
                    label='Neutrálny', color='#f39c12', alpha=0.7)
    ax.fill_between(dates, 
                    [p + n for p, n in zip(sentiment_data['positive'], sentiment_data['neutral'])],
                    sentiment_data['total'],
                    label='Negatívny', color='#e74c3c', alpha=0.7)
    
    # Formátovanie osí
    ax.set_xlabel('Dátum', fontsize=12, fontweight='bold')
    ax.set_ylabel('Počet promptov', fontsize=12, fontweight='bold')
    ax.set_title('Sentiment promptov v priebehu času', fontsize=14, fontweight='bold', pad=20)
    ax.legend(loc='upper left', fontsize=10)
    ax.grid(True, alpha=0.3)
    
    # Formátovanie dátumu na osi X
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    ax.xaxis.set_major_locator(mdates.WeekdayLocator(interval=2))
    plt.xticks(rotation=45, ha='right')
    
    # Uprav layout
    plt.tight_layout()
    
    # Ulož
    output_path = OUTPUT_DIR / "sentiment_over_time.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✅ Graf uložený: {output_path}")
    plt.close()


def create_word_count_graph(word_data: Dict):
    """Vytvorí graf počtu slov v priebehu času."""
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(fig_size[0], fig_size[1] * 1.5), sharex=True)
    
    dates = word_data['dates']
    
    # Graf 1: Priemerný počet slov na prompt
    ax1.plot(dates, word_data['avg_words'], 
             marker='o', markersize=4, linewidth=2, color='#3498db', label='Priemerný počet slov')
    ax1.fill_between(dates, word_data['avg_words'], alpha=0.3, color='#3498db')
    ax1.set_ylabel('Priemerný počet slov', fontsize=12, fontweight='bold')
    ax1.set_title('Priemerný počet slov na prompt v priebehu času', fontsize=14, fontweight='bold', pad=20)
    ax1.legend(loc='upper left', fontsize=10)
    ax1.grid(True, alpha=0.3)
    
    # Graf 2: Celkový počet slov a počet promptov
    ax2_twin = ax2.twinx()
    
    # Celkový počet slov (bar chart)
    ax2.bar(dates, word_data['total_words'], 
            alpha=0.6, color='#9b59b6', label='Celkový počet slov', width=1)
    
    # Počet promptov (line)
    ax2_twin.plot(dates, word_data['prompt_count'], 
                  marker='s', markersize=4, linewidth=2, color='#e67e22', label='Počet promptov')
    
    ax2.set_xlabel('Dátum', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Celkový počet slov', fontsize=12, fontweight='bold', color='#9b59b6')
    ax2_twin.set_ylabel('Počet promptov', fontsize=12, fontweight='bold', color='#e67e22')
    ax2.set_title('Celkový počet slov a počet promptov v priebehu času', fontsize=14, fontweight='bold', pad=20)
    
    # Legenda
    lines1, labels1 = ax2.get_legend_handles_labels()
    lines2, labels2 = ax2_twin.get_legend_handles_labels()
    ax2.legend(lines1 + lines2, labels1 + labels2, loc='upper left', fontsize=10)
    
    ax2.grid(True, alpha=0.3)
    ax2.tick_params(axis='y', labelcolor='#9b59b6')
    ax2_twin.tick_params(axis='y', labelcolor='#e67e22')
    
    # Formátovanie dátumu na osi X
    ax2.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    ax2.xaxis.set_major_locator(mdates.WeekdayLocator(interval=2))
    plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45, ha='right')
    
    # Uprav layout
    plt.tight_layout()
    
    # Ulož
    output_path = OUTPUT_DIR / "word_count_over_time.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✅ Graf uložený: {output_path}")
    plt.close()


def main():
    """Hlavná funkcia."""
    print("="*80)
    print("Vytváranie grafov pre analýzu promptov")
    print("="*80)
    
    # Načítaj dáta
    print("\n📖 Načítavam dáta...")
    data = load_data()
    
    if not data:
        print("❌ Žiadne dáta na spracovanie!")
        return
    
    # Priprav dáta pre sentiment graf
    print("\n📊 Pripravujem dáta pre sentiment graf...")
    sentiment_data = prepare_sentiment_data(data)
    print(f"   Dátumov: {len(sentiment_data['dates'])}")
    print(f"   Celkom promptov: {sum(sentiment_data['total'])}")
    
    # Priprav dáta pre word count graf
    print("\n📊 Pripravujem dáta pre word count graf...")
    word_data = prepare_word_count_data(data)
    print(f"   Dátumov: {len(word_data['dates'])}")
    
    # Vytvor grafy
    print("\n🎨 Vytváram grafy...")
    create_sentiment_graph(sentiment_data)
    create_word_count_graph(word_data)
    
    print("\n" + "="*80)
    print("✅ Hotovo! Grafy sú uložené v:")
    print(f"   📁 {OUTPUT_DIR}/")
    print("="*80)


if __name__ == "__main__":
    main()

