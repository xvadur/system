#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Vytvorí markdown súbor z RAG výsledkov.
"""

import json
import sys
from pathlib import Path
from typing import List, Dict

# Import RAG query funkcie
sys.path.insert(0, str(Path(__file__).parent))
from query_rag_context import query_rag_with_context


def create_markdown_from_query(
    query: str,
    output_path: Path,
    week: str = None,
    top_k: int = 50,
    min_score: float = 0.3,
    title: str = None,
    user_only: bool = True  # Nový parameter: len user texty
) -> None:
    """
    Vykoná RAG query a vytvorí markdown súbor s výsledkami.
    """
    print(f"🔍 Vyhľadávam: '{query}'")
    if week:
        print(f"📅 Týždeň: {week}")
    
    # Vykonaj query
    results = query_rag_with_context(
        query=query,
        top_k=top_k,
        week=week,
        min_score=min_score
    )
    
    if "error" in results:
        print(f"❌ Chyba: {results['error']}")
        return
    
    # Odstráň duplikáty (podľa textu)
    seen = set()
    unique_results = []
    for r in results.get("results", []):
        text_key = r.get("text", "").strip()[:100]
        if text_key not in seen:
            seen.add(text_key)
            unique_results.append(r)
    
    # Zoraď podľa skóre
    unique_results.sort(key=lambda x: x.get("score", 0), reverse=True)
    
    print(f"✅ Nájdených {len(unique_results)} unikátnych výsledkov")
    
    # Vytvor markdown
    md_lines = []
    
    # Hlavička
    md_lines.append(f"# {title or query}\n")
    md_lines.append(f"**Query:** `{query}`\n")
    if week:
        md_lines.append(f"**Týždeň:** {week}\n")
    md_lines.append(f"**Počet výsledkov:** {len(unique_results)}\n")
    md_lines.append("---\n\n")
    
    # Výsledky
    for idx, result in enumerate(unique_results, 1):
        text = result.get("text", "").strip()
        context_before = result.get("context_before", "").strip()
        context_after = result.get("context_after", "").strip()
        score = result.get("score", 0)
        date = result.get("date", "N/A")
        timestamp = result.get("timestamp", "N/A")
        
        md_lines.append(f"## Výsledok #{idx}\n")
        md_lines.append(f"**Skóre relevance:** {score:.3f}  \n")
        md_lines.append(f"**Dátum:** {date}  \n")
        md_lines.append(f"**Timestamp:** {timestamp}\n\n")
        
        # Kontext pred
        if context_before:
            md_lines.append("**Kontext pred:**\n")
            md_lines.append(f"{context_before}\n\n")
        
        # Hlavný text
        md_lines.append("**Relevantný text:**\n")
        md_lines.append(f"{text}\n\n")
        
        # Kontext po
        if context_after:
            md_lines.append("**Kontext po:**\n")
            md_lines.append(f"{context_after}\n\n")
        
        md_lines.append("---\n\n")
    
    # Ulož súbor
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(''.join(md_lines))
    
    print(f"✅ Markdown uložený: {output_path}")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Vytvor markdown z RAG výsledkov")
    parser.add_argument("query", type=str, help="Query pre RAG vyhľadávanie")
    parser.add_argument("--output", type=str, required=True, help="Cesta k výstupnému markdown súboru")
    parser.add_argument("--week", type=str, default=None, help="Týždeň (napr. 2025-W29)")
    parser.add_argument("--top-k", type=int, default=50, help="Počet výsledkov")
    parser.add_argument("--min-score", type=float, default=0.3, help="Minimálne skóre")
    parser.add_argument("--title", type=str, default=None, help="Nadpis markdown súboru")
    parser.add_argument("--user-only", action="store_true", default=True, help="Len user texty (nie AI odpovede)")
    
    args = parser.parse_args()
    
    create_markdown_from_query(
        query=args.query,
        output_path=Path(args.output),
        week=args.week,
        top_k=args.top_k,
        min_score=args.min_score,
        title=args.title,
        user_only=args.user_only
    )
