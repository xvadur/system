#!/usr/bin/env python3
"""
Analýza metrík Kortex backup promptov podľa mesiacov.
Vypočíta: počet promptov, word count, počet viet, median viet, priemerná dĺžka.
"""

import json
import re
from pathlib import Path
from collections import defaultdict
from statistics import median
from datetime import datetime

workspace_root = Path(__file__).parent.parent
input_file = workspace_root / "xvadur" / "data" / "kortex_guaranteed" / "user_prompts_guaranteed.jsonl"
output_dir = workspace_root / "xvadur" / "data" / "kortex_analysis"
output_dir.mkdir(parents=True, exist_ok=True)

print("📊 Analýza Kortex Backup Metrík podľa Mesiacov\n")
print(f"📁 Input: {input_file}")
print(f"📁 Output: {output_dir}\n")


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


def load_kortex_prompts() -> list:
    """Načíta všetky prompty z Kortex backupu."""
    prompts = []
    
    if not input_file.exists():
        print(f"⚠️  Súbor neexistuje: {input_file}")
        return prompts
    
    print(f"📖 Načítavam prompty z Kortex backupu...")
    
    with open(input_file, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            try:
                data = json.loads(line)
                
                # Extrahuj dátum
                date_created = data.get("date_created", "")
                if not date_created:
                    continue
                
                try:
                    # ISO format s timezone
                    if date_created.endswith('Z'):
                        date = datetime.fromisoformat(date_created.replace('Z', '+00:00'))
                    elif '+' in date_created or date_created.count('-') >= 3:
                        date = datetime.fromisoformat(date_created)
                    else:
                        continue
                except Exception as e:
                    continue
                
                text = data.get("extracted_text", "")
                if not text:
                    continue
                
                word_count = data.get("word_count", count_words(text))
                sentence_count = count_sentences(text)
                
                prompts.append({
                    "date": date,
                    "text": text,
                    "word_count": word_count,
                    "sentence_count": sentence_count,
                    "text_length": len(text),
                })
            except Exception as e:
                continue
    
    print(f"✅ Načítaných {len(prompts)} promptov")
    return prompts


def calculate_monthly_metrics(prompts: list) -> dict:
    """Vypočíta metriky pre každý mesiac."""
    monthly_data = defaultdict(lambda: {
        "prompts": [],
        "word_counts": [],
        "sentence_counts": [],
        "text_lengths": [],
    })
    
    for prompt in prompts:
        date = prompt["date"]
        month_key = f"{date.year}-{date.month:02d}"
        
        monthly_data[month_key]["prompts"].append(prompt)
        monthly_data[month_key]["word_counts"].append(prompt["word_count"])
        monthly_data[month_key]["sentence_counts"].append(prompt["sentence_count"])
        monthly_data[month_key]["text_lengths"].append(prompt["text_length"])
    
    # Vypočíta finálne metriky
    metrics = {}
    for month_key, data in monthly_data.items():
        prompts_list = data["prompts"]
        word_counts = data["word_counts"]
        sentence_counts = data["sentence_counts"]
        text_lengths = data["text_lengths"]
        
        if not prompts_list:
            continue
        
        metrics[month_key] = {
            "prompt_count": len(prompts_list),
            "total_words": sum(word_counts),
            "total_sentences": sum(sentence_counts),
            "avg_words": sum(word_counts) / len(word_counts) if word_counts else 0,
            "median_words": median(word_counts) if word_counts else 0,
            "avg_sentences": sum(sentence_counts) / len(sentence_counts) if sentence_counts else 0,
            "median_sentences": median(sentence_counts) if sentence_counts else 0,
            "avg_text_length": sum(text_lengths) / len(text_lengths) if text_lengths else 0,
            "total_text_length": sum(text_lengths),
        }
    
    return metrics


def format_month_name(month_key: str) -> str:
    """Formátuje názov mesiaca."""
    year, month = month_key.split('-')
    month_names = {
        '01': 'Január', '02': 'Február', '03': 'Marec', '04': 'Apríl',
        '05': 'Máj', '06': 'Jún', '07': 'Júl', '08': 'August',
        '09': 'September', '10': 'Október', '11': 'November', '12': 'December'
    }
    month_name = month_names.get(month, month)
    return f"{month_name} {year}"


def generate_markdown_table(metrics: dict) -> str:
    """Vygeneruje Markdown tabuľku s metrikami."""
    lines = []
    
    # Header
    lines.append("| Mesiac | Počet Promptov | Word Count | Priem. Words | Median Words | Počet Viet | Priem. Viet | Median Viet | Priem. Znaky |")
    lines.append("|--------|---------------|------------|--------------|--------------|------------|-------------|-------------|--------------|")
    
    # Zoradíme podľa mesiaca
    sorted_months = sorted(metrics.keys())
    
    for month_key in sorted_months:
        m = metrics[month_key]
        month_name = format_month_name(month_key)
        
        lines.append(
            f"| {month_name} | {m['prompt_count']} | {m['total_words']:,} | "
            f"{m['avg_words']:.1f} | {m['median_words']:.1f} | {m['total_sentences']:,} | "
            f"{m['avg_sentences']:.1f} | {m['median_sentences']:.1f} | {m['avg_text_length']:.0f} |"
        )
    
    # Total
    total_prompts = sum(m['prompt_count'] for m in metrics.values())
    total_words = sum(m['total_words'] for m in metrics.values())
    total_sentences = sum(m['total_sentences'] for m in metrics.values())
    total_text_length = sum(m['total_text_length'] for m in metrics.values())
    avg_words = total_words / total_prompts if total_prompts > 0 else 0
    avg_sentences = total_sentences / total_prompts if total_prompts > 0 else 0
    avg_text_length = total_text_length / total_prompts if total_prompts > 0 else 0
    
    lines.append("")
    lines.append(f"**Celkom:** {total_prompts} promptov, {total_words:,} slov, {total_sentences:,} viet")
    lines.append(f"**Priemer:** {avg_words:.1f} slov/prompt, {avg_sentences:.1f} viet/prompt, {avg_text_length:.0f} znakov/prompt")
    
    return "\n".join(lines)


def main():
    """Hlavná funkcia."""
    
    # Načítame prompty
    prompts = load_kortex_prompts()
    
    if not prompts:
        print("❌ Žiadne prompty na analýzu")
        return
    
    # Vypočítame metriky
    print(f"\n📊 Počítam metriky podľa mesiacov...")
    metrics = calculate_monthly_metrics(prompts)
    
    print(f"✅ Metriky vypočítané pre {len(metrics)} mesiacov\n")
    
    # Vypíšeme výsledky
    print("=" * 80)
    print("📊 METRICKY PODĽA MESIACOV")
    print("=" * 80)
    
    for month_key in sorted(metrics.keys()):
        m = metrics[month_key]
        month_name = format_month_name(month_key)
        
        print(f"\n📅 {month_name}:")
        print(f"   Prompty: {m['prompt_count']}")
        print(f"   Word count: {m['total_words']:,} (priemer: {m['avg_words']:.1f}, median: {m['median_words']:.1f})")
        print(f"   Vety: {m['total_sentences']:,} (priemer: {m['avg_sentences']:.1f}, median: {m['median_sentences']:.1f})")
        print(f"   Priem. dĺžka: {m['avg_text_length']:.0f} znakov")
    
    # Uložíme výsledky
    output_file = output_dir / "kortex_monthly_metrics.md"
    
    # Vygenerujeme Markdown dokument
    markdown_content = f"""# 📊 Kortex Backup Metriky podľa Mesiacov

**Vytvorené:** {datetime.now().strftime('%Y-%m-%d %H:%M')}  
**Zdroj:** `xvadur/data/dataset/prompts.jsonl`  
**Celkom promptov:** {len(prompts)}

---

## 📈 Metriky podľa Mesiacov

{generate_markdown_table(metrics)}

---

## 📊 Štatistiky

### Rozdelenie podľa Dĺžky

"""
    
    # Pridáme štatistiky
    all_word_counts = [p["word_count"] for p in prompts]
    all_sentence_counts = [p["sentence_count"] for p in prompts]
    
    markdown_content += f"""
- **Celkom promptov:** {len(prompts):,}
- **Celkom slov:** {sum(all_word_counts):,}
- **Celkom viet:** {sum(all_sentence_counts):,}
- **Priemerný počet slov:** {sum(all_word_counts) / len(all_word_counts):.1f}
- **Median slov:** {median(all_word_counts):.1f}
- **Priemerný počet viet:** {sum(all_sentence_counts) / len(all_sentence_counts):.1f}
- **Median viet:** {median(all_sentence_counts):.1f}

---

**Automaticky vygenerované:** {datetime.now().strftime('%Y-%m-%d %H:%M')}
"""
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(markdown_content)
    
    print(f"\n💾 Výsledky uložené: {output_file}")
    
    # Uložíme aj JSON pre ďalšie spracovanie
    json_file = output_dir / "kortex_monthly_metrics.json"
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump({
            "generated_at": datetime.now().isoformat(),
            "total_prompts": len(prompts),
            "months": metrics,
        }, f, indent=2, ensure_ascii=False)
    
    print(f"💾 JSON uložený: {json_file}")
    print("\n🎉 Analýza dokončená!")


if __name__ == "__main__":
    main()

