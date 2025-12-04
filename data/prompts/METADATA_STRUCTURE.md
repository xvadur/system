# 📊 Štruktúra Prompt Metadát

**Súbor:** `prompts_enriched.jsonl`  
**Účel:** Konsolidovaná štruktúra všetkých metadát pre prompty

---

## 🔄 Konsolidácia

Tento súbor vznikol zlúčením troch zdrojov:
1. `prompts_activities.jsonl` - Extrakcia aktivít a myšlienok
2. `prompts_nlp4sk.jsonl` - NLP analýza (sentiment, entities, concepts)
3. `prompts_categorized.jsonl` - Kategorizácia a kontext

**Skript:** `scripts/merge_prompt_metadata.py`

---

## 📋 Štruktúra Záznamu

Každý riadok v JSONL súbore je JSON objekt s týmito kľúčmi:

### Základné Metadáta
- `prompt_id` (str) - Unikátny identifikátor (`YYYY-MM-DD_NNN`)
- `date` (str) - Dátum promptu (`YYYY-MM-DD`)
- `timestamp` (str) - ISO timestamp promptu
- `word_count` (int) - Počet slov v prompte

### Activity Metadata
- `activity` (str, optional) - Čo robil (extrahované z promptu)
- `thoughts` (str, optional) - Nad čím rozmýšľal
- `summary_extracted_at` (str, optional) - Kedy bola aktivita extrahovaná

### NLP Metadata
- `sentiment` (str, optional) - Sentiment (`positive`, `negative`, `neutral`)
- `sentiment_score` (float, optional) - Sentiment score (0.0-1.0)
- `people` (List[str], optional) - Extrahované osoby
- `organizations` (List[str], optional) - Extrahované organizácie
- `locations` (List[str], optional) - Extrahované lokácie
- `technologies` (List[str], optional) - Extrahované technológie
- `concepts` (List[str], optional) - Extrahované koncepty/pojmy
- `analyzed_at` (str, optional) - Kedy bola NLP analýza vykonaná

### Category Metadata
- `category` (str, optional) - Hlavná kategória (`reflection`, `planning`, `technical`, atď.)
- `subcategory` (str, optional) - Podkategória (`emotional`, `tactical`, `strategic`, atď.)
- `context` (Dict, optional) - Kontextový objekt:
  - `projects` (List[str]) - Spomínané projekty
  - `people` (List[str]) - Spomínané osoby
  - `technologies` (List[str]) - Spomínané technológie
  - `emotions` (List[str]) - Identifikované emócie
- `categorized_at` (str, optional) - Kedy bola kategorizácia vykonaná

---

## 📝 Príklad Záznamu

```json
{
  "prompt_id": "2025-07-19_001",
  "date": "2025-07-19",
  "timestamp": "2025-07-19T02:19:19.998000+00:00",
  "word_count": 61,
  
  "activity": "Adam pracoval na surovom zápise pre projekt iShowSpeed...",
  "thoughts": "Rozmýšľal o tom, ako sa menia témy v jeho zápise...",
  "summary_extracted_at": "2025-12-03T15:23:35.257404",
  
  "sentiment": "negative",
  "sentiment_score": 0.4533628523349762,
  "people": ["Cibula"],
  "organizations": [],
  "locations": [],
  "technologies": ["zapisal"],
  "concepts": ["tem", "text", "surova", "cyklik", "odpoved", ...],
  "analyzed_at": "2025-12-03T19:09:21.831652",
  
  "category": "reflection",
  "subcategory": "emotional",
  "context": {
    "projects": [],
    "people": ["Cibula"],
    "technologies": ["zapisal"],
    "emotions": ["negative"]
  },
  "categorized_at": "2025-12-03T19:31:42.605648"
}
```

---

## 🚀 Použitie

### Načítanie všetkých záznamov

```python
import json
from pathlib import Path

prompts = []
with open('data/prompts/prompts_enriched.jsonl', 'r') as f:
    for line in f:
        data = json.loads(line)
        prompts.append(data)

print(f"Načítaných {len(prompts)} promptov")
```

### Filtrovanie podľa kategórie

```python
# Len reflection prompty
reflection = [p for p in prompts if p.get('category') == 'reflection']

# Len technical prompty
technical = [p for p in prompts if p.get('category') == 'technical']
```

### Filtrovanie podľa sentimentu

```python
# Len pozitívne prompty
positive = [p for p in prompts if p.get('sentiment') == 'positive']

# Len negatívne prompty s vysokým score
negative_strong = [
    p for p in prompts 
    if p.get('sentiment') == 'negative' 
    and p.get('sentiment_score', 0) > 0.7
]
```

### Vyhľadávanie podľa ľudí

```python
# Všetky prompty o Vlado
vlado_prompts = [
    p for p in prompts 
    if 'Vlado' in p.get('people', [])
]
```

### Vyhľadávanie podľa technológií

```python
# Všetky prompty o n8n
n8n_prompts = [
    p for p in prompts 
    if 'n8n' in p.get('technologies', [])
]
```

### Temporálne analýzy

```python
# Prompty podľa mesiacov
from collections import defaultdict

by_month = defaultdict(list)
for p in prompts:
    month = p['date'][:7]  # YYYY-MM
    by_month[month].append(p)

# Počet promptov za mesiac
for month, month_prompts in sorted(by_month.items()):
    print(f"{month}: {len(month_prompts)} promptov")
```

### Kombinované filtre

```python
# Pozitívne reflection prompty o AI
ai_reflection_positive = [
    p for p in prompts
    if p.get('category') == 'reflection'
    and p.get('sentiment') == 'positive'
    and ('ai' in p.get('concepts', []) or 'AI' in p.get('technologies', []))
]
```

---

## 📊 Štatistiky

**Aktuálny stav:**
- Celkom záznamov: 649
- Má activity: 649 (100%)
- Má NLP: 649 (100%)
- Má category: 647 (99.7%)

**Aktualizácia:**
- Spusti `scripts/merge_prompt_metadata.py` po každej aktualizácii zdrojových súborov

---

## 🔄 Workflow

1. **Extrakcia aktivít** → `prompts_activities.jsonl`
2. **NLP analýza** → `prompts_nlp4sk.jsonl`
3. **Kategorizácia** → `prompts_categorized.jsonl`
4. **Konsolidácia** → `prompts_enriched.jsonl` (tento súbor)

---

## 💡 Výhody Konsolidovanej Štruktúry

1. **Jeden zdroj pravdy** - Všetky metadáta na jednom mieste
2. **Jednoduchšie dotazy** - Nemusíš načítavať 3 súbory
3. **Lepšia performance** - Jeden súbor je rýchlejší ako 3
4. **Kompletnosť** - Všetky metadáta v jednom zázname
5. **Jednoduchšia údržba** - Jeden súbor na aktualizáciu

---

**Vytvorené:** 2025-12-03  
**Status:** ✅ Aktívne používané

