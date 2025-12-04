# 🧠 RAG System - Extended (Prompts + AI Responses)

**Status:** ✅ Implementované  
**Dátum:** 2025-12-04  
**Verzia:** Extended (v2.0)

---

## 📋 Prehľad

Rozšírený RAG systém zahŕňa nielen user prompty, ale aj AI odpovede z conversation pairs. Toto poskytuje kompletný kontext dialógu a lepšie možnosti vyhľadávania.

---

## 🆕 Nové Funkcie

### 1. Conversation Pairs v Indexe

- **Zdroj:** `xvadur/data/kortex_guaranteed/conversation_pairs_guaranteed.jsonl`
- **Formát:** Kombinovaný dialóg (`User: ...\n\nAssistant: ...`)
- **Počet:** 1,822 conversation pairs
- **Content Type:** `pair`

### 2. Content Type Filtering

Môžeš filtrovať výsledky podľa typu:
- `prompt` - len user prompty
- `response` - len AI odpovede (ak sú samostatné)
- `pair` - kompletný dialóg (prompt + odpoveď)
- `None` - všetko (default)

### 3. Rozšírené Metadata

Každý chunk má teraz:
- `content_type` - typ obsahu (prompt/response/pair)
- `user_text` - user prompt (pre pairs)
- `ai_text` - AI odpoveď (pre pairs)
- `session` - session ID (pre pairs)

---

## 🚀 Použitie

### Rebuild Indexu s AI Odpoveďami

```bash
python3 scripts/rag/build_rag_index.py
```

**Čo sa stane:**
- Načíta prompty z `data/prompts/prompts_split` (ak existuje)
- Načíta conversation pairs z `xvadur/data/kortex_guaranteed/conversation_pairs_guaranteed.jsonl`
- Kombinuje prompt + odpoveď ako jeden chunk
- Vytvorí FAISS index s embeddings
- Uloží metadata a chunks

**Čas:** ~10-15 minút (závisí od počtu chunkov)  
**Náklady:** ~$10-20 (pre ~3,644 chunkov)

---

### Vyhľadávanie

#### Základné Vyhľadávanie (Všetko)

```bash
python3 scripts/rag/rag_search.py "tvoj dotaz" 5 true
```

#### Filtrovanie podľa Content Type

```bash
# Len conversation pairs (kompletný dialóg)
python3 scripts/rag/rag_search.py "transformácia identity" 10 true pair

# Len user prompty
python3 scripts/rag/rag_search.py "ako som riešil n8n" 5 true prompt

# Všetko (default)
python3 scripts/rag/rag_search.py "tvoj dotaz" 5 true none
```

---

## 📊 Štruktúra Dát

### Conversation Pairs

Každý pár sa ukladá ako kombinovaný dialóg:

```
User: [user prompt text]

Assistant: [AI response text]
```

**Výhody:**
- Kompletný kontext - vidíš prompt aj odpoveď
- Lepšie syntézy - RAG môže použiť celý dialóg
- Zachovaná súvislosť

---

## 🔧 Konfigurácia

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

## 📈 Výhody

1. **Lepší kontext** - kompletný dialóg namiesto len promptov
2. **Viac dát** - 1,822 párov = 3,644 chunkov (prompty + odpovede)
3. **Lepšie syntézy** - RAG môže použiť aj AI odpovede
4. **Flexibilita** - možnosť filtrovať podľa typu

---

## 🔍 Príklady Použitia

### Príklad 1: Vyhľadávanie v Conversation Pairs

```bash
python3 scripts/rag/rag_search.py "čo AI hovorilo o mojej transformácii" 10 true pair
```

**Výsledok:** Nájde conversation pairs, kde AI hovorilo o transformácii.

### Príklad 2: Vyhľadávanie v User Prompts

```bash
python3 scripts/rag/rag_search.py "ako som riešil n8n problémy" 5 true prompt
```

**Výsledok:** Nájde len user prompty o n8n.

### Príklad 3: Všetko

```bash
python3 scripts/rag/rag_search.py "AI recepčná" 10 true
```

**Výsledok:** Nájde všetko (prompty aj conversation pairs) o AI recepčnej.

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

## 🔄 Spätná Kompatibilita

- Existujúce prompty zostanú v indexe
- Pôvodné search funkcie fungujú bez zmeny
- Nové funkcie sú voliteľné (content_type_filter)

---

## 💡 Tipy

1. **Pre kompletný kontext:** Použi `content_type_filter="pair"` - uvidíš prompt aj odpoveď
2. **Pre špecifické vyhľadávanie:** Použi `content_type_filter="prompt"` - len tvoje prompty
3. **Pre syntézy:** Použi všetko (bez filteru) - RAG môže použiť najrelevantnejšie výsledky

---

## 🐛 Troubleshooting

### Chyba: "Conversation pairs file neexistuje"

**Riešenie:** Skontroluj, či existuje `xvadur/data/kortex_guaranteed/conversation_pairs_guaranteed.jsonl`

### Chyba: "Žiadne conversation pairs"

**Riešenie:** Skript pokračuje len s promptmi (ak existujú)

### Index je príliš veľký

**Riešenie:** Nastav `INCLUDE_AI_RESPONSES = False` v `build_rag_index.py`

---

**Vytvorené:** 2025-12-04  
**Status:** ✅ Implementované, ⏸️ Rebuild pozastavený (OpenAI kvóta)

## ⚠️ Aktuálny Stav (2025-12-04)

**Implementácia:** ✅ Hotová
- Všetky funkcie implementované
- API key loading opravený (načítava z `.env`)
- Content type filtering funguje

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

**Alternatíva:** Použiť len prompty (bez conversation pairs) - nastav `INCLUDE_AI_RESPONSES = False`


