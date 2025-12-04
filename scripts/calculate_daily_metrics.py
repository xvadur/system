#!/usr/bin/env python3
"""
Vypočíta denné metriky pre danú session.
"""

import sys
from pathlib import Path
from datetime import date, datetime
import json

# Add workspace root to path
workspace_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(workspace_root))

from scripts.mcp_helpers import get_time_from_mcp

def calculate_metrics_for_session(session_content: str, session_date: date) -> dict:
    """
    Vypočíta metriky pre daný session obsah a dátum.
    
    Metriky:
    - Počet promptov (z `development/data/prompts_log.jsonl`)
    - XP získané (z `development/logs/XVADUR_XP.md`)
    - Čas práce (odhad z logov)
    """
    
    # Placeholder implementácia - reálna by parsovala logy
    
    prompts_log_path = workspace_root / "development" / "data" / "prompts_log.jsonl"
    prompt_count = 0
    if prompts_log_path.exists():
        with prompts_log_path.open("r", encoding="utf-8") as f:
            for line in f:
                try:
                    prompt_data = json.loads(line)
                    saved_at_str = prompt_data.get("metadata", {}).get("saved_at")
                    if saved_at_str:
                        saved_at = datetime.fromisoformat(saved_at_str).date()
                        if saved_at == session_date:
                            prompt_count += 1
                except json.JSONDecodeError:
                    continue

    return {
        "date": session_date.isoformat(),
        "prompt_count": prompt_count,
        "xp_earned": 150, # Placeholder
        "work_time_minutes": 240, # Placeholder
        "calculated_at": get_time_from_mcp().isoformat(),
    }

if __name__ == "__main__":
    # Príklad použitia
    today = date.today()
    # Tento skript by normálne bol volaný z iného procesu,
    # ale pre testovanie môžeme vytvoriť fiktívny obsah.
    fake_session_content = "Dnes som pracoval na XYZ."
    metrics = calculate_metrics_for_session(fake_session_content, today)
    print(json.dumps(metrics, indent=4))
