# 📚 Prompts Database - Dokumentácia a Metriky

**Vytvorené:** 2025-12-03  
**Status:** 🟢 Aktívna práca  
**Účel:** Centralizovaná dokumentácia a metriky pre databázu promptov

---

## 📊 Základné Metriky

### Celkové Štatistiky
- **Celkový počet promptov:** 664 (historické) + 45 (aktuálne v `prompts_log.jsonl`)
- **Časové obdobie:** 2025-07-19 až 2025-11-06 (historické) + 2025-12-02 až teraz (aktuálne)
- **Formát:** JSON (historické) + JSONL (aktuálne)
- **Organizácia:** Podľa dátumov v `prompts_split/` adresári

### Rozdelenie podľa Mesiacov

| Mesiac | Počet Promptov | Word Count | Počet Viet | Median Viet | Top 3 Témy |
|--------|---------------|------------|------------|-------------|------------|
| Júl 2025 | 153 | 23,539 | 1,198 | 5.0 | AI Technologie, Depresia/Frustrácia, Automatizácia/Kód |
| August 2025 | 185 | 51,506 | 2,337 | 6.0 | AI Technologie, Biznis/Projekty, Depresia/Frustrácia |
| September 2025 | 214 | 124,768 | 5,559 | 10.0 | AI Technologie, Biznis/Projekty, Depresia/Frustrácia |
| Október 2025 | 96 | 45,490 | 2,415 | 13.0 | AI Technologie, Depresia/Frustrácia, Biznis/Projekty |
| November 2025 | 16 | 7,053 | 378 | 12.0 | AI Technologie, Depresia/Frustrácia, Biznis/Projekty |
| December 2025 | 44 | 2,592 | 154 | 1.0 | Osobný Rozvoj, Workspace Systémy, AI Technologie |

**Celkom:** 708 promptov, 254,948 slov, 12,041 viet

---

## 📁 Štruktúra Databázy

### Historické Prompty (`prompts_split/`)
```
data/prompts/prompts_split/
├── 2025-07-19/     # 15 promptov
├── 2025-07-20/     # 19 promptov
├── 2025-07-21/     # 10 promptov
├── ...
└── 2025-11-06/     # 1 prompt
```

**Formát JSON súboru:**
```json
{
  "date": "2025-07-27",
  "timestamp": "2025-07-27T01:59:58.460000+00:00",
  "index": 10,
  "text": "...",
  "word_count": 1074,
  "source_path": "data/chronology/2025-07-27.md",
  "author_guess": "adam"
}
```

### Aktuálne Prompty (`prompts_log.jsonl`)
```
xvadur/data/prompts_log.jsonl
```

**Formát JSONL (jeden JSON objekt na riadok):**
```json
{
  "timestamp": "2025-12-03T13:08:44.711645+01:00",
  "role": "user",
  "content": "...",
  "metadata": {
    "source": "auto_save",
    "extraction_method": "real_time_agent_hook",
    "saved_at": "2025-12-03T13:08:44.711645+01:00"
  }
}
```

### Extrahované Aktivity (`prompts_activities.jsonl`) ⭐
```
data/prompts/prompts_activities.jsonl
```

**Formát JSONL (jeden JSON objekt na riadok):**
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

**Použitie:**
- Časová os aktivít: "Čo som robil v septembri 2025"
- Vyhľadávanie podľa aktivity
- Analýza myšlienok a tém
- Generovanie monthly summaries

**Vytvorené pomocou:** `scripts/extract_prompt_activities.py`

### NLP Analýza (`prompts_nlp4sk.jsonl`) ⭐
```
data/prompts/prompts_nlp4sk.jsonl
```

**Formát JSONL (jeden JSON objekt na riadok):**
```json
{
  "prompt_id": "2025-07-19_001",
  "date": "2025-07-19",
  "sentiment": "negative",
  "sentiment_score": 0.453,
  "people": ["Cibula"],
  "technologies": ["zapisal"],
  "concepts": ["tem", "text", "surova", "cyklik"],
  "analyzed_at": "2025-12-03T19:09:21"
}
```

**Obsahuje:**
- Sentiment analýza (negative/neutral/positive)
- Extrakcia entít (people, organizations, locations, technologies)
- Extrakcia pojmov (concepts)

**Vytvorené pomocou:** `scripts/analyze_prompts_nlp4sk.py` (lokálne NLP nástroje: Stanza, Hugging Face)

### Granularná Kategorizácia (`prompts_categorized.jsonl`) ⭐⭐
```
data/prompts/prompts_categorized.jsonl
```

