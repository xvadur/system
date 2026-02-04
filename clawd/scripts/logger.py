import json
import os
from datetime import datetime

LOG_FILE = "/Users/_xvadur/clawd/memory/daily_logs.json"

def add_log(activity, category, energy, note, xp, timestamp=None):
    if not timestamp:
        timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    
    new_entry = {
        "timestamp": timestamp,
        "activity": activity,
        "category": category,
        "energy": int(energy),
        "note": note,
        "xp": int(xp)
    }

    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            try:
                logs = json.load(f)
            except json.JSONDecodeError:
                logs = []
    else:
        logs = []

    logs.append(new_entry)

    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(logs, f, indent=2, ensure_ascii=False)
    
    print(f"Log added: {activity} at {timestamp}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 5:
        add_log(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6] if len(sys.argv) > 6 else None)
