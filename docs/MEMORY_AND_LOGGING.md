# 🧠 Memory and Logging System

**Status:** ✅ Aktívny & Produkčný  
**Verzia:** 2.0.0  
**Posledná aktualizácia:** 2025-12-09

---

## 🎯 Prehľad

Tento dokument popisuje integrovaný systém pamäte a logovania v XVADUR workspace. Systémy sú navzájom prepojené a poskytujú:
1. **Nulovú stratu kontextu** - Všetky interakcie sú automaticky uložené
2. **RAG vyhľadávanie** - Semantic search v histórii
3. **Automatické logovanie** - Triple-write (Markdown + JSONL + SQLite)
4. **Kontinuitu medzi sessionami** - Seamless pokračovanie práce

---

## 🏗️ Architektúra

### 1. MinisterOfMemory System

Systém automaticky zachytáva, ukladá a organizuje všetky interakcie medzi užívateľom (Adam) a AI (xvadur_architect).

#### Core Komponenty (`core/ministers/`)
- **`memory.py`**: Hlavná logika (`MinisterOfMemory`, `AssistantOfMemory`). Riadi ukladanie a formátovanie.
- **`storage.py`**: Implementácia úložiska. Používa `FileStore` pre trvalé ukladanie do JSONL.
- **`sqlite_store.py`**: SQLite backend pre cold storage (archivácia).
- **`__init__.py`**: Exportuje rozhranie pre zvyšok systému.

#### Automatizácia (`scripts/`)
- **`auto_save_prompt.py`**: Skript pre manuálne ukladanie promptov (používa sa pri `/savegame`).
- **`save_conversation_prompts.py`**: Dávkové ukladanie pri `/savegame` - hlavný mechanizmus ukladania promptov.

#### Dáta (`development/data/`)
- **`prompts_log.jsonl`**: Hlavná databáza promptov (append-only JSONL).
- **`archive.db`**: SQLite databáza pre cold storage (archivácia starších záznamov).

---

### 2. Logging System

Logging systém je plne integrovaný s Context Engineering a poskytuje automatické triple-write logovanie do Markdown, JSONL a SQLite formátov.

#### Triple-Write Systém (Hot/Cold Storage)

**Tri formáty súčasne:**
- `development/logs/XVADUR_LOG.md` - Markdown pre človeka (čitateľný formát)
- `development/logs/XVADUR_LOG.jsonl` - JSONL pre AI (token-efektívne načítanie)

**Výhody:**
- Agent načítava len JSONL (rýchlejšie, menej tokenov)
- Človek číta Markdown (prehľadnejšie)
- Automatická synchronizácia oboch formátov

#### Triple-Write Architecture (Hot/Cold Storage)

**Tri úrovne úložiska:**
- **Hot Storage:** `development/logs/XVADUR_LOG.jsonl` (max 100 záznamov) - rýchly prístup
- **Cold Storage:** `development/data/archive.db` (SQLite) - dlhodobá archivácia
- **Markdown:** `development/logs/XVADUR_LOG.md` - čitateľný formát

---

## 🔄 Workflow

### Kompletný Cyklus: LOAD_GAME → WORK → SAVE_GAME

#### 1. Load Game (`/loadgame`) - Načítanie Kontextu

**Účel:** Načíta kontext z predchádzajúcej sessiony pre plynulé pokračovanie.

**Načítava (priorita JSON formáty):**
1. **Save Game:** `SAVE_GAME_LATEST.json` → status, narrative, quests
2. **Log:** `XVADUR_LOG.jsonl` → posledných 5 záznamov (Hot Storage)
3. **XP:** `XVADUR_XP.json` → aktuálny status
4. **Profil:** `xvadur_profile.md` → sekcia "IV. SÚČASNÝ PROFIL" (voliteľné)

**Token Optimalizácia:**
- Pred optimalizáciou: ~7,200 tokenov (Markdown)
- Po optimalizácii (JSON): ~4,350 tokenov
- Redukcia: ~40% tokenov

**Health Check:** Po načítaní overí štruktúru questov a konzistenciu dát.

---

#### 2. Active Workflow (Počas Práce)

**Automatické Logovanie:**

**Pri zadávaní tasku:**
```python
from scripts.utils.log_manager import log_task_started

log_task_started("Implementácia feature X", "Popis úlohy")
```

**Pri dokončení tasku:**
```python
from scripts.utils.log_manager import log_task_completed

log_task_completed(
    task_name="Implementácia feature X",
    files_changed=["file1.py", "file2.py"],
    xp_estimate=5.0,
    completed=["Feature implementovaný", "Testy pridané"],
    results={"status": "success", "test_coverage": "85%"}
)
```

**Triple-Write Systém:**
Každý záznam sa automaticky zapíše do:
- `XVADUR_LOG.md` - Markdown (čitateľný pre človeka)
- `XVADUR_LOG.jsonl` - JSONL (Hot Storage, max 100 záznamov)
- `archive.db` - SQLite (Cold Storage, neobmedzená kapacita)

---

#### 3. Save Game (`/savegame`) - Uloženie Stavu

