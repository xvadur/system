#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RAG Agent Helper: Wrapper pre Cursor agenta na automatické vyhľadávanie v RAG indexe.

Tento skript môže byť volaný z Cursor agenta cez terminal command.
Vracia JSON výsledky, ktoré môže agent použiť v odpovedi.
"""

import json
import sys
import re
from pathlib import Path
from typing import List, Dict, Optional
from collections import Counter

try:
    import faiss
    import numpy as np
    from openai import OpenAI
except ImportError:
    print(json.dumps({"error": "Missing dependencies: faiss-cpu, numpy, openai"}))
    sys.exit(1)

import os

# Konfigurácia
INDEX_DIR = Path("data/rag_index")
EMBEDDING_MODEL = "qwen/qwen3-embedding-8b"  # Qwen3 Embedding 8B cez OpenRouter
EMBEDDING_DIM = 4096  # qwen3-embedding-8b má 4096 dimenzií (cez OpenRouter)
# Poznámka: Starý index môže mať 1536 dimenzií (OpenAI text-embedding-3-small)
# Skript automaticky detekuje dimenzie indexu
USE_OPENROUTER = True  # Použiť OpenRouter API namiesto OpenAI
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"  # OpenRouter API endpoint

# Načítanie API key z .env súboru alebo environmentu
def load_api_key():
    """Načíta OpenRouter API key z .env súboru alebo environmentu."""
    # Priorita: OpenRouter keys
    api_key = os.getenv("OPENROUTER_API_KEY") or os.getenv("OPEROUTER_API_KEY") or os.getenv("OPEN_ROUTER")
    if api_key:
        return api_key
    
    env_files = [
        Path(".env"),
        Path("mcp/.env")
    ]
    
    for env_file in env_files:
        if env_file.exists():
            try:
                # Najprv prečítaj celý súbor a hľadaj OpenRouter key
                with open(env_file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                
                # Hľadaj len OpenRouter keys
                for line in lines:
                    line = line.strip()
                    if (line.startswith("OPENROUTER_API_KEY=") or 
                        line.startswith("OPEROUTER_API_KEY=") or 
                        line.startswith("OPEN_ROUTER=")):
                        key = line.split("=", 1)[1].strip()
                        key = key.strip('"').strip("'")
                        if key and key != "changeme":
                            return key
            except Exception:
                continue
    
    return None


def load_index(index_dir: Path) -> tuple:
    """Načíta FAISS index a metadata."""
    index_path = index_dir / "faiss.index"
    metadata_path = index_dir / "metadata.json"
    chunks_path = index_dir / "chunks.json"
    
    if not index_path.exists():
        return None, None, None, None
    
    index = faiss.read_index(str(index_path))
    
    # Detekcia dimenzií indexu (uložíme do globálnej premennej pre použitie v search_rag)
    actual_dim = index.d
    global EMBEDDING_DIM
    if actual_dim != EMBEDDING_DIM:
        # Index má iné dimenzie - upravíme globálnu premennú
        EMBEDDING_DIM = actual_dim
    
    with open(metadata_path, 'r', encoding='utf-8') as f:
        metadata = json.load(f)
    
    with open(chunks_path, 'r', encoding='utf-8') as f:
        chunks = json.load(f)
    
    # Vytvorenie TF-IDF indexu pre keyword search
    tfidf_index = build_tfidf_index(chunks)
    
    return index, metadata, chunks, tfidf_index


def tokenize(text: str) -> List[str]:
    """Tokenizuje text na slová (slovenčina + angličtina)."""
    # Odstránenie diakritiky a lowercase
    text = text.lower()
    # Extrahovanie slov (písmená, čísla, podčiarkovníky)
    words = re.findall(r'\b\w+\b', text)
    return words


def build_tfidf_index(chunks: List[str]) -> Dict:
    """
    Vytvorí jednoduchý TF-IDF index pre keyword search.
    
    Returns:
        Dict s term frequencies a document frequencies
    """
    # Počet dokumentov
    num_docs = len(chunks)
    
    # Term frequency pre každý dokument
    doc_term_freqs = []
    # Document frequency pre každý term
    doc_freq = Counter()
    
    for chunk in chunks:
        tokens = tokenize(chunk)
        term_freq = Counter(tokens)
        doc_term_freqs.append(term_freq)
        
        # Počítanie document frequency (v koľkých dokumentoch sa term vyskytuje)
        unique_terms = set(tokens)
        for term in unique_terms:
            doc_freq[term] += 1
    
    return {
        "doc_term_freqs": doc_term_freqs,
        "doc_freq": doc_freq,
        "num_docs": num_docs
    }


def keyword_search(
    query: str,
    chunks: List[str],
    tfidf_index: Dict,
    top_k: int = 10
) -> List[Dict]:
    """
    Keyword search pomocou TF-IDF.
    
    Args:
        query: Vyhľadávací dotaz
        chunks: Text chunkov
        tfidf_index: TF-IDF index
        top_k: Počet výsledkov
    
    Returns:
        List of search results with TF-IDF scores
    """
    query_tokens = tokenize(query)
    if not query_tokens:
        return []
    
    doc_term_freqs = tfidf_index["doc_term_freqs"]
    doc_freq = tfidf_index["doc_freq"]
    num_docs = tfidf_index["num_docs"]
    
    scores = []
    
    for idx, chunk in enumerate(chunks):
        if idx >= len(doc_term_freqs):
            continue
        
        term_freq = doc_term_freqs[idx]
        score = 0.0
        
        # TF-IDF výpočet pre každý query token
        for token in query_tokens:
            # Term Frequency (TF)
            tf = term_freq.get(token, 0)
            if tf == 0:
                continue
            
            # Inverse Document Frequency (IDF)
            df = doc_freq.get(token, 0)
            if df == 0:
                continue
            
            idf = np.log(num_docs / (1 + df))
            
            # TF-IDF score
            score += tf * idf
        
        if score > 0:
            scores.append({
                "idx": idx,
                "score": score,
                "text": chunk
            })
    
    # Zoradenie podľa score
    scores.sort(key=lambda x: x["score"], reverse=True)
    
    # Vrátenie top-k výsledkov
    return scores[:top_k]


def search_rag(
    query: str,
    top_k: int = 5,
    min_score: float = 0.4,
    use_hybrid: bool = True,
    semantic_weight: float = 0.7,
    keyword_weight: float = 0.3,
    content_type_filter: Optional[str] = None,
    index_dir: Optional[Path] = None
) -> List[Dict]:
    """
    Hybrid search v RAG indexe - kombinuje semantic (embeddings) a keyword (TF-IDF) search.
    
    Args:
        query: Vyhľadávací dotaz
        top_k: Počet výsledkov
        min_score: Minimálne similarity score (0-1)
        use_hybrid: Použiť hybrid search (True) alebo len semantic (False)
        semantic_weight: Váha semantic search (0-1)
        keyword_weight: Váha keyword search (0-1)
        content_type_filter: Filter podľa content_type ("prompt", "response", "pair", alebo None pre všetko)
    
    Returns:
        List of search results with metadata
    """
    # Načítanie API key (OpenRouter)
    api_key = load_api_key()
    if not api_key:
        return [{"error": "OPENROUTER_API_KEY nie je nastavený. Nastav OPENROUTER_API_KEY v .env alebo environmente."}]
    
    # Načítanie indexu (použi poskytnutý index_dir alebo default)
    index_path = index_dir if index_dir else INDEX_DIR
    index, metadata, chunks, tfidf_index = load_index(index_path)
    if index is None:
        return [{"error": f"RAG index neexistuje v {index_path}. Spusti najprv build_rag_index.py"}]
    
    actual_dim = index.d
    
    # Vždy používame OpenRouter s qwen modelom
    embedding_model = EMBEDDING_MODEL
    use_openrouter_for_emb = USE_OPENROUTER
    
    # Ak index má iné dimenzie, treba ho rebuildnúť
    # Ak index má iné dimenzie, treba ho rebuildnúť
    if actual_dim != EMBEDDING_DIM:
        return [{"error": f"Nezhoda dimenzií: index má {actual_dim}, qwen/qwen3-embedding-8b má {EMBEDDING_DIM}. Treba rebuildnúť index:\n  python3 archive/rag/rag/build_rag_index.py"}]
    
    # SEMANTIC SEARCH (embeddings) - VŽDY používame OpenRouter
    # OpenAI SDK je kompatibilné s OpenRouter API
    client = OpenAI(
        api_key=api_key, 
        base_url=OPENROUTER_BASE_URL,
        default_headers={
            "HTTP-Referer": "https://github.com/xvadur/system",
            "X-Title": "RAG Agent Helper"
        }
    )
    try:
        response = client.embeddings.create(
            model=embedding_model,
            input=[query]
        )
        query_embedding = np.array([response.data[0].embedding], dtype=np.float32)
        
        # Kontrola dimenzií
        if query_embedding.shape[1] != actual_dim:
            return [{"error": f"Nezhoda dimenzií: embedding má {query_embedding.shape[1]}, index má {actual_dim}"}]
    except Exception as e:
        return [{"error": f"Chyba pri generovaní embeddingu: {str(e)}"}]
    
    # Semantic search - vezmeme viac výsledkov pre hybrid kombináciu
    search_k = top_k * 3 if use_hybrid else top_k
    distances, semantic_indices = index.search(query_embedding, search_k)
    
    semantic_results = {}
    for distance, idx in zip(distances[0], semantic_indices[0]):
        if idx < len(chunks) and idx < len(metadata):
            score = float(1 / (1 + distance))
            semantic_results[idx] = {
                "score": score,
                "distance": float(distance)
            }
    
    # KEYWORD SEARCH (TF-IDF)
    keyword_results = {}
    if use_hybrid and tfidf_index:
        keyword_matches = keyword_search(query, chunks, tfidf_index, top_k=search_k)
        
        # Normalizácia TF-IDF skóre (0-1)
        if keyword_matches:
            max_tfidf = max(m["score"] for m in keyword_matches)
            if max_tfidf > 0:
                for match in keyword_matches:
                    idx = match["idx"]
                    normalized_score = match["score"] / max_tfidf
                    keyword_results[idx] = {
                        "score": normalized_score,
                        "tfidf": match["score"]
                    }
    
    # HYBRID KOMBINÁCIA
    if use_hybrid and keyword_results:
        # Kombinácia semantic + keyword výsledkov
        all_indices = set(semantic_results.keys()) | set(keyword_results.keys())
        hybrid_scores = {}
        
        for idx in all_indices:
            semantic_score = semantic_results.get(idx, {}).get("score", 0.0)
            keyword_score = keyword_results.get(idx, {}).get("score", 0.0)
            
            # Vážený priemer
            hybrid_score = (semantic_score * semantic_weight) + (keyword_score * keyword_weight)
            hybrid_scores[idx] = {
                "hybrid_score": hybrid_score,
                "semantic_score": semantic_score,
                "keyword_score": keyword_score
            }
        
        # Zoradenie podľa hybrid score
        sorted_indices = sorted(
            hybrid_scores.items(),
            key=lambda x: x[1]["hybrid_score"],
            reverse=True
        )
    else:
        # Len semantic search
        sorted_indices = sorted(
            semantic_results.items(),
            key=lambda x: x[1]["score"],
            reverse=True
        )
        # Prekonvertovanie na rovnaký formát
        sorted_indices = [
            (idx, {
                "hybrid_score": data["score"],
                "semantic_score": data["score"],
                "keyword_score": 0.0
            })
            for idx, data in sorted_indices
        ]
    
    # Zostavenie výsledkov
    results = []
    for rank, (idx, scores) in enumerate(sorted_indices[:top_k], 1):
        if idx >= len(chunks) or idx >= len(metadata):
            continue
        
        hybrid_score = scores["hybrid_score"]
        
        # Filtrovanie podľa minimálneho score
        if hybrid_score < min_score:
            continue
        
        meta = metadata[idx]
        
        # Filtrovanie podľa content_type
        content_type = meta.get("content_type", "prompt")
        if content_type_filter and content_type != content_type_filter:
            continue
        
        results.append({
            "rank": rank,
            "score": hybrid_score,
            "semantic_score": scores["semantic_score"],
            "keyword_score": scores["keyword_score"],
            "text": chunks[idx],
            "date": meta.get("date", "N/A"),
            "timestamp": meta.get("timestamp", "N/A"),
            "source_path": meta.get("source_path", "N/A"),
            "chunk_index": meta.get("chunk_index", 0),
            "total_chunks": meta.get("total_chunks", 1),
            "content_type": content_type,
            "search_type": "hybrid" if use_hybrid and keyword_results else "semantic"
        })
    
    return results


def query_rag_with_synthesis(
    query: str,
    top_k: int = 10,
    min_score: float = 0.4,
    use_hybrid: bool = True,
    model: str = "deepseek/deepseek-v3.2",
    temperature: float = 0.3
) -> Dict:
    """
    RAG Query s automatickou syntézou odpovede.
    
    Namiesto surových promptov vráti syntetizovanú odpoveď, ktorá obsahuje
    hlavné informácie z relevantných promptov.
    
    Args:
        query: Vyhľadávací dotaz
        top_k: Počet výsledkov pre syntézu
        min_score: Minimálne similarity score
        use_hybrid: Použiť hybrid search
        model: LLM model pre syntézu cez OpenRouter (napr. deepseek/deepseek-v3.2)
        temperature: Temperature pre LLM
    
    Returns:
        Dict s syntetizovanou odpoveďou a metadátami
    """
    # 1. RAG Search - nájde relevantné prompty
    rag_results = search_rag(query, top_k=top_k, min_score=min_score, use_hybrid=use_hybrid)
    
    if not rag_results or "error" in rag_results[0]:
        return {
            "query": query,
            "synthesized_answer": "Nenašli sa relevantné výsledky v RAG indexe.",
            "sources_count": 0,
            "sources": []
        }
    
    # 2. Zostavenie kontextu z výsledkov
    context_parts = []
    sources = []
    
    for result in rag_results[:top_k]:
        date = result.get("date", "N/A")
        text = result.get("text", "")
        score = result.get("score", 0.0)
        source_path = result.get("source_path", "N/A")
        
        context_parts.append(f"[Dátum: {date}, Relevance: {score:.2f}]\n{text}")
        sources.append({
            "date": date,
            "score": score,
            "source_path": source_path
        })
    
    context = "\n\n---\n\n".join(context_parts)
    
    # 3. Syntéza pomocou LLM cez OpenRouter
    api_key = load_api_key()
    if not api_key:
        return {
            "query": query,
            "error": "OPENROUTER_API_KEY nie je nastavený",
            "raw_results": rag_results
        }
    
    # VŽDY používame OpenRouter
    client = OpenAI(
        api_key=api_key, 
        base_url=OPENROUTER_BASE_URL,
        default_headers={
            "HTTP-Referer": "https://github.com/xvadur/system",
            "X-Title": "RAG Query Synthesis"
        }
    )
    
    # System prompt pre syntézu
    system_prompt = """Si expertný analytik a syntetizátor informácií. Tvoja úloha je vytvoriť syntetizovanú odpoveď na základe relevantných textov z RAG vyhľadávania.

