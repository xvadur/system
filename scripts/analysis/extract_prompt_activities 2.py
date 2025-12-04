#!/usr/bin/env python3
"""
Extrahuje aktivitu a myšlienky z každého promptu pomocou OpenAI API.
Ukladá výsledky do prompts_activities.jsonl.
"""

import json
import os
import sys
import time
import logging
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
PROMPTS_SPLIT_DIR = Path("data/prompts/prompts_split")
PROMPTS_LOG_PATH = Path("xvadur/data/prompts_log.jsonl")
OUTPUT_FILE = Path("data/prompts/prompts_activities.jsonl")
ERROR_LOG = Path("data/prompts/extraction_errors.log")
MAX_WORDS = 1000
BATCH_SIZE = 10
MODEL = "gpt-4o-mini"  # Rýchlejší a lacnejší model
TEST_MODE = False  # Ak True, spracuje len prvých 20 promptov
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
                        # Ignoruje komentáre a prázdne riadky
                        if line.startswith("#") or not line:
                            continue
                        if line.startswith("OPENAI_API_KEY="):
                            key = line.split("=", 1)[1].strip()
                            # Odstráni quotes ak existujú
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


def load_historical_prompts() -> List[Dict]:
    """Načíta všetky historické prompty z prompts_split."""
    prompts = []
    
    for day_dir in sorted(PROMPTS_SPLIT_DIR.glob("*")):
        if not day_dir.is_dir():
            continue
        
        for json_file in sorted(day_dir.glob("*.json")):
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                if not data.get("text"):
                    continue
                
                date_str = data.get("date", day_dir.name)
                try:
                    date = datetime.strptime(date_str, "%Y-%m-%d")
                except:
                    continue
                
                word_count = data.get("word_count", 0)
                
                prompts.append({
                    "prompt_id": f"{day_dir.name}_{json_file.stem}",
                    "date": date,
                    "timestamp": data.get("timestamp", ""),
                    "text": data.get("text", ""),
                    "word_count": word_count,
                })
            except Exception as e:
                logger.warning(f"Chyba pri načítaní {json_file}: {e}")
                continue
    
    logger.info(f"Načítaných {len(prompts)} historických promptov")
    return prompts


def load_current_prompts() -> List[Dict]:
    """Načíta aktuálne prompty z prompts_log.jsonl."""
    prompts = []
    
    if not PROMPTS_LOG_PATH.exists():
        return prompts
    
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
                    
                    timestamp_str = data.get("timestamp", "")
                    try:
                        if '+' in timestamp_str or timestamp_str.endswith('Z'):
                            date = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
                        else:
                            date = datetime.fromisoformat(timestamp_str)
                    except:
                        continue
                    
                    text = data.get("content", "")
                    # Počíta slová
                    word_count = len(text.split())
                    
                    prompts.append({
                        "prompt_id": f"current_{line_num}",
                        "date": date,
                        "timestamp": timestamp_str,
                        "text": text,
                        "word_count": word_count,
                    })
                except Exception as e:
                    logger.warning(f"Chyba pri parsovaní riadku {line_num}: {e}")
                    continue
    except Exception as e:
        logger.error(f"Chyba pri načítaní {PROMPTS_LOG_PATH}: {e}")
    
    logger.info(f"Načítaných {len(prompts)} aktuálnych promptov")
    return prompts


def filter_prompts_by_length(prompts: List[Dict], max_words: int = MAX_WORDS) -> List[Dict]:
    """Filtruje prompty podľa dĺžky."""
    filtered = [p for p in prompts if p.get("word_count", 0) < max_words]
    logger.info(f"Filtrovaných {len(filtered)} promptov z {len(prompts)} (limit: {max_words} slov)")
    return filtered


def load_existing_activities() -> set:
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
        logger.warning(f"Chyba pri načítaní existujúcich aktivít: {e}")
    
    logger.info(f"Načítaných {len(existing)} už spracovaných promptov")
    return existing


def extract_activity_summary(prompt_text: str, client: OpenAI, max_retries: int = 3) -> Optional[Dict]:
    """Extrahuje aktivitu a myšlienky z promptu pomocou OpenAI API."""
    
    system_prompt = """Si asistent, ktorý analyzuje prompty a extrahuje z nich aktivitu a myšlienky.
Odpovedaj vždy v JSON formáte:
{
  "activity": "1-2 vety o tom, čo Adam robil",
  "thoughts": "1-3 vety o tom, nad čím rozmýšľal"
}

Ak nie je jasné, čo robil, napíš "Konzultácia/Reflexia" pre aktivitu."""

    user_prompt = f"""Z tohto textu extrahuj:
1. Čo Adam robil v túto chvíľu (konkrétna aktivita/projekt)
2. Nad čím rozmýšľal (témy, myšlienky, problémy)

Text:
{prompt_text[:4000]}"""  # Limit na 4000 znakov pre bezpečnosť

    for attempt in range(max_retries):
        try:
            # Vytvor request
            request_params = {
                "model": MODEL,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                "temperature": 0.3,
                "max_tokens": 300
            }
            
            # response_format podporuje len gpt-4o a gpt-4-turbo
            if "gpt-4" in MODEL:
                request_params["response_format"] = {"type": "json_object"}
            
            response = client.chat.completions.create(**request_params)
            
            content = response.choices[0].message.content.strip()
            
            # Parsuje JSON odpoveď
            try:
                result = json.loads(content)
                activity = result.get("activity", "").strip()
                thoughts = result.get("thoughts", "").strip()
                
                # Validácia
                if not activity:
                    activity = "Konzultácia/Reflexia"
                if not thoughts:
                    thoughts = "Nie je jasné"
                
                return {
                    "activity": activity,
                    "thoughts": thoughts
                }
            except json.JSONDecodeError:
                # Fallback - ak nie je JSON, skúsi parsovať text
                logger.warning("Odpoveď nie je v JSON formáte, parsujem text...")
                activity = ""
                thoughts = ""
                
                lines = content.split('\n')
                for line in lines:
                    line = line.strip()
                    if 'activity' in line.lower() or 'aktivita' in line.lower():
                        if ':' in line:
                            activity = line.split(':', 1)[1].strip().strip('"').strip("'")
                    elif 'thoughts' in line.lower() or 'myšlienky' in line.lower():
                        if ':' in line:
                            thoughts = line.split(':', 1)[1].strip().strip('"').strip("'")
                
                return {
                    "activity": activity or "Konzultácia/Reflexia",
                    "thoughts": thoughts or "Nie je jasné"
                }
            
        except Exception as e:
            if attempt < max_retries - 1:
                wait_time = (attempt + 1) * 2  # Exponential backoff
                logger.warning(f"Chyba pri API volaní (pokus {attempt + 1}/{max_retries}): {e}. Čakám {wait_time}s...")
                time.sleep(wait_time)
            else:
                logger.error(f"Zlyhalo API volanie po {max_retries} pokusoch: {e}")
                return None
    
    return None


