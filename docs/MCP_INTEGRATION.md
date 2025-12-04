# 🤖 MCP (Multi-Capable Peripheral) Integrácia

**Verzia:** 1.0.0  
**Posledná aktualizácia:** 2025-12-04

---

## Prehľad

Tento dokument popisuje, ako je **MCP Docker systém** integrovaný do XVADUR workspace a ako sa používa v automatizačných procesoch.

MCP (Multi-Capable Peripheral) je systém, ktorý poskytuje prístup k širokej škále nástrojov priamo z Cursor IDE. V tomto projekte je nakonfigurovaný ako `MCP_DOCKER` a obsahuje 59 nástrojov.

---

## Aktuálny Stav

- **MCP Server:** `MCP_DOCKER`
- **Konfigurácia:** V `Cursor Settings`
- **Počet nástrojov:** 59
- **Dostupné služby:**
  - **Obsidian MCP** (13 funkcií): Operácie s knowledge base (vytváranie, čítanie, update poznámok).
  - **GitHub MCP** (50+ funkcií): Kompletná integrácia s GitHub (commity, PR, issues, branches).
  - **Browser MCP** (13 funkcií): Automatizácia webového prehliadača.
  - **Fetch MCP**: Načítavanie obsahu z webu.
  - **Sequential Thinking MCP**: Pokročilé analytické a reasoning nástroje.
  - **Time MCP**: Operácie s časom a časovými zónami.

---

## Architektúra Integrácie

Integrácia je postavená na **fallback logike**, čo znamená, že systém je plne funkčný aj bez prístupu k MCP. To je kľúčové pre robustnosť, najmä v prostredí GitHub Actions, kde MCP nemusí byť dostupné.

### `scripts/mcp_helpers.py`

Tento súbor je centrálnym bodom pre všetku MCP interakciu. Obsahuje wrapper funkcie pre najčastejšie používané MCP nástroje.

**Kľúčové princípy:**
1.  **Abstrakcia:** Skripty nevolajú MCP priamo, ale cez tieto helper funkcie.
2.  **Fallback:** Každá funkcia obsahuje `try...except` blok. Ak volanie MCP zlyhá (napr. `ValueError: MCP not available`), funkcia vykoná alternatívnu, lokálnu operáciu (napr. `subprocess.run(['git', 'commit', ...])`).
3.  **Konzistentné API:** Funkcie poskytujú jednoduché a konzistentné rozhranie pre skripty.

**Príklad (`git_commit_via_mcp`):**
```python
def git_commit_via_mcp(message: str, files: list) -> bool:
    """Commit cez GitHub MCP (ak je dostupný).
    
    Fallback: subprocess git commit
    """
    try:
        # Tu by bolo volanie GitHub MCP
        # napr. mcp_proxy.call('github.create_commit', ...)
        raise ValueError("MCP not available")
        return True
    except Exception:
        # Fallback na štandardný git
        subprocess.run(['git', 'add'] + files, check=True)
        subprocess.run(['git', 'commit', '-m', message], check=True)
        return True
```

---

## Použitie v Automatizáciách

MCP nástroje sú integrované do kľúčových automatizačných workflowov:

### 1. Auto Session Rotation (`auto-session-rotation.yml`)

- **Time MCP:** Používa sa v `create_new_session.py` na získanie presného timestampu pre novú session.
  - **Fallback:** `datetime.now()` s `zoneinfo`.
- **Sequential Thinking MCP:** Používa sa v `auto_archive_session.py` na vygenerovanie sumáru včerajšej session.
  - **Fallback:** Jednoduché parsovanie a extrakcia kľúčových sekcií z Markdown.
- **Obsidian MCP:** Voliteľný export archivovanej session do Obsidianu.
  - **Fallback:** Žiadna akcia (len logovanie, že export zlyhal).
- **GitHub MCP:** Commit a push zmien.
  - **Fallback:** `subprocess` volanie `git`.

### 2. Morning Review Prep (`morning-review-prep.yml`)

- **Sequential Thinking MCP:** V `generate_daily_review.py` analyzuje včerajšie metriky a sumár a generuje analytický text s odporúčaniami na nový deň.
  - **Fallback:** Formátovaný text s metrikami bez hĺbkovej analýzy.
- **Obsidian MCP:** Voliteľný export denného review do Obsidianu.
  - **Fallback:** Žiadna akcia.

---

## Ako Pridať Nové MCP Nástroje

1.  **Pridaj do `mcp_helpers.py`:** Vytvor novú wrapper funkciu s fallback logikou.
2.  **Integruj do skriptu:** Použi novú helper funkciu v relevantnom automatizačnom skripte.
3.  **Aktualizuj dokumentáciu:** Pridaj informácie o novom nástroji do tohto dokumentu.
