#!/usr/bin/env python3
"""
Garantuje, že súbory neobsahujú žiadne duplikáty.
Vytvorí finálne validované súbory s garantovanou absenciou duplikátov.
Používa celý text pre hash (nie len prvých 1000 znakov).
"""

import json
import hashlib
from pathlib import Path
from typing import Set, Dict
from collections import defaultdict

workspace_root = Path(__file__).parent.parent
input_dir = workspace_root / "xvadur" / "data" / "kortex_final"
output_dir = workspace_root / "xvadur" / "data" / "kortex_guaranteed"

output_dir.mkdir(parents=True, exist_ok=True)

print("✅ GARANCIA ŽIADNYCH DUPLIKÁTOV\n")
print(f"📁 Input: {input_dir}")
print(f"📁 Output: {output_dir}\n")

print("Tento skript garantuje, že výstupné súbory NEOBSAHUJÚ žiadne duplikáty.")
print("Používa hash z celého textu (nie len z prvých 1000 znakov).\n")


def normalize_text(text: str) -> str:
    """Normalizuje text pre hash - celý text, nie len vzorka."""
    return " ".join(text.lower().split())


def hash_full_text(text: str) -> str:
    """Vytvorí hash z celého normalizovaného textu."""
    normalized = normalize_text(text)
    return hashlib.md5(normalized.encode('utf-8')).hexdigest()


def guarantee_no_duplicates(input_file: Path, output_file: Path, file_type: str) -> Dict:
    """Garantuje absenciu duplikátov v súbore."""
    print(f"\n📄 Spracovávam {file_type}...")
    
    if not input_file.exists():
        print(f"  ⚠️  Súbor neexistuje: {input_file}")
        return {}
    
    seen_hashes: Set[str] = set()
    duplicates_removed = 0
    total_count = 0
    kept_count = 0
    
    print(f"  📖 Načítavam súbor a garantujem absenciu duplikátov...")
    
    with open(input_file, 'r', encoding='utf-8') as f_in, \
         open(output_file, 'w', encoding='utf-8') as f_out:
        
        for line_num, line in enumerate(f_in, 1):
            try:
                data = json.loads(line)
                text = data.get("extracted_text", "")
                total_count += 1
                
                # Prázdne texty vždy ponecháme
                if not text or not text.strip():
                    f_out.write(line)
                    kept_count += 1
                    continue
                
                # Hash z celého textu (nie len vzorka)
                text_hash = hash_full_text(text)
                
                # Ak sme už videli tento hash, je to duplikát - PRESKOČÍME
                if text_hash in seen_hashes:
                    duplicates_removed += 1
                    if duplicates_removed <= 5:  # Zobrazíme prvých 5
                        print(f"    ⚠️  Duplikát na riadku {line_num} - preskakujem")
                    continue
                
                # Prvý výskyt - pridáme hash a zapíšeme
                seen_hashes.add(text_hash)
                f_out.write(line)
                kept_count += 1
                
            except Exception as e:
                print(f"  ⚠️  Chyba na riadku {line_num}: {e}")
                continue
    
    print(f"  ✅ Spracovaných {total_count} záznamov")
    print(f"  ✅ Odstránených {duplicates_removed} duplikátov")
    print(f"  ✅ Ponechaných {kept_count} unikátnych textov")
    print(f"  ✅ Garantovaných {len(seen_hashes)} unikátnych hashov")
    print(f"  ✅ Uložené: {output_file.name}\n")
    
    return {
        "total": total_count,
        "kept": kept_count,
        "removed": duplicates_removed,
        "unique_hashes": len(seen_hashes),
    }


