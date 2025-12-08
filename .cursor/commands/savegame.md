---
description: Uloží stav cez manifest + kompaktný JSON, minimalizuje tokeny a udrží logy ako headlines.
---

# SYSTEM PROMPT: MANIFEST-DRIVEN SAVEGAME

Cieľ: **aktualizovať `development/state_manifest.json` ako jediné vstupné miesto**
a uložiť stručný JSON savegame. Markdown logy slúžia len ako čitateľné headlines,
nie ako zdroj pravdy.

## 🔐 Poradie krokov

1) **Prompty & XP (povinné)**
- Ulož aktuálne user prompty cez existujúci skript (`development/data/prompts_log.jsonl`).
- Prepočítaj XP (`scripts.calculate_xp`) a zapíš **len JSON** (`development/logs/XVADUR_XP.json`).

2) **Zber stavu**
- Načítaj posledné logy priamo cez manifest (limit `log_window.main_last_n`).
- Zhrň aktuálny fokus/questy do krátkeho statusu (max ~10 viet celkovo).

3) **Kompaktný savegame (JSON)**
- Súbor: `development/sessions/save_games/SAVE_GAME_LATEST.json` (prepísať).
- Stručná štruktúra: metadata (timestamp), status (level/xp/streak), narrative.summary,
  quests, instructions/next steps. Žiadne duplicitné markdown copy.

4) **Aktualizuj manifest**
- `last_updated` nastav na aktuálne ISO.
- Udrž `paths` a `log_window` konzistentné; doplň `current_focus` a `active_project` podľa stavu.
- Ulož pomocou `StateManifest.save()`.

```python
from datetime import datetime
from core.state_manifest import StateManifest
manifest = StateManifest.load()
manifest.update(current_focus="...", active_project="...")
manifest.save()
```

5) **Logovanie (ľudská vrstva)**
- Do `development/logs/XVADUR_LOG.jsonl` pridaj udalosť savegame.
- Do `development/logs/XVADUR_LOG.md` pridaj krátku headline vetu (bez detailného stavu).

6) **Git commit & push**
- `git add` aktualizované JSON + manifest + log headlines.
- Commit napr. `chore(savegame): refresh manifest state` a pushni.

## ⚠️ Pravidlá
- **Žiadne markdown savegame** – stav žije v JSON + manifeste.
- **Token disciplína:** naratívny sumár drž krátky, nespisuj 50+ riadkov.
- **Nezapisuj duplicitné dáta** medzi JSON/Markdown.
- **Ak chýbajú kľúčové polia v manifeste**, vypýtaj si ich pred uložením.

Spúšťač: `/savegame`
