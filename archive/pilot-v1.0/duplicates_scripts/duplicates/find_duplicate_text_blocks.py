#!/usr/bin/env python3
"""
Rýchle hľadanie opakujúcich sa veľkých blokov textu pomocou hashovania.
Hľadá presné alebo takmer presné duplikáty veľkých blokov (500+ znakov).
"""

import json
import hashlib
from pathlib import Path
from typing import Dict, List
from collections import defaultdict

workspace_root = Path(__file__).parent.parent
input_dir = workspace_root / "xvadur" / "data" / "kortex_cleaned"
output_dir = workspace_root / "xvadur" / "data" / "kortex_analysis"

output_dir.mkdir(parents=True, exist_ok=True)

print("🔍 Hľadanie opakujúcich sa blokov textu\n")
print(f"📁 Input: {input_dir}")
print(f"📁 Output: {output_dir}\n")

# Konfigurácia
MIN_BLOCK_SIZE = 500  # Minimálna veľkosť bloku (znaky)
HASH_SAMPLE_SIZE = 1000  # Koľko znakov použiť pre hash (prvých 1000)


def normalize_text(text: str) -> str:
    """Normalizuje text pre hash (odstráni whitespace, lowercase)."""
    return " ".join(text.lower().split())


def find_duplicate_blocks(input_file: Path, file_type: str) -> Dict:
    """Nájde opakujúce sa bloky textu."""
    print(f"\n📄 Analyzujem {file_type}...")
    
    if not input_file.exists():
        print(f"  ⚠️  Súbor neexistuje: {input_file}")
        return {}
    
    # Hash map: hash -> list of occurrences
    text_hashes = defaultdict(list)
    total_texts = 0
    texts_processed = 0
    
    print(f"  📖 Načítavam súbor a počítam hash...")
    
    with open(input_file, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            try:
                data = json.loads(line)
                text = data.get("extracted_text", "")
                total_texts += 1
                
                if not text or len(text) < MIN_BLOCK_SIZE:
                    continue
                
                texts_processed += 1
                
                # Normalizujeme text
                normalized = normalize_text(text)
                
                # Vytvoríme hash z prvých N znakov (pre rýchlosť)
                hash_sample = normalized[:HASH_SAMPLE_SIZE]
                text_hash = hashlib.md5(hash_sample.encode()).hexdigest()
                
                # Uložíme výskyt
                text_hashes[text_hash].append({
                    "line_num": line_num,
                    "uuid": data.get("uuid"),
                    "date_created": data.get("date_created"),
                    "text_length": len(text),
                    "word_count": data.get("word_count", len(text.split())),
                    "text_sample": text[:200],  # Prvých 200 znakov pre zobrazenie
                })
                
            except Exception:
                continue
    
    print(f"  ✅ Načítaných {total_texts} textov, {texts_processed} s dĺžkou >= {MIN_BLOCK_SIZE}")
    
    # Nájdeme duplikáty (hash, ktorý sa vyskytuje viackrát)
    duplicate_hashes = {
        h: items for h, items in text_hashes.items()
        if len(items) > 1
    }
    
    print(f"  🔍 Opakujúce sa bloky textu: {len(duplicate_hashes)}")
    
    # Zoradíme podľa počtu výskytov
    sorted_duplicates = sorted(
        duplicate_hashes.items(),
        key=lambda x: len(x[1]),
        reverse=True
    )
    
    # Príprava výsledkov
    total_duplicate_occurrences = sum(len(items) for _, items in duplicate_hashes.items())
    
    top_duplicates = []
    for hash_val, items in sorted_duplicates[:20]:  # Top 20
        top_duplicates.append({
            "occurrences": len(items),
            "text_sample": items[0]["text_sample"],
            "avg_length": sum(i["text_length"] for i in items) / len(items),
            "word_count": items[0]["word_count"],
            "first_seen": min(i["date_created"] for i in items if i.get("date_created")),
            "last_seen": max(i["date_created"] for i in items if i.get("date_created")),
            "all_occurrences": [
                {
                    "line_num": i["line_num"],
                    "date": i.get("date_created", "")[:10],
                    "length": i["text_length"],
                }
                for i in items
            ],
        })
    
    return {
        "total_texts": total_texts,
        "texts_processed": texts_processed,
        "unique_blocks": len(text_hashes),
        "duplicate_blocks": len(duplicate_hashes),
        "total_duplicate_occurrences": total_duplicate_occurrences,
        "top_duplicates": top_duplicates,
    }


def main():
    """Hlavná funkcia."""
    
    results = {}
    
    print("=" * 60)
    
    # Analyzujeme user prompty
    if (input_dir / "user_prompts_cleaned.jsonl").exists():
        results["user_prompts"] = find_duplicate_blocks(
            input_dir / "user_prompts_cleaned.jsonl",
            "user prompty"
        )
    
    # Analyzujeme AI odpovede
    if (input_dir / "ai_responses_cleaned.jsonl").exists():
        results["ai_responses"] = find_duplicate_blocks(
            input_dir / "ai_responses_cleaned.jsonl",
            "AI odpovede"
        )
    
    # Uložíme výsledky
    output_file = output_dir / "duplicate_text_blocks.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    # Vypíšeme súhrn
    print("\n" + "=" * 60)
    print("📊 SÚHRN - OPAKUJÚCE SA BLOKY TEXTU")
    print("=" * 60)
    
    for file_type, stats in results.items():
        if not stats:
            continue
        
        print(f"\n📄 {file_type}:")
        print(f"  Celkom textov: {stats.get('total_texts', 0)}")
        print(f"  Textov >= {MIN_BLOCK_SIZE} znakov: {stats.get('texts_processed', 0)}")
        print(f"  Unikátnych blokov: {stats.get('unique_blocks', 0)}")
        print(f"  Opakujúce sa bloky: {stats.get('duplicate_blocks', 0)}")
        print(f"  Celkom výskytov duplikátov: {stats.get('total_duplicate_occurrences', 0)}")
        
        top_duplicates = stats.get('top_duplicates', [])
        if top_duplicates:
            print(f"\n  🔝 Top opakujúce sa bloky:")
            for i, dup in enumerate(top_duplicates[:5], 1):
                print(f"    {i}. {dup['occurrences']}x výskytov, ~{dup['avg_length']:.0f} znakov")
                print(f"       Prvý výskyt: {dup.get('first_seen', 'N/A')[:10]}")
                print(f"       Posledný výskyt: {dup.get('last_seen', 'N/A')[:10]}")
                print(f"       Sample: {dup['text_sample']}...")
    
    print(f"\n💾 Výsledky uložené: {output_file}")
    print("\n🎉 Analýza dokončená!")


if __name__ == "__main__":
    main()

