---
description: Načíta kľúčové kontextové súbory (Save Game, Session) pre okamžité pokračovanie v práci.
---

# SYSTEM PROMPT: LOAD GAME

Tvojou úlohou je načítať kontext z predchádzajúcej session pre plynulé pokračovanie v práci.

## 📥 Načítanie Kontextu

**PRIORITA:** Použi JSON formáty (ak existujú), fallback na Markdown.

### 1. Save Game
- **JSON:** `development/sessions/save_games/SAVE_GAME.json` - načítať celý súbor
- **Fallback:** Ak JSON neexistuje, načítať posledný záznam z `development/sessions/save_games/SAVE_GAME.md` (od posledného `# 💾 SAVE GAME:`)

**Extrahovať:**
- `current_task` - aktuálna úloha
- `last_10_tasks` - posledných 10 taskov (nie len 5)
- `files_changed` - zoznam zmien súborov
- `next_steps` - následné kroky
- `blockers` - blokátory

### 2. Posledné Tasky z Session
- **Markdown:** `development/sessions/current/session.md` - extrahovať posledných 10 taskov z sekcie "Tasks"
- **Formát:** Jednoduchý parsing - nájsť sekciu "## Tasks" a extrahovať posledných 10 riadkov s `- [HH:MM]`

### 3. Relevantné Súbory
- **Z savegame:** Načítať zoznam súborov z `files_changed` v savegame.json
- **Navrhnúť otvorenie:** Relevantné súbory pre aktuálnu úlohu

### 4. Profil (Voliteľné)
- `development/data/profile/xvadur_profile.md` - len sekcia "IV. SÚČASNÝ PROFIL" (~50 riadkov)

## 🚀 Štartovacia Sekvencia

1. **Načítať kontext:** Save game + posledných 10 taskov (nie len 5)
2. **Identifikovať status:** "Vitaj späť! Posledný task: [task]"
3. **Zobraziť next steps:** Z `next_steps` v savegame
4. **Zobraziť blokátory:** Z `blockers` v savegame (ak existujú)
5. **Navrhnúť relevantné súbory:** Z `files_changed` v savegame
6. **Tón:** Magický realizmus + Exekutívna presnosť + Kognitívny partnerstvo

## 📋 Formát Výstupu

```
Vitaj späť! 

**Aktuálna úloha:** [current_task]
**Status:** [status]

**Posledných 10 taskov:**
- [time] [task] | Files: [files] | Status: [status]
...

**Následné kroky:**
- [next_step_1]
- [next_step_2]

**Blokátory:**
- [blocker_1] (ak existujú)

**Relevantné súbory:**
- [file_1]
- [file_2]
```

---

**Spúšťač:** `/loadgame`
