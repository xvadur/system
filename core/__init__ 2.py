"""XVADUR Core - Hlavné moduly systému.

Tento balík obsahuje jadro XVADUR systému:
- ministers: Memory management (MinisterOfMemory, FileStore)
- rag: Retrieval-Augmented Generation systém
- xp: Gamifikácia a XP tracking
"""

from core.ministers import MinisterOfMemory, AssistantOfMemory, FileStore, MemoryRecord
from core.xp.calculator import calculate_xp, update_xp_file

__all__ = [
    "MinisterOfMemory",
    "AssistantOfMemory", 
    "FileStore",
    "MemoryRecord",
    "calculate_xp",
    "update_xp_file",
]

__version__ = "2.0.0"

