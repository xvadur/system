#!/usr/bin/env python3
"""
Pokročilá analýza duplikátov v extrahovaných dátach.
- Detekcia veľkých kúskov kódu
- Čiastočné duplikáty (similarity)
- Opakujúce sa bloky textu
"""

import json
import re
import hashlib
from pathlib import Path
from typing import Dict, List, Set, Tuple
from difflib import SequenceMatcher
from collections import defaultdict

workspace_root = Path(__file__).parent.parent
input_dir = workspace_root / "xvadur" / "data" / "kortex_cleaned"
output_dir = workspace_root / "xvadur" / "data" / "kortex_analysis"

output_dir.mkdir(parents=True, exist_ok=True)

print("🔍 Pokročilá analýza duplikátov\n")
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
        if clean_match.strip():
            code_blocks.append(clean_match.strip())
    
    return code_blocks


def extract_code_snippets(text: str) -> List[str]:
    """Extrahuje kódové snippet-y (def, class, import, atď.)."""
    snippets = []
    
    # Python patterns
    python_patterns = [
        (r'def\s+\w+[^`]*?(?=\n\s*(?:def|class|$)|\Z)', 'python'),
        (r'class\s+\w+[^`]*?(?=\n\s*(?:def|class|$)|\Z)', 'python'),
        (r'import\s+[^\n]+', 'python'),
        (r'from\s+\w+\s+import[^\n]+', 'python'),
    ]
    
    for pattern, lang in python_patterns:
        matches = re.findall(pattern, text, re.MULTILINE)
        snippets.extend([(m, lang) for m in matches if m.strip()])
    
    # JavaScript/TypeScript patterns
    js_patterns = [
        (r'function\s+\w+[^`]*?(?=\n\s*(?:function|class|$)|\Z)', 'js'),
        (r'const\s+\w+\s*=[^;]+;', 'js'),
        (r'let\s+\w+\s*=[^;]+;', 'js'),
    ]
    
    for pattern, lang in js_patterns:
        matches = re.findall(pattern, text, re.MULTILINE)
        snippets.extend([(m, lang) for m in matches if m.strip()])
    
    return snippets


def similarity_ratio(text1: str, text2: str) -> float:
    """Vypočíta podobnosť medzi dvoma textami (0-1)."""
    # Normalizujeme texty
    norm1 = " ".join(text1.lower().split())
    norm2 = " ".join(text2.lower().split())
    
    if not norm1 or not norm2:
        return 0.0
    
    return SequenceMatcher(None, norm1, norm2).ratio()


def find_partial_duplicates(texts: List[Tuple[str, Dict]], threshold: float = 0.8, max_compare: int = 5000) -> List[Dict]:
    """Nájde čiastočné duplikáty (podobnosť > threshold)."""
    duplicates = []
    seen = set()
    
    total = len(texts)
    print(f"  🔍 Hľadám čiastočné duplikáty (threshold: {threshold})...")
    print(f"  📊 Porovnávam {min(total, max_compare)} textov...")
    
    # Limit počtu porovnaní pre rýchlosť
    texts_to_compare = texts[:max_compare]
    
    for i, (text1, meta1) in enumerate(texts_to_compare):
        if i in seen:
            continue
        
        if (i + 1) % 100 == 0:
            print(f"    Progress: {i+1}/{len(texts_to_compare)}")
        
        similar = []
        for j, (text2, meta2) in enumerate(texts_to_compare[i+1:], start=i+1):
            if j in seen:
                continue
            
            # Rýchla kontrola - ak sú texty príliš rôzne v dĺžke, preskočíme
            len_diff = abs(len(text1) - len(text2)) / max(len(text1), len(text2), 1)
            if len_diff > 0.5:  # Viac ako 50% rozdiel v dĺžke
                continue
            
            similarity = similarity_ratio(text1, text2)
            if similarity >= threshold:
                similar.append((j, similarity, meta2))
        
        if similar:
            # Označíme všetky podobné ako duplikáty
            group = [meta1] + [meta2 for _, _, meta2 in similar]
            duplicates.append({
                "group": group,
                "similarity": max(s[1] for s in similar),
                "count": len(group),
            })
            seen.add(i)
            seen.update(j for j, _, _ in similar)
    
    return duplicates


