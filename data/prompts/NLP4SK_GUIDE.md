# 📖 Návod na Analýzu Promptov pomocou Lokálnych NLP Nástrojov

**Skript:** `scripts/analyze_prompts_nlp4sk.py`  
**Výstup:** `data/prompts/prompts_nlp4sk.jsonl`

**⚠️ DÔLEŽITÉ:** Tento skript teraz používa **lokálne NLP nástroje** (Stanza, Hugging Face) namiesto NLP4SK API.  
**Pozri:** [LOCAL_NLP_GUIDE.md](LOCAL_NLP_GUIDE.md) pre kompletný návod.

---

## 🚀 Rýchly Štart

### 1. Inštalácia Závislostí

Nainštaluj potrebné Python balíky:

```bash
pip install stanza transformers torch
```

### 2. Stiahnutie Stanza Modelu

Prvé spustenie skriptu automaticky stiahne slovenský model, ale môžeš ho stiahnuť manuálne:

```bash
python3 -c "import stanza; stanza.download('sk')"
```

**Poznámka:** Skript už **nevyžaduje NLP4SK API key** - všetko funguje lokálne!

### 3. Test Mode (Odporúčané na začiatok)

V `scripts/analyze_prompts_nlp4sk.py` nastav:
```python
TEST_MODE = True
TEST_LIMIT = 20
```

Spusti:
```bash
python3 scripts/analyze_prompts_nlp4sk.py
```

Toto spracuje len prvých 20 promptov pre testovanie.

### 4. Plné Spracovanie

V `scripts/analyze_prompts_nlp4sk.py` nastav:
```python
TEST_MODE = False
```

Spusti:
```bash
python3 scripts/analyze_prompts_nlp4sk.py
```

---

## 📊 Čo Skript Robí

1. **Načíta prompty:**
   - Z `data/prompts/prompts_activities.jsonl` (650 aktivít)

2. **Analyzuje pomocou NLP4SK API:**
   - **Sentiment analýza:** Pozitívny/negatívny/neutrálny sentiment
   - **Extrakcia entít (NER):** People, organizations, locations, technologies
   - **Extrakcia pojmov:** Kľúčové koncepty z textu

3. **Ukladá:**
   - Do `data/prompts/prompts_nlp4sk.jsonl`
   - Resume functionality - ak skript spadne, môže pokračovať

---

## 📁 Formát Výstupu

**Súbor:** `data/prompts/prompts_nlp4sk.jsonl`

```json
{
  "prompt_id": "2025-09-15_001",
  "date": "2025-09-15",
  "timestamp": "2025-09-15T13:18:41.861000+00:00",
  "word_count": 738,
  "sentiment": "positive",
  "sentiment_score": 0.75,
  "people": ["Vlado", "Petr"],
  "organizations": ["OpenAI"],
  "locations": [],
  "technologies": ["n8n", "Chainlit", "MCP"],
  "concepts": ["AI projekt", "automatizácia", "workflow"],
  "analyzed_at": "2025-12-03T16:00:00+01:00"
}
```

---

## 🔍 Použité NLP Nástroje

Skript používa tieto lokálne NLP nástroje:

1. **Analýza sentimentu:**
   - **Nástroj:** Hugging Face Transformers (`cardiffnlp/twitter-xlm-roberta-base-sentiment`)
   - **Výstup:** `sentiment` (positive/negative/neutral), `sentiment_score` (0.0-1.0)

2. **Extrakcia entít (NER):**
   - **Nástroj:** Stanza NER (slovenský model)
   - **Výstup:** `people`, `organizations`, `locations`, `technologies`

3. **Extrakcia pojmov:**
   - **Nástroj:** Stanza (noun phrases a významné slová)
   - **Výstup:** `concepts` (zoznam kľúčových pojmov)

---

## ⚙️ Konfigurácia

V `scripts/analyze_prompts_nlp4sk.py`:

```python
BATCH_SIZE = 10           # Progress update každých N promptov
TEST_MODE = False         # Test mode (len prvých N promptov)
TEST_LIMIT = 20           # Počet promptov v test mode
```

---

## 🔄 Resume Functionality

Ak skript spadne alebo ho prerušíš:
- Skript automaticky načíta už spracované prompty z output súboru
- Preskočí ich a pokračuje len s novými
- Môžeš ho spustiť znova bez obáv o duplikáty

---

## 💰 Náklady

- **NLP4SK API:** Pravdepodobne zdarma alebo veľmi lacné (závisí od poskytovateľa)
- **Čas:** ~10-15 minút pre 650 promptov (s rate limiting 1.1s medzi requestmi)

---

## 🐛 Troubleshooting

### Chyba: "ModuleNotFoundError: No module named 'stanza'"
```bash
pip install stanza transformers torch
```

### Chyba: "Chyba pri inicializácii Stanza"
```bash
# Stiahni slovenský model manuálne
python3 -c "import stanza; stanza.download('sk')"
```

### Chyba: "Out of memory"
- Transformers modely môžu byť pamäťovo náročné
- Skús spracovať menej promptov naraz (TEST_MODE)
- Alebo použij GPU (ak máš)

**Pozri:** [LOCAL_NLP_GUIDE.md](LOCAL_NLP_GUIDE.md) pre viac troubleshooting tipov.

---

## 📝 Príklady Použitia

### Načítať analýzy pre mesiac:
```python
import json
from pathlib import Path

analyses = []
with open('data/prompts/prompts_nlp4sk.jsonl', 'r') as f:
    for line in f:
        data = json.loads(line)
        if data['date'].startswith('2025-09'):
            analyses.append(data)

for analysis in analyses:
    print(f"{analysis['date']}: sentiment={analysis.get('sentiment')}, people={analysis.get('people')}")
```

### Vyhľadať podľa sentimentu:
```python
# Nájsť všetky negatívne prompty
negative = [a for a in analyses if a.get('sentiment') == 'negative']
```

### Vyhľadať podľa technológií:
```python
# Nájsť všetky prompty o n8n
n8n_prompts = [a for a in analyses if 'n8n' in a.get('technologies', [])]
```

### Vyhľadať podľa ľudí:
```python
# Nájsť všetky prompty o Vlado
vlado_prompts = [a for a in analyses if 'Vlado' in a.get('people', [])]
```

---

## 🔗 Migrácia z NLP4SK API

Skript bol **upravený** na použitie lokálnych NLP nástrojov namiesto NLP4SK API:

- ✅ **Odstránené:** NLP4SK API volania, API key požiadavky
- ✅ **Pridané:** Stanza pre NER, Hugging Face pre sentiment
- ✅ **Zachované:** Rovnaký výstupný formát, resume functionality

**Výhody:**
- Bez API kľúča
- Offline spracovanie
- Zdarma
- Súkromné (dáta zostávajú lokálne)

**Pozri:** [LOCAL_NLP_GUIDE.md](LOCAL_NLP_GUIDE.md) pre kompletný návod.

---

**Vytvorené:** 2025-12-03  
**Aktualizované:** 2025-12-03 (migrácia na lokálne NLP nástroje)  
**Status:** ✅ Pripravené na použitie