**Formát JSONL (jeden JSON objekt na riadok):**
```json
{
  "prompt_id": "2025-07-19_001",
  "date": "2025-07-19",
  "sentiment": "negative",
  "category": "reflection",
  "subcategory": "emotional",
  "context": {
    "projects": [],
    "people": ["Cibula"],
    "technologies": ["zapisal"],
    "emotions": ["negative"]
  },
  "categorized_at": "2025-12-03T19:31:42"
}
```

**Obsahuje:**
- Všetko z NLP analýzy (sentiment, people, technologies, concepts)
- **Kategórie:** work, reflection, planning, problem_solving, learning
- **Subkategórie:** philosophical, personal, emotional, technical, strategic, business, design, debugging, research, tactical
- **Kontext:** projects, people, technologies, emotions

**Štatistiky (647 promptov):**
- **Kategórie:** 61.5% reflection, 15.8% work, 10.0% planning, 7.4% problem_solving, 5.3% learning
- **Top projekty:** n8n (89), Recepčná (11), aiappla (6)
- **Top emócie:** neutral (410), negative (129), frustration (49), positive (45)

**Použitie:**
- Analýza typov aktivít (reflection vs work)
- Projektová analýza (na čom pracoval)
- Emocionálna analýza (ako sa cítil)
- Temporálna analýza (ako sa menili kategórie v čase)

**Vytvorené pomocou:** `scripts/categorize_prompts_granular.py` (OpenAI API)

### Konsolidovaná Štruktúra (`prompts_enriched.jsonl`) ⭐⭐⭐ **ODPORÚČANÉ**
```
data/prompts/prompts_enriched.jsonl
```

**Účel:** Zlúčené metadáta z troch zdrojov (activities + NLP + categories) do jednej štruktúry.

**Formát JSONL (jeden JSON objekt na riadok):**
```json
{
  "prompt_id": "2025-07-19_001",
  "date": "2025-07-19",
  "timestamp": "2025-07-19T02:19:19.998000+00:00",
  "word_count": 61,
  
  "activity": "Adam pracoval na surovom zápise...",
  "thoughts": "Rozmýšľal o tom, ako sa menia témy...",
  "summary_extracted_at": "2025-12-03T15:23:35",
  
  "sentiment": "negative",
  "sentiment_score": 0.453,
  "people": ["Cibula"],
  "organizations": [],
  "locations": [],
  "technologies": ["zapisal"],
  "concepts": ["tem", "text", "surova", ...],
  "analyzed_at": "2025-12-03T19:09:21",
  
  "category": "reflection",
  "subcategory": "emotional",
  "context": {
    "projects": [],
    "people": ["Cibula"],
    "technologies": ["zapisal"],
    "emotions": ["negative"]
  },
  "categorized_at": "2025-12-03T19:31:42"
}
```

**Obsahuje:**
- ✅ Všetky základné metadáta (prompt_id, date, timestamp, word_count)
- ✅ Activity metadata (activity, thoughts)
- ✅ NLP metadata (sentiment, entities, concepts)
- ✅ Category metadata (category, subcategory, context)

**Štatistiky (649 promptov):**
- Má activity: 649 (100%)
- Má NLP: 649 (100%)
- Má category: 647 (99.7%)

**Výhody:**
- **Jeden zdroj pravdy** - Všetky metadáta na jednom mieste
- **Jednoduchšie dotazy** - Nemusíš načítavať 3 súbory
- **Lepšia performance** - Jeden súbor je rýchlejší
- **Kompletnosť** - Všetky metadáta v jednom zázname

**Vytvorené pomocou:** `scripts/merge_prompt_metadata.py`

**Dokumentácia:** Pozri [METADATA_STRUCTURE.md](METADATA_STRUCTURE.md) pre kompletnú dokumentáciu štruktúry a príklady použitia.

### Temporálna Mapa (`temporal_map.json`) ⭐⭐ **NAJNOVŠÍ**
```
data/prompts/temporal_map.json
```

**Obsahuje:**
- **Story arcs:** Príbehy projektov v čase (sekvencie promptov o tom istom projekte)
- **Temporálne clustery:** Súvisiace prompty v rámci 7 dní (zdieľajú projekty, kategórie alebo koncepty)

**Formát JSON:**
```json
{
  "story_arcs": [
    {
      "project": "n8n",
      "prompt_ids": ["2025-07-19_013", ...],
      "prompt_count": 89,
      "start_date": "2025-07-19",
      "end_date": "2025-11-01",
      "duration_days": 106,
      "dominant_category": "work",
      "sentiment_trend": "neutral"
    }
  ],
  "temporal_clusters": [
    {
      "cluster_id": "cluster_1",
      "prompt_ids": [...],
      "prompt_count": 51,
      "projects": ["n8n", "github"],
      "dominant_category": "reflection"
    }
  ]
}
```

