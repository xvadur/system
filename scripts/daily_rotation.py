#!/usr/bin/env python3
"""
Denná rotácia: Archivácia + nová session + nová branch + git push
Spúšťa sa každú polnoc automaticky cez macOS launchd.

Tento skript:
1. Archivuje včerajšiu session → development/sessions/archive/YYYY-MM-DD.md
2. Vytvorí novú git branch: session-YYYY-MM-DD
3. Vytvorí novú prázdnu session.md
4. Pushne zmeny na GitHub
"""

import sys
import subprocess
from pathlib import Path
from datetime import datetime

# Add workspace root to path
workspace_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(workspace_root))

from scripts.auto_archive_session import archive_current_session
from scripts.create_new_session import create_new_session

def daily_rotation():
    """
    Hlavná funkcia pre dennú rotáciu.
    Spúšťa sa každú polnoc a urobí všetko naraz.
    """
    start_time = datetime.now()
    
    print("=" * 60)
    print(f"🌙 Denná rotácia spustená: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    errors = []
    
    try:
        # 1. Archivácia včerajšej session
        print("\n📦 Krok 1/4: Archivácia včerajšej session...")
        try:
            session_path = workspace_root / "development" / "sessions" / "current" / "session.md"
            if session_path.exists():
                archive_current_session()
                print("✅ Archivácia dokončená")
            else:
                print("⚠️  Session neexistuje, preskakujem archiváciu (vytvorí sa nová)")
        except Exception as e:
            error_msg = f"Archivácia zlyhala: {e}"
            errors.append(error_msg)
            print(f"❌ {error_msg}", file=sys.stderr)
        
        # 2. Vytvorenie novej git branch
        print("\n🌿 Krok 2/4: Vytvorenie novej git branch...")
        try:
            today_str = datetime.now().strftime('%Y-%m-%d')
            branch_name = f"session-{today_str}"
            
            # Skontroluj, či už existuje
            result = subprocess.run(
                ["git", "rev-parse", "--verify", branch_name],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                print(f"⚠️  Branch {branch_name} už existuje, prepínam sa na ňu...")
                subprocess.run(
                    ["git", "checkout", branch_name],
                    check=True,
                    capture_output=True
                )
            else:
                # Vytvor novú branch z main (alebo aktuálnej branch)
                current_branch = subprocess.run(
                    ["git", "rev-parse", "--abbrev-ref", "HEAD"],
                    capture_output=True,
                    text=True
                ).stdout.strip()
                
                subprocess.run(
                    ["git", "checkout", "-b", branch_name, current_branch],
                    check=True,
                    capture_output=True
                )
                print(f"✅ Nová branch vytvorená: {branch_name}")
        except subprocess.CalledProcessError as e:
            error_msg = f"Vytvorenie branch zlyhalo: {e}"
            errors.append(error_msg)
            print(f"⚠️  {error_msg} (pokračujem s aktuálnou branch)", file=sys.stderr)
        
        # 3. Vytvorenie novej session
        print("\n🆕 Krok 3/4: Vytvorenie novej session...")
        try:
            create_new_session()
            print("✅ Nová session vytvorená")
        except Exception as e:
            error_msg = f"Vytvorenie session zlyhalo: {e}"
            errors.append(error_msg)
            print(f"❌ {error_msg}", file=sys.stderr)
        
        # 4. Git commit + push na GitHub
        print("\n🚀 Krok 4/4: Git commit + push na GitHub...")
        try:
            today_str = datetime.now().strftime('%Y-%m-%d')
            branch_name = f"session-{today_str}"
            commit_message = f"chore(daily): automatická rotácia {today_str}"
            
            # Git add
            subprocess.run(
                ["git", "add", "."],
                check=True,
                capture_output=True
            )
            
            # Git commit
            subprocess.run(
                ["git", "commit", "-m", commit_message],
                check=True,
                capture_output=True
            )
            
            # Git push (s upstream tracking ak je to nová branch)
            try:
                subprocess.run(
                    ["git", "push", "-u", "origin", branch_name],
                    check=True,
                    capture_output=True,
                    timeout=30
                )
                print(f"✅ Zmeny pushnuté na GitHub (branch: {branch_name})")
            except subprocess.CalledProcessError:
                # Fallback: push aktuálnej branch
                subprocess.run(
                    ["git", "push"],
                    check=True,
                    capture_output=True
                )
                print(f"✅ Zmeny pushnuté na GitHub (aktuálna branch)")
        except subprocess.CalledProcessError as e:
            error_msg = f"Git push zlyhal: {e}"
            errors.append(error_msg)
            print(f"⚠️  {error_msg} (skús manuálne)", file=sys.stderr)
        except Exception as e:
            error_msg = f"Git operácia zlyhala: {e}"
            errors.append(error_msg)
            print(f"⚠️  {error_msg} (skús manuálne)", file=sys.stderr)
        
        # Finálne zhrnutie
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        print("\n" + "=" * 60)
        if errors:
            print(f"⚠️  Denná rotácia dokončená s {len(errors)} chybami")
            print(f"⏱️  Čas: {duration:.1f}s")
            for error in errors:
                print(f"   - {error}")
        else:
            print(f"✅ Denná rotácia úspešne dokončená!")
            print(f"⏱️  Čas: {duration:.1f}s")
        
        print("=" * 60)
        
        # Exit code: 0 ak OK, 1 ak chyby
        return 0 if not errors else 1
        
    except Exception as e:
        error_msg = f"Kritická chyba v dennej rotácii: {e}"
        print(f"\n❌ {error_msg}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    exit_code = daily_rotation()
    sys.exit(exit_code)
