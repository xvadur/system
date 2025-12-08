#!/usr/bin/env python3
"""
Denná rotácia: Archivácia + nová session + metriky + git push
Spúšťa sa každú polnoc automaticky cez macOS launchd.

Tento skript:
1. Archivuje včerajšiu session
2. Vytvorí novú session
3. Vypočíta denné metriky
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
from scripts.generate_daily_review import generate_daily_review
from scripts.calculate_xp import calculate_xp, update_xp_file
from scripts.utils.log_manager import add_log_entry
from scripts.utils.git_helper import git_push_changes

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
        print("\n📦 Krok 1/5: Archivácia včerajšej session...")
        try:
            archive_current_session()
            print("✅ Archivácia dokončená")
        except Exception as e:
            error_msg = f"Archivácia zlyhala: {e}"
            errors.append(error_msg)
            print(f"❌ {error_msg}", file=sys.stderr)
        
        # 2. Vytvorenie novej session
        print("\n🆕 Krok 2/5: Vytvorenie novej session...")
        try:
            create_new_session()
            print("✅ Nová session vytvorená")
        except Exception as e:
            error_msg = f"Vytvorenie session zlyhalo: {e}"
            errors.append(error_msg)
            print(f"❌ {error_msg}", file=sys.stderr)
        
        # 3. Generovanie denného review
        print("\n📊 Krok 3/5: Generovanie denného review...")
        try:
            generate_daily_review()
            print("✅ Review vygenerované")
        except Exception as e:
            error_msg = f"Generovanie review zlyhalo: {e}"
            errors.append(error_msg)
            print(f"⚠️  {error_msg} (nie kritické)", file=sys.stderr)
        
        # 4. Výpočet XP
        print("\n🎮 Krok 4/5: Výpočet denných metrík a XP...")
        try:
            prompts_log_path = workspace_root / "development" / "data" / "prompts_log.jsonl"
            log_path = workspace_root / "development" / "logs" / "XVADUR_LOG.md"
            
            if prompts_log_path.exists() and log_path.exists():
                xp_data = calculate_xp(str(prompts_log_path), str(log_path))
                update_xp_file(
                    str(workspace_root / "development" / "logs" / "XVADUR_XP.md"),
                    xp_data
                )
                print(f"✅ XP vypočítané: {xp_data.get('total_xp', 0)} (Level {xp_data.get('current_level', 1)})")
            else:
                print("⚠️  Súbory pre XP výpočet neexistujú (nie kritické)")
        except Exception as e:
            error_msg = f"Výpočet XP zlyhal: {e}"
            errors.append(error_msg)
            print(f"⚠️  {error_msg} (nie kritické)", file=sys.stderr)
        
        # 5. Git push na GitHub
        print("\n🚀 Krok 5/5: Push zmien na GitHub...")
        try:
            commit_message = f"chore(daily): automatická rotácia {datetime.now().strftime('%Y-%m-%d')}"
            if git_push_changes(commit_message):
                print("✅ Zmeny pushnuté na GitHub")
            else:
                error_msg = "Git push zlyhal"
                errors.append(error_msg)
                print(f"⚠️  {error_msg} (skús manuálne)", file=sys.stderr)
        except Exception as e:
            error_msg = f"Git push zlyhal: {e}"
            errors.append(error_msg)
            print(f"⚠️  {error_msg} (skús manuálne)", file=sys.stderr)
        
        # Finálne logovanie
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
        
        # Log do XVADUR_LOG.md
        add_log_entry(
            action_name=f"Denná rotácia {datetime.now().strftime('%Y-%m-%d')}",
            status="Completed" if not errors else "Completed with warnings",
            xp_estimate=15.0
        )
        
        # Exit code: 0 ak OK, 1 ak chyby
        return 0 if not errors else 1
        
    except Exception as e:
        error_msg = f"Kritická chyba v dennej rotácii: {e}"
        print(f"\n❌ {error_msg}", file=sys.stderr)
        add_log_entry(
            action_name=f"Denná rotácia {datetime.now().strftime('%Y-%m-%d')}",
            status="Failed",
            xp_estimate=0.0
        )
        return 1

if __name__ == "__main__":
    exit_code = daily_rotation()
    sys.exit(exit_code)


