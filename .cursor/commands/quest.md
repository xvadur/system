---
description: Vytvorí GitHub Issue (Quest) pre úlohu a zapíše do lokálneho logu.
---

# SYSTEM PROMPT: QUEST COMMAND

Tvojou úlohou je vytvoriť **GitHub Issue (Quest)** pre úlohu, ktorú užívateľ zadá, a automaticky ju synchronizovať s lokálnym logom.

## 🎯 Účel

Quest System umožňuje jednoducho vytvárať a trackovať úlohy cez GitHub Issues. Každá úloha sa automaticky:
- Vytvorí ako GitHub Issue
- Zapíše do lokálneho logu (`development/logs/XVADUR_LOG.md`)
- Môže sa automaticky zatvoriť po dokončení (cez commit message `fixes #123`)

## 📋 Workflow

### 1. Vytvorenie Questu

**Vstup:** Užívateľ zadá `/quest [popis úlohy]`

**Príklady:**
```
/quest Uprav cursorrules - pridať MCP pravidlo
/quest Oprav nekonzistentné cesty v dokumentácii
/quest Implementovať automatické zatváranie Issues
```

### 2. Postup (Agent MUSÍ vykonať)

#### Krok 1: Extrahovať popis úlohy
- Získaj text za `/quest` ako popis úlohy
- Ak je popis prázdny, požiadaj užívateľa o doplnenie

#### Krok 2: Vytvoriť GitHub Issue cez MCP

Použi Python kód na vytvorenie Issue:

```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd()))

from scripts.mcp_helpers import create_github_issue

# Extrahuj popis úlohy z user_query
quest_description = "Uprav cursorrules - pridať MCP pravidlo"  # Získaj z user inputu

# Vytvor Issue
result = create_github_issue(
    title=quest_description,
    body=f"""## Quest: {quest_description}

**Vytvorené:** Automaticky cez `/quest` command
**Status:** Open

## Popis
{quest_description}

## Poznámky
- Táto úloha bola vytvorená automaticky
- Po dokončení pridaj `fixes #{issue_number}` do commit message pre automatické zatvorenie
""",
    labels=["quest", "task"]
)

if result.get("success"):
    issue_number = result.get("number")
    issue_url = result.get("url")
    print(f"✅ Vytvorená úloha #{issue_number}: {quest_description}")
    print(f"🔗 {issue_url}")
else:
    print(f"❌ Chyba pri vytváraní Issue: {result.get('error', 'Neznáma chyba')}")
```

#### Krok 3: Zapísať do lokálneho logu

**⚠️ KRITICKÉ:** Po vytvorení Issue MUSÍŠ okamžite zapísať do `development/logs/XVADUR_LOG.md`.

**Formát zápisu:**
```markdown
[HH:MM] 🔹 Vytvorená úloha #123: [Popis úlohy]
```

**Príklad:**
```markdown
[14:30] 🔹 Vytvorená úloha #123: Uprav cursorrules - pridať MCP pravidlo
```

**Technika:**
1. Načítaj aktuálny čas (použi `get_time_from_mcp()` z `mcp_helpers.py` alebo `datetime.now()`)
2. Načítaj `development/logs/XVADUR_LOG.md`
3. Pridaj nový záznam na začiatok súboru (po hlavičke)
4. Ulož súbor

**Python kód pre zápis:**
```python
from datetime import datetime
from pathlib import Path

log_path = Path("development/logs/XVADUR_LOG.md")
current_time = datetime.now().strftime("%H:%M")

log_entry = f"\n[{current_time}] 🔹 Vytvorená úloha #{issue_number}: {quest_description}\n"

# Načítaj súbor
with open(log_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Vlož záznam po hlavičke (po "---")
if "---" in content:
    parts = content.split("---", 2)
    if len(parts) >= 2:
        new_content = parts[0] + "---" + parts[1] + log_entry + parts[2] if len(parts) > 2 else parts[0] + "---" + parts[1] + log_entry
    else:
        new_content = content + log_entry
else:
    # Ak nie je hlavička, pridaj na začiatok
    new_content = log_entry + content

# Ulož súbor
with open(log_path, 'w', encoding='utf-8') as f:
    f.write(new_content)
```

#### Krok 4: Vrátiť výsledok užívateľovi

**Formát výstupu:**
```
✅ Vytvorená úloha #123: Uprav cursorrules - pridať MCP pravidlo
🔗 https://github.com/xvadur/system/issues/123

📝 Zapísané do logu: development/logs/XVADUR_LOG.md

💡 Tip: Po dokončení úlohy pridaj `fixes #123` do commit message pre automatické zatvorenie Issue.
```

## 🔄 Integrácia s Workflow

### Po vytvorení Questu

1. **Agent môže začať pracovať na úlohe:**
   - Upravovať súbory
   - Zapisovať do logu pribežne
   - V commit message použiť Issue number: `feat: uprav cursorrules (#123)`

2. **Automatické zatvorenie:**
   - GitHub automaticky zatvorí Issue, ak commit message obsahuje:
     - `fixes #123`
     - `closes #123`
     - `resolves #123`
   - Alebo explicitne cez `/quest close #123`

### Explicitné zatvorenie Questu

Ak chce užívateľ zatvoriť Quest explicitne:
```
/quest close #123
```

Agent MUSÍ:
1. Zatvoriť Issue cez MCP (`close_github_issue()`)
2. Zapísať do logu: `[HH:MM] ✅ Dokončená úloha #123: [Popis]`

## 📝 Príklady Použitia

### Príklad 1: Jednoduchá úloha
```
Užívateľ: /quest Oprav typo v README.md

Agent:
1. Vytvorí Issue #124: "Oprav typo v README.md"
2. Zapíše do logu: [15:20] 🔹 Vytvorená úloha #124: Oprav typo v README.md
3. Vráti Issue number a URL
```

### Príklad 2: Komplexná úloha
```
Užívateľ: /quest Refaktorovať mcp_helpers.py - pridať error handling

Agent:
1. Vytvorí Issue #125 s detailným popisom
2. Zapíše do logu
3. Môže začať pracovať na úlohe
```

## ⚠️ Dôležité

- **Vždy zapísať do logu:** Bez zápisu do logu sa Quest nestráca, ale nie je viditeľný v chronologickom prehľade
- **Issue number:** Vždy vráť Issue number užívateľovi pre tracking
- **Fallback:** Ak MCP nie je dostupný, Issue sa nevytvorí, ale zapíše sa do logu s poznámkou
- **Repository:** Issues sa vytvárajú v `xvadur/system` repozitári

## 🔗 Súvisiace

- **MCP Helpers:** `scripts/mcp_helpers.py` - funkcie `create_github_issue()`, `close_github_issue()`
- **Lokálny log:** `development/logs/XVADUR_LOG.md`
- **Dokumentácia:** `docs/QUEST_SYSTEM.md`

---
**Spúšťač:** `/quest [popis úlohy]`

