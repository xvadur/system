#!/usr/bin/env python3
"""
Migračný skript pre prompts_log.jsonl.

Opraví nekonzistentné formáty v prompts_log.jsonl:
- Doplní chýbajúce 'timestamp' polia (z metadata.extracted_at alebo aktuálny čas)
- Doplní chýbajúce 'role' polia (default 'user')
- Normalizuje formát na štandardný MemoryRecord formát
"""

import json
import sys
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, Any

# Add workspace root to path
workspace_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(workspace_root))

from core.ministers.memory import MemoryRecord

def migrate_prompts_log(prompts_log_path: Path, backup: bool = True) -> int:
    """
    Migruje prompts_log.jsonl na konzistentný formát.
    
    Args:
        prompts_log_path: Cesta k prompts_log.jsonl súboru
        backup: Vytvoriť backup pred migráciou
        
    Returns:
        Počet migrovaných záznamov
    """
    if not prompts_log_path.exists():
        print(f"❌ Súbor {prompts_log_path} neexistuje!")
        return 0
    
    # Vytvor backup
    if backup:
        backup_path = prompts_log_path.with_suffix('.jsonl.backup')
        shutil.copy2(prompts_log_path, backup_path)
        print(f"✅ Backup vytvorený: {backup_path}")
    
    # Načítaj všetky záznamy
    records = []
    migrated_count = 0
    
    with open(prompts_log_path, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            
            try:
                data = json.loads(line)
                
                # Normalizuj formát
                normalized = normalize_record(data, line_num)
                if normalized:
                    records.append(normalized)
                    if normalized != data:  # Ak sa zmenil formát
                        migrated_count += 1
                        
            except json.JSONDecodeError as e:
                print(f"⚠️  Riadok {line_num}: Nevalidný JSON - {e}")
                continue
    
    # Prepíš súbor normalizovanými záznamami
    with open(prompts_log_path, 'w', encoding='utf-8') as f:
        for record in records:
            f.write(json.dumps(record, ensure_ascii=False) + '\n')
    
    print(f"✅ Migrácia dokončená:")
    print(f"   - Celkový počet záznamov: {len(records)}")
    print(f"   - Migrovaných záznamov: {migrated_count}")
    print(f"   - Súbor prepísaný: {prompts_log_path}")
    
    return migrated_count


def normalize_record(data: Dict[str, Any], line_num: int) -> Dict[str, Any] | None:
    """
    Normalizuje jeden záznam na štandardný MemoryRecord formát.
    
    Args:
        data: JSON objekt z riadku
        line_num: Číslo riadku pre error reporting
        
    Returns:
        Normalizovaný záznam alebo None ak je nevalidný
    """
    # Content je povinný
    if 'content' not in data:
        print(f"⚠️  Riadok {line_num}: Chýba 'content', preskakujem")
        return None
    
    normalized = {
        'content': data['content'],
        'metadata': data.get('metadata', {})
    }
    
    # Normalizuj timestamp
    if 'timestamp' in data:
        normalized['timestamp'] = data['timestamp']
    elif 'metadata' in data and 'extracted_at' in data['metadata']:
        normalized['timestamp'] = data['metadata']['extracted_at']
        # Odstráň extracted_at z metadata (už je v timestamp)
        if 'extracted_at' in normalized['metadata']:
            del normalized['metadata']['extracted_at']
    else:
        # Použi aktuálny čas
        normalized['timestamp'] = datetime.now().isoformat()
        normalized['metadata']['migrated_at'] = datetime.now().isoformat()
        normalized['metadata']['migration_note'] = 'Timestamp doplnený počas migrácie'
    
    # Normalizuj role
    if 'role' in data:
        normalized['role'] = data['role']
    else:
        normalized['role'] = 'user'
        if 'migration_note' not in normalized['metadata']:
            normalized['metadata']['migration_note'] = 'Role doplnená počas migrácie'
        else:
            normalized['metadata']['migration_note'] += ', role doplnená'
    
    return normalized


def main():
    """Main entry point."""
    prompts_log_path = workspace_root / "development" / "data" / "prompts_log.jsonl"
    
    print("=" * 60)
    print("MIGRÁCIA PROMPTS_LOG.JSONL")
    print("=" * 60)
    print()
    
    migrated = migrate_prompts_log(prompts_log_path, backup=True)
    
    if migrated > 0:
        print()
        print("✅ Migrácia úspešná!")
        print(f"   {migrated} záznamov bolo normalizovaných")
    else:
        print()
        print("ℹ️  Žiadne záznamy nepotrebovali migráciu")
    
    print()
    print("=" * 60)


if __name__ == "__main__":
    main()

