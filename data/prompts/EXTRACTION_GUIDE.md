# 📖 Návod na Extrakciu Aktivit z Promptov

**Skript:** `scripts/extract_prompt_activities.py`  
**Výstup:** `data/prompts/prompts_activities.jsonl`

---

## 🚀 Rýchly Štart

### 1. Nastavenie API Key

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

### 2. Test Mode (Odporúčané na začiatok)

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

### 3. Plné Spracovanie

V `scripts/extract_prompt_activities.py` nastav:
```python
TEST_MODE = False
```

Spusti:
```bash
python3 scripts/extract_prompt_activities.py
```

---

## 📊 Čo Skript Robí

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

---

## 📁 Formát Výstupu

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

---

## ⚙️ Konfigurácia

V `scripts/extract_prompt_activities.py`:

```python
MAX_WORDS = 1000          # Limit pre spracovanie
BATCH_SIZE = 10           # Progress update každých N promptov
MODEL = "gpt-4o-mini"     # OpenAI model (gpt-4o-mini alebo gpt-4o)
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

## 📈 Odhadované Náklady

- **Počet promptov:** ~606 promptov < 1000 slov
- **Model:** gpt-4o-mini (~$0.15 per 1M input tokens, ~$0.60 per 1M output tokens)
- **Odhadované náklady:** $2-5 pre všetky prompty
- **Čas:** ~10-15 minút (s rate limiting 1.1s medzi requestmi)

---

## 🐛 Troubleshooting

### Chyba: "OPENAI_API_KEY nie je nastavený"
```bash
export OPENAI_API_KEY='sk-...'
```

### Chyba: "Rate limit exceeded"
- Skript automaticky čaká medzi requestmi (1.1s)
- Ak stále zlyhá, zvýš čas medzi requestmi v kóde

### Chyba: "JSON decode error"
- Skript má fallback parsing pre textové odpovede
- Chyby sa logujú do `data/prompts/extraction_errors.log`

---

## 📝 Príklady Použitia

### Načítať aktivity pre mesiac:
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

### Vyhľadať podľa aktivity:
```python
# Nájsť všetky prompty o AI
ai_activities = [a for a in activities if 'ai' in a['activity'].lower()]
```

---

**Vytvorené:** 2025-12-03  
**Status:** ✅ Pripravené na použitie

