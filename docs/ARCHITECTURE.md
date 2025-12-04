# 🏗️ XVADUR Architektúra

**Verzia:** 2.0.0  
**Posledná aktualizácia:** 2025-12-04

---

## Prehľad

XVADUR je modulárny kognitívny systém navrhnutý pre:
1. **Pamäť** - Automatické ukladanie a vyhľadávanie v histórii
2. **Analýza** - RAG-based semantic search
3. **Gamifikácia** - XP/Level systém pre tracking progresu
4. **Automatizácia** - GitHub Actions pre denné/týždenné úlohy

---

## Vrstvy Systému

```
┌─────────────────────────────────────────────────────┐
│                  Cursor IDE Layer                   │
│  (/loadgame, /savegame, .cursorrules, AI Agent)     │
├─────────────────────────────────────────────────────┤
│                  Core Layer (Python)                │
│  ┌─────────────┬─────────────┬─────────────┐       │
│  │  ministers  │     rag     │     xp      │       │
│  │  (Memory)   │  (Search)   │   (Game)    │       │
│  └─────────────┴─────────────┴─────────────┘       │
├─────────────────────────────────────────────────────┤
│                  Data Layer (JSONL)                 │
│  conversations.jsonl | prompts_log.jsonl | xp.jsonl│
├─────────────────────────────────────────────────────┤
│              Automation Layer (GitHub)              │
│     daily-metrics | weekly-synthesis | backup       │
└─────────────────────────────────────────────────────┘
```

---

## Core Moduly

### 1. Ministers (`core/ministers/`)

**Účel:** Memory management a persistence

**Komponenty:**
- `MinisterOfMemory` - Orchestrácia pamäťových operácií
- `AssistantOfMemory` - Taktické operácie (ingest, recall)
- `MemoryRecord` - Dátový model pre pamäťové jednotky
- `FileStore` - JSONL persistence

**Dátový tok:**
```
User Prompt → .cursorrules → auto_save_prompt.py → FileStore → prompts_log.jsonl
```

### 2. RAG (`core/rag/`)

**Účel:** Semantic search v histórii

**Komponenty:**
- `build_index.py` - Vytvorenie FAISS indexu
- `search.py` - Hybrid search (semantic + keyword)

**Technológie:**
- OpenAI Embeddings (`text-embedding-3-small`)
- FAISS (Facebook AI Similarity Search)
- TF-IDF pre keyword matching

**Konfigurácia:**
- `INCLUDE_AI_RESPONSES` - Zahrnutie AI odpovedí
- `COMBINE_PAIRS` - Kombinovanie prompt + response

### 3. XP (`core/xp/`)

**Účel:** Gamifikácia a progress tracking

**Level systém:**
| Level | Názov | XP Potrebné |
|-------|-------|-------------|
| 1 | Novice | 0 |
| 2 | Apprentice | 50 |
| 3 | Journeyman | 150 |
| 4 | Craftsman | 350 |
| 5 | Expert | 750 |
| 6 | Master | 1,550 |
| 7 | Architect | 3,150 |

**XP Zdroje:**
- Log entries: 0.5 XP
- File changes: 0.1 XP
- Completed tasks: 0.5 XP
- Prompts: 0.1 XP
- Words (per 1000): 0.5 XP

---

## Dátové Štruktúry

### conversations.jsonl
```json
{
  "session": "session_id",
  "timestamp": "2025-12-04T12:00:00+01:00",
  "user": "User prompt text...",
  "assistant": "AI response text..."
}
```

### prompts_log.jsonl
```json
{
  "timestamp": "2025-12-04T12:00:00+01:00",
  "role": "user",
  "content": "Prompt text...",
  "metadata": {
    "source": "auto_save",
    "extraction_method": "real_time_agent_hook"
  }
}
```

### xp_history.jsonl
```json
{
  "timestamp": "2025-12-04T12:00:00+01:00",
  "total_xp": 159.78,
  "current_level": 5,
  "breakdown": {
    "from_log": 145.6,
    "from_prompts": 9.58,
    "bonuses": 4.6
  }
}
```

---

## GitHub Actions

### daily-metrics.yml
- **Trigger:** Cron (23:59 UTC)
- **Akcie:** Výpočet XP, update grafov, commit

### weekly-synthesis.yml
- **Trigger:** Cron (nedeľa 23:00 UTC)
- **Akcie:** Agregácia týždenných metrík, vytvorenie reportu

### backup.yml
- **Trigger:** Push do main
- **Akcie:** Validácia JSONL súborov, integrity check

---

## Cursor Integrácia

### .cursorrules
Systémový prompt, ktorý:
1. Automaticky ukladá user prompty
2. Definuje agent personu
3. Riadi workflow (loadgame/savegame)

### Commands
- `/loadgame` - Hierarchické načítanie kontextu
- `/savegame` - Uloženie + batch prompt save + git push

---

## Migrácia z Pilot v1.0

**Zmeny:**
1. Nová adresárová štruktúra (`core/`, `data/`, `sessions/`)
2. Modulárny Python package (`core/__init__.py`)
3. GitHub Actions automatizácie
4. Zjednodušené dátové úložisko (Single Source of Truth)

**Zachované:**
- MinisterOfMemory logika
- RAG systém
- XP kalkulátor
- Cursor commands

**Archivované:**
- Historické prompty (664 súborov)
- Kortex skripty
- Duplicates skripty
- Synthesis súbory

---

## Ďalší Rozvoj

1. **RAG Rebuild** - Dokončiť po doplnení OpenAI kreditu
2. **XP v2.0** - Implementovať nový level systém
3. **Weekly Reports** - Automatické syntézy
4. **Dashboard** - HTML vizualizácia metrík

---

**Vytvorené:** 2025-12-04  
**Autor:** xvadur_architect