Požiadavky:
- Odpoveď musí byť syntetizovaná (nie len zoznam surových textov)
- Obsahuj hlavné informácie, kľúčové body a súvislosti
- Zachovaj dôležité fakty, dátumy a kontext
- Odpoveď musí byť čitateľná a zmysluplná
- Ak je to chronológia, formátuj ju chronologicky
- Ak je to analýza, poskytni syntézu hlavných myšlienok
- Používaj markdown formátovanie pre prehľadnosť

NEPOUŽÍVAJ:
- Zoznam surových citácií
- Len prekopírované texty
- Neformátovaný text

POUŽÍVAJ:
- Syntetizované odstavce
- Hlavné body a zhrnutia
- Chronologické usporiadanie (ak je relevantné)
- Markdown formátovanie"""
    
    user_prompt = f"""Otázka: {query}

Relevantné texty z RAG vyhľadávania:
{context}

Vytvor syntetizovanú odpoveď, ktorá obsahuje hlavné informácie z týchto textov. 
Odpoveď musí byť užitočná a čitateľná, nie len zoznam surových citácií."""
    
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=temperature
        )
        
        synthesized_answer = response.choices[0].message.content
        
        return {
            "query": query,
            "synthesized_answer": synthesized_answer,
            "sources_count": len(sources),
            "sources": sources,
            "raw_results_count": len(rag_results),
            "model_used": model
        }
        
    except Exception as e:
        return {
            "query": query,
            "error": f"Chyba pri syntéze: {str(e)}",
            "raw_results": rag_results
        }


def format_result(result: Dict) -> str:
    """Formátuje výsledok pre pekný výpis"""
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
    """Hlavná funkcia - volaná z Cursor agenta alebo CLI"""
    if len(sys.argv) < 2:
        print("Použitie: python rag_agent_helper.py 'query' [top_k] [min_score] [use_hybrid] [mode] [content_type] [output_format]")
        print("\nParametre:")
        print("  query          - Vyhľadávací dotaz (povinný)")
        print("  top_k          - Počet výsledkov (default: 5)")
        print("  min_score      - Minimálne similarity score (default: 0.4)")
        print("  use_hybrid     - Použiť hybrid search (default: true)")
        print("  mode           - 'search' alebo 'query' (default: search)")
        print("  content_type   - Filter: 'prompt', 'response', 'pair', alebo None (default: None)")
        print("  output_format  - 'json' alebo 'pretty' (default: json)")
        print("\nPríklady:")
        print("  python rag_agent_helper.py 'ako som riešil n8n' 5 0.4 true search None pretty")
        print("  python rag_agent_helper.py 'chronológia augusta' 10 0.4 true query None json")
        sys.exit(1)
    
    query = sys.argv[1]
    top_k = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    min_score = float(sys.argv[3]) if len(sys.argv) > 3 else 0.4
    use_hybrid = sys.argv[4].lower() == "true" if len(sys.argv) > 4 else True
    mode = sys.argv[5].lower() if len(sys.argv) > 5 else "search"  # "search" alebo "query"
    content_type_filter = sys.argv[6] if len(sys.argv) > 6 else None
    output_format = sys.argv[7].lower() if len(sys.argv) > 7 else "json"  # "json" alebo "pretty"
    
    if content_type_filter and content_type_filter.lower() == "none":
        content_type_filter = None
    
    if mode == "query":
        # Syntetizovaná odpoveď
        model = sys.argv[8] if len(sys.argv) > 8 else "deepseek/deepseek-v3.2"
        result = query_rag_with_synthesis(
            query=query,
            top_k=top_k,
            min_score=min_score,
            use_hybrid=use_hybrid,
            model=model
        )
        
        if output_format == "pretty":
            print("="*60)
            print("✅ RAG QUERY - SYNTHESIS MODE")
            print("="*60)
            print(f"Dotaz: {query}")
            print(f"Model: {model}")
            print("="*60)
            print("\n" + result.get("synthesized_answer", "Žiadna odpoveď"))
            print("\n" + "="*60)
            print(f"Zdrojov: {result.get('sources_count', 0)}")
            print("="*60)
        else:
            print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        # Search mode - surové výsledky
        results = search_rag(
            query, 
            top_k=top_k, 
            min_score=min_score, 
            use_hybrid=use_hybrid,
            content_type_filter=content_type_filter
        )
        
        if output_format == "pretty":
            print("="*60)
            print("🔍 RAG SEARCH - " + ("HYBRID MODE" if use_hybrid else "SEMANTIC MODE"))
            print("="*60)
            print(f"Dotaz: {query}")
            print(f"Top K: {top_k}")
            print(f"Mode: {'Hybrid (Semantic + Keyword)' if use_hybrid else 'Semantic only'}")
            if content_type_filter:
                print(f"Content Type Filter: {content_type_filter}")
            print("="*60)
            print()
            
            if not results:
                print("❌ Nenašli sa žiadne výsledky")
                return
            
            print(f"✅ Nájdených {len(results)} výsledkov:\n")
            
            for result in results:
                print(format_result(result))
        else:
            # JSON výstup (pre agenta)
            output = {
                "query": query,
                "search_type": "hybrid" if use_hybrid else "semantic",
                "results_count": len(results),
                "results": results
            }
            print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
