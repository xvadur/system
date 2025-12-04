# 📁 XVADUR Konfigurácia

**Adresár:** `xvadur/config/`  
**Účel:** Konfiguračné súbory a dokumentácia pre XVADUR systém

---

## 📋 Obsah Adresára

### Dokumentácia

1. **`GIT_SETUP.md`** - Kompletná dokumentácia git setupu
   - Automatický git push na GitHub
   - Nastavenie post-commit hooku
   - Konfigurácia a troubleshooting
   - Best practices

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
   - Kompletný návod: `xvadur/config/GIT_SETUP.md`

---

## 📚 Dokumentácia

### Git Setup

**Súbor:** `GIT_SETUP.md`

Kompletná dokumentácia git setupu:
- ✅ Post-commit hook pre automatický push
- ✅ Integrácia do `/savegame` príkazu
- ✅ Konfigurácia a troubleshooting
- ✅ Best practices
- ⚠️ Prečo hooks sa necommitnú
- 🔧 Ako nastaviť hooks na novom počítači

**Poznámka:** Dokumentácia pre `/xvadur` príkaz je v `.cursor/commands/xvadur.md`

---

## 🔗 Súvisiace Súbory

- **Cursor Commands:** `.cursor/commands/`
  - `savegame.md` - ukladanie session stavu (automatický git push)
  - `loadgame.md` - načítanie session stavu
  - `xvadur.md` - konverzačná vrstva (filozofické rozhovory)

- **Git Hook:** `.git/hooks/post-commit` (lokálny)
- **Hook Template:** `xvadur/config/hooks/post-commit` (v repozitári)

---

## 💡 Poznámky

- **Git Hooks:** Hooks sa necommitnú do repozitára (štandardné správanie)
- **Hook Template:** Template je v repozitári (`hooks/post-commit`) pre ľahké nastavenie na novom počítači
- **Dokumentácia:** Git dokumentácia je konsolidovaná do jedného súboru (`GIT_SETUP.md`)

---

**Vytvorené:** 2025-12-02  
**Status:** ✅ Aktívne

