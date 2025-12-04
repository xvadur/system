#!/usr/bin/env python3
"""
Analýza čiastočných duplikátov v texte na vzorke (prvých 500 textov).
Hľadá podobné texty, ktoré sa môžu kopírovať medzi vláknami.
"""

import json
import hashlib
from pathlib import Path
from typing import Dict, List, Tuple
from difflib import SequenceMatcher
from collections import defaultdict

workspace_root = Path(__file__).parent.parent
input_dir = workspace_root / "xvadur" / "data" / "kortex_cleaned"
output_dir = workspace_root / "xvadur" / "data" / "kortex_analysis"

output_dir.mkdir(parents=True, exist_ok=True)

print("🔍 Analýza čiastočných duplikátov na vzorke\n")
print(f"📁 Input: {input_dir}")
print(f"📁 Output: {output_dir}\n")

# Konfigurácia
SAMPLE_SIZE = 500  # Počet textov na analýzu
SIMILARITY_THRESHOLD = 0.8  # 80% podobnosť = duplikát
MIN_TEXT_LENGTH = 200  # Minimálna dĺžka textu pre analýzu (znaky)


def similarity_ratio(text1: str, text2: str) -> float:
    """Vypočíta podobnosť medzi dvoma textami (0-1)."""
    # Normalizujeme texty
    norm1 = " ".join(text1.lower().split())
    norm2 = " ".join(text2.lower().split())
    
    if not norm1 or not norm2:
        return 0.0
    
    # Použijeme SequenceMatcher pre rýchlejšie porovnanie
    return SequenceMatcher(None, norm1, norm2).ratio()


def find_similar_texts(texts: List[Tuple[str, Dict]], threshold: float = 0.8) -> List[Dict]:
    """Nájde podobné texty (podobnosť >= threshold)."""
    similar_groups = []
    seen_indices = set()
    
    total = len(texts)
    print(f"  🔍 Porovnávam {total} textov...")
    
    for i, (text1, meta1) in enumerate(texts):
        if i in seen_indices:
            continue
        
        if (i + 1) % 50 == 0:
            print(f"    Progress: {i+1}/{total}")
        
        # Skontrolujeme dĺžku
        if len(text1) < MIN_TEXT_LENGTH:
            continue
        
        similar_items = []
        
        for j, (text2, meta2) in enumerate(texts[i+1:], start=i+1):
            if j in seen_indices:
                continue
            
            # Rýchla kontrola - ak sú texty príliš rôzne v dĺžke, preskočíme
            len_diff = abs(len(text1) - len(text2)) / max(len(text1), len(text2), 1)
            if len_diff > 0.4:  # Viac ako 40% rozdiel v dĺžke
                continue
            
            # Vypočítame podobnosť
            similarity = similarity_ratio(text1, text2)
            
            if similarity >= threshold:
                similar_items.append({
                    "index": j,
                    "similarity": similarity,
                    "meta": meta2,
                })
        
        if similar_items:
            # Vytvoríme skupinu podobných textov
            group = {
                "primary": meta1,
                "similar": similar_items,
                "similarity": max(item["similarity"] for item in similar_items),
                "count": len(similar_items) + 1,
            }
            similar_groups.append(group)
            
            # Označíme všetky podobné ako spracované
            seen_indices.add(i)
            seen_indices.update(item["index"] for item in similar_items)
    
    return similar_groups


def analyze_file(input_file: Path, file_type: str, sample_size: int = 500) -> Dict:
    """Analyzuje jeden súbor na vzorke."""
    print(f"\n📄 Analyzujem {file_type} (vzorka: prvých {sample_size})...")
    
    if not input_file.exists():
        print(f"  ⚠️  Súbor neexistuje: {input_file}")
        return {}
    
    texts_with_meta = []
    total_count = 0
    
    print(f"  📖 Načítavam súbor...")
    
    with open(input_file, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            if line_num > sample_size:
                break
            
            try:
                data = json.loads(line)
                text = data.get("extracted_text", "")
                total_count += 1
                
                if not text or len(text) < MIN_TEXT_LENGTH:
                    continue
                
                texts_with_meta.append((text, {
                    "line_num": line_num,
                    "uuid": data.get("uuid"),
                    "date_created": data.get("date_created"),
                    "text_length": len(text),
                    "word_count": data.get("word_count", len(text.split())),
                }))
            except Exception:
                continue
    
    print(f"  ✅ Načítaných {len(texts_with_meta)} textov (z {total_count} celkom)")
    
    # Hľadáme podobné texty
    print(f"  🔍 Hľadám podobné texty (threshold: {SIMILARITY_THRESHOLD})...")
    similar_groups = find_similar_texts(texts_with_meta, threshold=SIMILARITY_THRESHOLD)
    
    print(f"  ✅ Nájdených {len(similar_groups)} skupín podobných textov")
    
    # Zoradíme podľa počtu výskytov a podobnosti
    similar_groups_sorted = sorted(
        similar_groups,
        key=lambda x: (x["count"], x["similarity"]),
        reverse=True
    )
    
    # Príprava detailov
    total_similar_texts = sum(group["count"] for group in similar_groups)
    
    return {
        "total_analyzed": len(texts_with_meta),
        "similarity_groups": len(similar_groups),
        "total_similar_texts": total_similar_texts,
        "top_groups": similar_groups_sorted[:20],  # Top 20 skupín
    }


def main():
    """Hlavná funkcia."""
    
    results = {}
    
    print("=" * 60)
    
    # Analyzujeme user prompty
    if (input_dir / "user_prompts_cleaned.jsonl").exists():
        results["user_prompts"] = analyze_file(
            input_dir / "user_prompts_cleaned.jsonl",
            "user prompty",
            sample_size=SAMPLE_SIZE
        )
    
    # Analyzujeme AI odpovede
    if (input_dir / "ai_responses_cleaned.jsonl").exists():
        results["ai_responses"] = analyze_file(
            input_dir / "ai_responses_cleaned.jsonl",
            "AI odpovede",
            sample_size=SAMPLE_SIZE
        )
    
    # Uložíme výsledky
    output_file = output_dir / "text_similarity_analysis.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    # Vypíšeme súhrn
    print("\n" + "=" * 60)
    print("📊 SÚHRN ANALÝZY PODOBNOSTI TEXTU")
    print("=" * 60)
    
    for file_type, stats in results.items():
        if not stats:
            continue
        
        print(f"\n📄 {file_type}:")
        print(f"  Analyzovaných textov: {stats.get('total_analyzed', 0)}")
        print(f"  Skupín podobných textov: {stats.get('similarity_groups', 0)}")
        print(f"  Celkom podobných textov: {stats.get('total_similar_texts', 0)}")
        
        top_groups = stats.get('top_groups', [])
        if top_groups:
            print(f"\n  🔝 Top podobné texty:")
            for i, group in enumerate(top_groups[:5], 1):
                primary = group["primary"]
                print(f"    {i}. Skupina s {group['count']} podobnými textmi (similarity: {group['similarity']:.2%})")
                print(f"       Primary: line {primary['line_num']}, {primary['word_count']} slov, {primary.get('date_created', 'N/A')[:10]}")
                print(f"       Text sample: {primary.get('text_sample', 'N/A')[:100]}...")
                for sim in group['similar'][:2]:  # Prvých 2 podobných
                    print(f"       - Similar: line {sim['meta']['line_num']}, similarity {sim['similarity']:.2%}")
    
    print(f"\n💾 Výsledky uložené: {output_file}")
    print("\n🎉 Analýza dokončená!")


if __name__ == "__main__":
    main()

