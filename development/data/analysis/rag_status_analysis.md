# Analýza Stavu RAG Systému

**Dátum:** 2025-12-13  
**Účel:** Analýza aktuálneho stavu RAG systému a identifikácia chýbajúcich dát

---

## 📊 Aktuálny Stav RAG Systému

### Existujúce Komponenty

#### 1. RAG Index (`data/rag_index/`)
✅ **Existuje:**
- `faiss.index` - FAISS vector index
- `metadata.json` - Metadata pre chunk-y (12,042 riadkov)
- `chunks.json` - Text chunk-y

**Zdroj dát:**
- Prompty z `data/prompts/prompts_split` (664 promptov)
- Conversation pairs z `development/data/conversations.jsonl` (1,822 párov)

**Štatistiky z metadát:**
- Datumový rozsah: 2025-07-19 až aktuálne
- Content types: `prompt`, `pair`
- Celkový počet chunkov: ~12,042

#### 2. RAG Kód (`archive/rag/rag/`)
✅ **Existuje:**
- `build_rag_index.py` - Builder pre RAG index (632 riadkov)
  - Podporuje prompty aj conversation pairs
  - Hybrid search (semantic + keyword/TF-IDF)
  - Chunking s max veľkosťou 2000 znakov
  - Embedding model: `text-embedding-3-small` (1536 dimenzií)
  
- `rag_agent_helper.py` - Helper pre vyhľadávanie (604 riadkov)
  - Hybrid search (semantic + TF-IDF)
  - Query synthesis mode (automatická syntéza odpovedí)
  - Content type filtering
  - JSON aj pretty output

#### 3. Dokumentácia
✅ **Existuje:**
- `archive/docs/rag/rag/RAG_GUIDE.md` - Kompletný návod

---

## ❌ Chýbajúce / Problémové Komponenty

### 1. conversations_clean_backup.jsonl
❌ **Problém:** 
- Súbor existuje: `development/data/conversations_clean_backup.jsonl`
- Veľkosť: **54,420 riadkov** (veľmi veľký súbor)
- Formát: Multi-line JSON (nie čistý JSONL)
- **NENÍ v RAG indexe** - tieto konverzácie nie sú indexované

**Obsah:**
- Záznamy majú štruktúru:
  ```json
  {
    "user_prompt": {
      "uuid": "...",
      "session": "...",
      "date_created": "2025-10-30T15:32:03.726000Z",
      ...
    },
    "ai_response": {
      ...
    },
    "timestamp": "2025-10-30T15:32:03.726000Z"
  }
  ```

**Čo to znamená:**
- Máme **54,420 konverzácií** z posledných 4 mesiacov, ktoré nie sú v RAG indexe
- Aktuálny RAG index obsahuje len `conversations.jsonl` (1,822 párov)
- To znamená, že **~96% konverzácií chýba v RAG indexe**

### 2. Rozdelenie conversations_clean_backup.jsonl
⚠️ **Potrebné:**
- Súbor je príliš veľký (54,420 riadkov)
- Potrebuje rozdelenie podľa mesiacov (aspoň 4 časti)
- Cieľ: `development/data/conversations_by_month/conversations_YYYY-MM.jsonl`

### 3. Aktualizácia build_rag_index.py
⚠️ **Potrebné:**
- Skript aktuálne načíta len `development/data/conversations.jsonl`
- Musí byť upravený na načítanie rozdelenej `conversations_clean_backup.jsonl`
- Alebo načítanie všetkých súborov z `conversations_by_month/`

---

## 🔍 Analýza conversations_clean_backup.jsonl

### Formát Súboru
- **Typ:** Multi-line JSON (nie čistý JSONL)
- **Veľkosť:** 54,420 riadkov
- **Obsah:** Konverzácie s timestampmi

### Identifikované Timestamps
Z grep výsledkov:
- `date_created`: "2025-10-30T15:32:03.726000Z"
- `timestamp`: "2025-10-30T15:32:03.726000Z"

### Potrebné Úpravy

#### 1. Parsovanie Súboru
Súbor nie je čistý JSONL (jeden JSON objekt na riadok), ale multi-line JSON. Potrebujeme:
- Streaming parser alebo
- Konverzia na JSONL formát

#### 2. Rozdelenie Podľa Mesiacov
Cieľ: Rozdeliť 54,420 konverzácií podľa mesiacov:
- `conversations_2025-08.jsonl`
- `conversations_2025-09.jsonl`
- `conversations_2025-10.jsonl`
- `conversations_2025-11.jsonl`
- (prípadne ďalšie mesiace)

#### 3. Integrácia do RAG
Po rozdelení potrebujeme:
- Aktualizovať `build_rag_index.py` na načítanie súborov z `conversations_by_month/`
- Rebuild RAG indexu s novými dátami

---

## 📋 Ďalšie Kroky

### Fáza 1: Analýza conversations_clean_backup.jsonl
1. ✅ Vytvoriť analýzu štruktúry súboru
2. ✅ Identifikovať dátumový rozsah
3. ⏳ Rozdeliť podľa mesiacov

### Fáza 2: Rozdelenie Súboru
1. ⏳ Vytvoriť skript na rozdelenie podľa mesiacov
2. ⏳ Skontrolovať kvalitu rozdelenia
3. ⏳ Validovať, že všetky konverzácie sú rozdelené

### Fáza 3: Aktualizácia RAG
1. ⏳ Upraviť `build_rag_index.py` na načítanie mesiacových súborov
2. ⏳ Rebuild RAG indexu
3. ⏳ Validovať, že všetky konverzácie sú indexované

### Fáza 4: Hlbková Analýza
1. ⏳ Aplikovať analytickú dekompozíciu z `interview_decomposition.md` na všetky konverzácie
2. ⏳ Identifikovať vzorce, témy a príležitosti v celom časovom období
3. ⏳ Vytvoriť syntetizovanú analýzu

---

## 💡 Odporúčania

### Prioritizácia
1. **Vysoká priorita:** Rozdelenie `conversations_clean_backup.jsonl` podľa mesiacov
2. **Vysoká priorita:** Aktualizácia `build_rag_index.py` na načítanie mesiacových súborov
3. **Stredná priorita:** Rebuild RAG indexu s novými dátami
4. **Nízka priorita:** Hlbková analýza (môže čakať na rebuild)

### Technické Poznámky
- Súbor je veľký (54,420 riadkov) - použiť streaming parsing
- Multi-line JSON formát - potrebný opatrný parsing
- Rozdelenie podľa mesiacov - zjednoduší spracovanie a indexovanie

---

**Status:** 🔄 V procese  
**Posledná aktualizácia:** 2025-12-13

