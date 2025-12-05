#!/usr/bin/env python3
"""
Generuje denný review na základe včerajšieho sumáru a metrík.
"""

import sys
import json
from pathlib import Path

# Add workspace root to path
workspace_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(workspace_root))

from scripts.mcp_helpers import (
    analyze_with_sequential_thinking,
    export_to_obsidian,
    get_time_from_mcp
)
from scripts.utils.log_manager import add_log_entry # Import novej funkcie

def generate_daily_review():
    """
    Hlavná funkcia pre generovanie denného review.
    1. Načíta včerajší sumár a metriky.
    2. Vygeneruje text review pomocou Sequential Thinking MCP.
    3. Uloží review do staging/review.
    4. Exportuje do Obsidianu.
    """
    add_log_entry(
        action_name="Spustenie generovania denného review",
        status="Started",
    )

    staging_yesterday_path = workspace_root / "staging" / "sessions" / "yesterday"
    summary_path = staging_yesterday_path / "summary.md"
    metrics_path = staging_yesterday_path / "metrics.json"
    review_path = workspace_root / "staging" / "review" / "daily_review.md"
    
    review_path.parent.mkdir(exist_ok=True)
    
    summary = ""
    if summary_path.exists():
        summary = summary_path.read_text(encoding="utf-8")
        
    metrics = {}
    if metrics_path.exists():
        with metrics_path.open("r", encoding="utf-8") as f:
            metrics = json.load(f)
            
    if not summary and not metrics:
        add_log_entry(
            action_name="Generovanie denného review",
            status="Failed",
            files_changed=[str(summary_path), str(metrics_path)],
            xp_estimate=0.0
        )
        print("Chyba: Neboli nájdené dáta z včerajšieho dňa.", file=sys.stderr)
        return

    # 2. Generovanie review
    review_prompt = f"""
    Vytvor denný review pre Adama na základe nasledujúcich dát:

    Včerajší sumár:
    ---
    {summary}
    ---

    Včerajšie metriky:
    ---
    {json.dumps(metrics, indent=2)}
    ---

    Štruktúra review:
    1.  **Včerajší Deň v Kocke:** Krátky sumár úspechov a kľúčových bodov.
    2.  **Metriky:** Prehľad XP, promptov a času.
    3.  **Odporúčania na Dnes:** 1-2 konkrétne, akčné odporúčania.
    """
    
    review_content = analyze_with_sequential_thinking(review_prompt)
    
    # Pridanie hlavičky
    today_str = get_time_from_mcp().strftime("%Y-%m-%d")
    final_review_content = f"# 🌅 Denný Review: {today_str}\n\n{review_content}"
    
    # 3. Uloženie review
    review_path.write_text(final_review_content, encoding="utf-8")
    print(f"✅ Denný review uložený do: {review_path}")
    
    # 4. Export do Obsidianu
    obsidian_path = f"Reviews/{today_str}_daily_review.md"
    if export_to_obsidian(final_review_content, obsidian_path):
        print(f"✅ Review exportovaný do Obsidianu: {obsidian_path}")
    else:
        print("⚠️ Nepodarilo sa exportovať review do Obsidianu (MCP nie je dostupné).")

    add_log_entry(
        action_name="Generovanie denného review",
        status="Completed",
        files_changed=[str(review_path)],
        xp_estimate=2.0 # Príklad hodnoty XP
    )

if __name__ == "__main__":
    generate_daily_review()
