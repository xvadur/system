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

# Debug logging - relative to workspace root
# Script is in core/rag/, so go up 2 levels to workspace root
_workspace_root = Path(__file__).parent.parent.parent
DEBUG_LOG_PATH = _workspace_root / ".cursor" / "debug.log"

def debug_log(location: str, message: str, data: dict, hypothesis_id: str = None):
    """Write debug log entry."""
    try:
        import json
        from datetime import datetime
        log_entry = {
            "timestamp": int(datetime.now().timestamp() * 1000),
            "location": location,
            "message": message,
            "data": data,
            "sessionId": "debug-session",
            "runId": "run1",
            "hypothesisId": hypothesis_id
        }
        with open(DEBUG_LOG_PATH, 'a', encoding='utf-8') as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')
    except Exception:
        pass  # Fail silently

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
CONVERSATION_PAIRS_FILE = Path("development/data/conversations.jsonl")
OUTPUT_DIR = Path("data/rag_index")
EMBEDDING_MODEL = "text-embedding-3-small"  # Lacnejšie, rýchlejšie
EMBEDDING_DIM = 1536  # text-embedding-3-small má 1536 dimenzií
BATCH_SIZE = 100  # Počet promptov na batch
MAX_CHUNK_SIZE = 2000  # Maximálna veľkosť chunku (znaky)

# Flags
INCLUDE_AI_RESPONSES = True  # Pridať AI odpovede do indexu
COMBINE_PAIRS = True  # Kombinovať prompt + odpoveď ako jeden chunk

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
            except Exception:
                continue
    
    return None

API_KEY = load_api_key()
if not API_KEY:
    print("⚠️  OPENAI_API_KEY nie je nastavený")
    print("   Nastav ho v environmente alebo v .env súbore")
    sys.exit(1)


def load_prompts(prompts_dir: Path) -> List[Dict]:
    """
    Načíta všetky prompty z prompts_clean/prompts_split.
    
    Returns:
        List of prompt dictionaries with metadata
    """
    prompts = []
    
    print(f"📖 Načítavam prompty z: {prompts_dir}")
    
    if not prompts_dir.exists():
        print(f"⚠️  Adresár neexistuje: {prompts_dir}")
        return prompts
    
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
                    "content_type": "prompt",  # Označenie typu
                })
            except Exception as e:
                print(f"⚠️  Chyba pri načítaní {json_file}: {e}")
                continue
    
    print(f"✅ Načítaných {len(prompts)} promptov")
    return prompts


