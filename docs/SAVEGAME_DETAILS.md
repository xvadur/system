# 💾 SAVEGAME - Technické Detaily

**Poznámka:** Tento súbor obsahuje technické detaily pre `/savegame` command. Základné inštrukcie sú v `.cursor/commands/savegame.md`.

---

## Automatické Uloženie Promptov (Krok 0)

**⚠️ KRITICKÉ:** Pred vytvorením save game MUSÍŠ automaticky uložiť všetky user prompty z aktuálnej konverzácie.

### Postup:

```python
import sys
from pathlib import Path
from datetime import datetime
sys.path.insert(0, str(Path.cwd()))

from scripts.utils.save_conversation_prompts import save_prompts_batch

# Automaticky zbier všetky user prompty z aktuálnej konverzácie
prompts_to_save = []

# Pre každý user prompt v konverzácii:
# prompts_to_save.append({
#     'content': 'text promptu',
#     'metadata': {
#         'session': datetime.now().strftime('%Y-%m-%d'),
#         'source': 'savegame',
#         'extracted_at': datetime.now().isoformat()
#     }
# })

saved_count = save_prompts_batch(prompts_to_save)
print(f"✅ Uložených {saved_count} promptov z konverzácie")
```

**Poznámka:**
- Skript automaticky detekuje duplikáty a uloží len nové prompty
- Prompty sa ukladajú do `development/data/prompts_log.jsonl` cez `MinisterOfMemory` a `FileStore`

---

## Automatický Výpočet XP (Krok 0.5)

**⚠️ DÔLEŽITÉ:** Po uložení promptov MUSÍŠ automaticky vypočítať a aktualizovať XP.

### Postup:

```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd()))

from core.xp.calculator import calculate_xp, update_xp_file

# Vypočítaj XP z logu a promptov
xp_data = calculate_xp()

# Aktualizuj XVADUR_XP.md
update_xp_file('development/logs/XVADUR_XP.md', xp_data)

print(f"✅ XP vypočítané: {xp_data['total_xp']} XP (Level {xp_data['current_level']})")
```

**Automatizácia:**
- Parsuje `logs/XVADUR_LOG.md` (záznamy, súbory, úlohy)
- Parsuje `development/data/prompts_log.jsonl` (prompty, word count)
- Počíta streak dní
- Počíta level podľa exponenciálneho systému
- Aktualizuje `development/logs/XVADUR_XP.md` s novými hodnotami

---

## Načítanie Promptov z MinisterOfMemory

Použi Python kód na načítanie posledných promptov:

```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd()))

try:
    from core.ministers.memory import MinisterOfMemory, AssistantOfMemory
    from core.ministers.storage import FileStore
    
    prompts_log_path = Path("development/data/prompts_log.jsonl")
    if prompts_log_path.exists():
        file_store = FileStore(prompts_log_path)
        assistant = AssistantOfMemory(store=file_store)
        minister = MinisterOfMemory(assistant=assistant)
        
        # Načítaj posledných 50 promptov
        recent_prompts = minister.review_context(limit=50)
        # Vytvor sumarizáciu
        narrative_brief = minister.narrative_brief(limit=50)
        
        # Použi tieto dáta pri vytváraní naratívneho kontextu
except Exception as e:
    # Ak MinisterOfMemory nie je dostupný, pokračuj bez neho
    recent_prompts = []
    narrative_brief = ""
```

---

## Generovanie Markdown Obsahu

### Štruktúra:

```markdown
# 💾 SAVE GAME: [Dátum] [Čas]

---

## 📊 Status
- **Rank:** [Rank - odvodiť z Level alebo použiť existujúci]
- **Level:** [Level - z kroku 0.5, xp_data['current_level']]
- **XP:** [Current XP] / [Next Level XP] ([Percent]%)
- **Streak:** [X] dní
- **Last Log:** [Link na log]

## 🧠 Naratívny Kontext (Story so far)

[Generuj podrobný naratív z poslednej konverzácie, minimálne 10 viet. Pokry tieto dimenzie:]

1. **Začiatok session:** Ako sme štartovali túto iteráciu?
2. **Kľúčové rozhodnutia:** Aké zásadné voľby alebo pivoty nastali?
3. **Tvorba nástrojov/skriptov:** Čo bolo vytvorené alebo refaktorované?
4. **Introspektívne momenty:** Aké dôležité Aha-momenty sa objavili?
5. **Strety so systémom:** Kde vznikla frikcia?
6. **Gamifikačný progres:** Koľko XP/Level bolo získaných?
7. **Prepojenie s dlhodobou víziou:** Ako sa aktuálne rozhodnutia viažu na Magnum Opus?
8. **Otvorené slučky:** Aké questy/blokátory ostávajú riešiť?
9. **Analytické poznámky:** Výrazné vzorce v myslení alebo štýle
10. **Sumarizácia:** Krátky záver s odporúčaním pre ďalšie kroky

## 🎯 Aktívne Questy & Next Steps
- [Quest 1]
- [Quest 2]

## ⚠️ Inštrukcie pre Nového Agenta
[Čo má agent vedieť o užívateľovi a štýle komunikácie?]
```

