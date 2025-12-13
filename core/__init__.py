"""XVADUR Core - Hlavné moduly systému.

Tento balík obsahuje jadro XVADUR systému:
- xp: Gamifikácia a XP tracking (manuálne použitie)
"""

from core.xp.calculator import calculate_xp, update_xp_file

__all__ = [
    "calculate_xp",
    "update_xp_file",
]

__version__ = "2.0.0"

