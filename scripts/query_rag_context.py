#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Query-based RAG s kontextom: Vráti relevantné odseky s kontextom pred/po.
"""

import json
import re
import sys
from pathlib import Path
from typing import List, Dict, Optional

# Import RAG helper funkcií
sys.path.insert(0, str(Path(__file__).parent.parent / "archive" / "rag" / "rag"))
from rag_agent_helper import search_rag, INDEX_DIR

# Konfigurácia indexov
INDEX_DIR_BY_WEEK = Path("data/rag_index_by_week")


def split_into_sentences(text: str) -> List[str]:
    """
    Rozdelí text na vety.
    
    Podporuje slovenčinu a angličtinu.
    """
    if not text or not text.strip():
        return []
    
    # Regex pre rozdelenie viet (slovenčina + angličtina)
    # Podporuje: . ! ? ... a kombinácie
    sentence_endings = r'[.!?]+(?:\s+|$)'
    sentences = re.split(sentence_endings, text)
    
    # Vyčistiť a filtrovať prázdne vety
    cleaned = []
    for sent in sentences:
        sent = sent.strip()
        if sent and len(sent) > 5:  # Minimálna dĺžka vety
            cleaned.append(sent)
    
    # Ak sa nepodarilo rozdeliť, vráť celý text ako jednu vetu
    if not cleaned:
        return [text.strip()] if text.strip() else []
    
    return cleaned


def extract_relevant_paragraph(
    chunk_text: str,
    query: str,
    context_sentences: int = 2,
    paragraph_sentences: int = 3
) -> Dict[str, str]:
    """
    Extrahuje relevantný odsek z chunk textu s kontextom pred/po.
    
    Args:
        chunk_text: Celý chunk text
        query: Pôvodná query pre nájdenie relevantnej časti
        context_sentences: Počet viet kontextu pred/po (default: 2)
        paragraph_sentences: Počet viet v relevantnom odseku (default: 3)
    
    Returns:
        Dict s kľúčmi: text, context_before, context_after
    """
    if not chunk_text or not chunk_text.strip():
        return {
            "text": "",
            "context_before": "",
            "context_after": ""
        }
    
    # Ak chunk obsahuje "User:" a "Assistant:", zameraj sa len na Assistant časť
    if "Assistant:" in chunk_text:
        # Rozdel na User a Assistant časť
        parts = re.split(r'Assistant:\s*', chunk_text, flags=re.IGNORECASE, maxsplit=1)
        if len(parts) > 1:
            # Použi len Assistant časť
            assistant_text = parts[1]
            # Ak je User časť krátka, môžeme ju použiť ako kontext
            user_part = parts[0].replace("User:", "").strip()
            use_user_as_context = len(user_part) < 200
        else:
            assistant_text = chunk_text
            use_user_as_context = False
    else:
        assistant_text = chunk_text
        use_user_as_context = False
    
    # Rozdeliť na vety
    sentences = split_into_sentences(assistant_text)
    
    if not sentences:
        return {
            "text": chunk_text.strip(),
            "context_before": "",
            "context_after": ""
        }
    
    # Ak je len jedna veta, vráť ju bez kontextu
    if len(sentences) == 1:
        return {
            "text": sentences[0],
            "context_before": "",
            "context_after": ""
        }
    
    # Nájdi najrelevantnejšiu vetu
    query_lower = query.lower()
    query_words = set(re.findall(r'\b\w+\b', query_lower))
    
    best_sentence_idx = 0
    best_score = 0
    
    for idx, sentence in enumerate(sentences):
        sentence_lower = sentence.lower()
        sentence_words = set(re.findall(r'\b\w+\b', sentence_lower))
        
        # Score: počet spoločných slov
        common_words = query_words & sentence_words
        score = len(common_words)
        
        # Bonus ak query je priamo v vete
        if query_lower in sentence_lower:
            score += 10
        
        if score > best_score:
            best_score = score
            best_sentence_idx = idx
    
    # Vypočítaj rozsah relevantného odseku
    start_idx = max(0, best_sentence_idx - (paragraph_sentences // 2))
    end_idx = min(len(sentences), start_idx + paragraph_sentences)
    
    # Uprav start_idx ak by sme presiahli koniec
    if end_idx == len(sentences):
        start_idx = max(0, end_idx - paragraph_sentences)
    
    # Extrahuj relevantný odsek
    relevant_sentences = sentences[start_idx:end_idx]
    paragraph_text = " ".join(relevant_sentences)
    
    # Extrahuj kontext pred
    context_before_start = max(0, start_idx - context_sentences)
    context_before_sentences = sentences[context_before_start:start_idx]
    context_before = " ".join(context_before_sentences) if context_before_sentences else ""
    
    # Ak máme User časť a je krátka, pridaj ju na začiatok kontextu
    if use_user_as_context and user_part:
        if context_before:
            context_before = f"User: {user_part}\n\n{context_before}"
        else:
            context_before = f"User: {user_part}"
    
    # Extrahuj kontext po
    context_after_end = min(len(sentences), end_idx + context_sentences)
    context_after_sentences = sentences[end_idx:context_after_end]
    context_after = " ".join(context_after_sentences) if context_after_sentences else ""
    
    return {
        "text": paragraph_text,
        "context_before": context_before,
        "context_after": context_after
    }


def query_rag_with_context(
    query: str,
    top_k: int = 20,
    index_dir: Optional[Path] = None,
    week: Optional[str] = None,
    min_score: float = 0.3
) -> Dict:
    """
    Query-based RAG search s extrakciou relevantných odsekov a kontextom.
    
    Args:
        query: Vyhľadávací dotaz
        top_k: Počet výsledkov (default: 20)
        index_dir: Adresár s RAG indexom (ak None, použije week alebo default)
        week: Týždeň pre týždenný index (napr. "2025-W29")
        min_score: Minimálne similarity score (default: 0.3)
    
    Returns:
        Dict s výsledkami v JSON formáte
    """
    # Urči index_dir
    if index_dir is None:
        if week:
            index_dir = INDEX_DIR_BY_WEEK / week
        else:
            index_dir = INDEX_DIR
    
    # RAG search
    search_results = search_rag(
        query=query,
        top_k=top_k,
        min_score=min_score,
        use_hybrid=True,
        index_dir=index_dir
    )
    
    # Kontrola chýb
    if not search_results:
        return {
            "query": query,
            "total_results": 0,
            "error": "Žiadne výsledky alebo chyba pri vyhľadávaní",
            "results": []
        }
    
    if isinstance(search_results, list) and search_results and "error" in search_results[0]:
        return {
            "query": query,
            "total_results": 0,
            "error": search_results[0].get("error", "Neznáma chyba"),
            "results": []
        }
    
    # Spracuj výsledky - FILTROVANIE: len user texty (nie AI odpovede)
    formatted_results = []
    
    for result in search_results:
        chunk_text = result.get("text", "")
        if not chunk_text:
            continue
        
        # Extrahuj len USER časť (pred "Assistant:" alebo ak nie je "Assistant:", ber celý text)
        user_text = chunk_text
        if "Assistant:" in chunk_text or "\n\nAssistant:" in chunk_text:
            # Rozdel na user a assistant časť
            parts = chunk_text.split("\n\nAssistant:", 1)
            user_text = parts[0]
            # Odstráň "User:" prefix ak existuje
            if user_text.startswith("User:"):
                user_text = user_text[5:].strip()
        
        # Preskoč ak je user_text prázdny alebo je to len AI odpoveď
        if not user_text or user_text.strip() == "":
            continue
        
        # Kontrola: ak text obsahuje typické AI frázy na začiatku a nie je tam "User:", preskoč
        ai_phrases = [
            "Samozrejme", "Ako kAI", "Prezident", "Na základe", 
            "Toto je", "Vaša", "Váš", "Vy potrebujete", "Je to",
            "Tento dokument", "Fáza 1:", "Fáza 2:", "###", "**"
        ]
        first_sentence = user_text.split(".")[0].strip()
        if any(phrase in first_sentence[:50] for phrase in ai_phrases):
            # Možno je to AI, ale skontroluj či nie je to user citácia
            if "User:" not in chunk_text[:200] and not user_text.strip().startswith('"'):
                continue
        
        # Použi user_text namiesto chunk_text
        chunk_text = user_text
        
        # Extrahuj relevantný odsek s kontextom
        extracted = extract_relevant_paragraph(
            chunk_text=chunk_text,
            query=query,
            context_sentences=2,
            paragraph_sentences=3
        )
        
        # Zostav výsledok
        formatted_result = {
            "text": extracted["text"],
            "context_before": extracted["context_before"],
            "context_after": extracted["context_after"],
            "score": result.get("score", 0.0),
            "date": result.get("date", "N/A"),
            "timestamp": result.get("timestamp", "N/A"),
            "source": result.get("source_path", "N/A"),
            "metadata": {
                "content_type": result.get("content_type", "unknown"),
                "session": result.get("session", result.get("metadata", {}).get("session", "N/A")),
                "week": result.get("week", "N/A")
            }
        }
        
        formatted_results.append(formatted_result)
    
    return {
        "query": query,
        "total_results": len(formatted_results),
        "results": formatted_results
    }


if __name__ == "__main__":
    # Test
    if len(sys.argv) > 1:
        query = sys.argv[1]
        week = sys.argv[2] if len(sys.argv) > 2 else None
        
        result = query_rag_with_context(query, week=week)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("Použitie: python3 query_rag_context.py 'query' [week]")
        print("Príklad: python3 query_rag_context.py 'čo vie Adam o AI' 2025-W29")