**Štatistiky (647 promptov):**
- **Story arcs:** 18 projektov
- **Temporálne clustery:** 51 clusterov
- **Prompty v arcach:** 148 (22.9%)
- **Prompty v clusteroch:** 638 (98.6%)

**Top 5 story arcs:**
1. **n8n:** 89 promptov za 106 dní (2025-07-19 - 2025-11-01)
2. **Recepčná:** 11 promptov za 61 dní (2025-10-04 - 2025-12-03)
3. **aiappla:** 6 promptov za 60 dní (2025-08-02 - 2025-09-30)
4. **analyza_konvecia:** 5 promptov za 43 dní (2025-07-23 - 2025-09-03)
5. **github:** 4 promptov za 11 dní (2025-07-21 - 2025-07-31)

**Použitie:**
- Analýza projektových príbehov (ako sa vyvíjal projekt v čase)
- Identifikácia temporálnych vzorcov (kedy pracoval na čom)
- Nájdenie súvisiacich promptov (clustery)

**Vytvorené pomocou:** `scripts/create_temporal_map.py`

---

## 🔧 Nástroje a Skripty

### Existujúce Nástroje
1. **`scripts/auto_save_prompt.py`**
   - Automatické ukladanie promptov v reálnom čase
   - Ukladá do `xvadur/data/prompts_log.jsonl`
   - Používa MinisterOfMemory systém

2. **`scripts/extract_prompt_activities.py`** ⭐ **NOVÝ**
   - Extrahuje aktivitu a myšlienky z každého promptu pomocou OpenAI API
   - Filtruje prompty < 1000 slov (dlhé preskočí)
   - Ukladá výsledky do `data/prompts/prompts_activities.jsonl`
   - Resume functionality - môže pokračovať po prerušení
   - Test mode pre testovanie na malom sample

3. **`scripts/rag/build_rag_index.py`**
   - Vytvára FAISS index z historických promptov
   - Embeddings: `text-embedding-3-small` (1536 dimenzií)
   - Output: `data/rag_index/`

4. **`scripts/rag/rag_search.py`**
   - Vyhľadávanie v RAG indexe
   - Semantic search cez FAISS

5. **`ministers/memory.py`** + **`ministers/storage.py`**
   - MinisterOfMemory systém
   - FileStore pre persistentné ukladanie (JSONL)

---

## 📈 Metriky a Analýzy

### Plánované Analýzy
*(Bude dopĺňané počas práce)*

- [x] Celkový word count
- [x] Priemerná dĺžka promptu
- [x] Rozdelenie podľa dĺžky
- [x] Tematická analýza (topics, keywords)
- [x] Časové trendy (prompty za deň/mesiac)
- [ ] Emocionálna analýza (ak je dostupná)
- [ ] Komplexita jazyka (readability score)
- [ ] Unikátne slová (vocabulary diversity)
- [ ] Gramatické kategórie (slovesá, podstatné mená, atď.)

### Aktuálne Metriky

**Vypočítané:** 2025-12-03

- **Celkový počet promptov:** 708 (664 historických + 44 aktuálnych)
- **Celkový word count:** 254,948 slov
- **Celkový počet viet:** 12,041 viet
- **Priemerný word count na prompt:** ~360 slov
- **Priemerný počet viet na prompt:** ~17 viet

**Top mesiace podľa aktivity:**
1. **September 2025:** 214 promptov, 124,768 slov (najaktívnejší mesiac)
2. **August 2025:** 185 promptov, 51,506 slov
3. **Júl 2025:** 153 promptov, 23,539 slov

**Trendy:**
- **Najvyšší median viet:** Október 2025 (13.0 viet na prompt)
- **Najnižší median viet:** December 2025 (1.0 veta na prompt) - čiastočné dáta
- **Najviac slov:** September 2025 (124,768 slov)

**Dominantné témy:**
- **AI Technologie:** Dominantná téma v každom mesiaci (okrem decembra 2025)
  - Najvyššie skóre: September 2025 (2,396 výskytov)
  - Témy: ChatGPT, OpenAI, LLM, prompty, API, automatizácia, n8n, workflow
- **Depresia/Frustrácia:** Častá téma v júli až novembri 2025
  - Najvyššie skóre: September 2025 (514 výskytov)
  - **⚠️ Dôležité zistenie:** Väčšina nie je skutočná depresia! (pozri `DEPRESSION_ANALYSIS.md`)
    - 41.9% je neistota/konzultácia ("neviem", "neviem ako")
    - 8.1% je frustrácia z práce ("odpor", "nefunguje")
    - Len 8.7% je skutočná depresia ("smutok", "strateny", "sam")
