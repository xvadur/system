# ✅ RAG Query s Automatickou Syntézou

**Dátum:** 2025-12-XX  
**Status:** ✅ Funkčný  
**Problém vyriešený:** Namiesto surových promptov dostávaš syntetizovanú odpoveď

---

## 🎯 Čo sa Zmenilo?

**Predtým:**
- RAG vracal surové prompty
- Ty si musel prečítať všetky prompty
- Ja som len zobrazoval výsledky

**Teraz:**
- RAG vyhľadá relevantné prompty
- **Ja (agent) ich použijem v GPT-4 na syntézu odpovede**
- Ty dostaneš už spracovanú, syntetizovanú odpoveď s hlavnými informáciami

---

## 🚀 Ako to Funguje?

### Workflow:

```
1. TY: "urob mi chronológiu augusta"
   ↓
2. JA: Zavolám /rag/query (nie /rag/search)
   ↓
3. RAG: Vyhľadá relevantné prompty z augusta
   ↓
4. GPT-4: Syntetizuje odpoveď z týchto promptov
   ↓
5. TY: Dostaneš syntetizovanú chronológiu (nie surové prompty)
```

---

## 🔧 Nový Endpoint

### `/rag/query` (Syntetizovaná odpoveď)

**Request:**
```json
{
  "query": "urob mi chronológiu augusta",
  "top_k": 10,
  "min_score": 0.4,
  "model": "gpt-4o-mini"
}
```

**Response:**
```json
{
  "query": "urob mi chronológiu augusta",
  "synthesized_answer": "# Chronológia Augusta 2025\n\n## 2025-08-01\nZačal som pracovať na AI recepčnej...\n\n## 2025-08-05\nRiešil som problém s n8n workflow...\n\n...",
  "sources_count": 10,
  "sources": [
    {"date": "2025-08-01", "score": 0.85, "source_path": "..."},
    ...
  ],
  "model_used": "gpt-4o-mini"
}
```

---

## 📊 Porovnanie: `/rag/search` vs `/rag/query`

| Aspekt | `/rag/search` | `/rag/query` |
|--------|----------------|--------------|
| **Výstup** | Surové prompty | Syntetizovaná odpoveď |
| **Musíš čítať** | Áno (všetky prompty) | Nie (už spracované) |
| **Formát** | JSON s výsledkami | Syntetizovaný text |
| **Použitie** | Keď chceš surové dáta | Keď chceš odpoveď |

---

## 💡 Príklady Použitia

### Príklad 1: Chronológia Augusta

**TY:** "urob mi chronológiu augusta"

**JA (s `/rag/query`):**
> Na základe RAG vyhľadávania som našiel 10 relevantných promptov z augusta. Tu je syntetizovaná chronológia:
> 
> # Chronológia Augusta 2025
> 
> ## 2025-08-01
> Začal som pracovať na AI recepčnej. Hlavná téma bola integrácia s n8n a automatizácia procesov.
> 
> ## 2025-08-05
> Riešil som problém s n8n workflow. Identifikoval som, že problém bol v konfigurácii GitHub credentials.
> 
> ## 2025-08-15
> Dokončil som prvú verziu AI recepčnej. Testoval som ju s reálnymi dátami a fungovala dobre.
> 
> ...
> 
> *Zdroj: 10 promptov z augusta 2025*

**Výhoda:** Ty dostaneš už spracovanú chronológiu, nie surové prompty.

---

### Príklad 2: Analýza Témy

**TY:** "čo som hovoril o svojej transformácii identity?"

**JA (s `/rag/query`):**
> Na základe RAG vyhľadávania som našiel 8 relevantných promptov o tvojej transformácii identity. Tu je syntetizovaná analýza:
> 
> # Transformácia Identity: Sanitár → AI Developer
> 
> Tvoja transformácia identity prebiehala v niekoľkých fázach:
> 
> **Fáza 1: Post-hospital Reset (Apríl–Jún 2025)**
> Po odchode z nemocnice si sa rozhodol odísť zo zdravotníctva. Hlavný dôvod bol fyzická zraniteľnosť a potreba zmeny.
> 
> **Fáza 2: Legitimizačný Bod (Jún 2025)**
> Stretnutie s Petrom Utekalom v Skyparku bolo kľúčové. Videl si v ňom "budúce ja" a získal si validáciu pre svoju transformáciu.
> 
> **Fáza 3: On-boarding & Frikcia (Júl 2025)**
> Nástup do AI Apply priniesol nové výzvy. Učil si sa Retool, n8n, a zároveň si riešil vnútorné konflikty o svojej kompetencii.
> 
> ...
> 
> *Zdroj: 8 promptov z júla–septembra 2025*

**Výhoda:** Ty dostaneš syntetizovanú analýzu, nie surové prompty.

---

## 🔧 Technické Detaily

### Funkcia: `query_rag_with_synthesis()`

**Lokácia:** `xvadur_brave/scripts/rag_agent_helper.py`

**Čo robí:**
1. Zavolá `search_rag()` - nájde relevantné prompty
2. Zostaví kontext z výsledkov
3. Použije GPT-4 na syntézu odpovede
4. Vráti syntetizovanú odpoveď

**Parametre:**
- `query`: Vyhľadávací dotaz
- `top_k`: Počet výsledkov (default: 10)
- `min_score`: Minimálne similarity score (default: 0.4)
- `model`: OpenAI model (default: "gpt-4o-mini")
- `temperature`: Temperature pre LLM (default: 0.3)

---

## 📝 Ako Používať v Konverzácii

### Automatické Použitie (Odporúčané)

**Stačí sa pýtať prirodzene:**
```
"urob mi chronológiu augusta"
"čo som hovoril o svojej transformácii identity?"
"ako som riešil n8n problémy?"
```

**Ja (agent) automaticky:**
1. Rozpoznám, že potrebuješ syntetizovanú odpoveď
2. Zavolám `/rag/query` (nie `/rag/search`)
3. Syntetizujem odpoveď z relevantných promptov
4. Dám ti už spracovanú odpoveď

---

## ⚙️ Konfigurácia

### Model Výber

- **`gpt-4o-mini`** (default): Rýchlejší, lacnejší, dobrá kvalita
- **`gpt-4o`**: Lepšia kvalita, pomalší, drahší

### Top K Výber

- **5-10**: Pre konkrétne otázky
- **10-20**: Pre komplexnejšie analýzy
- **20+**: Pre chronológie a prehľady

---

## 🎯 Výhody

1. **Syntetizovaná odpoveď** - Nie surové prompty
2. **Hlavné informácie** - Už spracované a zhrnuté
3. **Čitateľnosť** - Formátovaná a zmysluplná odpoveď
4. **Automatizácia** - Ja to spracujem za teba

---

## ⚠️ Poznámky

- **Náklady:** Každá syntéza používa GPT-4 API (malé náklady)
- **Latencia:** Syntéza trvá o niečo dlhšie ako len search (cca +2-3 sekundy)
- **Kvalita:** Závisí od kvality RAG výsledkov a GPT-4 modelu

---

**Status:** ✅ Funkčný a pripravený na použitie!

