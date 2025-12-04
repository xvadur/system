# 🧠 MinisterOfMemory Systém

**Status:** ✅ Aktívny & Produkčný  
**Typ:** Automatizovaný pamäťový systém  
**Core Komponent:** `ministers.memory`

---

## 🎯 Účel
Systém automaticky zachytáva, ukladá a organizuje všetky interakcie medzi užívateľom (Adam) a AI (xvadur_architect). Slúži ako "dlhodobá pamäť" projektu, ktorá umožňuje:
1. **Nulovú stratu kontextu** (všetko sa ukladá).
2. **RAG vyhľadávanie** v histórii.
3. **Analýzu a metriky** (Human 3.0 evaluácia).
4. **Kontinuitu** medzi sessionami.

---

## 🏗️ Architektúra

Systém je postavený na modulárnej architektúre `ministers` balíčka.

### 1. Core Komponenty (`ministers/`)
- **`memory.py`**: Hlavná logika (`MinisterOfMemory`, `AssistantOfMemory`). Riadi ukladanie a formátovanie.
- **`storage.py`**: Implementácia úložiska. Používa `FileStore` pre trvalé ukladanie do JSONL.
- **`__init__.py`**: Exportuje rozhranie pre zvyšok systému.

### 2. Automatizácia (`scripts/`)
- **`auto_save_prompt.py`**: Skript volaný priamo z `.cursorrules`. Pri každej odpovedi AI automaticky uloží prompt.
- **`save_conversation_prompts.py`**: Dávkové ukladanie pri `/savegame` (backup).

### 3. Dáta (`xvadur/data/`)
- **`prompts_log.jsonl`**: Hlavná databáza promptov (append-only JSONL).
- **`dataset/`**: Vyčistené a dedupikované dáta pre analýzu/RAG.

---

## 🔄 Workflow

### A. Real-time Ukladanie (Primárny tok)
1. Užívateľ napíše prompt.
2. Cursor AI generuje odpoveď.
3. **Pred odpoveďou** `.cursorrules` automaticky spustí `scripts/auto_save_prompt.py`.
4. Prompt sa uloží do `xvadur/data/prompts_log.jsonl`.

### B. Batch Backup (Sekundárny tok)
1. Užívateľ spustí `/savegame`.
2. Systém spustí `scripts/save_conversation_prompts.py`.
3. Uložia sa všetky prompty z aktuálnej konverzácie (s detekciou duplikátov).

---

## 📊 Dáta a Metriky

Systém sleduje nielen text, ale aj metadáta:
- **Timestamp:** Kedy bol prompt vytvorený.
- **Session ID:** Ku ktorej session patrí.
- **Source:** Odkiaľ prišiel (auto-save vs batch).
- **XP:** Automatický výpočet XP za aktivitu.

---

## 🛠️ Údržba a Čistenie

V minulosti existovali alternatívne prístupy (background tracker, file watcher), ktoré boli **odstránené** v prospech robustného riešenia cez `.cursorrules`.

**Zastaralé (Odstránené):**
- `scripts/conversation_tracker.py`
- `scripts/conversation_watcher.py`
- `xvadur/config/conversation_tracker_config.json`

Súčasný systém je **pasívny, bezúdržbový a plne automatizovaný**.

---

## 🔗 Súvisiace Dokumenty
- **`xvadur/data/kortex_analysis/KORTEX_ANALYSIS.md`**: Analýza historických dát.
- **`xvadur/docs/README.md`**: Hlavný rozcestník dokumentácie.

