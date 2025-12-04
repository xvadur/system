#!/usr/bin/env python3
"""
Čistenie extrahovaných dát z Kortex backupu.
- Odstránenie duplikátov
- Odstránenie prázdnych záznamov
- Filtrovanie príliš krátkych alebo príliš dlhých textov
"""

import json
import sys
import hashlib
from pathlib import Path
from typing import Dict, List, Set
from collections import defaultdict

workspace_root = Path(__file__).parent.parent
input_dir = workspace_root / "xvadur" / "data" / "kortex_extracted"
output_dir = workspace_root / "xvadur" / "data" / "kortex_cleaned"

output_dir.mkdir(parents=True, exist_ok=True)

print("🧹 Čistenie extrahovaných dát z Kortex backupu\n")
print(f"📁 Input: {input_dir}")
print(f"📁 Output: {output_dir}\n")

# Konfigurácia filtrov
MIN_WORDS = 3  # Minimálny počet slov
MAX_WORDS = 50000  # Maximálny počet slov (príliš dlhé odpovede)


def hash_text(text: str) -> str:
    """Vytvorí hash z textu pre detekciu duplikátov."""
    # Normalizujeme text: lowercase, odstránenie whitespace
    normalized = " ".join(text.lower().split())
    return hashlib.md5(normalized.encode('utf-8')).hexdigest()


def is_valid_text(text: str) -> bool:
    """Skontroluje, či je text validný (nie prázdny, má minimálnu dĺžku)."""
    if not text or not text.strip():
        return False
    
    words = text.split()
    word_count = len(words)
    
    if word_count < MIN_WORDS:
        return False
    
    if word_count > MAX_WORDS:
        return False
    
    return True


def clean_user_prompts() -> Dict:
    """Vyčistí user prompty."""
    print("📝 Čistím user prompty...")
    
    input_file = input_dir / "user_prompts.jsonl"
    output_file = output_dir / "user_prompts_cleaned.jsonl"
    
    seen_hashes: Set[str] = set()
    cleaned_count = 0
    duplicates_count = 0
    empty_count = 0
    too_short_count = 0
    total_count = 0
    
    word_counts = []
    
    with open(input_file, 'r', encoding='utf-8') as f_in, \
         open(output_file, 'w', encoding='utf-8') as f_out:
        
        for line in f_in:
            total_count += 1
            data = json.loads(line)
            
            text = data.get("extracted_text", "")
            
            # Preskočíme prázdne
            if not text:
                empty_count += 1
                continue
            
            # Kontrola validity
            if not is_valid_text(text):
                too_short_count += 1
                continue
            
            # Kontrola duplikátov
            text_hash = hash_text(text)
            if text_hash in seen_hashes:
                duplicates_count += 1
                continue
            
            seen_hashes.add(text_hash)
            
            # Pridáme hash do dát
            data["text_hash"] = text_hash
            
            # Zapíšeme
            f_out.write(json.dumps(data, ensure_ascii=False) + "\n")
            cleaned_count += 1
            
            word_count = data.get("word_count", len(text.split()))
            word_counts.append(word_count)
    
    avg_words = sum(word_counts) / len(word_counts) if word_counts else 0
    
    print(f"  ✅ Celkom: {total_count}")
    print(f"  ✅ Vyčistených: {cleaned_count}")
    print(f"  ✅ Duplikátov: {duplicates_count}")
    print(f"  ✅ Prázdnych: {empty_count}")
    print(f"  ✅ Príliš krátkych: {too_short_count}")
    print(f"  ✅ Priemerná dĺžka: {avg_words:.1f} slov")
    print(f"  ✅ Uložené: {output_file.name}\n")
    
    return {
        "total": total_count,
        "cleaned": cleaned_count,
        "duplicates": duplicates_count,
        "empty": empty_count,
        "too_short": too_short_count,
        "avg_words": avg_words,
        "unique_texts": len(seen_hashes),
    }


