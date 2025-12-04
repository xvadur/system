# 🧠 XVADUR Workspace

**Magnum Opus: Architektúra Osobného Kognitívneho Systému v2.0**

Modulárny workspace pre transformáciu myslenia a práce s AI. Obsahuje pamäťový systém, RAG vyhľadávanie, gamifikáciu a automatizácie.

---

## 🚀 Quick Start

```bash
# 1. Klonovanie
git clone https://github.com/xvadur/system.git
cd system

# 2. Virtuálne prostredie
python3 -m venv venv
source venv/bin/activate

# 3. Inštalácia závislostí
pip install -r requirements.txt

# 4. Konfigurácia
cp .env.example .env
# Edituj .env a pridaj OPENAI_API_KEY
```

---

## 📁 Štruktúra

```
xvadur-workspace/
├── development/             # Tvoja práca
├── staging/                 # Denný review
├── production/              # Automatizácie
│
├── core/                    # Jadro systému (Memory, RAG, XP)
├── data/                    # Globálne dáta (RAG index)
├── sessions/                # Session management
│   ├── current/             # Aktuálna session
│   ├── archive/             # Archív
│   └── save_games/          # Checkpointy
│
├── logs/                    # Logy (XP, Activity)
├── docs/                    # Dokumentácia
├── scripts/                 # Utility skripty
└── archive/                 # Archív pilotného stavu
```

---

## 🎮 Cursor Commands

| Príkaz | Popis |
|--------|-------|
| `/loadgame` | Načítanie kontextu pre novú session |
| `/savegame` | Uloženie stavu + git commit/push |
| `/xvadur` | Konverzačný režim |

---

## 📊 Aktuálny Status

- **Level:** 5 (Expert)
- **XP:** 159.78 / 750
- **Dataset:** 1,822 konverzačných párov
- **Obdobie:** 126 dní (Kortex) + 4 dni (Cursor)

---

## 🔧 Hlavné Komponenty

### 1. MinisterOfMemory (`core/ministers/`)
Automatické ukladanie a vyhľadávanie v histórii konverzácií.

```python
from core import MinisterOfMemory, FileStore

store = FileStore(Path("data/prompts_log.jsonl"))
minister = MinisterOfMemory(assistant=AssistantOfMemory(store=store))
minister.log_event("user", "Môj prompt...")
```

### 2. RAG System (`core/rag/`)
Hybrid search (semantic + keyword) v histórii promptov.

```bash
python core/rag/rag_agent_helper.py "ako som riešil X" 5 0.4 true search
```

### 3. XP System (`core/xp/`)
Gamifikácia s automatickým výpočtom z logu a promptov.

```python
from core import calculate_xp, update_xp_file

xp_data = calculate_xp()
update_xp_file("logs/XVADUR_XP.md", xp_data)
```

---

## 🤖 GitHub Actions

| Workflow | Trigger | Popis |
|----------|---------|-------|
| `daily-metrics.yml` | 23:59 UTC | Denný výpočet XP |
| `weekly-synthesis.yml` | Nedeľa 23:00 | Týždenný report |
| `backup.yml` | Push do main | Validácia dát |

---

## 📖 Dokumentácia

- **[ARCHITEKTÚRA](docs/ARCHITECTURE.md):** Detailný popis v2.0 architektúry.
- **[SESSION MANAGEMENT](docs/SESSION_MANAGEMENT.md):** Popis 3-vrstvového session managementu.
- **[MCP INTEGRÁCIA](docs/MCP_INTEGRATION.md):** Ako sa používa MCP Docker systém.
- **[MEMORY SYSTÉM](docs/MEMORY_SYSTEM.md):** Ako funguje `MinisterOfMemory`.
- **[RAG SYSTÉM](docs/rag/RAG_GUIDE.md):** Návod na použitie RAG.

---

## 🏷️ Verzie

| Tag | Popis |
|-----|-------|
| `pilot-v1.0` | Pilotná verzia (2025-12-04) |

---

**Vytvorené:** 2025-12-04  
**Verzia:** 2.0.0  
**Status:** ✅ Aktívny
