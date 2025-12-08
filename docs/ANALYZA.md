# 🛰️ AetheroOS Repozitár — Architektonická Analýza

<!-- AETH: Premier-level audit of logging, state, context, and commands. -->

## SECTION 1 — Repository Map
- `README.md`: Rýchly prehľad štruktúry, commandov a statusu.
- `.cursor/commands/`: Cursor orchestrace (`/loadgame`, `/savegame`, `/quest`, `/xvadur`).
- `core/`: Jadro (ministerstvá, RAG, XP); obsahuje základné `MinisterOfMemory` a úložiská.
- `ministers/`: Premier-facing fasády (napr. `MinisterOfMemory` wrapper) pre AetheroOS hierarchiu.
- `development/`: Aktívne dáta — `logs/` (activity & XP), `sessions/` (current, archive, save_games), `data/` (profil).
- `docs/`: Architektonické materiály (napr. `ARCHITECTURE.md`) a táto analýza.
- `data/`: RAG indexy a globálne dátové zdroje (napr. `prompts_log.jsonl`).
- `scripts/`: Utility pre prompty, XP, RAG a syntézu.
- `staging/`, `production/`, `archive/`: Layered prostredia na review/automatizáciu.

## SECTION 2 — Logging Architecture
- Primárne logy: `development/logs/XVADUR_LOG.jsonl` (structured JSONL) s fallbackom `development/logs/XVADUR_LOG.md`.
- XP logy: `development/logs/XVADUR_XP.json` (stav) + fallback `development/logs/XVADUR_XP.md`.
- Append model: prírastkové riadky (JSONL) alebo markdown sekcie; `/loadgame` číta iba posledné záznamy (5 položiek), aby obmedzil tokeny.
- Logy sú používané pri `/loadgame` pre rýchle obnovenie posledných udalostí a XP statusu (priorita JSON → Markdown). 

## SECTION 3 — State & Context Architecture
- Savegame: `development/sessions/save_games/SAVE_GAME_LATEST.json` (priority) a `SAVE_GAME.md` (fallback); obsahuje status, narrative summary a quests.
- Aktívna session: `development/sessions/current/` (pracovný kontext); archív v `development/sessions/archive/`.
- Profil: `development/data/profile/xvadur_profile.md` (sekcia IV ako voliteľný kontext pri loadgame).
- Prompt história: `data/prompts_log.jsonl` (auto-save hook) využiteľná cez `MinisterOfMemory`.
- Rekonštrukcia kontextu: `/loadgame` načíta savegame (JSON preferované), posledné logy a XP; profil iba selektívne. JSON-first stratégia minimalizuje parsing a token náklady.

## SECTION 4 — Command Architecture
- `/loadgame` (`.cursor/commands/loadgame.md`): hierarchické načítanie kontextu (savegame → log → XP → profil). Implementuje selektívne čítanie, limity (5 záznamov) a fallbacky.
- `/savegame` (`.cursor/commands/savegame.md`): batch ukladanie promptov, XP prepočet a generovanie savegame; požaduje git commit/push po uložení.
- `/quest`, `/xvadur`: režijné príkazy pre questovanie a dialóg.
- Logika explicitná v markdown príručkách; operácie sú kódovo riadené (FileStore, MinisterOfMemory) skôr než implicitné LLM správanie.

## SECTION 5 — Token Cost Analysis
- Potenciálne nafukovanie: veľké `.cursorrules` + viacnásobné Markdown fallbacky (savegame/log/XP) zdvojujú obsah.
- `/loadgame` zmierňuje riziko limitmi na počet záznamov a preferenciou JSON; profil sekcie sú optional.
- Ukladanie dlhých narratív v savegame Markdown môže zvyšovať tokeny pri fallback čítaní.

## SECTION 6 — Architectural Diagnosis
- **Silné stránky:** Layered prostredia; JSON-first načítanie; jasné príkazové workflow; modulárne core balíky (memory/RAG/XP).
- **Slabiny:** Dvojité formáty (JSON + Markdown) vytvárajú redundantný stav; manuálne markdown parsing je krehké; povinný git push pri `/savegame` zvyšuje prevádzkovú záťaž.
- **Kontradikcie:** Snaha šetriť tokeny vs. dlhé savegame narácie; simultánne logovanie do viacerých formátov.
- **Chýbajúce abstrakcie:** Jednotný log writer/reader; ľahký stavový manifest; ochrana token budgetu pri generovaní narratív.

## SECTION 7 — Recommendations
- Zaviesť ľahký JSON manifest (posledný save/log/XP pointer) ako jediný vstup pre `/loadgame`, s Markdown len na archiváciu.
- Zjednotiť logovanie cez jednu utilitu, ktorá zapisuje JSONL a len krátke Markdown headliny, nie úplné duplikáty.
- Obmedziť savegame Markdown na stručné sumáre; detailné narácie archivovať inde.
- Voliteľne oddeliť git push od `/savegame` (batch pipeline) pre nižšiu prevádzkovú záťaž.
- Využiť `MinisterOfMemory` priamo pre načítanie posledných promptov namiesto manuálneho parsovania Markdown.
