# 💾 SAVEGAME - Token Optimization Guide

**Problém:** `/savegame` workflow spotrebúval ~5M tokenov kvôli:
- Čítaniu celých súborov namiesto selektívneho načítania
- Chýbajúcemu token trackingu
- Neaplikovaniu context engineering kompresie

**Riešenie:** Optimalizovaný workflow s integrovaným context engineeringom.

---

## 🎯 Kľúčové Princípy

### 1. Selektívne Načítanie

**❌ ZLE:**
```python
# Číta celý súbor (373 riadkov = ~15K tokenov)
read_file('development/sessions/save_games/SAVE_GAME.md')
```

**✅ DOBRE:**
```python
# Len posledný záznam (posledných 100 riadkov = ~4K tokenov)
read_file('development/sessions/save_games/SAVE_GAME.md', offset=-100)

# Alebo len sekcia
read_file('development/logs/XVADUR_XP.md', section="📊 Aktuálny Status")

# Alebo JSON (malý, rýchly)
read_file('development/logs/XVADUR_XP.json')
```

### 2. Token Tracking

**Vždy trackuj tokeny pred načítaním:**
```python
from core.context_engineering.token_metrics import TokenBudgetTracker

tracker = TokenBudgetTracker()
tokens = tracker.estimate_tokens(content)
if tokens > 1000:
    # Použi selektívne načítanie alebo kompresiu
    pass
```

### 3. Kompresia Kontextu

**Aplikuj kompresiu keď utilization > 80%:**
```python
from core.context_engineering.compress_context import CompressContextManager

if utilization > COMPRESSION_THRESHOLD:
    compressor = CompressContextManager(file_store)
    result = compressor.consolidate_memory(
        limit=20,
        target_compression_ratio=0.5
    )
```

### 4. Izolácia Kontextu

**Použi izoláciu pre relevantný kontext:**
```python
from core.context_engineering.isolate_context import IsolateContextManager

isolator = IsolateContextManager()
isolated = isolator.isolate_for_task(
    task_id="savegame",
    task_description="Uložiť save game",
    records=all_records
)
```

---

## 📊 Optimalizovaný Workflow

### Krok 1: Inicializácia

```python
from scripts.utils.optimized_savegame import OptimizedSaveGame

optimizer = OptimizedSaveGame()
```

### Krok 2: Uloženie Promptov (s kompresiou)

```python
prompts = [...]  # Zoznam promptov z konverzácie
saved_count = optimizer.save_prompts_optimized(prompts)
```

**Automaticky:**
- Uloží prompty
- Skontroluje utilization
- Aplikuje kompresiu ak > 80%

### Krok 3: Výpočet XP

```python
xp_data = optimizer.calculate_xp_optimized()
```

**Automaticky:**
- Vypočíta XP
- Aktualizuje súbory
- Vráti data

### Krok 4: Vytvorenie Save Game

```python
save_game = optimizer.create_save_game_optimized(
    narrative=narrative_text,
    quests=quests_list,
    instructions=instructions_dict
)
```

**Automaticky:**
- Načíta len potrebné dáta (selektívne)
- Vytvorí save game objekt
- Uloží JSON a Markdown

### Krok 5: Token Tracking

```python
metrics = optimizer.tracker.get_metrics_summary()
print(f"Token usage: {metrics['utilization_ratio']:.2%}")
```

---

## 📈 Očakávané Úspory

| Operácia | Pred | Po | Úspora |
|----------|------|-----|--------|
| Načítanie SAVE_GAME.md | 15K tokens | 4K tokens | 73% |
| Načítanie XVADUR_LOG.md | 20K tokens | 2K tokens | 90% |
| Načítanie XVADUR_XP.md | 5K tokens | 0.5K tokens | 90% |
| Celkovo | ~5M tokens | ~500K tokens | 90% |

---

## ⚠️ Pravidlá

1. **NIKDY nečítaj celé súbory** - používaj selektívne načítanie
2. **PRIORITA JSON formátov** - rýchlejšie a menšie
3. **Trackuj tokeny** - pred každým read_file
4. **Aplikuj kompresiu** - ak utilization > 80%
5. **Používaj optimalizované metódy** - `OptimizedSaveGame` trieda

---

## 🔧 Integrácia do `/savegame` Command

Aktualizuj `.cursor/commands/savegame.md` s inštrukciami na používanie `OptimizedSaveGame`.

**Pozri:** `.cursor/commands/savegame.md` (aktualizované)
