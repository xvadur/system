---
description: Automatické ukladanie user promptov do prompts_log.jsonl v reálnom čase
---

# AUTOMATICKÉ UKLADANIE PROMPTOV

Tento systém automaticky ukladá každý user prompt do `xvadur/data/prompts_log.jsonl` v reálnom čase, bez čakania na file watcher alebo Cursor súbory.

## Ako to funguje

1. **Automatický hook v `.cursorrules`:**
   - Pri každej odpovedi sa automaticky spustí ukladanie promptu
   - Uloženie sa deje ticho, bez zobrazovania v odpovedi
   - Používa `scripts/auto_save_prompt.py`

2. **Helper skript:**
   - `scripts/auto_save_prompt.py` - ukladá prompty do MinisterOfMemory
   - Používa `FileStore` pre trvalé ukladanie
   - Automaticky pridáva metadata (timestamp, source, extraction_method)

## Použitie

### Automatické (odporúčané)
Systém funguje automaticky - každý user prompt sa uloží pri každej odpovedi.

### Manuálne
Ak potrebuješ uložiť prompt manuálne:

```bash
source .venv/bin/activate
python3 scripts/auto_save_prompt.py "Tvoj prompt tu"
```

Alebo v Python kóde:

```python
from scripts.auto_save_prompt import save_prompt
save_prompt("Tvoj prompt tu")
```

## Výhody

- ✅ **Reálny čas** - prompty sa ukladajú okamžite, nie po uložení Cursor súborov
- ✅ **Spoľahlivosť** - nezávislé od file watchera alebo Cursor ukladania
- ✅ **Ticho** - neobťažuje odpoveď
- ✅ **Automatické** - funguje bez manuálnej práce

## Súvisiace súbory

- `scripts/auto_save_prompt.py` - helper skript
- `xvadur/data/prompts_log.jsonl` - úložisko promptov
- `.cursorrules` - obsahuje automatický hook
- `ministers/memory.py` - MinisterOfMemory systém
- `ministers/storage.py` - FileStore implementácia

