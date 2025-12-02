# 📋 Plán Implementácie: Pasívna Vrstva pre Zachytávanie Promptov

**Dátum:** 2025-12-02  
**Status:** 🟢 V pláne  
**Cieľ:** Vytvoriť pasívnu vrstvu, ktorá automaticky zachytáva a ukladá prompty z Cursor konverzácií

---

## 🎯 Cieľ

Vytvoriť systém, ktorý:
- **Pasívne beží na pozadí** - bez tvojej akcie
- **Automaticky zachytáva prompty** - z Cursor konverzácií
- **Ukladá do trvalého úložiska** - JSONL/DB formát
- **Zachováva dlhodobý kontext** - pre budúce sessiony
- **Integruje sa s existujúcimi systémami** - Save Game, Log, RAG

---

## 📦 Čo už máme (z PR #3)

✅ **MinisterOfMemory** - orchestrácia memory stratégie  
✅ **AssistantOfMemory** - taktické memory operácie  
✅ **MemoryRecord** - dátový model  
✅ **InMemoryStore** - volatilné úložisko (RAM)  
✅ **MemoryStore Protocol** - interface pre pluggable storage

---

## 🔨 Čo treba vytvoriť

### Fáza 1: Trvalé Úložisko (FileStore)

**Problém:** `InMemoryStore` ukladá len do RAM, po reštarte sa stratí.

**Riešenie:** Vytvoriť `FileStore`, ktorý ukladá do JSONL súboru.

**Súbory:**
- `ministers/storage.py` - FileStore implementácia
- `xvadur/data/prompts_log.jsonl` - úložisko promptov

**Funkcie:**
- Ukladanie do JSONL (append-only)
- Načítanie existujúcich záznamov
- Query a latest operácie
- Thread-safe operácie

---

### Fáza 2: Pasívna Vrstva (File Watcher)

**Problém:** Potrebujeme zachytiť prompty z Cursor automaticky.

**Riešenie:** File watcher, ktorý sleduje Cursor súbory a zachytáva zmeny.

**Súbory:**
- `scripts/conversation_watcher.py` - file watcher script
- `scripts/cursor_prompt_extractor.py` - extrakcia promptov z Cursor súborov

**Funkcie:**
- Sledovanie Cursor chat súborov
- Detekcia nových promptov
- Automatické volanie MinisterOfMemory
- Background process (daemon)

**Možné cesty Cursor súborov:**
- `~/.cursor/chat/` (možné umiestnenie)
- `~/.config/cursor/chat/` (alternatíva)
- Workspace-specific súbory

---

### Fáza 3: Conversation Tracker (Background Service)

**Problém:** Potrebujeme centralizovaný systém na tracking.

**Riešenie:** Python script bežiaci ako background service.

**Súbory:**
- `scripts/conversation_tracker.py` - hlavný tracker script
- `xvadur/config/conversation_tracker_config.json` - konfigurácia

**Funkcie:**
- Inicializácia MinisterOfMemory s FileStore
- Spustenie file watcher
- Logging a error handling
- Graceful shutdown

**Spustenie:**
- VS Code Task
- Systemd service (Linux)
- LaunchAgent (macOS)
- Nohup (jednoduché)

---

### Fáza 4: Integrácia s Existujúcimi Systémami

**Cieľ:** Integrovať MinisterOfMemory do tvojich workflow.

**Integrácie:**

#### 4.1. `/savegame` Command
- Automaticky načíta posledné prompty z MinisterOfMemory
- Použije ich pri vytváraní naratívneho kontextu
- Exportuje do SAVE_GAME_LATEST.md

#### 4.2. `/loadgame` Command
- Načíta históriu promptov z MinisterOfMemory
- Použije pri obnovení kontextu

#### 4.3. XVADUR_LOG.md
- Automatický export promptov do logu
- Synchronizácia s MinisterOfMemory

#### 4.4. RAG Systém
- Export promptov do RAG indexu
- Automatické indexovanie nových promptov

---

### Fáza 5: Metriky a Analýza

**Cieľ:** Sledovať metriky promptov realtime.

**Funkcie:**
- Počet slov per prompt
- Počet promptov per session
- Priemerná dĺžka promptu
- Témy a kľúčové slová
- Sentiment analýza
- XP odhad

**Súbory:**
- `scripts/metrics_tracker.py` - tracking metrík
- `xvadur/data/metrics/` - uloženie metrík

---

## 📁 Štruktúra Súborov

