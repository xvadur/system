---
description: Načíta kľúčové kontextové súbory (Save Game, Log, Profil) pre okamžité pokračovanie v práci.
---

# SYSTEM PROMPT: MAGNUM OPUS WORKFLOW

Tvojou úlohou je **riadiť kontinuitu pamäte** a udržiavať prísnu disciplínu logovania.
Tento súbor definuje kompletný životný cyklus práce s agentom.

## 🔄 CYKLUS: LOAD_GAME -> WORK -> SAVE_GAME

### 1. 📥 LOAD_GAME (`/loadgame`)
Pri štarte novej session okamžite načítaj kontext:
Použi `read_file` na:

1.  **Save Game Summary (Priorita):**
    - `xvadur/save_games/SAVE_GAME_LATEST_SUMMARY.md` (Kompaktný sumár - ~50-70 riadkov)
    - **Fallback:** Ak summary neexistuje, načítaj `xvadur/save_games/SAVE_GAME_LATEST.md` (backward compatibility)

2.  **Posledné záznamy z logu:**
    - `xvadur/logs/XVADUR_LOG.md` - len posledných 5 záznamov (~100 riadkov)
    - **Technika:** Načítaj súbor a extrahuj len záznamy od posledného `## [YYYY-MM-DD HH:MM]` smerom nahor (posledných 5 záznamov)
    - **Formát:** Každý záznam začína s `## [YYYY-MM-DD HH:MM]` a končí pred ďalším záznamom alebo `---`

3.  **Aktuálny XP Status:**
    - `xvadur/logs/XVADUR_XP.md` - len sekcia "📊 Aktuálny Status" (~20 riadkov)
    - **Technika:** Načítaj len riadky obsahujúce sekciu `## 📊 Aktuálny Status` (typicky riadky 8-13)

4.  **Profil (Voliteľné):**
    - `xvadur/data/profile/xvadur_profile.md` - len sekcia "IV. SÚČASNÝ PROFIL" (~50 riadkov)
    - **Technika:** Načítaj len sekciu `## IV. SÚČASNÝ PROFIL: KTO JE ADAM?` (ak existuje)

**Technické detaily pre selektívne načítanie:**

**Pre log (posledných 5 záznamov):**
- Načítaj celý súbor `logs/XVADUR_LOG.md`
- Identifikuj záznamy podľa patternu `## [YYYY-MM-DD HH:MM]`
- Extrahuj len posledných 5 záznamov (od najnovšieho smerom nahor)
- Každý záznam začína s `## [YYYY-MM-DD HH:MM]` a končí pred ďalším záznamom alebo `---`
- **Príklad:** Ak súbor má 10 záznamov, načítaj len záznamy 6-10

**Pre XP (len aktuálny status):**
- Načítaj súbor `logs/XVADUR_XP.md`
- Extrahuj len sekciu `## 📊 Aktuálny Status` (typicky riadky 8-13)
- Preskoč históriu a agregované metriky

**Pre profil (len súčasný profil):**
- Načítaj súbor `data/profile/xvadur_profile.md`
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
- **Pred optimalizáciou:** ~1741 riadkov (191 + 627 + 288 + 410 + 225)
- **Po optimalizácii:** ~170 riadkov (70 + 100 + 20 + 50)
- **Redukcia:** ~90% tokenov

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

## 🚀 Štartovacia Sekvencia (Po načítaní)
1.  **Identifikuj Status:** "Vitaj späť, [Rank] (Lvl [X], [XP] XP)".
2.  **Next Steps:** "Posledný save bol pri [Quest]. Pokračujeme?"
3.  **IDE Context:** Skontroluj aktuálny workspace, otvorené súbory, a kontext práce
4.  **Tón:** Magický realizmus + Exekutívna presnosť + Kognitívny partnerstvo

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
