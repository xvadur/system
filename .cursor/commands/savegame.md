---
description: Uloží aktuálny kontext konverzácie do pracovného JSON súboru pre prenos do novej session.
---

# SYSTEM PROMPT: SAVE GAME

Tvojou úlohou je vytvoriť **"Save Game"** súbor, ktorý zachytáva aktuálny stav konverzácie pre plynulé načítanie v novej session.

**⚠️ KRITICKÉ:** Po vytvorení save game súboru MUSÍŠ automaticky commitnúť a pushnúť všetky zmeny na GitHub pomocou MCP operácií.

---

## 1. Získanie Aktuálneho Času

**KRITICKÉ:** VŽDY použiť MCP Time pre timestamp.

1. **Získať aktuálny čas:** Použi `mcp_MCP_DOCKER_get_current_time` 
2. **Formát:** ISO 8601 s timezone (napr. `2025-12-10T14:30:00+01:00`)
3. **Fallback:** Len ak MCP Time nie je dostupné, použij `datetime.now(timezone.utc)`

---

## 2. Extrakcia Dát z Konverzácie

### 2.1 Parsovanie session.md

**Načítaj:** `development/sessions/current/session.md`

**Extrahovať:**
- **Posledných 10 taskov** (nie len 3) z sekcie "## Tasks"
- **Formát parsing:** Nájsť sekciu "## Tasks" a extrahovať posledných 10 riadkov s `- [HH:MM]`
- **Struktúra:** Pre každý task extrahovať: time, task, files, status

**Príklad:**
```markdown
## Tasks
- [14:30] Implementácia automatického logovania - pridané pravidlá | Files: [.cursorrules] | Status: completed
- [15:00] Aktualizácia templates - zjednodušené session template | Files: [templates/session_template.md] | Status: completed
```

### 2.2 Získanie Zmenených Súborov

**Metódy (v poradí priority):**
1. **Z git status:** Použi `run_terminal_cmd` s `git status --porcelain` (ak je potrebné)
2. **Z konverzácie:** Extrahovať súbory, ktoré boli spomenuté alebo zmenené
3. **Z session.md:** Extrahovať súbory z "Files Changed" sekcie

### 2.3 Extrakcia Next Steps

**Z konverzácie:**
- Hľadať frázy: "ďalšie kroky", "next steps", "potrebujem", "chcem", "plánujem"
- Extrahovať konkrétne, akčné kroky (nie abstraktné)
- Ignorovať naratívne popisy

### 2.4 Extrakcia Blokátorov

**Z konverzácie:**
- Hľadať frázy: "blokátor", "problém", "výzva", "neviem", "zaseknutý"
- Extrahovať konkrétne blokátory (nie abstraktné)
- Ignorovať všeobecné problémy

### 2.5 Identifikácia Current Task

**Z konverzácie alebo session.md:**
- Posledný aktívny task
- Alebo aktuálna úloha, na ktorej sa pracuje

---

## 3. Generovanie Save Game JSON

**Formát:** Pracovný JSON (nie naratívny) - len konkrétne dáta

```json
{
  "last_updated": "YYYY-MM-DDTHH:MM:SS+00:00",
  "current_task": "[Konkrétna úloha]",
  "status": "in_progress|completed|blocked",
  "last_10_tasks": [
    {
      "time": "HH:MM",
      "task": "[Názov tasku]",
      "files": ["cesta/k/súboru.py"],
      "status": "completed|in_progress"
    }
  ],
  "files_changed": ["cesta/k/súboru.py"],
  "next_steps": [
    "Konkrétny krok 1",
    "Konkrétny krok 2"
  ],
  "blockers": [
    "Blokátor 1",
    "Blokátor 2"
  ]
}
```

**Ulož do:** `development/sessions/save_games/SAVE_GAME.json`

**KRITICKÉ:**
- `last_updated` získavať cez MCP Time s timezone
- Pracovný formát (nie naratívny) - len konkrétne dáta
- Posledných 10 taskov (nie len 3)

---

## 4. Git Commit & Push (Automatické - POVINNÉ)

**⚠️ DÔLEŽITÉ:** Po vytvorení save game súboru MUSÍŠ automaticky commitnúť a pushnúť všetky zmeny.

**🎯 PRIORITA:** Použi MCP GitHub operácie namiesto subprocess git príkazov.

### Postup:

1. **Zisti, čo sa zmenilo:**
   - Použi `read_file` na načítanie zmien
   - Zahrň všetky zmenené súbory (vrátane SAVE_GAME.json)

2. **Použi MCP GitHub operácie (PRIORITA):**
   - Použi `mcp_MCP_DOCKER_push_files` nástroj priamo
   - Fallback: Použi `scripts/mcp_helpers.git_commit_via_mcp()` (ak MCP zlyhá)

3. **Commit message formát:**
   ```
   savegame: [YYYY-MM-DD] - [Krátky popis toho, čo sa robilo v session]
   ```

---

## 💡 Kedy použiť `/savegame`

- Pred ukončením konverzácie
- Pred začatím novej témy/projektu
- Po dosiahnutí významného milestone
- Na konci pracovného dňa

**Čo Save Game zachytáva:**
- Aktuálna úloha
- Posledných 10 taskov z session
- Zmenené súbory
- Následné kroky (konkrétne)
- Blokátory (konkrétne)

---

**Spúšťač:** `/savegame`
