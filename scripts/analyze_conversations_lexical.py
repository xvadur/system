#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Lexikálna analýza konverzácií:
- Základné metriky (vocabulary, TTR, frekvenčná distribúcia)
- Pokročilé metriky (hapax legomena, Zipfov zákon, lexikálna hustota)
- Vizualizácie (wordcloud, frekvenčné grafy)
- Porovnania (User vs AI, sessions, časové obdobia)
"""

import json
import sys
import re
from pathlib import Path
from datetime import datetime
from collections import Counter, defaultdict
from typing import Dict, List, Tuple
import math

try:
    from wordcloud import WordCloud
    import matplotlib.pyplot as plt
    import seaborn as sns
    import numpy as np
    HAS_VIZ = True
except ImportError:
    HAS_VIZ = False
    print("⚠️  wordcloud/matplotlib nie je nainštalovaný - vizualizácie preskočené")

# Slovenské stopwords (základná sada)
SLOVAK_STOPWORDS = {
    'a', 'ale', 'ani', 'áno', 'bez', 'cez', 'čo', 'do', 'ho', 'i', 'je', 'jeho',
    'ju', 'k', 'keď', 'ktorý', 'ma', 'mi', 'na', 'nie', 'o', 'od', 'po', 'pre',
    'pri', 'sa', 'so', 'sú', 'táto', 'to', 'tu', 'ty', 'v', 'vo', 'vy', 'z', 'za',
    'že', 'ako', 'aký', 'alebo', 'alebo', 'ani', 'bol', 'bola', 'boli', 'bolo',
    'by', 'byť', 'čo', 'dávať', 'kto', 'ktorý', 'ktorá', 'ktoré', 'môže', 'môže',
    'musieť', 'naj', 'nech', 'nie', 'niekto', 'niektorý', 'niektorá', 'niektoré',
    'podľa', 'preto', 'práve', 'pri', 'rád', 'ráda', 'rádi', 'rádo', 'rovnako',
    'samý', 'samá', 'samé', 'samí', 'sám', 'sama', 'sami', 'samo', 'svoj', 'svojí',
    'tam', 'tento', 'táto', 'tieto', 'tiež', 'tým', 'už', 'vám', 'váš', 'váša',
    'váše', 'váši', 'väčšia', 'väčšie', 'väčšiu', 'väčší', 'viac', 'viaceré', 'viacero',
    'však', 'všetci', 'všetko', 'všetky', 'zase', 'zase', 'žiadny', 'žiadna', 'žiadne'
}

CONVERSATIONS_DIR = Path("development/data/conversations_by_month")
OUTPUT_DIR = Path("development/data/analysis")
OUTPUT_REPORT = OUTPUT_DIR / "conversations_lexical_analysis.md"


def clean_text(text: str) -> str:
    """Vyčistí text: odstránenie interpunkcie, normalizácia."""
    # Odstránenie diakritiky z interpunkcie, zachovanie slovenských znakov
    text = text.lower()
    # Odstránenie viacerých medzier
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def tokenize(text: str, remove_stopwords: bool = False) -> List[str]:
    """Tokenizácia textu na slová."""
    # Vyčistenie
    text = clean_text(text)
    
    # Rozdelenie na slová (slovenské znaky + medzery)
    # Zachováme slovenské znaky (á, é, í, ó, ú, ý, ô, ŕ, ľ, ň, š, č, ž, ť, ď)
    words = re.findall(r'[a-záäéíóúýôŕľňščžťď]+', text)
    
    # Filtrovanie stopwords
    if remove_stopwords:
        words = [w for w in words if w not in SLOVAK_STOPWORDS and len(w) > 2]
    
    return words


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


def calculate_basic_metrics(words: List[str]) -> Dict:
    """Vypočíta základné lexikálne metriky."""
    if not words:
        return {}
    
    total_words = len(words)
    unique_words = len(set(words))
    ttr = unique_words / total_words if total_words > 0 else 0
    
    # Frekvenčná distribúcia
    freq_dist = Counter(words)
    
    # Hapax legomena (slová, ktoré sa vyskytujú len raz)
    hapax = sum(1 for count in freq_dist.values() if count == 1)
    hapax_ratio = hapax / unique_words if unique_words > 0 else 0
    
    return {
        'total_words': total_words,
        'unique_words': unique_words,
        'ttr': ttr,
        'hapax_count': hapax,
        'hapax_ratio': hapax_ratio,
        'freq_dist': freq_dist,
        'avg_word_length': sum(len(w) for w in words) / total_words if total_words > 0 else 0
    }


def calculate_zipf_metrics(freq_dist: Counter) -> Dict:
    """Analyzuje Zipfov zákon distribúciu."""
    if not freq_dist:
        return {}
    
    # Zoradiť podľa frekvencie (od najvyššej)
    sorted_freqs = sorted(freq_dist.values(), reverse=True)
    
    # Zipfov rád (1, 2, 3, ...)
    ranks = list(range(1, len(sorted_freqs) + 1))
    
    # Logaritmy pre analýzu
    log_ranks = [math.log(r) for r in ranks]
    log_freqs = [math.log(f) for f in sorted_freqs]
    
    # Lineárna regresia pre Zipfov parameter
    if len(log_ranks) > 1:
        # Jednoduchý odhad (môže byť presnejší s numpy)
        slope = (len(log_ranks) * sum(lr * lf for lr, lf in zip(log_ranks, log_freqs)) - 
                sum(log_ranks) * sum(log_freqs)) / \
               (len(log_ranks) * sum(lr**2 for lr in log_ranks) - sum(log_ranks)**2)
    else:
        slope = -1.0
    
    return {
        'zipf_slope': slope,
        'top_freq': sorted_freqs[0] if sorted_freqs else 0,
        'ranks': ranks[:100],  # Top 100
        'frequencies': sorted_freqs[:100]
    }


def estimate_content_words(words: List[str]) -> float:
    """
    Odhad lexikálnej hustoty.
    Jednoduchý prístup: pomery dlhších slov (pravdepodobne obsahové) vs. kratších.
    """
    if not words:
        return 0.0
    
    # Obsahové slová: dĺžka >= 5 znakov (nepresné, ale funkčné)
    content_words = [w for w in words if len(w) >= 5]
    return len(content_words) / len(words) if len(words) > 0 else 0.0


def analyze_lexical(records: List[Dict]) -> Dict:
    """Hlavná lexikálna analýza."""
    print("📊 Analyzujem lexikálne metriky...")
    
    all_user_words = []
    all_ai_words = []
    all_words = []
    
    user_texts = []
    ai_texts = []
    
    by_session = defaultdict(lambda: {'user': [], 'ai': []})
    by_month = defaultdict(lambda: {'user': [], 'ai': []})
    
    for i, record in enumerate(records):
        if (i + 1) % 500 == 0:
            print(f"  Spracovaných {i+1:,}/{len(records):,} konverzácií...", flush=True)
        
        user_text = record.get("user_prompt", {}).get("extracted_text", "")
        ai_text = record.get("ai_response", {}).get("extracted_text", "")
        
        if not user_text or not ai_text:
            continue
        
        # Tokenizácia
        user_words = tokenize(user_text, remove_stopwords=False)
        ai_words = tokenize(ai_text, remove_stopwords=False)
        
        all_user_words.extend(user_words)
        all_ai_words.extend(ai_words)
        all_words.extend(user_words)
        all_words.extend(ai_words)
        
        user_texts.append(user_text)
        ai_texts.append(ai_text)
        
        # Podľa session
        session = record.get("session", "")
        if session:
            by_session[session]['user'].extend(user_words)
            by_session[session]['ai'].extend(ai_words)
        
        # Podľa mesiacov
        dt = extract_datetime(record)
        if dt:
            month_key = f"{dt.year}-{dt.month:02d}"
            by_month[month_key]['user'].extend(user_words)
            by_month[month_key]['ai'].extend(ai_words)
    
    # Základné metriky
    print("  Vypočítavam základné metriky...")
    user_metrics = calculate_basic_metrics(all_user_words)
    ai_metrics = calculate_basic_metrics(all_ai_words)
    overall_metrics = calculate_basic_metrics(all_words)
    
    # Zipfov zákon
    print("  Analyzujem Zipfov zákon...")
    user_zipf = calculate_zipf_metrics(user_metrics.get('freq_dist', Counter()))
    ai_zipf = calculate_zipf_metrics(ai_metrics.get('freq_dist', Counter()))
    
    # Lexikálna hustota
    print("  Vypočítavam lexikálnu hustotu...")
    user_lex_density = estimate_content_words(all_user_words)
    ai_lex_density = estimate_content_words(all_ai_words)
    
    # Analýza podľa session (top sessions)
    top_sessions = sorted(by_session.items(), 
                         key=lambda x: len(x[1]['user']), reverse=True)[:10]
    
    session_metrics = {}
    for session, words_dict in top_sessions:
        user_ws = words_dict['user']
        ai_ws = words_dict['ai']
        session_metrics[session] = {
            'user': calculate_basic_metrics(user_ws),
            'ai': calculate_basic_metrics(ai_ws)
        }
    
    # Analýza podľa mesiacov
    month_metrics = {}
    for month, words_dict in sorted(by_month.items()):
        user_ws = words_dict['user']
        ai_ws = words_dict['ai']
        month_metrics[month] = {
            'user': calculate_basic_metrics(user_ws),
            'ai': calculate_basic_metrics(ai_ws)
        }
    
    return {
        'user': {
            'words': all_user_words,
            'metrics': user_metrics,
            'zipf': user_zipf,
            'lexical_density': user_lex_density
        },
        'ai': {
            'words': all_ai_words,
            'metrics': ai_metrics,
            'zipf': ai_zipf,
            'lexical_density': ai_lex_density
        },
        'overall': {
            'words': all_words,
            'metrics': overall_metrics
        },
        'sessions': session_metrics,
        'months': month_metrics
    }


def create_wordcloud(words: List[str], title: str, output_path: Path):
    """Vytvorí wordcloud."""
    if not HAS_VIZ:
        return
    
    if not words:
        return
    
    # Frekvenčná distribúcia
    freq_dist = Counter(words)
    
    # Vytvorenie wordcloud (bez stopwords)
    words_no_stopwords = [w for w in words if w not in SLOVAK_STOPWORDS and len(w) > 2]
    if not words_no_stopwords:
        return
    
    text = ' '.join(words_no_stopwords)
    
    try:
        wordcloud = WordCloud(
            width=1600,
            height=800,
            background_color='white',
            max_words=200,
            relative_scaling=0.5,
            colormap='viridis'
        ).generate(text)
        
        plt.figure(figsize=(16, 8))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.title(title, fontsize=20, pad=20)
        plt.tight_layout()
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        plt.close()
        
        print(f"  ✅ Wordcloud uložený: {output_path}")
    except Exception as e:
        print(f"  ⚠️  Chyba pri vytváraní wordcloud: {e}")


def create_frequency_chart(freq_dist: Counter, title: str, output_path: Path, top_n: int = 50):
    """Vytvorí frekvenčný graf top N slov."""
    if not HAS_VIZ:
        return
    
    if not freq_dist:
        return
    
    top_words = freq_dist.most_common(top_n)
    words, freqs = zip(*top_words) if top_words else ([], [])
    
    plt.figure(figsize=(14, 8))
    plt.barh(range(len(words)), freqs, color='steelblue')
    plt.yticks(range(len(words)), words)
    plt.xlabel('Frekvencia', fontsize=12)
    plt.ylabel('Slová', fontsize=12)
    plt.title(title, fontsize=16, pad=20)
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"  ✅ Frekvenčný graf uložený: {output_path}")


def create_zipf_plot(zipf_data: Dict, title: str, output_path: Path):
    """Vytvorí Zipfov graf (log-log plot)."""
    if not HAS_VIZ:
        return
    
    if not zipf_data.get('ranks'):
        return
    
    ranks = zipf_data['ranks']
    freqs = zipf_data['frequencies']
    
    plt.figure(figsize=(10, 8))
    plt.loglog(ranks, freqs, 'o', markersize=4, alpha=0.6)
    plt.xlabel('Poradie (rank) - log scale', fontsize=12)
    plt.ylabel('Frekvencia - log scale', fontsize=12)
    plt.title(f'{title}\nZipf slope: {zipf_data["zipf_slope"]:.2f}', fontsize=14)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"  ✅ Zipfov graf uložený: {output_path}")


def create_comparison_plots(data: Dict, output_dir: Path):
    """Vytvorí porovnávacie grafy."""
    if not HAS_VIZ:
        return
    
    print("\n🎨 Vytváram vizualizácie...")
    
    # Wordclouds
    create_wordcloud(data['user']['words'], 
                    'User Prompts - Najčastejšie slová', 
                    output_dir / 'wordcloud_user.png')
    create_wordcloud(data['ai']['words'], 
                    'AI Responses - Najčastejšie slová', 
                    output_dir / 'wordcloud_ai.png')
    
    # Frekvenčné grafy
    user_freq = data['user']['metrics'].get('freq_dist', Counter())
    ai_freq = data['ai']['metrics'].get('freq_dist', Counter())
    
    create_frequency_chart(user_freq, 
                          'Top 50 slov - User Prompts', 
                          output_dir / 'frequency_user.png', 
                          top_n=50)
    create_frequency_chart(ai_freq, 
                          'Top 50 slov - AI Responses', 
                          output_dir / 'frequency_ai.png', 
                          top_n=50)
    
    # Zipfov grafy
    create_zipf_plot(data['user']['zipf'], 
                    'Zipfov zákon - User Prompts', 
                    output_dir / 'zipf_user.png')
    create_zipf_plot(data['ai']['zipf'], 
                    'Zipfov zákon - AI Responses', 
                    output_dir / 'zipf_ai.png')
    
    # Porovnanie TTR podľa mesiacov
    months = sorted(data['months'].keys())
    user_ttrs = [data['months'][m]['user'].get('ttr', 0) for m in months]
    ai_ttrs = [data['months'][m]['ai'].get('ttr', 0) for m in months]
    
    plt.figure(figsize=(12, 6))
    x = np.arange(len(months))
    width = 0.35
    plt.bar(x - width/2, user_ttrs, width, label='User', alpha=0.8)
    plt.bar(x + width/2, ai_ttrs, width, label='AI', alpha=0.8)
    plt.xlabel('Mesiac', fontsize=12)
    plt.ylabel('TTR (Type-Token Ratio)', fontsize=12)
    plt.title('Lexikálna diverzita (TTR) podľa mesiacov', fontsize=14)
    plt.xticks(x, months, rotation=45)
    plt.legend()
    plt.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    plt.savefig(output_dir / 'ttr_by_month.png', dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"  ✅ Porovnávací graf TTR uložený: {output_dir / 'ttr_by_month.png'}")


def generate_report(data: Dict, output_file: Path, output_dir: Path) -> str:
    """Generuje Markdown report."""
    report = []
    
    report.append("# Lexikálna Analýza Konverzácií\n")
    report.append(f"**Dátum analýzy:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # Celkové metriky
    user_m = data['user']['metrics']
    ai_m = data['ai']['metrics']
    overall_m = data['overall']['metrics']
    
    report.append("## 📊 Základné Metriky\n")
    report.append("### Celkový Prehľad\n")
    report.append(f"- **Celkový počet slov:** {overall_m.get('total_words', 0):,}")
    report.append(f"- **Vocabular size (unikátne slová):** {overall_m.get('unique_words', 0):,}")
    report.append(f"- **Type-Token Ratio (TTR):** {overall_m.get('ttr', 0):.4f}")
    report.append(f"- **Hapax legomena:** {overall_m.get('hapax_count', 0):,} ({overall_m.get('hapax_ratio', 0)*100:.1f}% z unikátnych)")
    report.append(f"- **Priemerná dĺžka slova:** {overall_m.get('avg_word_length', 0):.2f} znakov\n")
    
    # Porovnanie User vs AI
    report.append("### Porovnanie User Prompts vs AI Responses\n")
    report.append("| Metrika | User Prompts | AI Responses | Rozdiel |")
    report.append("|---------|--------------|--------------|---------|")
    report.append(f"| Celkový počet slov | {user_m.get('total_words', 0):,} | {ai_m.get('total_words', 0):,} | {(ai_m.get('total_words', 0) - user_m.get('total_words', 0)):+,} |")
    report.append(f"| Unikátne slová | {user_m.get('unique_words', 0):,} | {ai_m.get('unique_words', 0):,} | {(ai_m.get('unique_words', 0) - user_m.get('unique_words', 0)):+,} |")
    report.append(f"| TTR | {user_m.get('ttr', 0):.4f} | {ai_m.get('ttr', 0):.4f} | {(ai_m.get('ttr', 0) - user_m.get('ttr', 0)):+.4f} |")
    report.append(f"| Hapax legomena | {user_m.get('hapax_count', 0):,} | {ai_m.get('hapax_count', 0):,} | {(ai_m.get('hapax_count', 0) - user_m.get('hapax_count', 0)):+,} |")
    report.append(f"| Lexikálna hustota | {data['user']['lexical_density']:.4f} | {data['ai']['lexical_density']:.4f} | {(data['ai']['lexical_density'] - data['user']['lexical_density']):+.4f} |")
    report.append(f"| Priemerná dĺžka slova | {user_m.get('avg_word_length', 0):.2f} | {ai_m.get('avg_word_length', 0):.2f} | {(ai_m.get('avg_word_length', 0) - user_m.get('avg_word_length', 0)):+.2f} |\n")
    
    # Vizualizácie
    report.append("## 🎨 Vizualizácie\n")
    report.append("### Wordclouds\n")
    report.append("![User Wordcloud](wordcloud_user.png)\n")
    report.append("*Najčastejšie slová v User Prompts*\n")
    report.append("\n![AI Wordcloud](wordcloud_ai.png)\n")
    report.append("*Najčastejšie slová v AI Responses*\n")
    
    report.append("\n### Frekvenčné Grafy\n")
    report.append("![User Frequency](frequency_user.png)\n")
    report.append("\n![AI Frequency](frequency_ai.png)\n")
    
    report.append("\n### Zipfov zákon\n")
    report.append("![User Zipf](zipf_user.png)\n")
    report.append("\n![AI Zipf](zipf_ai.png)\n")
    report.append(f"\n**Zipf slope - User:** {data['user']['zipf'].get('zipf_slope', 0):.3f}")
    report.append(f"**Zipf slope - AI:** {data['ai']['zipf'].get('zipf_slope', 0):.3f}\n")
    
    # Top slová
    report.append("\n## 📝 Top 30 Najčastejších Slov\n")
    report.append("### User Prompts\n")
    report.append("| Slovo | Frekvencia |")
    report.append("|-------|------------|")
    for word, freq in user_m.get('freq_dist', Counter()).most_common(30):
        report.append(f"| {word} | {freq:,} |")
    
    report.append("\n### AI Responses\n")
    report.append("| Slovo | Frekvencia |")
    report.append("|-------|------------|")
    for word, freq in ai_m.get('freq_dist', Counter()).most_common(30):
        report.append(f"| {word} | {freq:,} |")
    
    # Analýza podľa mesiacov
    report.append("\n## 📅 Lexikálna Diverzita Podľa Mesiacov\n")
    report.append("![TTR by Month](ttr_by_month.png)\n")
    report.append("\n| Mesiac | User TTR | AI TTR | User Hapax | AI Hapax |")
    report.append("|--------|----------|--------|------------|----------|")
    for month in sorted(data['months'].keys()):
        m_user = data['months'][month]['user']
        m_ai = data['months'][month]['ai']
        report.append(f"| {month} | {m_user.get('ttr', 0):.4f} | {m_ai.get('ttr', 0):.4f} | {m_user.get('hapax_count', 0):,} | {m_ai.get('hapax_count', 0):,} |")
    
    # Top sessions
    report.append("\n## 💬 Top Sessions - Lexikálna Analýza\n")
    report.append("| Session | User TTR | AI TTR | User Unique | AI Unique |")
    report.append("|---------|----------|--------|-------------|-----------|")
    for session in list(data['sessions'].keys())[:10]:
        s_user = data['sessions'][session]['user']
        s_ai = data['sessions'][session]['ai']
        session_short = session[:8] + '...' if len(session) > 8 else session
        report.append(f"| `{session_short}` | {s_user.get('ttr', 0):.4f} | {s_ai.get('ttr', 0):.4f} | {s_user.get('unique_words', 0):,} | {s_ai.get('unique_words', 0):,} |")
    
    # Interpretácia
    report.append("\n## 💡 Interpretácia\n")
    
    if user_m.get('ttr', 0) > ai_m.get('ttr', 0):
        report.append("- **User má vyššiu lexikálnu diverzitu** (vyšší TTR) - používaš rozmanitejšiu slovnú zásobu")
    else:
        report.append("- **AI má vyššiu lexikálnu diverzitu** - AI používa rozmanitejšiu slovnú zásobu")
    
    if data['user']['lexical_density'] > data['ai']['lexical_density']:
        report.append("- **User má vyššiu lexikálnu hustotu** - viac obsahových slov vs. funkčných")
    else:
        report.append("- **AI má vyššiu lexikálnu hustotu** - viac obsahových slov")
    
    user_zipf_slope = data['user']['zipf'].get('zipf_slope', -1)
    report.append(f"- **Zipfov parameter (User):** {user_zipf_slope:.3f} (typicky -1.0 až -1.5)")
    report.append(f"- **Zipfov parameter (AI):** {data['ai']['zipf'].get('zipf_slope', -1):.3f}")
    
    return "\n".join(report)


def main():
    """Hlavná funkcia"""
    print("="*60)
    print("📊 LEXIKÁLNA ANALÝZA KONVERZÁCIÍ")
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
    data = analyze_lexical(records)
    
    # Vytvorenie vizualizácií
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    create_comparison_plots(data, OUTPUT_DIR)
    
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

