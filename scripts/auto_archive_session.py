#!/usr/bin/env python3
"""
Archivuje aktuálnu session z development vrstvy do stagingu,
generuje sumár a metriky.
"""

import sys
import json
from pathlib import Path
from datetime import date
import shutil

# Add workspace root to path
workspace_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(workspace_root))

from scripts.mcp_helpers import (
    analyze_with_sequential_thinking,
    export_to_obsidian,
    get_time_from_mcp,
)
from scripts.calculate_daily_metrics import calculate_metrics_for_session

def archive_current_session():
    """
    Hlavná funkcia pre archiváciu session.
    1. Prečíta aktuálnu session.
    2. Vytvorí sumár pomocou MCP.
    3. Vypočíta metriky.
    4. Presunie session do staging/yesterday.
    5. Uloží sumár a metriky.
    6. Exportuje do Obsidianu.
    """
    dev_current_session_path = workspace_root / "development" / "sessions" / "current" / "session.md"
    staging_yesterday_path = workspace_root / "staging" / "sessions" / "yesterday"
    
    staging_yesterday_path.mkdir(exist_ok=True)
    
    if not dev_current_session_path.exists():
        print(f"Chyba: Súbor {dev_current_session_path} neexistuje.", file=sys.stderr)
        return

    # 1. Prečítanie obsahu session
    session_content = dev_current_session_path.read_text(encoding="utf-8")
    
    # 2. Vytvorenie sumáru pomocou MCP
    summary_prompt = f"Zosumarizuj nasledujúci session záznam:\n\n{session_content}"
    summary = analyze_with_sequential_thinking(summary_prompt)
    
    # 3. Vypočítanie metrík (bude implementované v calculate_daily_metrics.py)
    today = date.today()
    metrics = calculate_metrics_for_session(session_content, today)
    
    # 4. Presun session súboru
    archived_session_path = staging_yesterday_path / "session.md"
    shutil.move(str(dev_current_session_path), str(archived_session_path))
    
    # 5. Uloženie sumáru a metrík
    summary_path = staging_yesterday_path / "summary.md"
    summary_path.write_text(summary, encoding="utf-8")
    
    metrics_path = staging_yesterday_path / "metrics.json"
    with metrics_path.open("w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=4)
        
    print(f"✅ Session archivovaná do {archived_session_path}")
    print(f"✅ Sumár uložený do {summary_path}")
    print(f"✅ Metriky uložené do {metrics_path}")
    
    # 6. Export do Obsidianu
    obsidian_path = f"Sessions/Archive/{today.strftime('%Y-%m-%d')}_session.md"
    if export_to_obsidian(session_content, obsidian_path):
        print(f"✅ Session exportovaná do Obsidianu: {obsidian_path}")
    else:
        print("⚠️ Nepodarilo sa exportovať session do Obsidianu (MCP nie je dostupné).")

if __name__ == "__main__":
    archive_current_session()
