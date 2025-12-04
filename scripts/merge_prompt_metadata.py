#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Merge Prompt Metadata: Konsolidácia troch JSONL súborov do jednej štruktúry.

Zlúči:
- prompts_activities.jsonl (activity, thoughts)
- prompts_nlp4sk.jsonl (sentiment, entities, concepts)
- prompts_categorized.jsonl (category, subcategory, context)

Výstup: prompts_enriched.jsonl (kompletná štruktúra s všetkými metadátami)
"""

import json
import sys
from pathlib import Path
from typing import Dict, Optional
from collections import defaultdict

# Cesty k súborom
ACTIVITIES_FILE = Path("data/prompts/prompts_activities.jsonl")
NLP4SK_FILE = Path("data/prompts/prompts_nlp4sk.jsonl")
CATEGORIZED_FILE = Path("data/prompts/prompts_categorized.jsonl")
OUTPUT_FILE = Path("data/prompts/prompts_enriched.jsonl")


def load_jsonl(file_path: Path) -> Dict[str, Dict]:
    """
    Načíta JSONL súbor a vráti dictionary s prompt_id ako kľúčom.
    
    Returns:
        Dict[str, Dict] - {prompt_id: data}
    """
    data = {}
    
    if not file_path.exists():
        print(f"⚠️  Súbor neexistuje: {file_path}")
        return data
    
    print(f"📖 Načítavam: {file_path.name}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            
            try:
                record = json.loads(line)
                prompt_id = record.get("prompt_id")
                
                if not prompt_id:
                    print(f"⚠️  Riadok {line_num}: Chýba prompt_id")
                    continue
                
                data[prompt_id] = record
            except json.JSONDecodeError as e:
                print(f"⚠️  Riadok {line_num}: JSON decode error - {e}")
                continue
    
    print(f"   ✅ Načítaných {len(data)} záznamov")
    return data


def merge_metadata(
    activities: Dict[str, Dict],
    nlp4sk: Dict[str, Dict],
    categorized: Dict[str, Dict]
) -> Dict[str, Dict]:
    """
    Zlúči metadáta z troch zdrojov do jednej štruktúry.
    
    Štruktúra výstupu:
    {
        "prompt_id": str,
        "date": str,
        "timestamp": str,
        "word_count": int,
        
        # Activity metadata
        "activity": Optional[str],
        "thoughts": Optional[str],
        "summary_extracted_at": Optional[str],
        
        # NLP metadata
        "sentiment": Optional[str],
        "sentiment_score": Optional[float],
        "people": Optional[List[str]],
        "organizations": Optional[List[str]],
        "locations": Optional[List[str]],
        "technologies": Optional[List[str]],
        "concepts": Optional[List[str]],
        "analyzed_at": Optional[str],
        
        # Category metadata
        "category": Optional[str],
        "subcategory": Optional[str],
        "context": Optional[Dict],
        "categorized_at": Optional[str]
    }
    """
    # Zbieranie všetkých prompt_id
    all_ids = set()
    all_ids.update(activities.keys())
    all_ids.update(nlp4sk.keys())
    all_ids.update(categorized.keys())
    
    print(f"\n🔀 Zlučujem metadáta pre {len(all_ids)} promptov...")
    
    merged = {}
    stats = defaultdict(int)
    
    for prompt_id in sorted(all_ids):
        # Začíname s prázdnym záznamom
        record = {
            "prompt_id": prompt_id,
            "date": None,
            "timestamp": None,
            "word_count": None,
        }
        
        # Activity metadata
        if prompt_id in activities:
            act = activities[prompt_id]
            record.update({
                "date": act.get("date"),
                "timestamp": act.get("timestamp"),
                "word_count": act.get("word_count"),
                "activity": act.get("activity"),
                "thoughts": act.get("thoughts"),
                "summary_extracted_at": act.get("summary_extracted_at"),
            })
            stats["has_activity"] += 1
        
        # NLP metadata (ak nie je v activities, použijeme nlp4sk)
        if prompt_id in nlp4sk:
            nlp = nlp4sk[prompt_id]
            # Aktualizuj len ak ešte nemáme základné metadáta
            if not record.get("date"):
                record["date"] = nlp.get("date")
            if not record.get("timestamp"):
                record["timestamp"] = nlp.get("timestamp")
            if not record.get("word_count"):
                record["word_count"] = nlp.get("word_count")
            
            record.update({
                "sentiment": nlp.get("sentiment"),
                "sentiment_score": nlp.get("sentiment_score"),
                "people": nlp.get("people", []),
                "organizations": nlp.get("organizations", []),
                "locations": nlp.get("locations", []),
                "technologies": nlp.get("technologies", []),
                "concepts": nlp.get("concepts", []),
                "analyzed_at": nlp.get("analyzed_at"),
            })
            stats["has_nlp"] += 1
        
        # Category metadata (categorized obsahuje aj NLP, takže má prioritu)
        if prompt_id in categorized:
            cat = categorized[prompt_id]
            # Aktualizuj základné metadáta ak chýbajú
            if not record.get("date"):
                record["date"] = cat.get("date")
            if not record.get("timestamp"):
                record["timestamp"] = cat.get("timestamp")
            if not record.get("word_count"):
                record["word_count"] = cat.get("word_count")
            
            # Aktualizuj NLP metadáta (categorized má všetko z nlp4sk)
            record.update({
                "sentiment": cat.get("sentiment"),
                "sentiment_score": cat.get("sentiment_score"),
                "people": cat.get("people", []),
                "organizations": cat.get("organizations", []),
                "locations": cat.get("locations", []),
                "technologies": cat.get("technologies", []),
                "concepts": cat.get("concepts", []),
                "analyzed_at": cat.get("analyzed_at"),
            })
            
            # Pridaj category metadata
            record.update({
                "category": cat.get("category"),
                "subcategory": cat.get("subcategory"),
                "context": cat.get("context"),
                "categorized_at": cat.get("categorized_at"),
            })
            stats["has_category"] += 1
        
        merged[prompt_id] = record
    
    # Štatistiky
    print(f"\n📊 Štatistiky:")
    print(f"   ✅ Má activity: {stats['has_activity']}")
    print(f"   ✅ Má NLP: {stats['has_nlp']}")
    print(f"   ✅ Má category: {stats['has_category']}")
    print(f"   📝 Celkom záznamov: {len(merged)}")
    
    return merged


def save_jsonl(data: Dict[str, Dict], output_path: Path) -> None:
    """Uloží zlúčené dáta do JSONL súboru."""
    print(f"\n💾 Ukladám do: {output_path}")
    
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        for prompt_id in sorted(data.keys()):
            json.dump(data[prompt_id], f, ensure_ascii=False)
            f.write('\n')
    
    print(f"   ✅ Uložených {len(data)} záznamov")


def main():
    """Hlavná funkcia."""
    print("=" * 60)
    print("🔀 MERGE PROMPT METADATA")
    print("=" * 60)
    
    # Načítanie dát
    activities = load_jsonl(ACTIVITIES_FILE)
    nlp4sk = load_jsonl(NLP4SK_FILE)
    categorized = load_jsonl(CATEGORIZED_FILE)
    
    # Merge
    merged = merge_metadata(activities, nlp4sk, categorized)
    
    # Uloženie
    save_jsonl(merged, OUTPUT_FILE)
    
    print("\n" + "=" * 60)
    print("✅ HOTOVO!")
    print("=" * 60)
    print(f"\n📁 Výstupný súbor: {OUTPUT_FILE}")
    print(f"📊 Celkom záznamov: {len(merged)}")
    print(f"\n💡 Použitie:")
    print(f"   import json")
    print(f"   with open('{OUTPUT_FILE}', 'r') as f:")
    print(f"       for line in f:")
    print(f"           data = json.loads(line)")
    print(f"           # data obsahuje všetky metadáta")


if __name__ == "__main__":
    main()

