#!/usr/bin/env python3
"""
Archive Query - CLI nástroj pre query nad Cold Storage (SQLite).

Tento modul poskytuje rozhranie pre historické analýzy nad archivovanými
log záznamami v SQLite databáze.

Použitie:
    # Základné query
    python scripts/utils/archive_query.py --type task --limit 10
    
    # XP summary
    python scripts/utils/archive_query.py --xp-summary
    
    # Quest summary
    python scripts/utils/archive_query.py --quest 20
    
    # Agregácie
    python scripts/utils/archive_query.py --aggregate type
    
    # Export do JSON
    python scripts/utils/archive_query.py --type task --output results.json
"""

import sys
import json
import argparse
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any

# Add workspace root to path
workspace_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(workspace_root))

from core.ministers.sqlite_store import SQLiteStore

# Cesta k SQLite databáze
SQLITE_DB_PATH = workspace_root / "development" / "data" / "archive.db"


def get_store() -> Optional[SQLiteStore]:
    """Vráti SQLiteStore inštanciu."""
    if not SQLITE_DB_PATH.exists():
        print(f"❌ SQLite databáza neexistuje: {SQLITE_DB_PATH}")
        print("   Spusti najprv: python scripts/utils/migrate_to_sqlite.py")
        return None
    
    return SQLiteStore(SQLITE_DB_PATH)


def format_entry(entry: Dict[str, Any], verbose: bool = False) -> str:
    """Formátuje záznam pre výstup."""
    timestamp = entry.get('timestamp', '')[:16]  # YYYY-MM-DDTHH:MM
    title = entry.get('title', 'N/A')
    entry_type = entry.get('type', 'N/A')
    status = entry.get('status', 'N/A')
    xp = entry.get('xp_estimate', 0) or 0
    
    line = f"[{timestamp}] {title}"
    
    if verbose:
        line += f"\n   Type: {entry_type}, Status: {status}, XP: {xp}"
        if entry.get('files_changed'):
            line += f"\n   Files: {', '.join(entry['files_changed'][:3])}"
        if entry.get('quest_id'):
            line += f"\n   Quest: #{entry['quest_id']}"
    
    return line


def cmd_query(args) -> int:
    """Vykoná query nad archívom."""
    store = get_store()
    if store is None:
        return 1
    
    results = store.query(
        type=args.type,
        status=args.status,
        date_from=args.date_from,
        date_to=args.date_to,
        quest_id=args.quest,
        limit=args.limit
    )
    
    if args.output:
        # Export do JSON
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        print(f"✅ Exportovaných {len(results)} záznamov do {args.output}")
    else:
        # Výstup na konzolu
        print(f"\n📋 Výsledky ({len(results)} záznamov):")
        print("-" * 60)
        for entry in results:
            print(format_entry(entry, verbose=args.verbose))
        print("-" * 60)
    
    return 0


def cmd_xp_summary(args) -> int:
    """Zobrazí XP summary."""
    store = get_store()
    if store is None:
        return 1
    
    summary = store.get_xp_summary()
    
    print("\n💰 XP SUMMARY")
    print("=" * 60)
    print(f"Total XP: {summary.get('total_xp', 0):.2f}")
    
    print("\n📊 XP podľa typu:")
    for item in summary.get('by_type', []):
        print(f"   - {item.get('type', 'N/A')}: {item.get('xp', 0):.2f}")
    
    print("\n📅 XP podľa dňa (posledných 7 dní):")
    for item in summary.get('by_day', []):
        print(f"   - {item.get('date', 'N/A')}: {item.get('xp', 0):.2f}")
    
    print("=" * 60)
    return 0


def cmd_quest_summary(args) -> int:
    """Zobrazí quest summary."""
    store = get_store()
    if store is None:
        return 1
    
    summary = store.get_quest_summary(args.quest)
    
    if not summary.get('found'):
        print(f"❌ Quest #{args.quest} nenájdený")
        return 1
    
    print(f"\n🎯 QUEST #{args.quest} SUMMARY")
    print("=" * 60)
    print(f"Počet záznamov: {summary.get('entry_count', 0)}")
    print(f"Total XP: {summary.get('total_xp', 0):.2f}")
    print(f"Statusy: {', '.join(summary.get('statuses', []))}")
    
    first = summary.get('first_entry', {})
    last = summary.get('last_entry', {})
    
    print(f"\nPrvý záznam: [{first.get('timestamp', '')[:16]}] {first.get('title', 'N/A')}")
    print(f"Posledný záznam: [{last.get('timestamp', '')[:16]}] {last.get('title', 'N/A')}")
    print("=" * 60)
    return 0


