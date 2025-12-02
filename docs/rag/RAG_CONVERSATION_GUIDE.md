# 🧠 RAG Konverzácia: Kompletný Návod

## 📋 Prehľad

RAG systém je teraz **plne integrovaný** do konverzácie. Môžeš s ním viesť prirodzenú konverzáciu - stačí sa pýtať na minulosť, identitu, alebo akýkoľvek kontext z tvojich 664 promptov.

---

## 🎯 Ako to Funguje?

### Automatické Použitie

Keď sa pýtaš na niečo z minulosti, automaticky vyhľadám v RAG indexe:

**Príklady otázok, ktoré spustia RAG:**
- "Čo som hovoril o X?"
- "Ako som riešil Y?"
- "Kde som sa zmieňoval o Z?"
- "Ako som sa transformoval?"
- "Čo sa stalo v júli 2025?"

**Ja (agent) automaticky:**
1. Rozpoznám, že potrebuješ kontext z minulosti
2. Zavolám RAG search (`/rag/search` endpoint)
3. Nájdem relevantné prompty z tvojich dát
4. Použijem ich v odpovedi s citáciami

---

## 💬 Príklady Konverzácie

### Príklad 1: Otázka o Identite

**Ty:** "Čo som hovoril o svojej transformácii identity?"

**Ja (s RAG):**
> Na základe RAG vyhľadávania som našiel relevantné prompty o tvojej transformácii identity:
> 
> **Z 2025-07-20:**
> > "Transformácia identity nie je len zmena práce, ale zmena celého systému myslenia..."
> 
> **Z 2025-09-15:**
> > "Od sanitára k AI podnikateľovi - toto je môj príbeh transformácie..."

### Príklad 2: Otázka o Minulosti

**Ty:** "Ako som riešil n8n problémy?"

**Ja (s RAG):**
> V tvojich promptoch som našiel niekoľko zmienok o riešení n8n problémov:
> 
> **Z 2025-10-04:**
> > "Riešil som n8n workflow automatizáciu, kde som musel nastaviť..."

---

## 🔧 Manuálne Použitie (Ak Potrebuješ)

### Cez MCP Endpoint

```bash
curl -X POST http://127.0.0.1:27125/rag/search \
  -H "Authorization: Bearer <OBSIDIAN_API_KEY>" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "transformácia identity",
    "top_k": 5,
    "min_score": 0.4
  }'
```

### Cez Python Skript

```bash
cd "/Users/_xvadur/Desktop/Magnum Opus"
source temp_pdf_env/bin/activate
python3 xvadur_brave/scripts/rag_agent_helper.py "tvoj dotaz" 5 0.4
```

---

## 📊 Parametre RAG Search

### `query` (povinný)
Vyhľadávací dotaz - čo hľadáš v promptoch.

### `top_k` (voliteľný, default: 5)
Počet výsledkov (1-50).

**Odporúčania:**
- `top_k: 3` - rýchle, presné výsledky
- `top_k: 5` - vyvážené (odporúčané)
- `top_k: 10` - viac kontextu

### `min_score` (voliteľný, default: 0.4)
Minimálne similarity score (0-1).

**Odporúčania:**
- `min_score: 0.5` - len vysoko relevantné výsledky
- `min_score: 0.4` - vyvážené (odporúčané)
- `min_score: 0.3` - viac výsledkov, menej relevantné

---

## 🎯 Kedy Použiť RAG?

### ✅ POUŽIŤ RAG, keď:
- Otázka je o minulosti ("Čo som hovoril...")
- Potrebuješ kontext z histórie
- Hľadáš relevantné prompty
- Chceš vidieť evolúciu myšlienok

### ❌ NEPOUŽIŤ RAG, keď:
- Otázka je čisto technická (ako niečo urobiť)
- Otázka je o budúcnosti (plány, vízie)
- Otázka nevyžaduje kontext z minulosti

---

## 🔄 Workflow

```
Tvoja otázka
    ↓
Rozpoznám potrebu kontextu?
    ↓ ÁNO
Zavolám /rag/search
    ↓
Nájdem relevantné prompty
    ↓
Použijem ich v odpovedi
    ↓
Citácie + Kontext
```

---

## 📝 Formát Odpovede s RAG

Keď použijem RAG, odpoveď bude obsahovať:

1. **Zhrnutie:** Čo som našiel
2. **Citácie:** Relevantné prompty s dátumami
3. **Kontext:** Ako to súvisí s tvojou otázkou
4. **Zdroj:** Odkazy na pôvodné súbory

---

## 🚀 Ďalšie Vylepšenia (Budúcnosť)

1. **Konverzačná pamäť:** RAG si pamätá predchádzajúce otázky
2. **Temporálne filtrovanie:** Vyhľadávanie len v určitom období
3. **Hybrid search:** Kombinácia semantic + keyword search
4. **Automatické citácie:** Vždy citovať zdroje

---

## 💡 Tipy

1. **Buď špecifický:** "Čo som hovoril o recepčnej v novembri?" je lepšie ako "Čo som hovoril o recepčnej?"
2. **Používaj dátumy:** "Čo sa stalo v júli 2025?" je presnejšie
3. **Kombinuj témy:** "Ako som riešil n8n + recepčná?" nájde relevantné prompty

---

**Status:** ✅ Funkčný  
**Integrácia:** MCP Server + Cursor Agent  
**Dáta:** 664 promptov → 1,204 chunkov