def save_activity(activity_data: Dict, output_path: Path):
    """Uloží jednu aktivitu do JSONL súboru."""
    try:
        with open(output_path, 'a', encoding='utf-8') as f:
            f.write(json.dumps(activity_data, ensure_ascii=False) + '\n')
            f.flush()
    except Exception as e:
        logger.error(f"Chyba pri ukladaní aktivity: {e}")
        raise


def main():
    """Hlavná funkcia."""
    logger.info("="*80)
    logger.info("Extrakcia aktivít z promptov")
    logger.info("="*80)
    
    # Vytvor output adresár ak neexistuje
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    # Načítaj prompty
    logger.info("📖 Načítavam prompty...")
    historical_prompts = load_historical_prompts()
    current_prompts = load_current_prompts()
    all_prompts = historical_prompts + current_prompts
    logger.info(f"✅ Celkom {len(all_prompts)} promptov")
    
    # Filtruj podľa dĺžky
    logger.info(f"🔍 Filtrujem prompty (limit: {MAX_WORDS} slov)...")
    filtered_prompts = filter_prompts_by_length(all_prompts, MAX_WORDS)
    
    # Načítaj už spracované
    existing_ids = load_existing_activities()
    
    # Filtruj už spracované
    prompts_to_process = [p for p in filtered_prompts if p["prompt_id"] not in existing_ids]
    logger.info(f"📊 Zostáva spracovať {len(prompts_to_process)} promptov")
    
    # Test mode - len prvých N promptov
    if TEST_MODE:
        prompts_to_process = prompts_to_process[:TEST_LIMIT]
        logger.info(f"🧪 TEST MODE: Spracujem len prvých {TEST_LIMIT} promptov")
    
    if not prompts_to_process:
        logger.info("✅ Všetky prompty už boli spracované!")
        return
    
    # Inicializuj OpenAI client
    client = OpenAI(api_key=API_KEY)
    
    # Spracuj prompty
    logger.info("🚀 Začínam extrakciu...")
    processed = 0
    failed = 0
    
    for i, prompt in enumerate(prompts_to_process, 1):
        prompt_id = prompt["prompt_id"]
        
        logger.info(f"[{i}/{len(prompts_to_process)}] Spracovávam {prompt_id} ({prompt['word_count']} slov)...")
        
        # Extrahuj aktivitu
        summary = extract_activity_summary(prompt["text"], client)
        
        if summary:
            # Vytvor aktivitu data
            activity_data = {
                "prompt_id": prompt_id,
                "date": prompt["date"].strftime("%Y-%m-%d") if isinstance(prompt["date"], datetime) else str(prompt["date"]),
                "timestamp": prompt["timestamp"],
                "word_count": prompt["word_count"],
                "activity": summary["activity"],
                "thoughts": summary["thoughts"],
                "summary_extracted_at": datetime.now().isoformat()
            }
            
            # Ulož
            save_activity(activity_data, OUTPUT_FILE)
            processed += 1
            logger.info(f"✅ Spracované: {summary['activity'][:50]}...")
        else:
            failed += 1
            logger.error(f"❌ Zlyhalo spracovanie {prompt_id}")
        
        # Rate limiting - 60 requests/min = max 1 request za sekundu
        if i < len(prompts_to_process):
            time.sleep(1.1)  # Malý buffer
        
        # Progress update každých BATCH_SIZE promptov
        if i % BATCH_SIZE == 0:
            logger.info(f"📊 Progress: {i}/{len(prompts_to_process)} ({i/len(prompts_to_process)*100:.1f}%)")
    
    # Finálny report
    logger.info("="*80)
    logger.info("VÝSLEDKY")
    logger.info("="*80)
    logger.info(f"✅ Úspešne spracovaných: {processed}")
    logger.info(f"❌ Zlyhalo: {failed}")
    logger.info(f"📁 Výstup: {OUTPUT_FILE}")
    logger.info(f"📋 Error log: {ERROR_LOG}")


if __name__ == "__main__":
    main()

