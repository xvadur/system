# Quest System - GitHub Issues Integrácia

**Quest System** umožňuje jednoducho vytvárať a trackovať úlohy cez GitHub Issues. Každá úloha sa automaticky synchronizuje s lokálnym logom a môže sa automaticky zatvoriť po dokončení.

---

## 🎯 Koncept

Quest System kombinuje:
- **Lokálne logy** (`development/logs/XVADUR_LOG.md`) - rýchle, chronologické zaznamenávanie
- **GitHub Issues** - štruktúrované úlohy, trackovanie, AI komentáre
- **Automatické zatváranie** - Issues sa zatvárajú automaticky po dokončení (cez commit messages)

---

## 🚀 Použitie

### Vytvorenie Questu

Použi `/quest` command v Cursor:

```
/quest Uprav cursorrules - pridať MCP pravidlo
/quest Oprav nekonzistentné cesty v dokumentácii
/quest Implementovať automatické zatváranie Issues
```

**Čo sa stane:**
1. ✅ Vytvorí sa GitHub Issue v `xvadur/system` repozitári (ak je MCP dostupný)
2. ✅ Zapíše sa do lokálneho logu: `[HH:MM] 🔹 Vytvorená úloha #123: [Popis]`
3. ✅ Vráti sa Issue number (#123) pre tracking

**Output:**
```
✅ Vytvorená úloha #123: Uprav cursorrules - pridať MCP pravidlo
🔗 https://github.com/xvadur/system/issues/123

📝 Zapísané do logu: development/logs/XVADUR_LOG.md

💡 Tip: Po dokončení úlohy pridaj `fixes #123` do commit message pre automatické zatvorenie Issue.
```

---

## 🔄 Workflow

### 1. Vytvorenie Questu

```
Užívateľ: /quest Oprav typo v README.md

Agent:
1. Vytvorí Issue #124 cez MCP helper funkciu
2. Zapíše do logu: [15:20] 🔹 Vytvorená úloha #124: Oprav typo v README.md
3. Vráti Issue number a URL
```

### 2. Práca na úlohe

Agent môže začať pracovať na úlohe:
- Upravovať súbory
- Zapisovať do logu pribežne
- V commit message použiť Issue number: `feat: oprav typo v README (#124)`

### 3. Automatické zatvorenie

GitHub automaticky zatvorí Issue, ak commit message obsahuje:
- `fixes #123`
- `closes #123`
- `resolves #123`

**Príklad commit message:**
```
feat: oprav typo v README.md

fixes #124
```

### 4. Explicitné zatvorenie (voliteľné)

Ak chceš zatvoriť Quest explicitne:
```
/quest close #123
```

Agent:
1. Zatvorí Issue cez MCP (`close_github_issue()`)
2. Zapíše do logu: `[HH:MM] ✅ Dokončená úloha #123: [Popis]`

---

## 📋 Komponenty

### 1. `/quest` Cursor Command

**Súbor:** `.cursor/commands/quest.md`

**Funkčnosť:**
- Extrahuje popis úlohy z user inputu
- Vytvorí GitHub Issue cez MCP helper funkciu
- Zapíše do lokálneho logu
- Vráti Issue number a URL

### 2. MCP Helper Funkcie

**Súbor:** `scripts/mcp_helpers.py`

**Funkcie:**
- `create_github_issue(title, body, labels)` - Vytvorí GitHub Issue
- `close_github_issue(issue_number, comment)` - Zatvorí GitHub Issue
- `get_github_issue(issue_number)` - Načíta informácie o Issue

**Fallback logika:**
- Ak MCP nie je dostupný, použije GitHub REST API (vyžaduje `GITHUB_TOKEN`)
- Ak ani REST API nie je dostupný, vráti error

### 3. GitHub Actions Workflow

**Súbor:** `.github/workflows/auto-close-issues.yml`

**Funkčnosť:**
- Spúšťa sa po push do `main` branch
- Parsuje `development/logs/XVADUR_LOG.md`
- Detekuje záznamy typu `✅ Dokončená úloha #123`
- Zatvára Issues automaticky (ak ešte nie sú zatvorené)

**Poznámka:** GitHub už podporuje automatické zatváranie Issues cez commit messages (`fixes #123`), takže tento workflow je voliteľný a slúži ako backup.

---

## 🔧 Technické Detaily

### Repository Info

Quest System automaticky zisťuje GitHub repository z git remote:
- Owner: `xvadur`
- Repo: `system`

Ak git remote nie je dostupný, použije sa fallback hodnota z `README.md`.

### MCP Integrácia

Quest System používa GitHub MCP funkcie:
- `mcp_MCP_DOCKER_issue_write` - vytvorenie/aktualizácia Issue
- `mcp_MCP_DOCKER_issue_read` - načítanie Issue
- `mcp_MCP_DOCKER_add_issue_comment` - komentovanie Issue

**Fallback:** GitHub REST API (ak MCP nie je dostupný)

### Lokálny Log Formát

```
[HH:MM] 🔹 Vytvorená úloha #123: [Popis úlohy]
[HH:MM] ✅ Dokončená úloha #123: [Popis úlohy]
```

---

## 📝 Príklady

### Príklad 1: Jednoduchá úloha

```
Užívateľ: /quest Oprav typo v README.md

Agent:
✅ Vytvorená úloha #124: Oprav typo v README.md
🔗 https://github.com/xvadur/system/issues/124

[Agent upraví README.md]

Commit: fix: oprav typo v README.md (fixes #124)

GitHub: Automaticky zatvorí Issue #124
```

### Príklad 2: Komplexná úloha

```
Užívateľ: /quest Refaktorovať mcp_helpers.py - pridať error handling

Agent:
✅ Vytvorená úloha #125: Refaktorovať mcp_helpers.py - pridať error handling
🔗 https://github.com/xvadur/system/issues/125

[Agent refaktoruje kód, pridá error handling]

Commit: refactor: pridať error handling do mcp_helpers.py (fixes #125)

GitHub: Automaticky zatvorí Issue #125
```

---

## ⚠️ Dôležité

- **Vždy zapísať do logu:** Bez zápisu do logu sa Quest nestráca, ale nie je viditeľný v chronologickom prehľade
- **Issue number:** Vždy vráť Issue number užívateľovi pre tracking
- **Fallback:** Ak MCP nie je dostupný, Issue sa nevytvorí, ale zapíše sa do logu s poznámkou
- **Repository:** Issues sa vytvárajú v `xvadur/system` repozitári

---

## 🔗 Súvisiace

- **Cursor Command:** `.cursor/commands/quest.md`
- **MCP Helpers:** `scripts/mcp_helpers.py`
- **Lokálny log:** `development/logs/XVADUR_LOG.md`
- **GitHub Actions:** `.github/workflows/auto-close-issues.yml`
- **MCP Integrácia:** `docs/MCP_INTEGRATION.md`

---

---

## 🧬 Anthropic Harness Pattern (NOVÉ - 2025-12-09)

Implementácia best practices z [Anthropic Engineering článku](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents).

### Prečo Anthropic Pattern?

> *"Generalized agents behave like amnesiacs with tool belts. Domain memory turns chaotic loops into durable progress."*
> — Nate B Jones (Y Combinator)

Tvoj systém už intuitívne implementoval tieto patterny. Teraz ich formalizujeme.

### Quest Schema 2.1

Každý quest teraz obsahuje `passes` a `validation` fields:

```json
{
  "id": "quest-15",
  "title": "Quest #15: Analýza Nate Jones Videa",
  "status": "in_progress",
  "passes": false,
  "validation": {
    "criteria": [
      "Transkript stiahnutý a spracovaný",
      "Calibration report vytvorený",
      "Gaps identifikované"
    ],
    "last_tested": null
  },
  "next_steps": [...],
  "blockers": []
}
```

### Field Definície

| Field | Typ | Popis |
|-------|-----|-------|
| `passes` | boolean | Či quest spĺňa všetky kritériá |
| `validation.criteria` | array | Zoznam kritérií (Definition of Done) |
| `validation.last_tested` | string/null | ISO timestamp poslednej validácie |

### Pravidlá Konzistencie

1. Quest s `passes: true` musí mať `status: completed`
2. Quest s `passes: false` nemôže mať `status: completed`
3. Pri každom `/savegame` sa validujú všetky aktívne questy

### Health Check (`/loadgame`)

Pri každom `/loadgame` sa spustí health check:

```
🏥 Health Check - Anthropic Harness Pattern
==================================================
✅ SAVE_GAME_LATEST.json existuje
✅ JSON validný
✅ 4 questov nájdených
✅ Všetky questy majú správny formát (passes + validation)
✅ Konzistencia passes vs status OK
==================================================
🏁 Health Check dokončený
```

### Validácia (`/savegame`)

Pri každom `/savegame` sa validujú questy:

1. Pre každý `in_progress` quest:
   - Over kritériá
   - Ak všetky splnené → `passes: true`, `status: completed`
   
2. Aktualizuj `validation.last_tested`

### CLI Nástroj

```bash
# Health check
python scripts/utils/validate_quest.py --health-check

# List všetkých questov
python scripts/utils/validate_quest.py --list

# Interaktívna validácia konkrétneho questu
python scripts/utils/validate_quest.py --quest quest-15

# Označ quest ako pass/fail
python scripts/utils/validate_quest.py --mark-pass quest-15
python scripts/utils/validate_quest.py --mark-fail quest-15
```

### Mapping: Anthropic ↔ XVADUR

| Anthropic Koncept | XVADUR Implementácia |
|-------------------|---------------------|
| Domain Memory | `XVADUR_LOG.jsonl`, `SAVE_GAME_LATEST.json` |
| Initializer Agent | `.cursorrules`, `/loadgame` |
| Feature List | `SAVE_GAME_LATEST.json` → `quests[]` |
| Progress Log | `XVADUR_LOG.jsonl` |
| Self-verify Testing | `validate_quest.py`, `validation.criteria` |
| Harness | 3-Layer Architecture |

### Zdroje

- **Anthropic Article:** [Effective Harnesses for Long-Running Agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)
- **Nate Jones Video:** `development/data/youtube/xNcEgqzlPqs_metadata.json` (ak existuje)
- **Calibration Report:** `development/sessions/archive/december-2025/quests/analysis_nate_jones_calibration.md`

---

**Vytvorené:** 2025-12-04  
**Posledná aktualizácia:** 2025-12-09  
**Status:** ✅ Aktívny

