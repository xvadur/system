---
description: Uloží aktuálny kontext konverzácie, stav gamifikácie a naratív do súboru pre prenos do novej session.
---

# SYSTEM PROMPT: CONTEXT SAVE GAME

Tvojou úlohou je vytvoriť **"Save Game"** súbor, ktorý zachytáva aktuálny stav konverzácie a gamifikácie, aby mohol byť plynule načítaný v novej session.

**⚠️ KRITICKÉ:** Po vytvorení save game súboru MUSÍŠ automaticky commitnúť a pushnúť všetky zmeny na GitHub pomocou git príkazov alebo MCP operácií.

---

## 0. TOKEN OPTIMIZATION (KRITICKÉ - PRVÝ KROK)

**⚠️ DÔLEŽITÉ:** Pred začatím `/savegame` MUSÍŠ použiť optimalizovaný workflow s context engineeringom.

**Použi `scripts/utils/optimized_savegame.py` → `OptimizedSaveGame`:**

```python
from scripts.utils.optimized_savegame import OptimizedSaveGame

optimizer = OptimizedSaveGame()
```

**Tento modul automaticky:**
- Trackuje tokeny cez `TokenBudgetTracker`
- Používa selektívne načítanie súborov (offset/limit, sekcie)
- Aplikuje kompresiu keď utilization > 80%
- Izoluje relevantný kontext pre úlohu

**PRAVIDLÁ:**
- **NIKDY nečítaj celé súbory** - používaj `read_file_selective()` alebo `read_file` s `offset`/`limit`
- **PRIORITA JSON formátov** - rýchlejšie a menšie než Markdown
- **Trackuj tokeny** - používaj `tracker.estimate_tokens()` pred každým read_file
- **Aplikuj kompresiu** - ak utilization > 80%, použij `CompressContextManager`

---

## 0.5. Automatické Uloženie Promptov (POVINNÉ)

**⚠️ KRITICKÉ:** Pred vytvorením save game MUSÍŠ automaticky uložiť všetky user prompty.

**Použi optimalizovanú verziu:**
```python
prompts_to_save = [...]  # Zoznam promptov z konverzácie
saved_count = optimizer.save_prompts_optimized(prompts_to_save)
```

**Automaticky:**
- Uloží prompty cez `save_prompts_batch()`
- Skontroluje utilization po uložení
- Aplikuje kompresiu ak utilization > 80%

---

## 0.6. Automatický Výpočet XP (POVINNÉ)

**⚠️ DÔLEŽITÉ:** Po uložení promptov MUSÍŠ automaticky vypočítať XP.

**Použi optimalizovanú verziu:**
```python
xp_data = optimizer.calculate_xp_optimized()
```

**Automaticky:**
- Vypočíta XP z logu a promptov
- Aktualizuje `XVADUR_XP.md` a `.json`
- Vráti XP data pre save game

---

## 1. Analýza Stavu (SELEKTÍVNE NAČÍTANIE)

**⚠️ KRITICKÉ:** Používaj selektívne načítanie namiesto celých súborov!

**Použi optimalizované metódy:**
```python
# XP Status - len status sekcia
xp_status = optimizer.get_xp_status()

# Posledné log záznamy - len posledných 5
recent_logs = optimizer.get_recent_log_entries(limit=5)

# Posledný save game - len summary
latest_summary = optimizer.get_latest_save_game_summary()
```

**NIKDY:**
- ❌ `read_file('development/logs/XVADUR_LOG.md')` - celý súbor!
- ✅ `read_file('development/logs/XVADUR_LOG.jsonl', offset=-5)` - len posledných 5
- ✅ `read_file('development/logs/XVADUR_XP.json')` - JSON je malý
- ✅ `optimizer.get_recent_log_entries(limit=5)` - optimalizovaná metóda

---

## 2. Generovanie Obsahu

Vytvor Markdown obsah s touto štruktúrou:

