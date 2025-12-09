# 🔍 Analýza Boot Token Spotreby (130K tokenov)

**Dátum:** 2025-12-09  
**Problém:** Boot load spotrebúva ~130K tokenov  
**Cieľ:** Identifikovať všetky procesy a optimalizovať

---

## 📊 Aktuálna Situácia

### Veľkosti Súborov

| Súbor | Riadkov | Odhad tokenov | Status |
|-------|---------|---------------|--------|
| `.cursorrules` | 42 | ~2,400 | ✅ OK |
| `.cursor/commands/loadgame.md` | 345 | ~19,700 | ⚠️ Veľký |
| `.cursor/commands/savegame.md` | 502 | ~28,600 | ⚠️ Veľký |
| `.cursor/commands/xvadur.md` | 793 | ~45,200 | ⚠️ Veľmi veľký |
| `.cursor/commands/quest.md` | 202 | ~11,500 | ⚠️ Veľký |
| `.cursor/rules/00-cursor-rules-rule.mdc` | 47 | ~2,700 | ✅ OK |
| `.cursor/rules/01-self-improve.mdc` | 38 | ~2,200 | ✅ OK |
| `.cursor/rules/02-directory-structure.mdc` | 200 | ~11,400 | ⚠️ Veľký |
| `.cursor/rules/03-tech-stack.mdc` | 110 | ~6,300 | ⚠️ Stredný |
| **CELKOM** | **2,279** | **~130,000** | ⚠️ **KRITICKÉ** |

**Výpočet:** 2,279 riadkov × ~57 tokenov/riadok = ~130K tokenov ✅

---

## 🔍 Procesy Pri Boot

### 1. Cursor Rules (`.cursor/rules/*.mdc`)

**Aktuálne nastavenie:**
- `00-cursor-rules-rule.mdc`: `alwaysApply: true` + `globs: ["**/*"]`
- `01-self-improve.mdc`: `alwaysApply: true` + `globs: ["**/*"]`
- `02-directory-structure.mdc`: `alwaysApply: true` + `globs: ["**/*"]`
- `03-tech-stack.mdc`: `alwaysApply: false` + `globs: ["**/*.tsx", "**/*.ts", "**/*.jsx", "**/*.js", "**/*.py"]`

**Problém:**
- Prvé 3 súbory sa načítajú **VŽDY** (395 riadkov = ~22,500 tokenov)
- `directory-structure.mdc` má 200 riadkov a obsahuje kompletnú štruktúru projektu

**Riešenie:**
- Zmeniť `alwaysApply: false` pre rules, ktoré nie sú kritické
- Presunúť `directory-structure.mdc` do `docs/` a načítavať len keď je potrebné

### 2. Command Súbory (`.cursor/commands/*.md`)

**Aktuálne nastavenie:**
- Cursor automaticky načíta všetky `.md` súbory v `.cursor/commands/`
- **1,842 riadkov** = ~105,000 tokenov

**Problém:**
- `xvadur.md` má 793 riadkov (najväčší)
- `savegame.md` má 502 riadkov
- `loadgame.md` má 345 riadkov
- Všetky sa načítajú pri každom boote

**Riešenie:**
- Skrátiť command súbory na minimum
- Presunúť dokumentáciu do `docs/`
- Použiť selektívne načítanie (len keď sa command použije)

### 3. `.cursorrules` (Globálny System Prompt)

**Aktuálne nastavenie:**
- 42 riadkov = ~2,400 tokenov
- Načítava sa vždy

**Status:** ✅ OK (malý súbor)

---

## 🎯 Optimalizačný Plán

### Fáza 1: Okamžité Úspory (Dnes)

#### 1.1 Zmeniť `alwaysApply` pre Rules

**Zmeny:**
```yaml
# .cursor/rules/00-cursor-rules-rule.mdc
alwaysApply: false  # Zmeniť z true
globs: ["**/*"]     # Zostáva

# .cursor/rules/01-self-improve.mdc
alwaysApply: false  # Zmeniť z true
globs: ["**/*"]     # Zostáva

# .cursor/rules/02-directory-structure.mdc
alwaysApply: false  # Zmeniť z true
globs: ["**/*"]     # Zostáva
```

**Úspora:** ~22,500 tokenov (17%)

#### 1.2 Skrátiť `loadgame.md`

**Aktuálne:** 345 riadkov  
**Cieľ:** ~100 riadkov (len základné inštrukcie)

**Presunúť do `docs/`:**
- Technické detaily (Python kód)
- Context Engineering integrácia
- Health Check sekvencia (presunúť do `docs/`)