---

## JSON Štruktúra

**Umiestnenie:** `development/sessions/save_games/SAVE_GAME_LATEST.json`

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
    "summary": "...",
    "key_decisions": [...],
    "key_moments": [...],
    "tools_created": [...],
    "open_loops": [...]
  },
  "quests": [...],
  "instructions": {...}
}
```

**Automatizácia:** Použi helper skript `scripts/generate_savegame_json.py` na generovanie JSON z Markdown

---

## Git Commit & Push (Krok 4)

**⚠️ KRITICKÉ:** Po vytvorení save game súboru MUSÍŠ automaticky commitnúť a pushnúť všetky zmeny na GitHub.

### MCP Priority (Priorita)

**A) Ak je MCP dostupné (Cursor IDE kontext):**

Použi MCP `push_files` nástroj priamo:

```python
# V Cursor IDE kontexte - AI môže volať MCP priamo:
from pathlib import Path
import subprocess

# Zisti zmenené súbory
result = subprocess.run(['git', 'status', '--porcelain'], capture_output=True, text=True)
changed_files = [line.split()[-1] for line in result.stdout.strip().split('\n') if line]

# Načítaj obsah súborov
files_to_push = []
for file_path in changed_files:
    if Path(file_path).exists():
        content = Path(file_path).read_text(encoding='utf-8')
        files_to_push.append({
            "path": file_path,
            "content": content
        })

# Volaj MCP push_files priamo (ak je dostupné)
# mcp_MCP_DOCKER_push_files(
#     owner="xvadur",
#     repo="system",
#     branch="main",
#     files=files_to_push,
#     message=f"savegame: {date} - {summary}"
# )
```

**B) Ak MCP nie je dostupné (fallback):**

Použi `git_commit_via_mcp()` helper funkciu:

```python
from scripts.mcp_helpers import git_commit_via_mcp
from pathlib import Path
import subprocess

# Zisti zmenené súbory
result = subprocess.run(['git', 'status', '--porcelain'], capture_output=True, text=True)
changed_files = [line.split()[-1] for line in result.stdout.strip().split('\n') if line]

# Commit + Push cez helper (fallback na subprocess)
success = git_commit_via_mcp(
    message=f"savegame: {date} - {summary}",
    files=changed_files if changed_files else None  # None = všetky zmeny
)

if success:
    print("✅ Save game commitnutý a pushnutý")
else:
    print("⚠️  Chyba pri commitnutí/pushnutí")
```

### Commit Message Formát

```
savegame: [YYYY-MM-DD] - [Krátky popis toho, čo sa robilo v session]
```

**Príklady:**
- `savegame: 2025-12-09 - MCP integrácia do savegame workflow`
- `savegame: 2025-12-09 - XP systém revízia, nové slash commands`
- `savegame: 2025-12-09 - Context Engineering optimalizácia`

### Čo sa automaticky pushne:

- ✅ Save game súbor (`development/sessions/save_games/SAVE_GAME_LATEST.md`)
- ✅ Save game JSON (`development/sessions/save_games/SAVE_GAME_LATEST.json`)
- ✅ Save game summary (`development/sessions/save_games/SAVE_GAME_LATEST_SUMMARY.md`)
- ✅ Aktualizované logy (`development/logs/XVADUR_LOG.md`, `development/logs/XVADUR_XP.md`)
- ✅ Všetky ostatné zmenené súbory v workspace

---

## Quest Validácia (Anthropic Harness Pattern)

**Prečo Quest Validácia?**

Podľa [Anthropic engineering article](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents),
agent by mal vždy aktualizovať stav questov pred uložením. Toto zabezpečuje, že `passes` field je vždy aktuálny.

**Postup:**

1. **Pre každý quest v `in_progress` stave:**
   - Over, či sú splnené všetky `validation.criteria`
   - Ak áno, nastav `passes: true` a `status: completed`
   - Ak nie, ponechaj `passes: false`

2. **Aktualizuj `validation.last_tested`:**
   - Nastav aktuálny timestamp pre všetky validované questy

**Quest Schema:**

```json
{
  "id": "quest-15",
  "title": "Quest #15: ...",
  "status": "in_progress",
  "passes": false,
  "validation": {
    "criteria": [
      "Kritérium 1 splnené",
      "Kritérium 2 splnené"
    ],
    "last_tested": "2025-12-09T03:00:00Z"
  },
  "next_steps": [...],
  "blockers": []
}
```

**Pravidlá:**
- Quest s `passes: true` musí mať `status: completed`
- Quest s `passes: false` nemôže mať `status: completed`
- `validation.criteria` definuje "Definition of Done" pre quest
- `validation.last_tested` sa aktualizuje pri každej validácii

**Automatická validácia:**

```bash
python scripts/utils/validate_quest.py --list
```

**Dokumentácia:** Viď `docs/QUEST_SYSTEM.md` pre kompletný popis Anthropic Harness Pattern integrácie.

---

**Vytvorené:** 2025-12-09  
**Účel:** Technické detaily pre `/savegame` command

