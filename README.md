# 🧠 XVADUR Workspace

**Čistý workspace pre XVADUR systém s RAG integráciou**

Tento workspace obsahuje izolovanú verziu XVADUR systému - filozofický, reflexívny a kreatívny konverzačný režim pre dokumentáciu transformácie s plnou RAG podporou.

---

## 📁 Štruktúra

```
xvadur-workspace/
├── xvadur/                    # Hlavná vrstva - XVADUR systém
│   ├── config/                # Konfigurácia (xvadur_command.md)
│   ├── data/                  # Dáta (metrics, sessions, synthesis)
│   ├── docs/                  # Dokumentácia
│   ├── logs/                  # Logy (XVADUR_LOG.md, XVADUR_XP.md)
│   ├── scripts/               # Skripty (backlinking, visualizations)
│   └── +/                     # Analýzy a poznámky
│
├── data/                      # RAG dáta
│   ├── rag_index/             # FAISS index (faiss.index, chunks.json, metadata.json)
│   └── prompts/               # Zdrojové prompty
│       └── prompts_split/     # 664 JSON súborov
│
├── scripts/                   # RAG skripty
│   └── rag/
│       ├── rag_agent_helper.py    # RAG helper pre Cursor agenta
│       ├── rag_search.py           # RAG search funkcie
│       └── build_rag_index.py      # Stavba RAG indexu
│
├── docs/                      # Dokumentácia
│   └── rag/                   # RAG dokumentácia
│
├── mcp/                       # MCP server (voliteľné)
│   └── obsidian_mcp_server.py
│
├── .cursor/                   # Cursor rules
│   └── rules/
│
├── .cursorrules               # Globálny systémový prompt
├── .gitignore                 # Git ignore
├── requirements.txt           # Python dependencies
└── README.md                  # Tento súbor
```

---

## 🚀 Rýchly Štart

### 1. Inštalácia závislostí

```bash
# Vytvorenie virtuálneho prostredia
python3 -m venv .venv
source .venv/bin/activate  # Na Mac/Linux
# alebo: .venv\Scripts\activate  # Na Windows

# Inštalácia dependencies
pip install -r requirements.txt
```

### 2. Nastavenie API kľúčov

Vytvor `.env` súbor v root adresári:

```bash
OPENAI_API_KEY=sk-tvoj-api-key
```

### 3. Testovanie RAG

```bash
# RAG Search
python3 scripts/rag/rag_agent_helper.py "tvoj dotaz" 5 0.4

# RAG Query s syntézou
python3 scripts/rag/rag_agent_helper.py "tvoj dotaz" 10 0.3 true query
```

### 4. Použitie v Cursor

Workspace je pripravený na prácu v Cursor IDE:
- `.cursorrules` - globálny systémový prompt
- `.cursor/rules/` - špecifické pravidlá
- RAG skripty sú pripravené na volanie z Cursor agenta

---

## 🧠 XVADUR Systém

XVADUR je filozofický, reflexívny a kreatívny konverzačný režim pre dokumentáciu transformácie.

### Funkcie:
- **Dokumentácia transformácie** - analytický spôsob, objektívne, bez obalu
- **RAG integrácia** - automatické citovanie relevantných pasáží z histórie
- **Backlinking** - automatické vytváranie `[[]]` linkov v Obsidian vaultu
- **XP tracking** - vlastný XP tracking systém
- **Vizualizácie** - ASCII grafy a heatmapy

### Použitie:

V Cursor použij command `/xvadur` alebo začni konverzáciu s `@xvadur`.

---

## 📊 RAG Systém

RAG (Retrieval-Augmented Generation) systém umožňuje vyhľadávanie v histórii 664 promptov.

### Dáta:
- **664 promptov** → **1,204 chunkov**
- **FAISS index** (lokálne, rýchle)
- **OpenAI embeddings** (`text-embedding-3-small`, 1536 dimenzií)

### Funkcie:
- **Semantic search** - vyhľadávanie podľa významu
- **Keyword search** - vyhľadávanie podľa kľúčových slov
- **Hybrid search** - kombinácia semantic + keyword
- **Query synthesis** - automatická syntéza odpovedí z promptov

### Rebuild RAG indexu:

```bash
python3 scripts/rag/build_rag_index.py
```

**Poznámka:** Rebuild trvá ~5-10 minút a stojí ~$5-10 (pre 664 promptov).

---

## 🔧 Konfigurácia

### Cesty v skriptoch:

Všetky cesty sú relatívne k root adresáru workspace:
- `data/rag_index/` - RAG index
- `data/prompts/prompts_split/` - Zdrojové prompty
- `.env` - Environment premenné

### Cursor Rules:

- `.cursorrules` - globálny systémový prompt
- `.cursor/rules/` - špecifické pravidlá pre rôzne aspekty

---

## 📝 Poznámky

- **Súčasný workspace** (`Magnum Opus`) zostáva pre Chat UI a dataset
- **Tento workspace** je izolovaný pre XVADUR systém a RAG
- **Obsidian vault** zostáva lokálne (necommituje sa)

---

## 🎯 Ďalšie Kroky

1. **Git inicializácia:**
   ```bash
   git init
   git add .
   git commit -m "feat: Initial XVADUR workspace"
   ```

2. **GitHub push:**
   ```bash
   git remote add origin https://github.com/tvoj-username/xvadur-workspace.git
   git push -u origin main
   ```

3. **Testovanie:**
   - Test RAG search
   - Test XVADUR skripty
   - Test Cursor rules

---

**Vytvorené:** 2025-12-01  
**Status:** ✅ Funkčný, pripravený na prácu






