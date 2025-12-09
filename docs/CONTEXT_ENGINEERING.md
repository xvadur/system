# Context Engineering Integration

Tento dokument popisuje integráciu Context Engineering praktík do Magnum Opus systému.

## Prehľad

Quest #20 implementuje štyri kľúčové patterns z Context-Engineering repozitára:

1. **Compress Context** - Rekurzívna konsolidácia pamäte
2. **Isolate Context** - Úlohou-špecifická izolácia kontextu
3. **Cognitive Tools** - Modulárne reasoning tools
4. **Token Metrics** - Tracking a evaluácia tokenov

## 1. Compress Context

### Účel
Rekurzívne konsoliduje pamäť pre efektívnejšie využitie tokenov.

### Použitie

```python
from core.context_engineering import CompressContextManager
from core.ministers.storage import FileStore
from pathlib import Path

# Inicializuj manažéra
store = FileStore(Path("development/data/prompts_log.jsonl"))
compressor = CompressContextManager(store)

# Konsoliduj pamäť
result = compressor.consolidate_memory(
    limit=20,  # Počet záznamov na konsolidáciu
    target_compression_ratio=0.5  # Cieľový kompresný pomer (50%)
)

print(f"Kompresia: {result.original_count} -> {result.compressed_count}")
print(f"Pomer: {result.compression_ratio:.2f}")
print(f"Obsah: {result.preserved_content}")
```

### Výhody
- **Token Efficiency**: Zníženie tokenov o 50%+ pri zachovaní kľúčových informácií
- **Recursive Improvement**: Iteratívne zlepšovanie kompresie
- **Metadata Preservation**: Zachovanie dôležitých metadát

## 2. Isolate Context

### Účel
Vytvorí minimálny, úlohou-špecifický kontext.

### Použitie

```python
from core.context_engineering import IsolateContextManager
from core.ministers.memory import MemoryRecord

# Inicializuj manažéra
isolator = IsolateContextManager()

# Izoluj kontext pre úlohu
isolation = isolator.isolate_for_task(
    task_id="quest-20",
    task_description="Implementovať Context Engineering",
    records=memory_records,
    keywords={"context", "engineering", "token", "optimization"}
)

print(f"Izolovaný obsah ({isolation.token_count} tokenov):")
print(isolation.isolated_content)

# Vytvor minimálny kontext
minimal = isolator.create_minimal_context(
    task_description="Implementovať Context Engineering",
    records=memory_records,
    max_tokens=800
)
```

### Výhody
- **Task-Specific**: Len relevantný kontext pre úlohu
- **Token Optimization**: Cieľový počet tokenov
- **Keyword Filtering**: Filtrovanie podľa kľúčových slov

## 3. Cognitive Tools

### Účel
Modulárne reasoning tools pre lepšie riešenie problémov.

### Použitie

```python
from core.context_engineering import (
    PromptProgram,
    CognitiveTool,
    create_analysis_tool,
    create_problem_solving_tool
)

# Vytvor prompt program
program = PromptProgram(
    description="Analyzovať a riešiť problém s token optimalizáciou"
)

# Pridaj kroky
program.add_step("Identifikuj hlavné problémy s token spotrebou")
program.add_step("Analyzuj príčiny vysokého využitia tokenov")
program.add_step("Navrhnite riešenia pre optimalizáciu")
program.add_step("Implementuj najlepšie riešenie")

# Formátuj pre použitie v prompte
formatted = program.format()
print(formatted)

# Použi preddefinovaný tool
analysis_tool = create_analysis_tool()
print(analysis_tool.format())
```

### Preddefinované Tools
- `create_analysis_tool()` - Analýza problémov
- `create_problem_solving_tool()` - Riešenie problémov
- `create_decision_making_tool()` - Rozhodovanie

### Výhody
- **Modular Reasoning**: Rozdelenie komplexných úloh na kroky
- **Reusability**: Znovupoužiteľné tools
- **Structured Output**: Štruktúrovaný výstup

## 4. Token Metrics

### Účel
Tracking a evaluácia tokenov pre optimalizáciu.

### Použitie

```python
from core.context_engineering import TokenBudgetTracker, TokenBudget

# Inicializuj tracker
budget = TokenBudget(
    context_window_size=16000,  # 16K tokens
    system_allocation=0.15,    # 15% pre system
    history_allocation=0.40,    # 40% pre históriu
    current_allocation=0.30,    # 30% pre aktuálny input
    reserve_allocation=0.15     # 15% rezerva
)

tracker = TokenBudgetTracker(budget)

# Trackuj použitie
metrics = tracker.track_usage(
    system_content="You are a helpful assistant...",
    history_content="Previous conversation...",
    current_content="Current user input...",
    output_content="Assistant response..."
)

print(f"Celkové tokeny: {metrics.total_tokens}")
print(f"Utilization: {metrics.utilization_ratio(16000):.2%}")

# Skontroluj budget
budget_check = tracker.check_budget(
    system_content="...",
    history_content="...",
    current_content="..."
)

if not budget_check["within_budget"]:
    print("⚠️ Presahuje budget!")
    for warning in budget_check["warnings"]:
        print(f"  - {warning}")
```

### Výhody
- **Real-Time Tracking**: Sledovanie tokenov v reálnom čase
- **Budget Alerts**: Varovania pri presiahnutí budgetu
- **Component Analysis**: Analýza jednotlivých komponentov

