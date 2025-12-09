# Context Engineering Schemas

Tento adresár obsahuje referenčné JSON schémy pre context engineering, adaptované z Context Engineering repozitára.

## Dostupné Schémy

### `context_v6.json`
Najkomplexnejšia verzia context schémy (v6.0.0) obsahujúca:

**Kľúčové komponenty:**
- **Repository Context** - Štruktúra repozitára, learning path, file tree
- **Conceptual Framework** - Biological metaphor (atoms → meta-recursive)
- **Protocol Framework** - 10 core protocols + meta-protocols
- **Integration Patterns** - System-level a application patterns
- **Mental Models** - Garden, Budget, River, Meta-Recursive, atď.
- **Design Principles** - Karpathy DNA, system design, implementation approach
- **Scoring Rubric** - Metriky pre hodnotenie (clarity, token efficiency, emergence, atď.)

**Protocol Framework:**
1. `attractor_co_emerge` - Strategické scaffoldovanie co-emergence
2. `recursive_emergence` - Rekurzívna field emergence
3. `recursive_memory_attractor` - Evolúcia field memory
4. `field_resonance_scaffold` - Resonance scaffolding
5. `field_self_repair` - Self-healing mechanizmy
6. `context_memory_persistence_attractor` - Long-term persistence
7. `meta_recursive_framework` - Self-reflection a improvement
8. `interpretability_scaffold` - Transparentné štruktúry
9. `collaborative_evolution` - Human-AI co-evolution
10. `cross_modal_bridge` - Cross-modal integration

**Integration Patterns:**
- System-level: self-maintaining coherence, collaborative evolution, adaptive persistence
- Application: persistent conversation, knowledge evolution, collaborative reasoning

## Použitie

### Referenčná Schéma

```python
import json
from pathlib import Path

# Načítaj schému
schema_path = Path("core/context_engineering/schemas/context_v6.json")
schema = json.loads(schema_path.read_text())

# Použi pre validáciu save game formátov
protocols = schema["conceptualFramework"]["protocolFramework"]["coreProtocols"]
```

### Integrácia s Save Game

Schéma môže byť použité ako referenčný formát pre:
- `development/sessions/save_games/SAVE_GAME_LATEST.json`
- Quest validation schemas
- Context Engineering config

### Scoring Rubric

```python
# Použi metriky pre hodnotenie
rubric = schema["conceptualFramework"]["modelInstructions"]["scoringRubric"]

# Príklad: Clarity Score
clarity_score = rubric["clarityScore"]  # 0-1; >0.8 = newbie comprehends
```

## Evolúcia Schém

| Verzia | Kľúčové Koncepty |
|--------|------------------|
| v2.0 | Základná štruktúra (atoms, molecules, cells) |
| v3.0 | Recursive patterns, field protocols |
| v4.0 | Quantum semantics, unified field theory |
| v5.0 | Protocol shells, unified system |
| v6.0 | Meta-recursive, interpretability, collaborative co-evolution |

## Pôvod

Schéma je adaptovaná z:
- `external/Context-Engineering/context-schemas/context_v6.0.json`
- Verzia: 6.0.0 (2024-07-01)
- Licencia: Podľa pôvodného repozitára

## Ďalšie Schémy

Pre viac schém pozri:
- `external/Context-Engineering/context-schemas/` (pôvodný zdroj)
- `60_protocols/schemas/` v pôvodnom repe

