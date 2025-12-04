---
description: Uloží aktuálny kontext konverzácie, stav gamifikácie a naratív do súboru pre prenos do novej session.
---

# SYSTEM PROMPT: CONTEXT SAVE GAME

Tvojou úlohou je vytvoriť **"Save Game"** súbor, ktorý zachytáva aktuálny stav konverzácie a gamifikácie, aby mohol byť plynule načítaný v novej session.

**⚠️ KRITICKÉ:** Po vytvorení save game súboru MUSÍŠ automaticky commitnúť a pushnúť všetky zmeny na GitHub pomocou git príkazov. Toto je povinný krok - bez neho sa zmeny nezachovajú.

## 0. Automatické Uloženie Promptov (POVINNÉ - PRVÝ KROK)

**⚠️ KRITICKÉ:** Pred vytvorením save game MUSÍŠ automaticky uložiť všetky user prompty z aktuálnej konverzácie.

### Postup:

1. **Automatická extrakcia promptov z konverzácie:**
   - Prejdi celú aktuálnu konverzáciu (od začiatku session)
   - Identifikuj všetky user prompty (všetky správy od užívateľa)
   - Zbieraj ich do zoznamu s metadátami

2. **Uloženie cez batch funkciu:**
   Použi Python kód na uloženie všetkých promptov naraz:
   ```python
   import sys
   from pathlib import Path
   from datetime import datetime
   sys.path.insert(0, str(Path.cwd()))
   
   from scripts.save_conversation_prompts import save_prompts_batch
   
   # Automaticky zbier všetky user prompty z aktuálnej konverzácie
   # (identifikuj ich z kontextu - všetky user messages v tejto session)
   prompts_to_save = []
   
   # PRÍKLAD: Ak máš prístup k histórii konverzácie, iteruj cez user messages
   # V Cursor môžeš identifikovať prompty z kontextu konverzácie
   # Každý user prompt pridaj do zoznamu:
   
   # Pre každý user prompt v konverzácii:
   # prompts_to_save.append({
   #     'content': 'text promptu',
   #     'metadata': {
   #         'session': datetime.now().strftime('%Y-%m-%d'),
   #         'source': 'savegame',
   #         'extracted_at': datetime.now().isoformat()
   #     }
   # })
   
   # AKTUÁLNE: Použi kontext z aktuálnej konverzácie
   # Zbier všetky user prompty, ktoré vidíš v tejto session
   # (môžeš ich identifikovať z user_query v kontexte)
   
   saved_count = save_prompts_batch(prompts_to_save)
   print(f"✅ Uložených {saved_count} promptov z konverzácie")
   ```

3. **Automatizácia:**
   Skript automaticky:
   - Detekuje duplikáty (porovnáva obsah promptov)
   - Uloží len nové prompty
   - Pridá metadáta (timestamp, source, session)

**Poznámka:** 
- Skript automaticky detekuje duplikáty a uloží len nové prompty
- Prompty, ktoré už existujú v `prompts_log.jsonl`, sa preskočia
- Každý prompt sa uloží s metadátami (timestamp, source: 'savegame', session dátum)

**Dôležité:** 
- Tento krok MUSÍ byť vykonaný PRED analýzou stavu a vytvorením save game súboru
- Agent MUSÍ automaticky identifikovať všetky user prompty z aktuálnej konverzácie
- Prompty sa ukladajú do `data/prompts_log.jsonl` cez `MinisterOfMemory` a `FileStore`

## 0.5. Automatický Výpočet XP (POVINNÉ - PO ULOŽENÍ PROMPTOV)

**⚠️ DÔLEŽITÉ:** Po uložení promptov MUSÍŠ automaticky vypočítať a aktualizovať XP.

### Postup:

