# 🔀 Hybrid Search: Kompletný Návod

## 📋 Prehľad

RAG systém teraz podporuje **hybrid search** - kombináciu semantic search (embeddings) a keyword search (TF-IDF). Toto výrazne zlepšuje presnosť vyhľadávania.

---

## 🎯 Ako to Funguje?

### 1. Semantic Search (Embeddings)
- Používa OpenAI embeddings (`text-embedding-3-small`)
- Nájde kontextovo podobné prompty
- Funguje dobre pre komplexné otázky

### 2. Keyword Search (TF-IDF)
- Používa TF-IDF (Term Frequency - Inverse Document Frequency)
- Nájde presné výskyty kľúčových slov
- Funguje dobre pre presné mená, dátumy, technické termíny

### 3. Hybrid Kombinácia
- Kombinuje oba výsledky pomocou váženého priemeru
- Default: 70% semantic + 30% keyword
- Vracia najrelevantnejšie výsledky

---

## 🚀 Použitie

### Automatické (Odporúčané)

Hybrid search je **predvolený režim**:

```bash
python3 xvadur_brave/scripts/rag_agent_helper.py "transformácia identity" 5 0.4
```

### Manuálne Nastavenie

```bash
# Hybrid search (default)
python3 xvadur_brave/scripts/rag_agent_helper.py "query" 5 0.4 true

# Len semantic search
python3 xvadur_brave/scripts/rag_agent_helper.py "query" 5 0.4 false
```

---

## 📊 Výstup Formát

```json
{
  "query": "transformácia identity",
  "search_type": "hybrid",
  "results_count": 5,
  "results": [
    {
      "rank": 1,
      "score": 0.85,
      "semantic_score": 0.82,
      "keyword_score": 0.91,
      "text": "...",
      "date": "2025-07-20",
      "search_type": "hybrid"
    }
  ]
}
```

---

## ⚙️ Parametre

### `semantic_weight` (default: 0.7)
Váha semantic search (0-1). Vyššia hodnota = viac dôrazu na kontextovú podobnosť.

### `keyword_weight` (default: 0.3)
Váha keyword search (0-1). Vyššia hodnota = viac dôrazu na presné výskyty.

### Príklady Nastavenia

**Pre komplexné otázky (viac semantic):**
```python
search_rag(query, semantic_weight=0.8, keyword_weight=0.2)
```

**Pre presné vyhľadávanie (viac keyword):**
```python
search_rag(query, semantic_weight=0.5, keyword_weight=0.5)
```

---

## 🔧 Technické Detaily

### TF-IDF Implementácia

```python
# Term Frequency (TF)
tf = počet_výskytov_slova_v_dokumente / celkový_počet_slov_v_dokumente

# Inverse Document Frequency (IDF)
idf = log(celkový_počet_dokumentov / počet_dokumentov_s_slovom)

# TF-IDF Score
score = tf * idf
```

### Hybrid Score Výpočet

```python
hybrid_score = (semantic_score * semantic_weight) + (keyword_score * keyword_weight)
```

---

## 📈 Výhody Hybrid Search

### 1. Lepšia Presnosť
- Semantic search nájde kontextovo podobné výsledky
- Keyword search nájde presné výskyty
- Kombinácia = najlepšie z oboch svetov

### 2. Flexibilita
- Funguje pre komplexné otázky (semantic)
- Funguje pre presné vyhľadávanie (keyword)
- Automaticky sa prispôsobí typu query

### 3. Lepšie Výsledky
- Menej falošných pozitív
- Viac relevantných výsledkov
- Lepšie ranking

---

## 🎯 Kedy Použiť Hybrid vs. Semantic?

### Hybrid Search (Odporúčané)
- ✅ Všetky otázky (default)
- ✅ Presné mená, dátumy
- ✅ Technické termíny
- ✅ Komplexné otázky

### Len Semantic Search
- ⚠️ Veľmi abstraktné otázky
- ⚠️ Keď keyword search nefunguje dobre
- ⚠️ Testovanie semantic search

---

## 🔄 Aktualizácia Indexu

TF-IDF index sa vytvára **automaticky** pri načítaní RAG indexu. Nie je potrebné ho vytvárať manuálne.

**Poznámka:** TF-IDF index sa vytvára v pamäti pri každom volaní. Pre veľké datasety by bolo lepšie ho uložiť do súboru (budúca vylepšenie).

---

## 📝 Príklady

### Príklad 1: Presné Meno

**Query:** "vlado recepčná"

**Semantic search:** Nájde prompty o recepčnej, ale možno nie presne o Vlado
**Keyword search:** Nájde presné výskyty "vlado" a "recepčná"
**Hybrid:** Kombinuje oboje → lepšie výsledky

### Príklad 2: Komplexná Otázka

**Query:** "ako som sa transformoval z sanitára na AI podnikateľa"

**Semantic search:** Nájde prompty o transformácii identity
**Keyword search:** Nájde výskyty "sanitár", "AI", "podnikateľ"
**Hybrid:** Kombinuje kontextovú podobnosť + presné výskyty

---

## 🚀 Ďalšie Vylepšenia (Budúcnosť)

1. **BM25 namiesto TF-IDF** - lepšie výsledky pre keyword search
2. **Caching TF-IDF indexu** - rýchlejšie načítanie
3. **Adaptívne váhy** - automatické nastavenie váh podľa typu query
4. **Query expansion** - automatické rozšírenie query

---

**Status:** ✅ Funkčný  
**Default:** Hybrid search (70% semantic, 30% keyword)  
**Performance:** ~1-2 sekundy (rovnako ako semantic search)

