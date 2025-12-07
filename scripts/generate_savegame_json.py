#!/usr/bin/env python3
"""
Helper skript pre automatické generovanie JSON z Markdown save game.

Použitie:
    from scripts.generate_savegame_json import generate_json_from_markdown
    generate_json_from_markdown(markdown_content, json_path)
"""

import json
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List


def parse_save_game_markdown(markdown_content: str) -> Dict[str, Any]:
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
    quest_current = None
    
    for i, line in enumerate(lines):
        line_stripped = line.strip()
        
        # Detekuj sekcie
        if line_stripped.startswith("# 💾 SAVE GAME:"):
            # Extrahuj dátum a čas
            date_match = re.search(r'(\d{4}-\d{2}-\d{2})', line_stripped)
            time_match = re.search(r'(\d{2}:\d{2})', line_stripped)
            if date_match:
                save_game["metadata"]["session_date"] = date_match.group(1)
                if time_match:
                    save_game["metadata"]["created_at"] = f"{date_match.group(1)}T{time_match.group(1)}:00Z"
                else:
                    save_game["metadata"]["created_at"] = f"{date_match.group(1)}T00:00:00Z"
        elif line_stripped.startswith("## 📊 Status"):
            current_section = "status"
        elif line_stripped.startswith("## 🧠 Naratívny Kontext"):
            current_section = "narrative"
        elif line_stripped.startswith("## 🎯 Aktívne Questy"):
            current_section = "quests"
        elif line_stripped.startswith("## ⚠️ Inštrukcie pre Nového Agenta"):
            current_section = "instructions"
        elif line_stripped.startswith("---"):
            # Separátor - koniec záznamu
            if current_section == "narrative" and narrative_lines:
                save_game["narrative"]["summary"] = " ".join(narrative_lines[:500])
            current_section = None
        elif current_section == "status":
            if "**Rank:**" in line_stripped:
                save_game["status"]["rank"] = line_stripped.split("**Rank:**")[1].strip()
            elif "**Level:**" in line_stripped:
                level_match = re.search(r'(\d+)', line_stripped)
                if level_match:
                    save_game["status"]["level"] = int(level_match.group(1))
            elif "**XP:**" in line_stripped:
                xp_match = re.search(r'(\d+\.?\d*)\s*/\s*(\d+\.?\d*)', line_stripped)
                if xp_match:
                    save_game["status"]["xp"] = float(xp_match.group(1))
                    save_game["status"]["xp_next_level"] = float(xp_match.group(2))
                    percent = (save_game["status"]["xp"] / save_game["status"]["xp_next_level"]) * 100
                    save_game["status"]["xp_percent"] = round(percent, 1)
            elif "**Streak:**" in line_stripped:
                streak_match = re.search(r'(\d+)', line_stripped)
                if streak_match:
                    save_game["status"]["streak_days"] = int(streak_match.group(1))
        elif current_section == "narrative":
            if line_stripped and not line_stripped.startswith("#"):
                narrative_lines.append(line_stripped)
            # Extrahuj kľúčové rozhodnutia a momenty
            if "**Kľúčové rozhodnutia:**" in line_stripped or "Kľúčové rozhodnutia" in line_stripped:
                # Nasledujúce riadky sú rozhodnutia
                pass
            elif line_stripped.startswith("- ") and "rozhodnutie" in line_stripped.lower():
                decision = line_stripped.replace("- ", "").strip()
                if decision:
                    save_game["narrative"]["key_decisions"].append(decision)
        elif current_section == "quests":
            if line_stripped.startswith("### "):
                quest_title = line_stripped.replace("### ", "").strip()
                quest_id = quest_title.lower().replace(" ", "-").replace(":", "")
                quest_current = {
                    "id": quest_id,
                    "title": quest_title,
                    "status": "new",
                    "next_steps": [],
                    "blockers": []
                }
                save_game["quests"].append(quest_current)
            elif quest_current:
                if "**Status:**" in line_stripped:
                    status_match = re.search(r'([🆕✅⏳❌])', line_stripped)
                    if status_match:
                        emoji = status_match.group(1)
                        status_map = {"🆕": "new", "✅": "completed", "⏳": "in_progress", "❌": "blocked"}
                        quest_current["status"] = status_map.get(emoji, "new")
                elif "**Next Steps:**" in line_stripped or line_stripped.startswith("- **Next Steps:**"):
                    # Nasledujúce riadky sú next steps
                    pass
                elif line_stripped.startswith("  ") or line_stripped.startswith("- "):
                    step = line_stripped.replace("- ", "").replace("  ", "").strip()
                    if step and not step.startswith("**"):
                        quest_current["next_steps"].append(step)
        elif current_section == "instructions":
            if line_stripped.startswith("- "):
                instruction = line_stripped.replace("- ", "").strip()
                if instruction:
                    if "preferuje" in instruction.lower() or "štýl" in instruction.lower():
                        save_game["instructions"]["style"].append(instruction)
                    else:
                        save_game["instructions"]["for_agent"].append(instruction)
    
    # Zlúč narrative lines ak ešte nie sú
    if not save_game["narrative"]["summary"] and narrative_lines:
        save_game["narrative"]["summary"] = " ".join(narrative_lines[:500])
    
    return save_game


def generate_json_from_markdown(markdown_content: str, json_path: Path) -> bool:
    """
    Generuje JSON súbor z Markdown save game obsahu.
    
    Args:
        markdown_content: Markdown obsah save game
        json_path: Cesta k výstupnému JSON súboru
    
    Returns:
        True ak úspešné, False inak
    """
    try:
        parsed = parse_save_game_markdown(markdown_content)
        
        # Vytvor adresár ak neexistuje
        json_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Ulož JSON
        with json_path.open('w', encoding='utf-8') as f:
            json.dump(parsed, f, ensure_ascii=False, indent=2)
        
        return True
    except Exception as e:
        print(f"❌ Chyba pri generovaní JSON: {e}")
        return False


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Použitie: python3 scripts/generate_savegame_json.py <markdown_file> [json_file]")
        sys.exit(1)
    
    md_path = Path(sys.argv[1])
    if not md_path.exists():
        print(f"❌ Markdown súbor neexistuje: {md_path}")
        sys.exit(1)
    
    if len(sys.argv) >= 3:
        json_path = Path(sys.argv[2])
    else:
        # Default: rovnaký názov, ale .json
        json_path = md_path.parent / f"{md_path.stem}.json"
    
    content = md_path.read_text(encoding='utf-8')
    
    if generate_json_from_markdown(content, json_path):
        print(f"✅ JSON vygenerovaný: {json_path}")
    else:
        print(f"❌ Chyba pri generovaní JSON")
        sys.exit(1)