def load_conversation_pairs(input_file: Path) -> List[Dict]:
    """
    Načíta conversation pairs z JSONL súboru.
    
    Returns:
        List of conversation pair dictionaries with metadata
    """
    pairs = []
    
    if not input_file.exists():
        print(f"⚠️  Súbor neexistuje: {input_file}")
        return pairs
    
    print(f"📖 Načítavam conversation pairs z: {input_file}")
    
    with open(input_file, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            
            try:
                pair_data = json.loads(line)
                
                user_text = pair_data.get("user_prompt", {}).get("extracted_text", "")
                ai_text = pair_data.get("ai_response", {}).get("extracted_text", "")
                timestamp = pair_data.get("timestamp", "")
                session = pair_data.get("session", "")
                
                # Validácia - oba texty musia existovať
                if not user_text or not user_text.strip():
                    continue
                if not ai_text or not ai_text.strip():
                    continue
                
                # Extrahovanie dátumu z timestamp
                date = ""
                if timestamp:
                    try:
                        from datetime import datetime
                        dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                        date = dt.strftime('%Y-%m-%d')
                    except:
                        date = timestamp[:10] if len(timestamp) >= 10 else ""
                
                pairs.append({
                    "id": f"pair_{session}_{line_num}",
                    "user_text": user_text.strip(),
                    "ai_text": ai_text.strip(),
                    "date": date,
                    "timestamp": timestamp,
                    "session": session,
                    "content_type": "pair",
                    "word_count": len(user_text.split()) + len(ai_text.split()),
                })
            except Exception as e:
                print(f"⚠️  Chyba pri načítaní riadku {line_num}: {e}")
                continue
    
    print(f"✅ Načítaných {len(pairs)} conversation pairs")
    return pairs


def create_dialogue_chunks(pair: Dict) -> List[str]:
    """
    Vytvorí chunky z dialógu (prompt + odpoveď kombinované).
    
    Formát: "User: ...\n\nAssistant: ..."
    
    Args:
        pair: Conversation pair dictionary
    
    Returns:
        List of dialogue chunks
    """
    user_text = pair.get("user_text", "")
    ai_text = pair.get("ai_text", "")
    
    # Kombinovaný dialóg
    dialogue = f"User: {user_text}\n\nAssistant: {ai_text}"
    
    # Ak je dialóg krátky, vráť ho ako jeden chunk
    if len(dialogue) <= MAX_CHUNK_SIZE:
        return [dialogue]
    
    # Ak je dlhý, rozdelíme ho inteligentne
    # Najprv skúsime rozdeliť podľa odsekov v AI odpovedi
    chunks = []
    
    # Ak je user prompt dlhý, môžeme ho rozdeliť
    if len(user_text) > MAX_CHUNK_SIZE // 2:
        user_chunks = chunk_text(user_text, MAX_CHUNK_SIZE // 2)
        ai_chunks = chunk_text(ai_text, MAX_CHUNK_SIZE // 2)
        
        # #region agent log
        debug_log(
            "build_rag_index.py:220",
            "create_dialogue_chunks: Before zip pairing",
            {
                "user_chunks_count": len(user_chunks),
                "ai_chunks_count": len(ai_chunks),
                "user_text_length": len(user_text),
                "ai_text_length": len(ai_text)
            },
            "A"
        )
        # #endregion
        
        # Kombinuj user a AI chunky
        paired_count = 0
        for i, (uc, ac) in enumerate(zip(user_chunks, ai_chunks)):
            # #region agent log
            debug_log(
                "build_rag_index.py:225",
                "create_dialogue_chunks: Processing zip pair",
                {
                    "pair_index": i,
                    "user_chunk_length": len(uc),
                    "ai_chunk_length": len(ac),
                    "combined_length": len(f"User: {uc}\n\nAssistant: {ac}")
                },
                "A"
            )
            # #endregion
            combined = f"User: {uc}\n\nAssistant: {ac}"
            if len(combined) <= MAX_CHUNK_SIZE:
                chunks.append(combined)
            else:
                # Ak je stále príliš dlhý, rozdeliť ešte viac
                chunks.extend(chunk_text(combined, MAX_CHUNK_SIZE))
            paired_count += 1
        
        # #region agent log
        debug_log(
            "build_rag_index.py:240",
            "create_dialogue_chunks: After zip pairing",
            {
                "paired_count": paired_count,
                "user_chunks_count": len(user_chunks),
                "ai_chunks_count": len(ai_chunks),
                "chunks_created": len(chunks),
                "user_chunks_lost": max(0, len(user_chunks) - paired_count),
                "ai_chunks_lost": max(0, len(ai_chunks) - paired_count)
            },
            "A"
        )
        # #endregion
        
        # Handle remaining chunks from longer list
        if len(user_chunks) > len(ai_chunks):
            # #region agent log
            debug_log(
                "build_rag_index.py:250",
                "create_dialogue_chunks: Handling remaining user chunks",
                {
                    "remaining_user_chunks": len(user_chunks) - paired_count,
                    "last_ai_chunk": ai_chunks[-1] if ai_chunks else None
                },
                "C"
            )
            # #endregion
            # Remaining user chunks - pair with last AI chunk or create standalone
            last_ai_chunk = ai_chunks[-1] if ai_chunks else ""
            for uc in user_chunks[paired_count:]:
                combined = f"User: {uc}\n\nAssistant: {last_ai_chunk}" if last_ai_chunk else f"User: {uc}"
                if len(combined) <= MAX_CHUNK_SIZE:
                    chunks.append(combined)
                else:
                    chunks.extend(chunk_text(combined, MAX_CHUNK_SIZE))
        elif len(ai_chunks) > len(user_chunks):
            # #region agent log
            debug_log(
                "build_rag_index.py:265",
                "create_dialogue_chunks: Handling remaining AI chunks",
                {
                    "remaining_ai_chunks": len(ai_chunks) - paired_count,
                    "last_user_chunk": user_chunks[-1] if user_chunks else None
                },
                "C"
            )
            # #endregion
            # Remaining AI chunks - pair with last user chunk
            last_user_chunk = user_chunks[-1] if user_chunks else ""
            for ac in ai_chunks[paired_count:]:
                combined = f"User: {last_user_chunk}\n\nAssistant: {ac}" if last_user_chunk else f"Assistant: {ac}"
                if len(combined) <= MAX_CHUNK_SIZE:
                    chunks.append(combined)
                else:
                    chunks.extend(chunk_text(combined, MAX_CHUNK_SIZE))
    else:
        # User prompt je krátky, rozdeliť len AI odpoveď
        ai_chunks = chunk_text(ai_text, MAX_CHUNK_SIZE - len(user_text) - 20)  # -20 pre "User: ...\n\nAssistant: "
        
        for ac in ai_chunks:
            combined = f"User: {user_text}\n\nAssistant: {ac}"
            chunks.append(combined)
    
    return chunks if chunks else [dialogue]


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


def build_index(prompts: List[Dict], pairs: List[Dict], output_dir: Path) -> None:
    """
    Vytvorí FAISS index z promptov a conversation pairs.
    
    Args:
        prompts: List of prompt dictionaries
        pairs: List of conversation pair dictionaries
        output_dir: Output directory for index files
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    
    client = OpenAI(api_key=API_KEY)
    
    # Zbieranie všetkých chunkov s metadátami
    all_chunks = []
    all_embeddings = []
    all_metadata = []
    
    print(f"\n🔨 Spracovávam {len(prompts)} promptov...")
    
    # Chunking promptov
    total_chunks = 0
    for prompt in prompts:
        chunks = chunk_text(prompt["text"])
        
        for chunk_idx, chunk_content in enumerate(chunks):
            all_chunks.append(chunk_content)
            all_metadata.append({
                "id": prompt["id"],
                "content_type": prompt.get("content_type", "prompt"),
                "chunk_index": chunk_idx,
                "total_chunks": len(chunks),
                "date": prompt["date"],
                "timestamp": prompt["timestamp"],
                "source_path": prompt.get("source_path", ""),
                "word_count": prompt["word_count"],
                "chunk_text": chunk_content[:100] + "..." if len(chunk_content) > 100 else chunk_content  # Preview
            })
            total_chunks += 1
    
    print(f"✅ Vytvorených {total_chunks} chunkov z {len(prompts)} promptov")
    if prompts:
        print(f"📊 Priemerne {total_chunks / len(prompts):.1f} chunkov na prompt")
    
    # Chunking conversation pairs
    if pairs and INCLUDE_AI_RESPONSES:
        print(f"\n🔨 Spracovávam {len(pairs)} conversation pairs...")
        
        pairs_chunks = 0
        for pair in pairs:
            if COMBINE_PAIRS:
                # Kombinovať prompt + odpoveď ako jeden chunk
                chunks = create_dialogue_chunks(pair)
            else:
                # Samostatné chunky pre user a AI
                user_chunks = chunk_text(pair["user_text"])
                ai_chunks = chunk_text(pair["ai_text"])
                chunks = []
                for uc in user_chunks:
                    chunks.append(f"User: {uc}")
                for ac in ai_chunks:
                    chunks.append(f"Assistant: {ac}")
            
            for chunk_idx, chunk_content in enumerate(chunks):
                all_chunks.append(chunk_content)
                all_metadata.append({
                    "id": pair["id"],
                    "content_type": pair.get("content_type", "pair"),
                    "chunk_index": chunk_idx,
                    "total_chunks": len(chunks),
                    "date": pair["date"],
                    "timestamp": pair["timestamp"],
                    "session": pair.get("session", ""),
                    "user_text": pair.get("user_text", "")[:200] + "..." if len(pair.get("user_text", "")) > 200 else pair.get("user_text", ""),
                    "ai_text": pair.get("ai_text", "")[:200] + "..." if len(pair.get("ai_text", "")) > 200 else pair.get("ai_text", ""),
                    "word_count": pair["word_count"],
                    "chunk_text": chunk_content[:100] + "..." if len(chunk_content) > 100 else chunk_content  # Preview
                })
                pairs_chunks += 1
        
        print(f"✅ Vytvorených {pairs_chunks} chunkov z {len(pairs)} conversation pairs")
        if pairs:
            print(f"📊 Priemerne {pairs_chunks / len(pairs):.1f} chunkov na pár")
        total_chunks += pairs_chunks
    
    print(f"\n📊 Celkovo {total_chunks} chunkov\n")
    
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
    if pairs:
        print(f"Celkový počet conversation pairs: {len(pairs)}")
    print(f"Celkový počet chunkov: {total_chunks}")
    if prompts:
        prompt_chunks = sum(1 for m in all_metadata if m.get("content_type") == "prompt")
        print(f"Chunky z promptov: {prompt_chunks}")
    if pairs:
        pair_chunks = sum(1 for m in all_metadata if m.get("content_type") == "pair")
        print(f"Chunky z conversation pairs: {pair_chunks}")
    if prompts:
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
    print("🧠 RAG INDEX BUILDER - Extended (Prompts + AI Responses)")
    print("="*60)
    print(f"Zdroj promptov: {PROMPTS_DIR}")
    if INCLUDE_AI_RESPONSES:
        print(f"Zdroj conversation pairs: {CONVERSATION_PAIRS_FILE}")
    print(f"Výstup: {OUTPUT_DIR}")
    print(f"Model: {EMBEDDING_MODEL}")
    print(f"Include AI Responses: {INCLUDE_AI_RESPONSES}")
    print(f"Combine Pairs: {COMBINE_PAIRS}")
    print("="*60)
    print()
    
    # Načítanie promptov
    prompts = []
    if PROMPTS_DIR.exists():
        prompts = load_prompts(PROMPTS_DIR)
    else:
        print(f"⚠️  Adresár neexistuje: {PROMPTS_DIR} (preskakujem)")
    
    # Načítanie conversation pairs
    pairs = []
    if INCLUDE_AI_RESPONSES:
        pairs = load_conversation_pairs(CONVERSATION_PAIRS_FILE)
    
    if not prompts and not pairs:
        print("❌ Nenašli sa žiadne dáta (prompty ani conversation pairs)")
        sys.exit(1)
    
    # Vytvorenie indexu
    build_index(prompts, pairs, OUTPUT_DIR)
    
    print("\n🎉 Hotovo! Teraz môžeš použiť rag_agent_helper.py na vyhľadávanie.")


if __name__ == "__main__":
    main()

