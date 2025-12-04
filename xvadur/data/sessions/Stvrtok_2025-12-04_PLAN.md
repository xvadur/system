# 📋 Plán: Štvrtok 2025-12-04 - Týždenné Témové Mapovanie

**Dátum:** 2025-12-04  
**Session:** Štvrtok (pokračovanie)  
**Status:** 📝 Plánovaná  

---

## 🎯 Cieľ Session

**Hlavný úkol:** Vytvoriť systém na týždenné témové mapovanie a praktické vizualizácie dát z Kortex backupu.

---

## ✅ Čo máme Hotové (Z Predchádzajúcej Session)

### 1. Vyčistené Dáta z Kortex Backupu
- ✅ **1,822 konverzačných párov** (user prompt + AI odpoveď)
- ✅ **1,801 unikátnych user promptov**
- ✅ **1,880 unikátnych AI odpovedí**
- ✅ **126 denných chronológií** (kompletný dialóg)
- ✅ **6 mesačných chronológií**
- ✅ **50 vygenerovaných promptov** od AI

### 2. Časové Pokrytie
- **Perióda:** 2025-07-16 až 2025-12-01
- **Aktívnych dní:** 126
- **Mesiacov:** 6

### 3. Vytvorené Skripty a Nástroje
- `scripts/extract_kortex_ai_responses.py` - Extrakcia AI odpovedí
- `scripts/create_kortex_chronology.py` - Vytvorenie chronológie
- `scripts/extract_generated_prompts_from_ai.py` - Extrakcia promptov
- `scripts/analyze_generated_prompts.py` - Analýza promptov

---

## 🎯 Plán na Túto Session

### FÁZA 1: Týždenné Témové Mapovanie (Priorita #1)

#### 1.1 Zoskupenie Promptov podľa Týždňov
- [ ] Načítať konverzačné páry z `kortex_guaranteed/conversation_pairs_guaranteed.jsonl`
- [ ] Zoskupiť podľa ISO týždňov (2025-W29 až W49)
- [ ] Vytvoriť štruktúrovaný dataset pre každý týždeň

#### 1.2 Identifikácia Hlavných Tém (NLP/Topic Modeling)
- [ ] Vytvoriť skript `scripts/identify_weekly_themes.py`
- [ ] Použiť NLP techniky na extrakciu tém:
  - Kľúčové slová a frázy
  - Frekvenčná analýza
  - Topic modeling (LDA alebo BERTopic)
  - Entity extraction (projekty, ľudia, koncepty)
- [ ] Identifikovať 3-5 hlavných tém pre každý týždeň

#### 1.3 Vytvorenie Týždenných Reportov
- [ ] Pre každý týždeň vytvoriť markdown report obsahujúci:
  - **Počet konverzácií**
  - **Priemerná dĺžka promptov** (slová)
  - **Priemerná dĺžka AI odpovedí** (slová)
  - **Dominantné témy** (3-5 hlavných tém)
  - **Kľúčové citácie** (top 3-5 najdôležitejších promptov)
  - **Trendy** (porovnanie s predchádzajúcim týždňom)
  - **Štatistiky** (aktivita podľa hodín, dni v týždni)

**Výstup:**
- `xvadur/data/kortex_analysis/weekly_themes/` - adresár s týždennými reportmi
- `xvadur/data/kortex_analysis/weekly_themes/README.md` - index a prehľad

---

### FÁZA 2: Rozšírenie RAG Systému

#### 2.1 Týždenné Syntézy
- [ ] Pridať do RAG systému možnosť týždenných syntéz
- [ ] Query: "Aké boli hlavné témy týždňa W38?"
- [ ] RAG nájde všetky prompty z toho týždňa
- [ ] Syntéza do "Týždenného Reportu"

#### 2.2 Tematické Syntézy
- [ ] Pridať možnosť tematických syntéz
- [ ] Query: "Ako som sa vyvíjal v téme 'AI recepčná'?"
- [ ] RAG nájde všetky prompty o recepčnej (naprieč časom)
- [ ] Syntéza do "Timeline témy"

#### 2.3 Automatické Rozširovanie Denných Záznamov
- [ ] Vytvoriť systém, ktorý automaticky rozširuje denné záznamy
- [ ] Pre každý deň:
  - Tvoje denné záznamy
  - + RAG syntéza relevantných promptov z minulosti
  - = Kompletný kontext dňa

---

### FÁZA 3: Praktické Vizualizácie (Namiesto Grafana)

