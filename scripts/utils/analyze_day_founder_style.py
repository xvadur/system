#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kontinuálna Analýza: Founder's Audit Style

Vytvorí analýzu konkrétneho dňa v štýle "Founder's Audit" (ako v analyza.md).
Môže analyzovať jeden deň alebo batch všetkých dní.

Štýl analýzy:
- Founder's Audit perspektíva
- Kritický rozbor (nie len pozitívne)
- Identifikácia vzorcov (Time Compression, Polymath, AI Native, atď.)
- Red Flags (kritické feedbacky)
- Záver s hodnotením
"""

import json
import sys
import os
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional
from collections import defaultdict

# OpenAI
try:
    from openai import OpenAI
except ImportError:
    print("❌ Chyba: Potrebuješ nainštalovať openai")
    print("   pip install openai")
    sys.exit(1)

# Konfigurácia
PROMPTS_ENRICHED = Path("data/prompts/prompts_enriched.jsonl")
PROMPTS_SPLIT_DIR = Path("data/prompts/prompts_split")
PROMPTS_LOG_PATH = Path("development/data/prompts_log.jsonl")
OUTPUT_DIR = Path("data/prompts/continuous_analysis")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# OpenRouter konfigurácia
MODEL = "tngtech/tng-r1t-chimera:free"  # FREE model cez OpenRouter
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

# OpenRouter API Key - načíta z .env súboru alebo environment
def load_api_key():
    """Načíta OpenRouter API key z .env súboru alebo environmentu."""
    # Najprv skús environment variable
    api_key = os.getenv("OPENROUTER_API_KEY")
    if api_key:
        return api_key
    
    # Potom skús .env súbor
    env_files = [
        Path(".env"),
        Path("mcp/.env")
    ]
    
    for env_file in env_files:
        if env_file.exists():
            try:
                with open(env_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        # Ignoruje komentáre a prázdne riadky
                        if line.startswith("#") or not line:
                            continue
                        if line.startswith("OPENROUTER_API_KEY="):
                            key = line.split("=", 1)[1].strip()
                            # Odstráni quotes ak existujú
                            key = key.strip('"').strip("'")
                            if key and key != "sk-...":
                                return key
            except Exception as e:
                print(f"⚠️  Chyba pri načítaní {env_file}: {e}")
                continue
    
    return None

API_KEY = load_api_key()
if not API_KEY:
    print("⚠️  OPENROUTER_API_KEY nie je nastavený")
    print("   Možnosti:")
    print("   1. Vytvor .env súbor v root adresári s: OPENROUTER_API_KEY=sk-or-v1-...")
    print("   2. Alebo nastav: export OPENROUTER_API_KEY='sk-or-v1-...'")
    sys.exit(1)


def load_prompts_by_date(target_date: str) -> Dict:
    """
    Načíta všetky prompty z konkrétneho dňa.
    
    Returns:
        Dict s:
        - enriched: List záznamov z prompts_enriched.jsonl
        - raw_texts: List originálnych textov z prompts_split
    """
    enriched = []
    raw_texts = []
    
    # Načítaj z enriched
    if PROMPTS_ENRICHED.exists():
        with open(PROMPTS_ENRICHED, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    data = json.loads(line)
                    if data.get('date') == target_date:
                        enriched.append(data)
                except:
                    continue
    
    # Načítaj originálne texty z prompts_split
    day_dir = PROMPTS_SPLIT_DIR / target_date
    if day_dir.exists() and day_dir.is_dir():
        for json_file in sorted(day_dir.glob("*.json")):
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    text = data.get("text", "")
                    if text:
                        raw_texts.append({
                            "prompt_id": f"{target_date}_{json_file.stem}",
                            "text": text,
                            "timestamp": data.get("timestamp", ""),
                            "word_count": data.get("word_count", len(text.split()))
                        })
            except:
                continue
    
    # Načítaj z prompts_log (aktuálne prompty)
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
                    
                    timestamp_str = data.get("timestamp", "")
                    if not timestamp_str:
                        continue
                    
                    # Extrahuj dátum z timestampu
                    try:
                        if '+' in timestamp_str or timestamp_str.endswith('Z'):
                            date_obj = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
                        else:
                            date_obj = datetime.fromisoformat(timestamp_str)
                        date_str = date_obj.strftime("%Y-%m-%d")
                        
                        if date_str == target_date:
                            text = data.get("content", "")
                            if text:
                                raw_texts.append({
                                    "prompt_id": f"current_{line_num}",
                                    "text": text,
                                    "timestamp": timestamp_str,
                                    "word_count": len(text.split())
                                })
                    except:
                        continue
                except:
                    continue
    
    return {
        "date": target_date,
        "enriched": enriched,
        "raw_texts": raw_texts,
        "total_prompts": len(enriched) + len(raw_texts)
    }


def create_founder_audit_prompt(day_data: Dict, profile_context: Optional[str] = None) -> str:
    """
    Vytvorí prompt pre LLM v štýle Founder's Audit.
    
    Štýl:
    - Founder's Audit perspektíva
    - Kritický rozbor
    - Identifikácia vzorcov
    - Red Flags
    - Záver
    """
    date = day_data["date"]
    enriched = day_data["enriched"]
    raw_texts = day_data["raw_texts"]
    
    # Zostav kontext
    context_parts = []
    
    # Základné štatistiky
    total_prompts = len(enriched) + len(raw_texts)
    total_words = sum(e.get('word_count', 0) for e in enriched) + sum(r.get('word_count', 0) for r in raw_texts)
    
    context_parts.append(f"**Dátum:** {date}")
    context_parts.append(f"**Počet promptov:** {total_prompts}")
    context_parts.append(f"**Celkový word count:** {total_words}")
    
    # Aktivity
    if enriched:
        activities = [e.get('activity') for e in enriched if e.get('activity')]
        if activities:
            context_parts.append(f"\n**Aktivity:**")
            for i, act in enumerate(activities[:5], 1):  # Top 5
                context_parts.append(f"{i}. {act}")
    
    # Myšlienky
    if enriched:
        thoughts = [e.get('thoughts') for e in enriched if e.get('thoughts')]
        if thoughts:
            context_parts.append(f"\n**Myšlienky:**")
            for i, thought in enumerate(thoughts[:5], 1):  # Top 5
                context_parts.append(f"{i}. {thought}")
    
    # Sentiment
    if enriched:
        sentiments = [e.get('sentiment') for e in enriched if e.get('sentiment')]
        if sentiments:
            sentiment_counts = defaultdict(int)
            for s in sentiments:
                sentiment_counts[s] += 1
            context_parts.append(f"\n**Sentiment:** {dict(sentiment_counts)}")
    
    # Projekty a technológie
    if enriched:
        all_projects = []
        all_tech = []
        for e in enriched:
            context_obj = e.get('context', {})
            if isinstance(context_obj, dict):
                all_projects.extend(context_obj.get('projects', []))
                all_tech.extend(context_obj.get('technologies', []))
        
        if all_projects:
            unique_projects = list(set(all_projects))
            context_parts.append(f"\n**Projekty:** {', '.join(unique_projects[:10])}")
        if all_tech:
            unique_tech = list(set(all_tech))
            context_parts.append(f"\n**Technológie:** {', '.join(unique_tech[:10])}")
    
    # Originálne texty (prvých 3 pre kontext)
    if raw_texts:
        context_parts.append(f"\n**Originálne prompty (výber):**")
        for i, prompt in enumerate(raw_texts[:3], 1):
            text_preview = prompt['text'][:500] + "..." if len(prompt['text']) > 500 else prompt['text']
            context_parts.append(f"\n**Prompt {i}:**\n{text_preview}")
    
    context = "\n".join(context_parts)
    
    # Profile context (ak je poskytnutý)
    profile_section = ""
    if profile_context:
        profile_section = f"""
