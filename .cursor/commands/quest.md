---
description: Vytvorí GitHub Issue (Quest) pre úlohu a zapíše do lokálneho logu.
---

# QUEST COMMAND

Spravuje celý životný cyklus questov – od vytvorenia cez aktualizáciu stavu až po uzatvorenie – a automaticky ich synchronizuje s lokálnym logom.

## Workflow

1. **Extrahuj popis úlohy** z `/quest [popis]`
2. **Vytvor alebo aktualizuj GitHub Issue cez MCP**  
   - Nový quest: `scripts/mcp_helpers.create_github_issue()`  
   - Úprava statusu (pozastavený, ukončený, checkpoint): `scripts/mcp_helpers.update_github_issue()` alebo pridaním komentára
3. **Loguj akciu do session.md** (`development/sessions/current/session.md` v sekcii Tasks):  
   - Pridanie: `- [HH:MM] Quest #123: [Popis] | Status: new`  
   - Aktualizácia/pozastavenie/ukončenie/checkpoint: `- [HH:MM] Quest #123: [Popis] | Status: paused/closed/checkpoint [alebo iný]` (podľa akcie)  
   - Komentár: pripoj poznámku alebo dôvod k zmene statusu
4. **Vráť výsledok** užívateľovi (Issue number, URL, prípadne potvrdenie o zmene alebo checkpointu)

## Automatické zatvorenie

GitHub automaticky zatvorí Issue, ak commit message obsahuje: `fixes #123`, `closes #123`, `resolves #123`

## Technické detaily

Pozri `docs/QUEST_SYSTEM.md` pre kompletnú dokumentáciu, príklady a Python kód.

---
**Spúšťač:** `/quest [popis úlohy]`