**Účel:** Zachytiť aktuálny stav konverzácie, gamifikácie a naratívu.

**Postup (v poradí):**

1. **Krok 0: Automatické Uloženie Promptov (POVINNÉ)**
   - Extrakt všetkých user promptov z aktuálnej konverzácie
   - Uloženie cez `scripts/utils/save_conversation_prompts.py`
   - Automatická detekcia duplikátov
   - Uloženie do: `development/data/prompts_log.jsonl`

2. **Krok 0.5: Automatický Výpočet XP (POVINNÉ)**
   - Automaticky parsuje log a prompty
   - Počíta streak, level, XP breakdown
   - Aktualizuje `XVADUR_XP.md` a `XVADUR_XP.json`

3. **Krok 1: Analýza Stavu**
   - Načítať aktuálne hodnoty z XP, Log, Prompts

4. **Krok 2: Vytvorenie Save Game Súborov**
   - `SAVE_GAME_LATEST.json` - hlavný zdroj pravdy (JSON)
   - `SAVE_GAME_LATEST.md` - naratívny formát (Markdown)
   - `SAVE_GAME_LATEST_SUMMARY.md` - kompaktný summary

5. **Krok 3: Git Commit + Push (KRITICKÉ)**
   - Automatický commit a push všetkých zmien

**Poznámka:** Automatické ukladanie pri každej odpovedi bolo odstránené kvôli nestabilite `.cursorrules` mechanizmu. Všetky prompty sa teraz ukladajú pri `/savegame`, čo je spoľahlivejší a kontrolovateľnejší prístup.

---

### Kompletný Cyklus

```
┌─────────────────────────────────────────┐
│ 1. ŠTART SESSION                        │
│    /loadgame                            │
│    ↓                                    │
│    - Načíta Save Game (JSON priorita)   │
│    - Načíta posledných 5 log záznamov   │
│    - Načíta XP status                   │
│    - Health Check                       │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│ 2. AKTÍVNA PRÁCA                        │
│    Počas práce:                         │
│    ↓                                    │
│    - log_task_started()                 │
│    - [práca na úlohe]                   │
│    - log_task_completed()               │
│    ↓                                    │
│    Triple-write:                        │
│    - XVADUR_LOG.md                      │
│    - XVADUR_LOG.jsonl (Hot Storage)     │
│    - archive.db (Cold Storage)          │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│ 3. KONIEC SESSION                       │
│    /savegame                            │
│    ↓                                    │
│    Krok 0: Uložiť prompty               │
│    Krok 0.5: Vypočítať XP               │
│    Krok 1: Analyzovať stav              │
│    Krok 2: Vytvoriť Save Game           │
│    Krok 3: Git commit + push            │
└─────────────────────────────────────────┘
```

