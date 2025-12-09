# 📚 XVADUR Dokumentácia

Centrálny rozcestník pre kompletnú dokumentáciu projektu **Magnum Opus (XVADUR)**.

---

## 🗂️ Štruktúra Dokumentácie

### 🧠 Pamäť a Logovanie
- **[`MEMORY_AND_LOGGING.md`](MEMORY_AND_LOGGING.md)**  
  Kompletný popis Memory a Logging systémov. Zahrňuje MinisterOfMemory architektúru, triple-write logovanie (Markdown + JSONL + SQLite), automatické ukladanie promptov a Context Engineering integráciu.

### 🏗️ Architektúra Systému
- **[`ARCHITECTURE.md`](ARCHITECTURE.md)**  
  Detailný popis v2.0 architektúry. Vrstvy systému, Core moduly (ministers, RAG, XP), dátové toky a automatizácie.

### 🔄 Session Management
- **[`SESSION_MANAGEMENT.md`](SESSION_MANAGEMENT.md)**  
  3-vrstvová architektúra session managementu (Development/Staging/Production). Denný session rotation, branch management, MCP integrácia.

### 🎯 Quest System
- **[`QUEST_SYSTEM.md`](QUEST_SYSTEM.md)**  
  Integrácia s GitHub Issues pre trackovanie úloh. Automatické vytváranie, zatváranie questov, synchronizácia s lokálnym logom.

### 🛠️ Context Engineering
- **[`CONTEXT_ENGINEERING.md`](CONTEXT_ENGINEERING.md)**  
  Integrácia Context Engineering praktík (Compress Context, Isolate Context, Cognitive Tools, Token Metrics) do systému.

### 💾 Token Optimization
- **[`TOKEN_OPTIMIZATION.md`](TOKEN_OPTIMIZATION.md)**  
  Stratégie na optimalizáciu tokenovej spotreby. Best practices pre zníženie nákladov pri práci s AI.

### 🔀 Git Branching
- **[`GIT_BRANCHING.md`](GIT_BRANCHING.md)**  
  Branching stratégia projektu. Typy branchov, workflow, automatické merge policies.

### 🤖 RAG System
- **[`rag/RAG_GUIDE.md`](rag/RAG_GUIDE.md)**  
  Návod na použitie Retrieval-Augmented Generation systému. Semantic search, indexovanie, query formáty.

---

## 🔗 Rýchle Odkazy

### Hlavné Komponenty
- **Core:** `core/` - ministers (Memory), rag (Search), xp (Game)
- **Dáta:** `development/data/` - Prompty, Dataset, Profil
- **Logy:** `development/logs/` - XP, Activity Log (triple-write: MD + JSONL + SQLite)
- **Sessions:** `development/sessions/` - Current, Archive, Save Games

### Cursor Commands
- **`/loadgame`** - Načítanie kontextu pre novú session
- **`/savegame`** - Uloženie stavu + git commit/push
- **`/xvadur`** - Konverzačný režim
- **`/quest`** - Vytvorenie questu (GitHub Issue)

### Automatizácie
- **Local Scheduler:** Denný rotation systém (macOS launchd)
- **MCP Integration:** GitHub, Obsidian, Browser, Time nástroje (voliteľné)

---

## 🔄 Workflow: Kompletný Cyklus

### 1. Štart Sessiony (`/loadgame`)
**Účel:** Načíta kontext z predchádzajúcej sessiony

**Načítava (priorita JSON):**
1. **Save Game:** `SAVE_GAME_LATEST.json` → status, narrative, quests
2. **Log:** `XVADUR_LOG.jsonl` → posledných 5 záznamov (Hot Storage)
3. **XP:** `XVADUR_XP.json` → aktuálny status
4. **Profil:** `xvadur_profile.md` → sekcia "IV. SÚČASNÝ PROFIL" (voliteľné)

**Token Optimalizácia:** JSON formáty redukujú tokeny o ~40% (7,200 → 4,350 tokenov)

**Health Check:** Overí štruktúru questov a konzistenciu dát

---

### 2. Aktívna Práca (Počas Sessiony)

**Automatické Logovanie:**
```python
# Pri začiatku tasku
log_task_started("Názov tasku", "Popis")

# Pri dokončení tasku
log_task_completed("Názov", files_changed=[...], xp_estimate=5.0)
```

**Triple-Write Systém:**
Každý záznam sa automaticky zapíše do:
- `XVADUR_LOG.md` - Markdown (čitateľný)
- `XVADUR_LOG.jsonl` - JSONL (Hot Storage, max 100 záznamov)
- `archive.db` - SQLite (Cold Storage, neobmedzená kapacita)

---

### 3. Koniec Sessiony (`/savegame`)
**Účel:** Zachytiť kompletný stav pre prenos do novej sessiony

**Postup:**
1. **Krok 0:** Uložiť všetky user prompty z konverzácie → `prompts_log.jsonl`
2. **Krok 0.5:** Automaticky vypočítať XP → aktualizovať `XVADUR_XP.md/json`
3. **Krok 1:** Analyzovať aktuálny stav (XP, Log, Prompts)
4. **Krok 2:** Vytvoriť Save Game súbory:
   - `SAVE_GAME_LATEST.json` (hlavný zdroj pravdy)
   - `SAVE_GAME_LATEST.md` (naratívny formát)
   - `SAVE_GAME_LATEST_SUMMARY.md` (kompaktný summary)
5. **Krok 3:** Git commit + push (povinné)

---

### 4. Kompletný Cyklus

```
/loadgame → WORK (s automatickým logovaním) → /savegame
     ↓                                              ↓
  Načíta kontext                              Uloží stav
  (Save Game, Log, XP)                        (Prompty, XP, Naratív)
```

**Výhody:**
- ✅ Žiadna strata kontextu medzi sessionami
- ✅ Token optimalizácia (JSON formáty)
- ✅ Hot/Cold Storage architektúra
- ✅ Automatizácia (minimálna manuálna práca)
- ✅ Git verziovanie pri každom save game
- ✅ Gamifikácia (automatický XP tracking)

**Detailný popis:** Pozri [`SYSTEM_AUDIT.md`](SYSTEM_AUDIT.md#-kompletný-workflow-od-cursorrules-po-saveload-game)

---

## 📖 Čítanie Podľa Potreby

### Pre Začiatočníkov
1. **Hlavný README** (`../README.md`) - Rýchly prehľad a inštalácia
2. **ARCHITECTURE.md** - Pochopenie celkovej štruktúry
3. **MEMORY_AND_LOGGING.md** - Ako funguje pamäťový systém

### Pre Vývojárov
1. **CONTEXT_ENGINEERING.md** - Pokročilé techniky optimalizácie
2. **TOKEN_OPTIMIZATION.md** - Optimalizácia nákladov
3. **SESSION_MANAGEMENT.md** - Workflow a automatizácie

### Pre Správcov Systému
1. **GIT_BRANCHING.md** - Branching stratégia
2. **QUEST_SYSTEM.md** - Trackovanie úloh
3. **ARCHITECTURE.md** - Celková architektúra

---

## 🔄 Aktualizácia Dokumentácie

Dokumentácia je aktualizovaná:
- **Automaticky:** Pri `/savegame` cykloch
- **Manuálne:** Pri zásadných zmenách architektúry
- **Po Quest Completion:** Reflexia a dokumentácia nových feature

**Posledná revízia:** 2025-12-09 (Workspace Refactoring)

---

*Dokumentácia je súčasťou Magnum Opus v2.0 - Architektúry Osobného Kognitívneho Systému.*
