#!/usr/bin/env python3
"""
Porovnanie metrík: Historické prompty vs. Kortex backup
"""

import json
from pathlib import Path
from datetime import datetime

workspace_root = Path(__file__).parent.parent

print("📊 POROVNANIE: Historické Prompty vs. Kortex Backup\n")

# Načítame Kortex metriky
kortex_file = workspace_root / "xvadur/data/kortex_analysis/kortex_monthly_metrics.json"
with open(kortex_file, 'r') as f:
    kortex_data = json.load(f)

# Historické metriky (z README)
historical = {
    '2025-07': {'prompts': 153, 'words': 23539, 'sentences': 1198, 'median_sentences': 5.0, 'name': 'Júl 2025'},
    '2025-08': {'prompts': 185, 'words': 51506, 'sentences': 2337, 'median_sentences': 6.0, 'name': 'August 2025'},
    '2025-09': {'prompts': 214, 'words': 124768, 'sentences': 5559, 'median_sentences': 10.0, 'name': 'September 2025'},
    '2025-10': {'prompts': 96, 'words': 45490, 'sentences': 2415, 'median_sentences': 13.0, 'name': 'Október 2025'},
    '2025-11': {'prompts': 16, 'words': 7053, 'sentences': 378, 'median_sentences': 12.0, 'name': 'November 2025'},
}

kortex_months = kortex_data['months']

# Vytvoríme porovnanie
print("=" * 100)
print(f"{'Mesiac':<20} {'Historické':<30} {'Kortex Backup':<30} {'Rozdiel':<30}")
print("=" * 100)
print(f"{'':<20} {'Prompty':<10} {'Words':<15} {'Prompty':<10} {'Words':<15} {'Prompty':<10} {'Words':<15}")
print("-" * 100)

total_historical_prompts = 0
total_historical_words = 0
total_kortex_prompts = 0
total_kortex_words = 0

for month_key in sorted(kortex_months.keys()):
    k = kortex_months[month_key]
    
    # Nájdeme historické metriky
    h = historical.get(month_key, {})
    h_prompts = h.get('prompts', 0)
    h_words = h.get('words', 0)
    h_name = h.get('name', month_key)
    
    k_prompts = k['prompt_count']
    k_words = k['total_words']
    
    diff_prompts = k_prompts - h_prompts
    diff_words = k_words - h_words
    
    if h_prompts > 0:
        month_name = h_name
    else:
        month_names = {
            '2025-07': 'Júl 2025', '2025-08': 'August 2025', '2025-09': 'September 2025',
            '2025-10': 'Október 2025', '2025-11': 'November 2025', '2025-12': 'December 2025'
        }
        month_name = month_names.get(month_key, month_key)
    
    print(f"{month_name:<20} {h_prompts:<10} {h_words:<15,} {k_prompts:<10} {k_words:<15,} {diff_prompts:+d} {diff_words:+,}")
    
    total_historical_prompts += h_prompts
    total_historical_words += h_words
    total_kortex_prompts += k_prompts
    total_kortex_words += k_words

print("-" * 100)
print(f"{'CELKOM':<20} {total_historical_prompts:<10} {total_historical_words:<15,} {total_kortex_prompts:<10} {total_kortex_words:<15,} {total_kortex_prompts - total_historical_prompts:+d} {total_kortex_words - total_historical_words:+,}")
print("=" * 100)

print(f"\n📈 ROZDIELY:")
print(f"   Prompty: {total_kortex_prompts - total_historical_prompts:+d} ({((total_kortex_prompts / total_historical_prompts - 1) * 100) if total_historical_prompts > 0 else 0:.1f}%)")
print(f"   Words: {total_kortex_words - total_historical_words:+,} ({((total_kortex_words / total_historical_words - 1) * 100) if total_historical_words > 0 else 0:.1f}%)")

# Vytvoríme markdown tabuľku
output_file = workspace_root / "xvadur/data/kortex_analysis/comparison_historical_vs_kortex.md"

markdown = f"""# 📊 Porovnanie: Historické Prompty vs. Kortex Backup

**Vytvorené:** {datetime.now().strftime('%Y-%m-%d %H:%M')}

---

## 📈 Porovnanie Metrík podľa Mesiacov

| Mesiac | Historické Prompty | Kortex Backup | Rozdiel |
|--------|-------------------|---------------|---------|
|        | Prompty | Words   | Prompty | Words   | Prompty | Words   |
|--------|---------|---------|---------|---------|---------|---------|
"""

for month_key in sorted(kortex_months.keys()):
    k = kortex_months[month_key]
    h = historical.get(month_key, {})
    
    h_prompts = h.get('prompts', 0)
    h_words = h.get('words', 0)
    h_name = h.get('name', '')
    
    if not h_name:
        month_names = {
            '2025-07': 'Júl 2025', '2025-08': 'August 2025', '2025-09': 'September 2025',
            '2025-10': 'Október 2025', '2025-11': 'November 2025', '2025-12': 'December 2025'
        }
        h_name = month_names.get(month_key, month_key)
    
    k_prompts = k['prompt_count']
    k_words = k['total_words']
    
    diff_prompts = k_prompts - h_prompts
    diff_words = k_words - h_words
    
    markdown += f"| {h_name} | {h_prompts} | {h_words:,} | {k_prompts} | {k_words:,} | +{diff_prompts} | +{diff_words:,} |\n"

markdown += f"""
---

## 📊 Celkové Rozdiely

| Metrika | Historické | Kortex Backup | Rozdiel |
|---------|-----------|---------------|---------|
| **Prompty** | {total_historical_prompts} | {total_kortex_prompts} | +{total_kortex_prompts - total_historical_prompts} ({((total_kortex_prompts / total_historical_prompts - 1) * 100) if total_historical_prompts > 0 else 0:.1f}%) |
| **Words** | {total_historical_words:,} | {total_kortex_words:,} | +{total_kortex_words - total_historical_words:,} ({((total_kortex_words / total_historical_words - 1) * 100) if total_historical_words > 0 else 0:.1f}%) |

---

**Automaticky vygenerované:** {datetime.now().strftime('%Y-%m-%d %H:%M')}
"""

with open(output_file, 'w', encoding='utf-8') as f:
    f.write(markdown)

print(f"\n💾 Porovnanie uložené: {output_file}")

