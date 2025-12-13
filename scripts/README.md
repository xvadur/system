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
├── create_new_session.py        # Vytvorenie novej session
├── daily_rotation.py            # Denný rotation workflow
├── generate_daily_review.py     # Generovanie denného review (voliteľné)
└── generate_savegame_json.py    # Generovanie save game JSON
```

---

## 🚀 Aktívne Používané Skripty

### Session Management
- **`create_new_session.py`**: Vytváranie nových denných sessions
- **`auto_archive_session.py`**: Automatická archivácia sessions
- **`daily_rotation.py`**: Denný rotation workflow (merguje branches, vytvára nové sessiony)
- **`generate_daily_review.py`**: Generovanie denného review s analýzou

### Save Game
- **`generate_savegame_json.py`**: Generovanie save game JSON súboru z Markdown

---

## 🛠️ Utility Skripty (`utils/`)

**Poznámka:** Niektoré utility skripty používajú odstránené moduly (`core/ministers/`, `core/context_engineering/`) a môžu vyžadovať úpravu alebo sú deprecated.

### Git & GitHub
- **`git_helper.py`**: Git operácie helpers
- **`cleanup_branches.py`**: Vyčistenie starých branches

### Validation & Testing
- **`validate_quest.py`**: Validácia quest štruktúry
- **`validate_schemas.py`**: Validácia JSON/JSONL schém
- **`test_context_engineering.py`**: Testovanie Context Engineering komponentov

### Context & Memory (Deprecated)
- **`load_context_optimized.py`**: ⚠️ Deprecated - používa odstránené moduly
- **`export_to_log.py`**: ⚠️ Deprecated - používa odstránené moduly
- **`migrate_to_sqlite.py`**: ⚠️ Deprecated - používa odstránené moduly
- **`migrate_prompts_log.py`**: ⚠️ Deprecated - používa odstránené moduly

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
- `core.xp.calculator` - XP výpočty (manuálne použitie)

---

## 📝 Poznámky

- **Zjednodušený systém:** Odstránené moduly `core/ministers/`, `core/context_engineering/`, triple-write logging
- **XP výpočet:** Používa sa `core.xp.calculator` (manuálne použitie, nie automatizácia)
- **Legacy skripty:** Niektoré utility skripty používajú odstránené moduly a sú deprecated
- **Session management:** Jednoduchý workflow - `session.md` + `savegame.json`

---

**Posledná aktualizácia:** 2025-12-10 (System Simplification)
