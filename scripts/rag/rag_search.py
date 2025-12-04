#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RAG Search: Vyhľadávanie v RAG indexe pomocou semantic search.
"""

import json
import sys
from pathlib import Path
from typing import List, Dict, Optional

try:
    import faiss
    import numpy as np
    from openai import OpenAI
except ImportError:
    print("❌ Chyba: Potrebuješ nainštalovať faiss-cpu, numpy a openai")
    print("   pip install faiss-cpu numpy openai")
    sys.exit(1)

import os

# Konfigurácia
INDEX_DIR = Path("data/rag_index")
EMBEDDING_MODEL = "text-embedding-3-small"
EMBEDDING_DIM = 1536
DEFAULT_TOP_K = 5

# Načítanie API key z .env súboru alebo environmentu
def load_api_key():
    """Načíta OpenAI API key z .env súboru alebo environmentu."""
    # Skús najprv environment
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        return api_key
    
    # Ak nie je v environmente, skús načítať z .env súboru
    env_files = [
        Path(".env"),
        Path("mcp/.env")
    ]
    
    for env_file in env_files:
        if env_file.exists():
            try:
                with open(env_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        if line.startswith("OPENAI_API_KEY="):
                            # Odstráni "OPENAI_API_KEY=" a quotes ak existujú
                            key = line.split("=", 1)[1].strip()
                            key = key.strip('"').strip("'")
                            if key and key != "changeme":
                                return key
            except Exception as e:
                continue
    
    return None

API_KEY = load_api_key()
if not API_KEY:
    print("⚠️  OPENAI_API_KEY nie je nastavený")
    print("   Nastav ho v environmente alebo v .env súbore")
    sys.exit(1)


def load_index(index_dir: Path) -> tuple:
    """
    Načíta FAISS index a metadata.
    
    Returns:
        (index, metadata, chunks, tfidf_index) tuple
    """
    index_path = index_dir / "faiss.index"
    metadata_path = index_dir / "metadata.json"
    chunks_path = index_dir / "chunks.json"
    
    if not index_path.exists():
        print(f"❌ Index neexistuje: {index_path}")
        print(f"   Spusti najprv build_rag_index.py")
        sys.exit(1)
    
    # Načítanie indexu
    index = faiss.read_index(str(index_path))
    
    # Načítanie metadát
    with open(metadata_path, 'r', encoding='utf-8') as f:
        metadata = json.load(f)
    
    # Načítanie chunkov
    with open(chunks_path, 'r', encoding='utf-8') as f:
        chunks = json.load(f)
    
    # Vytvorenie TF-IDF indexu pre keyword search
    from rag_agent_helper import build_tfidf_index
    tfidf_index = build_tfidf_index(chunks)
    
    return index, metadata, chunks, tfidf_index


def search(
    query: str,
    index,
    metadata: List[Dict],
    chunks: List[str],
    client: OpenAI,
    top_k: int = DEFAULT_TOP_K
) -> List[Dict]:
    """
    Vyhľadáva v RAG indexe.
    
    Args:
        query: Vyhľadávací dotaz
        index: FAISS index
        metadata: Metadata pre chunkov
        chunks: Text chunkov
        client: OpenAI client
        top_k: Počet výsledkov
    
    Returns:
        List of search results with metadata
    """
    # Generovanie embeddingu pre query
    response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=[query]
    )
    query_embedding = np.array([response.data[0].embedding], dtype=np.float32)
    
    # Vyhľadávanie v indexe
    distances, indices = index.search(query_embedding, top_k)
    
    # Zostavenie výsledkov
    results = []
    for i, (distance, idx) in enumerate(zip(distances[0], indices[0])):
        if idx < len(chunks) and idx < len(metadata):
            results.append({
                "rank": i + 1,
                "score": float(1 / (1 + distance)),  # Konverzia distance na similarity score
                "distance": float(distance),
                "text": chunks[idx],
                "metadata": metadata[idx]
            })
    
    return results


def format_result(result: Dict) -> str:
    """Formátuje výsledok pre výpis"""
    text = result.get("text", "")
    date = result.get("date", "N/A")
    source_path = result.get("source_path", "N/A")
    chunk_index = result.get("chunk_index", 0)
    total_chunks = result.get("total_chunks", 1)
    search_type = result.get("search_type", "semantic")
    content_type = result.get("content_type", "prompt")
    
    # Skrátenie textu ak je príliš dlhý
    if len(text) > 500:
        text = text[:500] + "..."
    
    # Hybrid search info
    score_info = f"Score: {result['score']:.4f}"
    if search_type == "hybrid":
        semantic_score = result.get("semantic_score", 0)
        keyword_score = result.get("keyword_score", 0)
        score_info += f" (Semantic: {semantic_score:.4f}, Keyword: {keyword_score:.4f})"
    
    output = f"""
{'='*60}
Rank #{result['rank']} - {search_type.upper()} - {score_info}
Type: {content_type.upper()}
{'='*60}
Dátum: {date}
Zdroj: {source_path}
Chunk: {chunk_index + 1}/{total_chunks}
{'='*60}

{text}

"""
    return output


def main():
    """Hlavná funkcia"""
    if len(sys.argv) < 2:
        print("Použitie: python rag_search.py 'tvoj dotaz' [top_k] [use_hybrid] [content_type]")
        print("Príklad: python rag_search.py 'ako som riešil n8n problémy' 5 true")
        print("Príklad: python rag_search.py 'transformácia identity' 10 true pair")
        print("Content types: prompt, response, pair, alebo None (všetko)")
        sys.exit(1)
    
    query = sys.argv[1]
    top_k = int(sys.argv[2]) if len(sys.argv) > 2 else DEFAULT_TOP_K
    use_hybrid = sys.argv[3].lower() == "true" if len(sys.argv) > 3 else True
    content_type_filter = sys.argv[4] if len(sys.argv) > 4 else None
    
    if content_type_filter and content_type_filter.lower() == "none":
        content_type_filter = None
    
    print("="*60)
    print("🔍 RAG SEARCH - HYBRID MODE" if use_hybrid else "🔍 RAG SEARCH - SEMANTIC MODE")
    print("="*60)
    print(f"Dotaz: {query}")
    print(f"Top K: {top_k}")
    print(f"Mode: {'Hybrid (Semantic + Keyword)' if use_hybrid else 'Semantic only'}")
    if content_type_filter:
        print(f"Content Type Filter: {content_type_filter}")
    print("="*60)
    print()
    
    # Načítanie indexu
    print("📖 Načítavam index...")
    index, metadata, chunks, tfidf_index = load_index(INDEX_DIR)
    print(f"✅ Index načítaný ({index.ntotal} vektorov)\n")
    
    # Vyhľadávanie (použijeme hybrid search z rag_agent_helper)
    from rag_agent_helper import search_rag
    print(f"🔍 {'Hybrid search (semantic + keyword)' if use_hybrid else 'Semantic search'}...\n")
    
    results = search_rag(
        query, 
        top_k=top_k, 
        min_score=0.3, 
        use_hybrid=use_hybrid,
        content_type_filter=content_type_filter
    )
    
    # Výpis výsledkov
    if not results:
        print("❌ Nenašli sa žiadne výsledky")
        return
    
    print(f"✅ Nájdených {len(results)} výsledkov:\n")
    
    for result in results:
        print(format_result(result))


if __name__ == "__main__":
    main()

