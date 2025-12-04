#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Rozdelí všetky prompty po týždňoch a vytvorí PDF súbory.

Načíta prompty z:
- data/prompts/prompts_split/ (historické)
- xvadur/data/prompts_log.jsonl (aktuálne)

Vytvorí:
- Markdown dokument pre každý týždeň
- PDF súbor pre každý týždeň
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from typing import List, Dict
from collections import defaultdict

# Markdown to PDF
try:
    import markdown
    from weasyprint import HTML, CSS
    from weasyprint.text.fonts import FontConfiguration
except ImportError:
    print("❌ Chyba: Potrebuješ nainštalovať markdown a weasyprint")
    print("   pip install markdown weasyprint")
    sys.exit(1)

# Konfigurácia
PROMPTS_SPLIT_DIR = Path("data/prompts/prompts_split")
PROMPTS_LOG_PATH = Path("xvadur/data/prompts_log.jsonl")
OUTPUT_DIR = Path("data/prompts/weekly_pdfs")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def load_all_prompts() -> List[Dict]:
    """Načíta všetky prompty z prompts_split a prompts_log."""
    prompts = []
    
    # Načítaj z prompts_split
    print("📖 Načítavam prompty z prompts_split...")
    for day_dir in sorted(PROMPTS_SPLIT_DIR.glob("*")):
        if not day_dir.is_dir():
            continue
        
        for json_file in sorted(day_dir.glob("*.json")):
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                text = data.get("text", "")
                if not text:
                    continue
                
                date_str = data.get("date", day_dir.name)
                try:
                    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
                    # Normalizuj na naive datetime
                    if date_obj.tzinfo is not None:
                        date_obj = date_obj.replace(tzinfo=None)
                except:
                    continue
                
                prompts.append({
                    "date": date_str,
                    "date_obj": date_obj,
                    "text": text,
                    "timestamp": data.get("timestamp", ""),
                    "word_count": data.get("word_count", len(text.split())),
                    "source": "prompts_split"
                })
            except Exception as e:
                print(f"⚠️  Chyba pri načítaní {json_file}: {e}")
                continue
    
    # Načítaj z prompts_log
    print("📖 Načítavam prompty z prompts_log...")
    if PROMPTS_LOG_PATH.exists():
        with open(PROMPTS_LOG_PATH, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                try:
                    data = json.loads(line)
                    if data.get("role") != "user":
                        continue
                    
                    content = data.get("content", "")
                    if not content:
                        continue
                    
                    timestamp_str = data.get("timestamp", "")
                    if timestamp_str:
                        try:
                            if '+' in timestamp_str or timestamp_str.endswith('Z'):
                                date_obj = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
                            else:
                                date_obj = datetime.fromisoformat(timestamp_str)
                            
                            # Normalizuj na naive datetime
                            if date_obj.tzinfo is not None:
                                date_obj = date_obj.replace(tzinfo=None)
                            
                            date_str = date_obj.strftime("%Y-%m-%d")
                        except:
                            continue
                    else:
                        continue
                    
                    prompts.append({
                        "date": date_str,
                        "date_obj": date_obj,
                        "text": content,
                        "timestamp": timestamp_str,
                        "word_count": len(content.split()),
                        "source": "prompts_log"
                    })
                except json.JSONDecodeError:
                    continue
                except Exception as e:
                    print(f"⚠️  Chyba pri načítaní riadku {line_num}: {e}")
                    continue
    
    print(f"✅ Načítaných {len(prompts)} promptov celkom")
    return prompts


def group_by_week(prompts: List[Dict]) -> Dict[str, List[Dict]]:
    """Rozdelí prompty podľa týždňov (ISO týždeň)."""
    weeks = defaultdict(list)
    
    for prompt in prompts:
        date_obj = prompt.get('date_obj')
        if not date_obj:
            continue
        
        # ISO týždeň: (rok, týždeň, deň)
        iso_week = date_obj.isocalendar()
        week_key = f"{iso_week[0]}-W{iso_week[1]:02d}"
        
        weeks[week_key].append(prompt)
    
    # Zoraď prompty v každom týždni podľa dátumu
    for week_key in weeks:
        weeks[week_key].sort(key=lambda x: x.get('date_obj', datetime.min))
    
    return dict(sorted(weeks.items()))


def create_markdown(week_key: str, prompts: List[Dict]) -> str:
    """Vytvorí markdown dokument pre týždeň."""
    # Extrahuj rok a týždeň
    year, week_num = week_key.split('-W')
    week_num = int(week_num)
    
    # Nájdi prvý a posledný deň týždňa
    first_prompt = prompts[0]
    last_prompt = prompts[-1]
    first_date = first_prompt['date']
    last_date = last_prompt['date']
    
    # Štatistiky
    total_prompts = len(prompts)
    total_words = sum(p.get('word_count', 0) for p in prompts)
    
    # Vytvor markdown
    md_lines = [
        f"# Prompty - Týždeň {week_num}, {year}",
        "",
        f"**Obdobie:** {first_date} - {last_date}",
        f"**Počet promptov:** {total_prompts}",
        f"**Celkový word count:** {total_words:,}",
        "",
        "---",
        "",
    ]
    
    # Skupina podľa dní
    current_date = None
    for prompt in prompts:
        date_str = prompt['date']
        
        if date_str != current_date:
            if current_date is not None:
                md_lines.append("")
            md_lines.append(f"## {date_str}")
            md_lines.append("")
            current_date = date_str
        
        # Prompt text
        text = prompt['text']
        timestamp = prompt.get('timestamp', '')
        word_count = prompt.get('word_count', 0)
        
        md_lines.append(f"**Timestamp:** {timestamp} | **Words:** {word_count}")
        md_lines.append("")
        md_lines.append(text)
        md_lines.append("")
        md_lines.append("---")
        md_lines.append("")
    
    return "\n".join(md_lines)


def markdown_to_pdf(markdown_content: str, output_path: Path):
    """Konvertuje markdown do PDF pomocou weasyprint."""
    # Konvertuj markdown na HTML
    html_content = markdown.markdown(
        markdown_content,
        extensions=['extra', 'codehilite', 'nl2br']
    )
    
    # CSS pre PDF
    css_content = """
    @page {
        size: A4;
        margin: 2cm;
    }
    body {
        font-family: 'Helvetica', 'Arial', sans-serif;
        font-size: 11pt;
        line-height: 1.6;
        color: #333;
    }
    h1 {
        font-size: 24pt;
        margin-top: 0;
        margin-bottom: 1em;
        color: #000;
        border-bottom: 2px solid #000;
        padding-bottom: 0.5em;
    }
    h2 {
        font-size: 18pt;
        margin-top: 1.5em;
        margin-bottom: 0.5em;
        color: #333;
        border-bottom: 1px solid #ccc;
        padding-bottom: 0.3em;
    }
    h3 {
        font-size: 14pt;
        margin-top: 1em;
        margin-bottom: 0.5em;
        color: #555;
    }
    p {
        margin: 0.5em 0;
    }
    code {
        background-color: #f5f5f5;
        padding: 2px 4px;
        border-radius: 3px;
        font-family: 'Courier New', monospace;
        font-size: 10pt;
    }
    pre {
        background-color: #f5f5f5;
        padding: 1em;
        border-radius: 5px;
        overflow-x: auto;
    }
    hr {
        border: none;
        border-top: 1px solid #ccc;
        margin: 1em 0;
    }
    """
    
    # Vytvor HTML dokument
    html_doc = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>{css_content}</style>
    </head>
    <body>
        {html_content}
    </body>
    </html>
    """
    
    # Konvertuj na PDF
    try:
        HTML(string=html_doc).write_pdf(output_path)
        return True
    except Exception as e:
        print(f"❌ Chyba pri vytváraní PDF: {e}")
        return False


def main():
    """Hlavná funkcia."""
    print("=" * 60)
    print("📚 ROZDELENIE PROMPTOV PO TÝŽDŇOCH A VYTVORENIE PDF")
    print("=" * 60)
    print()
    
    # Načítaj prompty
    prompts = load_all_prompts()
    
    if not prompts:
        print("❌ Žiadne prompty na spracovanie!")
        return
    
    # Rozdel podľa týždňov
    print("\n📅 Rozdeľujem prompty podľa týždňov...")
    weeks = group_by_week(prompts)
    print(f"✅ Nájdených {len(weeks)} týždňov")
    
    # Vytvor PDF pre každý týždeň
    print("\n📄 Vytváram PDF súbory...")
    success_count = 0
    error_count = 0
    
    for week_key, week_prompts in weeks.items():
        print(f"\n📅 Spracovávam {week_key} ({len(week_prompts)} promptov)...")
        
        # Vytvor markdown
        markdown_content = create_markdown(week_key, week_prompts)
        
        # Ulož markdown (voliteľné)
        md_path = OUTPUT_DIR / f"prompts_{week_key}.md"
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        
        # Vytvor PDF
        pdf_path = OUTPUT_DIR / f"prompts_{week_key}.pdf"
        if markdown_to_pdf(markdown_content, pdf_path):
            print(f"   ✅ PDF vytvorené: {pdf_path.name}")
            success_count += 1
        else:
            print(f"   ❌ Chyba pri vytváraní PDF pre {week_key}")
            error_count += 1
    
    print("\n" + "=" * 60)
    print("✅ HOTOVO!")
    print("=" * 60)
    print(f"📊 Úspešných: {success_count}")
    print(f"❌ Chýb: {error_count}")
    print(f"📁 Výstupný adresár: {OUTPUT_DIR}")
    print("\n💡 Súbory:")
    print(f"   - Markdown: {OUTPUT_DIR}/*.md")
    print(f"   - PDF: {OUTPUT_DIR}/*.pdf")


if __name__ == "__main__":
    main()