#### 3.1 Jednoduchý HTML Dashboard
- [ ] Vytvoriť skript `scripts/generate_kortex_dashboard.py`
- [ ] Generovať HTML stránku s:
  - **Týždenné Heat Mapy** (aktivita, počet konverzácií)
  - **Timeline Aktivít** (aktivita podľa hodín, dní)
  - **Tematické Mapy** (vizualizácia tém naprieč časom)
  - **Trendové Grafy** (zmeny v komplexnosti, dĺžke)
  - **Interaktívne Filtrovanie** (podľa týždňa, témy, mesiaca)

**Výstup:**
- `xvadur/data/kortex_analysis/dashboard.html` - HTML dashboard
- Použitie: `python scripts/generate_kortex_dashboard.py` → otvoríš v prehliadači

#### 3.2 Vizualizácie Metrík
- [ ] Word count trends (podľa týždňa/mesiaca)
- [ ] Aktivita podľa hodín (heat map)
- [ ] Aktivita podľa dní v týždni
- [ ] Komplexnosť promptov (priemerná dĺžka)
- [ ] Tematická distribúcia (pie chart alebo bar chart)

---

### FÁZA 4: Dokumentácia a Organizácia

#### 4.1 Aktualizácia README Súborov
- [ ] Aktualizovať `xvadur/data/kortex_analysis/README.md`
- [ ] Pridať dokumentáciu k týždenným témam
- [ ] Pridať dokumentáciu k dashboardu

#### 4.2 Zhrnutie Výsledkov
- [ ] Vytvoriť `xvadur/data/kortex_analysis/NEXT_STEPS.md`
- [ ] Dokumentovať, čo sa dá ďalej robiť s dátami
- [ ] Navrhnúť ďalšie kroky (napr. finetuning dataset)

---

## 📊 Očakávané Výstupy

### 1. Týždenné Témové Mapovanie
- **18 týždenných reportov** (W29-W49)
- Každý report obsahuje:
  - Dominantné témy
  - Kľúčové citácie
  - Štatistiky a trendy

### 2. Rozšírený RAG Systém
- Týždenné syntézy
- Tematické syntézy
- Automatické rozširovanie denných záznamov

### 3. HTML Dashboard
- Interaktívna vizualizácia dát
- Heat mapy, grafy, filtre
- Otvoríš v prehliadači

---

## 🔧 Technické Detaily

### Skripty na Vytvorenie

1. **`scripts/identify_weekly_themes.py`**
   - Vstup: Konverzačné páry (JSONL)
   - Výstup: Týždenné témy a reporty
   - Technológie: NLP (spaCy, NLTK alebo transformers)

2. **`scripts/extend_rag_system.py`**
   - Rozšírenie existujúceho RAG systému
   - Pridanie týždenných a tematických syntéz

3. **`scripts/generate_kortex_dashboard.py`**
   - Generovanie HTML dashboardu
   - Použitie: Plotly alebo Chart.js pre interaktívne grafy

---

## ⏱️ Časový Odhad

- **Fáza 1 (Týždenné témy):** 2-3 hodiny
- **Fáza 2 (RAG rozšírenie):** 1-2 hodiny
- **Fáza 3 (Dashboard):** 2-3 hodiny
- **Fáza 4 (Dokumentácia):** 30 min - 1 hodina

**Celkom:** ~6-9 hodín práce

---

## 📝 Poznámky

### Prečo NIE Grafana/Metabase?
- Overkill pre 1,822 konverzácií
- Setup a maintenance náročnosť
- Python + HTML je jednoduchšie a rýchlejšie
- Môžeš otvoriť v prehliadači bez databázy

### Prečo Týždenné Témové Mapovanie?
- **Praktická hodnota:** Vidíš, čo si riešil každý týždeň
- **Trendy:** Identifikuješ hlavné témy a ich vývoj
- **Kontext:** Lepšie pochopenie transformácie
- **Základ pre syntézy:** RAG môže použiť týždenné témy

### RAG Integrácia
- Namiesto len vyhľadávania → syntézy
- Namiesto len promptov → kompletný dialóg (prompt + odpoveď)
- Namiesto len dát → praktické využitie

---

## 🚀 Začiatok Session

1. Načítať tento plán: `xvadur/data/sessions/Stvrtok_2025-12-04_PLAN.md`
2. Prečítať `xvadur/save_games/SAVE_GAME_LATEST.md` pre kontext
3. Začať s Fázou 1: Týždenné Témové Mapovanie

---

**Vytvorené:** 2025-12-04 05:00  
**Status:** 📝 Pripravené na spustenie

