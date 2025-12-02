#!/usr/bin/env python3
"""Automatic prompt saver - called from Cursor agent to save user prompts in real-time."""

import sys
import json
from pathlib import Path
from datetime import datetime

# Add workspace root to path
workspace_root = Path(__file__).parent.parent
sys.path.insert(0, str(workspace_root))

from ministers.memory import MinisterOfMemory, AssistantOfMemory
from ministers.storage import FileStore


def save_prompt(prompt_content: str, metadata: dict = None):
    """Save a user prompt to prompts_log.jsonl.
    
    Args:
        prompt_content: The user prompt text to save.
        metadata: Optional metadata dictionary.
    """
    try:
        prompts_log_path = workspace_root / "xvadur" / "data" / "prompts_log.jsonl"
        file_store = FileStore(prompts_log_path)
        assistant = AssistantOfMemory(store=file_store)
        minister = MinisterOfMemory(assistant=assistant)
        
        # Prepare metadata
        if metadata is None:
            metadata = {}
        
        metadata.update({
            'source': 'auto_save',
            'extraction_method': 'real_time_agent_hook',
            'saved_at': datetime.now().isoformat(),
        })
        
        # Save prompt
        minister.log_event(
            role='user',
            content=prompt_content,
            metadata=metadata,
        )
        
        return True
    except Exception as e:
        # Fail silently - don't break the conversation
        return False


def main():
    """Main entry point - accepts prompt from stdin or command line."""
    if len(sys.argv) > 1:
        # Prompt from command line arguments
        prompt_content = ' '.join(sys.argv[1:])
    else:
        # Prompt from stdin
        prompt_content = sys.stdin.read().strip()
    
    if not prompt_content:
        return
    
    success = save_prompt(prompt_content)
    if success:
        print(f"✅ Prompt saved ({len(prompt_content)} chars)", file=sys.stderr)
    else:
        print("⚠️ Failed to save prompt", file=sys.stderr)


if __name__ == "__main__":
    main()