def cmd_aggregate(args) -> int:
    """Zobrazí agregácie."""
    store = get_store()
    if store is None:
        return 1
    
    results = store.aggregate(
        field="xp_estimate",
        agg_func="SUM",
        group_by=args.group_by
    )
    
    print(f"\n📊 AGREGÁCIA XP podľa {args.group_by}")
    print("=" * 60)
    for item in results:
        key = item.get(args.group_by, 'N/A')
        value = item.get('value', 0) or 0
        print(f"   - {key}: {value:.2f}")
    print("=" * 60)
    return 0


def cmd_stats(args) -> int:
    """Zobrazí štatistiky archívu."""
    store = get_store()
    if store is None:
        return 1
    
    total = store.count()
    
    print("\n📊 ARCHIVE STATS")
    print("=" * 60)
    print(f"Celkový počet záznamov: {total}")
    
    # Počet podľa typu
    print("\nPodľa typu:")
    for entry_type in ['task', 'session', 'quest_created', 'quest_closed', 'savegame', 'analysis']:
        count = store.count(type=entry_type)
        if count > 0:
            print(f"   - {entry_type}: {count}")
    
    # Počet podľa statusu
    print("\nPodľa statusu:")
    for status in ['started', 'completed', 'in_progress', 'open']:
        count = store.count(status=status)
        if count > 0:
            print(f"   - {status}: {count}")
    
    print("=" * 60)
    return 0


def cmd_recent(args) -> int:
    """Zobrazí posledné záznamy z archívu."""
    store = get_store()
    if store is None:
        return 1
    
    # Posledných N dní
    date_from = (datetime.now() - timedelta(days=args.days)).strftime('%Y-%m-%d')
    
    results = store.query(
        date_from=date_from,
        limit=args.limit
    )
    
    print(f"\n📅 POSLEDNÉ ZÁZNAMY (od {date_from})")
    print("=" * 60)
    for entry in results:
        print(format_entry(entry, verbose=args.verbose))
    print("=" * 60)
    print(f"Celkom: {len(results)} záznamov")
    return 0


def main():
    parser = argparse.ArgumentParser(
        description="Query nástroj pre Cold Storage (SQLite archív)"
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Príkazy')
    
    # Query command
    query_parser = subparsers.add_parser('query', help='Vyhľadaj záznamy')
    query_parser.add_argument('--type', help='Filter podľa typu')
    query_parser.add_argument('--status', help='Filter podľa statusu')
    query_parser.add_argument('--date-from', help='Od dátumu (YYYY-MM-DD)')
    query_parser.add_argument('--date-to', help='Do dátumu (YYYY-MM-DD)')
    query_parser.add_argument('--quest', type=int, help='Filter podľa quest ID')
    query_parser.add_argument('--limit', type=int, default=20, help='Max výsledkov')
    query_parser.add_argument('--output', '-o', help='Export do JSON súboru')
    query_parser.add_argument('--verbose', '-v', action='store_true', help='Detailný výstup')
    
    # XP Summary command
    xp_parser = subparsers.add_parser('xp', help='XP summary')
    
    # Quest Summary command
    quest_parser = subparsers.add_parser('quest', help='Quest summary')
    quest_parser.add_argument('quest', type=int, help='Quest ID')
    
    # Aggregate command
    agg_parser = subparsers.add_parser('aggregate', help='Agregácie')
    agg_parser.add_argument('group_by', choices=['type', 'status', 'date', 'quest_id'], help='Group by pole')
    
    # Stats command
    stats_parser = subparsers.add_parser('stats', help='Štatistiky archívu')
    
    # Recent command
    recent_parser = subparsers.add_parser('recent', help='Posledné záznamy')
    recent_parser.add_argument('--days', type=int, default=7, help='Počet dní dozadu')
    recent_parser.add_argument('--limit', type=int, default=50, help='Max výsledkov')
    recent_parser.add_argument('--verbose', '-v', action='store_true', help='Detailný výstup')
    
    args = parser.parse_args()
    
    if args.command is None:
        # Default: zobraz stats
        args.command = 'stats'
    
    # Dispatch
    if args.command == 'query':
        return cmd_query(args)
    elif args.command == 'xp':
        return cmd_xp_summary(args)
    elif args.command == 'quest':
        return cmd_quest_summary(args)
    elif args.command == 'aggregate':
        return cmd_aggregate(args)
    elif args.command == 'stats':
        return cmd_stats(args)
    elif args.command == 'recent':
        return cmd_recent(args)
    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())

