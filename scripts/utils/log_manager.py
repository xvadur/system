"""
Log Manager - Dual-write systém pre XVADUR logging

Zapisuje súčasne do:
- XVADUR_LOG.md (Markdown pre človeka)
- XVADUR_LOG.jsonl (JSON pre AI - token-efektívne)

Použitie:
    from scripts.utils.log_manager import add_log_entry
    add_log_entry("Názov akcie", "completed", files_changed=["file.py"])
"""

import sys
import json
from pathlib import Path
from datetime import datetime
from typing import List, Optional, Dict, Any

# Add workspace root to path
workspace_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(workspace_root))

# Cesty k log súborom
LOG_MD_PATH = workspace_root / "development" / "logs" / "XVADUR_LOG.md"
LOG_JSONL_PATH = workspace_root / "development" / "logs" / "XVADUR_LOG.jsonl"


def add_log_entry(
    action_name: str, 
    status: str, 
    files_changed: Optional[List[str]] = None, 
    xp_estimate: Optional[float] = None,
    entry_type: str = "task",
    completed: Optional[List[str]] = None,
    results: Optional[Dict[str, Any]] = None,
    decisions: Optional[List[str]] = None,
    quest_id: Optional[int] = None
):
    """Pridá nový záznam do XVADUR_LOG.md a XVADUR_LOG.jsonl (dual-write).

    Args:
        action_name: Názov akcie (napr. "Implementácia session rotationu").
        status: Status akcie (napr. "started", "completed", "in_progress").
        files_changed: Zoznam zmienených súborov (voliteľné).
        xp_estimate: Odhad XP za dokončenie akcie (voliteľné).
        entry_type: Typ záznamu ("task", "session", "quest_created", "quest_closed", "analysis", "savegame").
        completed: Zoznam dokončených položiek (voliteľné).
        results: Slovník s výsledkami (voliteľné).
        decisions: Zoznam kľúčových rozhodnutí (voliteľné).
        quest_id: ID GitHub Issue (voliteľné).
    """
    now = datetime.now()
    current_time = now.strftime('%H:%M')
    current_date = now.strftime('%Y-%m-%d')
    iso_timestamp = now.isoformat()

    # === 1. MARKDOWN ZÁZNAM ===
    _write_markdown_entry(action_name, status, files_changed, xp_estimate, current_time)

    # === 2. JSONL ZÁZNAM ===
    _write_jsonl_entry(
        action_name=action_name,
        status=status,
        files_changed=files_changed,
        xp_estimate=xp_estimate,
        entry_type=entry_type,
        completed=completed,
        results=results,
        decisions=decisions,
        quest_id=quest_id,
        current_time=current_time,
        current_date=current_date,
        iso_timestamp=iso_timestamp
    )


def _write_markdown_entry(
    action_name: str, 
    status: str, 
    files_changed: Optional[List[str]], 
    xp_estimate: Optional[float],
    current_time: str
):
    """Zapíše záznam do Markdown logu."""
    log_entry = f"[{current_time}] 🔹 {action_name}\n"
    if files_changed:
        log_entry += "  - *Zmenené súbory:*\n"
        for f in files_changed:
            log_entry += f"    - {f}\n"
    log_entry += f"  - *Status:* {status}\n"
    if xp_estimate is not None:
        log_entry += f"  - *XP:* {xp_estimate}\n"

    try:
        # Načítaj existujúci obsah
        if LOG_MD_PATH.exists():
            content = LOG_MD_PATH.read_text(encoding='utf-8')
        else:
            content = "# 🧠 XVADUR LOG\n\n**Účel:** Záznam vykonanej práce a zmien v projekte\n\n---\n"
        
        # Nájdi pozíciu po hlavičke (po prvom "---")
        if "---" in content:
            parts = content.split("---", 1)
            new_content = parts[0] + "---\n" + log_entry + "\n" + parts[1] if len(parts) > 1 else parts[0] + "---\n" + log_entry
        else:
            new_content = content + "\n" + log_entry
        
        LOG_MD_PATH.write_text(new_content, encoding='utf-8')
    except Exception as e:
        print(f"Error writing to XVADUR_LOG.md: {e}", file=sys.stderr)


def _write_jsonl_entry(
    action_name: str,
    status: str,
    files_changed: Optional[List[str]],
    xp_estimate: Optional[float],
    entry_type: str,
    completed: Optional[List[str]],
    results: Optional[Dict[str, Any]],
    decisions: Optional[List[str]],
    quest_id: Optional[int],
    current_time: str,
    current_date: str,
    iso_timestamp: str
):
    """Zapíše záznam do JSONL logu."""
    # Vytvor JSON objekt
    entry = {
        "timestamp": iso_timestamp,
        "date": current_date,
        "time": current_time,
        "title": action_name,
        "type": entry_type,
        "status": status
    }
    
    # Pridaj voliteľné polia len ak existujú
    if files_changed:
        entry["files_changed"] = files_changed
    if xp_estimate is not None:
        entry["xp_estimate"] = xp_estimate
    if completed:
        entry["completed"] = completed
    if results:
        entry["results"] = results
    if decisions:
        entry["decisions"] = decisions
    if quest_id is not None:
        entry["quest_id"] = quest_id

    try:
        # Append do JSONL súboru
        with open(LOG_JSONL_PATH, 'a', encoding='utf-8') as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    except Exception as e:
        print(f"Error writing to XVADUR_LOG.jsonl: {e}", file=sys.stderr)


def get_recent_log_entries(limit: int = 5) -> List[Dict[str, Any]]:
    """Načíta posledných N záznamov z JSONL logu.
    
    Args:
        limit: Počet záznamov na načítanie (default: 5)
    
    Returns:
        Zoznam posledných N log záznamov
    """
    if not LOG_JSONL_PATH.exists():
        return []
    
    entries = []
    try:
        with open(LOG_JSONL_PATH, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    entries.append(json.loads(line))
        return entries[-limit:]
    except Exception as e:
        print(f"Error reading XVADUR_LOG.jsonl: {e}", file=sys.stderr)
        return []


if __name__ == "__main__":
    # Príklad použitia dual-write
    add_log_entry(
        action_name="Test dual-write systému",
        status="completed",
        files_changed=["scripts/utils/log_manager.py"],
        xp_estimate=2.0,
        entry_type="task",
        completed=["Implementácia dual-write", "Pridanie JSONL podpory"],
        results={"md_write": "OK", "jsonl_write": "OK"}
    )
    print("✅ Dual-write test: Záznam pridaný do MD aj JSONL")
    
    # Ukáž posledné záznamy
    recent = get_recent_log_entries(3)
    print(f"\n📋 Posledné 3 záznamy z JSONL:")
    for entry in recent:
        print(f"  - [{entry.get('time')}] {entry.get('title')}")
