# Prompt Templates

Tento adresár obsahuje špecializované prompt šablóny pre agentické systémy, adaptované z Context Engineering repozitára.

## Dostupné Šablóny

### Memory Agent (`memory_agent.md`)
Modulárny systém pre správu knowledge base a organizačnej pamäte.

**Workflow:**
1. **Ingest** - Načítanie nových knowledge nodes
2. **Curate** - Čistenie a deduplikácia
3. **Semantic Link** - Vytváranie sémantických prepojení
4. **Contextual Retrieve** - Kontextové vyhľadávanie
5. **Recursive Refine** - Rekurzívne vylepšovanie
6. **Audit/Version** - Audit a verzovanie zmien

**Použitie:**
- Knowledge base management
- MinisterOfMemory vylepšenia
- Save game struktúry

### Verification Loop (`verification_loop.md`)
Šablóna pre self-verification procesy - zachytávanie chýb, validácia výsledkov.

**Použitie:**
- Quest validácia (Anthropic Harness Pattern)
- Code review
- Kritické rozhodnutia
- Komplexné výpočty

**Variácie:**
- Triple Check Verification
- Peer Review Simulation
- Progressive Refinement

### Chain of Thought (`chain_of_thought.md`)
Šablóna pre explicitné step-by-step reasoning procesy.

**Použitie:**
- Komplexné problémy
- Logické úvahy
- Multi-step analýzy
- Transparentné reasoning

**Variácie:**
- Self-Prompted Chain of Thought
- Guided Problem Decomposition
- Scenario Analysis

## Integrácia s XVADUR Systémom

### MinisterOfMemory
- `memory_agent.md` poskytuje framework pre vylepšenie `core/ministers/memory.py`
- Workflow: ingest → curate → link → retrieve → refine → audit

### Quest System
- `verification_loop.md` sa používa pre Quest validáciu
- Integrácia s `scripts/utils/validate_quest.py`

### Context Engineering
- Všetky šablóny sú kompatibilné s `core/context_engineering/`
- Môžu byť použité v `CognitiveTool` a `PromptProgram`

## Použitie

### Základné použitie

```python
from pathlib import Path

# Načítaj šablónu
template_path = Path("templates/prompts/memory_agent.md")
template = template_path.read_text()

# Nahraď parametre
filled_template = template.replace("{{parameter}}", "value")
```

### Integrácia s Cognitive Tools

```python
from core.context_engineering.cognitive_tools import PromptProgram

# Vytvor program z šablóny
program = PromptProgram(
    description="Memory management workflow",
    template=template
)

# Spusti program
result = program.execute(context={...})
```

## Pôvod

Šablóny sú adaptované z:
- `external/Context-Engineering/20_templates/PROMPTS/`
- Verzia: 2025-07-08
- Licencia: Podľa pôvodného repozitára

## Ďalšie Šablóny

Pre viac šablón pozri:
- `external/Context-Engineering/20_templates/PROMPTS/` (pôvodný zdroj)
- `core/context_engineering/cognitive_tools.py` (implementácia)

