#!/usr/bin/env python3
"""
Migračný skript pre konverziu Markdown kontextových súborov do štrukturovaných JSON formátov.

Účel: Optimalizovať token spotrebu pri /loadgame a /savegame commands.

Použitie:
    python scripts/migrate_to_structured_format.py [--dry-run] [--backup]
"""

import json
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any
import sys

# Pridaj workspace root do path
workspace_root = Path(__file__).parent.parent
sys.path.insert(0, str(workspace_root))


def parse_log_entry(markdown_content: str) -> Optional[Dict[str, Any]]:
    """
    Parsuje jeden log entry z Markdown formátu do JSON.
    
    Formát:
    ## [YYYY-MM-DD HH:MM] 🔹 Title
    
    **Vykonané:**
    - ✅ Item 1
    - ✅ Item 2
    
    **Hlavné Výsledky:**
    - **Key:** Value
    
    **Zmeny v súboroch:**
    - `path/to/file` - description
    """
    lines = markdown_content.strip().split('\n')
    
    # Extrahuj dátum a čas z hlavičky
    header_match = re.match(r'## \[(\d{4}-\d{2}-\d{2})(?:\s+(\d{2}:\d{2}))?\]\s*🔹\s*(.+)', lines[0])
    if not header_match:
        return None
    
    date = header_match.group(1)
    time = header_match.group(2) or "00:00"
    title = header_match.group(3).strip()
    
    # Vytvor timestamp
    timestamp = f"{date}T{time}:00Z"
    
    entry = {
        "timestamp": timestamp,
        "date": date,
        "time": time,
        "title": title,
        "type": "session" if "Session:" in title else "task",
        "completed": [],
        "results": {},
        "decisions": [],
        "files_changed": [],
        "status": "completed",
        "xp_estimate": 0.0
    }
    
    # Parsuj sekcie
    current_section = None
    for line in lines[1:]:
        line = line.strip()
        if not line:
            continue
        
        # Detekuj sekcie
        if line.startswith("**Vykonané:**"):
            current_section = "completed"
        elif line.startswith("**Hlavné Výsledky:**"):
            current_section = "results"
        elif line.startswith("**Kľúčové rozhodnutia:**"):
            current_section = "decisions"
        elif line.startswith("**Zmeny v súboroch:**"):
            current_section = "files_changed"
        elif line.startswith("**Status:**"):
            current_section = "status"
        elif line.startswith("- ✅"):
            # Completed item
            item = line.replace("- ✅", "").strip()
            if item:
                entry["completed"].append(item)
        elif line.startswith("- **"):
            # Result item (key: value)
            match = re.match(r'- \*\*(.+?):\*\*\s*(.+)', line)
            if match:
                key = match.group(1).lower().replace(" ", "_")
                value = match.group(2).strip()
                entry["results"][key] = value
        elif line.startswith("- "):
            # Decision item
            item = line.replace("- ", "").strip()
            if item and current_section == "decisions":
                entry["decisions"].append(item)
        elif line.startswith("`") and current_section == "files_changed":
            # File change item: `path` - description
            match = re.match(r'`(.+?)`\s*-\s*(.+)', line)
            if match:
                path = match.group(1)
                desc = match.group(2).strip()
                action = "updated"
                if "nový" in desc.lower() or "vytvorený" in desc.lower():
                    action = "created"
                elif "odstránený" in desc.lower():
                    action = "deleted"
                
                entry["files_changed"].append({
                    "path": path,
                    "action": action,
                    "desc": desc
                })
    
    return entry


