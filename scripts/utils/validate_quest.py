#!/usr/bin/env python3
"""
validate_quest.py - Validátor Questov podľa Anthropic Harness Pattern

Tento skript implementuje "Self-verify testing" pattern z Anthropic článku:
https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents

Umožňuje:
- Validáciu jednotlivých questov proti ich kritériám
- Aktualizáciu `passes` fieldu v SAVE_GAME.json
- Health check pred začatím práce

Použitie:
    python validate_quest.py                    # Validuje všetky questy
    python validate_quest.py --quest quest-15   # Validuje konkrétny quest
    python validate_quest.py --health-check     # Spustí health check
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Dict, Any

# Cesty k súborom
WORKSPACE_ROOT = Path(__file__).parent.parent.parent
SAVE_GAME_PATH = WORKSPACE_ROOT / "development" / "sessions" / "save_games" / "SAVE_GAME.json"


def load_save_game() -> Dict[str, Any]:
    """Načíta SAVE_GAME.json"""
    if not SAVE_GAME_PATH.exists():
        print(f"❌ SAVE_GAME.json nenájdený: {SAVE_GAME_PATH}")
        sys.exit(1)
    
    with open(SAVE_GAME_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_save_game(data: Dict[str, Any]) -> None:
    """Uloží SAVE_GAME.json"""
    with open(SAVE_GAME_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"✅ SAVE_GAME.json aktualizovaný")


def validate_quest(quest: Dict[str, Any], interactive: bool = True) -> bool:
    """
    Validuje quest proti jeho kritériám.
    
    Ak je interactive=True, pýta sa užívateľa na potvrdenie každého kritéria.
    Ak je interactive=False, vráti False (vyžaduje manuálnu validáciu).
    
    Returns:
        bool: True ak quest passes, False inak
    """
    quest_id = quest.get('id', 'unknown')
    title = quest.get('title', 'Unknown Quest')
    validation = quest.get('validation', {})
    criteria = validation.get('criteria', [])
    
    if not criteria:
        print(f"⚠️ Quest '{title}' nemá definované kritériá validácie")
        return False
    
    print(f"\n🎯 Validácia: {title}")
    print(f"   ID: {quest_id}")
    print(f"   Status: {quest.get('status', 'unknown')}")
    print(f"   Kritériá ({len(criteria)}):")
    
    all_passed = True
    
    for i, criterion in enumerate(criteria, 1):
        print(f"\n   [{i}/{len(criteria)}] {criterion}")
        
        if interactive:
            response = input("   Splnené? (y/n/s=skip): ").strip().lower()
            if response == 'y':
                print("   ✅ Splnené")
            elif response == 's':
                print("   ⏭️ Preskočené")
            else:
                print("   ❌ Nesplnené")
                all_passed = False
        else:
            print("   ⏸️ Vyžaduje manuálnu validáciu")
            all_passed = False
    
    return all_passed


def update_quest_passes(quest_id: str, passes: bool) -> None:
    """Aktualizuje `passes` field pre konkrétny quest"""
    data = load_save_game()
    
    for quest in data.get('quests', []):
        if quest.get('id') == quest_id:
            quest['passes'] = passes
            quest['validation']['last_tested'] = datetime.now().isoformat()
            print(f"✅ Quest '{quest_id}' passes={passes}")
            save_save_game(data)
            return
    
    print(f"❌ Quest '{quest_id}' nenájdený")


def health_check() -> bool:
    """
    Spustí health check pred začatím práce.
    
    Kontroluje:
    1. Či existuje SAVE_GAME.json
    2. Či existuje aspoň jeden quest
    3. Či sú questy v správnom formáte (s passes a validation)
    4. Či nie sú nejaké questy s passes=True ale status != completed
    
    Returns:
        bool: True ak health check prešiel, False inak
    """
    print("\n🏥 Health Check - Anthropic Harness Pattern")
    print("=" * 50)
    
    # 1. Kontrola existencie súboru
    if not SAVE_GAME_PATH.exists():
        print("❌ SAVE_GAME.json neexistuje")
        return False
    print("✅ SAVE_GAME.json existuje")
    
    # 2. Načítanie a kontrola štruktúry
    try:
        data = load_save_game()
    except json.JSONDecodeError as e:
        print(f"❌ Chyba pri parsovaní JSON: {e}")
        return False
    print("✅ JSON validný")
    
    # 3. Kontrola questov
    quests = data.get('quests', [])
    if not quests:
        print("⚠️ Žiadne questy nenájdené")
        return True  # Nie je to chyba, len upozornenie
    print(f"✅ {len(quests)} questov nájdených")
    
    # 4. Kontrola formátu questov
    issues = []
    for quest in quests:
        quest_id = quest.get('id', 'unknown')
        
        # Kontrola passes field
        if 'passes' not in quest:
            issues.append(f"Quest '{quest_id}' nemá 'passes' field")
        
        # Kontrola validation field
        if 'validation' not in quest:
            issues.append(f"Quest '{quest_id}' nemá 'validation' field")
        elif 'criteria' not in quest.get('validation', {}):
            issues.append(f"Quest '{quest_id}' nemá 'validation.criteria'")
    
    if issues:
        print(f"⚠️ {len(issues)} problémov nájdených:")
        for issue in issues:
            print(f"   - {issue}")
        return False
    print("✅ Všetky questy majú správny formát (passes + validation)")
    
    # 5. Kontrola konzistencie
    inconsistent = []
    for quest in quests:
        passes = quest.get('passes', False)
        status = quest.get('status', 'unknown')
        
        # Quest s passes=True by mal mať status completed
        if passes and status not in ['completed', 'done']:
            inconsistent.append(f"Quest '{quest.get('id')}' má passes=True ale status='{status}'")
    
    if inconsistent:
        print(f"⚠️ {len(inconsistent)} nekonzistencií:")
        for item in inconsistent:
            print(f"   - {item}")
    else:
        print("✅ Konzistencia passes vs status OK")
    
    print("\n" + "=" * 50)
    print("🏁 Health Check dokončený")
    return len(issues) == 0


def list_quests() -> None:
    """Zobrazí všetky questy so statusom"""
    data = load_save_game()
    quests = data.get('quests', [])
    
    print("\n📋 Zoznam Questov")
    print("=" * 60)
    
    for quest in quests:
        quest_id = quest.get('id', 'unknown')
        title = quest.get('title', 'Unknown')
        status = quest.get('status', 'unknown')
        passes = quest.get('passes', False)
        criteria_count = len(quest.get('validation', {}).get('criteria', []))
        
        status_emoji = "✅" if passes else "❌"
        print(f"{status_emoji} [{status:12}] {title[:40]}")
        print(f"   ID: {quest_id}")
        print(f"   Kritériá: {criteria_count}")
        print()


def main():
    """Hlavná funkcia"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Validátor Questov podľa Anthropic Harness Pattern"
    )
    parser.add_argument(
        '--quest', '-q',
        help="ID konkrétneho questu na validáciu"
    )
    parser.add_argument(
        '--health-check', '-hc',
        action='store_true',
        help="Spustí health check"
    )
    parser.add_argument(
        '--list', '-l',
        action='store_true',
        help="Zobrazí zoznam questov"
    )
    parser.add_argument(
        '--non-interactive', '-n',
        action='store_true',
        help="Spustí v neinteraktívnom režime"
    )
    parser.add_argument(
        '--mark-pass', '-p',
        help="Označí quest ako passes=True"
    )
    parser.add_argument(
        '--mark-fail', '-f',
        help="Označí quest ako passes=False"
    )
    
    args = parser.parse_args()
    
    # Health check
    if args.health_check:
        success = health_check()
        sys.exit(0 if success else 1)
    
    # List questov
    if args.list:
        list_quests()
        sys.exit(0)
    
    # Označenie questu ako pass/fail
    if args.mark_pass:
        update_quest_passes(args.mark_pass, True)
        sys.exit(0)
    
    if args.mark_fail:
        update_quest_passes(args.mark_fail, False)
        sys.exit(0)
    
    # Validácia konkrétneho questu
    if args.quest:
        data = load_save_game()
        for quest in data.get('quests', []):
            if quest.get('id') == args.quest:
                interactive = not args.non_interactive
                passes = validate_quest(quest, interactive=interactive)
                if interactive:
                    response = input(f"\nAktualizovať passes={passes}? (y/n): ").strip().lower()
                    if response == 'y':
                        update_quest_passes(args.quest, passes)
                sys.exit(0 if passes else 1)
        
        print(f"❌ Quest '{args.quest}' nenájdený")
        sys.exit(1)
    
    # Bez argumentov - validácia všetkých questov
    data = load_save_game()
    quests = data.get('quests', [])
    
    print(f"\n🎯 Validácia {len(quests)} questov")
    print("=" * 60)
    
    for quest in quests:
        if quest.get('status') in ['completed', 'done']:
            print(f"⏭️ Preskočené (completed): {quest.get('title', 'Unknown')}")
            continue
        
        interactive = not args.non_interactive
        passes = validate_quest(quest, interactive=interactive)
        
        if interactive:
            response = input(f"\nAktualizovať passes={passes}? (y/n): ").strip().lower()
            if response == 'y':
                update_quest_passes(quest.get('id'), passes)


if __name__ == "__main__":
    main()

