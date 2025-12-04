# 🚀 Git Setup - Automatický Push a Hooks

**Status:** ✅ Aktívne  
**Dátum vytvorenia:** 2025-12-02

---

## 📋 Prehľad

Tento dokument popisuje automatizáciu pushu na GitHub v rámci XVADUR workspace. Všetky zmeny sa automaticky synchronizujú na GitHub po každom git commite pomocou post-commit hooku.

---

## 🔧 Ako to Funguje

### Git Post-Commit Hook

**Súbor:** `.git/hooks/post-commit`  
**Template:** `xvadur/config/hooks/post-commit`

Tento hook sa automaticky spustí po každom `git commit` a:
- ✅ Automaticky pushne zmeny na GitHub
- ✅ Zobrazí informácie o pushi (remote, branch)
- ✅ Zobrazí posledný commit
- ✅ Handluje chyby (ak push zlyhá, zobrazí chybovú správu)

**Výhody:**
- **Automatizácia:** Žiadne manuálne pushy
- **Zálohovanie:** Všetky zmeny sú okamžite na GitHub
- **Synchronizácia:** Workspace je vždy v súlade s GitHub

### Integrácia do `/savegame` Príkazu

**Súbor:** `.cursor/commands/savegame.md`

Príkaz `/savegame` teraz automaticky:
1. Vytvorí save game súbor
2. Pridá súbory do git
3. Vytvorí commit
4. Post-commit hook automaticky pushne na GitHub

---

## ⚙️ Konfigurácia

### Nastavenie Remote (Ak ešte nie je nastavený)

```bash
cd /Users/_xvadur/Desktop/xvadur-workspace
git remote add origin https://github.com/xvadur/system.git
git push -u origin main
```

### Inštalácia Hooku (Po Klonovaní Repozitára)

**⚠️ Dôležité:** Git hooks sa necommitnú do repozitára (štandardné správanie). Preto treba hook nastaviť manuálne na každom počítači.

```bash
# Skopírovať hook template do .git/hooks/
cp xvadur/config/hooks/post-commit .git/hooks/post-commit

# Nastaviť oprávnenia na spustenie
chmod +x .git/hooks/post-commit
```

**Poznámka:** Hook template je v repozitári (`xvadur/config/hooks/post-commit`), stačí ho skopírovať na správne miesto.

### Kontrola Hooku

```bash
# Skontrolovať, či hook existuje
ls -la .git/hooks/post-commit

# Skontrolovať oprávnenia (mal by byť executable)
chmod +x .git/hooks/post-commit
```

### Testovanie Hooku

```bash
# Vytvoriť test commit
echo "test" > test.txt
git add test.txt
git commit -m "test: Testing post-commit hook"
# Hook by sa mal automaticky spustiť a pushnúť na GitHub
```

---

## 📊 Čo sa Pushuje

### Automaticky po Commit:
- ✅ Všetky zmenené súbory
- ✅ Nové súbory
- ✅ Aktualizované dokumenty
- ✅ Log súbory (`xvadur/logs/`)
- ✅ Save games (`xvadur/save_games/`)
- ✅ Session dokumenty (`xvadur/data/sessions/`)

### Čo sa NEPushuje (podľa `.gitignore`):
- ❌ `.env` súbory (API keys)
- ❌ `node_modules/`
- ❌ Python cache (`__pycache__/`)
- ❌ IDE nastavenia (`.vscode/`, `.idea/`)
- ❌ Log súbory (`.log`, `.jsonl`)

---

## 🔍 Riešenie Problémov

### Hook sa Nespúšťa

**Príčina:** Hook nemá oprávnenia na spustenie

**Riešenie:**
```bash
chmod +x .git/hooks/post-commit
```

### Push Zlyhá

**Príčiny:**
- Žiadne pripojenie na internet
- Neplatné GitHub credentials
- Konflikty v repozitári

**Riešenie:**
```bash
# Skontrolovať pripojenie
git remote -v

# Manuálny push
git push origin main

# Skontrolovať git config
git config --list | grep user
```

### Hook Pushuje Nevhodné Súbory

**Príčina:** `.gitignore` nie je správne nastavený

**Riešenie:**
1. Skontrolovať `.gitignore` súbor
2. Pridať nechcené súbory/adresáre
3. Odstrániť už commitnuté súbory:
   ```bash
   git rm --cached <súbor>
   git commit -m "chore: Remove unwanted files"
   ```

---

## 💡 Best Practices

### 1. Commit Messages

Používaj popisné commit messages:
```bash
git commit -m "feat: Add new feature"
git commit -m "fix: Fix bug in script"
git commit -m "docs: Update documentation"
git commit -m "savegame: 2025-12-02 - Workspace setup"
```

### 2. Časté Commity

Commituj často a v menších krokoch:
- ✅ Po každej dokončenej úlohe
- ✅ Po vytvorení `/savegame`
- ✅ Po významných zmenách

### 3. Pred Pushom

Skontroluj zmeny pred commitom:
```bash
git status          # Čo sa zmenilo
git diff            # Detail zmien
git log --oneline   # Históriu commitov
```

---

## 📝 Príklady Použitia

### Automatický Push po `/savegame`

1. Použi príkaz `/savegame`
2. Agent vytvorí save game súbor
3. Agent pridá súbory do git a commitne
4. Hook automaticky pushne na GitHub

### Automatický Push po Manuálnom Commite

```bash
# Vytvor zmeny
echo "update" >> README.md

# Commit
git add README.md
git commit -m "docs: Update README"
# Hook automaticky pushne na GitHub
```

---

## 🔐 Bezpečnosť

### Ochrana Citlivých Dát

- ✅ `.env` súbory sú v `.gitignore`
- ✅ API keys sa nikdy necommitnú
- ✅ Citlivé dáta zostávajú lokálne

### Overenie Pred Pushom

Hook skontroluje:
- ✅ Existuje remote origin
- ✅ Branch má tracking nastavený
- ✅ Push je úspešný (ak nie, zobrazí chybu)

---

## 🎯 Výhody Automatizácie

1. **Zálohovanie:** Všetky zmeny sú okamžite zálohované
2. **Synchronizácia:** Workspace je vždy v súlade s GitHub
3. **Pohodlie:** Žiadne manuálne pushy
4. **Bezpečnosť:** History je zachovaná
5. **Kolaborácia:** Ľahké zdieľanie práce

---

## 📚 Referencie

- **Git Hooks Dokumentácia:** [Git Hooks](https://git-scm.com/book/en/v2/Customizing-Git-Git-Hooks)
- **Post-Commit Hook:** `.git/hooks/post-commit` (lokálny)
- **Hook Template:** `xvadur/config/hooks/post-commit` (v repozitári)
- **Save Game Command:** `.cursor/commands/savegame.md`
- **Git Ignore:** `.gitignore`

---

**Vytvorené:** 2025-12-02  
**Status:** ✅ Aktívne a funkčné

