#!/usr/bin/env python3
"""Save all user prompts from current conversation to prompts_log.jsonl.

This script is called from /savegame command to ensure all prompts from the session are saved.
"""

import sys
import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any

# Add workspace root to path
workspace_root = Path(__file__).parent.parent
sys.path.insert(0, str(workspace_root))

from core.ministers.memory import MinisterOfMemory, AssistantOfMemory
from core.ministers.storage import FileStore
from core.context_engineering.token_metrics import TokenBudgetTracker, TokenBudget
from core.context_engineering.compress_context import CompressContextManager
from core.context_engineering.config import COMPRESSION_THRESHOLD, CONTEXT_WINDOW_SIZE


def get_existing_prompts() -> set:
    """Get set of existing prompt contents (for deduplication)."""
    prompts_log_path = workspace_root / "development" / "data" / "prompts_log.jsonl"
    existing = set()
    
    if prompts_log_path.exists():
        try:
            with open(prompts_log_path, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        try:
                            record = json.loads(line)
                            # Use content as key for deduplication
                            content = record.get('content', '')
                            if content:
                                existing.add(content.strip())
                        except json.JSONDecodeError:
                            continue
        except Exception:
            pass
    
    return existing


def save_prompts_batch(prompts: List[Dict[str, Any]]) -> int:
    """Save multiple prompts to prompts_log.jsonl.
    
    Args:
        prompts: List of prompt dictionaries with 'content' and optional 'metadata'
    
    Returns:
        Number of prompts actually saved (excluding duplicates)
    """
    if not prompts:
        return 0
    
    try:
        prompts_log_path = workspace_root / "development" / "data" / "prompts_log.jsonl"
        file_store = FileStore(prompts_log_path)
        assistant = AssistantOfMemory(store=file_store)
        minister = MinisterOfMemory(assistant=assistant)
        
        # Inicializuj token tracker
        tracker = TokenBudgetTracker(TokenBudget(context_window_size=CONTEXT_WINDOW_SIZE))
        
        existing = get_existing_prompts()
        saved_count = 0
        
        for prompt_data in prompts:
            content = prompt_data.get('content', '').strip()
            if not content:
                continue
            
            # Skip if already exists
            if content in existing:
                continue
            
            # Trackuj tokeny pred uložením
            token_count = tracker.estimate_tokens(content)
            
            metadata = prompt_data.get('metadata', {})
            metadata.update({
                'source': 'savegame_batch',
                'extraction_method': 'savegame_command',
                'saved_at': datetime.now().isoformat(),
                'token_count': token_count,
            })
            
            # Save prompt
            minister.log_event(
                role='user',
                content=content,
                metadata=metadata,
            )
            
            existing.add(content)  # Add to set to avoid duplicates in same batch
            saved_count += 1
        
        # Skontroluj utilization po uložení
        recent_records = minister.review_context(limit=50)
        if recent_records:
            history_content = "\n".join([r.to_summary() for r in recent_records])
            metrics = tracker.track_usage(history_content=history_content)
            utilization = metrics.utilization_ratio(CONTEXT_WINDOW_SIZE)
            
            # Ak je utilization vysoká, komprimuj
            if utilization > COMPRESSION_THRESHOLD:
                try:
                    compressor = CompressContextManager(file_store)
                    result = compressor.consolidate_memory(
                        limit=20,
                        target_compression_ratio=0.5
                    )
                    print(f"✅ Kompresia aplikovaná: {result.compression_ratio:.2f}", file=sys.stderr)
                except Exception as e:
                    print(f"⚠️ Chyba pri kompresii: {e}", file=sys.stderr)
        
        return saved_count
    except Exception as e:
        print(f"Error saving prompts: {e}", file=sys.stderr)
        return 0


def save_prompt(prompt_content: str, metadata: dict = None) -> bool:
    """Save a single prompt (wrapper for compatibility)."""
    if not prompt_content or not prompt_content.strip():
        return False
    
    prompts = [{
        'content': prompt_content,
        'metadata': metadata or {}
    }]
    
    return save_prompts_batch(prompts) > 0


def main():
    """Main entry point - accepts prompts from stdin (JSON array) or command line."""
    prompts_to_save = []
    
    if len(sys.argv) > 1:
        # Prompts from command line arguments (space-separated)
        for arg in sys.argv[1:]:
            if arg.strip():
                prompts_to_save.append({
                    'content': arg,
                    'metadata': {}
                })
    else:
        # Prompts from stdin (JSON array format)
        try:
            stdin_content = sys.stdin.read().strip()
            if stdin_content:
                # Try to parse as JSON array
                try:
                    prompts_data = json.loads(stdin_content)
                    if isinstance(prompts_data, list):
                        prompts_to_save = prompts_data
                    elif isinstance(prompts_data, dict):
                        prompts_to_save = [prompts_data]
                except json.JSONDecodeError:
                    # If not JSON, treat as single prompt
                    prompts_to_save = [{
                        'content': stdin_content,
                        'metadata': {}
                    }]
        except Exception:
            pass
    
    if not prompts_to_save:
        return
    
    saved_count = save_prompts_batch(prompts_to_save)
    if saved_count > 0:
        print(f"✅ Saved {saved_count} prompt(s) to prompts_log.jsonl", file=sys.stderr)
    else:
        print("ℹ️ No new prompts to save (all already exist)", file=sys.stderr)


if __name__ == "__main__":
    main()

