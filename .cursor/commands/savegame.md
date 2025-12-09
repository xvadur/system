---
description: Uloží aktuálny kontext konverzácie, stav gamifikácie a naratív do súboru pre prenos do novej session.
---

# SYSTEM PROMPT: CONTEXT SAVE GAME

Tvojou úlohou je vytvoriť **"Save Game"** súbor, ktorý zachytáva aktuálny stav konverzácie a gamifikácie, aby mohol byť plynule načítaný v novej session.

**⚠️ KRITICKÉ:** Po vytvorení save game súboru MUSÍŠ automaticky commitnúť a pushnúť všetky zmeny na GitHub pomocou git príkazov alebo MCP operácií.

---

## 0. Automatické Uloženie Promptov (POVINNÉ - PRVÝ KROK)

**⚠️ KRITICKÉ:** Pred vytvorením save game MUSÍŠ automaticky uložiť všetky user prompty z aktuálnej konverzácie.

- Prejdi celú aktuálnu konverzáciu (od začiatku session)
- Identifikuj všetky user prompty (všetky správy od užívateľa)
- Ulož cez `scripts/utils/save_conversation_prompts.py` → `save_prompts_batch()`
- Prompty sa ukladajú do `development/data/prompts_log.jsonl`

**Technické detaily:** Pozri `docs/SAVEGAME_DETAILS.md`

---

## 0.5. Automatický Výpočet XP (POVINNÉ - PO ULOŽENÍ PROMPTOV)

**⚠️ DÔLEŽITÉ:** Po uložení promptov MUSÍŠ automaticky vypočítať a aktualizovať XP.

- Použi `core.xp.calculator.calculate_xp()` na výpočet XP
- Aktualizuj `development/logs/XVADUR_XP.md` a `.json`
- Použi hodnoty v save game naratíve

**Technické detaily:** Pozri `docs/SAVEGAME_DETAILS.md`

---

## 1. Analýza Stavu

Zisti aktuálne hodnoty z:
- `development/logs/XVADUR_XP.md` (XP, Level - už aktualizované v kroku 0.5)
- `development/logs/XVADUR_LOG.md` (posledné záznamy)
- `development/data/prompts_log.jsonl` (ak existuje - prompty z MinisterOfMemory)

Načítaj prompty z MinisterOfMemory (voliteľné) - pozri `docs/SAVEGAME_DETAILS.md`

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

## 3. Uloženie

Ulož obsah do **dvoch formátov**:

1. **Markdown:**
   - `development/sessions/save_games/SAVE_GAME.md` - **APPEND** (pridaj nový záznam)
   - Formát: `# 💾 SAVE GAME: [Dátum]` až `---` (separátor)

2. **JSON:**
   - `development/sessions/save_games/SAVE_GAME_LATEST.json` - **OVERWRITE** (vždy len najnovší)
   - Použi štruktúru z `docs/SAVEGAME_DETAILS.md`
   - Helper: `scripts/generate_savegame_json.py`

**Dodatočné aktualizácie:**
- Aktualizuj `development/logs/XVADUR_XP.md` a `.json`
- Pridaj záznam do `development/logs/XVADUR_LOG.md` a `.jsonl`
- Over, že všetky prompty sú uložené

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
