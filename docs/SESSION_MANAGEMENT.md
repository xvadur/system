#  Súbor: docs/SESSION_MANAGEMENT.md
# Popis: Dokumentácia pre 3-vrstvový session management.
# Autor: AI Agent
# Dátum: 2025-12-04

# 🔄 Session Management v3

**Verzia:** 3.0.0  
**Posledná aktualizácia:** 2025-12-04

---

## Prehľad

Tento dokument popisuje 3-vrstvovú architektúru pre session management v XVADUR workspace. Cieľom je oddeliť priebežnú prácu od automatizovaných procesov a ranného review.

---

## Vrstvy Systému

### 1. 🛠️ Development Layer (`development/`)

- **Účel:** Tvoja primárna pracovná zóna.
- **Obsah:**
  - `sessions/current/session.md`: Aktívny session súbor, v ktorom pracuješ.
  - `sessions/save_games/`: Umiestnenie pre `/savegame` a `/loadgame` checkpointy.
  - `logs/`: Tvoje `XVADUR_LOG.md` a `XVADUR_XP.md`.
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

### 3. 🚀 Production Layer (`production/`)

- **Účel:** Dlhodobá archivácia a agregácia metrík.
- **Obsah:**
  - `metrics/`: Agregované denné a týždenné metriky.
  - `sessions/archive/`: Dlhodobý archív všetkých sessions.
- **Workflow:**
  - Plne automatizované procesy.
  - Dáta sa sem presúvajú zo `staging` vrstvy.

---

## Automatizačné Procesy

### 1. Auto Session Rotation (`.github/workflows/auto-session-rotation.yml`)

- **Trigger:** Každý deň o 00:00 UTC.
- **Kroky:**
  1.  Spustí `scripts/auto_archive_session.py`:
      - Presunie `development/sessions/current/session.md` do `staging/sessions/yesterday/`.
      - Vygeneruje `summary.md` a `metrics.json`.
  2.  Spustí `scripts/create_new_session.py`:
      - Vytvorí novú session v `staging/sessions/today/` z template.
      - Skopíruje ju do `development/sessions/current/`.
  3.  Commitne zmeny.

### 2. Morning Review Prep (`.github/workflows/morning-review-prep.yml`)

- **Trigger:** Každý deň o 06:00 UTC.
- **Kroky:**
  1.  Spustí `scripts/generate_daily_review.py`:
      - Načíta dáta zo `staging/sessions/yesterday/`.
      - Vygeneruje `staging/review/daily_review.md` pomocou `Sequential Thinking MCP`.
  2.  Commitne zmeny.

---

## Tvoj Denný Workflow

1.  **Ráno:**
    - Otvoríš `staging/review/daily_review.md`.
    - Skontroluješ včerajšie metriky a sumár.
    - Otvoríš `development/sessions/current/session.md`, ktorý je už pripravený.
    - Doplníš `🎯 Cieľ Dňa`.

2.  **Počas Dňa:**
    - Pracuješ v `development/sessions/current/session.md`.
    - Používaš `/savegame` na vytváranie checkpointov v `development/sessions/save_games/`.

3.  **Večer:**
    - Automatizácia sa postará o archiváciu a prípravu na ďalší deň.
