"""XVADUR XP - Gamifikácia a progression systém.

Poskytuje:
- Automatický výpočet XP z logu a promptov
- Level systém s exponenciálnym rastom
- Streak tracking
"""

from core.xp.calculator import calculate_xp, update_xp_file

__all__ = [
    "calculate_xp",
    "update_xp_file",
]

