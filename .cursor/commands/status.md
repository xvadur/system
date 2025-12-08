---
description: Zobrazí rýchly stav z `development/state_manifest.json` bez čítania celej histórie.
---

# SYSTEM PROMPT: STATE MANIFEST STATUS

Použi manifest ako jediný vstup. Cieľ: vrátiť stručný stav (projekt, fokus,
XP, posledné logy) bez čítania ďalších súborov.

```python
from core.state_manifest import StateManifest
manifest = StateManifest.load()
report = manifest.status_report()
```

## Výstup
- last_updated, active_project, current_focus
- session.current_session_file + last_checkpoint
- XP status (level/xp/streak)
- Posledných `log_window.main_last_n` záznamov z JSONL
- Ak existuje, `narrative.summary` zo savegame JSON

## Pravidlá
- Nepoužívaj markdown fallbacky ani dlhé naratívy.
- Ak manifest chýba polia, vypýtaj si ich a navrhni doplnenie.
- Token disciplina: drž odpoveď do ~250 tokenov.

Spúšťač: `/status`
