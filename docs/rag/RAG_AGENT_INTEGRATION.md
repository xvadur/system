# 🧠 RAG Agent Integration: Ako používať RAG v Cursor agentovi

## 📋 Prehľad

RAG systém je teraz integrovaný do Cursor agenta. Keď potrebuješ kontext z minulosti alebo relevantné prompty, môžem automaticky vyhľadať v RAG indexe.

---

## 🔧 Technické Detaily

### Skript: `rag_agent_helper.py`

**Lokalizácia:** `xvadur_brave/scripts/rag_agent_helper.py`

**Použitie:**
```bash
source temp_pdf_env/bin/activate
python3 xvadur_brave/scripts/rag_agent_helper.py "query" [top_k] [min_score]
```

**Výstup:** JSON s výsledkami vyhľadávania

**Príklad:**
```bash
python3 xvadur_brave/scripts/rag_agent_helper.py "transformácia identity" 5 0.4
```

**Výstup formát:**
```json
{
  "query": "transformácia identity",
  "results_count": 3,
  "results": [
    {
      "rank": 1,
      "score": 0.48,
      "text": "...",
      "date": "2025-07-20",
      "timestamp": "2025-07-20T01:13:51.386000+00:00",
      "source_path": "data/chronology/2025-07-20.md"
    }
  ]
}
```

---

## 🎯 Kedy použiť RAG Search

### Automaticky použiť RAG, keď:

1. **Otázky o minulosti:**
   - "Čo som hovoril o X?"
   - "Ako som riešil Y?"
   - "Kedy som sa zmieňoval o Z?"

2. **Otázky o identite:**
   - "Ako som sa transformoval?"
   - "Čo som hovoril o svojej identite?"
   - "Kde som sa zmieňoval ako Adam?"

3. **Potreba kontextu:**
   - Keď užívateľ spomína niečo z minulosti
   - Keď potrebujem pochopiť súvislosti
   - Keď chcem nájsť relevantné prompty

4. **Temporálne otázky:**
   - "Čo sa stalo v júli 2025?"
   - "Ako som sa zmenil medzi X a Y?"

### NEPOUŽIŤ RAG, keď:

- Otázka je čisto technická (ako niečo urobiť)
- Otázka je o budúcnosti (plány, vízie)
- Otázka nevyžaduje kontext z minulosti

---

## 💻 Ako to používať v Cursor agentovi

### Krok 1: Identifikuj, či potrebuješ RAG

Keď užívateľ povie niečo ako:
- "Čo som hovoril o..."
- "Ako som riešil..."
- "Kde som sa zmieňoval o..."

### Krok 2: Zavolaj RAG search

```bash
cd "/Users/_xvadur/Desktop/Magnum Opus" && source temp_pdf_env/bin/activate && python3 xvadur_brave/scripts/rag_agent_helper.py "query" 5 0.4
```

### Krok 3: Parsuj JSON výsledky

Výsledky obsahujú:
- `text` - obsah promptu
- `date` - dátum
- `score` - similarity score (0-1)
- `source_path` - zdroj súboru

### Krok 4: Použi výsledky v odpovedi

Citovať relevantné prompty a poskytnúť kontext z minulosti.

---

## 📊 Príklady Použitia

### Príklad 1: Otázka o identite

**Užívateľ:** "Čo som hovoril o svojej transformácii identity?"

**Agent akcia:**
```bash
python3 xvadur_brave/scripts/rag_agent_helper.py "transformácia identity" 5 0.4
```

**Výsledok:** Nájde relevantné prompty o transformácii identity z júla-septembra 2025.

### Príklad 2: Otázka o minulosti

**Užívateľ:** "Ako som riešil n8n problémy?"

**Agent akcia:**
```bash
python3 xvadur_brave/scripts/rag_agent_helper.py "riešenie n8n problémov" 5 0.4
```

**Výsledok:** Nájde relevantné prompty o riešení n8n problémov.

### Príklad 3: Temporálna otázka

**Užívateľ:** "Čo sa stalo v júli 2025?"

**Agent akcia:**
```bash
python3 xvadur_brave/scripts/rag_agent_helper.py "júl 2025 udalosti" 10 0.3
```

**Výsledok:** Nájde relevantné prompty z júla 2025.

---

## ⚙️ Parametre

### `query` (povinný)
Vyhľadávací dotaz - čo hľadáš v promptoch.

### `top_k` (voliteľný, default: 5)
Počet výsledkov, ktoré chceš dostať (1-50).

### `min_score` (voliteľný, default: 0.4)
Minimálne similarity score (0-1). Nižšie = viac výsledkov, ale menej relevantné.

**Odporúčania:**
- `min_score: 0.5` - len vysoko relevantné výsledky
- `min_score: 0.4` - vyvážené (odporúčané)
- `min_score: 0.3` - viac výsledkov, menej relevantné

---

## 🔄 Workflow

```
Užívateľ otázka
    ↓
Potrebujem kontext z minulosti?
    ↓ ÁNO
Zavolaj RAG search
    ↓
Parsuj JSON výsledky
    ↓
Použi výsledky v odpovedi
    ↓
Citovať relevantné prompty
```

---

## 📝 Poznámky

- **Virtual Environment:** Vždy aktivuj `temp_pdf_env` pred použitím
- **API Key:** Automaticky načítaný z `.env` súboru
- **Performance:** RAG search trvá ~1-2 sekundy
- **Limit:** Max 50 výsledkov na query

---

## 🚀 Ďalšie Vylepšenia (Budúcnosť)

1. **Automatická detekcia:** Agent automaticky rozpozná, kedy použiť RAG
2. **Caching:** Uloženie výsledkov pre rýchlejšie opakované otázky
3. **Hybrid search:** Kombinácia semantic + keyword search
4. **Temporálne filtrovanie:** Vyhľadávanie len v určitom časovom období

---

**Dátum vytvorenia:** 2025-12-XX  
**Status:** ✅ Funkčný  
**Integrácia:** Cursor Agent (Aethero)