def clean_ai_responses() -> Dict:
    """Vyčistí AI odpovede."""
    print("🤖 Čistím AI odpovede...")
    
    input_file = input_dir / "ai_responses.jsonl"
    output_file = output_dir / "ai_responses_cleaned.jsonl"
    
    seen_hashes: Set[str] = set()
    cleaned_count = 0
    duplicates_count = 0
    empty_count = 0
    too_short_count = 0
    total_count = 0
    
    word_counts = []
    
    with open(input_file, 'r', encoding='utf-8') as f_in, \
         open(output_file, 'w', encoding='utf-8') as f_out:
        
        for line in f_in:
            total_count += 1
            data = json.loads(line)
            
            text = data.get("extracted_text", "")
            
            # Preskočíme prázdne
            if not text:
                empty_count += 1
                continue
            
            # Kontrola validity
            if not is_valid_text(text):
                too_short_count += 1
                continue
            
            # Kontrola duplikátov
            text_hash = hash_text(text)
            if text_hash in seen_hashes:
                duplicates_count += 1
                continue
            
            seen_hashes.add(text_hash)
            
            # Pridáme hash do dát
            data["text_hash"] = text_hash
            
            # Zapíšeme
            f_out.write(json.dumps(data, ensure_ascii=False) + "\n")
            cleaned_count += 1
            
            word_count = data.get("word_count", len(text.split()))
            word_counts.append(word_count)
    
    avg_words = sum(word_counts) / len(word_counts) if word_counts else 0
    
    print(f"  ✅ Celkom: {total_count}")
    print(f"  ✅ Vyčistených: {cleaned_count}")
    print(f"  ✅ Duplikátov: {duplicates_count}")
    print(f"  ✅ Prázdnych: {empty_count}")
    print(f"  ✅ Príliš krátkych: {too_short_count}")
    print(f"  ✅ Priemerná dĺžka: {avg_words:.1f} slov")
    print(f"  ✅ Uložené: {output_file.name}\n")
    
    return {
        "total": total_count,
        "cleaned": cleaned_count,
        "duplicates": duplicates_count,
        "empty": empty_count,
        "too_short": too_short_count,
        "avg_words": avg_words,
        "unique_texts": len(seen_hashes),
    }