**Detailný popis:** Pozri [`SYSTEM_AUDIT.md`](SYSTEM_AUDIT.md#-kompletný-workflow-od-cursorrules-po-saveload-game)

---

## 📊 Formáty a Štruktúra

### Prompt Formát (`prompts_log.jsonl`)

```json
{
  "timestamp": "2025-12-09T06:05:00+01:00",
  "role": "user",
  "content": "Môj prompt...",
  "session_id": "2025-12-09",
  "source": "savegame",
  "metadata": {
    "xp": 2.5,
    "word_count": 150
  }
}
```

### Log Formát (Markdown - `XVADUR_LOG.md`)

```markdown
[HH:MM] 🔹 Task: Názov tasku
  - *Zmenené súbory:*
    - file1.py
    - file2.py
  - *Status:* completed
  - *XP:* 5.0
```

### Log Formát (JSONL - `XVADUR_LOG.jsonl`)

```json
{
  "timestamp": "2025-12-09T04:41:55.695441",
  "date": "2025-12-09",
  "time": "04:41",
  "title": "Task: Názov tasku",
  "type": "task",
  "status": "completed",
  "files_changed": ["file1.py", "file2.py"],
  "xp_estimate": 5.0,
  "completed": ["Feature implementovaný"],
  "results": {
    "status": "success",
    "token_metrics": {
      "token_count": 150,
      "context_window_size": 16000
    }
  }
}
```

---

## 🔧 Context Engineering Integrácia

### Token Tracking

Každý log záznam automaticky trackuje tokeny:
- Odhad tokenov pre záznam
- Utilization ratio
- Token metrics v results

### Optimalizované Načítanie

**Použitie v `/loadgame`:**
```python
from scripts.utils.log_manager import get_optimized_log_context

# Načíta posledných 5 záznamov s automatickou optimalizáciou
context = get_optimized_log_context(limit=5, use_compression=True)

# Vráti:
# - entries: List[Dict] - optimalizované záznamy
# - token_metrics: TokenMetrics - metriky tokenov
# - utilization: float - utilization ratio
# - optimized: bool - či bola aplikovaná kompresia
```

**Automatická kompresia:**
- Ak utilization > threshold (default 80%), automaticky komprimuje
- Zostane len najnovší a najdôležitejší obsah
- Zachová sa token budget

### Izolácia Kontextu

Pre task-specific kontext:
- Filtrovanie podľa kľúčových slov
- Relevantné záznamy pre úlohu
- Optimalizácia tokenov

```python
from core.context_engineering.isolate_context import IsolateContextManager

isolator = IsolateContextManager(store)
result = isolator.isolate_context_for_task(
    task_id="quest-20",
    task_description="Implementovať Context Engineering",
    keywords={"context", "engineering", "token"},
    limit=20
)
```

---

## 📖 Použitie v Kóde

### Základné Logovanie

```python
from scripts.utils.log_manager import add_log_entry

add_log_entry(
    action_name="Názov akcie",
    status="completed",
    files_changed=["file.py"],
    xp_estimate=2.0,
    entry_type="task"
)
```

### Automatické Logovanie Taskov

```python
from scripts.utils.log_manager import log_task_started, log_task_completed

# Začiatok tasku
log_task_started("Implementácia feature", "Popis úlohy")

# ... práca ...

# Dokončenie tasku
log_task_completed(
    "Implementácia feature",
    files_changed=["feature.py"],
    xp_estimate=5.0
)
```

### Optimalizované Načítanie

```python
from scripts.utils.log_manager import get_optimized_log_context

# Načíta optimalizovaný kontext
context = get_optimized_log_context(limit=5, use_compression=True)

# Použiť v loadgame
for entry in context['entries']:
    print(f"[{entry['time']}] {entry['title']}")
```

### MinisterOfMemory Použitie

```python
from core.ministers.memory import MinisterOfMemory, AssistantOfMemory
from core.ministers.storage import FileStore
from pathlib import Path

store = FileStore(Path("development/data/prompts_log.jsonl"))
assistant = AssistantOfMemory(store=store)
minister = MinisterOfMemory(assistant=assistant)

# Log event
minister.log_event("user", "Môj prompt...")

# Review context
recent_prompts = minister.review_context(limit=20)
```

---

## 🔄 Integrácia s `/loadgame` a `/savegame`

### `/loadgame` Command

Používa optimalizované načítanie:
- Načíta posledných 5 záznamov z JSONL (nie MD)
- Automatická kompresia ak je utilization vysoká
- Token tracking a metriky
- Načíta posledné prompty z `prompts_log.jsonl` cez MinisterOfMemory

### `/savegame` Command

- Prompty sa ukladajú len pri savegame (nie pri každom tasku)
- Automatické logovanie do logu pri vytvorení save game
- Triple-write (Markdown + JSONL + SQLite)
- Archivácia starších záznamov do cold storage

---

## ⚙️ Konfigurácia

Konfigurácia je v `development/data/context_engineering_config.json`:

```json
{
  "compression": {
    "threshold": 0.8,
    "target_ratio": 0.5
  },
  "token_budget": {
    "context_window_size": 16000
  },
  "storage": {
    "hot_storage_limit": 100,
    "cold_storage_enabled": true
  }
}
```

---

## 📊 Dáta a Metriky

Systém sleduje nielen text, ale aj metadáta:
- **Timestamp:** Kedy bol prompt/záznam vytvorený
- **Session ID:** Ku ktorej session patrí
- **Source:** Odkiaľ prišiel (auto-save vs batch)
- **XP:** Automatický výpočet XP za aktivitu
- **Token Metrics:** Tracking tokenovej spotreby

---

## ✅ Výhody

1. **Token Efektívnosť:** Agent načítava len JSONL (menej tokenov)
2. **Čitateľnosť:** Človek číta Markdown (prehľadnejšie)
3. **Automatizácia:** Triple-write automaticky synchronizuje všetky tri formáty (MD + JSONL + SQLite)
4. **Optimalizácia:** Context Engineering automaticky optimalizuje tokeny
5. **Kompresia:** Automatická kompresia pri vysokom utilization
6. **Hot/Cold Storage:** Efektívne využitie úložiska (rýchly prístup + archivácia)

---

## 🛠️ Údržba a Čistenie

V minulosti existovali alternatívne prístupy (background tracker, file watcher), ktoré boli **odstránené** v prospech robustného riešenia.

**Zastaralé (Odstránené):**
- `scripts/conversation_tracker.py`
- `scripts/conversation_watcher.py`

Súčasný systém je **pasívny, bezúdržbový a plne automatizovaný**.

---

## 🔗 Súvisiace Dokumenty

- **`docs/README.md`**: Hlavný rozcestník dokumentácie
- **`docs/ARCHITECTURE.md`**: Detailný popis v2.0 architektúry
- **`docs/CONTEXT_ENGINEERING.md`**: Context Engineering integrácia
- **`.cursor/commands/loadgame.md`**: `/loadgame` command dokumentácia
- **`.cursor/commands/savegame.md`**: `/savegame` command dokumentácia

---

## 🚀 Budúce Rozšírenia

- [ ] Session log automatické vytváranie pri každej session
- [ ] RAG integrácia pre inteligentné vyhľadávanie v logu
- [ ] Automatické sumarizovanie starých záznamov
- [ ] Export do Obsidian formátu
- [ ] Real-time sync medzi hot a cold storage