def parse_save_game(markdown_content: str) -> Dict[str, Any]:
    """
    Parsuje Save Game Markdown do JSON formátu.
    """
    lines = markdown_content.split('\n')
    
    save_game = {
        "metadata": {
            "created_at": datetime.now().isoformat() + "Z",
            "session_date": "",
            "session_name": ""
        },
        "status": {
            "rank": "",
            "level": 1,
            "xp": 0.0,
            "xp_next_level": 10.0,
            "xp_percent": 0.0,
            "streak_days": 0
        },
        "narrative": {
            "summary": "",
            "key_decisions": [],
            "key_moments": [],
            "tools_created": [],
            "open_loops": []
        },
        "quests": [],
        "instructions": {
            "for_agent": [],
            "style": []
        }
    }
    
    current_section = None
    narrative_lines = []
    
    for i, line in enumerate(lines):
        line = line.strip()
        
        # Detekuj sekcie
        if line.startswith("# 💾 SAVE GAME:"):
            date_match = re.search(r'(\d{4}-\d{2}-\d{2})', line)
            if date_match:
                save_game["metadata"]["session_date"] = date_match.group(1)
        elif line.startswith("## 📊 Status"):
            current_section = "status"
        elif line.startswith("## 🧠 Naratívny Kontext"):
            current_section = "narrative"
        elif line.startswith("## 🎯 Aktívne Questy"):
            current_section = "quests"
        elif line.startswith("## ⚠️ Inštrukcie pre Nového Agenta"):
            current_section = "instructions"
        elif line.startswith("**Rank:**"):
            save_game["status"]["rank"] = line.split("**Rank:**")[1].strip()
        elif line.startswith("**Level:**"):
            level_match = re.search(r'(\d+)', line)
            if level_match:
                save_game["status"]["level"] = int(level_match.group(1))
        elif line.startswith("**XP:**"):
            xp_match = re.search(r'(\d+\.?\d*)\s*/\s*(\d+\.?\d*)', line)
            if xp_match:
                save_game["status"]["xp"] = float(xp_match.group(1))
                save_game["status"]["xp_next_level"] = float(xp_match.group(2))
        elif line.startswith("**Streak:**"):
            streak_match = re.search(r'(\d+)', line)
            if streak_match:
                save_game["status"]["streak_days"] = int(streak_match.group(1))
        elif current_section == "narrative" and line and not line.startswith("#"):
            narrative_lines.append(line)
        elif line.startswith("### ") and current_section == "quests":
            # Quest title
            quest_title = line.replace("### ", "").strip()
            save_game["quests"].append({
                "id": quest_title.lower().replace(" ", "-"),
                "title": quest_title,
                "status": "new",
                "next_steps": [],
                "blockers": []
            })
        elif line.startswith("- **Status:**") and save_game["quests"]:
            status_match = re.search(r'([🆕✅⏳❌])', line)
            if status_match:
                emoji = status_match.group(1)
                status_map = {"🆕": "new", "✅": "completed", "⏳": "in_progress", "❌": "blocked"}
                save_game["quests"][-1]["status"] = status_map.get(emoji, "new")
        elif line.startswith("- **Next Steps:**") and save_game["quests"]:
            current_section = "quest_next_steps"
        elif current_section == "quest_next_steps" and line.startswith("  "):
            step = line.strip()
            if step:
                save_game["quests"][-1]["next_steps"].append(step)
    
    # Zlúč narrative lines
    save_game["narrative"]["summary"] = " ".join(narrative_lines[:500])  # Limit na 500 slov
    
    return save_game


def parse_xp_status(markdown_content: str) -> Dict[str, Any]:
    """
    Parsuje XP Status Markdown do JSON formátu.
    """
    lines = markdown_content.split('\n')
    
    xp_data = {
        "timestamp": datetime.now().isoformat() + "Z",
        "status": {
            "total_xp": 0.0,
            "level": 1,
            "next_level_xp": 10.0,
            "xp_needed": 10.0,
            "xp_percent": 0.0,
            "streak_days": 0
        },
        "breakdown": {
            "from_work": {
                "entries": {"count": 0, "xp_per_entry": 0.5, "total": 0.0},
                "files_changed": {"count": 0, "xp_per_file": 0.1, "total": 0.0},
                "tasks_completed": {"count": 0, "xp_per_task": 0.5, "total": 0.0},
                "subtotal": 0.0
            },
            "from_activity": {
                "prompts": {"count": 0, "xp_per_prompt": 0.1, "total": 0.0},
                "word_count": {"count": 0, "xp_per_1000_words": 0.5, "total": 0.0},
                "subtotal": 0.0
            },
            "bonuses": {
                "streak": {"days": 0, "xp_per_day": 0.2, "total": 0.0},
                "sessions": {"count": 0, "xp_per_session": 1.0, "total": 0.0},
                "subtotal": 0.0
            }
        },
        "total": 0.0
    }
    
    current_section = None
    
    for line in lines:
        line = line.strip()
        
        if "**Celkové XP:**" in line:
            xp_match = re.search(r'(\d+\.?\d*)', line)
            if xp_match:
                xp_data["status"]["total_xp"] = float(xp_match.group(1))
        elif "**Level:**" in line:
            level_match = re.search(r'(\d+)', line)
            if level_match:
                xp_data["status"]["level"] = int(level_match.group(1))
        elif "**Next Level:**" in line:
            xp_match = re.search(r'(\d+\.?\d*)', line)
            if xp_match:
                xp_data["status"]["next_level_xp"] = float(xp_match.group(1))
        elif "**Streak:**" in line:
            streak_match = re.search(r'(\d+)', line)
            if streak_match:
                xp_data["status"]["streak_days"] = int(streak_match.group(1))
    
    return xp_data


