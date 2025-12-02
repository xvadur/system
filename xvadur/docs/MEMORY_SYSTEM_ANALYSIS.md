# Analýza Memory Systému - Čo je Potrebné?

## 📊 Aktuálny Stav

Máme **dva spôsoby** ukladania promptov:
1. **Automatické cez `.cursorrules`** (nové, primárne) - ukladá prompty v reálnom čase
2. **Background tracker** (staré, alternatíva) - sleduje Cursor súbory a extrahuje prompty

## ✅ POTREBNÉ (Používa sa v `.cursorrules`)

### Kritické súbory:
- ✅ `scripts/auto_save_prompt.py` - **POTREBNÉ** - používa sa v `.cursorrules`
- ✅ `ministers/storage.py` - **POTREBNÉ** - FileStore implementácia
- ✅ `ministers/memory.py` - **POTREBNÉ** - MinisterOfMemory systém
- ✅ `ministers/__init__.py` - **POTREBNÉ** - package exports

### Dôvod:
Tieto súbory sú **kritické** pre automatické ukladanie cez `.cursorrules`. Bez nich systém nefunguje.

---

## 🔄 VOLITEĽNÉ (Môže byť užitočné)

### Export a Metriky:
- ⚠️ `scripts/export_to_log.py` - **VOLITEĽNÉ** - export promptov do markdown
- ⚠️ `scripts/metrics_tracker.py` - **VOLITEĽNÉ** - tracking metrík (word count, sentiment)
- ⚠️ `.vscode/tasks.json` - **VOLITEĽNÉ** - VS Code tasks (môže byť užitočné)

### Dôvod:
Tieto súbory nie sú kritické, ale môžu byť užitočné pre:
- Export promptov do `XVADUR_LOG.md`
- Analýzu metrík (počet slov, sentiment, XP odhad)
- Manuálne spustenie úloh

---

## ❌ NEPOTREBNÉ (Ak ukladáme cez `.cursorrules`)

### Background Tracker Systém:
- ❌ `scripts/conversation_tracker.py` - **NEPOTREBNÉ** - background service
- ❌ `scripts/conversation_watcher.py` - **NEPOTREBNÉ** - file watcher
- ❌ `scripts/cursor_prompt_extractor.py` - **NEPOTREBNÉ** - extrakcia z Cursor súborov
- ❌ `xvadur/config/conversation_tracker_config.json` - **NEPOTREBNÉ** - konfigurácia trackeru

### Dôvod:
Tieto súbory boli vytvorené pre **pasívne zachytávanie** promptov z Cursor súborov. Keďže teraz ukladáme prompty **priamo v reálnom čase** cez `.cursorrules`, tento systém nie je potrebný.

### Výnimka:
Môžeš ich **ponechať ako backup/alternatívu**, ak:
- Chceš mať duplicitné riešenie (ak `.cursorrules` zlyhá)
- Chceš extrahovať staré prompty z Cursor súborov
- Chceš sledovať zmeny v Cursor súboroch

---

## 📦 ZÁVISLOSTI

### Potrebné:
- ✅ Všetky built-in Python moduly (json, pathlib, datetime, atď.)

### Nepotrebné (ak odstrániš tracker):
- ❌ `watchdog>=3.0.0` - **NEPOTREBNÉ** - používa sa len v file watcheri

---

## 🎯 Odporúčanie

### Možnosť 1: Minimálna verzia (odstrániť tracker)
**Odstrániť:**
- `scripts/conversation_tracker.py`
- `scripts/conversation_watcher.py`
- `scripts/cursor_prompt_extractor.py`
- `xvadur/config/conversation_tracker_config.json`
- Tasks v `.vscode/tasks.json` (tracker-related)
- `watchdog` z `requirements.txt`

**Ponechať:**
- `scripts/auto_save_prompt.py` ✅
- `ministers/*` ✅
- `scripts/export_to_log.py` ⚠️ (užitočné)
- `scripts/metrics_tracker.py` ⚠️ (užitočné)

### Možnosť 2: Hybrid verzia (ponechať ako backup)
**Ponechať všetko:**
- Automatické ukladanie cez `.cursorrules` (primárne)
- Background tracker (backup/alternatíva)
- Export a metriky (užitočné nástroje)

**Výhody:**
- Duplicitné riešenie (ak `.cursorrules` zlyhá)
- Možnosť extrahovať staré prompty z Cursor súborov
- Flexibilita

---

## 📝 Zhrnutie

**Minimálne potrebné pre fungovanie:**
1. `scripts/auto_save_prompt.py`
2. `ministers/storage.py`
3. `ministers/memory.py`
4. `ministers/__init__.py`

**Všetko ostatné je voliteľné alebo nepotrebné.**

---

**Vytvorené:** 2025-12-02  
**Status:** Analýza dokončená

