#!/usr/bin/env python3
"""
Odstránenie duplikátov z vyčistených dát na základe analýzy duplikátov.
Ponechá len prvý výskyt každého duplikátu.
"""

import json
import hashlib
from pathlib import Path
from typing import Dict, Set
from collections import defaultdict

workspace_root = Path(__file__).parent.parent
input_dir = workspace_root / "xvadur" / "data" / "kortex_cleaned"
analysis_file = workspace_root / "xvadur" / "data" / "kortex_analysis" / "duplicate_text_blocks.json"
output_dir = workspace_root / "xvadur" / "data" / "kortex_final"

output_dir.mkdir(parents=True, exist_ok=True)

print("🗑️  Odstránenie duplikátov z vyčistených dát\n")
print(f"📁 Input: {input_dir}")
print(f"📁 Output: {output_dir}\n")

# Konfigurácia
MIN_BLOCK_SIZE = 500
HASH_SAMPLE_SIZE = 1000


def normalize_text(text: str) -> str:
    """Normalizuje text pre hash."""
    return " ".join(text.lower().split())


def load_duplicate_hashes(analysis_file: Path) -> Dict[str, Set[str]]:
    """Načíta hash duplikátov z analýzy."""
    if not analysis_file.exists():
        print(f"  ⚠️  Analýza neexistuje: {analysis_file}")
        return {"user_prompts": set(), "ai_responses": set()}
    
    print(f"  📖 Načítavam analýzu duplikátov...")
    
    with open(analysis_file, 'r', encoding='utf-8') as f:
        analysis_data = json.load(f)
    
    duplicate_hashes = {
        "user_prompts": set(),
        "ai_responses": set(),
    }
    
    # Získame hash duplikátov z analýzy
    # (potrebujeme rekonštruovať hash z textových vzoriek)
    # Alebo použijeme iný prístup - prečítame všetky duplikáty a vytvoríme hash mapu
    
    return duplicate_hashes


