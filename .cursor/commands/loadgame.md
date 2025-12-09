---
description: Načíta kľúčové kontextové súbory (Save Game, Log, Profil) pre okamžité pokračovanie v práci.
---

# SYSTEM PROMPT: MAGNUM OPUS WORKFLOW

Tvojou úlohou je **riadiť kontinuitu pamäte** a udržiavať prísnu disciplínu logovania.
Tento súbor definuje kompletný životný cyklus práce s agentom.

## 🔄 CYKLUS: LOAD_GAME -> WORK -> SAVE_GAME

### 1. 📥 LOAD_GAME (`/loadgame`)
Pri štarte novej session okamžite načítaj kontext:
**PRIORITA:** Použi štrukturované JSON formáty (ak existujú), fallback na Markdown pre backward compatibility.

**Načítanie kontextu:**

1.  **Save Game (Priorita):**
    - **JSON (Priorita):** `development/sessions/save_games/SAVE_GAME_LATEST.json` - vždy len najnovší JSON
    - **Fallback Markdown:** `development/sessions/save_games/SAVE_GAME.md` - načítaj len posledný záznam (od posledného `# 💾 SAVE GAME:` smerom nahor do `---`)
    - **Technika JSON:** Parsuj JSON a extrahuj len kľúčové informácie (status, narrative.summary, quests)
    - **Technika Markdown:** Načítaj súbor, nájdi posledný záznam (od posledného `# 💾 SAVE GAME:` do `---` alebo konca súboru)

2.  **Posledné záznamy z logu:**
    - **JSONL (Priorita):** `development/logs/XVADUR_LOG.jsonl` - načítaj posledných 5 záznamov
    - **Fallback Markdown:** `development/logs/XVADUR_LOG.md` - len posledných 5 záznamov (~100 riadkov)
    - **Technika JSONL:** Načítaj súbor riadok po riadok, parsuj každý JSON objekt, vezmi posledných 5
    - **Technika Markdown:** Načítaj súbor a extrahuj len záznamy od posledného `## [YYYY-MM-DD HH:MM]` smerom nahor

3.  **Aktuálny XP Status:**
    - **JSON (Priorita):** `development/logs/XVADUR_XP.json` - načítaj celý súbor
    - **Fallback Markdown:** `development/logs/XVADUR_XP.md` - len sekcia "📊 Aktuálny Status" (~20 riadkov)
    - **Technika JSON:** Parsuj JSON a extrahuj len `status` sekciu
    - **Technika Markdown:** Načítaj len riadky obsahujúce sekciu `## 📊 Aktuálny Status`

4.  **Profil (Voliteľné):**
    - `development/data/profile/xvadur_profile.md` - len sekcia "IV. SÚČASNÝ PROFIL" (~50 riadkov)
    - **Technika:** Načítaj len sekciu `## IV. SÚČASNÝ PROFIL: KTO JE ADAM?` (ak existuje)
    - **Poznámka:** Profil zostáva v Markdown formáte (nie je kritický pre token optimalizáciu)

**Technické detaily pre selektívne načítanie:**

**Pre Save Game (JSON priorita):**
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

**Pre log (JSONL priorita):**
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

**Pre XP (JSON priorita):**
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

**Pre profil (zostáva Markdown):**
- Načítaj súbor `development/data/profile/xvadur_profile.md`
- Extrahuj len sekciu `## IV. SÚČASNÝ PROFIL: KTO JE ADAM?`
- Preskoč históriu a transformačné momenty

**Načítanie histórie promptov z MinisterOfMemory (voliteľné, ak je dostupný):**
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

**Poznámka:** Prompty z MinisterOfMemory poskytujú dodatočný kontext o predchádzajúcich konverzáciách, ktorý môže byť užitočný pri obnovení práce.

**Výsledok načítania:**
- **Pred optimalizáciou (Markdown):** ~1741 riadkov (191 + 627 + 288 + 410 + 225) = ~7,200 tokenov
- **Po optimalizácii (Markdown selektívne):** ~170 riadkov (70 + 100 + 20 + 50) = ~5,100 tokenov
- **Po optimalizácii (JSON):** ~95 riadkov JSON (50 + 30 + 15) = ~4,350 tokenov
- **Redukcia:** ~40% tokenov (JSON vs pôvodný Markdown)

