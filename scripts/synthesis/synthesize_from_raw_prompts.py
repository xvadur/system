#!/usr/bin/env python3
"""
Chronologická syntéza z originálnych surových promptov pomocou Grok-4.
Používa veľké kontextové okno (2M tokenov) na syntézu celých období naraz.
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
PROMPTS_SPLIT_DIR = Path("data/prompts/prompts_split")
PROMPTS_LOG_PATH = Path("development/data/prompts_log.jsonl")
OUTPUT_DIR = Path("data/prompts/synthesis")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# OpenRouter konfigurácia
# DeepSeek R1T2 Chimera má 163k token kontext a je FREE!
MODEL = "tngtech/deepseek-r1t2-chimera:free"  # 163k token kontext, FREE!
FALLBACK_MODEL = "mistralai/mistral-7b-instruct:free"  # Fallback ak nefunguje
OPENROUTER_API_KEY = "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"
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

# DeepSeek R1T2 Chimera: 163k tokenov ≈ 122k slov
# Mistral 7B: ~32k tokenov ≈ 24k slov
MAX_CONTEXT_WORDS_DEEPSEEK = 120_000  # Pre DeepSeek
MAX_CONTEXT_WORDS_FALLBACK = 20_000  # Pre Mistral fallback
MAX_CONTEXT_WORDS = MAX_CONTEXT_WORDS_DEEPSEEK  # Začneme s DeepSeek


def load_raw_prompts() -> List[Dict]:
    """Načíta originálne surové prompty z prompts_split a prompts_log."""
    prompts = []
    
    # Načítaj z prompts_split
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
                
                word_count = data.get("word_count", len(text.split()))
                
                prompts.append({
                    "prompt_id": f"{day_dir.name}_{json_file.stem}",
                    "date": date_str,
                    "date_obj": date_obj,
                    "text": text,
                    "word_count": word_count,
                    "timestamp": data.get("timestamp", ""),
                    "source": "prompts_split"
                })
            except Exception as e:
                continue
    
    # Načítaj z prompts_log
    if PROMPTS_LOG_PATH.exists():
        try:
            with open(PROMPTS_LOG_PATH, 'r', encoding='utf-8') as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        data = json.loads(line)
                        if data.get("role") != "user":
                            continue
                        
                        text = data.get("content", "")
                        if not text:
                            continue
                        
                        timestamp_str = data.get("timestamp", "")
                        try:
                            if '+' in timestamp_str or timestamp_str.endswith('Z'):
                                date_obj = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
                            else:
                                date_obj = datetime.fromisoformat(timestamp_str)
                            # Normalizuj na naive datetime
                            if date_obj.tzinfo is not None:
                                date_obj = date_obj.replace(tzinfo=None)
                        except:
                            continue
                        
                        date_str = date_obj.strftime("%Y-%m-%d")
                        word_count = len(text.split())
                        
                        prompts.append({
                            "prompt_id": f"current_{line_num}",
                            "date": date_str,
                            "date_obj": date_obj,
                            "text": text,
                            "word_count": word_count,
                            "timestamp": timestamp_str,
                            "source": "prompts_log"
                        })
                    except:
                        continue
        except Exception as e:
            pass
    
    # Zoraď podľa dátumu
    prompts.sort(key=lambda x: x.get('date_obj', datetime.min))
    
    print(f"✅ Načítaných {len(prompts)} originálnych promptov")
    return prompts


def synthesize_evolution(prompts: List[Dict], client: OpenAI, period: str = None) -> str:
    """
    Syntetizuje vývoj myslenia a konania z originálnych promptov.
    
    Perspektívy:
    1. Ako sa myslenie vyvíjalo (témy, otázky, úvahy)
    2. Ako sa konanie vyvíjalo (projekty, aktivity, rozhodnutia)
    3. Vzťah medzi myslením a konaním
    4. Temporálne vzorce a zmeny
    """
    print(f"\n🧠 Syntetizujem vývoj myslenia a konania...")
    
    # Zostav chronologický text
    if period:
        period_prompts = [p for p in prompts if p.get('date', '').startswith(period)]
        period_label = period
    else:
        period_prompts = prompts
        period_label = "celé obdobie"
    
    if not period_prompts:
        return "Žiadne prompty pre toto obdobie"
    
    # Zostav chronologický kontext
    context_parts = []
    total_words = 0
    
    for prompt in period_prompts:
        date = prompt.get('date', '')
        text = prompt.get('text', '')
        word_count = prompt.get('word_count', 0)
        
        # Limit na MAX_CONTEXT_WORDS
        if total_words + word_count > MAX_CONTEXT_WORDS:
            break
        
        context_parts.append(f"[{date}]\n{text}")
        total_words += word_count
    
    context = "\n\n---\n\n".join(context_parts)
    
    print(f"   Syntetizujem {len(period_prompts)} promptov ({total_words:,} slov)...")
    
    system_prompt = """Si expertný analytik a naratívny syntetizátor. Tvoja úloha je vytvoriť hlbokú syntézu vývoja myslenia a konania z chronologických promptov.

