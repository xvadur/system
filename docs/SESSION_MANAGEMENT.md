# 🔄 Session Management v3.1

**Verzia:** 3.1.0  
**Posledná aktualizácia:** 2025-12-09

---

## Prehľad

Tento dokument popisuje session management v XVADUR workspace. Aktuálne používa lokálny scheduler systém (macOS launchd) pre denné rotácie. GitHub Actions workflows nie sú implementované.

---

## Vrstvy Systému

### 1. 🛠️ Development Layer (`development/`)

- **Účel:** Tvoja primárna pracovná zóna.
- **Obsah:**
  - `sessions/current/session.md`: Aktívny session súbor, v ktorom pracuješ.
  - `sessions/save_games/`: Umiestnenie pre `/savegame` a `/loadgame` checkpointy.
  - `logs/`: Tvoje `XVADUR_LOG.md`, `XVADUR_LOG.jsonl`, `XVADUR_XP.md`, `XVADUR_XP.json`
  - `data/`: `prompts_log.jsonl` a ďalšie dáta generované počas práce.
- **Workflow:**
  - Každodenná práca sa deje tu.
  - Cursor commands (`/savegame`, `/loadgame`) operujú výhradne v tomto adresári.

### 2. 🌅 Staging Layer (`staging/`)

- **Účel:** Príprava a review denných sessions.
- **Obsah:**
  - `sessions/today/`: Nová session, automaticky vytvorená o 00:00 z `templates/session_template.md`.
  - `sessions/yesterday/`: Archivovaná session z predchádzajúceho dňa, spolu so sumárom (`summary.md`) a metrikami (`metrics.json`).
  - `review/daily_review.md`: Automaticky generovaný ranný review (o 06:00) s analýzou a odporúčaniami.
- **Workflow:**
  - Ráno si pozrieš `daily_review.md`.
  - `staging/sessions/today/session.md` je automaticky skopírovaná do `development/sessions/current/` pre tvoju prácu.

### 3. 🚀 Production Layer (`production/`) - ⚠️ NIE JE IMPLEMENTOVANÉ

**Status:** Production layer bol plánovaný v dokumentácii, ale nie je aktuálne implementovaný. Dáta sa archivujú v `development/sessions/archive/` a metriky sú v `development/logs/`.

- **Poznámka:** Tento layer môže byť implementovaný v budúcnosti pre automatizovanú archiváciu a agregáciu metrík.

---

## Denný Session Rotation (Lokálny Scheduler)

### Lokálny Scheduler Systém

Systém používa macOS launchd pre automatizované denné rotácie.

- **Konfigurácia:** `scripts/local_scheduler/com.xvadur.daily_rotation.plist`
- **Inštalácia:** `scripts/local_scheduler/install_scheduler.sh`

### Časový Plán

**00:00 (Polnoc):**
- Spustí sa `scripts/daily_rotation.py`:
  1. Archivuje včerajšiu session
  2. Vytvorí novú session
  3. Vygeneruje denné metriky
  4. Vypočíta XP
  5. (Voliteľne) Pushne zmeny na GitHub

### Manuálne Spustenie

```bash
# Spustiť dennú rotáciu manuálne
python3 scripts/daily_rotation.py
```

---

## ⚠️ Poznámka: GitHub Actions Nie Sú Implementované

Pôvodne plánované GitHub Actions workflows (`.github/workflows/`) nie sú aktuálne implementované. Systém používa lokálny scheduler namiesto toho.

**Pôvodne plánované workflowy (nie sú aktívne):**
- Auto Session Rotation
- Morning Review Prep
- Session Setup

**Aktuálne riešenie:** Lokálny scheduler (`scripts/local_scheduler/`)

---

## Tvoj Denný Workflow

1.  **Ráno o 7:00:**
    - Nájdeš pripravenú session v `development/sessions/current/session.md`
    - Otvoríš `staging/review/daily_review.md` pre včerajší sumár
    - Doplníš `🎯 Cieľ Dňa` do novej session

2.  **Počas Dňa:**
    - Pracuješ v `development/sessions/current/session.md`
    - Používaš `/savegame` na checkpointy
    - **Priebežné task logging:** Každá úloha sa automaticky zapisuje do `XVADUR_LOG.md`

3.  **Automatizácia:**
    - O polnoci: Session rotation a archivácia
    - O 6:00: Generovanie ranného review  
    - O 7:00: Príprava novej session

---

## MCP Nástroje (Voliteľné)

MCP nástroje môžu byť použité v skriptoch, ale nie sú povinné:
- **GitHub MCP:** Branch management, mergovanie, commity (fallback na git CLI)
- **Time MCP:** Presné časové synchronizácie (fallback na datetime)
- **Sequential Thinking MCP:** Analýza a generovanie review (voliteľné)
- **Obsidian MCP:** Export do knowledge base (voliteľné)

---

## Súvisiace Dokumenty

- `core/mcp/README.md` - Kompletná MCP integrácia dokumentácia
- `scripts/mcp_helpers.py` - MCP wrapper funkcie
- `scripts/local_scheduler/` - Lokálny scheduler konfigurácia
- `scripts/daily_rotation.py` - Denný rotation script
