# 📖 Kompletný Návod na Analýzu Promptov

**Účel:** Návod na extrakciu aktivít a NLP analýzu promptov  
**Skripty:** 
- `scripts/extract_prompt_activities.py` - Extrakcia aktivít
- `scripts/analyze_prompts_nlp4sk.py` - NLP analýza

---

## 📋 Obsah

1. [Extrakcia Aktivít z Promptov](#extrakcia-aktivit)
2. [Lokálna NLP Analýza](#lokálna-nlp-analýza)
3. [Príklady Použitia](#príklady-použitia)

---

## 🔍 Extrakcia Aktivít

**Skript:** `scripts/extract_prompt_activities.py`  
**Výstup:** `data/prompts/prompts_activities.jsonl`

### Rýchly Štart

#### 1. Nastavenie API Key

**Odporúčané:** Vytvor `.env` súbor v root adresári workspace:

```bash
# Skopíruj template
cp .env.example .env

# Uprav .env a nahraď 'sk-...' svojím skutočným API kľúčom
# Získaj ho z: https://platform.openai.com/api-keys
```

Alebo nastav environment variable (dočasné):
```bash
export OPENAI_API_KEY='sk-...'
```

**Poznámka:** `.env` súbor je už v `.gitignore`, takže sa necommitne do gitu.

#### 2. Test Mode (Odporúčané na začiatok)

V `scripts/extract_prompt_activities.py` nastav:
```python
TEST_MODE = True
TEST_LIMIT = 20
```

Spusti:
```bash
python3 scripts/extract_prompt_activities.py
```

Toto spracuje len prvých 20 promptov pre testovanie.

#### 3. Plné Spracovanie

V `scripts/extract_prompt_activities.py` nastav:
```python
TEST_MODE = False
```

Spusti:
```bash
python3 scripts/extract_prompt_activities.py
```

### Čo Skript Robí

1. **Načíta prompty:**
   - Historické: `data/prompts/prompts_split/` (664 promptov)
   - Aktuálne: `xvadur/data/prompts_log.jsonl` (44 promptov)

2. **Filtruje:**
   - Preskočí prompty >= 1000 slov (dlhé prompty)
   - Zostáva ~606 promptov < 1000 slov

3. **Extrahuje:**
   - Pre každý prompt zavolá OpenAI API
   - Extrahuje: aktivitu (čo robil) + myšlienky (nad čím rozmýšľal)

4. **Ukladá:**
   - Do `data/prompts/prompts_activities.jsonl`
   - Resume functionality - ak skript spadne, môže pokračovať

### Formát Výstupu

**Súbor:** `data/prompts/prompts_activities.jsonl`

```json
{
  "prompt_id": "2025-09-15_001",
  "date": "2025-09-15",
  "timestamp": "2025-09-15T13:18:41.861000+00:00",
  "word_count": 738,
  "activity": "Písal filozofickú úvahu o histórii ľudstva, kresťanstve a Jungovi",
  "thoughts": "Rozmýšľal o princípoch civilizácií, manipulácii mas, kresťanstve a jeho interpretácii, Jungovej dekonštrukcii boha",
  "summary_extracted_at": "2025-12-03T16:00:00+01:00"
}
```

### Konfigurácia

V `scripts/extract_prompt_activities.py`:

```python
MAX_WORDS = 1000          # Limit pre spracovanie
BATCH_SIZE = 10           # Progress update každých N promptov
MODEL = "gpt-4o-mini"     # OpenAI model (gpt-4o-mini alebo gpt-4o)
TEST_MODE = False         # Test mode (len prvých N promptov)
TEST_LIMIT = 20           # Počet promptov v test mode
```

### Resume Functionality

Ak skript spadne alebo ho prerušíš:
- Skript automaticky načíta už spracované prompty z output súboru
- Preskočí ich a pokračuje len s novými
- Môžeš ho spustiť znova bez obáv o duplikáty

### Odhadované Náklady

- **Počet promptov:** ~606 promptov < 1000 slov
- **Model:** gpt-4o-mini (~$0.15 per 1M input tokens, ~$0.60 per 1M output tokens)
- **Odhadované náklady:** $2-5 pre všetky prompty
- **Čas:** ~10-15 minút (s rate limiting 1.1s medzi requestmi)

### Troubleshooting (Extrakcia)

**Chyba: "OPENAI_API_KEY nie je nastavený"**
```bash
export OPENAI_API_KEY='sk-...'
```

**Chyba: "Rate limit exceeded"**
- Skript automaticky čaká medzi requestmi (1.1s)
- Ak stále zlyhá, zvýš čas medzi requestmi v kóde

**Chyba: "JSON decode error"**
- Skript má fallback parsing pre textové odpovede
- Chyby sa logujú do `data/prompts/extraction_errors.log`

---

## 🧠 Lokálna NLP Analýza

**Skript:** `scripts/analyze_prompts_nlp4sk.py`  
**Výstup:** `data/prompts/prompts_nlp4sk.jsonl`  
**Nástroje:** Stanza, Hugging Face Transformers

### Rýchly Štart

#### 1. Inštalácia Závislostí

Nainštaluj potrebné Python balíky:

```bash
pip install stanza transformers torch
```

**Poznámka:** PyTorch môže byť veľký (~2GB). Ak máš GPU, nainštaluj `torch` s CUDA podporou.

#### 2. Stiahnutie Stanza Modelu

Prvé spustenie skriptu automaticky stiahne slovenský model (~500MB), ale môžeš ho stiahnuť manuálne:

```bash
python3 -c "import stanza; stanza.download('sk')"
```

**Čas:** ~2-5 minút (závisí od rýchlosti internetu)

#### 3. Test Mode (Odporúčané na začiatok)

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

#### 4. Plné Spracovanie

V `scripts/analyze_prompts_nlp4sk.py` nastav:
```python
TEST_MODE = False
```

Spusti:
```bash
python3 scripts/analyze_prompts_nlp4sk.py
```

### Čo Skript Robí

1. **Načíta prompty:**
   - Z `data/prompts/prompts_activities.jsonl` (650 aktivít)

2. **Analyzuje pomocou lokálnych NLP nástrojov:**
   - **Sentiment analýza:** Hugging Face transformers (multilingual model)
   - **Extrakcia entít (NER):** Stanza NER (people, organizations, locations, technologies)
   - **Extrakcia pojmov:** Stanza (noun phrases a významné slová)

3. **Ukladá:**
   - Do `data/prompts/prompts_nlp4sk.jsonl`
   - Resume functionality - ak skript spadne, môže pokračovať

### Formát Výstupu

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

### Použité Nástroje

#### Stanza

- **Účel:** NER (Named Entity Recognition), tokenizácia, lematizácia, POS tagging
- **Model:** Slovenský model (`sk`)
- **Veľkosť:** ~500MB
- **Prvé spustenie:** Automaticky stiahne model

**Funkcie:**
- Extrakcia entít (people, organizations, locations)
- Identifikácia technológií (podľa kľúčových slov)
- Extrakcia pojmov (podstatné mená a vlastné mená)

#### Hugging Face Transformers

- **Účel:** Sentiment analýza
- **Model:** `cardiffnlp/twitter-xlm-roberta-base-sentiment` (multilingual)
- **Veľkosť:** ~500MB
- **Prvé spustenie:** Automaticky stiahne model

**Funkcie:**
- Analýza sentimentu (positive, negative, neutral)
- Sentiment score (0.0-1.0)

### Konfigurácia

V `scripts/analyze_prompts_nlp4sk.py`:

```python
BATCH_SIZE = 10           # Progress update každých N promptov
TEST_MODE = False         # Test mode (len prvých N promptov)
TEST_LIMIT = 20           # Počet promptov v test mode
```

### Resume Functionality

Ak skript spadne alebo ho prerušíš:
- Skript automaticky načíta už spracované prompty z output súboru
- Preskočí ich a pokračuje len s novými
- Môžeš ho spustiť znova bez obáv o duplikáty

### Náklady a Performance

#### Náklady
- **Zdarma:** Žiadne API náklady
- **Disk:** ~1-2 GB (modely)
- **RAM:** ~2-4 GB počas spracovania

#### Performance
- **Prvé spustenie:** ~5-10 minút (stiahnutie modelov)
- **Čas spracovania:** ~15-20 minút pre 650 promptov (CPU)
- **S GPU:** ~5-10 minút pre 650 promptov

### Troubleshooting (NLP Analýza)

**Chyba: "ModuleNotFoundError: No module named 'stanza'"**
```bash
pip install stanza transformers torch
```

**Chyba: "Chyba pri inicializácii Stanza"**
```bash
# Stiahni slovenský model manuálne
python3 -c "import stanza; stanza.download('sk')"
```

**Chyba: "Out of memory"**
- Transformers modely môžu byť pamäťovo náročné
- Skús spracovať menej promptov naraz (TEST_MODE)
- Alebo použij GPU (ak máš)

**Chyba: "Model not found"**
- Prvé spustenie automaticky stiahne modely
- Ak zlyhá, stiahni manuálne:
  ```bash
  python3 -c "import stanza; stanza.download('sk')"
  ```

**Pomalé spracovanie**
- Normálne pre CPU (15-20 min pre 650 promptov)
- Ak máš GPU, môžeš upraviť `device=-1` na `device=0` v `init_sentiment_pipeline()`

---

## 📝 Príklady Použitia

### Extrakcia Aktivít

#### Načítať aktivity pre mesiac:
```python
import json
from pathlib import Path

activities = []
with open('data/prompts/prompts_activities.jsonl', 'r') as f:
    for line in f:
        data = json.loads(line)
        if data['date'].startswith('2025-09'):
            activities.append(data)

for act in activities:
    print(f"{act['date']}: {act['activity']}")
```

#### Vyhľadať podľa aktivity:
```python
# Nájsť všetky prompty o AI
ai_activities = [a for a in activities if 'ai' in a['activity'].lower()]
```

### NLP Analýza

#### Načítať analýzy pre mesiac:
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

#### Vyhľadať podľa sentimentu:
```python
# Nájsť všetky negatívne prompty
negative = [a for a in analyses if a.get('sentiment') == 'negative']
```

#### Vyhľadať podľa technológií:
```python
# Nájsť všetky prompty o n8n
n8n_prompts = [a for a in analyses if 'n8n' in a.get('technologies', [])]
```

#### Vyhľadať podľa ľudí:
```python
# Nájsť všetky prompty o Vlado
vlado_prompts = [a for a in analyses if 'Vlado' in a.get('people', [])]
```

### Kombinovaná Analýza

#### Spojiť aktivity s NLP analýzou:
```python
import json

# Načítať aktivity
activities = {}
with open('data/prompts/prompts_activities.jsonl', 'r') as f:
    for line in f:
        data = json.loads(line)
        activities[data['prompt_id']] = data

# Načítať NLP analýzy
analyses = {}
with open('data/prompts/prompts_nlp4sk.jsonl', 'r') as f:
    for line in f:
        data = json.loads(line)
        analyses[data['prompt_id']] = data

# Spojiť dáta
for prompt_id in activities:
    if prompt_id in analyses:
        activity = activities[prompt_id]
        analysis = analyses[prompt_id]
        print(f"{activity['date']}: {activity['activity']} | Sentiment: {analysis.get('sentiment')}")
```

---

## 🔗 Workflow

**Odporúčaný postup:**

1. **Krok 1:** Extrahuj aktivity z promptov
   ```bash
   python3 scripts/extract_prompt_activities.py
   ```
   Výstup: `data/prompts/prompts_activities.jsonl`

2. **Krok 2:** Spusti NLP analýzu na extrahovaných aktivitách
   ```bash
   python3 scripts/analyze_prompts_nlp4sk.py
   ```
   Výstup: `data/prompts/prompts_nlp4sk.jsonl`

3. **Krok 3:** Použi dáta pre analýzy, vizualizácie, alebo ďalšie spracovanie

---

## 📚 Ďalšie Zdroje

- **Stanza:** https://stanfordnlp.github.io/stanza/
- **Hugging Face:** https://huggingface.co/
- **Transformers:** https://huggingface.co/docs/transformers/
- **OpenAI API:** https://platform.openai.com/api-keys

---

**Vytvorené:** 2025-12-03  
**Status:** ✅ Pripravené na použitie

