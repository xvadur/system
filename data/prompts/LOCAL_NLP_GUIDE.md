# 📖 Návod na Lokálnu NLP Analýzu Promptov

**Skript:** `scripts/analyze_prompts_nlp4sk.py`  
**Výstup:** `data/prompts/prompts_nlp4sk.jsonl`

**Nástroje:** Stanza, Hugging Face Transformers

---

## 🚀 Rýchly Štart

### 1. Inštalácia Závislostí

Nainštaluj potrebné Python balíky:

```bash
pip install stanza transformers torch
```

**Poznámka:** PyTorch môže byť veľký (~2GB). Ak máš GPU, nainštaluj `torch` s CUDA podporou.

### 2. Stiahnutie Stanza Modelu

Prvé spustenie skriptu automaticky stiahne slovenský model (~500MB), ale môžeš ho stiahnuť manuálne:

```bash
python3 -c "import stanza; stanza.download('sk')"
```

**Čas:** ~2-5 minút (závisí od rýchlosti internetu)

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

2. **Analyzuje pomocou lokálnych NLP nástrojov:**
   - **Sentiment analýza:** Hugging Face transformers (multilingual model)
   - **Extrakcia entít (NER):** Stanza NER (people, organizations, locations, technologies)
   - **Extrakcia pojmov:** Stanza (noun phrases a významné slová)

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
  "sentiment_score": 0.85,
  "people": ["Vlado", "Petr"],
  "organizations": ["OpenAI"],
  "locations": [],
  "technologies": ["n8n", "Chainlit", "MCP"],
  "concepts": ["projekt", "automatizácia", "workflow"],
  "analyzed_at": "2025-12-03T16:00:00+01:00"
}
```

---

## 🔧 Použité Nástroje

### Stanza

- **Účel:** NER (Named Entity Recognition), tokenizácia, lematizácia, POS tagging
- **Model:** Slovenský model (`sk`)
- **Veľkosť:** ~500MB
- **Prvé spustenie:** Automaticky stiahne model

**Funkcie:**
- Extrakcia entít (people, organizations, locations)
- Identifikácia technológií (podľa kľúčových slov)
- Extrakcia pojmov (podstatné mená a vlastné mená)

### Hugging Face Transformers

- **Účel:** Sentiment analýza
- **Model:** `cardiffnlp/twitter-xlm-roberta-base-sentiment` (multilingual)
- **Veľkosť:** ~500MB
- **Prvé spustenie:** Automaticky stiahne model

**Funkcie:**
- Analýza sentimentu (positive, negative, neutral)
- Sentiment score (0.0-1.0)

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

## 💰 Náklady a Performance

### Náklady
- **Zdarma:** Žiadne API náklady
- **Disk:** ~1-2 GB (modely)
- **RAM:** ~2-4 GB počas spracovania

### Performance
- **Prvé spustenie:** ~5-10 minút (stiahnutie modelov)
- **Čas spracovania:** ~15-20 minút pre 650 promptov (CPU)
- **S GPU:** ~5-10 minút pre 650 promptov

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

### Chyba: "Model not found"
- Prvé spustenie automaticky stiahne modely
- Ak zlyhá, stiahni manuálne:
  ```bash
  python3 -c "import stanza; stanza.download('sk')"
  ```

### Pomalé spracovanie
- Normálne pre CPU (15-20 min pre 650 promptov)
- Ak máš GPU, môžeš upraviť `device=-1` na `device=0` v `init_sentiment_pipeline()`

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

## 🔗 Porovnanie s NLP4SK API

| Vlastnosť | Lokálne NLP | NLP4SK API |
|-----------|-------------|------------|
| **Náklady** | Zdarma | ? (vyžaduje API key) |
| **Offline** | ✅ Áno | ❌ Nie |
| **API Key** | ❌ Nie | ✅ Áno |
| **Sentiment** | ✅ Multilingual model | ✅ Špecializované |
| **Extrakcia entít** | ✅ Stanza NER | ✅ Špecializované |
| **Presnosť** | Dobrá | Pravdepodobne lepšia |
| **Rýchlosť** | Stredná (CPU) | Rýchla (API) |

**Odporúčanie:** Použi lokálne NLP, ak nemáš NLP4SK API key alebo chceš offline spracovanie.

---

## 📚 Ďalšie Zdroje

- **Stanza:** https://stanfordnlp.github.io/stanza/
- **Hugging Face:** https://huggingface.co/
- **Transformers:** https://huggingface.co/docs/transformers/

---

**Vytvorené:** 2025-12-03  
**Status:** ✅ Pripravené na použitie

