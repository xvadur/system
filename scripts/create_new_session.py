#!/usr/bin/env python3
"""
Vytvorí novú dennú session z template.
"""

import sys
from pathlib import Path
from datetime import datetime, timezone

# Add workspace root to path
workspace_root = Path(__file__).resolve().parent.parent

def create_new_session():
    """
    Vytvorí novú prázdnu session.md v development/sessions/current/
    Používa template z templates/session_template.md
    """
    today = datetime.now(timezone.utc)
    session_path = workspace_root / "development" / "sessions" / "current" / "session.md"
    template_path = workspace_root / "templates" / "session_template.md"
    
    # Vytvor adresár ak neexistuje
    session_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Načítaj template
    if template_path.exists():
        template_content = template_path.read_text(encoding="utf-8")
        
        # Nahraď placeholdery
        session_content = template_content.replace("[YYYY-MM-DD]", today.strftime('%Y-%m-%d'))
        session_content = session_content.replace("[YYYY-MM-DD HH:MM]", today.strftime('%Y-%m-%d %H:%M'))
        
        # Odstráň príklady z template (riadky s [HH:MM], [Task], atď.)
        lines = session_content.split('\n')
        cleaned_lines = []
        for line in lines:
            # Preskoč príklady v Tasks sekcii
            if line.strip().startswith('- [HH:MM]') or line.strip() == '- [cesta/k/súboru.py]':
                continue
            # Preskoč príklady v Notes sekcii
            if line.strip() == '- [Technické poznámky]':
                cleaned_lines.append('- ')
                continue
            cleaned_lines.append(line)
        
        session_content = '\n'.join(cleaned_lines)
    else:
        # Fallback: jednoduchý template ak template neexistuje
        session_content = f"""# Session: {today.strftime('%Y-%m-%d')}

**Účel:** Denný záznam práce a úloh

---

## Tasks

- 

---

## Notes

- 

---

## Files Changed

- 

---

**Vytvorené:** {today.strftime('%Y-%m-%d %H:%M')}  
**Posledná aktualizácia:** {today.strftime('%Y-%m-%d %H:%M')}  
**Status:** Aktívna
"""
    
    session_path.write_text(session_content, encoding="utf-8")
    print(f"✅ Nová session vytvorená: {session_path}")
    print(f"   Template použité: {template_path if template_path.exists() else 'fallback'}")

if __name__ == "__main__":
    create_new_session()