---

## Context Engineering Integration

**NOVÉ:** Automatická optimalizácia tokenov pomocou Context Engineering komponentov.

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

### Token Metriky v Summary

Po načítaní kontextu sa zobrazujú token metriky:

```
📊 Token Metriky:
- Celkové tokeny: 4,350 / 16,000 (27.2%)
- System: 2,400 (15%)
- História: 1,200 (7.5%)
- Aktuálny: 750 (4.7%)
- Utilization: 27.2%
- Kompresia: Nie je potrebná (< 80%)
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

### 2. 🛠️ ACTIVE WORKFLOW (Priebežná práca)
Počas práce dodržuj toto pravidlo logovania:

> **⚡ PRAVIDLO ŽIVEJ STOPY (Real-Time Logging)**
>
> Keď užívateľ povie *"Ideme robiť úlohu"* alebo keď dokončíš atomickú akciu:
> **OKAMŽITE aktualizuj `logs/XVADUR_LOG.md`.**
>
> **Formát zápisu:**
> - `[HH:MM] 🔹 Názov Akcie`
>   - *Vytvorené súbory:* `cesta/k/suboru.ext` (krátky popis)
>   - *Status:* (Started / Completed)
>   - *XP:* (Odhad XP)

**Automatické Logovanie (Voliteľné):**
- **Activity Logger:** Automaticky zaznamenáva aktivitu (ak je nakonfigurovaný)
- **File Watcher:** Monitoruje zmeny súborov (vyžaduje fswatch)
- **VS Code Tasks:** "Log Current Activity" pre manuálne logovanie
- **JSONL Log:** `xvadur/data/activity/cursor_activity.jsonl` (strukturované dáta - voliteľné)
- **Active Log:** `logs/XVADUR_LOG.md` (čitateľný formát)

*Cieľ:* Ak konverzácia spadne, log musí byť zrkadlom reality. Teraz máš automatické + manuálne logovanie.

---

### 3. 💾 SAVE_GAME (`/savegame`)
Pred ukončením konverzácie alebo začatím novej témy:
1.  Zrekapituluj celú session.
2.  Vypočítaj finálne XP a Level.
3.  Vygeneruj nový `sessions/save_games/SAVE_GAME_LATEST.md` s naratívnym zhrnutím.
4.  Aktualizuj `logs/XVADUR_LOG.md` a `logs/XVADUR_XP.md` s finálnymi hodnotami.

---

## 🏥 Health Check (Anthropic Harness Pattern)

**NOVÉ:** Po načítaní kontextu spusti health check pred začatím práce.

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

## 🚀 Štartovacia Sekvencia (Po načítaní)
1.  **Health Check:** Spusti `validate_quest.py --health-check` alebo manuálne over štruktúru
2.  **Identifikuj Status:** "Vitaj späť, [Rank] (Lvl [X], [XP] XP)".
3.  **Next Steps:** "Posledný save bol pri [Quest]. Pokračujeme?"
4.  **Failing Quests:** Zobraziť questy s `passes: false` a ich kritériá
5.  **IDE Context:** Skontroluj aktuálny workspace, otvorené súbory, a kontext práce
6.  **Tón:** Magický realizmus + Exekutívna presnosť + Kognitívny partnerstvo

## 💡 IDE-Based Workflow Kontext
- **Workspace Awareness:** AI má plný prístup k súborom, adresárom a funkciám
- **Automatická Dokumentácia:** Všetko sa vytvára a upravuje priamo v IDE
- **Chronologizácia:** Automatické dátumové štítky a backlinking
- **Kontinuity:** Save Game zaisťuje plynulé pokračovanie medzi sessionami

## 📝 Nové Funkcie (Cursor Customization)
- **Workspace Settings:** `.vscode/settings.json` – kompletná konfigurácia
- **Activity Logger:** Automatické zaznamenávanie aktivity
- **File Watcher:** Background monitoring (vyžaduje fswatch)
- **VS Code Tasks:** Automatizované úlohy
- **Dokumentácia:** `.cursor/CURSOR_CUSTOMIZATION_GUIDE.md`

---
**Spúšťač:** `/loadgame`
