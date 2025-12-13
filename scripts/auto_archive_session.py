#!/usr/bin/env python3
"""
Archivuje aktuálnu session z development/sessions/current/ 
do development/sessions/archive/YYYY-MM-DD.md
"""

import sys
from pathlib import Path
from datetime import date

# Add workspace root to path
workspace_root = Path(__file__).resolve().parent.parent

def archive_current_session():
    """
    Archivuje aktuálnu session.md do archive/YYYY-MM-DD.md
    """
    today = date.today()
    current_session_path = workspace_root / "development" / "sessions" / "current" / "session.md"
    archive_dir = workspace_root / "development" / "sessions" / "archive"
    archived_session_path = archive_dir / f"{today.strftime('%Y-%m-%d')}.md"
    
    if not current_session_path.exists():
        print(f"⚠️  Session neexistuje: {current_session_path}")
        return
    
    # Vytvor archive adresár ak neexistuje
    archive_dir.mkdir(parents=True, exist_ok=True)
    
    # Presuň session do archívu
    current_session_path.rename(archived_session_path)
    print(f"✅ Session archivovaná: {archived_session_path}")

if __name__ == "__main__":
    archive_current_session()