def guarantee_no_duplicate_pairs(input_file: Path, output_file: Path) -> Dict:
    """Garantuje absenciu duplikátov v konverzačných pároch."""
    print(f"\n🔗 Spracovávam konverzačné páry...")
    
    if not input_file.exists():
        print(f"  ⚠️  Súbor neexistuje: {input_file}")
        return {}
    
    seen_pair_hashes: Set[str] = set()
    duplicates_removed = 0
    total_count = 0
    kept_count = 0
    
    print(f"  📖 Načítavam súbor a garantujem absenciu duplikátov...")
    
    with open(input_file, 'r', encoding='utf-8') as f_in, \
         open(output_file, 'w', encoding='utf-8') as f_out:
        
        for line_num, line in enumerate(f_in, 1):
            try:
                data = json.loads(line)
                total_count += 1
                
                user_text = data.get("user_prompt", {}).get("extracted_text", "")
                ai_text = data.get("ai_response", {}).get("extracted_text", "")
                
                if not user_text or not ai_text:
                    continue
                
                # Hash kombinácie user + AI textu (celý text)
                combined_text = normalize_text(user_text) + "\n---SEPARATOR---\n" + normalize_text(ai_text)
                pair_hash = hash_full_text(combined_text)
                
                # Ak sme už videli tento hash, je to duplikát - PRESKOČÍME
                if pair_hash in seen_pair_hashes:
                    duplicates_removed += 1
                    if duplicates_removed <= 5:
                        print(f"    ⚠️  Duplikát páru na riadku {line_num} - preskakujem")
                    continue
                
                # Prvý výskyt - pridáme hash a zapíšeme
                seen_pair_hashes.add(pair_hash)
                f_out.write(line)
                kept_count += 1
                
            except Exception as e:
                print(f"  ⚠️  Chyba na riadku {line_num}: {e}")
                continue
    
    print(f"  ✅ Spracovaných {total_count} párov")
    print(f"  ✅ Odstránených {duplicates_removed} duplikátov")
    print(f"  ✅ Ponechaných {kept_count} unikátnych párov")
    print(f"  ✅ Garantovaných {len(seen_pair_hashes)} unikátnych hashov")
    print(f"  ✅ Uložené: {output_file.name}\n")
    
    return {
        "total": total_count,
        "kept": kept_count,
        "removed": duplicates_removed,
        "unique_hashes": len(seen_pair_hashes),
    }


def main():
    """Hlavná funkcia."""
    
    results = {}
    
    print("=" * 60)
    
    # Garantujeme absenciu duplikátov v každom súbore
    user_stats = guarantee_no_duplicates(
        input_dir / "user_prompts_final.jsonl",
        output_dir / "user_prompts_guaranteed.jsonl",
        "user prompty"
    )
    results["user_prompts"] = user_stats
    
    ai_stats = guarantee_no_duplicates(
        input_dir / "ai_responses_final.jsonl",
        output_dir / "ai_responses_guaranteed.jsonl",
        "AI odpovede"
    )
    results["ai_responses"] = ai_stats
    
    pairs_stats = guarantee_no_duplicate_pairs(
        input_dir / "conversation_pairs_final.jsonl",
        output_dir / "conversation_pairs_guaranteed.jsonl"
    )
    results["conversation_pairs"] = pairs_stats
    
    # Uložíme štatistiky
    stats_file = output_dir / "guarantee_stats.json"
    with open(stats_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    # Finálna validácia
    print("=" * 60)
    print("🔍 FINÁLNA VALIDÁCIA")
    print("=" * 60)
    
    all_clean = True
    
    for file_type, stats in results.items():
        if not stats:
            continue
        
        removed = stats.get("removed", 0)
        if removed > 0:
            print(f"\n⚠️  {file_type}: Odstránených {removed} duplikátov")
            all_clean = False
        else:
            print(f"\n✅ {file_type}: Žiadne duplikáty")
    
    if all_clean:
        print("\n" + "=" * 60)
        print("✅ VŠETKY SÚBORY SÚ GARANTOVANE BEZ DUPLIKÁTOV!")
        print("=" * 60)
    else:
        print("\n" + "=" * 60)
        print("✅ DUPLIKÁTY BOLI ODSTRÁNENÉ - SÚBORY SÚ TERAZ BEZ DUPLIKÁTOV!")
        print("=" * 60)
    
    # Súhrn
    print("\n📊 SÚHRN:")
    print(f"  User prompty: {results.get('user_prompts', {}).get('kept', 0)} unikátnych")
    print(f"  AI odpovede: {results.get('ai_responses', {}).get('kept', 0)} unikátnych")
    print(f"  Konverzačné páry: {results.get('conversation_pairs', {}).get('kept', 0)} unikátnych")
    
    print(f"\n💾 Štatistiky uložené: {stats_file}")
    print(f"📁 Garantované súbory: {output_dir}")
    print("\n🎉 Garancia dokončená!")


if __name__ == "__main__":
    main()

