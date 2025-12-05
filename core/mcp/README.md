# 🤖 MCP (Multi-Capable Peripheral) Integrácia

**Verzia:** 2.0.0  
**Posledná aktualizácia:** 2025-12-05
**Umiestnenie:** `core/mcp/README.md`

---

## Prehľad

Tento dokument popisuje, ako je **MCP Docker systém** integrovaný do XVADUR workspace a ako sa používa v automatizačných procesoch.

MCP (Multi-Capable Peripheral) je systém, ktorý poskytuje prístup k širokej škále nástrojov priamo z Cursor IDE. V tomto projekte je nakonfigurovaný ako `MCP_DOCKER` a obsahuje 59 nástrojov.

---

## Architektúra Integrácie

Integrácia je postavená na **fallback logike**, čo znamená, že systém je plne funkčný aj bez prístupu k MCP. To je kľúčové pre robustnosť, najmä v prostredí GitHub Actions, kde MCP nemusí byť dostupné.

### `scripts/mcp_helpers.py`

Tento súbor je centrálnym bodom pre všetku MCP interakciu. Obsahuje wrapper funkcie pre najčastejšie používané MCP nástroje.

**Kľúčové princípy:**
1.  **Abstrakcia:** Skripty nevolajú MCP priamo, ale cez tieto helper funkcie.
2.  **Fallback:** Každá funkcia obsahuje `try...except` blok. Ak volanie MCP zlyhá (napr. `ValueError: MCP not available`), funkcia vykoná alternatívnu, lokálnu operáciu (napr. `subprocess.run(['git', 'commit', ...])`).
3.  **Konzistentné API:** Funkcie poskytujú jednoduché a konzistentné rozhranie pre skripty.

---

## Session Management Systém

### Denný Session Rotation

Systém automaticky spravuje denné sessiony pomocou MCP nástrojov:

1. **O polnoci:** Automatický merge session branch a vytvorenie novej branch pre nasledujúci deň
2. **O 7:00:** Vytvorenie novej session v `sessions/current/` pre aktuálny deň
3. **Archivácia:** Presun predchádzajúcich session do `sessions/archived/`

### GitHub Integrácia

- **Automatické mergovanie:** Denné mergovanie session branch cez GitHub MCP
- **Branch management:** Vytváranie nových branch pre každý deň
- **Commit policies:** Konzistentné commit message formáty

---

## Použitie v Automatizáciách

MCP nástroje sú integrované do kľúčových automatizačných workflowov:

### 1. Denný Session Rotation

- **Time MCP:** Presné timestampy pre session rotation
- **GitHub MCP:** Automatické mergovanie branch a vytváranie nových
- **Sequential Thinking MCP:** Generovanie session sumárov

### 2. Auto Session Creation (`auto-session-rotation.yml`)

- **Time MCP:** Používa sa v `create_new_session.py` na získanie presného timestampu
- **Fallback:** `datetime.now()` s `zoneinfo`
- **GitHub MCP:** Commit a push zmien do session branch

### 3. Morning Review Prep (`morning-review-prep.yml`)

- **Sequential Thinking MCP:** Analýza včerajších metrík a generovanie odporúčaní
- **Obsidian MCP:** Export denného review do knowledge base

---

## Ako Pridať Nové MCP Nástroje

1.  **Pridaj do `mcp_helpers.py`:** Vytvor novú wrapper funkciu s fallback logikou
2.  **Integruj do skriptu:** Použi novú helper funkciu v relevantnom automatizačnom skripte
3.  **Aktualizuj dokumentáciu:** Pridaj informácie o novom nástroji do tohto dokumentu

---

## Súvisiace Dokumenty

- `docs/SESSION_MANAGEMENT.md` - Detailný popis session management systému
- `scripts/mcp_helpers.py` - Hlavný MCP helper modul
- `scripts/create_new_session.py` - Vytváranie nových denných session
- `scripts/auto_archive_session.py` - Archivácia session

