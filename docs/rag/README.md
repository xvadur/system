# 📚 RAG Dokumentácia

Tento priečinok obsahuje dokumentáciu pre RAG (Retrieval-Augmented Generation) systém.

## 📖 Dokumenty

- **[RAG_GUIDE.md](RAG_GUIDE.md)** - Kompletný návod na RAG systém (Quick Start, Rozšírené Funkcie, Použitie, Advanced Features, Troubleshooting)

## 🚀 Rýchly Start

```bash
# Vytvorenie RAG indexu
python3 scripts/rag/build_rag_index.py

# Základné vyhľadávanie (pekný výstup)
python3 scripts/rag/rag_agent_helper.py "tvoj dotaz" 5 0.4 true search None pretty

# Syntetizovaná odpoveď
python3 scripts/rag/rag_agent_helper.py "tvoj dotaz" 10 0.4 true query None pretty
```

## 📂 Štruktúra

```
scripts/
├── rag/
│   ├── build_rag_index.py    # Stavba RAG indexu
│   └── rag_agent_helper.py   # RAG search + syntéza (kompletný nástroj)
└── docs/
    └── rag/                   # RAG dokumentácia (tento priečinok)
        ├── README.md
        └── RAG_GUIDE.md       # Kompletný návod
```

---

**Poznámka:** Všetky markdown dokumentačné súbory boli konsolidované do jedného `RAG_GUIDE.md` pre lepšiu organizáciu a jednoduchšie používanie.
