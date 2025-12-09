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
┌─────────────────────────────────────────────────────────────┐
│                      Cursor IDE Layer                       │
│      (/loadgame, /savegame, .cursorrules, AI Agent)         │
├─────────────────────────────────────────────────────────────┤
│         Development / Staging / Production Layers           │
│ (Session Management, Automatizácia, Denný Review)           │
├─────────────────────────────────────────────────────────────┤
│                      Core Layer (Python)                    │
│      ┌─────────────┬─────────────┬─────────────┐           │
│      │  ministers  │     rag     │     xp      │           │
│      │  (Memory)   │  (Search)   │   (Game)    │           │
│      └─────────────┴─────────────┴─────────────┘           │
├─────────────────────────────────────────────────────────────┤
│                      Data Layer (JSONL)                     │
│ conversations.jsonl | prompts_log.jsonl | xp_history.jsonl  │
├─────────────────────────────────────────────────────────────┤
│                  Automation Layer (GitHub)                  │
│     daily-metrics | weekly-synthesis | session-rotation     │
└─────────────────────────────────────────────────────────────┘
```

---

## Core Moduly

### 🧠 `core/ministers` (Memory)

- **Účel:** Správa pamäte a ukladanie dát.

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
  "user_prompt": {
    "extracted_text": "User prompt text..."
  },
  "ai_response": {
    "extracted_text": "AI response text..."
  }
}
```
**Poznámka:** Tento súbor môže neexistovať (legacy formát). Aktuálne sa používa `prompts_log.jsonl` pre ukladanie promptov.

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

### XVADUR_LOG.jsonl
```json
{
  "timestamp": "2025-12-08T01:15:00+01:00",
  "date": "2025-12-08",
  "time": "01:15",
  "title": "Quest #13: Dual-write systém implementovaný",
  "type": "task",
  "status": "completed",
  "files_changed": ["development/logs/XVADUR_LOG.jsonl", "scripts/utils/log_manager.py"],
  "xp_estimate": 2.0,
  "completed": ["Vytvorený XVADUR_LOG.jsonl", "Rozšírený log_manager.py"],
  "results": {"md_write": "OK", "jsonl_write": "OK"},
  "decisions": [],
  "quest_id": 13,
  "xp_earned": 2.0,
  "notes": "Scheduler nie je nainštalovaný!"
}
```
**Poznámka:** Dual-write systém zapisuje súčasne do `XVADUR_LOG.md` (Markdown) a `XVADUR_LOG.jsonl` (JSON). Voliteľné polia: `files_changed`, `xp_estimate`, `completed`, `results`, `decisions`, `quest_id`, `xp_earned`, `notes`.

### xp_history.jsonl
```json
{
  "timestamp": "2025-12-04T12:00:00+01:00",
  "total_xp": 159.78,
  "level": 5,
  "next_level_xp": 200,
  "xp_needed": 40.22,
  "streak_days": 3,
  "breakdown": {
    "from_work": {
      "entries": {"count": 29, "xp": 14.5},
      "files": {"count": 61, "xp": 6.1},
      "tasks": {"count": 250, "xp": 125.0},
      "total": 145.6
    },
    "from_activity": {
      "prompts": {"count": 80, "xp": 8.0},
      "words": {"count": 3163, "xp": 1.58},
      "total": 9.58
    },
    "bonuses": {
      "streak": {"days": 3, "xp": 0.6},
      "sessions": {"count": 4, "xp": 4.0},
      "total": 4.6
    }
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

## Quest System (Anthropic Harness Pattern)

**Verzia:** 2.1.0 (2025-12-09)

Implementácia Anthropic best practices pre long-running agents.

### Quest Schema

```json
{
  "id": "quest-15",
  "title": "Quest #15: ...",
  "status": "in_progress",
  "passes": false,
  "validation": {
    "criteria": [
      "Kritérium 1 splnené",
      "Kritérium 2 splnené"
    ],
    "last_tested": "2025-12-09T03:00:00Z"
  },
  "next_steps": [...],
  "blockers": []
}
```

### Anthropic Pattern Fields

| Field | Typ | Popis |
|-------|-----|-------|
| `passes` | boolean | Či quest spĺňa všetky kritériá |
| `validation.criteria` | array | Zoznam kritérií (Definition of Done) |
| `validation.last_tested` | string | ISO timestamp poslednej validácie |

### Workflow

1. **Health Check** (`/loadgame`):
   - Overenie štruktúry questov
   - Kontrola konzistencie `passes` vs `status`
   
2. **Validácia** (`/savegame`):
   - Pre každý quest over kritériá
   - Aktualizuj `passes` a `last_tested`

3. **Nástroje:**
   - `scripts/utils/validate_quest.py --health-check`
   - `scripts/utils/validate_quest.py --list`
   - `scripts/utils/validate_quest.py --quest quest-15`

### Dokumentácia

- **Zdroj:** [Anthropic Engineering - Effective Harnesses](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)
- **Analýza:** `development/sessions/current/analysis_nate_jones_calibration.md`

---

## Ďalší Rozvoj

1. **RAG Rebuild** - Dokončiť po doplnení OpenAI kreditu
2. **XP v2.0** - Implementovať nový level systém
3. **Weekly Reports** - Automatické syntézy
4. **Dashboard** - HTML vizualizácia metrík
5. **Quest Automation** - Automatické testovanie kritérií questov

---

**Vytvorené:** 2025-12-04  
**Autor:** xvadur_architect

