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
- **`auto_save_prompt.py`**: Skript pre manuálne ukladanie promptov (používa sa pri `/savegame`).
- **`save_conversation_prompts.py`**: Dávkové ukladanie pri `/savegame` - hlavný mechanizmus ukladania promptov.

### 3. Dáta (`development/data/`)
- **`prompts_log.jsonl`**: Hlavná databáza promptov (append-only JSONL).
- **`dataset/`**: Vyčistené a dedupikované dáta pre analýzu/RAG (ak existuje).

---

## 🔄 Workflow

### A. Ukladanie pri Savegame (Primárny tok)
1. Užívateľ spustí `/savegame`.
2. Systém spustí `scripts/save_conversation_prompts.py`.
3. Uložia sa všetky prompty z aktuálnej konverzácie (s detekciou duplikátov) do `development/data/prompts_log.jsonl`.

**Poznámka:** Automatické ukladanie pri každej odpovedi bolo odstránené kvôli nestabilite `.cursorrules` mechanizmu. Všetky prompty sa teraz ukladajú pri `/savegame`, čo je spoľahlivejší a kontrolovateľnejší prístup.

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
- **`docs/README.md`**: Hlavný rozcestník dokumentácie.
- **`docs/ARCHITECTURE.md`**: Detailný popis v2.0 architektúry.