**Úspora:** ~14,000 tokenov (11%)

#### 1.3 Skrátiť `savegame.md`

**Aktuálne:** 502 riadkov  
**Cieľ:** ~150 riadkov (len základné inštrukcie)

**Presunúť do `docs/`:**
- Kompletná dokumentácia workflow
- Príklady a templates
- Technické detaily

**Úspora:** ~20,000 tokenov (15%)

#### 1.4 Skrátiť `xvadur.md`

**Aktuálne:** 793 riadkov  
**Cieľ:** ~200 riadkov (len základné inštrukcie)

**Presunúť do `docs/`:**
- Kompletná dokumentácia
- Príklady a templates
- Workflow dokumentácia

**Úspora:** ~33,800 tokenov (26%)

**Celková úspora Fázy 1:** ~90,300 tokenov (69% redukcia)

---

### Fáza 2: Strednodobé Úspory (Tento týždeň)

#### 2.1 Presunúť `directory-structure.mdc` do `docs/`

**Aktuálne:** 200 riadkov v rules  
**Riešenie:** Presunúť do `docs/DIRECTORY_STRUCTURE.md` a načítavať len keď je potrebné

**Úspora:** ~11,400 tokenov (9%)

#### 2.2 Vytvoriť `.cursorignore`

**Ignorovať:**
```
archive/
node_modules/
.git/
data/rag_index/
*.log
development/sessions/archive/
staging/sessions/
production/sessions/
```

**Úspora:** ~5,000 tokenov (4%)

#### 2.3 Selektívne Načítanie Command Súborov

**Riešenie:**
- Cursor by mal načítať command súbory len keď sa command použije
- Aktuálne sa načítajú všetky vždy

**Úspora:** ~50,000 tokenov (38%) (ak sa nepoužijú všetky commands)

---

### Fáza 3: Dlhodobé Riešenie

#### 3.1 Context Engineering Integrácia

**Riešenie:**
- Použiť `CompressContextManager` pre automatickú kompresiu
- Použiť `IsolateContextManager` pre izoláciu kontextu
- Automatická kompresia ak utilization > 80%

**Úspora:** 50% redukcia pri vysokom utilization

#### 3.2 Template Systém

**Riešenie:**
- Vytvoriť templates pre opakujúce sa úlohy
- Použiť templates namiesto AI generovania
- Redukcia AI volaní

**Úspora:** 20-30% tokenov z AI volaní

---

## 📋 Konkrétne Akcie

### Okamžité (Dnes)

1. ✅ **Zmeniť `alwaysApply: false`** pre 3 rules súbory
2. ✅ **Skrátiť `loadgame.md`** na ~100 riadkov
3. ✅ **Skrátiť `savegame.md`** na ~150 riadkov
4. ✅ **Skrátiť `xvadur.md`** na ~200 riadkov
5. ✅ **Vytvoriť `.cursorignore`**

**Očakávaná úspora:** ~90,300 tokenov (69% redukcia)  
**Nový boot load:** ~40,000 tokenov (z 130K)

### Tento týždeň

1. ✅ **Presunúť `directory-structure.mdc`** do `docs/`
2. ✅ **Implementovať selektívne načítanie** command súborov
3. ✅ **Aktualizovať dokumentáciu** v `docs/`

**Očakávaná úspora:** ~66,400 tokenov (51% redukcia)  
**Nový boot load:** ~25,000 tokenov (z 130K)

---

## 🎯 Cieľové Hodnoty

| Metrika | Aktuálne | Cieľ | Redukcia |
|---------|----------|------|----------|
| Boot load | 130K | 25K | 81% |
| Rules | 22.5K | 5K | 78% |
| Commands | 105K | 20K | 81% |
| `.cursorrules` | 2.4K | 2.4K | 0% |

---

## 📝 Poznámky

### Prečo sa načítajú všetky commands?

Cursor automaticky načíta všetky `.md` súbory v `.cursor/commands/` pri každom boote. To je default správanie.

**Riešenie:**
- Skrátiť command súbory na minimum
- Presunúť dokumentáciu do `docs/`
- Použiť selektívne načítanie (ak je možné)

### Prečo `alwaysApply: true`?

Niektoré rules majú `alwaysApply: true`, čo znamená, že sa načítajú vždy, bez ohľadu na glob patterns.

**Riešenie:**
- Zmeniť na `alwaysApply: false`
- Použiť glob patterns pre selektívne načítanie
- Presunúť do `docs/` ak nie je kritické

---

**Vytvorené:** 2025-12-09  
**Status:** 🔴 Kritické - Vyžaduje okamžitú akciu