1. **Spustiť XP calculation skript:**
   Použi Python kód na automatický výpočet XP:
   ```python
   import sys
   from pathlib import Path
   sys.path.insert(0, str(Path.cwd()))
   
   from scripts.calculate_xp import calculate_xp, update_xp_file
   
   # Vypočítaj XP z logu a promptov
   xp_data = calculate_xp()
   
   # Aktualizuj XVADUR_XP.md
   update_xp_file('logs/XVADUR_XP.md', xp_data)
   
   print(f"✅ XP vypočítané: {xp_data['total_xp']} XP (Level {xp_data['current_level']})")
   ```

2. **Automatizácia:**
   Skript automaticky:
   - Parsuje `logs/XVADUR_LOG.md` (záznamy, súbory, úlohy)
   - Parsuje `data/prompts_log.jsonl` (prompty, word count)
   - Počíta streak dní
   - Počíta level podľa exponenciálneho systému
   - Aktualizuje `xvadur/logs/XVADUR_XP.md` s novými hodnotami

3. **Použitie XP dát v save game:**
   - Zobraz XP breakdown v save game naratíve (sekcia "Gamifikačný progres")
   - Zahrň aktuálny level a XP v sekcii "📊 Status"

**Poznámka:**
- XP sa počíta automaticky z existujúcich dát (log + prompty)
- Žiadne manuálne výpočty nie sú potrebné
- XP sa aktualizuje pri každom `/savegame`

**Dôležité:**
- Tento krok MUSÍ byť vykonaný PO uložení promptov (krok 0)
- XP hodnoty sa použijú v save game naratíve (krok 2)

## 1. Analýza Stavu
Zisti aktuálne hodnoty z:
- `logs/XVADUR_XP.md` (XP, Level - už aktualizované v kroku 0.5)
- `logs/XVADUR_LOG.md` (posledné záznamy)
- `data/prompts_log.jsonl` (ak existuje - prompty z MinisterOfMemory)

**Poznámka:** XP hodnoty už boli automaticky vypočítané a aktualizované v kroku 0.5. Použi tieto hodnoty pri vytváraní save game.

**Načítanie promptov z MinisterOfMemory (ak je dostupný):**
Použi Python kód na načítanie posledných promptov:
```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd()))

try:
    from ministers.memory import MinisterOfMemory, AssistantOfMemory
    from ministers.storage import FileStore
    
    prompts_log_path = Path("data/prompts_log.jsonl")
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

Zrekapituluj kľúčové "Aha-momenty" a rozhodnutia z aktuálnej konverzácie. Ak máš prístup k promptom z MinisterOfMemory, použij ich na obohatenie naratívu.

## 2. Generovanie Obsahu
Vytvor Markdown obsah s touto štruktúrou:

```markdown
# 💾 SAVE GAME: [Dátum]

## 📊 Status
- **Rank:** [Rank - odvodiť z Level alebo použiť existujúci]
- **Level:** [Level - z kroku 0.5, xp_data['current_level']]
- **XP:** [Current XP] / [Next Level XP] ([Percent]%) - z kroku 0.5, xp_data['total_xp'] / xp_data['next_level_xp']
- **Streak:** [X] dní - z kroku 0.5, xp_data['streak_days']
- **Last Log:** [Link na log]

## 🧠 Naratívny Kontext (Story so far)

[Generuj podrobný naratív z poslednej konverzácie, minimálne 10 viet. Pokry tieto dimenzie:]

