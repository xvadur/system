#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Git Branch Cleanup Script: Vymaže staré a nepotrebné branchy.

Použitie:
    python scripts/utils/cleanup_branches.py [--dry-run] [--force]
    
Príklady:
    # Dry run - len ukáže čo by sa vymazalo
    python scripts/utils/cleanup_branches.py --dry-run
    
    # Skutočné vymazanie
    python scripts/utils/cleanup_branches.py --force
"""

import subprocess
import sys
import argparse
from pathlib import Path

# Workspace root
_workspace_root = Path(__file__).parent.parent.parent


def run_command(cmd: list, cwd: Path = None) -> tuple[str, int]:
    """
    Spustí shell príkaz a vráti výstup a exit code.
    
    Args:
        cmd: Zoznam argumentov príkazu
        cwd: Working directory (default: workspace root)
    
    Returns:
        Tuple (output, exit_code)
    """
    if cwd is None:
        cwd = _workspace_root
    
    try:
        result = subprocess.run(
            cmd,
            cwd=cwd,
            capture_output=True,
            text=True,
            check=False
        )
        return result.stdout.strip(), result.returncode
    except Exception as e:
        print(f"❌ Chyba pri spustení príkazu {' '.join(cmd)}: {e}")
        return "", 1


def get_merged_branches() -> list[str]:
    """
    Získa zoznam branchov, ktoré sú už zlúčené do main.
    
    Returns:
        Zoznam názvov branchov
    """
    output, _ = run_command(["git", "branch", "--merged", "main"])
    branches = [
        b.strip().replace("*", "").strip()
        for b in output.split("\n")
        if b.strip() and "main" not in b
    ]
    return branches


def get_remote_branches() -> list[str]:
    """
    Získa zoznam remote branchov.
    
    Returns:
        Zoznam názvov remote branchov
    """
    output, _ = run_command(["git", "branch", "-r"])
    branches = [
        b.strip().replace("origin/", "")
        for b in output.split("\n")
        if b.strip() and "HEAD" not in b
    ]
    return branches


def is_deprecated_branch(branch_name: str) -> bool:
    """
    Zistí, či je branch deprecated podľa nového modelu.
    
    Args:
        branch_name: Názov branchu
    
    Returns:
        True ak je deprecated
    """
    deprecated_patterns = [
        "session-",
        "codex/",
    ]
    
    return any(pattern in branch_name for pattern in deprecated_patterns)


def get_current_branch() -> str:
    """
    Získa názov aktuálneho branchu.
    
    Returns:
        Názov aktuálneho branchu
    """
    output, _ = run_command(["git", "rev-parse", "--abbrev-ref", "HEAD"])
    return output.strip()


def cleanup_local_branches(dry_run: bool = True) -> list[str]:
    """
    Vymaže lokálne deprecated branchy.
    
    Args:
        dry_run: Ak True, len ukáže čo by sa vymazalo
    
    Returns:
        Zoznam vymazaných branchov
    """
    current_branch = get_current_branch()
    merged = get_merged_branches()
    deprecated = [
        b for b in merged 
        if is_deprecated_branch(b) and b != current_branch
    ]
    
    if not deprecated:
        print("✅ Žiadne deprecated branchy na vymazanie")
        return []
    
    print(f"\n📋 Nájdené deprecated branchy ({len(deprecated)}):")
    for branch in deprecated:
        print(f"   - {branch}")
    
    if dry_run:
        print("\n⚠️  DRY RUN - nič sa nevymaže")
        return []
    
    deleted = []
    for branch in deprecated:
        print(f"\n🗑️  Vymazávam lokálny branch: {branch}")
        _, exit_code = run_command(["git", "branch", "-d", branch])
        if exit_code == 0:
            deleted.append(branch)
            print(f"   ✅ Vymazané: {branch}")
        else:
            print(f"   ⚠️  Nepodarilo sa vymazať: {branch}")
    
    return deleted


def cleanup_remote_branches(dry_run: bool = True) -> list[str]:
    """
    Vymaže remote deprecated branchy.
    
    Args:
        dry_run: Ak True, len ukáže čo by sa vymazalo
    
    Returns:
        Zoznam vymazaných remote branchov
    """
    remote = get_remote_branches()
    deprecated = [b for b in remote if is_deprecated_branch(b)]
    
    if not deprecated:
        print("✅ Žiadne deprecated remote branchy na vymazanie")
        return []
    
    print(f"\n📋 Nájdené deprecated remote branchy ({len(deprecated)}):")
    for branch in deprecated:
        print(f"   - origin/{branch}")
    
    if dry_run:
        print("\n⚠️  DRY RUN - nič sa nevymaže")
        return []
    
    deleted = []
    for branch in deprecated:
        print(f"\n🗑️  Vymazávam remote branch: origin/{branch}")
        _, exit_code = run_command(["git", "push", "origin", "--delete", branch])
        if exit_code == 0:
            deleted.append(branch)
            print(f"   ✅ Vymazané: origin/{branch}")
        else:
            print(f"   ⚠️  Nepodarilo sa vymazať: origin/{branch}")
    
    return deleted


def prune_remote_tracking(dry_run: bool = True):
    """
    Vyčistí tracking branchy, ktoré už neexistujú na remote.
    
    Args:
        dry_run: Ak True, len ukáže čo by sa vyčistilo
    """
    if dry_run:
        print("\n📋 Prune remote tracking branches (dry-run)")
        print("   Spustí: git remote prune origin")
        return
    
    print("\n🧹 Čistím remote tracking branchy...")
    run_command(["git", "remote", "prune", "origin"])
    print("   ✅ Hotovo")


def main():
    """Hlavná funkcia."""
    parser = argparse.ArgumentParser(
        description="Vyčistí staré a deprecated git branchy"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Len ukáže čo by sa vymazalo, nič nespustí"
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Skutočné vymazanie (vyžaduje explicitné potvrdenie)"
    )
    
    args = parser.parse_args()
    
    dry_run = not args.force
    
    if not dry_run:
        response = input("\n⚠️  Naozaj chceš vymazať deprecated branchy? (yes/no): ")
        if response.lower() != "yes":
            print("❌ Zrušené")
            sys.exit(0)
    
    print("🔍 Analyzujem git branchy...")
    
    # Cleanup lokálne branchy
    local_deleted = cleanup_local_branches(dry_run=dry_run)
    
    # Cleanup remote branchy
    remote_deleted = cleanup_remote_branches(dry_run=dry_run)
    
    # Prune remote tracking
    prune_remote_tracking(dry_run=dry_run)
    
    # Summary
    print("\n" + "="*60)
    print("📊 SUMMARY")
    print("="*60)
    if dry_run:
        print("⚠️  DRY RUN - nič sa nevymazalo")
    else:
        print(f"✅ Lokálne branchy vymazané: {len(local_deleted)}")
        print(f"✅ Remote branchy vymazané: {len(remote_deleted)}")
        if local_deleted:
            print("\n   Lokálne:")
            for b in local_deleted:
                print(f"     - {b}")
        if remote_deleted:
            print("\n   Remote:")
            for b in remote_deleted:
                print(f"     - origin/{b}")


if __name__ == "__main__":
    main()

