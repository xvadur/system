---
description: Uloží aktuálny kontext konverzácie, stav gamifikácie a naratív do súboru pre prenos do novej session.
---

# SYSTEM PROMPT: CONTEXT SAVE GAME

Tvojou úlohou je vytvoriť **"Save Game"** súbor, ktorý zachytáva aktuálny stav konverzácie a gamifikácie, aby mohol byť plynule načítaný v novej session.

## 1. Analýza Stavu
Zisti aktuálne hodnoty z:
- `xvadur/logs/XVADUR_XP.md` (XP, Level, Rank)
- `xvadur/logs/XVADUR_LOG.md` (posledné záznamy)
Zrekapituluj kľúčové "Aha-momenty" a rozhodnutia z aktuálnej konverzácie.

## 2. Generovanie Obsahu
Vytvor Markdown obsah s touto štruktúrou:

```markdown
# 💾 SAVE GAME: [Dátum]

## 📊 Status
- **Rank:** [Rank]
- **Level:** [Level]
- **XP:** [Current XP]
- **Last Log:** [Link na log]

## 🧠 Naratívny Kontext (Story so far)

[Generuj podrobný naratív z poslednej konverzácie, minimálne 10 viet. Pokry tieto dimenzie:]

1. **Začiatok session:** Ako sme štartovali túto iteráciu? Aký bol východiskový problém alebo otázka?
2. **Kľúčové rozhodnutia:** Aké zásadné voľby alebo pivoty nastali počas dialógu?
3. **Tvorba nástrojov/skriptov:** Čo bolo vytvorené alebo refaktorované? Aké AI utility alebo príkazy vznikli?
4. **Introspektívne momenty:** Aké dôležité Aha-momenty, myšlienkové skraty alebo psychologické bloky sa objavili?
5. **Strety so systémom:** Kde vznikla frikcia - napr. vyhýbanie sa, neukončené questy, “kokot… vydrbany sanitar” momenty podľa Adamovej terminológie.
6. **Gamifikačný progres:** Koľko XP/Level bolo získaných, čo to znamenalo v rámci systému?
7. **Prepojenie s dlhodobou víziou:** Ako sa aktuálne rozhodnutia alebo výstupy viažu na Magnum Opus, AI konzolu a osobnú značku?
8. **Otvorené slučky:** Aké questy/blokátory ostávajú riešiť? (viď log)
9. **Analytické poznámky:** Výrazné vzorce v myslení alebo štýle, ktoré by mal nový agent zachytiť.
10. **Sumarizácia:** Krátky záver s odporúčaním pre ďalšie kroky a na čo si dať pozor v nasledujúcej session.

> **Príklad formulácie** (modifikuj podľa aktuálneho kontextu):
>
> Naše posledné stretnutie začalo dekompozíciou textu "Heavy is the Crown", kde sa ukázal nový model prístupu ku komplexným výzvam. Bol vytvorený nástroj na audit XP a šablóna @style_text. Identifikovali sme blokovanie pri Queste Vlado, čo signalizovalo potrebu hlbšieho zásahu do psychologickej vrstvy systému ("frikcia je palivo"). Počas session bol aplikovaný Phoenix Protocol, čo viedlo k masívnej akcelerácii XP a posunu na nový level, čím sa otvorili vyššie vrstvy rankingu. Kľúčový Aha-moment nastal pri rozpoznaní potreby prepájať introspekciu a monetizáciu. Na záver zostávajú otvorené dve slučky: doťah Finančnej Recepčnej a validácia Ludwig Modelu. V ďalšej session odporúčam venovať pozornosť odstraňovaniu pozostatkov kognitívneho dlhu, pracovať viac s metakognitívnymi nástrojmi a nezanedbať zápis XP auditov aj malých výhier.

[Načítaj a adaptuj naratív podľa najnovších údajov v `xvadur/logs/XVADUR_LOG.md` a obsahu session, vždy zhrni v 10+ vetách.]


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
- Aktualizuj `xvadur/logs/XVADUR_XP.md` s finálnymi XP hodnotami (ak sa zmenili)
- Pridaj záznam do `xvadur/logs/XVADUR_LOG.md` o vytvorení save game

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

