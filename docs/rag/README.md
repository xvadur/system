# 📚 RAG System - Rýchly Prehľad

RAG (Retrieval-Augmented Generation) systém pre vyhľadávanie v histórii promptov a conversation pairs.

---

## 🚀 Rýchly Start

```bash
# 1. Vytvorenie RAG indexu
python3 core/rag/build_rag_index.py

# 2. Základné vyhľadávanie
python3 core/rag/rag_agent_helper.py "tvoj dotaz" 5 0.4 true search None pretty

# 3. Syntetizovaná odpoveď
python3 core/rag/rag_agent_helper.py "tvoj dotaz" 10 0.4 true query None pretty
```

---

## 📖 Dokumentácia

- **[RAG_GUIDE.md](RAG_GUIDE.md)** - Kompletný návod:
  - Quick Start & Inštalácia
  - Rozšírené funkcie
  - Použitie a príklady
  - Advanced features (Hybrid Search)
  - Troubleshooting

---

## 📂 Štruktúra

```
core/
├── rag/
│   ├── build_rag_index.py      # Stavba RAG indexu
│   └── rag_agent_helper.py     # RAG search + syntéza

data/
└── rag_index/
    ├── faiss.index              # FAISS index
    ├── metadata.json            # Metadata chunkov
    └── chunks.json              # Text chunkov

docs/
└── rag/
    ├── README.md                # Tento súbor (rýchly prehľad)
    └── RAG_GUIDE.md             # Kompletný návod
```

---

## 🔗 Súvisiace Dokumenty

- **Architektúra:** [`docs/ARCHITECTURE.md`](../ARCHITECTURE.md) - RAG systém v celkovej architektúre
- **Memory System:** [`docs/MEMORY_AND_LOGGING.md`](../MEMORY_AND_LOGGING.md) - Integrácia s MinisterOfMemory

---

**Posledná aktualizácia:** 2025-12-09