## KONTEXT: ADAM PROFILE
{profile_context}

---
"""
    
    # Prompt pre LLM
    prompt = f"""# FOUNDER'S AUDIT: Analýza Dňa {date}

{profile_section}

## DÁTA Z DŇA {date}

{context}

---

## INŠTRUKCIE

Urob analýzu tohto dňa z pohľadu **Foundera** (ako v analyza.md).

**Tvoj štýl:**
- Priamy, analytický, bez obalu
- Kritický rozbor (nie len pozitívne)
- Identifikácia vzorcov a trendov
- Red Flags (kritické feedbacky)
- Záver s hodnotením

**Štruktúra analýzy:**

### FOUNDER'S AUDIT: Adam Rudavský (Snapshot: {date})

**Verdikt:** [Krátke hodnotenie - High-Variance Individual? Lineárny? Exponenciálny?]

**Kritický rozbor:**

#### 1. [Identifikovaný Vzorec/Téma]
> *[Citácia z promptov]*

**Founderov pohľad:**
[Analýza z pohľadu foundera - čo to znamená, prečo je to dôležité]

**Analýza:** [Hlbšia analýza vzorca]

#### 2. [Ďalší Vzorec/Téma]
...

### KRITICKÝ FEEDBACK (The "Red Flags")

[Ak existujú red flags - identifikuj ich a vysvetli]

