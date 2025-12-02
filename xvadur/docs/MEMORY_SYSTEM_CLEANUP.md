# 🧹 Čistenie Memory Systému

## 📊 Súčasný Stav

Máme **dva spôsoby** ukladania promptov:
1. ✅ **Automatické cez `.cursorrules`** (nové, primárne) - funguje v reálnom čase
2. ⚠️ **Background tracker** (staré, alternatíva) - sleduje Cursor súbory

## ✅ ČO JE POTREBNÉ (Kritické)

### Pre automatické ukladanie cez `.cursorrules`:

1. **`scripts/auto_save_prompt.py`** ✅
   - Používa sa v `.cursorrules`
   - Ukladá prompty v reálnom čase
   - **NEPODMIENENE POTREBNÉ**

2. **`ministers/storage.py`** ✅
   - FileStore implementácia
   - Trvalé ukladanie do JSONL
   - **NEPODMIENENE POTREBNÉ**

3. **`ministers/memory.py`** ✅
   - MinisterOfMemory systém
   - MemoryRecord, AssistantOfMemory
   - **NEPODMIENENE POTREBNÉ**

4. **`ministers/__init__.py`** ✅
   - Package exports
   - **NEPODMIENENE POTREBNÉ**

---

## ⚠️ ČO JE VOLITEĽNÉ (Užitočné, ale nie kritické)

1. **`scripts/export_to_log.py`** ⚠️
   - Export promptov do `XVADUR_LOG.md`
   - Užitočné pre markdown export
   - **MÔŽE BYŤ UŽITOČNÉ**

2. **`scripts/metrics_tracker.py`** ⚠️
   - Tracking metrík (word count, sentiment, XP)
   - Užitočné pre analýzu
   - **MÔŽE BYŤ UŽITOČNÉ**

3. **`.vscode/tasks.json`** ⚠️
   - VS Code tasks pre export a metriky
   - Užitočné pre manuálne spustenie
   - **MÔŽE BYŤ UŽITOČNÉ**

---

## ❌ ČO NIE JE POTREBNÉ (Ak ukladáme cez `.cursorrules`)

### Background Tracker Systém:

1. **`scripts/conversation_tracker.py`** ❌
   - Background service pre file watching
   - **NEPOTREBNÉ** - prompty sa ukladajú cez `.cursorrules`

2. **`scripts/conversation_watcher.py`** ❌
   - File watcher pre Cursor súbory
   - **NEPOTREBNÉ** - nepotrebujeme sledovať súbory

3. **`scripts/cursor_prompt_extractor.py`** ❌
   - Extrakcia promptov z Cursor JSON súborov
   - **NEPOTREBNÉ** - prompty sa ukladajú priamo

4. **`xvadur/config/conversation_tracker_config.json`** ❌
   - Konfigurácia pre tracker
   - **NEPOTREBNÉ** - tracker sa nepoužíva

5. **`watchdog` dependency** ❌
   - Python package pre file watching
   - **NEPOTREBNÉ** - používa sa len v watcheri

### VS Code Tasks (tracker-related):

- "Start Conversation Tracker" ❌
- "Stop Conversation Tracker" ❌

---

## 🎯 Odporúčanie

### Možnosť 1: Minimálna verzia (odporúčané)

**Odstrániť:**
- `scripts/conversation_tracker.py`
- `scripts/conversation_watcher.py`
- `scripts/cursor_prompt_extractor.py`
- `xvadur/config/conversation_tracker_config.json`
- Tracker tasks z `.vscode/tasks.json`
- `watchdog` z `requirements.txt`

**Ponechať:**
- `scripts/auto_save_prompt.py` ✅
- `ministers/*` ✅
- `scripts/export_to_log.py` ⚠️
- `scripts/metrics_tracker.py` ⚠️
- Export a metriky tasks v `.vscode/tasks.json` ⚠️

### Možnosť 2: Hybrid verzia (backup)

**Ponechať všetko:**
- Automatické ukladanie cez `.cursorrules` (primárne)
- Background tracker (backup, ak `.cursorrules` zlyhá)
- Export a metriky (užitočné nástroje)

**Výhody:**
- Duplicitné riešenie
- Možnosť extrahovať staré prompty
- Flexibilita

---

## 📝 Zhrnutie

**Minimálne potrebné:**
- `scripts/auto_save_prompt.py`
- `ministers/storage.py`
- `ministers/memory.py`
- `ministers/__init__.py`

**Všetko ostatné je voliteľné alebo nepotrebné.**

---

**Vytvorené:** 2025-12-02

