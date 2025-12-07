# 📋 Štrukturovaný Kontextový Systém

**Účel:** Optimalizovať token spotrebu pri `/loadgame` a `/savegame` commands cez štrukturované JSON formáty.

**Status:** ✅ Implementované (Quest #7)  
**Posledná aktualizácia:** 2025-12-05 (Zjednodušený systém - odstránené SUMMARY súbory)

---

## 🎯 Prehľad

Systém používa **hybridný prístup** - zachováva Markdown pre ľudí a pridáva JSON pre AI:

```
development/
├── logs/
│   ├── XVADUR_LOG.md          # Čitateľný Markdown (pre ľudí)
│   └── XVADUR_LOG.jsonl        # Štrukturovaný JSONL (pre AI)
├── sessions/
│   └── save_games/
│       ├── SAVE_GAME.md            # Chronologický Markdown (appenduje sa, pre ľudí)
│       └── SAVE_GAME_LATEST.json   # Najnovší JSON (prepísuje sa, pre AI)
└── logs/
    ├── XVADUR_XP.md           # Čitateľný Markdown (pre ľudí)
    └── XVADUR_XP.json          # Štrukturovaný JSON (pre AI)
```

---

## 📊 Formáty

### 1. Log Entry (JSONL)

**Súbor:** `development/logs/XVADUR_LOG.jsonl`

**Formát:** Jeden JSON objekt na riadok (JSONL)

```json
{
  "timestamp": "2025-12-05T08:00:00Z",
  "date": "2025-12-05",
  "time": "08:00",
  "title": "Session: GitHub Logika & Session Rotation Systém",
  "type": "session",
  "completed": [
    "Presun MCP_INTEGRATION.md z docs/ do core/mcp/README.md",
    "Aktualizácia SESSION_MANAGEMENT.md dokumentácie"
  ],
  "results": {
    "mcp_dokumentacia": "Presunutá na správne miesto v core/mcp/",
    "session_rotation": "Automatický merge branch o polnoci"
  },
  "decisions": [
    "GitHub branch strategy: session-YYYY-MM-DD branches",
    "Časový plán: 00:00 UTC (merge + archivácia)"
  ],
  "files_changed": [
    {"path": "core/mcp/README.md", "action": "created", "desc": "nová MCP dokumentácia"},
    {"path": "docs/SESSION_MANAGEMENT.md", "action": "updated", "desc": "aktualizovaná s novou logikou"}
  ],
  "status": "completed",
  "xp_estimate": 8.0
}
```

**Úspora tokenov:** ~70% (štruktúrované dáta namiesto naratívu)

---

### 2. Save Game (JSON)

**Súbor:** `development/sessions/save_games/SAVE_GAME_LATEST.json`  
**Poznámka:** Vždy len najnovší JSON (prepísanie pri každom `/savegame`)

**Formát:** Jeden JSON objekt

```json
{
  "metadata": {
    "created_at": "2025-12-05T20:45:00Z",
    "session_date": "2025-12-05",
    "session_name": "Piatok 2025-12-05"
  },
  "status": {
    "rank": "AI Developer",
    "level": 1,
    "xp": 0.0,
    "xp_next_level": 10.0,
    "xp_percent": 0.0,
    "streak_days": 0
  },
  "narrative": {
    "summary": "Naša dnešná session začala identifikáciou kritického problému...",
    "key_decisions": [
      "Migrácia na lokálny scheduler (cost-saving)",
      "Jeden master skript namiesto troch schedulerov"
    ],
    "key_moments": [
      "Zistil si, že dlhuješ GitHubu 30€",
      "Navrhli sme štrukturované formáty namiesto naratívnych dokumentov"
    ],
    "tools_created": [
      {"name": "daily_rotation.py", "path": "scripts/daily_rotation.py", "desc": "Master skript pre dennú rotáciu"}
    ],
    "open_loops": [
      "Refaktorovanie kontextu pre token optimalizáciu",
      "Testovanie lokálneho scheduleru"
    ]
  },
  "quests": [
    {
      "id": "refaktorovanie-kontextu",
      "title": "Refaktorovanie kontextu - optimalizácia token spotreby",
      "status": "new",
      "next_steps": [
        "Navrhnúť štrukturované formáty (JSON/YAML) pre logy a save games",
        "Vytvoriť migračné skripty"
      ],
      "blockers": []
    }
  ],
  "instructions": {
    "for_agent": [
      "Prezident migruje z GitHub Actions na lokálny scheduler (cost-saving)",
      "Identifikovaná potreba optimalizácie token spotreby cez štrukturované formáty"
    ],
    "style": [
      "Preferuje jednoduché, efektívne riešenia",
      "Rýchlo sa rozhoduje pri identifikácii problémov"
    ]
  }
}
```

**Úspora tokenov:** ~70% (štruktúrované dáta + kompaktný naratív)

---

### 3. XP Status (JSON)

**Súbor:** `development/logs/XVADUR_XP.json`

**Formát:** Jeden JSON objekt

```json
{
  "timestamp": "2025-12-05T20:41:00Z",
  "status": {
    "total_xp": 0.0,
    "level": 1,
    "next_level_xp": 10.0,
    "xp_needed": 10.0,
    "xp_percent": 0.0,
    "streak_days": 0
  },
  "breakdown": {
    "from_work": {
      "entries": {"count": 0, "xp_per_entry": 0.5, "total": 0.0},
      "files_changed": {"count": 0, "xp_per_file": 0.1, "total": 0.0},
      "tasks_completed": {"count": 0, "xp_per_task": 0.5, "total": 0.0},
      "subtotal": 0.0
    },
    "from_activity": {
      "prompts": {"count": 0, "xp_per_prompt": 0.1, "total": 0.0},
      "word_count": {"count": 0, "xp_per_1000_words": 0.5, "total": 0.0},
      "subtotal": 0.0
    },
    "bonuses": {
      "streak": {"days": 0, "xp_per_day": 0.2, "total": 0.0},
      "sessions": {"count": 0, "xp_per_session": 1.0, "total": 0.0},
      "subtotal": 0.0
    }
  },
  "total": 0.0
}
```

**Úspora tokenov:** ~50% (štruktúrované dáta namiesto textu)

---

## 📝 Zmeny v Systéme (2025-12-05)

**Zjednodušenie:**
- ❌ Odstránené `SAVE_GAME_LATEST_SUMMARY.md` a `SAVE_GAME_LATEST_SUMMARY.json`
- ✅ `SAVE_GAME.md` - appenduje sa (chronologický záznam pre ľudí)
- ✅ `SAVE_GAME_LATEST.json` - vždy len najnovší JSON (pre AI pri `/loadgame`)

**Výhody:**
- Jednoduchší systém (menej súborov)
- Chronologická dokumentácia v jednom súbore
- JSON vždy obsahuje len najnovší stav (efektívne pre `/loadgame`)

---

## 🔄 Workflow

### `/loadgame` Command

**Priorita:** JSON formáty (ak existujú), fallback na Markdown

1. **Save Game:**
   - Skús načítať `SAVE_GAME_LATEST.json` (vždy len najnovší)
   - Ak neexistuje, použij `SAVE_GAME.md` (len posledný záznam - od posledného `# 💾 SAVE GAME:` do `---`)

2. **Log:**
   - Skús načítať `XVADUR_LOG.jsonl` (posledných 5 záznamov)
   - Ak neexistuje, použij `XVADUR_LOG.md` (selektívne načítanie)

3. **XP Status:**
   - Skús načítať `XVADUR_XP.json`
   - Ak neexistuje, použij `XVADUR_XP.md` (len status sekcia)

4. **Profil:**
   - Zostáva Markdown (`xvadur_profile.md`)

**Výsledok:** ~40% úspora tokenov oproti pôvodnému Markdown

---

### `/savegame` Command

**Generuje oba formáty:** Markdown (append) + JSON (prepísanie)

1. **Vytvor Markdown (appenduje sa):**
   - `SAVE_GAME.md` - pridaj nový záznam na koniec súboru
   - Chronologický záznam všetkých session (pre ľudí)

2. **Vytvor JSON (prepísanie):**
   - `SAVE_GAME_LATEST.json` - vždy len najnovší JSON (prepísanie)
   - Automaticky generované pomocou `scripts/generate_savegame_json.py`

3. **Aktualizuj Log:**
   - Pridaj záznam do `XVADUR_LOG.md` (Markdown)
   - Pridaj záznam do `XVADUR_LOG.jsonl` (JSONL)

4. **Aktualizuj XP:**
   - Aktualizuj `XVADUR_XP.md` (Markdown)
   - Aktualizuj `XVADUR_XP.json` (JSON)

**Automatizácia:** JSON sa generuje automaticky pomocou helper skriptu pri `/savegame`

---

## 🛠️ Migrácia

### Migračný Skript

**Súbor:** `scripts/migrate_to_structured_format.py`

**Použitie:**
```bash
# Dry run (len zobrazí, čo by sa migrovalo)
python3 scripts/migrate_to_structured_format.py --dry-run

# Skutočná migrácia
python3 scripts/migrate_to_structured_format.py

# S backupom pôvodných súborov
python3 scripts/migrate_to_structured_format.py --backup
```

**Čo migruje:**
- `XVADUR_LOG.md` → `XVADUR_LOG.jsonl`
- `SAVE_GAME_LATEST.md` → `SAVE_GAME_LATEST.json`
- `SAVE_GAME_LATEST_SUMMARY.md` → `SAVE_GAME_LATEST_SUMMARY.json`
- `XVADUR_XP.md` → `XVADUR_XP.json`

**Bezpečnosť:**
- Markdown súbory zostávajú nezmenené (backward compatibility)
- JSON súbory sa vytvárajú ako nové súbory
- Môžeš použiť `--backup` pre vytvorenie backupu

---

## 📈 Výsledky

### Token Úspora

**Pred optimalizáciou (Markdown):**
- Save Game Summary: ~2,100 tokenov
- Log (5 záznamov): ~3,000 tokenov
- XP Status: ~600 tokenov
- Profil: ~1,500 tokenov
- **Celkom:** ~7,200 tokenov

**Po optimalizácii (JSON):**
- Save Game Summary: ~1,500 tokenov (-29%)
- Log (5 záznamov): ~900 tokenov (-70%)
- XP Status: ~450 tokenov (-25%)
- Profil: ~1,500 tokenov (zostáva Markdown)
- **Celkom:** ~4,350 tokenov (-40%)

**Celková úspora:** ~40% tokenov pri `/loadgame`

---

## 🔧 Implementácia

### Komponenty

1. **Návrh formátov:** `development/docs/CONTEXT_FORMAT_DESIGN.md`
2. **Migračný skript:** `scripts/migrate_to_structured_format.py`
3. **Aktualizované commands:**
   - `.cursor/commands/loadgame.md` (JSON priorita)
   - `.cursor/commands/savegame.md` (generovanie JSON + Markdown)

### Backward Compatibility

- ✅ Markdown súbory zostávajú nezmenené
- ✅ `/loadgame` funguje s Markdown aj JSON
- ✅ `/savegame` generuje oba formáty
- ✅ Migrácia je voliteľná (JSON sa vytvárajú automaticky)

---

## 📝 Poznámky

- **Profil zostáva Markdown:** Nie je kritický pre token optimalizáciu
- **Hybridný prístup:** Zachováva čitateľnosť pre ľudí, optimalizuje pre AI
- **Automatická generácia:** JSON sa vytvárajú automaticky pri `/savegame`
- **Queryable:** JSON formáty sa dajú ľahko parsovať a queryovať

---

**Status:** ✅ Implementované  
**Quest:** #7 - Refaktorovanie kontextu - optimalizácia token spotreby  
**Dokončené:** 2025-12-05

