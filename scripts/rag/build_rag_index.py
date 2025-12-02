#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RAG Index Builder: Vytvorí FAISS index z prompts_clean dát.

Fáza 1: MVP - len prompts_clean/prompts_split
"""

import json
import os
import sys
from pathlib import Path
from typing import List, Dict, Optional
import time

# OpenAI pre embeddings
try:
    from openai import OpenAI
except ImportError:
    print("❌ Chyba: Potrebuješ nainštalovať openai")
    print("   pip install openai")
    sys.exit(1)

# FAISS pre vector database
try:
    import faiss
    import numpy as np
except ImportError:
    print("❌ Chyba: Potrebuješ nainštalovať faiss-cpu a numpy")
    print("   pip install faiss-cpu numpy")
    sys.exit(1)

# Konfigurácia
PROMPTS_DIR = Path("data/prompts/prompts_split")
OUTPUT_DIR = Path("data/rag_index")
EMBEDDING_MODEL = "text-embedding-3-small"  # Lacnejšie, rýchlejšie
EMBEDDING_DIM = 1536  # text-embedding-3-small má 1536 dimenzií
BATCH_SIZE = 100  # Počet promptov na batch
MAX_CHUNK_SIZE = 2000  # Maximálna veľkosť chunku (znaky)

# OpenAI API Key (z environment alebo .env)
API_KEY = os.getenv("OPENAI_API_KEY")
if not API_KEY:
    print("⚠️  OPENAI_API_KEY nie je nastavený v environment")
    print("   Nastav ho: export OPENAI_API_KEY='sk-...'")
    sys.exit(1)


def load_prompts(prompts_dir: Path) -> List[Dict]:
    """
    Načíta všetky prompty z prompts_clean/prompts_split.
    
    Returns:
        List of prompt dictionaries with metadata
    """
    prompts = []
    
    print(f"📖 Načítavam prompty z: {prompts_dir}")
    
    for day_dir in sorted(prompts_dir.glob("*")):
        if not day_dir.is_dir():
            continue
        
        for json_file in sorted(day_dir.glob("*.json")):
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Validácia
                if not data.get("text") or not data.get("author_guess") == "adam":
                    continue
                
                prompts.append({
                    "id": f"{day_dir.name}_{json_file.stem}",
                    "text": data.get("text", ""),
                    "date": data.get("date", ""),
                    "timestamp": data.get("timestamp", ""),
                    "index": data.get("index", 0),
                    "source_path": data.get("source_path", ""),
                    "word_count": data.get("word_count", 0),
                })
            except Exception as e:
                print(f"⚠️  Chyba pri načítaní {json_file}: {e}")
                continue
    
    print(f"✅ Načítaných {len(prompts)} promptov")
    return prompts


def chunk_text(text: str, max_size: int = MAX_CHUNK_SIZE) -> List[str]:
    """
    Inteligentné chunking textu.
    
    Pre prompty: ak je text < max_size, vráti celý text ako jeden chunk.
    Ak je dlhší, rozdelí podľa odsekov.
    """
    if len(text) <= max_size:
        return [text]
    
    # Rozdelenie podľa odsekov (\n\n)
    chunks = []
    paragraphs = text.split("\n\n")
    
    current_chunk = ""
    for para in paragraphs:
        # Ak pridaním odseku prekročíme max_size, uložíme aktuálny chunk
        if len(current_chunk) + len(para) + 2 > max_size and current_chunk:
            chunks.append(current_chunk.strip())
            current_chunk = para
        else:
            current_chunk += "\n\n" + para if current_chunk else para
    
    # Pridaj posledný chunk
    if current_chunk:
        chunks.append(current_chunk.strip())
    
    # Ak je niektorý chunk stále príliš dlhý, rozdelíme ho podľa viet
    final_chunks = []
    for chunk in chunks:
        if len(chunk) <= max_size:
            final_chunks.append(chunk)
        else:
            # Rozdelenie podľa viet
            sentences = chunk.split(". ")
            current = ""
            for sent in sentences:
                if len(current) + len(sent) + 2 > max_size and current:
                    final_chunks.append(current.strip() + ".")
                    current = sent
                else:
                    current += ". " + sent if current else sent
            if current:
                final_chunks.append(current.strip())
    
    return final_chunks if final_chunks else [text]


def generate_embeddings(client: OpenAI, texts: List[str], model: str = EMBEDDING_MODEL) -> List[List[float]]:
    """
    Generuje embeddings pre batch textov.
    
    Args:
        client: OpenAI client
        texts: List of texts to embed
        model: Embedding model name
    
    Returns:
        List of embedding vectors
    """
    try:
        response = client.embeddings.create(
            model=model,
            input=texts
        )
        return [item.embedding for item in response.data]
    except Exception as e:
        print(f"❌ Chyba pri generovaní embeddings: {e}")
        return []


def build_index(prompts: List[Dict], output_dir: Path) -> None:
    """
    Vytvorí FAISS index z promptov.
    
    Args:
        prompts: List of prompt dictionaries
        output_dir: Output directory for index files
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    
    client = OpenAI(api_key=API_KEY)
    
    # Zbieranie všetkých chunkov s metadátami
    all_chunks = []
    all_embeddings = []
    all_metadata = []
    
    print(f"\n🔨 Spracovávam {len(prompts)} promptov...")
    
    # Chunking
    total_chunks = 0
    for prompt in prompts:
        chunks = chunk_text(prompt["text"])
        
        for chunk_idx, chunk_content in enumerate(chunks):
            all_chunks.append(chunk_content)
            all_metadata.append({
                "id": prompt["id"],
                "chunk_index": chunk_idx,
                "total_chunks": len(chunks),
                "date": prompt["date"],
                "timestamp": prompt["timestamp"],
                "source_path": prompt["source_path"],
                "word_count": prompt["word_count"],
                "chunk_text": chunk_content[:100] + "..." if len(chunk_content) > 100 else chunk_content  # Preview
            })
            total_chunks += 1
    
    print(f"✅ Vytvorených {total_chunks} chunkov z {len(prompts)} promptov")
    print(f"📊 Priemerne {total_chunks / len(prompts):.1f} chunkov na prompt\n")
    
    # Generovanie embeddings po batchoch
    print(f"🚀 Generujem embeddings (model: {EMBEDDING_MODEL})...")
    print(f"   Batch size: {BATCH_SIZE}\n")
    
    for i in range(0, len(all_chunks), BATCH_SIZE):
        batch = all_chunks[i:i + BATCH_SIZE]
        batch_num = (i // BATCH_SIZE) + 1
        total_batches = (len(all_chunks) + BATCH_SIZE - 1) // BATCH_SIZE
        
        print(f"   Batch {batch_num}/{total_batches} ({len(batch)} chunkov)...", end=" ", flush=True)
        
        embeddings = generate_embeddings(client, batch, EMBEDDING_MODEL)
        
        if embeddings:
            all_embeddings.extend(embeddings)
            print(f"✅")
        else:
            print(f"❌ Chyba")
            # Pridaj prázdne embeddings (budeme ich musieť preskočiť)
            all_embeddings.extend([[0.0] * EMBEDDING_DIM] * len(batch))
        
        # Rate limiting (OpenAI má limit 5000 requests/min)
        if i + BATCH_SIZE < len(all_chunks):
            time.sleep(0.1)
    
    # Validácia
    if len(all_embeddings) != len(all_chunks):
        print(f"❌ Chyba: Počet embeddings ({len(all_embeddings)}) != počet chunkov ({len(all_chunks)})")
        return
    
    # Konverzia na numpy array
    print(f"\n💾 Vytváram FAISS index...")
    embeddings_array = np.array(all_embeddings, dtype=np.float32)
    
    # Vytvorenie FAISS indexu (L2 distance)
    index = faiss.IndexFlatL2(EMBEDDING_DIM)
    index.add(embeddings_array)
    
    # Uloženie indexu
    index_path = output_dir / "faiss.index"
    faiss.write_index(index, str(index_path))
    print(f"✅ FAISS index uložený: {index_path}")
    
    # Uloženie metadát
    metadata_path = output_dir / "metadata.json"
    with open(metadata_path, 'w', encoding='utf-8') as f:
        json.dump(all_metadata, f, ensure_ascii=False, indent=2)
    print(f"✅ Metadata uložené: {metadata_path}")
    
    # Uloženie chunkov (pre debugging a retrieval)
    chunks_path = output_dir / "chunks.json"
    with open(chunks_path, 'w', encoding='utf-8') as f:
        json.dump(all_chunks, f, ensure_ascii=False, indent=2)
    print(f"✅ Chunks uložené: {chunks_path}")
    
    # Štatistiky
    print(f"\n{'='*60}")
    print(f"📊 ŠTATISTIKY")
    print(f"{'='*60}")
    print(f"Celkový počet promptov: {len(prompts)}")
    print(f"Celkový počet chunkov: {total_chunks}")
    print(f"Priemerne chunkov na prompt: {total_chunks / len(prompts):.1f}")
    print(f"Embedding dimenzie: {EMBEDDING_DIM}")
    print(f"FAISS index veľkosť: {index.ntotal} vektorov")
    print(f"{'='*60}\n")
    
    print(f"✅ RAG index úspešne vytvorený!")
    print(f"   Index: {index_path}")
    print(f"   Metadata: {metadata_path}")
    print(f"   Chunks: {chunks_path}")


def main():
    """Hlavná funkcia"""
    print("="*60)
    print("🧠 RAG INDEX BUILDER - MVP")
    print("="*60)
    print(f"Zdroj: {PROMPTS_DIR}")
    print(f"Výstup: {OUTPUT_DIR}")
    print(f"Model: {EMBEDDING_MODEL}")
    print("="*60)
    print()
    
    # Kontrola existencie adresára
    if not PROMPTS_DIR.exists():
        print(f"❌ Adresár neexistuje: {PROMPTS_DIR}")
        sys.exit(1)
    
    # Načítanie promptov
    prompts = load_prompts(PROMPTS_DIR)
    
    if not prompts:
        print("❌ Nenašli sa žiadne prompty")
        sys.exit(1)
    
    # Vytvorenie indexu
    build_index(prompts, OUTPUT_DIR)
    
    print("\n🎉 Hotovo! Teraz môžeš použiť rag_search.py na vyhľadávanie.")


if __name__ == "__main__":
    main()

