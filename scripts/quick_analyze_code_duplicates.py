#!/usr/bin/env python3
"""
Rýchla analýza duplikátov - len code blocks a snippets.
Bez porovnávania podobností textov (to je príliš pomalé).
"""

import json
import re
import hashlib
from pathlib import Path
from typing import Dict, List
from collections import defaultdict

workspace_root = Path(__file__).parent.parent
input_dir = workspace_root / "xvadur" / "data" / "kortex_cleaned"
output_dir = workspace_root / "xvadur" / "data" / "kortex_analysis"

output_dir.mkdir(parents=True, exist_ok=True)

print("🔍 Rýchla analýza duplikátov (code blocks)\n")
print(f"📁 Input: {input_dir}")
print(f"📁 Output: {output_dir}\n")


def extract_code_blocks(text: str) -> List[str]:
    """Extrahuje code blocks z textu."""
    code_blocks = []
    
    # Markdown code blocks
    pattern = r'```[\s\S]*?```'
    matches = re.findall(pattern, text)
    for match in matches:
        # Odstránime ``` z začiatku a konca
        clean_match = re.sub(r'^```\w*\n?', '', match)
        clean_match = re.sub(r'\n?```$', '', clean_match)
        if clean_match.strip() and len(clean_match.strip()) > 50:
            code_blocks.append(clean_match.strip())
    
    return code_blocks


def analyze_file(input_file: Path, file_type: str) -> Dict:
    """Analyzuje jeden súbor."""
    print(f"\n📄 Analyzujem {file_type}...")
    
    if not input_file.exists():
        print(f"  ⚠️  Súbor neexistuje: {input_file}")
        return {}
    
    code_blocks_all = defaultdict(list)  # hash -> list of occurrences
    texts_with_code = []
    total_texts = 0
    
    print(f"  📖 Načítavam súbor...")
    
    with open(input_file, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            try:
                data = json.loads(line)
                text = data.get("extracted_text", "")
                total_texts += 1
                
                if not text:
                    continue
                
                # Extrahujeme code blocks
                code_blocks = extract_code_blocks(text)
                
                if code_blocks:
                    texts_with_code.append({
                        "line_num": line_num,
                        "uuid": data.get("uuid"),
                        "date_created": data.get("date_created"),
                        "code_blocks_count": len(code_blocks),
                    })
                
                for block in code_blocks:
                    # Hash code blocku (prvých 1000 znakov pre lepšiu detekciu)
                    block_sample = block[:1000].strip()
                    block_hash = hashlib.md5(block_sample.encode()).hexdigest()
                    
                    code_blocks_all[block_hash].append({
                        "sample": block[:300],  # Prvých 300 znakov pre zobrazenie
                        "full_length": len(block),
                        "line_num": line_num,
                        "uuid": data.get("uuid"),
                        "date_created": data.get("date_created"),
                    })
            except Exception as e:
                continue
    
    print(f"  ✅ Načítaných {total_texts} textov")
    print(f"  📦 Textov s code blocks: {len(texts_with_code)}")
    
    # Detekcia opakujúcich sa code blocks
    duplicate_code_blocks = {
        h: items for h, items in code_blocks_all.items() 
        if len(items) > 1
    }
    
    print(f"  🔍 Opakujúce sa code blocks: {len(duplicate_code_blocks)}")
    
    # Zoradíme podľa počtu výskytov
    sorted_duplicates = sorted(
        duplicate_code_blocks.items(),
        key=lambda x: len(x[1]),
        reverse=True
    )
    
    # Príprava detailov
    top_duplicates = []
    total_duplicate_occurrences = 0
    
    for block_hash, items in sorted_duplicates[:20]:  # Top 20
        total_duplicate_occurrences += len(items)
        top_duplicates.append({
            "occurrences": len(items),
            "sample": items[0]["sample"],
            "avg_length": sum(i["full_length"] for i in items) / len(items),
            "first_seen": min(i["date_created"] for i in items if i.get("date_created")),
            "last_seen": max(i["date_created"] for i in items if i.get("date_created")),
        })
    
    return {
        "total_texts": total_texts,
        "texts_with_code_blocks": len(texts_with_code),
        "unique_code_blocks": len(code_blocks_all),
        "duplicate_code_blocks": len(duplicate_code_blocks),
        "total_duplicate_occurrences": total_duplicate_occurrences,
        "top_duplicates": top_duplicates,
    }


def main():
    """Hlavná funkcia."""
    
    results = {}
    
    print("=" * 60)
    
    # Analyzujeme user prompty
    if (input_dir / "user_prompts_cleaned.jsonl").exists():
        results["user_prompts"] = analyze_file(
            input_dir / "user_prompts_cleaned.jsonl",
            "user prompty"
        )
    
    # Analyzujeme AI odpovede
    if (input_dir / "ai_responses_cleaned.jsonl").exists():
        results["ai_responses"] = analyze_file(
            input_dir / "ai_responses_cleaned.jsonl",
            "AI odpovede"
        )
    
    # Uložíme výsledky
    output_file = output_dir / "code_duplicates_analysis.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    # Vypíšeme súhrn
    print("\n" + "=" * 60)
    print("📊 SÚHRN ANALÝZY CODE BLOCKS DUPLIKÁTOV")
    print("=" * 60)
    
    for file_type, stats in results.items():
        if not stats:
            continue
        
        print(f"\n📄 {file_type}:")
        print(f"  Celkom textov: {stats.get('total_texts', 0)}")
        print(f"  Textov s code blocks: {stats.get('texts_with_code_blocks', 0)}")
        print(f"  Unikátnych code blocks: {stats.get('unique_code_blocks', 0)}")
        print(f"  Opakujúce sa code blocks: {stats.get('duplicate_code_blocks', 0)}")
        print(f"  Celkom výskytov duplikátov: {stats.get('total_duplicate_occurrences', 0)}")
        
        if stats.get('top_duplicates'):
            print(f"\n  🔝 Top duplikáty:")
            for i, dup in enumerate(stats['top_duplicates'][:5], 1):
                print(f"    {i}. {dup['occurrences']}x výskytov")
                print(f"       Dĺžka: ~{dup['avg_length']:.0f} znakov")
                print(f"       Sample: {dup['sample'][:100]}...")
    
    print(f"\n💾 Výsledky uložené: {output_file}")
    print("\n🎉 Rýchla analýza dokončená!")


if __name__ == "__main__":
    main()

