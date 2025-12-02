# 📁 XVADUR Konfigurácia

**Adresár:** `xvadur/config/`  
**Účel:** Konfiguračné súbory a dokumentácia pre XVADUR systém

---

## 📋 Obsah Adresára

### Dokumentácia

1. **`AUTOMATIC_GIT_PUSH.md`** - Kompletná dokumentácia automatického git push na GitHub
   - Ako funguje automatizácia
   - Konfigurácia a nastavenie
   - Riešenie problémov
   - Best practices

2. **`GIT_HOOKS_SETUP.md`** - Inštrukcie pre nastavenie git hooks
   - Ako nastaviť hooks na novom počítači
   - Riešenie problémov s hooks
   - Poznámky o git hooks

3. **`xvadur_command.md`** - Dokumentácia pre `/xvadur` príkaz
   - Konverzačná vrstva pre filozofické a reflexívne rozhovory
   - XP tracking, backlinking, visualizácie

### Hook Templates

- **`hooks/post-commit`** - Git post-commit hook template
  - Automatický push na GitHub po každom commite
  - Nastavenie: `cp xvadur/config/hooks/post-commit .git/hooks/post-commit && chmod +x .git/hooks/post-commit`

---

## 🚀 Rýchly Start

### Nastavenie Automatického Git Push

1. **Inštalácia hooku:**
   ```bash
   cp xvadur/config/hooks/post-commit .git/hooks/post-commit
   chmod +x .git/hooks/post-commit
   ```

2. **Testovanie:**
   ```bash
   echo "test" > test.txt
   git add test.txt
   git commit -m "test: Testing automatic push"
   # Hook by sa mal automaticky spustiť
   ```

3. **Dokumentácia:**
   - Detailný návod: `xvadur/config/AUTOMATIC_GIT_PUSH.md`
   - Setup guide: `xvadur/config/GIT_HOOKS_SETUP.md`

---

## 📚 Dokumentácia

### Automatický Git Push

**Súbor:** `AUTOMATIC_GIT_PUSH.md`

Popisuje automatizáciu pushu na GitHub:
- ✅ Post-commit hook pre automatický push
- ✅ Integrácia do `/savegame` príkazu
- ✅ Konfigurácia a troubleshooting
- ✅ Best practices

### Git Hooks Setup

**Súbor:** `GIT_HOOKS_SETUP.md`

Inštrukcie pre nastavenie hooks:
- ⚠️ Prečo hooks sa necommitnú
- 🔧 Ako nastaviť hooks na novom počítači
- 📝 Poznámky a odporúčania

### XVADUR Command

**Súbor:** `xvadur_command.md`

Dokumentácia konverzačnej vrstvy:
- 🧠 Filozofické a reflexívne rozhovory
- 📊 XP tracking a gamifikácia
- 🔗 Backlinking a knowledge graph
- 📈 Visualizácie metrík

---

## 🔗 Súvisiace Súbory

- **Cursor Commands:** `.cursor/commands/`
  - `savegame.md` - ukladanie session stavu
  - `loadgame.md` - načítanie session stavu
  - `xvadur.md` - konverzačná vrstva

- **Git Hook:** `.git/hooks/post-commit` (lokálny)
- **Hook Template:** `xvadur/config/hooks/post-commit` (v repozitári)

---

## 💡 Poznámky

- **Git Hooks:** Hooks sa necommitnú do repozitára (štandardné správanie)
- **Hook Template:** Template je v repozitári pre ľahké nastavenie na novom počítači
- **Dokumentácia:** Všetka dokumentácia je v tomto adresári pre lepšiu organizáciu

---

**Vytvorené:** 2025-12-02  
**Status:** ✅ Aktívne

