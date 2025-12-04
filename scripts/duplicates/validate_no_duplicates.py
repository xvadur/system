#!/usr/bin/env python3
"""
Validácia, že finálne súbory neobsahujú žiadne duplikáty.
Používa presnejšiu metódu - porovnáva celý text, nie len hash prvých 1000 znakov.
"""

import json
import hashlib
from pathlib import Path
from typing import Dict, List, Set
from collections import defaultdict

workspace_root = Path(__file__).parent.parent
input_dir = workspace_root / "xvadur" / "data" / "kortex_final"
output_dir = workspace_root / "xvadur" / "data" / "kortex_validated"

output_dir.mkdir(parents=True, exist_ok=True)

print("✅ Validácia duplikátov vo finálnych súboroch\n")
print(f"📁 Input: {input_dir}")
print(f"📁 Output: {output_dir}\n")


def normalize_text_full(text: str) -> str:
    """Normalizuje celý text pre presné porovnanie."""
    # Normalizujeme whitespace a lowercase
    normalized = " ".join(text.lower().split())
    return normalized


def hash_full_text(text: str) -> str:
    """Vytvorí hash z celého normalizovaného textu."""
    normalized = normalize_text_full(text)
    return hashlib.md5(normalized.encode('utf-8')).hexdigest()


def validate_file(input_file: Path, file_type: str) -> Dict:
    """Validuje jeden súbor na duplikáty."""
    print(f"\n📄 Validujem {file_type}...")
    
    if not input_file.exists():
        print(f"  ⚠️  Súbor neexistuje: {input_file}")
        return {"status": "error", "error": "File not found"}
    
    text_hashes: Dict[str, List[Dict]] = defaultdict(list)
    total_count = 0
    duplicates_found = []
    
    print(f"  📖 Načítavam súbor a kontrolujem duplikáty...")
    
    with open(input_file, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            try:
                data = json.loads(line)
                text = data.get("extracted_text", "")
                total_count += 1
                
                if not text:
                    continue
                
                # Vytvoríme hash z celého textu (nie len z prvých 1000 znakov)
                text_hash = hash_full_text(text)
                
                # Uložíme výskyt
                occurrence = {
                    "line_num": line_num,
                    "uuid": data.get("uuid"),
                    "date_created": data.get("date_created"),
                    "text_length": len(text),
                    "word_count": data.get("word_count", len(text.split())),
                }
                
                text_hashes[text_hash].append(occurrence)
                
                # Ak sa hash už vyskytuje, je to duplikát
                if len(text_hashes[text_hash]) > 1:
                    duplicates_found.append({
                        "hash": text_hash,
                        "occurrences": len(text_hashes[text_hash]),
                        "line_nums": [occ["line_num"] for occ in text_hashes[text_hash]],
                    })
                    
            except Exception as e:
                print(f"  ⚠️  Chyba na riadku {line_num}: {e}")
                continue
    
    # Nájdeme všetky duplikáty
    duplicate_hashes = {
        h: items for h, items in text_hashes.items()
        if len(items) > 1
    }
    
    print(f"  ✅ Načítaných {total_count} textov")
    print(f"  🔍 Unikátnych textov: {len(text_hashes)}")
    print(f"  ⚠️  Duplikátov nájdených: {len(duplicate_hashes)}")
    
    if duplicate_hashes:
        total_duplicate_occurrences = sum(len(items) - 1 for items in duplicate_hashes.values())
        print(f"  ⚠️  Celkom duplikátnych výskytov: {total_duplicate_occurrences}")
        
        # Zobrazíme prvých 5 duplikátov
        print(f"\n  🔝 Príklady duplikátov:")
        for i, (hash_val, items) in enumerate(list(duplicate_hashes.items())[:5], 1):
            print(f"    {i}. Hash {hash_val[:16]}... - {len(items)} výskytov")
            for item in items:
                print(f"       - Riadok {item['line_num']}, {item.get('date_created', 'N/A')[:10]}")
        
        return {
            "status": "has_duplicates",
            "total_texts": total_count,
            "unique_texts": len(text_hashes),
            "duplicate_count": len(duplicate_hashes),
            "total_duplicate_occurrences": total_duplicate_occurrences,
            "duplicates": [
                {
                    "hash": h[:16] + "...",
                    "occurrences": len(items),
                    "line_nums": [item["line_num"] for item in items],
                }
                for h, items in list(duplicate_hashes.items())[:20]
            ],
        }
    else:
        print(f"  ✅ Žiadne duplikáty nájdené!")
        return {
            "status": "no_duplicates",
            "total_texts": total_count,
            "unique_texts": len(text_hashes),
            "duplicate_count": 0,
        }


def remove_remaining_duplicates(input_file: Path, output_file: Path, file_type: str) -> Dict:
    """Odstráni zostávajúce duplikáty z finálneho súboru."""
    print(f"\n🗑️  Odstraňujem zostávajúce duplikáty z {file_type}...")
    
    seen_hashes: Set[str] = set()
    duplicates_removed = 0
    total_count = 0
    kept_count = 0
    
    with open(input_file, 'r', encoding='utf-8') as f_in, \
         open(output_file, 'w', encoding='utf-8') as f_out:
        
        for line_num, line in enumerate(f_in, 1):
            try:
                data = json.loads(line)
                text = data.get("extracted_text", "")
                total_count += 1
                
                if not text:
                    # Prázdne texty ponecháme
                    f_out.write(line)
                    kept_count += 1
                    continue
                
                # Hash celého textu
                text_hash = hash_full_text(text)
                
                # Ak sme už videli tento hash, je to duplikát
                if text_hash in seen_hashes:
                    duplicates_removed += 1
                    continue
                
                # Prvý výskyt - uložíme a zapíšeme
                seen_hashes.add(text_hash)
                f_out.write(line)
                kept_count += 1
                
            except Exception:
                continue
    
    print(f"  ✅ Odstránených {duplicates_removed} duplikátov")
    print(f"  ✅ Ponechaných {kept_count} unikátnych textov")
    
    return {
        "total": total_count,
        "kept": kept_count,
        "removed": duplicates_removed,
    }


def main():
    """Hlavná funkcia."""
    
    results = {}
    
    print("=" * 60)
    
    # Validujeme každý súbor
    user_validation = validate_file(
        input_dir / "user_prompts_final.jsonl",
        "user prompty"
    )
    results["user_prompts"] = user_validation
    
    ai_validation = validate_file(
        input_dir / "ai_responses_final.jsonl",
        "AI odpovede"
    )
    results["ai_responses"] = ai_validation
    
    # Konverzačné páry validujeme inak (kombinácia user + AI)
    print(f"\n🔗 Validujem konverzačné páry...")
    pairs_file = input_dir / "conversation_pairs_final.jsonl"
    
    if pairs_file.exists():
        pair_hashes: Dict[str, List[int]] = defaultdict(list)
        total_pairs = 0
        
        with open(pairs_file, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                try:
                    data = json.loads(line)
                    total_pairs += 1
                    
                    user_text = data.get("user_prompt", {}).get("extracted_text", "")
                    ai_text = data.get("ai_response", {}).get("extracted_text", "")
                    
                    if not user_text or not ai_text:
                        continue
                    
                    # Hash kombinácie user + AI textu
                    combined_text = user_text + "\n---\n" + ai_text
                    pair_hash = hash_full_text(combined_text)
                    
                    pair_hashes[pair_hash].append(line_num)
                    
                except Exception:
                    continue
        
        duplicate_pairs = {h: items for h, items in pair_hashes.items() if len(items) > 1}
        
        print(f"  ✅ Načítaných {total_pairs} párov")
        print(f"  🔍 Unikátnych párov: {len(pair_hashes)}")
        print(f"  ⚠️  Duplikátov nájdených: {len(duplicate_pairs)}")
        
        if duplicate_pairs:
            total_duplicate_occurrences = sum(len(items) - 1 for items in duplicate_pairs.values())
            print(f"  ⚠️  Celkom duplikátnych výskytov: {total_duplicate_occurrences}")
        
        results["conversation_pairs"] = {
            "status": "no_duplicates" if not duplicate_pairs else "has_duplicates",
            "total_pairs": total_pairs,
            "unique_pairs": len(pair_hashes),
            "duplicate_count": len(duplicate_pairs),
        }
    
    # Uložíme výsledky validácie
    validation_file = output_dir / "validation_results.json"
    with open(validation_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    # Súhrn
    print("\n" + "=" * 60)
    print("📊 SÚHRN VALIDÁCIE")
    print("=" * 60)
    
    has_duplicates = False
    
    for file_type, validation in results.items():
        if not validation or validation.get("status") == "error":
            continue
        
        status = validation.get("status", "unknown")
        duplicate_count = validation.get("duplicate_count", 0)
        
        print(f"\n📄 {file_type}:")
        if status == "no_duplicates":
            print(f"  ✅ Žiadne duplikáty")
            print(f"  ✅ Unikátnych textov: {validation.get('unique_texts', 0)}")
        else:
            print(f"  ⚠️  Nájdených {duplicate_count} duplikátov")
            print(f"  ⚠️  Celkom {validation.get('total_duplicate_occurrences', 0)} duplikátnych výskytov")
            has_duplicates = True
    
    # Ak sú duplikáty, odstránime ich
    if has_duplicates:
        print(f"\n🗑️  Odstraňujem zostávajúce duplikáty...")
        
        if results.get("user_prompts", {}).get("status") == "has_duplicates":
            remove_remaining_duplicates(
                input_dir / "user_prompts_final.jsonl",
                output_dir / "user_prompts_validated.jsonl",
                "user prompty"
            )
        
        if results.get("ai_responses", {}).get("status") == "has_duplicates":
            remove_remaining_duplicates(
                input_dir / "ai_responses_final.jsonl",
                output_dir / "ai_responses_validated.jsonl",
                "AI odpovede"
            )
        
        print(f"\n✅ Finálne súbory bez duplikátov: {output_dir}")
    else:
        print(f"\n✅ Všetky súbory sú bez duplikátov!")
    
    print(f"\n💾 Validácia uložená: {validation_file}")
    print("\n🎉 Validácia dokončená!")


if __name__ == "__main__":
    main()