```markdown
# 💾 SAVE GAME: [Dátum] [Čas]

---

## 📊 Status
- **Rank:** [Rank]
- **Level:** [Level]
- **XP:** [Current XP] / [Next Level XP] ([Percent]%)
- **Streak:** [X] dní

## 🧠 Naratívny Kontext (Story so far)

[Generuj podrobný naratív z poslednej konverzácie, minimálne 10 viet. Pokry:]
1. Začiatok session
2. Kľúčové rozhodnutia
3. Tvorba nástrojov/skriptov
4. Introspektívne momenty
5. Strety so systémom
6. Gamifikačný progres
7. Prepojenie s dlhodobou víziou
8. Otvorené slučky
9. Analytické poznámky
10. Sumarizácia

## 🎯 Aktívne Questy & Next Steps
- [Quest 1]
- [Quest 2]

## ⚠️ Inštrukcie pre Nového Agenta
[Čo má agent vedieť o užívateľovi a štýle komunikácie?]
```

**Detaily:** Pozri `docs/SAVEGAME_DETAILS.md` pre kompletnú šablónu

---

## 3. Uloženie (OPTIMALIZOVANÉ)

**Použi optimalizovanú metódu:**
```python
save_game = optimizer.create_save_game_optimized(
    narrative=narrative_text,
    quests=quests_list,
    instructions=instructions_dict
)
```

**Automaticky:**
- Načíta len potrebné dáta (selektívne)
- Vytvorí save game objekt
- Uloží JSON (`SAVE_GAME_LATEST.json`)
- Appendne Markdown (`SAVE_GAME.md`) - len nový záznam

**Dodatočné aktualizácie:**
- XP už aktualizované v kroku 0.6
- Log záznamy - použij `log_task_completed()` z `log_manager.py`
- Prompty už uložené v kroku 0.5

**Token tracking:**
```python
metrics = optimizer.tracker.get_metrics_summary()
print(f"Token usage: {metrics['utilization_ratio']:.2%}")
```

---

## 4. Git Commit & Push (Automatické - POVINNÉ)

**⚠️ DÔLEŽITÉ:** Po vytvorení save game súboru MUSÍŠ automaticky commitnúť a pushnúť všetky zmeny.

**🎯 PRIORITA:** Použi MCP GitHub operácie namiesto subprocess git príkazov.

### Postup:

1. **Zisti, čo sa zmenilo:**
   - `git status --short` na zistenie všetkých zmien
   - Zahrň všetky zmenené súbory

2. **Použi MCP GitHub operácie (PRIORITA):**
   - Ak je MCP dostupné: Použi `mcp_MCP_DOCKER_push_files` nástroj priamo
   - Fallback: Použi `scripts/mcp_helpers.git_commit_via_mcp()` (fallback na subprocess)

3. **Commit message formát:**
   ```
   savegame: [YYYY-MM-DD] - [Krátky popis toho, čo sa robilo v session]
   ```

**Detaily:** Pozri `docs/SAVEGAME_DETAILS.md` pre MCP integráciu

---

## 4.5. Quest Validácia (Anthropic Harness Pattern)

**Postup:**
- Pre každý quest v `in_progress` stave over `validation.criteria`
- Ak sú splnené, nastav `passes: true` a `status: completed`
- Aktualizuj `validation.last_tested`

**Automatická validácia:**
```bash
python scripts/utils/validate_quest.py --list
```

**Detaily:** Pozri `docs/SAVEGAME_DETAILS.md` a `docs/QUEST_SYSTEM.md`

---

## 💡 IDE-Based Workflow Kontext

**Kedy použiť `/savegame`:**
- Pred ukončením konverzácie
- Pred začatím novej témy/projektu
- Po dosiahnutí významného milestone
- Na konci pracovného dňa

**Čo Save Game zachytáva:**
- Naratívny kontext (kompletný príbeh session)
- Gamifikačný stav (XP, Level, Rank, progres)
- Aktívne questy
- Inštrukcie pre agenta

---

**Spúšťač:** `/savegame`  
**Dokumentácia:** `docs/SAVEGAME_DETAILS.md` (technické detaily)