- **Biznis/Projekty:** Významná téma v auguste až novembri 2025
  - Najvyššie skóre: September 2025 (588 výskytov)
  - Témy: Newsletter, mladí lekári, stratégia, monetizácia
- **Osobný Rozvoj:** Dominantná téma v decembri 2025 (46 výskytov)
- **Workspace Systémy:** Nová téma v decembri 2025 (42 výskytov)
  - Témy: Cursor, Obsidian, MCP, savegame, loadgame, logy

---

## 🎯 Ciele Práce s Databázou

### Fáza 1: Analýza a Dokumentácia ✅
- [x] Vytvorenie README dokumentu
- [x] Základné štatistiky (počet, word count, časové obdobie)
- [ ] Analýza štruktúry dát

### Fáza 2: Konzolidácia a Migrácia
- [ ] Spojenie historických a aktuálnych promptov
- [ ] Unifikácia formátu (ak je potrebné)
- [ ] Validácia dát (duplikáty, chyby)

### Fáza 3: Rozšírené Analýzy
- [ ] Tematická analýza
- [ ] Časové trendy
- [ ] Emocionálna analýza
- [ ] Komplexita jazyka

### Fáza 4: Integrácia a Vylepšenia
- [ ] Aktualizácia RAG indexu
- [ ] Vylepšenie vyhľadávania
- [ ] Integrácia s MinisterOfMemory
- [ ] Automatizácia metrík

---

## 📝 Priebežné Poznámky

### 2025-12-03
- Vytvorený README dokument
- Identifikovaných 664 historických promptov
- 44 aktuálnych promptov v `prompts_log.jsonl`
- Začiatok práce s databázou promptov
- Vytvorený skript `scripts/analyze_prompts_metrics.py` pre analýzu metrík
- Vypočítané základné metriky podľa mesiacov:
  - Počet promptov, word count, počet viet, median viet
  - Celkom: 708 promptov, 254,948 slov, 12,041 viet
- Vytvorený skript `scripts/analyze_prompts_topics_final.py` pre tematickú analýzu
- Identifikované top 3 témy pre každý mesiac
- **Analýza "Depresie/Frustrácie":**
  - 322 promptov (45.5% z celkového počtu) obsahuje depresné/frustračné znaky
  - **Kľúčové zistenie:** Väčšina nie je skutočná depresia!
    - **Neistota (41.9%):** "neviem", "neviem ako", "neviem co" - konzultácia s AI, neistota pri práci
    - **Frustrácia z práce (8.1%):** "odpor", "nefunguje", "nemozem" - technické problémy, frustrácia z projektov
    - **Skutočná depresia (8.7%):** "smutok", "strateny", "sam", "opusteny" - skutočná depresia
    - **Zmiešané (41.3%):** Kombinácia viacerých kategórií
  - **Záver:** "Depresia/Frustrácia" ako téma je hlavne neistota a konzultácia s AI, nie skutočná depresia
- **Extrakcia aktivít z promptov:**
  - Vytvorený skript `scripts/extract_prompt_activities.py`
  - Extrahuje aktivitu a myšlienky z každého promptu pomocou OpenAI API
  - Filtruje prompty < 1000 slov (dlhé preskočí)
  - Ukladá výsledky do `data/prompts/prompts_activities.jsonl`
  - Resume functionality - môže pokračovať po prerušení
  - Test mode pre testovanie na malom sample
  - **Štatistiky:** 606 promptov < 1000 slov z 664 historických (91.3%)

---

## 🔗 Súvisiace Dokumenty

- `DEPRESSION_ANALYSIS.md` - Detailná analýza "Depresie/Frustrácie" v promptoch
- `scripts/rag/README.md` - RAG systém dokumentácia
- `xvadur/data/prompts_log.jsonl` - aktuálne prompty
- `ministers/memory.py` - MinisterOfMemory systém
- `data/rag_index/` - FAISS index pre vyhľadávanie

---

## 📚 Formáty a Štandardy

### Historické Prompty (JSON)
- **Povinné polia:** `date`, `timestamp`, `index`, `text`
- **Voliteľné polia:** `word_count`, `source_path`, `author_guess`
- **Kódovanie:** UTF-8
- **Organizácia:** `YYYY-MM-DD/XXX.json` (XXX = index)

### Aktuálne Prompty (JSONL)
- **Povinné polia:** `timestamp`, `role`, `content`
- **Voliteľné polia:** `metadata`
- **Kódovanie:** UTF-8
- **Formát:** Jeden JSON objekt na riadok

---

**Posledná aktualizácia:** 2025-12-03  
**Status:** 🟢 Aktívna práca