def analyze_file(input_file: Path, file_type: str) -> Dict:
    """Analyzuje jeden súbor."""
    print(f"\n📄 Analyzujem {file_type}...")
    
    if not input_file.exists():
        print(f"  ⚠️  Súbor neexistuje: {input_file}")
        return {}
    
    texts_with_meta = []
    code_blocks_all = defaultdict(list)  # hash -> list of (text_sample, meta)
    code_snippets_all = defaultdict(list)
    
    print(f"  📖 Načítavam súbor...")
    
    with open(input_file, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            try:
                data = json.loads(line)
                text = data.get("extracted_text", "")
                
                if not text:
                    continue
                
                # Extrahujeme code blocks
                code_blocks = extract_code_blocks(text)
                for block in code_blocks:
                    # Hash code blocku pre detekciu duplikátov (prvých 500 znakov)
                    block_sample = block[:500].strip()
                    if len(block_sample) > 50:  # Minimálna dĺžka
                        block_hash = hashlib.md5(block_sample.encode()).hexdigest()
                        code_blocks_all[block_hash].append({
                            "sample": block_sample,
                            "full_length": len(block),
                            "line_num": line_num,
                            "uuid": data.get("uuid"),
                        })
                
                # Extrahujeme code snippets
                code_snippets = extract_code_snippets(text)
                for snippet, lang in code_snippets:
                    snippet_sample = snippet[:200].strip()
                    if len(snippet_sample) > 20:  # Minimálna dĺžka
                        snippet_hash = hashlib.md5(snippet_sample.encode()).hexdigest()
                        code_snippets_all[snippet_hash].append({
                            "sample": snippet_sample,
                            "lang": lang,
                            "line_num": line_num,
                            "uuid": data.get("uuid"),
                        })
                
                # Uložíme text s metadátami
                texts_with_meta.append((text, {
                    "line_num": line_num,
                    "uuid": data.get("uuid"),
                    "date_created": data.get("date_created"),
                    "text_length": len(text),
                    "word_count": data.get("word_count", len(text.split())),
                }))
            except Exception as e:
                print(f"  ⚠️  Chyba na riadku {line_num}: {e}")
                continue
    
    print(f"  ✅ Načítaných {len(texts_with_meta)} textov")
    
    # Detekcia opakujúcich sa code blocks
    duplicate_code_blocks = {
        h: items for h, items in code_blocks_all.items() 
        if len(items) > 1
    }
    duplicate_code_snippets = {
        h: items for h, items in code_snippets_all.items() 
        if len(items) > 1
    }
    
    print(f"  📦 Opakujúce sa code blocks: {len(duplicate_code_blocks)}")
    print(f"  📦 Opakujúce sa code snippets: {len(duplicate_code_snippets)}")
    
    # Čiastočné duplikáty
    print(f"  🔍 Hľadám čiastočné duplikáty...")
    partial_duplicates = find_partial_duplicates(texts_with_meta, threshold=0.8, max_compare=2000)
    
    print(f"  ✅ Nájdených {len(partial_duplicates)} skupín čiastočných duplikátov")
    
    # Štatistiky
    total_duplicate_items = sum(d["count"] for d in partial_duplicates)
    
    # Príprava detailov pre výstup (len prvé príklady)
    code_blocks_examples = {}
    for block_hash, items in list(duplicate_code_blocks.items())[:10]:
        code_blocks_examples[block_hash] = {
            "count": len(items),
            "sample": items[0]["sample"][:200],
            "occurrences": len(items),
        }
    
    return {
        "total_texts": len(texts_with_meta),
        "duplicate_code_blocks": len(duplicate_code_blocks),
        "duplicate_code_snippets": len(duplicate_code_snippets),
        "partial_duplicate_groups": len(partial_duplicates),
        "total_partial_duplicates": total_duplicate_items,
        "code_blocks_examples": code_blocks_examples,
        "partial_duplicates_detail": partial_duplicates[:20],  # Prvých 20 pre detail
    }


def main():
    """Hlavná funkcia."""
    
    results = {}
    
    # Analyzujeme každý súbor
    print("=" * 60)
    
    if (input_dir / "user_prompts_cleaned.jsonl").exists():
        results["user_prompts"] = analyze_file(
            input_dir / "user_prompts_cleaned.jsonl",
            "user prompty"
        )
    else:
        print("  ⚠️  user_prompts_cleaned.jsonl neexistuje")
    
    if (input_dir / "ai_responses_cleaned.jsonl").exists():
        results["ai_responses"] = analyze_file(
            input_dir / "ai_responses_cleaned.jsonl",
            "AI odpovede"
        )
    else:
        print("  ⚠️  ai_responses_cleaned.jsonl neexistuje")
    
    # Uložíme výsledky
    output_file = output_dir / "duplicate_analysis.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    # Vypíšeme súhrn
    print("\n" + "=" * 60)
    print("📊 SÚHRN ANALÝZY DUPLIKÁTOV")
    print("=" * 60)
    
    for file_type, stats in results.items():
        if not stats:
            continue
        
        print(f"\n📄 {file_type}:")
        print(f"  Celkom textov: {stats.get('total_texts', 0)}")
        print(f"  Opakujúce sa code blocks: {stats.get('duplicate_code_blocks', 0)}")
        print(f"  Opakujúce sa code snippets: {stats.get('duplicate_code_snippets', 0)}")
        print(f"  Skupiny čiastočných duplikátov: {stats.get('partial_duplicate_groups', 0)}")
        print(f"  Celkom čiastočných duplikátov: {stats.get('total_partial_duplicates', 0)}")
    
    print(f"\n💾 Výsledky uložené: {output_file}")
    print("\n🎉 Analýza dokončená!")


if __name__ == "__main__":
    main()

