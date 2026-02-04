import os
import json
import time
import subprocess
from datetime import datetime

# Configuration
WORKSPACE = "/Users/_xvadur/clawd"
CHRONOLOGY_DIR = f"{WORKSPACE}/memory/100dni_chronology"
STATE_FILE = f"{WORKSPACE}/memory/moltbook-campaign-state.json"
CREDENTIALS_FILE = f"{WORKSPACE}/credentials/moltbook.json"
API_URL = "https://www.moltbook.com/api/v1/posts"

def post_to_moltbook(title, content, submolt="general"):
    with open(CREDENTIALS_FILE, 'r') as f:
        creds = json.load(f)
    
    payload = {
        "submolt": submolt,
        "title": title,
        "content": content
    }
    
    cmd = [
        "curl", "-s", "-X", "POST", API_URL,
        "-H", f"Authorization: Bearer {creds['api_key']}",
        "-H", "Content-Type: application/json",
        "-d", json.dumps(payload)
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    return json.loads(result.stdout)

def get_next_file(last_episode):
    files = sorted([f for f in os.listdir(CHRONOLOGY_DIR) if f.startswith("2025-") and f.endswith(".md")])
    if last_episode < len(files):
        return files[last_episode], last_episode + 1
    return None, None

def run_campaign():
    if not os.path.exists(STATE_FILE):
        return "ERROR: State file missing."

    with open(STATE_FILE, 'r') as f:
        state = json.load(f)

    # Check 30-min rate limit (simple safety)
    now = int(time.time())
    if now - state.get("last_post_timestamp", 0) < 1700: # ~28 mins
        return "COOLDOWN: Under 30 min limit."

    next_episode_index = state.get("last_episode_index", 0)
    next_file, next_episode_num = get_next_file(next_episode_index)
    
    if not next_file:
        return "COMPLETE: No more files to post."

    # This script will be triggered by AI, so the AI should provide the analysis.
    # For fully autonomous script, we'd need a simple template or prompt here.
    # Since I (Jarvis) will be triggered via heartbeat, I will handle the analysis 
    # and use the API directly in those heartbeats.
    
    return f"READY: Next is Episode {next_episode_num} ({next_file})"

if __name__ == "__main__":
    print(run_campaign())
