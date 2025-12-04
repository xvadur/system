# 🎯 Token Optimization Strategy

**Kritický problém:** Spotrebovaných 77% tokenov (48M) za jeden deň, zostáva len 5€.

## 📊 Analýza Problému

### Aktuálna Situácia
- **Cursor Pro:** 20€ kredit
- **Spotrebované:** 77% (48M tokenov)
- **Zostáva:** 5€ (~12M tokenov)
- **Čas:** Jeden deň práce

### Príčiny Vysokej Spotreby

1. **Veľký kontext v `.cursorrules`**
   - Dlhý systémový prompt
   - Opakujúce sa inštrukcie
   - Veľa dokumentácie v kontexte

2. **Časté AI volania**
   - Každý `/savegame` volá AI
   - Každý `/quest` volá AI
   - Automatické operácie cez AI

3. **Veľký workspace**
   - Veľa súborov v kontexte
   - Automatické načítanie celého workspace

## 🎯 Stratégie Optimalizácie

### 1. Optimalizácia `.cursorrules` (PRIORITA #1)

**Aktuálny stav:** ~1000+ riadkov, veľa opakujúcich sa inštrukcií

**Riešenia:**
- **Zmenšiť `.cursorrules` na minimum** - len základné inštrukcie
- **Použiť selektívne načítanie** - `/loadgame` len keď je potrebné
- **Presunúť dokumentáciu** - z `.cursorrules` do `docs/` a načítavať len keď je potrebné
- **Komprimovať inštrukcie** - odstrániť opakujúce sa časti

**Očakávaná úspora:** 30-50% tokenov

### 2. Redukcia AI Volaní

**Aktuálne problémy:**
- Každý `/savegame` volá AI pre generovanie naratívu
- Každý `/quest` volá AI
- Automatické operácie cez AI

**Riešenia:**
- **Menej časté `/savegame`** - len na konci dňa alebo po významných milestone
- **Použiť templates** - namiesto AI generovania použiť šablóny
- **Batch operácie** - zoskupiť viacero úloh do jedného AI volania
- **MCP namiesto AI** - použiť MCP pre automatizácie namiesto AI

**Očakávaná úspora:** 20-30% tokenov

### 3. Optimalizácia Workspace Kontextu

**Aktuálne problémy:**
- Cursor automaticky načítava celý workspace
- Veľa súborov v kontexte

**Riešenia:**
- **`.cursorignore`** - ignorovať nepotrebné súbory (archív, node_modules, atď.)
- **Selektívne otváranie** - otvárať len súbory, ktoré sú potrebné
- **Redukcia počtu súborov** - presunúť archív mimo workspace

**Očakávaná úspora:** 10-20% tokenov

### 4. Alternatívne Nástroje

**Možnosti:**
- **Lokálne AI modely** (Ollama, LM Studio) - bez tokenov, ale pomalšie
- **GitHub Copilot** - iná cenová štruktúra (možno výhodnejšia)
- **Kombinácia nástrojov** - Cursor len pre komplexné úlohy, lokálne AI pre jednoduchšie

### 5. Workflow Optimalizácia

**Zmeny:**
- **Menej automatizácie** - manuálne operácie namiesto AI
- **Git hooks namiesto AI** - automatizácia cez git hooks
- **Templates namiesto generovania** - použiť šablóny namiesto AI generovania

## 📋 Konkrétny Akčný Plán

### Fáza 1: Okamžité Úspory (Dnes)

1. **Zmenšiť `.cursorrules`**
   - Odstrániť opakujúce sa časti
   - Presunúť dokumentáciu do `docs/`
   - Zostane len základné: USER PROFILE, AGENT PERSONA, základné inštrukcie

2. **Vytvoriť `.cursorignore`**
   ```
   archive/
   node_modules/
   .git/
   data/rag_index/
   *.log
   ```

3. **Redukcia `/savegame`**
   - Len na konci dňa
   - Použiť template namiesto AI generovania

### Fáza 2: Strednodobé Úspory (Tento týždeň)

1. **Optimalizácia workflow**
   - Batch operácie
   - MCP namiesto AI kde je to možné
   - Templates pre opakujúce sa úlohy

2. **Presun archívu**
   - Presunúť `archive/` mimo workspace
   - Redukcia počtu súborov v workspace

### Fáza 3: Dlhodobé Riešenie (Tento mesiac)

1. **Vyhodnotiť alternatívy**
   - Testovať lokálne AI modely
   - Porovnať GitHub Copilot
   - Kombinácia nástrojov

2. **Monitorovanie spotreby**
   - Trackovať spotrebu tokenov
   - Identifikovať najväčšie žrúty
   - Optimalizovať postupne

## 💡 Odporúčania

### Pre Denné Použitie

1. **Použiť Cursor selektívne**
   - Len pre komplexné úlohy
   - Jednoduchšie úlohy riešiť manuálne alebo lokálnym AI

2. **Optimalizovať prompty**
   - Kratšie, konkrétnejšie prompty
   - Batch operácie namiesto viacerých malých

3. **Použiť MCP kde je to možné**
   - GitHub operácie cez MCP
   - Automatizácie cez MCP namiesto AI

### Pre Finančnú Udržateľnosť

1. **Zvážiť alternatívy**
   - GitHub Copilot (možno výhodnejšie)
   - Lokálne AI modely (bez tokenov)
   - Kombinácia nástrojov

2. **Monitorovať spotrebu**
   - Trackovať denné náklady
   - Identifikovať najväčšie žrúty
   - Optimalizovať postupne

## 🚨 Kritické Akcie (Teraz)

1. ✅ **Zmenšiť `.cursorrules`** - odstrániť opakujúce sa časti
2. ✅ **Vytvoriť `.cursorignore`** - ignorovať nepotrebné súbory
3. ✅ **Redukcia `/savegame`** - len na konci dňa
4. ✅ **Použiť templates** - namiesto AI generovania

---

**Vytvorené:** 2025-12-04  
**Status:** 🔴 Kritické - Potrebuje urgentné riešenie