Analyzuj tieto perspektívy:

1. **Vývoj myslenia:**
   - Ako sa menili témy a otázky v čase?
   - Aké myšlienkové vzorce sa opakovali?
   - Kde boli zlomy v myslení?
   - Ako sa hĺbka úvah menila?

2. **Vývoj konania:**
   - Aké projekty a aktivity sa objavovali?
   - Ako sa menil spôsob práce?
   - Kde boli rozhodujúce momenty?
   - Ako sa produktivita menila?

3. **Vzťah myslenia a konania:**
   - Ako myslenie ovplyvňovalo konanie?
   - Kde boli reflexie, ktoré viedli k akcii?
   - Kde boli akcie, ktoré viedli k reflexii?

4. **Temporálne vzorce:**
   - Identifikuj fázy (napr. explorácia → fokus → implementácia)
   - Nájdi cykly (reflexia → akcia → reflexia)
   - Identifikuj transformačné momenty

Vytvor syntetizovaný naratív, ktorý:
- Zachytáva vývoj v čase (nie len zoznam faktov)
- Identifikuje hlavné témy a ich transformácie
- Ukazuje vzťahy medzi myslením a konaním
- Odhaľuje temporálne vzorce a zmeny
- Je čitateľný a zmysluplný

Používaj markdown formátovanie."""

    user_prompt = f"""Analyzuj tieto chronologické prompty z {period_label} a vytvor syntézu vývoja myslenia a konania:

{context}

Vytvor syntetizovaný naratív, ktorý zachytáva:
- Ako sa myslenie vyvíjalo (témy, otázky, úvahy)
- Ako sa konanie vyvíjalo (projekty, aktivity, rozhodnutia)
- Vzťah medzi myslením a konaním
- Temporálne vzorce a transformačné momenty

