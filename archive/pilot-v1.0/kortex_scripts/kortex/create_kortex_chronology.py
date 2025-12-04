#!/usr/bin/env python3
"""
Vytvorenie chronológie z Kortex backup konverzačných párov.
Kompletný dialóg (user prompt + AI odpoveď) zoradený chronologicky podľa dátumov.
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from typing import List, Dict
from collections import defaultdict

workspace_root = Path(__file__).parent.parent
input_file = workspace_root / "xvadur" / "data" / "kortex_guaranteed" / "conversation_pairs_guaranteed.jsonl"
output_dir = workspace_root / "xvadur" / "data" / "kortex_chronology"

output_dir.mkdir(parents=True, exist_ok=True)

print("📅 Vytvorenie Chronológie z Kortex Backup Konverzácií\n")
print(f"📁 Input: {input_file}")
print(f"📁 Output: {output_dir}\n")


def load_conversation_pairs() -> List[Dict]:
    """Načíta všetky konverzačné páry."""
    pairs = []
    
    if not input_file.exists():
        print(f"⚠️  Súbor neexistuje: {input_file}")
        return pairs
    
    print(f"📖 Načítavam konverzačné páry...")
    
    with open(input_file, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            try:
                data = json.loads(line)
                
                user_prompt = data.get("user_prompt", {})
                ai_response = data.get("ai_response", {})
                
                user_text = user_prompt.get("extracted_text", "")
                ai_text = ai_response.get("extracted_text", "")
                
                if not user_text or not ai_text:
                    continue
                
                timestamp = data.get("timestamp", "")
                if not timestamp:
                    continue
                
                try:
                    # ISO format s timezone
                    if timestamp.endswith('Z'):
                        date_obj = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                    elif '+' in timestamp or timestamp.count('-') >= 3:
                        date_obj = datetime.fromisoformat(timestamp)
                    else:
                        continue
                except Exception:
                    continue
                
                pairs.append({
                    "date": date_obj.date(),
                    "datetime": date_obj,
                    "timestamp": timestamp,
                    "user_prompt": user_text,
                    "ai_response": ai_text,
                    "user_word_count": user_prompt.get("word_count", len(user_text.split())),
                    "ai_word_count": ai_response.get("word_count", len(ai_text.split())),
                    "session": data.get("session", ""),
                    "time_diff_seconds": data.get("time_diff_seconds", 0),
                })
            except Exception:
                continue
    
    print(f"✅ Načítaných {len(pairs)} konverzačných párov")
    return pairs


def group_by_date(pairs: List[Dict]) -> Dict[str, List[Dict]]:
    """Zoskupí konverzačné páry podľa dátumu."""
    grouped = defaultdict(list)
    
    for pair in pairs:
        date_str = pair["date"].strftime("%Y-%m-%d")
        grouped[date_str].append(pair)
    
    # Zoradíme páry v každom dni podľa času
    for date_str in grouped:
        grouped[date_str].sort(key=lambda x: x["datetime"])
    
    return dict(grouped)


def format_conversation_pair(pair: Dict, index: int) -> str:
    """Formátuje jeden konverzačný pár do Markdown."""
    user_text = pair["user_prompt"]
    ai_text = pair["ai_response"]
    time_str = pair["datetime"].strftime("%H:%M")
    
    lines = [
        f"\n### Konverzácia #{index} ({time_str})",
        "",
        "**Adam:**",
        f"{user_text}",
        "",
        "**AI:**",
        f"{ai_text}",
        "",
        "---",
    ]
    
    return "\n".join(lines)


def create_daily_chronology(date_str: str, pairs: List[Dict]) -> str:
    """Vytvorí chronológiu pre jeden deň."""
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    date_display = date_obj.strftime("%d. %B %Y")
    
    # Slovenské názvy mesiacov
    month_names = {
        1: 'januára', 2: 'februára', 3: 'marca', 4: 'apríla',
        5: 'mája', 6: 'júna', 7: 'júla', 8: 'augusta',
        9: 'septembra', 10: 'októbra', 11: 'novembra', 12: 'decembra'
    }
    
    day = date_obj.day
    month_name = month_names.get(date_obj.month, '')
    year = date_obj.year
    
    date_display_sk = f"{day}. {month_name} {year}"
    
    lines = [
        f"# Chronológia: {date_display_sk}",
        "",
        f"**Dátum:** {date_str}",
        f"**Počet konverzácií:** {len(pairs)}",
        "",
        "---",
    ]
    
    for i, pair in enumerate(pairs, 1):
        lines.append(format_conversation_pair(pair, i))
    
    # Štatistiky dňa
    total_user_words = sum(p["user_word_count"] for p in pairs)
    total_ai_words = sum(p["ai_word_count"] for p in pairs)
    avg_user_words = total_user_words / len(pairs) if pairs else 0
    avg_ai_words = total_ai_words / len(pairs) if pairs else 0
    
    lines.extend([
        "",
        "## 📊 Štatistiky Dňa",
        "",
        f"- **Celkom konverzácií:** {len(pairs)}",
        f"- **Celkom slov (Adam):** {total_user_words:,}",
        f"- **Celkom slov (AI):** {total_ai_words:,}",
        f"- **Priemer slov/prompt (Adam):** {avg_user_words:.1f}",
        f"- **Priemer slov/odpoveď (AI):** {avg_ai_words:.1f}",
        "",
        f"**Automaticky vygenerované:** {datetime.now().strftime('%Y-%m-%d %H:%M')}",
    ])
    
    return "\n".join(lines)


def create_monthly_chronology(month_key: str, dates: Dict[str, List[Dict]]) -> str:
    """Vytvorí chronológiu pre jeden mesiac."""
    year, month = month_key.split("-")
    month = int(month)
    
    month_names = {
        1: 'Január', 2: 'Február', 3: 'Marec', 4: 'Apríl',
        5: 'Máj', 6: 'Jún', 7: 'Júl', 8: 'August',
        9: 'September', 10: 'Október', 11: 'November', 12: 'December'
    }
    
    month_name = month_names.get(month, f"Mesiac {month}")
    month_display = f"{month_name} {year}"
    
    total_conversations = sum(len(pairs) for pairs in dates.values())
    total_days = len(dates)
    
    lines = [
        f"# Chronológia: {month_display}",
        "",
        f"**Mesiac:** {month_display}",
        f"**Aktívnych dní:** {total_days}",
        f"**Celkom konverzácií:** {total_conversations}",
        "",
        "---",
        "",
    ]
    
    # Zoradíme dátumy
    sorted_dates = sorted(dates.items())
    
    for date_str, pairs in sorted_dates:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        
        lines.append(f"## {date_obj.strftime('%d. %B %Y')}")
        lines.append("")
        lines.append(f"**Dátum:** {date_str} | **Konverzácií:** {len(pairs)}")
        lines.append("")
        
        for i, pair in enumerate(pairs, 1):
            time_str = pair["datetime"].strftime("%H:%M")
            lines.append(f"### {time_str}")
            lines.append("")
            lines.append(f"**Adam:** {pair['user_prompt'][:200]}...")
            lines.append("")
            lines.append(f"**AI:** {pair['ai_response'][:200]}...")
            lines.append("")
            lines.append("---")
            lines.append("")
    
    lines.append(f"\n**Automaticky vygenerované:** {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    
    return "\n".join(lines)


def main():
    """Hlavná funkcia."""
    
    # Načítame konverzačné páry
    pairs = load_conversation_pairs()
    
    if not pairs:
        print("❌ Žiadne konverzačné páry na spracovanie")
        return
    
    # Zoskupíme podľa dátumov
    print(f"\n📅 Zoskupujem podľa dátumov...")
    grouped_by_date = group_by_date(pairs)
    
    print(f"✅ Zoskupených do {len(grouped_by_date)} dní")
    
    # Zoskupíme podľa mesiacov
    grouped_by_month = defaultdict(dict)
    for date_str, date_pairs in grouped_by_date.items():
        year_month = date_str[:7]  # YYYY-MM
        grouped_by_month[year_month][date_str] = date_pairs
    
    print(f"✅ Zoskupených do {len(grouped_by_month)} mesiacov\n")
    
    # Vytvoríme denné chronológie
    print("📝 Vytváram denné chronológie...")
    daily_dir = output_dir / "daily"
    daily_dir.mkdir(exist_ok=True)
    
    for date_str, date_pairs in sorted(grouped_by_date.items()):
        chronology = create_daily_chronology(date_str, date_pairs)
        
        output_file = daily_dir / f"{date_str}.md"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(chronology)
        
        if len(list(daily_dir.glob("*.md"))) <= 5:  # Zobrazíme prvých 5
            print(f"  ✅ {date_str}.md ({len(date_pairs)} konverzácií)")
    
    print(f"  ✅ Vytvorených {len(grouped_by_date)} denných chronológií")
    
    # Vytvoríme mesačné chronológie
    print(f"\n📝 Vytváram mesačné chronológie...")
    monthly_dir = output_dir / "monthly"
    monthly_dir.mkdir(exist_ok=True)
    
    for month_key, month_dates in sorted(grouped_by_month.items()):
        chronology = create_monthly_chronology(month_key, month_dates)
        
        output_file = monthly_dir / f"{month_key}.md"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(chronology)
        
        total_conv = sum(len(pairs) for pairs in month_dates.values())
        print(f"  ✅ {month_key}.md ({total_conv} konverzácií, {len(month_dates)} dní)")
    
    print(f"  ✅ Vytvorených {len(grouped_by_month)} mesačných chronológií")
    
    # Vytvoríme index súbor
    index_file = output_dir / "README.md"
    index_content = f"""# 📅 Kortex Backup Chronológia

