# 📜 Scripts Directory

Organizované skripty pre XVADUR workspace.

---

## 📂 Štruktúra

```
scripts/
├── utils/                  # Utility skripty (log manager, git helpers, validácie)
├── analysis/               # Analýzy promptov (metriky, témy, depresia)
├── synthesis/              # Syntézy (chronológie, príbehy)
├── youtube/                # YouTube processing (transcripty, konverzia)
├── local_scheduler/        # Lokálny scheduler konfigurácia
│
├── auto_archive_session.py      # Automatická archivácia session
├── auto_save_prompt.py          # Legacy - už sa nepoužíva (prompty sa ukladajú pri /savegame)
├── calculate_daily_metrics.py   # Denné metriky
├── create_new_session.py        # Vytvorenie novej session
├── daily_rotation.py            # Denný rotation workflow
├── generate_daily_review.py     # Generovanie denného review
├── generate_savegame_json.py    # Generovanie save game JSON
└── migrate_to_structured_format.py  # Migrácia do štruktúrovaného formátu
```

---

## 🚀 Aktívne Používané Skripty

### Session Management
- **`create_new_session.py`**: Vytváranie nových denných sessions
- **`auto_archive_session.py`**: Automatická archivácia sessions
- **`daily_rotation.py`**: Denný rotation workflow (merguje branches, vytvára nové sessiony)
- **`generate_daily_review.py`**: Generovanie denného review s analýzou

### Save Game & Logging
- **`generate_savegame_json.py`**: Generovanie save game JSON súboru
- **`auto_save_prompt.py`**: Manuálne ukladanie promptov (legacy - používa sa pri `/savegame`)

### Metriky
- **`calculate_daily_metrics.py`**: Výpočet denných metrík

---

## 🛠️ Utility Skripty (`utils/`)

### Log Management
- **`log_manager.py`**: Dual-write logovanie (Markdown + JSONL), automatické logovanie taskov

### Git & GitHub
- **`git_helper.py`**: Git operácie helpers
- **`cleanup_branches.py`**: Vyčistenie starých branches

### Validation & Testing
- **`validate_quest.py`**: Validácia quest štruktúry
- **`validate_schemas.py`**: Validácia JSON/JSONL schém
- **`test_context_engineering.py`**: Testovanie Context Engineering komponentov

### Context & Memory
- **`load_context_optimized.py`**: Optimalizované načítanie kontextu pre `/loadgame`
- **`export_to_log.py`**: Export dát do logu
- **`migrate_to_sqlite.py`**: Migrácia do SQLite cold storage
- **`migrate_prompts_log.py`**: Migrácia prompts log

### Analysis & Metrics
- **`metrics_tracker.py`**: Tracking metrík
- **`analyze_day_founder_style.py`**: Analýza v štýle founder
- **`xvadur_visualizations.py`**: XP vizualizácie
- **`xvadur_backlinking.py`**: Backlinking pre session dokumenty

### Data Processing
- **`merge_prompt_metadata.py`**: Merge prompt metadát
- **`prepare_openai_finetuning.py`**: Príprava dát pre OpenAI finetuning
- **`save_conversation_prompts.py`**: Batch ukladanie konverzačných promptov (používa sa pri `/savegame`)

---

## 📋 Kategórie

### Analysis (`archive/scripts/analysis/`)
Skripty pre analýzu promptov - metriky, témy, depresia, vizualizácie.
**Status:** Archivované - používali zastarané cesty `xvadur/data/`

### Synthesis (`synthesis/`)
Skripty pre syntézu dát - chronológie, príbehy, analýzy.

### YouTube (`youtube/`)
Skripty pre prácu s YouTube dátami - konverzia transcriptov, processing.

### Local Scheduler (`local_scheduler/`)
Konfigurácia lokálneho scheduler systému (namiesto GitHub Actions).

---

## 🔗 Integrácia s Core

### Používanie Core Modulov

Skripty by mali používať core moduly namiesto duplicitnej logiky:

```python
# ✅ SPRÁVNE - používa core modul
from core.xp.calculator import calculate_xp, update_xp_file

# ❌ ZLE - duplicitná logika v scripts/
from scripts.calculate_xp import calculate_xp
```

**Core moduly:**
- `core.xp.calculator` - XP výpočty
- `core.rag.*` - RAG funkcionalita
- `core.ministers.*` - Memory systém
- `core.context_engineering.*` - Context Engineering

---

## 📝 Poznámky

- **Duplicitné skripty:** RAG skripty (`scripts/rag/`) sú duplicitné s `core/rag/` - používa sa `core/rag/`
- **XP výpočet:** Používa sa `core.xp.calculator` namiesto `scripts/calculate_xp.py`
- **Legacy skripty:** Niektoré skripty v `analysis/` sú historické a môžu byť archivované

---

**Posledná aktualizácia:** 2025-12-09 (Workspace Refactoring)
