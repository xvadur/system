"""XVADUR RAG - Retrieval-Augmented Generation systém.

Poskytuje:
- Semantic search pomocou FAISS
- Hybrid search (semantic + keyword)
- Content type filtering
"""

__all__ = [
    "build_index",
    "search",
]

