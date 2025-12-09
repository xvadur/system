# Logging System - Aktuálny Stav

## Prehľad

Logging systém je teraz plne integrovaný s Context Engineering a poskytuje automatické dual-write logovanie do Markdown aj JSONL formátov.

## Architektúra

### Dual-Write Systém

**Dva formáty súčasne:**
- `XVADUR_LOG.md` - Markdown pre človeka (čitateľný formát)
- `XVADUR_LOG.jsonl` - JSON pre AI (token-efektívne načítanie)

**Výhody:**
- Agent načítava len JSONL (rýchlejšie, menej tokenov)
- Človek číta Markdown (prehľadnejšie)
- Automatická synchronizácia oboch formátov

### Automatické Logovanie

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

## Context Engineering Integrácia

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

## Workflow Integrácia

### `.cursorrules` - Automatické Logovanie

```markdown
## 4. WORKFLOW
- **ACTIVE LOGGING:** Automaticky loguj pri každom zadávaní a dokončení tasku:
  - Pri zadávaní tasku: `log_task_started(task_name, description)`
  - Pri dokončení tasku: `log_task_completed(task_name, files_changed, xp_estimate)`
  - Dual-write: Automaticky zapisuje do `XVADUR_LOG.md` aj `XVADUR_LOG.jsonl`
```

### `/loadgame` Command

Používa optimalizované načítanie logu:
- Načíta posledných 5 záznamov z JSONL (nie MD)
- Automatická kompresia ak je utilization vysoká
- Token tracking a metriky

### `/savegame` Command

- Prompty sa ukladajú len pri savegame (nie pri každom tasku)
- Automatické logovanie do logu pri vytvorení save game

## Formát Záznamov

### Markdown Formát (`XVADUR_LOG.md`)

```markdown
[HH:MM] 🔹 Task: Názov tasku
  - *Zmenené súbory:*
    - file1.py
    - file2.py
  - *Status:* completed
  - *XP:* 5.0
```

### JSONL Formát (`XVADUR_LOG.jsonl`)

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

## Session Log

Session logy sú uložené v:
- `development/sessions/current/` - aktuálne sessiony
- Formát: `session_DD-MM-YYYY.md`

**Automatické vytváranie:**
- Cez `scripts/create_new_session.py`
- Automaticky loguje vytvorenie session cez `log_manager`

## Použitie v Kóde

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

## Integrácia s Context Engineering

### Token Tracking

Každý záznam automaticky trackuje tokeny:
- Odhad tokenov pre záznam
- Utilization ratio
- Token metrics v results

### Kompresia

Automatická kompresia pri vysokom utilization:
- Threshold: 80% (konfigurovateľné)
- Zostane len najnovší a najdôležitejší obsah
- Zachová sa token budget

### Izolácia

Pre task-specific kontext:
- Filtrovanie podľa kľúčových slov
- Relevantné záznamy pre úlohu
- Optimalizácia tokenov

## Konfigurácia

Konfigurácia je v `development/data/context_engineering_config.json`:

```json
{
  "compression": {
    "threshold": 0.8,
    "target_ratio": 0.5
  },
  "token_budget": {
    "context_window_size": 16000
  }
}
```

## Výhody

1. **Token Efektívnosť:** Agent načítava len JSONL (menej tokenov)
2. **Čitateľnosť:** Človek číta Markdown (prehľadnejšie)
3. **Automatizácia:** Dual-write automaticky synchronizuje oba formáty
4. **Optimalizácia:** Context Engineering automaticky optimalizuje tokeny
5. **Kompresia:** Automatická kompresia pri vysokom utilization

## Budúce Rozšírenia

- [ ] Session log automatické vytváranie pri každej session
- [ ] RAG integrácia pre inteligentné vyhľadávanie v logu
- [ ] Automatické sumarizovanie starých záznamov
- [ ] Export do Obsidian formátu