Odpoveď musí byť syntetizovaná (nie zoznam promptov), chronologická a zmysluplná."""

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.3,
            max_tokens=4000
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        return f"Chyba pri syntéze: {e}"


def synthesize_by_evolution_phases(prompts: List[Dict], client: OpenAI) -> Dict:
    """
    Syntetizuje podľa fáz vývoja (nie mesiacov, ale podľa zmien v myslení/konaní).
    """
    print(f"\n📊 Identifikujem fázy vývoja...")
    
    # Rozdel prompty do fáz podľa zmien v aktivitách
    # Použijeme jednoduchú heuristiku: zmeny v dĺžke promptov, témy, atď.
    
    phases = []
    current_phase = {
        "start_date": prompts[0].get('date') if prompts else None,
        "prompts": []
    }
    
    for i, prompt in enumerate(prompts):
        # Jednoduchá heuristika: ak je veľká zmena v word_count, začni novú fázu
        if i > 0:
            prev = prompts[i-1]
            word_diff = abs(prompt.get('word_count', 0) - prev.get('word_count', 0))
            avg_words = (prompt.get('word_count', 0) + prev.get('word_count', 0)) / 2
            
            # Ak je zmena > 50% priemeru, možno nová fáza
            if avg_words > 0 and word_diff / avg_words > 0.5 and len(current_phase["prompts"]) > 10:
                current_phase["end_date"] = prev.get('date')
                phases.append(current_phase)
                current_phase = {
                    "start_date": prompt.get('date'),
                    "prompts": []
                }
        
        current_phase["prompts"].append(prompt)
    
    # Pridaj poslednú fázu
    if current_phase["prompts"]:
        current_phase["end_date"] = prompts[-1].get('date') if prompts else None
        phases.append(current_phase)
    
    print(f"   Identifikovaných {len(phases)} fáz")
    
    # Syntetizuj každú fázu
    syntheses = {}
    for i, phase in enumerate(phases, 1):
        phase_label = f"Fáza {i}: {phase['start_date']} - {phase['end_date']}"
        print(f"   Syntetizujem {phase_label} ({len(phase['prompts'])} promptov)...")
        
        synthesis = synthesize_evolution(phase['prompts'], client, period=None)
        syntheses[phase_label] = synthesis
    
    return syntheses


def main():
    """Hlavná funkcia."""
    print("="*80)
    print("Chronologická syntéza z originálnych promptov (Grok-4)")
    print("="*80)
    
    # Načítaj originálne prompty
    print("\n📖 Načítavam originálne surové prompty...")
    prompts = load_raw_prompts()
    
    if not prompts:
        print("❌ Žiadne prompty na spracovanie!")
        return
    
    # Inicializuj OpenRouter client
    client = OpenAI(
        api_key=OPENROUTER_API_KEY,
        base_url=OPENROUTER_BASE_URL,
        default_headers={
            "HTTP-Referer": "https://github.com/xvadur-workspace",
            "X-Title": "Chronological Story Synthesis"
        }
    )
    
    # Test modelu
    global MODEL, MAX_CONTEXT_WORDS
    print(f"\n🔍 Testujem model {MODEL}...")
    try:
        test_response = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": "Test"}],
            max_tokens=10
        )
        print(f"✅ Model {MODEL} funguje! (163k token kontext, FREE!)")
        MAX_CONTEXT_WORDS = MAX_CONTEXT_WORDS_DEEPSEEK
    except Exception as e:
        error_str = str(e)
        if '402' in error_str or 'Insufficient' in error_str:
            print(f"💰 Model {MODEL} potrebuje kredit")
            print(f"   Používam fallback: {FALLBACK_MODEL}")
            MODEL = FALLBACK_MODEL
            MAX_CONTEXT_WORDS = MAX_CONTEXT_WORDS_FALLBACK
            # Test fallback
            try:
                test_response = client.chat.completions.create(
                    model=MODEL,
                    messages=[{"role": "user", "content": "Test"}],
                    max_tokens=10
                )
                print(f"✅ Fallback model {MODEL} funguje!")
            except Exception as e2:
                print(f"❌ Ani fallback nefunguje: {e2}")
                return
        else:
            print(f"❌ Model {MODEL} nie je dostupný: {e}")
            print(f"   Skúsim fallback: {FALLBACK_MODEL}")
            MODEL = FALLBACK_MODEL
            MAX_CONTEXT_WORDS = MAX_CONTEXT_WORDS_FALLBACK
            try:
                test_response = client.chat.completions.create(
                    model=MODEL,
                    messages=[{"role": "user", "content": "Test"}],
                    max_tokens=10
                )
                print(f"✅ Fallback model {MODEL} funguje!")
            except Exception as e2:
                print(f"❌ Ani fallback nefunguje: {e2}")
                return
    
    # Syntéza vývoja myslenia a konania
    print(f"\n📊 Syntéza vývoja myslenia a konania...")
    total_words = sum(p.get('word_count', 0) for p in prompts)
    print(f"   Celkom: {len(prompts)} promptov, {total_words:,} slov")
    print(f"   Kontextové okno: {MAX_CONTEXT_WORDS:,} slov na batch")
    
    syntheses = {}
    
    # Ak máme veľké kontextové okno, skús syntetizovať všetko naraz
    if MAX_CONTEXT_WORDS >= 100_000:  # Ak máme aspoň 100k slov kapacity
        if total_words < MAX_CONTEXT_WORDS:
            print(f"   ✅ Všetky prompty sa zmestia do jedného kontextu!")
            print(f"   Syntetizujem celé obdobie naraz...")
            synthesis = synthesize_evolution(prompts, client, period=None)
            syntheses["celé_obdobie"] = synthesis
        else:
            print(f"   ⚠️  Prompty sa nezmestia ({total_words:,} > {MAX_CONTEXT_WORDS:,})")
            print(f"   Syntetizujem podľa mesiacov...")
            # Syntéza podľa mesiacov
            periods = defaultdict(list)
            for prompt in prompts:
                date_str = prompt.get('date', '')
                if date_str:
                    period_key = date_str[:7]  # YYYY-MM
                    periods[period_key].append(prompt)
            
            for period in sorted(periods.keys()):
                period_prompts = periods[period]
                period_words = sum(p.get('word_count', 0) for p in period_prompts)
                
                print(f"\n📅 Syntetizujem {period} ({len(period_prompts)} promptov, {period_words:,} slov)...")
                synthesis = synthesize_evolution(period_prompts, client, period=period)
                syntheses[period] = synthesis
    else:
        # Fallback: syntéza podľa mesiacov (pre menšie kontextové okno)
        print(f"   Syntetizujem podľa mesiacov...")
        periods = defaultdict(list)
        for prompt in prompts:
            date_str = prompt.get('date', '')
            if date_str:
                period_key = date_str[:7]  # YYYY-MM
                periods[period_key].append(prompt)
        
        for period in sorted(periods.keys()):
            period_prompts = periods[period]
            period_words = sum(p.get('word_count', 0) for p in period_prompts)
            
            print(f"\n📅 Syntetizujem {period} ({len(period_prompts)} promptov, {period_words:,} slov)...")
            
            # Ak mesiac je príliš veľký, rozdel na týždne
            if period_words > MAX_CONTEXT_WORDS:
                print(f"   ⚠️  Mesiac je príliš veľký, rozdeľujem na týždne...")
                # Rozdel na týždne
                weeks = defaultdict(list)
                for prompt in period_prompts:
                    date_obj = prompt.get('date_obj')
                    if date_obj:
                        week_key = f"{period}_week_{date_obj.isocalendar()[1]}"
                        weeks[week_key].append(prompt)
                
                for week_key in sorted(weeks.keys()):
                    week_prompts = weeks[week_key]
                    week_words = sum(p.get('word_count', 0) for p in week_prompts)
                    if week_words > 0:  # Len ak má prompty
                        print(f"   Syntetizujem {week_key} ({len(week_prompts)} promptov, {week_words:,} slov)...")
                        synthesis = synthesize_evolution(week_prompts, client, period=week_key)
                        syntheses[week_key] = synthesis
            else:
                synthesis = synthesize_evolution(period_prompts, client, period=period)
                syntheses[period] = synthesis
    
    # Ulož
    periods_file = OUTPUT_DIR / "synthesis_evolution_from_raw.md"
    with open(periods_file, 'w', encoding='utf-8') as f:
        f.write("# Syntéza Vývoja Myslenia a Konania (z Originálnych Promptov)\n\n")
        f.write("Táto syntéza je vytvorená z **originálnych surových promptov**, nie z extrahovaných aktivít.\n\n")
        f.write("## Perspektívy Analýzy\n\n")
        f.write("1. **Vývoj myslenia**: Ako sa menili témy, otázky a úvahy v čase\n")
        f.write("2. **Vývoj konania**: Ako sa menili projekty, aktivity a rozhodnutia\n")
        f.write("3. **Vzťah myslenia a konania**: Ako myslenie ovplyvňovalo konanie a naopak\n")
        f.write("4. **Temporálne vzorce**: Fázy, cykly a transformačné momenty\n\n")
        f.write("---\n\n")
        for period, synthesis in sorted(syntheses.items()):
            f.write(f"## {period}\n\n{synthesis}\n\n---\n\n")
    print(f"✅ Uložené: {periods_file}")
    
    # Syntéza 2: Podľa fáz vývoja (voliteľné, môže byť pomalé)
    print(f"\n📊 Syntéza podľa fáz vývoja...")
    try:
        phase_syntheses = synthesize_by_evolution_phases(prompts, client)
        
        phases_file = OUTPUT_DIR / "synthesis_evolution_by_phases.md"
        with open(phases_file, 'w', encoding='utf-8') as f:
            f.write("# Syntéza Vývoja podľa Fáz\n\n")
            for phase, synthesis in phase_syntheses.items():
                f.write(f"## {phase}\n\n{synthesis}\n\n---\n\n")
        print(f"✅ Uložené: {phases_file}")
    except Exception as e:
        print(f"⚠️  Syntéza fáz zlyhala: {e}")
        print("   Pokračujem bez nej...")
    
    print("\n" + "="*80)
    print("✅ DOKONČENÉ")
    print("="*80)
    print(f"📁 Výstupné súbory v: {OUTPUT_DIR}/")
    print("="*80)


if __name__ == "__main__":
    main()

