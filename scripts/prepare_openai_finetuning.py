#!/usr/bin/env python3
"""
Pripraviť OpenAI Fine-tuning Dataset

Tento skript:
1. Načíta conversation_pairs_guaranteed.jsonl
2. Konvertuje do OpenAI fine-tuning formátu (messages array)
3. Validuje dataset podľa OpenAI požiadaviek
4. Uloží do JSONL súboru pripraveného na upload
5. Vytvorí štatistiky datasetu
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional
from collections import defaultdict

# Pridáme workspace root do sys.path
workspace_root = Path(__file__).parent.parent
sys.path.insert(0, str(workspace_root))

# Konfigurácia
INPUT_FILE = Path("xvadur/data/kortex_guaranteed/conversation_pairs_guaranteed.jsonl")
OUTPUT_DIR = Path("xvadur/data/finetuning")
OUTPUT_FILE = OUTPUT_DIR / "openai_finetuning_dataset.jsonl"
STATS_FILE = OUTPUT_DIR / "finetuning_stats.json"

# OpenAI požiadavky
MIN_EXAMPLES = 10
MAX_TOKENS_ESTIMATE = 1000000  # Odhad (1 token ≈ 4 znaky)


def estimate_tokens(text: str) -> int:
    """
    Odhad počtu tokenov (1 token ≈ 4 znaky pre angličtinu/slovenčinu).
    Pre presnejší odhad by sa použil tiktoken, ale to nie je nutné.
    """
    return len(text) // 4


def validate_example(messages: List[Dict[str, str]]) -> tuple[bool, Optional[str]]:
    """
    Validuje jeden príklad podľa OpenAI požiadaviek.
    
    Returns:
        (is_valid, error_message)
    """
    # Kontrola formátu
    if not isinstance(messages, list):
        return False, "Messages musí byť list"
    
    if len(messages) < 2:
        return False, "Messages musí obsahovať aspoň user a assistant"
    
    # Kontrola role
    roles = [msg.get("role") for msg in messages]
    if "user" not in roles or "assistant" not in roles:
        return False, "Messages musí obsahovať role 'user' a 'assistant'"
    
    # Kontrola content
    for msg in messages:
        if not isinstance(msg, dict):
            return False, "Každá message musí byť dict"
        if "role" not in msg or "content" not in msg:
            return False, "Každá message musí mať 'role' a 'content'"
        if not isinstance(msg["content"], str):
            return False, "Content musí byť string"
        if not msg["content"].strip():
            return False, "Content nemôže byť prázdny"
    
    return True, None


def convert_pair_to_openai_format(pair: Dict[str, Any]) -> Optional[Dict[str, List[Dict[str, str]]]]:
    """
    Konvertuje conversation pair do OpenAI fine-tuning formátu.
    
    Formát:
    {
        "messages": [
            {"role": "user", "content": "..."},
            {"role": "assistant", "content": "..."}
        ]
    }
    """
    try:
        user_text = pair.get("user_prompt", {}).get("extracted_text", "")
        ai_text = pair.get("ai_response", {}).get("extracted_text", "")
        
        # Kontrola prázdnych textov
        if not user_text or not user_text.strip():
            return None
        if not ai_text or not ai_text.strip():
            return None
        
        # Vytvorenie messages array
        messages = [
            {"role": "user", "content": user_text.strip()},
            {"role": "assistant", "content": ai_text.strip()}
        ]
        
        # Validácia
        is_valid, error = validate_example(messages)
        if not is_valid:
            print(f"⚠️  Neplatný príklad: {error}")
            return None
        
        return {"messages": messages}
    
    except Exception as e:
        print(f"⚠️  Chyba pri konverzii páru: {e}")
        return None


def load_conversation_pairs(input_file: Path) -> List[Dict[str, Any]]:
    """Načíta conversation pairs z JSONL súboru."""
    pairs = []
    
    if not input_file.exists():
        print(f"❌ Súbor neexistuje: {input_file}")
        sys.exit(1)
    
    print(f"📖 Načítavam conversation pairs z: {input_file}")
    
    with open(input_file, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            
            try:
                pair = json.loads(line)
                pairs.append(pair)
            except json.JSONDecodeError as e:
                print(f"⚠️  Chyba pri parsovaní riadku {line_num}: {e}")
                continue
    
    print(f"✅ Načítaných {len(pairs)} conversation pairs")
    return pairs


def prepare_dataset(pairs: List[Dict[str, Any]]) -> tuple[List[Dict], Dict[str, Any]]:
    """
    Konvertuje pairs do OpenAI formátu a vytvorí štatistiky.
    
    Returns:
        (valid_examples, stats)
    """
    valid_examples = []
    invalid_count = 0
    
    # Štatistiky
    total_user_length = 0
    total_assistant_length = 0
    total_tokens = 0
    
    print(f"\n🔄 Konvertujem {len(pairs)} párov do OpenAI formátu...")
    
    for i, pair in enumerate(pairs, 1):
        if i % 100 == 0:
            print(f"   Spracovaných {i}/{len(pairs)}...")
        
        openai_format = convert_pair_to_openai_format(pair)
        
        if openai_format:
            valid_examples.append(openai_format)
            
            # Štatistiky
            user_content = openai_format["messages"][0]["content"]
            assistant_content = openai_format["messages"][1]["content"]
            
            total_user_length += len(user_content)
            total_assistant_length += len(assistant_content)
            total_tokens += estimate_tokens(user_content) + estimate_tokens(assistant_content)
        else:
            invalid_count += 1
    
    # Vytvorenie štatistík
    stats = {
        "total_examples": len(pairs),
        "valid_examples": len(valid_examples),
        "invalid_examples": invalid_count,
        "avg_user_length": total_user_length // len(valid_examples) if valid_examples else 0,
        "avg_assistant_length": total_assistant_length // len(valid_examples) if valid_examples else 0,
        "total_tokens_estimate": total_tokens,
        "file_size_mb": 0.0  # Vypočítame neskôr
    }
    
    return valid_examples, stats


def save_dataset(examples: List[Dict], output_file: Path) -> int:
    """Uloží dataset do JSONL súboru a vráti veľkosť súboru v bytoch."""
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    print(f"\n💾 Ukladám dataset do: {output_file}")
    
    total_bytes = 0
    with open(output_file, 'w', encoding='utf-8') as f:
        for example in examples:
            line = json.dumps(example, ensure_ascii=False)
            f.write(line + '\n')
            total_bytes += len(line.encode('utf-8')) + 1  # +1 pre newline
    
    file_size_mb = total_bytes / (1024 * 1024)
    print(f"✅ Dataset uložený ({len(examples)} príkladov, {file_size_mb:.2f} MB)")
    
    return total_bytes


def validate_dataset(examples: List[Dict]) -> tuple[bool, List[str]]:
    """
    Validuje celý dataset podľa OpenAI požiadaviek.
    
    Returns:
        (is_valid, errors)
    """
    errors = []
    
    # Minimálny počet príkladov
    if len(examples) < MIN_EXAMPLES:
        errors.append(f"Dataset musí obsahovať aspoň {MIN_EXAMPLES} príkladov (má {len(examples)})")
    
    # Validácia každého príkladu
    for i, example in enumerate(examples, 1):
        is_valid, error = validate_example(example.get("messages", []))
        if not is_valid:
            errors.append(f"Príklad {i}: {error}")
    
    return len(errors) == 0, errors


def main():
    """Hlavná funkcia."""
    print("=" * 60)
    print("🚀 Pripraviť OpenAI Fine-tuning Dataset")
    print("=" * 60)
    
    # 1. Načítanie conversation pairs
    pairs = load_conversation_pairs(INPUT_FILE)
    
    if not pairs:
        print("❌ Žiadne conversation pairs na spracovanie")
        sys.exit(1)
    
    # 2. Konverzia do OpenAI formátu
    valid_examples, stats = prepare_dataset(pairs)
    
    if not valid_examples:
        print("❌ Žiadne platné príklady po konverzii")
        sys.exit(1)
    
    # 3. Validácia datasetu
    print(f"\n✅ Validujem dataset...")
    is_valid, errors = validate_dataset(valid_examples)
    
    if not is_valid:
        print("❌ Validácia zlyhala:")
        for error in errors[:10]:  # Zobrazíme prvých 10 chýb
            print(f"   - {error}")
        if len(errors) > 10:
            print(f"   ... a ďalších {len(errors) - 10} chýb")
        sys.exit(1)
    
    print("✅ Validácia úspešná")
    
    # 4. Uloženie datasetu
    total_bytes = save_dataset(valid_examples, OUTPUT_FILE)
    stats["file_size_mb"] = total_bytes / (1024 * 1024)
    
    # 5. Uloženie štatistík
    print(f"\n💾 Ukladám štatistiky do: {STATS_FILE}")
    with open(STATS_FILE, 'w', encoding='utf-8') as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)
    print("✅ Štatistiky uložené")
    
    # 6. Zhrnutie
    print("\n" + "=" * 60)
    print("✅ HOTOVO!")
    print("=" * 60)
    print(f"📊 Štatistiky:")
    print(f"   - Celkový počet príkladov: {stats['total_examples']}")
    print(f"   - Platných príkladov: {stats['valid_examples']}")
    print(f"   - Neplatných príkladov: {stats['invalid_examples']}")
    print(f"   - Priemerná dĺžka user promptu: {stats['avg_user_length']} znakov")
    print(f"   - Priemerná dĺžka AI odpovede: {stats['avg_assistant_length']} znakov")
    print(f"   - Odhadovaný počet tokenov: {stats['total_tokens_estimate']:,}")
    print(f"   - Veľkosť súboru: {stats['file_size_mb']:.2f} MB")
    print(f"\n📁 Dataset pripravený na upload:")
    print(f"   {OUTPUT_FILE}")
    print(f"\n💡 Ďalšie kroky:")
    print(f"   1. Otvor https://platform.openai.com/finetuning")
    print(f"   2. Upload súbor: {OUTPUT_FILE}")
    print(f"   3. Vyber model (gpt-3.5-turbo alebo gpt-4)")
    print(f"   4. Spusti tréning")


if __name__ == "__main__":
    main()


