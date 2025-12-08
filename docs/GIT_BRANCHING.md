# 🔀 Git Branching Strategy

**Verzia:** 1.0.0  
**Posledná aktualizácia:** 2025-12-08

---

## 📋 Prehľad

Tento dokument definuje branching stratégiu pre XVADUR systém. Cieľom je udržiavať čistý a prehľadný git workflow.

---

## 🌳 Branch Typy

### 1. **`main`** - Production Branch
- **Účel:** Hlavná vetva s produkčným kódom
- **Pravidlá:** 
  - Vždy stabilný a funkčný kód
  - Merge len cez Pull Request
  - Automatické testy musia prejsť
- **Protection:** ✅ Protected branch

### 2. **`feature/*`** - Feature Development
- **Formát:** `feature/quest-15-domain-memory` alebo `feature/youtube-processing`
- **Účel:** Vývoj nových funkcií
- **Životný cyklus:**
  - Vytvorenie z `main`
  - Vývoj funkcie
  - Merge do `main` cez PR
  - Automatické vymazanie po merge

### 3. **`quest/*`** - Quest/Issue Development
- **Formát:** `quest/18-git-branching` alebo `quest/15-domain-memory`
- **Účel:** Riešenie konkrétnych questov/issues
- **Životný cyklus:**
  - Vytvorenie z `main` pri otvorení questu
  - Vývoj riešenia
  - Merge do `main` cez PR
  - Automatické vymazanie po merge

### 4. **`fix/*`** - Bug Fixes
- **Formát:** `fix/memory-bug` alebo `fix/rag-index-error`
- **Účel:** Opravy chýb
- **Životný cyklus:**
  - Vytvorenie z `main`
  - Oprava bugu
  - Merge do `main` cez PR
  - Automatické vymazanie po merge

### 5. **`refactor/*`** - Code Refactoring
- **Formát:** `refactor/memory-system` alebo `refactor/rag-index`
- **Účel:** Refaktorovanie existujúceho kódu
- **Životný cyklus:**
  - Vytvorenie z `main`
  - Refaktorovanie
  - Merge do `main` cez PR
  - Automatické vymazanie po merge

### 6. **`docs/*`** - Documentation
- **Formát:** `docs/git-branching` alebo `docs/api-reference`
- **Účel:** Dokumentačné zmeny
- **Životný cyklus:**
  - Vytvorenie z `main`
  - Aktualizácia dokumentácie
  - Merge do `main` cez PR alebo direct commit (ak len docs)

---

## 🚫 DEPRECATED Branch Typy

### ❌ **`session-*`** - Session Branches (DEPRECATED)
- **Dôvod:** Session management sa presunul do `development/sessions/`
- **Akcia:** Všetky session branchy sa zlúčia do `main` a vymažú
- **Nahradenie:** Použiť `feature/*` alebo `quest/*` podľa typu práce

### ❌ **`codex/*`** - Codex Branches (DEPRECATED)
- **Dôvod:** Codex workflow sa už nepoužíva
- **Akcia:** Všetky codex branchy sa zlúčia do `main` a vymažú
- **Nahradenie:** Použiť `feature/*` alebo `quest/*`

---

## 📝 Naming Conventions

### Pravidlá:
1. **Malé písmená** - všetky branchy v lowercase
2. **Pomlčky** - používať `-` namiesto `_` alebo medzier
3. **Popisné názvy** - jasne identifikovať účel branchu
4. **Krátke názvy** - max 50 znakov

### Príklady:
```
✅ DOBRE:
- feature/youtube-processing
- quest/18-git-branching
- fix/memory-bug
- refactor/rag-index

❌ ZLE:
- session-pondelok-2025-12-08
- Feature/YouTubeProcessing
- quest_18_git_branching
- fix-memory-bug-urgent-important
```

---

## 🔄 Workflow

### Vytvorenie nového branchu:

```bash
# 1. Uisti sa, že si na main a máš najnovšie zmeny
git checkout main
git pull origin main

# 2. Vytvor nový branch
git checkout -b feature/nazov-funkcie
# alebo
git checkout -b quest/18-nazov-questu

# 3. Pracuj na zmene
git add .
git commit -m "feat: popis zmeny"

# 4. Pushni branch
git push origin feature/nazov-funkcie

# 5. Vytvor Pull Request na GitHub
gh pr create --title "Názov PR" --body "Popis"
```

### Merge do main:

```bash
# 1. Vytvor Pull Request (cez GitHub UI alebo gh CLI)
gh pr create --title "Názov PR" --body "Popis"

# 2. Po schválení PR sa automaticky merge do main
# 3. Vymaž lokálny branch
git checkout main
git pull origin main
git branch -d feature/nazov-funkcie

# 4. Vymaž remote branch (ak existuje)
git push origin --delete feature/nazov-funkcie
```

---

## 🧹 Cleanup Process

### Automatický cleanup:
- Po merge PR sa branch automaticky vymaže (ak je nastavené v GitHub settings)

### Manuálny cleanup:

```bash
# 1. Zisti ktoré branchy sú už zlúčené
git branch --merged main | grep -v main

# 2. Vymaž lokálne branchy
git branch -d branch-name

# 3. Vymaž remote branchy
git push origin --delete branch-name

# 4. Vyčistiť tracking branchy
git remote prune origin
```

---

## 📊 Branch Status Dashboard

### Aktuálne aktívne branchy:
- `main` - Production branch
- `feature/*` - Aktívne features
- `quest/*` - Aktívne questy

### Deprecated branchy (na vymazanie):
- `session-*` - Všetky session branchy
- `codex/*` - Všetky codex branchy
- `automation-helper` - Ak už nie je potrebný

---

## 🎯 Best Practices

1. **Časté commity** - commituj často s jasnými správami
2. **Pull pred push** - vždy pull pred pushom
3. **Rebase namiesto merge** - pre čistejšiu históriu (voliteľné)
4. **PR review** - vždy review pred merge do main
5. **Cleanup** - pravidelne vymazávať staré branchy

---

## 🔗 Súvisiace Dokumenty

- [ARCHITECTURE.md](ARCHITECTURE.md) - Systémová architektúra
- [SESSION_MANAGEMENT.md](SESSION_MANAGEMENT.md) - Session management
- [README.md](../README.md) - Hlavný README

---

## 📝 Changelog

### 2025-12-08 - v1.0.0
- Vytvorenie nového branching modelu
- Deprecation session a codex branchov
- Dokumentácia workflow a best practices

