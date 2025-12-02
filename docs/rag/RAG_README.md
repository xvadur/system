# 🧠 RAG System - Quick Start Guide

## 📋 Požiadavky

### 1. Inštalácia knižníc

```bash
pip install faiss-cpu numpy openai
```

**Poznámka:** Ak máš problém s `faiss-cpu`, skús:
```bash
pip install faiss-cpu --no-cache-dir
```

### 2. OpenAI API Key

Nastav environment premennú:
```bash
export OPENAI_API_KEY='sk-tvoj-api-key'
```

Alebo vytvor `.env` súbor v root adresári:
```
OPENAI_API_KEY=sk-tvoj-api-key
```

## 🚀 Použitie

### Krok 1: Vytvorenie RAG indexu

```bash
cd "/Users/_xvadur/Desktop/Magnum Opus"
python3 xvadur_brave/scripts/build_rag_index.py
```

**Čo sa stane:**
- Načíta všetky prompty z `prompts_clean/prompts_split`
- Vytvorí inteligentné chunky
- Generuje embeddings pomocou OpenAI
- Vytvorí FAISS index
- Uloží metadata a chunks

**Čas:** ~5-10 minút (závisí od počtu promptov)
**Náklady:** ~$5-10 (pre ~664 promptov)

### Krok 2: Vyhľadávanie

```bash
python3 xvadur_brave/scripts/rag_search.py "tvoj dotaz" [top_k]
```

**Príklady:**
```bash
# Základné vyhľadávanie (top 5 výsledkov)
python3 xvadur_brave/scripts/rag_search.py "ako som riešil n8n problémy"

# Viac výsledkov
python3 xvadur_brave/scripts/rag_search.py "transformácia identity" 10
```

## 📊 Výstup

Index sa vytvorí v:
- `xvadur_brave/data/rag_index/faiss.index` - FAISS index
- `xvadur_brave/data/rag_index/metadata.json` - Metadata pre každý chunk
- `xvadur_brave/data/rag_index/chunks.json` - Text chunkov

## 🔧 Troubleshooting

### Chyba: "ModuleNotFoundError: No module named 'faiss'"
```bash
pip install faiss-cpu numpy
```

### Chyba: "OPENAI_API_KEY nie je nastavený"
```bash
export OPENAI_API_KEY='sk-tvoj-key'
```

### Chyba: "Index neexistuje"
Spusti najprv `build_rag_index.py`

## 📈 Ďalšie kroky

Po úspešnom vytvorení indexu môžeš:
1. Integrovať do Cursor agenta
2. Pridať ďalšie dátové zdroje (chronológie, Obsidian)
3. Implementovať hybrid search (semantic + keyword)
4. Pridať prioritizáciu (hot/warm/cold memory)

