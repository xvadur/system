import subprocess
import os
from datetime import datetime

SAVE_DIR = "/Users/_xvadur/clawd/memory/evidence"

def take_screenshot():
    if not os.path.exists(SAVE_DIR):
        os.makedirs(SAVE_DIR)
    
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filepath = os.path.join(SAVE_DIR, f"screenshot_{timestamp}.png")
    
    try:
        # Použijeme macOS natívny screencapture
        subprocess.run(["screencapture", "-x", filepath], check=True)
        print(f"Screenshot saved: {filepath}")
        return filepath
    except Exception as e:
        print(f"Error taking screenshot: {e}")
        return None

if __name__ == "__main__":
    take_screenshot()
