# 📚 RAG Dokumentácia

Tento priečinok obsahuje dokumentáciu pre RAG (Retrieval-Augmented Generation) systém.

## 📖 Dokumenty

1. **[RAG_README.md](RAG_README.md)** - Základný prehľad RAG systému
2. **[RAG_CONVERSATION_GUIDE.md](RAG_CONVERSATION_GUIDE.md)** - Návod na konverzáciu s RAG
3. **[RAG_QUERY_SYNTHESIS.md](RAG_QUERY_SYNTHESIS.md)** - RAG Query s automatickou syntézou
4. **[RAG_AGENT_INTEGRATION.md](RAG_AGENT_INTEGRATION.md)** - Integrácia RAG do Cursor agenta
5. **[HYBRID_SEARCH_GUIDE.md](HYBRID_SEARCH_GUIDE.md)** - Hybrid Search (semantic + keyword)
6. **[KNOWLEDGE_GRAPH_GUIDE.md](KNOWLEDGE_GRAPH_GUIDE.md)** - Knowledge Graph a backlinking

## 🚀 Rýchly Start

```bash
# RAG Search
python3 xvadur_brave/scripts/rag_agent_helper.py "tvoj dotaz" 5 0.4

# RAG Query s syntézou
python3 xvadur_brave/scripts/rag_agent_helper.py "tvoj dotaz" 10 0.3 true query
```

## 📂 Štruktúra

```
xvadur_brave/
├── scripts/
│   ├── rag_agent_helper.py    # Hlavný RAG skript
│   ├── rag_search.py           # RAG search funkcie
│   └── build_rag_index.py     # Stavba RAG indexu
└── docs/
    └── rag/                    # RAG dokumentácia (tento priečinok)
        ├── README.md
        ├── RAG_README.md
        ├── RAG_CONVERSATION_GUIDE.md
        ├── RAG_QUERY_SYNTHESIS.md
        ├── RAG_AGENT_INTEGRATION.md
        ├── HYBRID_SEARCH_GUIDE.md
        └── KNOWLEDGE_GRAPH_GUIDE.md
```

---

**Poznámka:** Všetky markdown súbory boli presunuté z `scripts/` do `docs/rag/` pre lepšiu organizáciu.