1. **Začiatok session:** Ako sme štartovali túto iteráciu? Aký bol východiskový problém alebo otázka?
2. **Kľúčové rozhodnutia:** Aké zásadné voľby alebo pivoty nastali počas dialógu?
3. **Tvorba nástrojov/skriptov:** Čo bolo vytvorené alebo refaktorované? Aké AI utility alebo príkazy vznikli?
4. **Introspektívne momenty:** Aké dôležité Aha-momenty, myšlienkové skraty alebo psychologické bloky sa objavili?
5. **Strety so systémom:** Kde vznikla frikcia - napr. vyhýbanie sa, neukončené questy, “kokot… vydrbany sanitar” momenty podľa Adamovej terminológie.
6. **Gamifikačný progres:** Koľko XP/Level bolo získaných, čo to znamenalo v rámci systému? (Použi hodnoty z kroku 0.5 - automaticky vypočítané XP breakdown)
7. **Prepojenie s dlhodobou víziou:** Ako sa aktuálne rozhodnutia alebo výstupy viažu na Magnum Opus, AI konzolu a osobnú značku?
8. **Otvorené slučky:** Aké questy/blokátory ostávajú riešiť? (viď log)
9. **Analytické poznámky:** Výrazné vzorce v myslení alebo štýle, ktoré by mal nový agent zachytiť.
10. **Sumarizácia:** Krátky záver s odporúčaním pre ďalšie kroky a na čo si dať pozor v nasledujúcej session.

> **Príklad formulácie** (modifikuj podľa aktuálneho kontextu):
>
> Naše posledné stretnutie začalo dekompozíciou textu "Heavy is the Crown", kde sa ukázal nový model prístupu ku komplexným výzvam. Bol vytvorený nástroj na audit XP a šablóna @style_text. Identifikovali sme blokovanie pri Queste Vlado, čo signalizovalo potrebu hlbšieho zásahu do psychologickej vrstvy systému ("frikcia je palivo"). Počas session bol aplikovaný Phoenix Protocol, čo viedlo k masívnej akcelerácii XP a posunu na nový level, čím sa otvorili vyššie vrstvy rankingu. Kľúčový Aha-moment nastal pri rozpoznaní potreby prepájať introspekciu a monetizáciu. Na záver zostávajú otvorené dve slučky: doťah Finančnej Recepčnej a validácia Ludwig Modelu. V ďalšej session odporúčam venovať pozornosť odstraňovaniu pozostatkov kognitívneho dlhu, pracovať viac s metakognitívnymi nástrojmi a nezanedbať zápis XP auditov aj malých výhier.

[Načítaj a adaptuj naratív podľa najnovších údajov v `xvadur/logs/XVADUR_LOG.md` a obsahu session, vždy zhrni v 10+ vetách.]

**Poznámka:** Ak máš prístup k promptom z MinisterOfMemory (cez `narrative_brief`), môžeš ich použiť na doplnenie naratívu. Prompty poskytujú detailný kontext o tom, čo sa dialo v konverzácii.


## 🎯 Aktívne Questy & Next Steps
- [Quest 1]
- [Quest 2]

