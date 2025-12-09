---
description: Vytvorí GitHub Issue (Quest) pre úlohu a zapíše do lokálneho logu.
---

# QUEST COMMAND

Vytvorí GitHub Issue (Quest) pre úlohu a automaticky ju synchronizuje s lokálnym logom.

## Workflow

1. **Extrahuj popis úlohy** z `/quest [popis]`
2. **Vytvor GitHub Issue cez MCP** (`scripts/mcp_helpers.create_github_issue()`)
3. **Zapíš do logu** (`development/logs/XVADUR_LOG.md`): `[HH:MM] 🔹 Vytvorená úloha #123: [Popis]`
4. **Vráť výsledok** užívateľovi (Issue number, URL)

## Automatické zatvorenie

GitHub automaticky zatvorí Issue, ak commit message obsahuje: `fixes #123`, `closes #123`, `resolves #123`

## Technické detaily

Pozri `docs/QUEST_SYSTEM.md` pre kompletnú dokumentáciu, príklady a Python kód.

---
**Spúšťač:** `/quest [popis úlohy]`