def migrate_log_file(md_path: Path, jsonl_path: Path, dry_run: bool = False) -> int:
    """
    Migruje log Markdown súbor do JSONL formátu.
    """
    if not md_path.exists():
        print(f"⚠️  Log súbor neexistuje: {md_path}")
        return 0
    
    content = md_path.read_text(encoding='utf-8')
    
    # Rozdel na záznamy (každý začína s ## [YYYY-MM-DD])
    entries = re.split(r'\n## \[', content)
    
    jsonl_entries = []
    for i, entry in enumerate(entries):
        if i == 0:
            # Prvý záznam môže mať hlavičku súboru
            if not entry.strip().startswith("##"):
                continue
        else:
            # Pridaj späť ## [
            entry = "## [" + entry
        
        parsed = parse_log_entry(entry)
        if parsed:
            jsonl_entries.append(parsed)
    
    if not dry_run:
        jsonl_path.parent.mkdir(parents=True, exist_ok=True)
        with jsonl_path.open('w', encoding='utf-8') as f:
            for entry in jsonl_entries:
                f.write(json.dumps(entry, ensure_ascii=False) + '\n')
    
    print(f"✅ Migrovaných {len(jsonl_entries)} log záznamov z {md_path.name}")
    return len(jsonl_entries)


def migrate_save_game(md_path: Path, json_path: Path, dry_run: bool = False) -> bool:
    """
    Migruje Save Game Markdown do JSON formátu.
    """
    if not md_path.exists():
        print(f"⚠️  Save Game súbor neexistuje: {md_path}")
        return False
    
    content = md_path.read_text(encoding='utf-8')
    parsed = parse_save_game(content)
    
    if not dry_run:
        json_path.parent.mkdir(parents=True, exist_ok=True)
        with json_path.open('w', encoding='utf-8') as f:
            json.dump(parsed, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Migrovaný Save Game z {md_path.name}")
    return True


def migrate_xp_status(md_path: Path, json_path: Path, dry_run: bool = False) -> bool:
    """
    Migruje XP Status Markdown do JSON formátu.
    """
    if not md_path.exists():
        print(f"⚠️  XP súbor neexistuje: {md_path}")
        return False
    
    content = md_path.read_text(encoding='utf-8')
    parsed = parse_xp_status(content)
    
    if not dry_run:
        json_path.parent.mkdir(parents=True, exist_ok=True)
        with json_path.open('w', encoding='utf-8') as f:
            json.dump(parsed, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Migrovaný XP Status z {md_path.name}")
    return True


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Migruje Markdown kontextové súbory do JSON formátov')
    parser.add_argument('--dry-run', action='store_true', help='Len zobrazí, čo by sa migrovalo')
    parser.add_argument('--backup', action='store_true', help='Vytvorí backup pôvodných súborov')
    
    args = parser.parse_args()
    
    workspace_root = Path(__file__).parent.parent
    dev_dir = workspace_root / "development"
    
    print("🔄 Migrácia kontextových súborov do štrukturovaných formátov...")
    print(f"📁 Workspace: {workspace_root}")
    print(f"🔍 Dry run: {args.dry_run}")
    print()
    
    # Migrácia logu
    log_md = dev_dir / "logs" / "XVADUR_LOG.md"
    log_jsonl = dev_dir / "logs" / "XVADUR_LOG.jsonl"
    migrate_log_file(log_md, log_jsonl, dry_run=args.dry_run)
    
    # Migrácia Save Game
    save_game_md = dev_dir / "sessions" / "save_games" / "SAVE_GAME_LATEST.md"
    save_game_json = dev_dir / "sessions" / "save_games" / "SAVE_GAME_LATEST.json"
    migrate_save_game(save_game_md, save_game_json, dry_run=args.dry_run)
    
    # Migrácia Save Game Summary
    save_game_summary_md = dev_dir / "sessions" / "save_games" / "SAVE_GAME_LATEST_SUMMARY.md"
    save_game_summary_json = dev_dir / "sessions" / "save_games" / "SAVE_GAME_LATEST_SUMMARY.json"
    migrate_save_game(save_game_summary_md, save_game_summary_json, dry_run=args.dry_run)
    
    # Migrácia XP Status
    xp_md = dev_dir / "logs" / "XVADUR_XP.md"
    xp_json = dev_dir / "logs" / "XVADUR_XP.json"
    migrate_xp_status(xp_md, xp_json, dry_run=args.dry_run)
    
    print()
    print("✅ Migrácia dokončená!")
    
    if args.dry_run:
        print("💡 Spusti bez --dry-run pre skutočnú migráciu")


if __name__ == "__main__":
    main()

