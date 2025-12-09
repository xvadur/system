#!/usr/bin/env python3
"""
Granularná kategorizácia promptov pomocou OpenAI API.
Rozširuje prompts_nlp4sk.jsonl o kategórie, subkategórie a kontext.
"""

import json
import os
import sys
import time
import logging
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional

# OpenAI
try:
    from openai import OpenAI
except ImportError:
    print("❌ Chyba: Potrebuješ nainštalovať openai")
    print("   pip install openai")
    sys.exit(1)

# Konfigurácia
INPUT_FILE = Path("data/prompts/prompts_nlp4sk.jsonl")
OUTPUT_FILE = Path("data/prompts/prompts_categorized.jsonl")
ERROR_LOG = Path("data/prompts/categorization_errors.log")
BATCH_SIZE = 10
MODEL = "gpt-4o-mini"
TEST_MODE = False
TEST_LIMIT = 20

# OpenAI API Key - načíta z .env súboru alebo environment
def load_api_key():
    """Načíta OpenAI API key z .env súboru alebo environmentu."""
    # Najprv skús environment variable
    api_key = os.getenv("OPENAI_API_KEY")
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
                        if line.startswith("#") or not line:
                            continue
                        if line.startswith("OPENAI_API_KEY="):
                            key = line.split("=", 1)[1].strip()
                            key = key.strip('"').strip("'")
                            if key and key != "sk-...":
                                return key
            except Exception as e:
                logger.warning(f"Chyba pri načítaní {env_file}: {e}")
                continue
    
    return None

API_KEY = load_api_key()
if not API_KEY:
    print("⚠️  OPENAI_API_KEY nie je nastavený")
    print("   Možnosti:")
    print("   1. Vytvor .env súbor v root adresári s: OPENAI_API_KEY=sk-...")
    print("   2. Alebo nastav: export OPENAI_API_KEY='sk-...'")
    sys.exit(1)

# Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(ERROR_LOG),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def load_prompts() -> List[Dict]:
    """Načíta prompty z prompts_nlp4sk.jsonl."""
    prompts = []
    
    if not INPUT_FILE.exists():
        logger.error(f"❌ Súbor {INPUT_FILE} neexistuje!")
        return prompts
    
    try:
        with open(INPUT_FILE, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                try:
                    data = json.loads(line)
                    prompts.append(data)
                except json.JSONDecodeError as e:
                    logger.warning(f"Chyba pri parsovaní riadku {line_num}: {e}")
                    continue
    except Exception as e:
        logger.error(f"Chyba pri načítaní {INPUT_FILE}: {e}")
    
    logger.info(f"✅ Načítaných {len(prompts)} promptov")
    return prompts


def load_existing_categorizations() -> set:
    """Načíta už existujúce prompt_id z output súboru (pre resume functionality)."""
    existing = set()
    
    if not OUTPUT_FILE.exists():
        return existing
    
    try:
        with open(OUTPUT_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    data = json.loads(line)
                    prompt_id = data.get("prompt_id")
                    if prompt_id:
                        existing.add(prompt_id)
                except:
                    continue
    except Exception as e:
        logger.warning(f"Chyba pri načítaní existujúcich kategorizácií: {e}")
    
    logger.info(f"✅ Načítaných {len(existing)} už spracovaných promptov")
    return existing


def categorize_prompt(prompt_data: Dict, client: OpenAI, max_retries: int = 3) -> Optional[Dict]:
    """
    Kategorizuje prompt pomocou OpenAI API.
    
    Args:
        prompt_data: Dict s prompt_id, text, sentiment, concepts, atď.
        client: OpenAI client
        max_retries: Maximálny počet pokusov
    
    Returns:
        Dict s kategorizáciou alebo None pri chybe
    """
    # Zostavíme text na analýzu
    text = prompt_data.get("text", "")
    sentiment = prompt_data.get("sentiment", "unknown")
    concepts = prompt_data.get("concepts", [])
    technologies = prompt_data.get("technologies", [])
    people = prompt_data.get("people", [])
    
    # Zostavíme kontext pre lepšiu kategorizáciu
    context_parts = []
    if sentiment:
        context_parts.append(f"Sentiment: {sentiment}")
    if concepts:
        context_parts.append(f"Kľúčové pojmy: {', '.join(concepts[:10])}")
    if technologies:
        context_parts.append(f"Technológie: {', '.join(technologies[:5])}")
    if people:
        context_parts.append(f"Ľudia: {', '.join(people[:5])}")
    
    context_str = "\n".join(context_parts)
    
    system_prompt = """Si asistent, ktorý kategorizuje prompty do granularných kategórií.
Odpovedaj VŽDY v JSON formáte:
{
  "category": "work|reflection|planning|problem_solving|learning",
  "subcategory": "...",
  "context": {
    "projects": ["..."],
    "people": ["..."],
    "technologies": ["..."],
    "emotions": ["..."]
  }
}

Kategórie:
- work: Konkrétna práca na projekte, kód, implementácia
- reflection: Filozofická úvaha, sebareflexia, osobné myšlienky
- planning: Plánovanie, stratégia, rozhodovanie o budúcnosti
- problem_solving: Riešenie problému, debugging, hľadanie riešení
- learning: Učenie sa, výskum, získavanie nových znalostí

Subkategórie (príklady):
- work: ai_project, business, technical, writing
- reflection: personal, philosophical, emotional
- planning: strategic, tactical, daily
- problem_solving: debugging, design, optimization
- learning: tutorial, research, exploration

Kontext:
- projects: Konkrétne projekty (n8n, iShowSpeed, Recepčná, atď.)
- people: Ľudia spomínaní v texte (okrem "Adam")
- technologies: Technológie a nástroje
- emotions: Emocionálne stavy (frustration, excitement, uncertainty, atď.)"""

    user_prompt = f"""Kategorizuj tento prompt:

Text:
{text[:3000]}

Dodatočný kontext:
{context_str}

Vráť JSON s kategóriou, subkategóriou a kontextom."""

    for attempt in range(max_retries):
        try:
            request_params = {
                "model": MODEL,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                "temperature": 0.3,
                "max_tokens": 400
            }
            
            if "gpt-4" in MODEL:
                request_params["response_format"] = {"type": "json_object"}
            
            response = client.chat.completions.create(**request_params)
            content = response.choices[0].message.content.strip()
            
            # Parsuje JSON odpoveď
            try:
                result = json.loads(content)
                
                # Validácia
                category = result.get("category", "unknown")
                if category not in ["work", "reflection", "planning", "problem_solving", "learning"]:
                    category = "reflection"  # Default
                
                subcategory = result.get("subcategory", "")
                context = result.get("context", {})
                
                return {
                    "category": category,
                    "subcategory": subcategory,
                    "context": {
                        "projects": context.get("projects", []),
                        "people": context.get("people", []),
                        "technologies": context.get("technologies", []),
                        "emotions": context.get("emotions", [])
                    }
                }
            except json.JSONDecodeError:
                logger.warning("Odpoveď nie je v JSON formáte, parsujem text...")
                # Fallback parsing
                category = "reflection"
                subcategory = ""
                context = {"projects": [], "people": [], "technologies": [], "emotions": []}
                
                # Skúsi extrahovať aspoň kategóriu z textu
                content_lower = content.lower()
                if "work" in content_lower or "práca" in content_lower:
                    category = "work"
                elif "planning" in content_lower or "plán" in content_lower:
                    category = "planning"
                elif "problem" in content_lower or "problém" in content_lower:
                    category = "problem_solving"
                elif "learning" in content_lower or "učenie" in content_lower:
                    category = "learning"
                
                return {
                    "category": category,
                    "subcategory": subcategory,
                    "context": context
                }
            
        except Exception as e:
            if attempt < max_retries - 1:
                wait_time = (attempt + 1) * 2
                logger.warning(f"Chyba pri API volaní (pokus {attempt + 1}/{max_retries}): {e}. Čakám {wait_time}s...")
                time.sleep(wait_time)
            else:
                logger.error(f"Zlyhalo API volanie po {max_retries} pokusoch: {e}")
                return None
    
    return None


def save_categorization(categorized_data: Dict, output_path: Path):
    """Uloží kategorizovaný prompt do JSONL súboru."""
    try:
        with open(output_path, 'a', encoding='utf-8') as f:
            f.write(json.dumps(categorized_data, ensure_ascii=False) + '\n')
            f.flush()
    except Exception as e:
        logger.error(f"Chyba pri ukladaní kategorizácie: {e}")
        raise


def main():
    """Hlavná funkcia."""
    logger.info("="*80)
    logger.info("Granularná kategorizácia promptov")
    logger.info("="*80)
    
    # Vytvor output adresár ak neexistuje
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    # Načítaj prompty
    logger.info("📖 Načítavam prompty...")
    all_prompts = load_prompts()
    
    if not all_prompts:
        logger.error("❌ Žiadne prompty na spracovanie!")
        return
    
    # Načítaj už spracované
    existing_ids = load_existing_categorizations()
    
    # Filtruj už spracované
    prompts_to_process = [p for p in all_prompts if p.get("prompt_id") not in existing_ids]
    logger.info(f"📊 Zostáva spracovať {len(prompts_to_process)} promptov")
    
    # Test mode
    if TEST_MODE:
        prompts_to_process = prompts_to_process[:TEST_LIMIT]
        logger.info(f"🧪 TEST MODE: Spracujem len prvých {TEST_LIMIT} promptov")
    
    if not prompts_to_process:
        logger.info("✅ Všetky prompty už boli spracované!")
        return
    
    # Inicializuj OpenAI client
    client = OpenAI(api_key=API_KEY)
    
    # Spracuj prompty
    logger.info("🚀 Začínam kategorizáciu...")
    processed = 0
    failed = 0
    start_time = time.time()
    
    for i, prompt in enumerate(prompts_to_process, 1):
        prompt_id = prompt.get("prompt_id", "unknown")
        
        logger.info(f"[{i}/{len(prompts_to_process)}] Kategorizujem {prompt_id}...")
        
        # Kategorizuj prompt
        try:
            categorization = categorize_prompt(prompt, client)
            
            if categorization:
                # Spoj pôvodné dáta s kategorizáciou
                categorized_data = {
                    **prompt,  # Všetky pôvodné polia
                    "category": categorization["category"],
                    "subcategory": categorization["subcategory"],
                    "context": categorization["context"],
                    "categorized_at": datetime.now().isoformat()
                }
                
                # Ulož
                save_categorization(categorized_data, OUTPUT_FILE)
                processed += 1
                
                # Zobraz výsledky
                category = categorization.get("category", "unknown")
                subcategory = categorization.get("subcategory", "")
                projects_count = len(categorization.get("context", {}).get("projects", []))
                
                logger.info(f"✅ Spracované: {category}/{subcategory} (projekty: {projects_count})")
            else:
                failed += 1
                logger.error(f"❌ Zlyhalo kategorizovanie {prompt_id}")
        except Exception as e:
            failed += 1
            logger.error(f"❌ Zlyhalo spracovanie {prompt_id}: {e}")
            import traceback
            logger.debug(traceback.format_exc())
        
        # Rate limiting - 1 request za sekundu
        if i < len(prompts_to_process):
            time.sleep(1.1)
        
        # Progress update každých BATCH_SIZE promptov
        if i % BATCH_SIZE == 0:
            elapsed = time.time() - start_time
            avg_time = elapsed / i
            remaining = (len(prompts_to_process) - i) * avg_time
            logger.info(f"📊 Progress: {i}/{len(prompts_to_process)} ({i/len(prompts_to_process)*100:.1f}%) | "
                       f"Čas: {elapsed:.1f}s | Zostáva: ~{remaining:.1f}s")
    
    # Finálny report
    total_time = time.time() - start_time
    logger.info("="*80)
    logger.info("VÝSLEDKY")
    logger.info("="*80)
    logger.info(f"✅ Úspešne spracovaných: {processed}")
    logger.info(f"❌ Zlyhalo: {failed}")
    logger.info(f"⏱️  Celkový čas: {total_time:.1f}s ({total_time/60:.1f} minút)")
    logger.info(f"📁 Výstup: {OUTPUT_FILE}")
    logger.info(f"📋 Error log: {ERROR_LOG}")


if __name__ == "__main__":
    main()

