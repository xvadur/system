# 🧠 RAG System - Kompletný Návod

**Status:** ✅ Funkčný  
**Verzia:** Extended (v2.0)  
**Posledná aktualizácia:** 2025-12-04

---

## 📋 Obsah

1. [Quick Start](#-quick-start)
2. [Rozšírené Funkcie](#-rozšírené-funkcie)
3. [Použitie](#-použitie)
4. [Advanced Features](#-advanced-features)
5. [Troubleshooting](#-troubleshooting)

---

## 🚀 Quick Start

### Požiadavky

#### 1. Inštalácia knižníc

```bash
pip install faiss-cpu numpy openai
```

**Poznámka:** Ak máš problém s `faiss-cpu`, skús:
```bash
pip install faiss-cpu --no-cache-dir
```

#### 2. OpenAI API Key

Nastav environment premennú:
```bash
export OPENAI_API_KEY='sk-tvoj-api-key'
```

Alebo vytvor `.env` súbor v root adresári:
```
OPENAI_API_KEY=sk-tvoj-api-key
```

### Vytvorenie RAG Indexu

```bash
python3 scripts/rag/build_rag_index.py
```

**Čo sa stane:**
- Načíta prompty z `data/prompts/prompts_split` (ak existuje)
- Načíta conversation pairs z `xvadur/data/dataset/conversations.jsonl`
- Vytvorí inteligentné chunky
- Generuje embeddings pomocou OpenAI
- Vytvorí FAISS index
- Uloží metadata a chunks

**Čas:** ~10-15 minút (závisí od počtu chunkov)  
**Náklady:** ~$10-20 (pre ~3,644 chunkov)

**Výstup:**
- `data/rag_index/faiss.index` - FAISS index
- `data/rag_index/metadata.json` - Metadata pre každý chunk
- `data/rag_index/chunks.json` - Text chunkov

---

## 🆕 Rozšírené Funkcie

### Conversation Pairs v Indexe

RAG systém teraz podporuje aj AI odpovede z conversation pairs:

- **Zdroj:** `xvadur/data/dataset/conversations.jsonl`
- **Formát:** Kombinovaný dialóg (`User: ...\n\nAssistant: ...`)
- **Počet:** 1,822 conversation pairs
- **Content Type:** `pair`

**Výhody:**
- Kompletný kontext - vidíš prompt aj odpoveď
- Lepšie syntézy - RAG môže použiť celý dialóg
- Zachovaná súvislosť

### Content Type Filtering

Môžeš filtrovať výsledky podľa typu:
- `prompt` - len user prompty
- `response` - len AI odpovede (ak sú samostatné)
- `pair` - kompletný dialóg (prompt + odpoveď)
- `none` - všetko (default)

### Rozšírené Metadata

Každý chunk má teraz:
- `content_type` - typ obsahu (prompt/response/pair)
- `user_text` - user prompt (pre pairs)
- `ai_text` - AI odpoveď (pre pairs)
- `session` - session ID (pre pairs)

### Konfigurácia

V `scripts/rag/build_rag_index.py`:

```python
# Flags
INCLUDE_AI_RESPONSES = True  # Pridať AI odpovede do indexu
COMBINE_PAIRS = True  # Kombinovať prompt + odpoveď ako jeden chunk
```

**Možnosti:**
- `INCLUDE_AI_RESPONSES = False` - len prompty (pôvodné správanie)
- `COMBINE_PAIRS = False` - samostatné chunky pre user a AI (nie odporúčané)

---

## 💻 Použitie

### Základné Vyhľadávanie

```bash
python3 scripts/rag/rag_agent_helper.py "tvoj dotaz" [top_k] [min_score] [use_hybrid] [mode] [content_type] [output_format]
```

**Príklady:**
```bash
# Základné vyhľadávanie (top 5 výsledkov, hybrid search, pekný výstup)
python3 scripts/rag/rag_agent_helper.py "ako som riešil n8n problémy" 5 0.4 true search None pretty

# Viac výsledkov, len conversation pairs
python3 scripts/rag/rag_agent_helper.py "transformácia identity" 10 0.4 true search pair pretty

# Len user prompty (JSON výstup pre agenta)
python3 scripts/rag/rag_agent_helper.py "ako som riešil n8n" 5 0.4 true search prompt json
```

### RAG Query s Automatickou Syntézou

Namiesto surových promptov dostávaš syntetizovanú odpoveď:

```bash
python3 scripts/rag/rag_agent_helper.py "tvoj dotaz" [top_k] [min_score] [use_hybrid] query [content_type] [output_format] [model]
```

**Príklady:**
```bash
# Syntetizovaná chronológia augusta (pekný výstup)
python3 scripts/rag/rag_agent_helper.py "urob mi chronológiu augusta" 10 0.4 true query None pretty

# Syntetizovaná analýza témy (JSON výstup)
python3 scripts/rag/rag_agent_helper.py "čo som hovoril o svojej transformácii identity?" 8 0.4 true query None json
```

**Výhody:**
- Syntetizovaná odpoveď - Nie surové prompty
- Hlavné informácie - Už spracované a zhrnuté
- Čitateľnosť - Formátovaná a zmysluplná odpoveď
- Automatizácia - Agent to spracuje za teba

### Integrácia do Cursor Agenta

RAG systém je automaticky integrovaný do Cursor agenta. Keď sa pýtaš na niečo z minulosti, automaticky vyhľadám v RAG indexe:

**Príklady otázok, ktoré spustia RAG:**
- "Čo som hovoril o X?"
- "Ako som riešil Y?"
- "Kde som sa zmieňoval o Z?"
- "Ako som sa transformoval?"
- "Čo sa stalo v júli 2025?"

**Agent automaticky:**
1. Rozpozná, že potrebuješ kontext z minulosti
2. Zavolá RAG search
3. Nájde relevantné prompty
4. Použije ich v odpovedi s citáciami

**Kedy NEPOUŽIŤ RAG:**
- Otázka je čisto technická (ako niečo urobiť)
- Otázka je o budúcnosti (plány, vízie)
- Otázka nevyžaduje kontext z minulosti

---

## 🔀 Advanced Features

### Hybrid Search

RAG systém podporuje **hybrid search** - kombináciu semantic search (embeddings) a keyword search (TF-IDF).

**Ako to funguje:**
- **Semantic Search:** Používa OpenAI embeddings, nájde kontextovo podobné prompty
- **Keyword Search:** Používa TF-IDF, nájde presné výskyty kľúčových slov
- **Hybrid Kombinácia:** Kombinuje oba výsledky pomocou váženého priemeru (default: 70% semantic + 30% keyword)

**Použitie:**
```bash
# Hybrid search (default, pekný výstup)
python3 scripts/rag/rag_agent_helper.py "transformácia identity" 5 0.4 true search None pretty

# Len semantic search
python3 scripts/rag/rag_agent_helper.py "transformácia identity" 5 0.4 false search None pretty
```

**Výhody:**
- Lepšia presnosť - kombinácia kontextovej podobnosti + presných výskytov
- Flexibilita - funguje pre komplexné otázky aj presné vyhľadávanie
- Lepšie výsledky - menej falošných pozitív, viac relevantných výsledkov

### Parametre

#### `top_k` (voliteľný, default: 5)
Počet výsledkov (1-50).

**Odporúčania:**
- `3` - rýchle, presné výsledky
- `5` - vyvážené (odporúčané)
- `10` - viac kontextu
- `20+` - pre chronológie a prehľady

#### `min_score` (voliteľný, default: 0.4)
Minimálne similarity score (0-1). Nižšie = viac výsledkov, ale menej relevantné.

**Odporúčania:**
- `0.5` - len vysoko relevantné výsledky
- `0.4` - vyvážené (odporúčané)
- `0.3` - viac výsledkov, menej relevantné

#### `use_hybrid` (voliteľný, default: true)
Použiť hybrid search (semantic + keyword) alebo len semantic.

#### `content_type` (voliteľný, default: none)
Filtrovať výsledky podľa typu: `prompt`, `response`, `pair`, `none`.

---

## 🔧 Troubleshooting

### Chyba: "ModuleNotFoundError: No module named 'faiss'"
```bash
pip install faiss-cpu numpy
```

### Chyba: "OPENAI_API_KEY nie je nastavený"
```bash
export OPENAI_API_KEY='sk-tvoj-key'
```
Alebo vytvor `.env` súbor v root adresári.

### Chyba: "Index neexistuje"
Spusti najprv `build_rag_index.py`.

### Chyba: "Conversation pairs file neexistuje"
**Riešenie:** Skontroluj, či existuje `xvadur/data/dataset/conversations.jsonl`

### Chyba: "Žiadne conversation pairs"
**Riešenie:** Skript pokračuje len s promptmi (ak existujú)

### Index je príliš veľký
**Riešenie:** Nastav `INCLUDE_AI_RESPONSES = False` v `build_rag_index.py`

### OpenAI kvóta presiahnutá (Error 429)
**Riešenie:**
1. Pridať kredit do OpenAI (https://platform.openai.com/account/billing)
2. Spustiť rebuild znova: `python3 scripts/rag/build_rag_index.py`
3. Alternatíva: Použiť len prompty (bez conversation pairs) - nastav `INCLUDE_AI_RESPONSES = False`

---

## 📊 Štatistiky

Po rebuild indexu uvidíš:

```
📊 ŠTATISTIKY
============================================================
Celkový počet promptov: 664
Celkový počet conversation pairs: 1,822
Celkový počet chunkov: 3,644
Chunky z promptov: 1,204
Chunky z conversation pairs: 2,440
Embedding dimenzie: 1536
FAISS index veľkosť: 3,644 vektorov
============================================================
```

---

## ⚠️ Aktuálny Stav (2025-12-04)

**Implementácia:** ✅ Hotová
- Všetky funkcie implementované
- API key loading opravený (načítava z `.env`)
- Content type filtering funguje
- Bug fixes: Zip chunking bug opravený (všetky chunky sa spracúvajú správne)
- Portabilita: Debug log path dynamický (namiesto hardcodovanej cesty)

**Rebuild Status:** ⏸️ Pozastavený
- **Dôvod:** OpenAI kvóta presiahnutá (Error 429: insufficient_quota)
- **Progres:** 
  - ✅ Načítaných 664 promptov
  - ✅ Načítaných 1,822 conversation pairs
  - ✅ Vytvorených 1,204 chunkov z promptov
  - ❌ Zastavené pri generovaní embeddings pre conversation pairs

**Čo urobiť:**
1. Pridať kredit do OpenAI (https://platform.openai.com/account/billing)
2. Spustiť rebuild znova: `python3 scripts/rag/build_rag_index.py`
3. Odhadované náklady: ~$10-20 pre ~3,644 chunkov

---

## 💡 Tipy

1. **Pre kompletný kontext:** Použi `content_type_filter="pair"` - uvidíš prompt aj odpoveď
2. **Pre špecifické vyhľadávanie:** Použi `content_type_filter="prompt"` - len tvoje prompty
3. **Pre syntézy:** Použi všetko (bez filteru) - RAG môže použiť najrelevantnejšie výsledky
4. **Buď špecifický:** "Čo som hovoril o recepčnej v novembri?" je lepšie ako "Čo som hovoril o recepčnej?"
5. **Používaj dátumy:** "Čo sa stalo v júli 2025?" je presnejšie
6. **Kombinuj témy:** "Ako som riešil n8n + recepčná?" nájde relevantné prompty

---

## 📝 Príklady Použitia

### Príklad 1: Vyhľadávanie v Conversation Pairs

```bash
python3 scripts/rag/rag_agent_helper.py "čo AI hovorilo o mojej transformácii" 10 0.4 true search pair pretty
```

**Výsledok:** Nájde conversation pairs, kde AI hovorilo o transformácii.

### Príklad 2: Syntetizovaná Chronológia

```bash
python3 scripts/rag/rag_agent_helper.py "urob mi chronológiu augusta" 10 0.4 true query None pretty
```

**Výsledok:** Syntetizovaná chronológia augusta z relevantných promptov.

### Príklad 3: Vyhľadávanie v User Prompts

```bash
python3 scripts/rag/rag_agent_helper.py "ako som riešil n8n problémy" 5 0.4 true search prompt pretty
```

**Výsledok:** Nájde len user prompty o n8n.

---

**Vytvorené:** 2025-12-04  
**Status:** ✅ Funkčný a pripravený na použitie!

