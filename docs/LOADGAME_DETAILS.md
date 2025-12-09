# 📥 LOADGAME - Technické Detaily

**Poznámka:** Tento súbor obsahuje technické detaily pre `/loadgame` command. Základné inštrukcie sú v `.cursor/commands/loadgame.md`.

---

## Technické Detaily Pre Selektívne Načítanie

### Pre Save Game (JSON priorita)

```python
import json
from pathlib import Path

save_game_json = Path("development/sessions/save_games/SAVE_GAME_LATEST.json")
if save_game_json.exists():
    with open(save_game_json, 'r', encoding='utf-8') as f:
        data = json.load(f)
        # Extrahuj len kľúčové informácie:
        # - data['status'] (rank, level, xp)
        # - data['narrative']['summary'] (krátky sumár)
        # - data['quests'] (aktívne questy)
else:
    # Fallback na Markdown - načítaj len posledný záznam
    save_game_md = Path("development/sessions/save_games/SAVE_GAME.md")
    if save_game_md.exists():
        content = save_game_md.read_text(encoding='utf-8')
        # Nájdi posledný záznam (od posledného "# 💾 SAVE GAME:" do "---" alebo konca)
        last_entry_start = content.rfind("# 💾 SAVE GAME:")
        if last_entry_start != -1:
            last_entry = content[last_entry_start:]
            # Parsuj posledný záznam
```

### Pre log (JSONL priorita)

```python
import json
from pathlib import Path

log_jsonl = Path("development/logs/XVADUR_LOG.jsonl")
if log_jsonl.exists():
    entries = []
    with open(log_jsonl, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                entries.append(json.loads(line))
    # Vezmi posledných 5 záznamov
    recent_entries = entries[-5:]
else:
    # Fallback na Markdown (pôvodná logika)
    # Načítaj súbor a extrahuj posledných 5 záznamov
```

### Pre XP (JSON priorita)

```python
import json
from pathlib import Path

xp_json = Path("development/logs/XVADUR_XP.json")
if xp_json.exists():
    with open(xp_json, 'r', encoding='utf-8') as f:
        data = json.load(f)
        # Extrahuj len status sekciu
        status = data['status']
else:
    # Fallback na Markdown
    # Načítaj len sekciu "📊 Aktuálny Status"
```

### Pre profil (zostáva Markdown)

- Načítaj súbor `development/data/profile/xvadur_profile.md`
- Extrahuj len sekciu `## IV. SÚČASNÝ PROFIL: KTO JE ADAM?`
- Preskoč históriu a transformačné momenty

### Načítanie histórie promptov z MinisterOfMemory (voliteľné)

Ak existuje `data/prompts_log.jsonl`, môžeš načítať posledné prompty:

```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd()))

try:
    from core.ministers.memory import MinisterOfMemory, AssistantOfMemory
    from core.ministers.storage import FileStore
    
    prompts_log_path = Path("data/prompts_log.jsonl")
    if prompts_log_path.exists():
        file_store = FileStore(prompts_log_path)
        assistant = AssistantOfMemory(store=file_store)
        minister = MinisterOfMemory(assistant=assistant)
        
        # Načítaj posledných 20 promptov pre kontext
        recent_prompts = minister.review_context(limit=20)
        # Zobraz v summary, ak sú relevantné
except Exception:
    # Ak MinisterOfMemory nie je dostupný, pokračuj bez neho
    recent_prompts = []
```

---

## Context Engineering Integration

**Automatická optimalizácia tokenov pomocou Context Engineering komponentov.**

### Automatické Token Tracking

Po načítaní kontextu sa automaticky trackujú tokeny cez `TokenBudgetTracker`:

```python
from core.context_engineering.integration import load_context_with_optimization
from pathlib import Path

result = load_context_with_optimization(
    save_game_path=Path("development/sessions/save_games/SAVE_GAME_LATEST.json"),
    log_path=Path("development/logs/XVADUR_LOG.jsonl"),
    xp_path=Path("development/logs/XVADUR_XP.json"),
    prompts_log_path=Path("development/data/prompts_log.jsonl"),
    auto_compress=True,
    auto_isolate=True
)

# Výsledok obsahuje:
# - context_parts: Načítané komponenty kontextu
# - metrics: Token metriky
# - utilization: Utilization ratio (0.0-1.0)
# - compressed: Boolean - či bola aplikovaná kompresia
```

### Automatická Kompresia

Ak utilization > 80% (COMPRESSION_THRESHOLD), automaticky sa aplikuje `CompressContextManager`:

- **Threshold:** 80% utilization (konfigurovateľné v `context_engineering_config.json`)
- **Cieľový pomer:** 50% redukcia tokenov
- **Zachovanie:** Kľúčové informácie sú zachované

### Automatická Izolácia Kontextu

Pre nové questy sa automaticky izoluje kontext cez `IsolateContextManager`:

```python
from core.context_engineering.integration import isolate_context_for_task
from core.ministers.memory import MinisterOfMemory

minister = MinisterOfMemory(...)
isolation = minister.isolate_context_for_task(
    task_id="quest-20",
    task_description="Implementovať Context Engineering",
    keywords={"context", "engineering", "token"},
    limit=20
)

# Výsledok obsahuje:
# - isolated_content: Izolovaný obsah pre úlohu
# - token_count: Počet tokenov v izolovanom kontexte
# - relevant_records: Filtrované záznamy
```

### Python Helper Skript

Použi `scripts/utils/load_context_optimized.py` pre optimalizované načítanie:

```bash
# Načíta save game s optimalizáciou
python scripts/utils/load_context_optimized.py --save-game

# Načíta log entries s izoláciou pre úlohu
python scripts/utils/load_context_optimized.py --log --task "Implementovať Context Engineering"

# Vráti optimalizovaný sumár
python scripts/utils/load_context_optimized.py --summary --limit 10

# JSON výstup
python scripts/utils/load_context_optimized.py --save-game --log --json
```

### Konfigurácia

Konfigurácia je v `development/data/context_engineering_config.json`:

```json
{
  "compression_threshold": 0.8,
  "target_compression_ratio": 0.5,
  "context_window_size": 16000,
  "isolation_max_tokens": 800
}
```

---

## Health Check (Anthropic Harness Pattern)

**Prečo Health Check?**

Podľa [Anthropic engineering article](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents),
agent by mal vždy začať overením, že workspace je v čistom stave. Toto zabraňuje práci na broken codebase.

**Health Check Sekvencia:**

1. **Overiť štruktúru Questov:**
   - Každý quest musí mať `passes` a `validation` fields
   - Ak chýba, upozorniť užívateľa
   
2. **Skontrolovať konzistenciu:**
   - Quest s `passes: true` by mal mať `status: completed`
   - Quest s `status: in_progress` by mal mať `passes: false`

3. **Identifikovať failing questy:**
   - Zobraziť questy s `passes: false`
   - Odporučiť ktorý quest riešiť ako prvý

**Automatický Health Check (voliteľné):**

```bash
python scripts/utils/validate_quest.py --health-check
```

**Výstup Health Check:**

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

---

**Vytvorené:** 2025-12-09  
**Účel:** Technické detaily pre `/loadgame` command

