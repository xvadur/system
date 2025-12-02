# 📝 Git Hooks Setup - Poznámka

## ⚠️ Dôležité: Git Hooks sa Necommitnú

Git hooks (napr. `.git/hooks/post-commit`) **sa necommitnú** do repozitára. Toto je správne správanie, pretože:

1. **Lokálna konfigurácia:** Hooks sú lokálne pre každého vývojára
2. **Bezpečnosť:** Každý môže mať vlastné hooks
3. **Flexibilita:** Rôzne prostredia môžu mať rôzne nastavenia

---

## 🔧 Ako Nastaviť Hooks na Iných Počítačoch

Ak pracuješ na inom počítači alebo klonuješ repozitár:

### 1. Skopíruj Hook Manuálne

```bash
# Z aktuálneho workspace
cp .git/hooks/post-commit /cesta/k/novemu/workspace/.git/hooks/post-commit
chmod +x /cesta/k/novemu/workspace/.git/hooks/post-commit
```

### 2. Použi Hook Template z Repozitára

Hook template je v `xvadur/config/hooks/post-commit`:

```bash
# Po klonovaní repozitára
cp xvadur/config/hooks/post-commit .git/hooks/post-commit
chmod +x .git/hooks/post-commit
```

**Poznámka:** Hook template je už v repozitári, stačí ho skopírovať na správne miesto.

### 3. Alebo Použi Git Hooks Dir (Git 2.9+)

Nastaviť globálny hooks adresár:
```bash
git config --global core.hooksPath ~/.git-hooks
```

A skopírovať hooks tam.

---

## ✅ Riešenie Pre Tento Projekt

**Súčasný stav:**
- ✅ Hook je aktívny na aktuálnom počítači
- ✅ Automaticky pushuje po každom commite
- ⚠️ Pri klonovaní na nový počítač treba hook nastaviť manuálne

**Odporúčanie:**
- Hook je jednoduchý a dá sa rýchlo nastaviť
- Dokumentácia je v `xvadur/config/AUTOMATIC_GIT_PUSH.md`
- Hook template je v `xvadur/config/hooks/post-commit`

---

**Poznámka:** Toto je štandardné správanie git hooks. Nie je to problém, len to vyžaduje jednorazové nastavenie na novom počítači.