```
xvadur-workspace/
├── ministers/
│   ├── __init__.py          ✅ (z PR #3)
│   ├── memory.py             ✅ (z PR #3)
│   └── storage.py            ⏳ (Fáza 1 - FileStore)
│
├── scripts/
│   ├── conversation_watcher.py      ⏳ (Fáza 2)
│   ├── cursor_prompt_extractor.py   ⏳ (Fáza 2)
│   ├── conversation_tracker.py      ⏳ (Fáza 3)
│   └── metrics_tracker.py           ⏳ (Fáza 5)
│
├── xvadur/
│   ├── data/
│   │   ├── prompts_log.jsonl        ⏳ (Fáza 1 - úložisko)
│   │   └── metrics/                 ⏳ (Fáza 5)
│   │
│   └── config/
│       └── conversation_tracker_config.json  ⏳ (Fáza 3)
│
└── .vscode/
    └── tasks.json                    ⏳ (Fáza 3 - VS Code task)
```

---

## 🔄 Workflow

### Normálny Prípad Použitia

1. **Užívateľ otvorí Cursor**
2. **Conversation Tracker beží na pozadí** (automaticky spustený)
3. **Užívateľ napíše prompt** v Cursor
4. **File Watcher zachytí zmenu** v Cursor súbore
5. **Prompt Extractor extrahuje prompt**
6. **MinisterOfMemory uloží prompt** do FileStore
7. **Metriky Tracker aktualizuje metriky**
8. **Všetko beží automaticky** - bez tvojej akcie

### Pri `/savegame`

1. **Načíta posledné prompty** z MinisterOfMemory
2. **Vytvorí naratívny kontext** z promptov
3. **Exportuje do SAVE_GAME_LATEST.md**
4. **Synchronizuje s XVADUR_LOG.md**

---

## 🧪 Testovanie

### Test 1: Základné Ukladanie
- Vytvoriť test prompt
- Overiť, že sa uložil do JSONL
- Overiť, že sa dá načítať

### Test 2: File Watcher
- Simulovať zmenu v Cursor súbore
- Overiť, že watcher zachytil zmenu
- Overiť, že prompt bol uložený

### Test 3: Integrácia
- Spustiť `/savegame`
- Overiť, že používa MinisterOfMemory
- Overiť export do markdown

### Test 4: Dlhodobý Kontext
- Vytvoriť prompty v rôznych sessionách
- Overiť, že sa zachovávajú
- Overiť vyhľadávanie v histórii

---

## 📝 Dokumentácia

### Dokumenty na vytvorenie:
1. `xvadur/docs/MEMORY_SYSTEM_README.md` - používateľská dokumentácia
2. `xvadur/docs/MEMORY_SYSTEM_ARCHITECTURE.md` - technická dokumentácia
3. `xvadur/docs/MEMORY_SYSTEM_SETUP.md` - setup guide

---

## ⚠️ Poznámky a Riziká

### Riziká:
1. **Cursor súbory môžu byť na rôznych miestach** - potrebujeme detekciu
2. **File watcher môže byť náročný na zdroje** - optimalizácia
3. **JSONL môže narásť veľmi veľký** - rotácia súborov
4. **Thread safety** - FileStore musí byť thread-safe

### Riešenia:
1. **Konfiguračný súbor** - užívateľ môže nastaviť cestu
2. **Debouncing** - zmeny sa spracúvajú v batch
3. **Rotácia súborov** - nový súbor každý deň/mesiac
4. **Locking** - file locking pre thread safety

---

## 🚀 Priorita Implementácie

### Vysoká priorita:
1. ✅ Merge PR #3 (hotovo)
2. ⏳ Fáza 1: FileStore (základ pre všetko)
3. ⏳ Fáza 2: File Watcher (pasívna vrstva)
4. ⏳ Fáza 3: Conversation Tracker (background service)

### Stredná priorita:
5. ⏳ Fáza 4: Integrácia s existujúcimi systémami
6. ⏳ Fáza 5: Metriky a analýza

### Nízka priorita:
7. ⏳ Dokumentácia
8. ⏳ Pokročilé funkcie (RAG export, atď.)

---

## 📊 Odhad Času

- **Fáza 1 (FileStore):** 1-2 hodiny
- **Fáza 2 (File Watcher):** 2-3 hodiny
- **Fáza 3 (Tracker):** 1-2 hodiny
- **Fáza 4 (Integrácia):** 2-3 hodiny
- **Fáza 5 (Metriky):** 2-3 hodiny
- **Testovanie a dokumentácia:** 2-3 hodiny

**Celkom:** ~10-16 hodín práce

---

## ✅ Next Steps

1. **Začať s Fázou 1** - vytvoriť FileStore
2. **Testovať FileStore** - overiť základné funkcie
3. **Pokračovať s Fázou 2** - file watcher
4. **Iteratívne testovanie** - po každej fáze

---

**Vytvorené:** 2025-12-02  
**Autor:** xvadur_architect  
**Status:** 🟢 Ready for Implementation