def clean_conversation_pairs() -> Dict:
    """Vyčistí konverzačné páry."""
    print("🔗 Čistím konverzačné páry...")
    
    input_file = input_dir / "conversation_pairs.jsonl"
    output_file = output_dir / "conversation_pairs_cleaned.jsonl"
    
    # Načítame hash mapu vyčistených user promptov a AI odpovedí
    print("  📖 Načítavam hash mapy z vyčistených dát...")
    
    user_hashes: Set[str] = set()
    ai_hashes: Set[str] = set()
    
    # User prompty
    cleaned_user_file = output_dir / "user_prompts_cleaned.jsonl"
    if cleaned_user_file.exists():
        with open(cleaned_user_file, 'r', encoding='utf-8') as f:
            for line in f:
                data = json.loads(line)
                text_hash = data.get("text_hash")
                if text_hash:
                    user_hashes.add(text_hash)
    
    # AI odpovede
    cleaned_ai_file = output_dir / "ai_responses_cleaned.jsonl"
    if cleaned_ai_file.exists():
        with open(cleaned_ai_file, 'r', encoding='utf-8') as f:
            for line in f:
                data = json.loads(line)
                text_hash = data.get("text_hash")
                if text_hash:
                    ai_hashes.add(text_hash)
    
    print(f"  ✅ Načítaných {len(user_hashes)} user prompt hashov")
    print(f"  ✅ Načítaných {len(ai_hashes)} AI odpoveď hashov")
    
    # Teraz čistíme páry
    seen_pair_hashes: Set[str] = set()
    cleaned_count = 0
    duplicates_count = 0
    invalid_count = 0
    missing_user_count = 0
    missing_ai_count = 0
    total_count = 0
    
    with open(input_file, 'r', encoding='utf-8') as f_in, \
         open(output_file, 'w', encoding='utf-8') as f_out:
        
        for line in f_in:
            total_count += 1
            data = json.loads(line)
            
            user_prompt = data.get("user_prompt", {})
            ai_response = data.get("ai_response", {})
            
            user_text = user_prompt.get("extracted_text", "")
            ai_text = ai_response.get("extracted_text", "")
            
            # Preskočíme prázdne páry
            if not user_text or not ai_text:
                invalid_count += 1
                continue
            
            # Kontrola, či oba texty sú v cleaned dátach
            user_hash = hash_text(user_text)
            ai_hash = hash_text(ai_text)
            
            if user_hash not in user_hashes:
                missing_user_count += 1
                continue
            
            if ai_hash not in ai_hashes:
                missing_ai_count += 1
                continue
            
            # Kontrola duplikátov párov
            pair_hash = hashlib.md5((user_hash + ai_hash).encode()).hexdigest()
            if pair_hash in seen_pair_hashes:
                duplicates_count += 1
                continue
            
            seen_pair_hashes.add(pair_hash)
            
            # Pridáme hash do dát
            data["pair_hash"] = pair_hash
            data["user_prompt"]["text_hash"] = user_hash
            data["ai_response"]["text_hash"] = ai_hash
            
            # Zapíšeme
            f_out.write(json.dumps(data, ensure_ascii=False) + "\n")
            cleaned_count += 1
    
    print(f"  ✅ Celkom: {total_count}")
    print(f"  ✅ Vyčistených: {cleaned_count}")
    print(f"  ✅ Duplikátov: {duplicates_count}")
    print(f"  ✅ Nevalidných: {invalid_count}")
    print(f"  ✅ Chýbajúci user prompt: {missing_user_count}")
    print(f"  ✅ Chýbajúca AI odpoveď: {missing_ai_count}")
    print(f"  ✅ Uložené: {output_file.name}\n")
    
    return {
        "total": total_count,
        "cleaned": cleaned_count,
        "duplicates": duplicates_count,
        "invalid": invalid_count,
        "missing_user": missing_user_count,
        "missing_ai": missing_ai_count,
    }


def main():
    """Hlavná funkcia."""
    
    # Čistíme v poradí: user prompty, AI odpovede, páry
    user_stats = clean_user_prompts()
    ai_stats = clean_ai_responses()
    pairs_stats = clean_conversation_pairs()
    
    # Súhrn
    print("=" * 60)
    print("📊 SÚHRN ČISTENIA")
    print("=" * 60)
    
    print(f"\n📝 User prompty:")
    print(f"  {user_stats['cleaned']} / {user_stats['total']} vyčistených")
    print(f"  {user_stats['duplicates']} duplikátov odstránených")
    print(f"  {user_stats['unique_texts']} unikátnych textov")
    
    print(f"\n🤖 AI odpovede:")
    print(f"  {ai_stats['cleaned']} / {ai_stats['total']} vyčistených")
    print(f"  {ai_stats['duplicates']} duplikátov odstránených")
    print(f"  {ai_stats['unique_texts']} unikátnych textov")
    
    print(f"\n🔗 Konverzačné páry:")
    print(f"  {pairs_stats['cleaned']} / {pairs_stats['total']} vyčistených")
    print(f"  {pairs_stats['duplicates']} duplikátov odstránených")
    
    # Uložíme štatistiky
    stats_file = output_dir / "cleaning_stats.json"
    with open(stats_file, 'w', encoding='utf-8') as f:
        json.dump({
            "user_prompts": user_stats,
            "ai_responses": ai_stats,
            "conversation_pairs": pairs_stats,
        }, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Štatistiky uložené: {stats_file}")
    print(f"\n🎉 Čistenie dokončené!")
    print(f"📁 Výsledky: {output_dir}")


if __name__ == "__main__":
    main()

