import os
#!/usr/bin/env python3
"""
Chronologická syntéza príbehu z kategorizovaných promptov.
Vytvorí syntetizovaný naratív podľa rôznych perspektív.
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from typing import List, Dict
from collections import defaultdict

# OpenAI (pre OpenRouter)
try:
    from openai import OpenAI
except ImportError:
    print("❌ Chyba: Potrebuješ nainštalovať openai")
    print("   pip install openai")
    sys.exit(1)

# Konfigurácia
CATEGORIZED_FILE = Path("data/prompts/prompts_categorized.jsonl")
TEMPORAL_MAP_FILE = Path("data/prompts/temporal_map.json")
OUTPUT_DIR = Path("data/prompts/synthesis")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# OpenRouter konfigurácia
MODEL = "x-ai/grok-4.1-fast:free"
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY", "")
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"


def load_data() -> tuple:
    """Načíta kategorizované prompty a temporálnu mapu."""
    prompts = []
    with open(CATEGORIZED_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                try:
                    data = json.loads(line)
                    # Parsuj dátum
                    date_str = data.get('date', '')
                    if date_str:
                        try:
                            data['date_obj'] = datetime.strptime(date_str, "%Y-%m-%d")
                        except:
                            continue
                    prompts.append(data)
                except:
                    continue
    
    prompts.sort(key=lambda x: x.get('date_obj', datetime.min))
    
    temporal_map = {}
    if TEMPORAL_MAP_FILE.exists():
        with open(TEMPORAL_MAP_FILE, 'r', encoding='utf-8') as f:
            temporal_map = json.load(f)
    
    return prompts, temporal_map


def synthesize_by_period(prompts: List[Dict], client: OpenAI, period_days: int = 30) -> Dict:
    """
    Syntetizuje príbeh podľa časových období (mesiace).
    """
    print(f"\n📅 Syntetizujem podľa časových období ({period_days} dní)...")
    
    # Zoskupiť prompty podľa období
    periods = defaultdict(list)
    
    for prompt in prompts:
        date_obj = prompt.get('date_obj')
        if not date_obj:
            continue
        
        # Vypočítaj obdobie (mesiac)
        period_key = date_obj.strftime("%Y-%m")
        periods[period_key].append(prompt)
    
    syntheses = {}
    
    for period, period_prompts in sorted(periods.items()):
        print(f"   Syntetizujem {period} ({len(period_prompts)} promptov)...")
        
        # Zostav kontext
        context_parts = []
        for p in period_prompts[:50]:  # Limit na 50 promptov na obdobie
            date = p.get('date', '')
            text = p.get('text', '')
            category = p.get('category', '')
            subcategory = p.get('subcategory', '')
            projects = p.get('context', {}).get('projects', [])
            
            context_parts.append(
                f"[{date}] {category}/{subcategory} | Projekty: {', '.join(projects) if projects else 'žiadne'}\n"
                f"{text[:500]}"
            )
        
        context = "\n\n---\n\n".join(context_parts)
        
        # Syntéza
        system_prompt = """Si expertný naratívny syntetizátor. Tvoja úloha je vytvoriť chronologickú syntézu príbehu z promptov za dané obdobie.

Požiadavky:
- Vytvor syntetizovaný naratív (nie zoznam promptov)
- Zachovaj chronologické poradie
- Identifikuj hlavné témy, projekty a transformácie
- Zhrň kľúčové momenty a zmeny
- Používaj markdown formátovanie
- Odpoveď musí byť čitateľná a zmysluplná

Formát:
# [Obdobie] - Syntéza

## Hlavné Témy
- ...

## Projekty a Aktivity
- ...

## Transformácie a Zmeny
- ...

## Kľúčové Momenty
- ..."""

        user_prompt = f"""Vytvor chronologickú syntézu príbehu za obdobie {period} na základe týchto promptov:

{context}

Vytvor syntetizovaný naratív, ktorý zachytáva hlavné témy, projekty, transformácie a kľúčové momenty tohto obdobia."""

        try:
            response = client.chat.completions.create(
                model=MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.3,
                max_tokens=2000
            )
            
            synthesis = response.choices[0].message.content
            syntheses[period] = synthesis
            
        except Exception as e:
            print(f"      ❌ Chyba pri syntéze {period}: {e}")
            syntheses[period] = f"Chyba pri syntéze: {e}"
    
    return syntheses


def synthesize_story_arcs(temporal_map: Dict, prompts: List[Dict], client: OpenAI) -> Dict:
    """
    Syntetizuje príbehy projektov (story arcs).
    """
    print(f"\n📖 Syntetizujem story arcs...")
    
    story_arcs = temporal_map.get('story_arcs', [])
    syntheses = {}
    
    # Vytvor lookup mapu promptov
    prompts_by_id = {p.get('prompt_id'): p for p in prompts}
    
    for arc in story_arcs[:10]:  # Top 10 story arcs
        project = arc['project']
        prompt_ids = arc['prompt_ids']
        
        print(f"   Syntetizujem {project} ({len(prompt_ids)} promptov)...")
        
        # Zostav kontext z promptov v arce
        context_parts = []
        for prompt_id in prompt_ids:
            prompt = prompts_by_id.get(prompt_id)
            if not prompt:
                continue
            
            date = prompt.get('date', '')
            text = prompt.get('text', '')
            category = prompt.get('category', '')
            
            context_parts.append(f"[{date}] {category}\n{text[:400]}")
        
        context = "\n\n---\n\n".join(context_parts)
        
        # Syntéza
        system_prompt = """Si expertný naratívny syntetizátor. Tvoja úloha je vytvoriť syntézu príbehu projektu z chronologických promptov.