### ZÁVER: Kto si?

**Si [hodnotenie] s [charakteristiky].**

[Záverečné hodnotenie a odporúčania]

**Môj odkaz pre teba:**
[Krátka správa/odporúčanie]

---

**Dôležité:**
- Používaj konkrétne citácie z promptov
- Buď kritický, ale aj spravodlivý
- Identifikuj vzorce, nie len opíš fakty
- Founder's perspektíva = biznis, trakcia, udržateľnosť, riziká
"""
    
    return prompt


def analyze_day(target_date: str, client: OpenAI, profile_context: Optional[str] = None) -> Optional[str]:
    """
    Analyzuje konkrétny deň v štýle Founder's Audit.
    
    Returns:
        Analýza ako string (markdown) alebo None ak chyba
    """
    print(f"\n📅 Analyzujem deň: {target_date}")
    
    # Načítaj dáta
    day_data = load_prompts_by_date(target_date)
    
    if day_data["total_prompts"] == 0:
        print(f"   ⚠️  Žiadne prompty pre {target_date}")
        return None
    
    print(f"   ✅ Načítaných {day_data['total_prompts']} promptov")
    
    # Vytvor prompt
    prompt = create_founder_audit_prompt(day_data, profile_context)
    
    # Zavolaj LLM
    try:
        print(f"   🤖 Volám {MODEL}...")
        
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "Si skúsený founder a investor, ktorý robí audit trakcie a výkonu. Tvoja analýza je priama, kritická, ale spravodlivá. Identifikuješ vzorce, riziká a príležitosti."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=2000
        )
        
        analysis = response.choices[0].message.content
        
        print(f"   ✅ Analýza vytvorená ({len(analysis)} znakov)")
        return analysis
        
    except Exception as e:
        print(f"   ❌ Chyba: {e}")
        return None


def save_analysis(date: str, analysis: str) -> Path:
    """Uloží analýzu do markdown súboru."""
    output_file = OUTPUT_DIR / f"analysis_{date}.md"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(analysis)
        f.write("\n\n---\n\n")
        f.write(f"**Vytvorené:** {datetime.now().isoformat()}\n")
        f.write(f"**Model:** {MODEL}\n")
    
    return output_file


def get_all_dates() -> List[str]:
    """Získa zoznam všetkých dátumov s promptmi."""
    dates = set()
    
    # Z enriched
    if PROMPTS_ENRICHED.exists():
        with open(PROMPTS_ENRICHED, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    data = json.loads(line)
                    date = data.get('date')
                    if date:
                        dates.add(date)
                except:
                    continue
    
    # Z prompts_split
    for day_dir in PROMPTS_SPLIT_DIR.glob("*"):
        if day_dir.is_dir():
            dates.add(day_dir.name)
    
    # Z prompts_log
    if PROMPTS_LOG_PATH.exists():
        with open(PROMPTS_LOG_PATH, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    data = json.loads(line)
                    if data.get("role") != "user":
                        continue
                    
                    timestamp_str = data.get("timestamp", "")
                    if timestamp_str:
                        try:
                            if '+' in timestamp_str or timestamp_str.endswith('Z'):
                                date_obj = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
                            else:
                                date_obj = datetime.fromisoformat(timestamp_str)
                            date_str = date_obj.strftime("%Y-%m-%d")
                            dates.add(date_str)
                        except:
                            continue
                except:
                    continue
    
    return sorted(list(dates))


def load_profile_context() -> Optional[str]:
    """Načíta kontext z xvadur_profile.md (len súčasný profil)."""
    profile_path = Path("development/data/profile/xvadur_profile.md")
    
    if not profile_path.exists():
        return None
    
    try:
        with open(profile_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Extrahuj len sekciu "IV. SÚČASNÝ PROFIL"
        if "## IV. SÚČASNÝ PROFIL" in content:
            start_idx = content.find("## IV. SÚČASNÝ PROFIL")
            # Nájdi koniec sekcie (ďalší ## alebo koniec súboru)
            next_section = content.find("\n## ", start_idx + 1)
            if next_section == -1:
                profile_section = content[start_idx:]
            else:
                profile_section = content[start_idx:next_section]
            
            return profile_section
        
        return None
    except:
        return None


def main():
    """Hlavná funkcia."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Kontinuálna analýza: Founder's Audit Style")
    parser.add_argument("--date", type=str, help="Konkrétny dátum (YYYY-MM-DD)")
    parser.add_argument("--all", action="store_true", help="Analyzovať všetky dni")
    parser.add_argument("--batch", action="store_true", help="Batch mode (resume functionality)")
    parser.add_argument("--limit", type=int, help="Limit počtu dní (pre --all)")
    args = parser.parse_args()
    
    # Inicializuj OpenRouter client
    client = OpenAI(
        api_key=API_KEY,
        base_url=OPENROUTER_BASE_URL,
        default_headers={
            "HTTP-Referer": "https://github.com/xvadur-workspace",
            "X-Title": "Continuous Analysis: Founder's Audit"
        }
    )
    
    # Načítaj profile context
    profile_context = load_profile_context()
    if profile_context:
        print("✅ Načítaný profile context")
    
    print("=" * 60)
    print("🔍 KONTINUÁLNA ANALÝZA: FOUNDER'S AUDIT STYLE")
    print("=" * 60)
    
    if args.date:
        # Analýza konkrétneho dňa
        analysis = analyze_day(args.date, client, profile_context)
        if analysis:
            output_file = save_analysis(args.date, analysis)
            print(f"\n✅ Analýza uložená: {output_file}")
        else:
            print(f"\n❌ Nepodarilo sa vytvoriť analýzu pre {args.date}")
    
    elif args.all:
        # Analýza všetkých dní
        all_dates = get_all_dates()
        
        if args.limit:
            all_dates = all_dates[:args.limit]
        
        print(f"\n📊 Celkom dní na analýzu: {len(all_dates)}")
        
        # Resume functionality
        existing_analyses = set()
        if args.batch:
            for analysis_file in OUTPUT_DIR.glob("analysis_*.md"):
                date_str = analysis_file.stem.replace("analysis_", "")
                existing_analyses.add(date_str)
            print(f"   ✅ Nájdených {len(existing_analyses)} existujúcich analýz (preskočím)")
        
        success_count = 0
        error_count = 0
        
        for i, date in enumerate(all_dates, 1):
            if args.batch and date in existing_analyses:
                print(f"\n[{i}/{len(all_dates)}] ⏭️  Preskakujem {date} (už existuje)")
                continue
            
            print(f"\n[{i}/{len(all_dates)}] 📅 {date}")
            
            analysis = analyze_day(date, client, profile_context)
            
            if analysis:
                output_file = save_analysis(date, analysis)
                success_count += 1
                print(f"   ✅ Uložené: {output_file.name}")
            else:
                error_count += 1
                print(f"   ❌ Chyba pri analýze")
            
            # Rate limiting
            if i < len(all_dates):
                import time
                time.sleep(1.1)  # 1.1s medzi requestmi
        
        print("\n" + "=" * 60)
        print("✅ HOTOVO!")
        print("=" * 60)
        print(f"📊 Úspešných: {success_count}")
        print(f"❌ Chýb: {error_count}")
        print(f"📁 Výstupný adresár: {OUTPUT_DIR}")
    
    else:
        parser.print_help()
        print("\n💡 Príklady:")
        print("   # Analýza konkrétneho dňa:")
        print("   python3 scripts/analyze_day_founder_style.py --date 2025-09-04")
        print("\n   # Analýza všetkých dní:")
        print("   python3 scripts/analyze_day_founder_style.py --all")
        print("\n   # Batch mode (preskočí už existujúce):")
        print("   python3 scripts/analyze_day_founder_style.py --all --batch")
        print("\n   # Limitovaný počet dní:")
        print("   python3 scripts/analyze_day_founder_style.py --all --limit 10")


if __name__ == "__main__":
    main()