**Vytvorené:** {datetime.now().strftime('%Y-%m-%d %H:%M')}  
**Zdroj:** `xvadur/data/dataset/conversations.jsonl`

---

## 📊 Prehľad

- **Celkom konverzácií:** {len(pairs):,}
- **Aktívnych dní:** {len(grouped_by_date)}
- **Mesiacov:** {len(grouped_by_month)}
- **Časové obdobie:** {min(grouped_by_date.keys())} až {max(grouped_by_date.keys())}

---

## 📁 Súbory

### Denné Chronológie
- `daily/YYYY-MM-DD.md` - Kompletná chronológia pre jeden deň

### Mesačné Chronológie
- `monthly/YYYY-MM.md` - Súhrn chronológie pre jeden mesiac

---

## 📈 Štatistiky podľa Mesiacov

"""
    
    for month_key in sorted(grouped_by_month.keys()):
        month_dates = grouped_by_month[month_key]
        total_conv = sum(len(pairs) for pairs in month_dates.values())
        total_days = len(month_dates)
        
        index_content += f"- **{month_key}:** {total_conv} konverzácií, {total_days} aktívnych dní\n"
    
    index_content += f"""
---

**Automaticky vygenerované:** {datetime.now().strftime('%Y-%m-%d %H:%M')}
"""
    
    with open(index_file, 'w', encoding='utf-8') as f:
        f.write(index_content)
    
    print(f"\n💾 Index vytvorený: {index_file}")
    print(f"\n🎉 Chronológia vytvorená!")
    print(f"📁 Výsledky: {output_dir}")
    print(f"  - Denné: {daily_dir} ({len(grouped_by_date)} súborov)")
    print(f"  - Mesačné: {monthly_dir} ({len(grouped_by_month)} súborov)")


if __name__ == "__main__":
    main()

