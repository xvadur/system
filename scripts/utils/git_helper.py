#!/usr/bin/env python3
"""
Git Helper: Bezpečný git push s error handling.
"""

import os
import subprocess
import sys
from pathlib import Path
from typing import Optional

# Add workspace root to path
workspace_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(workspace_root))

def git_push_changes(commit_message: str, branch: Optional[str] = None) -> bool:
    """
    Bezpečne pushne zmeny na GitHub.
    
    Args:
        commit_message: Commit message
        branch: Branch name (ak None, použije aktuálnu branch)
    
    Returns:
        True ak úspešné, False ak zlyhalo
    """
    try:
        # Zmeň na workspace root
        original_dir = Path.cwd()
        os.chdir(workspace_root)
        
        # Získaj aktuálnu branch, ak nie je zadaná
        if not branch:
            result = subprocess.run(
                ["git", "rev-parse", "--abbrev-ref", "HEAD"],
                capture_output=True,
                text=True,
                check=True
            )
            branch = result.stdout.strip()
        
        # Skontroluj, či sú zmeny
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            capture_output=True,
            text=True,
            check=True
        )
        
        if not result.stdout.strip():
            print("ℹ️  Žiadne zmeny na commitnutie")
            os.chdir(original_dir)
            return True
        
        # Add všetky zmeny
        subprocess.run(
            ["git", "add", "-A"],
            check=True,
            capture_output=True
        )
        
        # Commit
        subprocess.run(
            ["git", "commit", "-m", commit_message],
            check=True,
            capture_output=True
        )
        
        # Pull pred pushom (rieši non-fast-forward)
        try:
            subprocess.run(
                ["git", "pull", "--rebase", "origin", branch],
                check=True,
                capture_output=True,
                timeout=30
            )
        except subprocess.CalledProcessError:
            # Ak pull zlyhá, skús normálny pull
            try:
                subprocess.run(
                    ["git", "pull", "origin", branch],
                    check=True,
                    capture_output=True,
                    timeout=30
                )
            except subprocess.CalledProcessError:
                # Ak aj to zlyhá, pokračuj s pushom (možno je už aktuálne)
                print("⚠️  Git pull zlyhal, pokračujem s pushom...", file=sys.stderr)
        
        # Push
        subprocess.run(
            ["git", "push", "origin", branch],
            check=True,
            capture_output=True
        )
        
        os.chdir(original_dir)
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"⚠️  Git chyba: {e}", file=sys.stderr)
        if hasattr(e, 'stderr') and e.stderr:
            print(f"   {e.stderr.decode() if isinstance(e.stderr, bytes) else e.stderr}", file=sys.stderr)
        os.chdir(original_dir)
        return False
    except Exception as e:
        print(f"⚠️  Neočakávaná chyba pri git push: {e}", file=sys.stderr)
        os.chdir(original_dir)
        return False

if __name__ == "__main__":
    # Test
    import sys
    commit_msg = sys.argv[1] if len(sys.argv) > 1 else "test commit"
    success = git_push_changes(commit_msg)
    sys.exit(0 if success else 1)