## Integrácia s MinisterOfMemory

```python
from core.ministers.memory import MinisterOfMemory, AssistantOfMemory
from core.ministers.storage import FileStore
from core.context_engineering import (
    CompressContextManager,
    IsolateContextManager,
    TokenBudgetTracker
)
from pathlib import Path

# Inicializuj MinisterOfMemory
store = FileStore(Path("development/data/prompts_log.jsonl"))
assistant = AssistantOfMemory(store=store)
minister = MinisterOfMemory(assistant=assistant)

# Pridaj Context Engineering komponenty
compressor = CompressContextManager(store)
isolator = IsolateContextManager()
tracker = TokenBudgetTracker()

# Použi v workflow
# 1. Trackuj tokeny
metrics = tracker.track_usage(...)

# 2. Ak je budget vysoký, komprimuj
if metrics.utilization_ratio(16000) > 0.8:
    result = compressor.consolidate_memory(limit=20, target_compression_ratio=0.5)
    print(f"Kompresia dokončená: {result.compression_ratio:.2f}")

# 3. Izoluj kontext pre novú úlohu
isolation = isolator.isolate_for_task(
    task_id="new-task",
    task_description="Nová úloha",
    records=minister.review_context(limit=10)
)
```

## Best Practices

1. **Compress Context**: Použi keď utilization > 80%
2. **Isolate Context**: Použi pre nové úlohy s veľkým kontextom
3. **Cognitive Tools**: Použi pre komplexné reasoning úlohy
4. **Token Metrics**: Trackuj kontinuálne pre optimalizáciu

## Integration Guide

### Ako funguje automatická integrácia

Context Engineering komponenty sú automaticky integrované do workflow:

1. **Pri `/loadgame`:**
   - Automaticky sa trackujú tokeny pri načítaní kontextu
   - Ak utilization > 80%, automaticky sa aplikuje kompresia
   - Pre nové questy sa automaticky izoluje kontext

2. **Pri ukladaní promptov:**
   - Každý prompt sa trackuje pred uložením
   - Ak utilization > 80%, automaticky sa komprimujú staršie prompty

3. **Pri exporte do logu:**
   - Pred exportom sa aplikuje kompresia ak je promptov veľa (>30)
   - Používa sa izolácia kontextu pre relevantné záznamy

### Konfigurácia Thresholds

Konfigurácia je v `development/data/context_engineering_config.json`:

```json
{
  "compression_threshold": 0.8,        // 80% utilization - trigger pre kompresiu
  "target_compression_ratio": 0.5,    // 50% redukcia tokenov
  "context_window_size": 16000,       // 16K tokens
  "isolation_max_tokens": 800,        // Max tokenov pre izoláciu
  "compression_max_iterations": 3,    // Max iterácií pre kompresiu
  "isolation_max_turns": 3            // Max výmen v histórii
}
```

### Príklady použitia v workflow

#### Automatická integrácia v `/loadgame`

```python
# V loadgame.md command sa automaticky používa:
from core.context_engineering.integration import load_context_with_optimization

result = load_context_with_optimization(
    save_game_path=Path("development/sessions/save_games/SAVE_GAME_LATEST.json"),
    log_path=Path("development/logs/XVADUR_LOG.jsonl"),
    auto_compress=True,
    auto_isolate=True
)

# Výsledok obsahuje token metriky a informáciu o kompresii
print(f"Utilization: {result['utilization']:.2%}")
print(f"Kompresia: {'Áno' if result['compressed'] else 'Nie'}")
```

#### Použitie v existujúcich skriptoch

```python
# V save_conversation_prompts.py sa automaticky trackujú tokeny
from core.context_engineering.token_metrics import TokenBudgetTracker

tracker = TokenBudgetTracker()
token_count = tracker.estimate_tokens(prompt_content)

# Ak utilization > threshold, automaticky sa komprimuje
if utilization > COMPRESSION_THRESHOLD:
    compressor.consolidate_memory(...)
```

#### Použitie MinisterOfMemory s Context Engineering

```python
from core.ministers.memory import MinisterOfMemory

minister = MinisterOfMemory(...)

# Automatická kompresia pri review_context
result = minister.get_context_with_compression(limit=20)
if result['compressed']:
    print(f"Kompresia aplikovaná: {result['utilization']:.2%}")

# Izolácia kontextu pre úlohu
isolation = minister.isolate_context_for_task(
    task_id="quest-20",
    task_description="Implementovať Context Engineering",
    keywords={"context", "engineering"}
)
print(f"Izolovaný obsah: {isolation['isolated_content']}")
```

### Best Practices

1. **Compress Context:** Použi keď utilization > 80%
2. **Isolate Context:** Použi pre nové úlohy s veľkým kontextom
3. **Token Metrics:** Trackuj kontinuálne pre optimalizáciu
4. **Konfigurácia:** Uprav thresholds podľa potreby v `context_engineering_config.json`

## Referencie

- [Context-Engineering Repozitár](../../external/Context-Engineering/)
- [Recursive Context Template](../../external/Context-Engineering/20_templates/recursive_context.py)
- [Minimal Context Template](../../external/Context-Engineering/20_templates/minimal_context.yaml)
- [Prompt Program Template](../../external/Context-Engineering/20_templates/prompt_program_template.py)
- [Token Budgeting Guide](../../external/Context-Engineering/40_reference/token_budgeting.md)