def remove_duplicates(input_file: Path, output_file: Path, file_type: str) -> Dict:
    """Odstráni duplikáty z jedného súboru."""
    print(f"\n📄 Čistím {file_type}...")
    
    if not input_file.exists():
        print(f"  ⚠️  Súbor neexistuje: {input_file}")
        return {}
    
    seen_hashes: Dict[str, int] = {}  # hash -> line number prvého výskytu
    duplicates_removed = 0
    total_count = 0
    kept_count = 0
    
    print(f"  📖 Načítavam súbor a identifikujem duplikáty...")
    
    # Najprv prejdeme súbor a identifikujeme duplikáty
    with open(input_file, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            try:
                data = json.loads(line)
                text = data.get("extracted_text", "")
                total_count += 1
                
                if not text or len(text) < MIN_BLOCK_SIZE:
                    # Krátke texty ponecháme
                    continue
                
                # Normalizujeme text
                normalized = normalize_text(text)
                hash_sample = normalized[:HASH_SAMPLE_SIZE]
                text_hash = hashlib.md5(hash_sample.encode()).hexdigest()
                
                # Ak sme už videli tento hash, je to duplikát
                if text_hash in seen_hashes:
                    duplicates_removed += 1
                    continue
                
                # Prvý výskyt - uložíme hash
                seen_hashes[text_hash] = line_num
                
            except Exception:
                continue
    
    print(f"  ✅ Nájdených {duplicates_removed} duplikátov z {total_count} textov")
    
    # Teraz prejdeme súbor znova a zapíšeme len unikátne záznamy
    print(f"  💾 Ukladám vyčistený súbor...")
    
    seen_hashes = {}  # Resetujeme
    duplicates_removed = 0
    kept_count = 0
    
    with open(input_file, 'r', encoding='utf-8') as f_in, \
         open(output_file, 'w', encoding='utf-8') as f_out:
        
        for line_num, line in enumerate(f_in, 1):
            try:
                data = json.loads(line)
                text = data.get("extracted_text", "")
                
                # Krátke texty vždy ponecháme
                if not text or len(text) < MIN_BLOCK_SIZE:
                    f_out.write(line)
                    kept_count += 1
                    continue
                
                # Normalizujeme text
                normalized = normalize_text(text)
                hash_sample = normalized[:HASH_SAMPLE_SIZE]
                text_hash = hashlib.md5(hash_sample.encode()).hexdigest()
                
                # Ak sme už videli tento hash, preskočíme (duplikát)
                if text_hash in seen_hashes:
                    duplicates_removed += 1
                    continue
                
                # Prvý výskyt - uložíme a zapíšeme
                seen_hashes[text_hash] = line_num
                f_out.write(line)
                kept_count += 1
                
            except Exception:
                continue
    
    print(f"  ✅ Odstránených {duplicates_removed} duplikátov")
    print(f"  ✅ Ponechaných {kept_count} unikátnych textov")
    print(f"  ✅ Uložené: {output_file.name}\n")
    
    return {
        "total": total_count,
        "kept": kept_count,
        "removed": duplicates_removed,
    }


def remove_duplicates_from_pairs(input_file: Path, output_file: Path, user_hashes: Set[str], ai_hashes: Set[str]) -> Dict:
    """Odstráni duplikáty z konverzačných párov."""
    print(f"\n🔗 Čistím konverzačné páry...")
    
    if not input_file.exists():
        print(f"  ⚠️  Súbor neexistuje: {input_file}")
        return {}
    
    seen_pair_hashes: Dict[str, int] = {}
    duplicates_removed = 0
    total_count = 0
    kept_count = 0
    
    print(f"  📖 Načítavam súbor...")
    
    with open(input_file, 'r', encoding='utf-8') as f_in, \
         open(output_file, 'w', encoding='utf-8') as f_out:
        
        for line_num, line in enumerate(f_in, 1):
            try:
                data = json.loads(line)
                total_count += 1
                
                user_prompt = data.get("user_prompt", {})
                ai_response = data.get("ai_response", {})
                
                user_text = user_prompt.get("extracted_text", "")
                ai_text = ai_response.get("extracted_text", "")
                
                if not user_text or not ai_text:
                    continue
                
                # Skontrolujeme, či user prompt alebo AI odpoveď nie sú duplikáty
                user_normalized = normalize_text(user_text)
                ai_normalized = normalize_text(ai_text)
                
                user_hash = hashlib.md5(user_normalized[:HASH_SAMPLE_SIZE].encode()).hexdigest()
                ai_hash = hashlib.md5(ai_normalized[:HASH_SAMPLE_SIZE].encode()).hexdigest()
                
                # Ak je user prompt alebo AI odpoveď duplikát, preskočíme
                if user_hash not in user_hashes and len(user_text) >= MIN_BLOCK_SIZE:
                    # User prompt je duplikát (nie je v cleaned user prompts)
                    duplicates_removed += 1
                    continue
                
                if ai_hash not in ai_hashes and len(ai_text) >= MIN_BLOCK_SIZE:
                    # AI odpoveď je duplikát
                    duplicates_removed += 1
                    continue
                
                # Kontrola duplikátu páru
                pair_hash = hashlib.md5((user_hash + ai_hash).encode()).hexdigest()
                if pair_hash in seen_pair_hashes:
                    duplicates_removed += 1
                    continue
                
                seen_pair_hashes[pair_hash] = line_num
                f_out.write(line)
                kept_count += 1
                
            except Exception:
                continue
    
    print(f"  ✅ Odstránených {duplicates_removed} duplikátov")
    print(f"  ✅ Ponechaných {kept_count} unikátnych párov")
    print(f"  ✅ Uložené: {output_file.name}\n")
    
    return {
        "total": total_count,
        "kept": kept_count,
        "removed": duplicates_removed,
    }


def main():
    """Hlavná funkcia."""
    
    results = {}
    
    print("=" * 60)
    
    # Najprv vyčistíme user prompty a AI odpovede
    user_stats = remove_duplicates(
        input_dir / "user_prompts_cleaned.jsonl",
        output_dir / "user_prompts_final.jsonl",
        "user prompty"
    )
    results["user_prompts"] = user_stats
    
    ai_stats = remove_duplicates(
        input_dir / "ai_responses_cleaned.jsonl",
        output_dir / "ai_responses_final.jsonl",
        "AI odpovede"
    )
    results["ai_responses"] = ai_stats
    
    # Načítame hash mapy vyčistených user promptov a AI odpovedí
    print(f"\n📖 Načítavam hash mapy vyčistených dát...")
    
    user_hashes = set()
    with open(output_dir / "user_prompts_final.jsonl", 'r', encoding='utf-8') as f:
        for line in f:
            data = json.loads(line)
            text = data.get("extracted_text", "")
            if text and len(text) >= MIN_BLOCK_SIZE:
                normalized = normalize_text(text)
                hash_val = hashlib.md5(normalized[:HASH_SAMPLE_SIZE].encode()).hexdigest()
                user_hashes.add(hash_val)
    
    ai_hashes = set()
    with open(output_dir / "ai_responses_final.jsonl", 'r', encoding='utf-8') as f:
        for line in f:
            data = json.loads(line)
            text = data.get("extracted_text", "")
            if text and len(text) >= MIN_BLOCK_SIZE:
                normalized = normalize_text(text)
                hash_val = hashlib.md5(normalized[:HASH_SAMPLE_SIZE].encode()).hexdigest()
                ai_hashes.add(hash_val)
    
    print(f"  ✅ Načítaných {len(user_hashes)} user prompt hashov")
    print(f"  ✅ Načítaných {len(ai_hashes)} AI odpoveď hashov")
    
    # Teraz vyčistíme konverzačné páry
    pairs_stats = remove_duplicates_from_pairs(
        input_dir / "conversation_pairs_cleaned.jsonl",
        output_dir / "conversation_pairs_final.jsonl",
        user_hashes,
        ai_hashes
    )
    results["conversation_pairs"] = pairs_stats
    
    # Uložíme štatistiky
    stats_file = output_dir / "removal_stats.json"
    with open(stats_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    # Súhrn
    print("=" * 60)
    print("📊 SÚHRN ODSTÁNENIA DUPLIKÁTOV")
    print("=" * 60)
    
    print(f"\n📝 User prompty:")
    print(f"  Ponechaných: {user_stats.get('kept', 0)}")
    print(f"  Odstránených: {user_stats.get('removed', 0)}")
    
    print(f"\n🤖 AI odpovede:")
    print(f"  Ponechaných: {ai_stats.get('kept', 0)}")
    print(f"  Odstránených: {ai_stats.get('removed', 0)}")
    
    print(f"\n🔗 Konverzačné páry:")
    print(f"  Ponechaných: {pairs_stats.get('kept', 0)}")
    print(f"  Odstránených: {pairs_stats.get('removed', 0)}")
    
    print(f"\n💾 Štatistiky uložené: {stats_file}")
    print(f"\n🎉 Odstránenie duplikátov dokončené!")
    print(f"📁 Finálne súbory: {output_dir}")


if __name__ == "__main__":
    main()

