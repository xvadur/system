#!/usr/bin/env python3
"""
Migračný skript pre Hot/Cold Storage architektúru.

Tento skript:
1. Načíta všetky existujúce záznamy z XVADUR_LOG.jsonl
2. Migruje ich do SQLite databázy (Cold Storage)
3. Ponechá posledných HOT_STORAGE_LIMIT záznamov v JSONL (Hot Storage)

Použitie:
    python scripts/utils/migrate_to_sqlite.py
    python scripts/utils/migrate_to_sqlite.py --dry-run  # Len simulácia
    python scripts/utils/migrate_to_sqlite.py --force    # Prepíš existujúcu DB
"""

import sys
import json
import argparse
from pathlib import Path
from datetime import datetime

# Add workspace root to path
workspace_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(workspace_root))

from core.ministers.sqlite_store import SQLiteStore

# Cesty k súborom
LOG_JSONL_PATH = workspace_root / "development" / "logs" / "XVADUR_LOG.jsonl"
SQLITE_DB_PATH = workspace_root / "development" / "data" / "archive.db"
BACKUP_PATH = LOG_JSONL_PATH.with_suffix(".jsonl.pre_migration_backup")

# Konfigurácia
HOT_STORAGE_LIMIT = 100


def load_jsonl_entries(path: Path) -> list:
    """Načíta všetky záznamy z JSONL súboru."""
    entries = []
    
    if not path.exists():
        print(f"⚠️  JSONL súbor neexistuje: {path}")
        return entries
    
    with open(path, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
                entries.append(entry)
            except json.JSONDecodeError as e:
                print(f"⚠️  Chyba pri parsovaní riadku {line_num}: {e}")
                continue
    
    return entries


def create_backup(source: Path, dest: Path) -> bool:
    """Vytvorí backup JSONL súboru."""
    try:
        import shutil
        shutil.copy(source, dest)
        return True
    except Exception as e:
        print(f"❌ Chyba pri vytváraní backupu: {e}")
        return False


def migrate_to_sqlite(entries: list, db_path: Path, force: bool = False) -> int:
    """Migruje záznamy do SQLite databázy."""
    
    # Skontroluj či DB existuje
    if db_path.exists() and not force:
        print(f"⚠️  SQLite databáza už existuje: {db_path}")
        print("   Použi --force pre prepísanie alebo --dry-run pre simuláciu")
        return 0
    
    # Vytvor SQLite store
    store = SQLiteStore(db_path)
    
    # Batch insert
    count = store.insert_batch(entries)
    
    return count


def trim_jsonl(path: Path, entries: list, limit: int) -> int:
    """Ponechá len posledných N záznamov v JSONL."""
    keep_entries = entries[-limit:] if len(entries) > limit else entries
    
    with open(path, 'w', encoding='utf-8') as f:
        for entry in keep_entries:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    
    return len(entries) - len(keep_entries)


def main():
    parser = argparse.ArgumentParser(
        description="Migruje JSONL záznamy do SQLite (Hot/Cold Storage)"
    )
    parser.add_argument(
        "--dry-run", 
        action="store_true", 
        help="Len simulácia, bez zmien"
    )
    parser.add_argument(
        "--force", 
        action="store_true", 
        help="Prepíš existujúcu SQLite databázu"
    )
    parser.add_argument(
        "--hot-limit", 
        type=int, 
        default=HOT_STORAGE_LIMIT,
        help=f"Počet záznamov ponechaných v Hot Storage (default: {HOT_STORAGE_LIMIT})"
    )
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("MIGRÁCIA NA HOT/COLD STORAGE ARCHITEKTÚRU")
    print("=" * 60)
    print(f"JSONL súbor: {LOG_JSONL_PATH}")
    print(f"SQLite databáza: {SQLITE_DB_PATH}")
    print(f"Hot Storage limit: {args.hot_limit}")
    print(f"Dry run: {args.dry_run}")
    print(f"Force: {args.force}")
    print("=" * 60)
    
    # 1. Načítaj záznamy
    print("\n📖 Načítavam JSONL záznamy...")
    entries = load_jsonl_entries(LOG_JSONL_PATH)
    print(f"   Načítaných {len(entries)} záznamov")
    
    if not entries:
        print("❌ Žiadne záznamy na migráciu")
        return 1
    
    # 2. Štatistiky
    print("\n📊 Štatistiky:")
    types = {}
    total_xp = 0
    for entry in entries:
        entry_type = entry.get('type', 'unknown')
        types[entry_type] = types.get(entry_type, 0) + 1
        total_xp += entry.get('xp_estimate', 0) or 0
    
    for entry_type, count in sorted(types.items()):
        print(f"   - {entry_type}: {count}")
    print(f"   - Total XP: {total_xp}")
    
    if args.dry_run:
        print("\n🔍 DRY RUN - žiadne zmeny nebudú vykonané")
        print(f"   - Do SQLite by bolo migrovaných: {len(entries)} záznamov")
        print(f"   - V JSONL by zostalo: {min(len(entries), args.hot_limit)} záznamov")
        print(f"   - Archivovaných by bolo: {max(0, len(entries) - args.hot_limit)} záznamov")
        return 0
    
    # 3. Vytvor backup
    print("\n💾 Vytváram backup...")
    if not create_backup(LOG_JSONL_PATH, BACKUP_PATH):
        print("❌ Backup zlyhal, migrácia zrušená")
        return 1
    print(f"   Backup vytvorený: {BACKUP_PATH}")
    
    # 4. Migruj do SQLite
    print("\n📦 Migrujem do SQLite (Cold Storage)...")
    migrated = migrate_to_sqlite(entries, SQLITE_DB_PATH, force=args.force)
    if migrated == 0 and len(entries) > 0:
        print("❌ Migrácia do SQLite zlyhala")
        return 1
    print(f"   Migrovaných {migrated} záznamov")
    
    # 5. Trim JSONL
    print("\n✂️  Trimming JSONL (Hot Storage)...")
    archived = trim_jsonl(LOG_JSONL_PATH, entries, args.hot_limit)
    remaining = len(entries) - archived
    print(f"   Archivovaných: {archived} záznamov")
    print(f"   Ponechaných v Hot Storage: {remaining} záznamov")
    
    # 6. Verifikácia
    print("\n✅ Verifikácia...")
    store = SQLiteStore(SQLITE_DB_PATH)
    sqlite_count = store.count()
    jsonl_count = len(load_jsonl_entries(LOG_JSONL_PATH))
    
    print(f"   SQLite (Cold Storage): {sqlite_count} záznamov")
    print(f"   JSONL (Hot Storage): {jsonl_count} záznamov")
    
    if sqlite_count == len(entries) and jsonl_count <= args.hot_limit:
        print("\n🎉 MIGRÁCIA ÚSPEŠNÁ!")
    else:
        print("\n⚠️  Migrácia dokončená s varovaním (skontroluj počty)")
    
    print("=" * 60)
    return 0


if __name__ == "__main__":
    sys.exit(main())

