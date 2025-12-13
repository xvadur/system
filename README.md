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
│   ├── sessions/            # Sessions (current, archive, save_games)
│   ├── data/                # Dáta (profile, prompts)
│   └── logs/                # Logy (historické)
├── staging/                 # Denný review
├── production/              # Automatizácie
│
├── core/                    # Jadro systému (XP - manuálne použitie)
├── scripts/                 # Utility skripty
│
├── docs/                    # Dokumentácia
├── templates/               # Templates pre sessiony a savegame
└── archive/                 # Archív pilotného stavu
```

---

## 🎮 Cursor Commands

| Príkaz | Popis |
|--------|-------|
| `/loadgame` | Načítanie kontextu pre novú session |
| `/savegame` | Uloženie stavu + git commit/push |
| `/xvadur` | Konverzačný režim |
| `/quest` | Vytvorenie questu (GitHub Issue) |

---

## 📊 Aktuálny Status

- **Level:** 5 (AI Developer Senior)
- **XP:** 199.59 / 200.0
- **Streak:** 4 dni
- **Dataset:** 1,822 konverzačných párov

---

## 🔧 Hlavné Komponenty

### 1. XP System (`core/xp/`)
Gamifikácia s manuálnym výpočtom (ak je potrebné).

```python
from core.xp.calculator import calculate_xp, update_xp_file

xp_data = calculate_xp()
update_xp_file("development/logs/XVADUR_XP.md", xp_data)
```

**Poznámka:** XP systém je dostupný pre manuálne použitie, ale nie je automatizovaný.

---

## 📖 Dokumentácia

Kompletná dokumentácia je v [`docs/`](docs/) adresári. Pre prehľad pozri [`docs/README.md`](docs/README.md).

### Kľúčové Dokumenty

- **[SESSION_MANAGEMENT.md](docs/SESSION_MANAGEMENT.md)**: 3-vrstvový session management
- **[QUEST_SYSTEM.md](docs/QUEST_SYSTEM.md)**: GitHub Issues integrácia
- **[TOKEN_OPTIMIZATION.md](docs/TOKEN_OPTIMIZATION.md)**: Stratégie optimalizácie tokenov
- **[XVADUR_DETAILS.md](docs/XVADUR_DETAILS.md)**: Konverzačný modul `/xvadur`

**Poznámka:** Niektoré dokumenty (ARCHITECTURE.md, SYSTEM_AUDIT.md) sú historické a odkazujú na odstránené moduly.

---

## 🤖 Integrácia

### MCP (Multi-Capable Peripheral)
MCP Docker systém poskytuje 59+ nástrojov (GitHub, Obsidian, Browser, Time). Viac informácií v [`core/mcp/README.md`](core/mcp/README.md).

### Local Scheduler
Lokálny scheduler (macOS launchd) pre automatizované denné rotácie sessions a metrík.

---

## 🏷️ Verzie

| Tag | Popis |
|-----|-------|
| `pilot-v1.0` | Pilotná verzia (2025-12-04) |
| `v2.0.0` | Aktuálna verzia - Magnum Opus v2.0 |

---

**Vytvorené:** 2025-12-04  
**Verzia:** 2.0.0 (Zjednodušená)  
**Status:** ✅ Aktívny  
**Posledná revízia:** 2025-12-10 (System Simplification & Enhanced Context)
