#!/usr/bin/env python3
"""
Vytvorí novú dennú session z template, vloží včerajší sumár
a prekopíruje ju do staging aj development vrstvy.
"""

import sys
from pathlib import Path
from datetime import date
import shutil

# Add workspace root to path
workspace_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(workspace_root))

from scripts.mcp_helpers import get_time_from_mcp

def create_new_session():
    """
    Hlavná funkcia pre vytvorenie novej session.
    1. Načíta template.
    2. Načíta včerajší sumár.
    3. Nahradí placeholdery v template.
    4. Uloží novú session do staging/today.
    5. Zkopíruje novú session do development/current.
    """
    template_path = workspace_root / "templates" / "session_template.md"
    staging_yesterday_summary_path = workspace_root / "staging" / "sessions" / "yesterday" / "summary.md"
    staging_today_path = workspace_root / "staging" / "sessions" / "today"
    dev_current_session_path = workspace_root / "development" / "sessions" / "current"
    
    staging_today_path.mkdir(exist_ok=True)
    dev_current_session_path.mkdir(exist_ok=True)
    
    if not template_path.exists():
        print(f"Chyba: Template {template_path} neexistuje.", file=sys.stderr)
        return

    # 1. Načítanie template
    template_content = template_path.read_text(encoding="utf-8")
    
    # 2. Načítanie včerajšieho sumáru
    summary_content = ""
    if staging_yesterday_summary_path.exists():
        summary_content = staging_yesterday_summary_path.read_text(encoding="utf-8")
    else:
        summary_content = "Včerajší sumár nebol nájdený."
        
    # 3. Nahradenie placeholderov
    today = date.today()
    current_time = get_time_from_mcp()
    
    session_content = template_content.replace("[Dátum]", today.strftime("%Y-%m-%d"))
    session_content = session_content.replace("[Názov]", "Nová Session") # Môže byť rozšírené
    session_content = session_content.replace("[YYYY-MM-DD]", today.strftime("%Y-%m-%d"))
    session_content = session_content.replace("[VČERAJŠÍ_SUMÁR]", summary_content)
    session_content = session_content.replace("[Timestamp]", current_time.isoformat())
    
    # 4. Uloženie do staging/today
    new_session_path_staging = staging_today_path / "session.md"
    new_session_path_staging.write_text(session_content, encoding="utf-8")
    print(f"✅ Nová session vytvorená v stagingu: {new_session_path_staging}")

    # 5. Kopírovanie do development/current
    new_session_path_dev = dev_current_session_path / "session.md"
    shutil.copy(str(new_session_path_staging), str(new_session_path_dev))
    print(f"✅ Nová session skopírovaná do developmentu: {new_session_path_dev}")

if __name__ == "__main__":
    create_new_session()
