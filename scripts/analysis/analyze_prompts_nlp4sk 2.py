#!/usr/bin/env python3
"""
Analyzuje prompty pomocou lokálnych NLP nástrojov (Stanza, Hugging Face, spaCy).
Extrahuje entít, sentiment a pojmy z každého promptu.
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

# Lokálne NLP knižnice
try:
    import stanza
    from transformers import pipeline
except ImportError:
    print("❌ Chyba: Potrebuješ nainštalovať stanza a transformers")
    print("   pip install stanza transformers torch")
    sys.exit(1)

# Konfigurácia
PROMPTS_SPLIT_DIR = Path("data/prompts/prompts_split")
PROMPTS_LOG_PATH = Path("xvadur/data/prompts_log.jsonl")
OUTPUT_FILE = Path("data/prompts/prompts_nlp4sk.jsonl")
ERROR_LOG = Path("data/prompts/nlp4sk_errors.log")
BATCH_SIZE = 10
TEST_MODE = False  # Ak True, spracuje len prvých 20 promptov
TEST_LIMIT = 20
MAX_WORDS = 1000  # Filtrovanie dlhých promptov

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

# Globálne pipeline objekty (lazy loading)
_stanza_nlp = None
_sentiment_pipeline = None


def init_stanza():
    """Inicializuje Stanza pipeline pre slovenčinu."""
    global _stanza_nlp
    
    if _stanza_nlp is not None:
        return _stanza_nlp
    
    try:
        logger.info("🔄 Inicializujem Stanza pipeline pre slovenčinu...")
        logger.info("   (Prvé spustenie môže trvať ~1-2 minúty - stiahnutie modelu)")
        # Použijeme default package, ktorý obsahuje všetky procesory vrátane NER
        _stanza_nlp = stanza.Pipeline('sk', use_gpu=False)
        logger.info("✅ Stanza pipeline inicializovaný")
        return _stanza_nlp
    except Exception as e:
        logger.error(f"❌ Chyba pri inicializácii Stanza: {e}")
        logger.error("   Skús: python3 -c 'import stanza; stanza.download(\"sk\")'")
        # Fallback - skús bez NER
        try:
            logger.info("🔄 Skúšam bez NER...")
            _stanza_nlp = stanza.Pipeline('sk', processors='tokenize,lemma,pos', use_gpu=False)
            logger.info("✅ Stanza pipeline inicializovaný (bez NER)")
            return _stanza_nlp
        except Exception as e2:
            logger.error(f"❌ Chyba aj bez NER: {e2}")
            return None


def init_sentiment_pipeline():
    """Inicializuje Hugging Face sentiment pipeline."""
    global _sentiment_pipeline
    
    if _sentiment_pipeline is not None:
        return _sentiment_pipeline
    
    try:
        logger.info("🔄 Inicializujem Hugging Face sentiment pipeline...")
        logger.info("   (Prvé spustenie môže trvať ~2-3 minúty - stiahnutie modelu)")
        import torch
        device = -1 if not torch.cuda.is_available() else 0
        
        # Skús najprv multilingual model optimalizovaný pre všeobecný text
        try:
            logger.info("   Skúšam nlptown/bert-base-multilingual-uncased-sentiment...")
            _sentiment_pipeline = pipeline(
                "sentiment-analysis",
                model="nlptown/bert-base-multilingual-uncased-sentiment",
                device=device
            )
            logger.info("✅ Sentiment pipeline inicializovaný (multilingual BERT)")
            return _sentiment_pipeline
        except Exception as e1:
            logger.warning(f"   Prvý model zlyhal: {e1}")
            # Fallback - skús default model
            try:
                logger.info("   Skúšam default sentiment model...")
                _sentiment_pipeline = pipeline("sentiment-analysis", device=device)
                logger.info("✅ Alternatívny sentiment pipeline inicializovaný (default)")
                return _sentiment_pipeline
            except Exception as e2:
                logger.error(f"❌ Chyba aj s default modelom: {e2}")
                return None
    except Exception as e:
        logger.error(f"❌ Chyba pri inicializácii sentiment pipeline: {e}")
        import traceback
        logger.debug(traceback.format_exc())
        return None


def extract_sentiment(text: str, sentiment_pipeline) -> Optional[Dict]:
    """Extrahuje sentiment pomocou Hugging Face transformers."""
    if not sentiment_pipeline:
        return None
    
    try:
        # Limit na 512 znakov (transformers limit)
        text_to_analyze = text[:512]
        result = sentiment_pipeline(text_to_analyze)
        
        if not result or len(result) == 0:
            return None
        
        # Rôzne modely môžu vracať rôzne formáty
        if isinstance(result, list):
            first_result = result[0] if len(result) > 0 else result
        else:
            first_result = result
        
        label = str(first_result.get('label', '')).upper()
        score = float(first_result.get('score', 0.0))
        
        # Mapovanie pre rôzne modely
        # nlptown/bert-base-multilingual-uncased-sentiment používa: "1 star", "2 stars", "3 stars", "4 stars", "5 stars"
        # Default model používa: POSITIVE, NEGATIVE
        # Twitter model používa: LABEL_0 (negative), LABEL_1 (neutral), LABEL_2 (positive)
        
        sentiment_map = {
            # Twitter model
            'LABEL_0': 'negative',
            'LABEL_1': 'neutral', 
            'LABEL_2': 'positive',
            # Default model
            'NEGATIVE': 'negative',
            'POSITIVE': 'positive',
            # nlptown model (5-star rating) - case insensitive
            '1 STAR': 'negative',
            '1 STARS': 'negative',
            '2 STAR': 'negative',
            '2 STARS': 'negative',
            '3 STAR': 'neutral',
            '3 STARS': 'neutral',
            '4 STAR': 'positive',
            '4 STARS': 'positive',
            '5 STAR': 'positive',
            '5 STARS': 'positive',
            # S lowercase (ak by sa stalo)
            '1 star': 'negative',
            '1 stars': 'negative',
            '2 star': 'negative',
            '2 stars': 'negative',
            '3 star': 'neutral',
            '3 stars': 'neutral',
            '4 star': 'positive',
            '4 stars': 'positive',
            '5 star': 'positive',
            '5 stars': 'positive',
            # Numerické verzie
            '1': 'negative',
            '2': 'negative',
            '3': 'neutral',
            '4': 'positive',
            '5': 'positive',
        }
        
        # Normalizuj label (odstráni medzery, lowercase)
        label_normalized = label.strip().upper()
        sentiment = sentiment_map.get(label_normalized, 'neutral')
        
        # Pre nlptown model: ak je 3 stars, považuj za neutral
        # Ak je score nízky (< 0.4), považuj za neutral (menej agresívne)
        if score < 0.4:
            sentiment = 'neutral'
        
        return {
            "sentiment": sentiment,
            "sentiment_score": score,
            "raw": result,
            "raw_label": label  # Pre debugging
        }
    except Exception as e:
        logger.warning(f"Chyba pri sentiment analýze: {e}")
        import traceback
        logger.debug(traceback.format_exc())
        return None


def extract_entities(text: str, stanza_nlp) -> Optional[Dict]:
    """Extrahuje entít pomocou Stanza NER alebo alternatívnych metód."""
    if not stanza_nlp:
        return None
    
    try:
        doc = stanza_nlp(text)
        
        people = []
        organizations = []
        locations = []
        technologies = []
        
        # Tech keywords pre identifikáciu technológií
        tech_keywords = ["api", "python", "javascript", "react", "openai", "n8n", 
                        "chainlit", "mcp", "docker", "git", "github", "node", "npm",
                        "typescript", "vue", "angular", "fastapi", "flask", "django",
                        "postgresql", "mysql", "mongodb", "redis", "elasticsearch"]
        
        # Skús použiť NER ak je dostupný
        has_ner = False
        for sentence in doc.sentences:
            if hasattr(sentence, 'entities') and sentence.entities:
                has_ner = True
                for entity in sentence.entities:
                    entity_type = entity.type
                    entity_text = entity.text
                    
                    if entity_type == "PERSON":
                        people.append(entity_text)
                    elif entity_type in ["ORG", "ORGANIZATION"]:
                        organizations.append(entity_text)
                    elif entity_type in ["LOC", "LOCATION", "GPE"]:
                        locations.append(entity_text)
        
        # Ak NER nie je dostupný, použijeme alternatívne metódy
        if not has_ner:
            # Extrahuje vlastné mená (PROPN) ako potenciálnych ľudí alebo organizácie
            # Ignorujeme "Adam" - je to užívateľ, ktorý píše o sebe
            ignored_names = ["adam", "adama", "adamovi", "adamom"]  # Rôzne skloňovania
            
            for sentence in doc.sentences:
                for word in sentence.words:
                    if word.upos == "PROPN" and len(word.text) > 2:
                        word_lower = word.text.lower()
                        
                        # Ignoruj "Adam" a jeho skloňovania
                        if word_lower in ignored_names:
                            continue
                        
                        # Skúsi identifikovať podľa kontextu
                        # Známe mená (môžeš rozšíriť)
                        known_names = ["vlado", "petr", "laura"]
                        if word_lower in known_names:
                            people.append(word.text)
                        else:
                            # Inak to môže byť organizácia alebo meno
                            # Pre jednoduchosť pridáme do people (môžeš upraviť)
                            if word.text[0].isupper():
                                people.append(word.text)
        
        # Vždy skúsi nájsť technológie v celom texte
        text_lower = text.lower()
        for keyword in tech_keywords:
            if keyword in text_lower:
                # Nájde kontext okolo kľúčového slova
                idx = text_lower.find(keyword)
                if idx >= 0:
                    start = max(0, idx - 10)
                    end = min(len(text), idx + len(keyword) + 10)
                    context = text[start:end]
                    # Extrahuje slovo (možno s veľkým písmenom)
                    words = context.split()
                    for word in words:
                        if keyword in word.lower() and word not in technologies:
                            # Vyčisti slovo (odstráni interpunkciu)
                            clean_word = word.strip('.,!?;:()[]{}"\'')
                            if clean_word and len(clean_word) > 2:
                                technologies.append(clean_word)
        
        return {
            "people": list(set(people)),  # Odstráni duplikáty
            "organizations": list(set(organizations)),
            "locations": list(set(locations)),
            "technologies": list(set(technologies)),
            "raw": None  # Stanza neposkytuje raw JSON
        }
    except Exception as e:
        logger.warning(f"Chyba pri NER: {e}")
        return None


def extract_concepts(text: str, stanza_nlp) -> Optional[Dict]:
    """Extrahuje kľúčové pojmy pomocou Stanza (noun phrases a významné slová)."""
    if not stanza_nlp:
        return None
    
    try:
        doc = stanza_nlp(text)
        concepts = []
        
        # Extrahuje podstatné mená a významné frázy
        for sentence in doc.sentences:
            for word in sentence.words:
                # Filtruje podstatné mená, vlastné mená a významné slová
                if word.upos in ['NOUN', 'PROPN'] and len(word.text) > 3:
                    # Použije lemma (základný tvar) namiesto skloňovaného tvaru
                    lemma = word.lemma if hasattr(word, 'lemma') and word.lemma else word.text
                    concepts.append(lemma.lower())
        
        # Odstráni duplikáty a vráti top 20
        unique_concepts = list(set(concepts))[:20]
        
        return {
            "concepts": unique_concepts,
            "raw": None
        }
    except Exception as e:
        logger.warning(f"Chyba pri extrakcii pojmov: {e}")
        return None


def analyze_prompt_with_local_nlp(prompt_data: Dict, stanza_nlp, sentiment_pipeline) -> Dict:
    """
    Analyzuje jeden prompt pomocou lokálnych NLP nástrojov.
    
    Args:
        prompt_data: Dict s prompt_id, text (surový text)
        stanza_nlp: Stanza pipeline objekt
        sentiment_pipeline: Hugging Face sentiment pipeline
    
    Returns:
        Dict s výsledkami analýzy
    """
    # Použijeme surový text priamo
    text_to_analyze = prompt_data.get("text", "")
    
    if not text_to_analyze.strip():
        logger.warning(f"⚠️  Prázdny text pre {prompt_data.get('prompt_id')}")
        text_to_analyze = ""
    
    # Konvertuj date na string ak je datetime objekt
    date_value = prompt_data.get("date")
    if isinstance(date_value, datetime):
        date_str = date_value.strftime("%Y-%m-%d")
    else:
        date_str = str(date_value) if date_value else ""
    
    results = {
        "prompt_id": prompt_data.get("prompt_id"),
        "date": date_str,
        "timestamp": prompt_data.get("timestamp", ""),
        "word_count": prompt_data.get("word_count", 0),
    }
    
    # Extrakcia sentimentu
    logger.info(f"  📊 Analyzujem sentiment...")
    sentiment_result = extract_sentiment(text_to_analyze, sentiment_pipeline)
    if sentiment_result:
        results["sentiment"] = sentiment_result.get("sentiment", "neutral")
        results["sentiment_score"] = sentiment_result.get("sentiment_score", 0.0)
    else:
        results["sentiment"] = None
        results["sentiment_score"] = None
    
    # Extrakcia entít
    logger.info(f"  🔍 Extrahujem entít...")
    entities_result = extract_entities(text_to_analyze, stanza_nlp)
    if entities_result:
        results["people"] = entities_result.get("people", [])
        results["organizations"] = entities_result.get("organizations", [])
        results["locations"] = entities_result.get("locations", [])
        results["technologies"] = entities_result.get("technologies", [])
    else:
        results["people"] = []
        results["organizations"] = []
        results["locations"] = []
        results["technologies"] = []
    
    # Extrakcia pojmov
    logger.info(f"  💡 Extrahujem pojmy...")
    concepts_result = extract_concepts(text_to_analyze, stanza_nlp)
    if concepts_result:
        results["concepts"] = concepts_result.get("concepts", [])
    else:
        results["concepts"] = []
    
    results["analyzed_at"] = datetime.now().isoformat()
    
    return results


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
    
    logger.info(f"✅ Načítaných {len(prompts)} historických promptov")
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
                    word_count = len(text.split())
                    
                    prompts.append({
                        "prompt_id": f"current_{line_num}",
                        "date": date,
                        "timestamp": timestamp_str,
                        "text": text,
                        "word_count": word_count,
                    })
                except json.JSONDecodeError as e:
                    logger.warning(f"Chyba pri parsovaní riadku {line_num}: {e}")
                    continue
    except Exception as e:
        logger.error(f"Chyba pri načítaní {PROMPTS_LOG_PATH}: {e}")
    
    logger.info(f"✅ Načítaných {len(prompts)} aktuálnych promptov")
    return prompts


def filter_prompts_by_length(prompts: List[Dict], max_words: int = MAX_WORDS) -> List[Dict]:
    """Filtruje prompty podľa dĺžky."""
    filtered = [p for p in prompts if p.get("word_count", 0) < max_words]
    logger.info(f"🔍 Filtrovaných {len(filtered)} promptov z {len(prompts)} (limit: {max_words} slov)")
    return filtered


def load_prompts() -> List[Dict]:
    """Načíta všetky prompty z surových dát (prompts_split + prompts_log)."""
    logger.info("📖 Načítavam surové prompty...")
    historical_prompts = load_historical_prompts()
    current_prompts = load_current_prompts()
    all_prompts = historical_prompts + current_prompts
    
    # Filtruj podľa dĺžky
    filtered_prompts = filter_prompts_by_length(all_prompts, MAX_WORDS)
    
    return filtered_prompts


def load_existing_analyses() -> set:
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
        logger.warning(f"Chyba pri načítaní existujúcich analýz: {e}")
    
    logger.info(f"✅ Načítaných {len(existing)} už spracovaných promptov")
    return existing


def save_analysis(analysis_data: Dict, output_path: Path):
    """Uloží jednu analýzu do JSONL súboru."""
    try:
        with open(output_path, 'a', encoding='utf-8') as f:
            f.write(json.dumps(analysis_data, ensure_ascii=False) + '\n')
            f.flush()
    except Exception as e:
        logger.error(f"Chyba pri ukladaní analýzy: {e}")
        raise


def main():
    """Hlavná funkcia."""
    logger.info("="*80)
    logger.info("Analýza promptov pomocou lokálnych NLP nástrojov")
    logger.info("="*80)
    
    # Vytvor output adresár ak neexistuje
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    # Inicializuj NLP pipeline
    logger.info("🔧 Inicializujem NLP nástroje...")
    stanza_nlp = init_stanza()
    sentiment_pipeline = init_sentiment_pipeline()
    
    if not stanza_nlp:
        logger.error("❌ Stanza pipeline sa nepodarilo inicializovať!")
        logger.error("   Skús: python3 -c 'import stanza; stanza.download(\"sk\")'")
        sys.exit(1)
    
    if not sentiment_pipeline:
        logger.warning("⚠️  Sentiment pipeline sa nepodarilo inicializovať!")
        logger.warning("   Analýza sentimentu nebude dostupná.")
    
    # Načítaj prompty
    logger.info("📖 Načítavam prompty...")
    all_prompts = load_prompts()
    
    if not all_prompts:
        logger.error("❌ Žiadne prompty na spracovanie!")
        return
    
    # Načítaj už spracované
    existing_ids = load_existing_analyses()
    
    # Filtruj už spracované
    prompts_to_process = [p for p in all_prompts if p.get("prompt_id") not in existing_ids]
    logger.info(f"📊 Zostáva spracovať {len(prompts_to_process)} promptov")
    
    # Test mode - len prvých N promptov
    if TEST_MODE:
        prompts_to_process = prompts_to_process[:TEST_LIMIT]
        logger.info(f"🧪 TEST MODE: Spracujem len prvých {TEST_LIMIT} promptov")
    
    if not prompts_to_process:
        logger.info("✅ Všetky prompty už boli spracované!")
        return
    
    # Spracuj prompty
    logger.info("🚀 Začínam analýzu pomocou lokálnych NLP nástrojov...")
    processed = 0
    failed = 0
    start_time = time.time()
    
    for i, prompt in enumerate(prompts_to_process, 1):
        prompt_id = prompt.get("prompt_id", "unknown")
        
        logger.info(f"[{i}/{len(prompts_to_process)}] Spracovávam {prompt_id}...")
        
        # Analyzuj prompt
        try:
            analysis = analyze_prompt_with_local_nlp(prompt, stanza_nlp, sentiment_pipeline)
            
            # Ulož
            save_analysis(analysis, OUTPUT_FILE)
            processed += 1
            
            # Zobraz výsledky
            sentiment = analysis.get("sentiment", "N/A")
            people_count = len(analysis.get("people", []))
            tech_count = len(analysis.get("technologies", []))
            concepts_count = len(analysis.get("concepts", []))
            
            logger.info(f"✅ Spracované: sentiment={sentiment}, people={people_count}, tech={tech_count}, concepts={concepts_count}")
        except Exception as e:
            failed += 1
            logger.error(f"❌ Zlyhalo spracovanie {prompt_id}: {e}")
            import traceback
            logger.debug(traceback.format_exc())
        
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

