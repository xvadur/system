import sys
from pathlib import Path
from datetime import datetime

# Add workspace root to path
workspace_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(workspace_root))

def add_log_entry(action_name: str, status: str, files_changed: list = None, xp_estimate: float = None):
    """Pridá nový záznam do XVADUR_LOG.md.

    Args:
        action_name: Názov akcie (napr. "Implementácia session rotationu").
        status: Status akcie (napr. "Started", "Completed").
        files_changed: Zoznam zmienených súborov (voliteľné).
        xp_estimate: Odhad XP za dokončenie akcie (voliteľné).
    """
    log_path = workspace_root / "development" / "logs" / "XVADUR_LOG.md"
    current_time = datetime.now().strftime('%H:%M')

    log_entry = f"[{current_time}] 🔹 {action_name}\n"
    if files_changed:
        log_entry += "  - *Zmenené súbory:*\n"
        for f in files_changed:
            log_entry += f"    - {f}\n"
    log_entry += f"  - *Status:* {status}\n"
    if xp_estimate is not None:
        log_entry += f"  - *XP:* {xp_estimate}\n"

    try:
        with open(log_path, 'a', encoding='utf-8') as f:
            f.write(log_entry + "\n")
    except Exception as e:
        print(f"Error writing to XVADUR_LOG.md: {e}", file=sys.stderr)


if __name__ == "__main__":
    # Príklad použitia
    add_log_entry(
        action_name="Testovacia akcia",
        status="Started",
        files_changed=["file1.py", "file2.md"],
        xp_estimate=5.0
    )
    print("Testovacia akcia zalogovaná do XVADUR_LOG.md")
