#  Súbor: docs/SESSION_MANAGEMENT.md
# Popis: Dokumentácia pre 3-vrstvový session management s MCP integráciou.
# Autor: AI Agent
# Dátum: 2025-12-05

# 🔄 Session Management v3.1

**Verzia:** 3.1.0  
**Posledná aktualizácia:** 2025-12-05

---

## Prehľad

Tento dokument popisuje 3-vrstvovú architektúru pre session management v XVADUR workspace s plnou MCP integráciou. Systém automaticky spravuje denné sessiony, branch rotation a ranné review.

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

## Denný Session Rotation s MCP

### GitHub Branch Strategy

- **`main`:** Hlavná stabilná vetva
- **`session-YYYY-MM-DD`:** Denné session vetvy (napr. `session-2025-12-05`)
- **Automatické mergovanie:** O polnoci sa aktuálna session branch merguje do main

### Časový Plán

1. **00:00 UTC (Polnoc):**
   - Merge aktuálnej session branch do `main`
   - Vytvorenie novej session branch pre nasledujúci deň
   - Archivácia včerajšej session

2. **07:00 SEČ (Ráno):**
   - Vytvorenie novej session v `development/sessions/current/`
   - Generovanie denného review

---

## Automatizačné Procesy s MCP Integráciou

### 1. Auto Session Rotation (`.github/workflows/auto-session-rotation.yml`)

- **Trigger:** Každý deň o 00:00 UTC.
- **Kroky:**
  1.  **GitHub MCP:** Merge aktuálnej session branch do `main`
  2.  **GitHub MCP:** Vytvorenie novej session branch
  3.  Spustí `scripts/auto_archive_session.py`:
      - Presunie `development/sessions/current/session.md` do `staging/sessions/yesterday/`.
      - Vygeneruje `summary.md` a `metrics.json`.
  4.  Spustí `scripts/create_new_session.py`:
      - Vytvorí novú session v `staging/sessions/today/` z template.
      - Skopíruje ju do `development/sessions/current/`.
  5.  **GitHub MCP:** Commitne zmeny do novej session branch.

### 2. Morning Review Prep (`.github/workflows/morning-review-prep.yml`)

- **Trigger:** Každý deň o 06:00 UTC.
- **Kroky:**
  1.  Spustí `scripts/generate_daily_review.py`:
      - Načíta dáta zo `staging/sessions/yesterday/`.
      - **Sequential Thinking MCP:** Vygeneruje `staging/review/daily_review.md`.
  2.  **GitHub MCP:** Commitne zmeny.

### 3. 7:00 Session Setup (`.github/workflows/morning-session-setup.yml`)

- **Trigger:** Každý deň o 07:00 SEČ.
- **Kroky:**
  1.  **Time MCP:** Overenie správneho časového pásma
  2.  Skopíruje `staging/sessions/today/session.md` do `development/sessions/current/`
  3.  Aktualizuje `XVADUR_LOG.md` s novou session informáciou
  4.  **GitHub MCP:** Commitne zmeny

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

## MCP Nástroje Použité

- **GitHub MCP:** Branch management, mergovanie, commity
- **Time MCP:** Presné časové synchronizácie
- **Sequential Thinking MCP:** Analýza a generovanie review
- **Obsidian MCP:** Export do knowledge base

---

## Súvisiace Dokumenty

- `core/mcp/README.md` - Kompletná MCP integrácia dokumentácia
- `scripts/mcp_helpers.py` - MCP wrapper funkcie
- `.github/workflows/` - Automatizačné workflowy
