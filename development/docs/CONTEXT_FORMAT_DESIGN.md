# 📋 Návrh Štrukturovaných Formátov pre Kontext

**Cieľ:** Optimalizovať token spotrebu pri `/loadgame` a `/savegame` cez štrukturované formáty (JSON) namiesto naratívnych Markdown dokumentov.

**Výhody:**
- ✅ Kompaktnejšie (menej tokenov)
- ✅ Queryable (ľahko parsovateľné)
- ✅ Typ-safe (štruktúrované dáta)
- ✅ Zachováva čitateľnosť Markdown pre ľudí

---

## 1. Log Entry Format (JSON)

### Aktuálny formát (Markdown):
```markdown
## [2025-12-05] 🔹 Session: GitHub Logika & Session Rotation Systém

**Vykonané:**
- ✅ Presun MCP_INTEGRATION.md z docs/ do core/mcp/README.md
- ✅ Aktualizácia SESSION_MANAGEMENT.md dokumentácie

**Hlavné Výsledky:**
- **MCP Dokumentácia:** Presunutá na správne miesto

**Zmeny v súboroch:**
- `core/mcp/README.md` - nová MCP dokumentácia
```

### Nový formát (JSON):
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

**Úspora tokenov:** ~60% (štruktúrované dáta namiesto naratívu)

---

## 2. Save Game Format (JSON)

### Aktuálny formát (Markdown):
```markdown
# 💾 SAVE GAME: 2025-12-05

## 📊 Status
- **Rank:** AI Developer
- **Level:** 1
- **XP:** 0.0 / 10 (0.0%)

## 🧠 Naratívny Kontext (Story so far)
Naša dnešná session začala identifikáciou kritického problému...
[~100 riadkov naratívu]

## 🎯 Aktívne Questy & Next Steps
### Refaktorovanie kontextu
- **Status:** 🆕 Nový quest
- **Next Steps:** Navrhnúť štrukturované formáty
```

### Nový formát (JSON):
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
    "summary": "Naša dnešná session začala identifikáciou kritického problému - GitHub Actions je spoplatnená služba...",
    "key_decisions": [
      "Migrácia na lokálny scheduler (cost-saving)",
      "Jeden master skript namiesto troch schedulerov"
    ],
    "key_moments": [
      "Zistil si, že dlhuješ GitHubu 30€",
      "Navrhli sme štrukturované formáty namiesto naratívnych dokumentov"
    ],
    "tools_created": [
      {"name": "daily_rotation.py", "path": "scripts/daily_rotation.py", "desc": "Master skript pre dennú rotáciu"},
      {"name": "git_helper.py", "path": "scripts/utils/git_helper.py", "desc": "Bezpečný git push helper"}
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

## 3. XP Tracking Format (JSON)

### Aktuálny formát (Markdown):
```markdown
## 📊 Aktuálny Status
- **Celkové XP:** 0.0
- **Level:** 1
- **Next Level:** 10 XP (potrebuje ešte 10.0 XP)
- **Streak:** 0 dní

## 💎 XP Breakdown
### Z Práce (Log)
- **Záznamy:** 0 × 0.5 = 0.0 XP
- **Zmeny súborov:** 0 × 0.1 = 0.0 XP
```

### Nový formát (JSON):
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

## 4. Hybridný Prístup (Odporúčaný)

**Zachovať Markdown pre ľudí, pridať JSON pre AI:**

```
development/
├── logs/
│   ├── XVADUR_LOG.md          # Čitateľný Markdown (pre ľudí)
│   └── XVADUR_LOG.jsonl        # Štrukturovaný JSONL (pre AI)
├── sessions/
│   └── save_games/
│       ├── SAVE_GAME_LATEST.md      # Čitateľný Markdown (pre ľudí)
│       ├── SAVE_GAME_LATEST.json    # Štrukturovaný JSON (pre AI)
│       ├── SAVE_GAME_LATEST_SUMMARY.md
│       └── SAVE_GAME_LATEST_SUMMARY.json
└── logs/
    ├── XVADUR_XP.md           # Čitateľný Markdown (pre ľudí)
    └── XVADUR_XP.json          # Štrukturovaný JSON (pre AI)
```

**Výhody:**
- ✅ Ľudia môžu čítať Markdown
- ✅ AI používa kompaktný JSON
- ✅ Obe formáty sa generujú automaticky
- ✅ Backward compatibility (Markdown zostáva)

---

## 5. Implementačný Plán

### Fáza 1: Návrh a schválenie
- ✅ Navrhnúť štruktúry (tento dokument)
- ⏳ Schváliť formáty s užívateľom

### Fáza 2: Migračné skripty
- Vytvoriť `scripts/migrate_to_structured_format.py`
- Konvertovať existujúce Markdown → JSON
- Validovať konverziu

### Fáza 3: Aktualizácia commands
- Aktualizovať `/savegame` na generovanie JSON + Markdown
- Aktualizovať `/loadgame` na načítanie JSON (fallback na Markdown)
- Testovať token úsporu

### Fáza 4: Dokumentácia
- Dokumentovať nové formáty
- Aktualizovať workflow dokumentáciu
- Vytvoriť migration guide

---

## 6. Odhadovaná Úspora Tokenov

**Aktuálne načítanie (`/loadgame`):**
- Save Game Summary: ~70 riadkov Markdown = ~2,100 tokenov
- Log (5 záznamov): ~100 riadkov = ~3,000 tokenov
- XP Status: ~20 riadkov = ~600 tokenov
- Profil: ~50 riadkov = ~1,500 tokenov
- **Celkom:** ~7,200 tokenov

**Po optimalizácii (JSON):**
- Save Game Summary: ~50 riadkov JSON = ~1,500 tokenov (-29%)
- Log (5 záznamov): ~30 riadkov JSON = ~900 tokenov (-70%)
- XP Status: ~15 riadkov JSON = ~450 tokenov (-25%)
- Profil: ~50 riadkov (zostáva Markdown) = ~1,500 tokenov
- **Celkom:** ~4,350 tokenov (-40%)

**Celková úspora:** ~40% tokenov pri `/loadgame`

---

**Status:** Návrh pripravený na review  
**Next Steps:** Schváliť formáty a začať implementáciu migračných skriptov