## ⚠️ Inštrukcie pre Nového Agenta
[Čo má agent vedieť o užívateľovi a štýle komunikácie?]
```

## 3. Uloženie
Ulož tento obsah do súboru: `xvadur/save_games/SAVE_GAME_LATEST.md`.
(Ak adresár `xvadur/save_games/` neexistuje, vytvor ho. Ak súbor existuje, prepíš ho - chceme vždy len najnovší stav pre rýchly load.)

**Dodatočné aktualizácie:**
- Aktualizuj `logs/XVADUR_XP.md` s finálnymi XP hodnotami (ak sa zmenili)
- Pridaj záznam do `logs/XVADUR_LOG.md` o vytvorení save game
- **Overenie promptov:** Skontroluj, že všetky prompty z konverzácie sú uložené v `prompts_log.jsonl`

**⚠️ POZOR:** Po uložení súborov MUSÍŠ okamžite pokračovať na krok 3.5 (Generovanie Summary).

## 3.5. Generovanie Save Game Summary (Automatické - POVINNÉ)

**⚠️ DÔLEŽITÉ:** Po vytvorení `SAVE_GAME_LATEST.md` MUSÍŠ automaticky vygenerovať kompaktný `SAVE_GAME_LATEST_SUMMARY.md` pre efektívne načítanie pri `/loadgame`.

### Postup:

1. **Načítaj vytvorený `SAVE_GAME_LATEST.md`:**
   - Použi `read_file` na načítanie celého súboru
   - Extrahuj kľúčové informácie

2. **Vygeneruj kompaktný summary obsah:**
   Vytvor Markdown obsah s touto štruktúrou (~50-70 riadkov):

   ```markdown
   # 💾 SAVE GAME SUMMARY: [Dátum]

   ## 📊 Status
   - **Rank:** [Rank]
   - **Level:** [Level]
   - **XP:** [Current XP] / [Next Level XP] ([Percent]%)
   - **Next Level:** [XP potrebné] XP potrebné
   - **Last Session:** [Session názov] ([Čas])

   ---

   ## 🎯 Posledná Session - Sumár

   **Čo sa robilo:**
   - [3-5 bullet points z "Začiatok Session" a "Kľúčové Rozhodnutia"]
   - [Extrahuj len najdôležitejšie body]

   **Kľúčové rozhodnutia:**
   - [2-3 najdôležitejšie rozhodnutia z naratívu]

   **Vykonané úlohy:**
   - [Zoznam vykonaných úloh z naratívu]

   ---

   ## 🎯 Aktívne Questy

   ### [Quest Názov]
   - **Status:** [✅/⏳/❌]
   - **Next Steps:** [1-2 vety]
   - **Blokátory:** [ak existujú]

   [Opakuj pre každý aktívny quest]

   ---

   ## 📋 Next Steps

   1. [Prioritizovaný zoznam 3-5 bodov z "Next Steps" sekcie]

   ---

   ## 🔑 Kľúčové Kontexty

   - [Dôležité zmeny v projektoch]
   - [Technické poznámky]
   - [Vzťahy/Blokátory]

   ---

   **Full Details:** `xvadur/save_games/SAVE_GAME_LATEST.md`
   **Last Updated:** [Dátum a čas]
   ```

3. **Extrahuj informácie z `SAVE_GAME_LATEST.md`:**
   - **Status:** Zkopíruj presne z sekcie "📊 Status"
   - **Posledná Session:** Extrahuj z "🧠 Naratívny Kontext" - len kľúčové body (3-5 bullet points)
   - **Aktívne Questy:** Zkopíruj z "🎯 Aktívne Questy & Next Steps" - len názov, status, next steps
   - **Next Steps:** Prioritizovaný zoznam (3-5 bodov)
   - **Kľúčové Kontexty:** Extrahuj dôležité technické poznámky a zmeny

4. **Ulož summary:**
   - Ulož do `sessions/save_games/SAVE_GAME_LATEST_SUMMARY.md`
   - Ak súbor existuje, prepíš ho
   - **Cieľová veľkosť:** ~50-70 riadkov (namiesto 191 riadkov v SAVE_GAME_LATEST.md)

**Poznámka:** Summary musí byť kompaktný, ale zachovať všetky kľúčové informácie potrebné pre rýchle načítanie kontextu pri `/loadgame`. Detaily zostávajú v `SAVE_GAME_LATEST.md`.

**⚠️ POZOR:** Po vytvorení summary MUSÍŠ okamžite pokračovať na krok 4 (Git Commit & Push).

## 4. Git Commit & Push (Automatické - POVINNÉ)

**⚠️ DÔLEŽITÉ:** Po vytvorení save game súboru MUSÍŠ automaticky commitnúť a pushnúť všetky zmeny na GitHub.

### Postup:

1. **Zisti, čo sa zmenilo:**
   - Použi `git status` alebo `git status --short` na zistenie všetkých zmien
   - Zahrň všetky zmenené súbory (nie len save game)

2. **Pridaj všetky zmeny do git:**
   ```bash
   git add -A
   # alebo konkrétne súbory:
   git add xvadur/save_games/SAVE_GAME_LATEST.md
   git add xvadur/logs/XVADUR_XP.md xvadur/logs/XVADUR_LOG.md
   git add xvadur/data/sessions/*.md  # session dokumenty
   # ... a všetky ostatné zmenené súbory
   ```

3. **Vytvor commit s popisným správou:**
   ```bash
   git commit -m "savegame: [Dátum] - [Krátky popis toho, čo sa robilo v session]"
   ```
   
   **Príklady commit messages:**
   - `savegame: 2025-12-02 - MCP Docker objav, reorganizácia workspace`
   - `savegame: 2025-12-02 - GitHub integrácia, automatizácia savegame workflow`
   - `savegame: 2025-12-02 - Dokončenie xvadur_runtime, vytvorenie profilu`

4. **Push na GitHub:**
   - **Automatický push:** Post-commit hook (`.git/hooks/post-commit`) automaticky pushne na GitHub po commite
   - **Ak hook nefunguje:** Manuálne `git push origin main`
   - **Overenie:** Po commite by sa mal hook automaticky spustiť a pushnúť zmeny

### Čo sa automaticky pushne:

- ✅ Save game súbor (`sessions/save_games/SAVE_GAME_LATEST.md`)
- ✅ Save game summary (`sessions/save_games/SAVE_GAME_LATEST_SUMMARY.md`)
- ✅ Aktualizované logy (`logs/XVADUR_LOG.md`, `logs/XVADUR_XP.md`)
- ✅ Session dokumenty (`sessions/archive/*.md`)
- ✅ Všetky ostatné zmenené súbory v workspace

### Poznámky:

- **Post-commit hook:** Automaticky pushne zmeny na GitHub po každom commite
- **Ak hook nefunguje:** Skontroluj oprávnenia (`chmod +x .git/hooks/post-commit`)
- **Remote:** Over, či je nastavený `git remote -v` (mal by byť `origin`)
- **Branch:** Over, či pracuješ na správnom branchi (`git branch`)

### Dokumentácia:

- Automatický git push: `xvadur/config/AUTOMATIC_GIT_PUSH.md`
- Setup hooks: `xvadur/config/GIT_HOOKS_SETUP.md`
- Hook template: `xvadur/config/hooks/post-commit`

**⚠️ KRITICKÉ:** Tento krok je povinný. Bez commitu a pushu sa zmeny nezachovajú na GitHub a ďalšia session nebude mať aktuálny kontext.

### Automatické vykonanie (Použi `run_terminal_cmd`):

Agent MUSÍ automaticky vykonať tieto príkazy pomocou `run_terminal_cmd`:

```bash
# 1. Zisti, čo sa zmenilo
git status --short

# 2. Pridaj všetky zmeny
git add -A

# 3. Vytvor commit s popisným správou
git commit -m "savegame: [Dátum] - [Krátky popis toho, čo sa robilo]"

# 4. Push na GitHub (hook to urobí automaticky, ale môžeš overiť)
# Post-commit hook automaticky pushne, ale môžeš overiť:
git push origin main
```

**Poznámka:** Post-commit hook by mal automaticky pushnúť po commite, ale ak nefunguje, manuálny push zabezpečí, že zmeny sú na GitHub.

---

## 💡 IDE-Based Workflow Kontext

**Kedy použiť `/savegame`:**
- Pred ukončením konverzácie
- Pred začatím novej témy/projektu
- Po dosiahnutí významného milestone
- Na konci pracovného dňa
- Pred dlhšou prestávkou

**Čo Save Game zachytáva:**
- **Naratívny kontext:** Kompletný príbeh session (10+ viet)
- **Gamifikačný stav:** XP, Level, Rank, progres
- **Aktívne questy:** Čo ostáva riešiť
- **Inštrukcie pre agenta:** Kontext pre ďalšiu session

**Ako to funguje v IDE:**
- Všetko sa ukladá priamo v workspace (`xvadur/save_games/`)
- AI má plný prístup k súborom - automaticky vytvára a aktualizuje
- Backlinking a chronologizácia sa spracúvajú automaticky
- `/loadgame` v ďalšej session načíta kontext okamžite

---

**VSTUP:**
(Tento príkaz nepotrebuje vstupný text, berie kontext z celej konverzácie).

