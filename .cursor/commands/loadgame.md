---
description: Načíta manifest a posledné logy pre okamžité pokračovanie s minimálnymi tokenmi.
---

# SYSTEM PROMPT: MANIFEST-DRIVEN LOADGAME

Tvojou úlohou je obnoviť kontext **primárne zo `development/state_manifest.json`**.
Manifest je jediný vstupný bod – všetko ostatné načítavaj len podľa ciest v ňom a s limitmi.

## 🔄 LOADGAME TOK-OPTIMAL FLOW

1) **Manifest ako zdroj pravdy**
- Súbor: `development/state_manifest.json`
- Účel: obsahuje cesty na savegame/logy a okno čítania.
- Ak manifest chýba, vytvor otázku pre užívateľa; nečítaj nič veľké navyše.

```python
from core.state_manifest import StateManifest
manifest = StateManifest.load()
status = manifest.status_report()
```

2) **Savegame (iba JSON)**
- Cesta: `manifest.resolve_path("savegame")`
- Načítaj len JSON (žiadny markdown fallback). Použi ho na stručný status/narratívny sumár.

```python
savegame = manifest.savegame_payload()
summary = savegame.get("narrative", {}).get("summary") if savegame else ""
```

3) **Logy s limitmi**
- Hlavný log: `manifest.resolve_path("log_main")` → načítaj **len posledných `main_last_n`** z JSONL.
- XP log: `manifest.resolve_path("log_xp")` → načítaj JSON status (žiadne markdown sekcie).
- Markdown logy používaj len na rýchle prelistovanie, nie ako zdroj stavu.

```python
recent_entries = manifest.recent_main_log_entries()
xp_status = manifest.xp_status()
```

4) **Profil (voliteľné)**
- `manifest.resolve_path("profile")` → načítaj len kľúčovú sekciu profilu, ak je potrebné.

5) **Výstup po načítaní**
- Stručný report: level/XP, current_focus, active_project, posledný checkpoint, posledné logy.
- Navrhni ďalšie kroky na základe `current_focus` a posledných logov.

## 🚀 Štartovacia Sekvencia
1. Potvrď manifest (čas `last_updated`).
2. Vypíš status (level/XP) + aktuálny quest/focus.
3. Zhrň posledné logy (max `main_last_n`).
4. Ponúkni pokračovanie alebo aktualizáciu manifestu, ak sa zmenil fokus.

## ❗ Pravidlá
- **Žiadne čítanie starých markdown savegame/log fallbackov** – manifest + JSON sú zdroj pravdy.
- **Token disciplína:** načítaj len to, čo určuje manifest (vrátane okien). Nepretriasaj históriu.
- **Ak manifest chýba alebo je neúplný:** pýtaj si údaje na jeho doplnenie pred ďalším čítaním.

Spúšťač: `/loadgame`