Požiadavky:
- Vytvor syntetizovaný naratív vývoja projektu
- Zachovaj chronologické poradie
- Identifikuj fázy vývoja, problémy, riešenia
- Zhrň kľúčové momenty a zmeny
- Používaj markdown formátovanie"""

        user_prompt = f"""Vytvor syntézu príbehu projektu "{project}" na základe týchto chronologických promptov:

{context}

Vytvor syntetizovaný naratív, ktorý zachytáva vývoj projektu, hlavné fázy, problémy, riešenia a kľúčové momenty."""

        try:
            response = client.chat.completions.create(
                model=MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.3,
                max_tokens=1500
            )
            
            synthesis = response.choices[0].message.content
            syntheses[project] = synthesis
            
        except Exception as e:
            print(f"      ❌ Chyba pri syntéze {project}: {e}")
            syntheses[project] = f"Chyba pri syntéze: {e}"
    
    return syntheses


def synthesize_transformations(prompts: List[Dict], client: OpenAI) -> str:
    """
    Syntetizuje transformačné momenty (zmeny sentimentu, kategórií).
    """
    print(f"\n🔄 Syntetizujem transformačné momenty...")
    
    # Identifikuj zmeny sentimentu a kategórií
    changes = []
    
    for i in range(1, len(prompts)):
        prev = prompts[i-1]
        curr = prompts[i]
        
        prev_sentiment = prev.get('sentiment')
        curr_sentiment = curr.get('sentiment')
        
        prev_category = prev.get('category')
        curr_category = curr.get('category')
        
        # Zmena sentimentu
        if prev_sentiment != curr_sentiment:
            changes.append({
                'date': curr.get('date', ''),
                'type': 'sentiment_change',
                'from': prev_sentiment,
                'to': curr_sentiment,
                'prompt_id': curr.get('prompt_id'),
                'text': curr.get('text', '')[:300]
            })
        
        # Zmena kategórie
        if prev_category != curr_category:
            changes.append({
                'date': curr.get('date', ''),
                'type': 'category_change',
                'from': prev_category,
                'to': curr_category,
                'prompt_id': curr.get('prompt_id'),
                'text': curr.get('text', '')[:300]
            })
    
    # Zostav kontext
    context_parts = []
    for change in changes[:30]:  # Top 30 zmien
        context_parts.append(
            f"[{change['date']}] {change['type']}: {change['from']} → {change['to']}\n"
            f"{change['text']}"
        )
    
    context = "\n\n---\n\n".join(context_parts)
    
    # Syntéza
    system_prompt = """Si expertný analytik transformácií. Tvoja úloha je identifikovať a syntetizovať kľúčové transformačné momenty v príbehu.

Požiadavky:
- Identifikuj hlavné transformačné momenty
- Vysvetli význam zmien
- Vytvor syntetizovaný naratív transformácií
- Používaj markdown formátovanie"""

    user_prompt = f"""Na základe týchto zmien sentimentu a kategórií vytvor syntézu transformačných momentov:

{context}

Vytvor syntetizovaný naratív, ktorý identifikuje hlavné transformačné momenty, ich význam a súvislosti."""

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.3,
            max_tokens=2000
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        return f"Chyba pri syntéze: {e}"


def main():
    """Hlavná funkcia."""
    print("="*80)
    print("Chronologická syntéza príbehu")
    print("="*80)
    
    # Načítaj dáta
    print("\n📖 Načítavam dáta...")
    prompts, temporal_map = load_data()
    print(f"✅ Načítaných {len(prompts)} promptov")
    
    # Inicializuj OpenRouter client
    client = OpenAI(
        api_key=OPENROUTER_API_KEY,
        base_url=OPENROUTER_BASE_URL,
        default_headers={
            "HTTP-Referer": "https://github.com/xvadur-workspace",
            "X-Title": "Chronological Story Synthesis"
        }
    )
    
    # Syntéza podľa období
    period_syntheses = synthesize_by_period(prompts, client)
    
    # Syntéza story arcs
    story_arc_syntheses = {}
    if temporal_map:
        story_arc_syntheses = synthesize_story_arcs(temporal_map, prompts, client)
    
    # Syntéza transformácií
    transformation_synthesis = synthesize_transformations(prompts, client)
    
    # Ulož výsledky
    print("\n💾 Ukladám výsledky...")
    
    # Syntéza podľa období
    periods_file = OUTPUT_DIR / "synthesis_by_periods.md"
    with open(periods_file, 'w', encoding='utf-8') as f:
        f.write("# Chronologická Syntéza podľa Období\n\n")
        for period, synthesis in sorted(period_syntheses.items()):
            f.write(f"## {period}\n\n{synthesis}\n\n---\n\n")
    print(f"✅ Uložené: {periods_file}")
    
    # Story arcs
    arcs_file = OUTPUT_DIR / "synthesis_story_arcs.md"
    with open(arcs_file, 'w', encoding='utf-8') as f:
        f.write("# Syntéza Story Arcs (Príbehy Projektov)\n\n")
        for project, synthesis in story_arc_syntheses.items():
            f.write(f"## {project}\n\n{synthesis}\n\n---\n\n")
    print(f"✅ Uložené: {arcs_file}")
    
    # Transformácie
    trans_file = OUTPUT_DIR / "synthesis_transformations.md"
    with open(trans_file, 'w', encoding='utf-8') as f:
        f.write("# Syntéza Transformačných Momentov\n\n")
        f.write(transformation_synthesis)
    print(f"✅ Uložené: {trans_file}")
    
    print("\n" + "="*80)
    print("✅ DOKONČENÉ")
    print("="*80)
    print(f"📁 Výstupné súbory v: {OUTPUT_DIR}/")
    print("="*80)


if __name__ == "__main__":
    main()

