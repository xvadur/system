#!/usr/bin/env python3
"""Automatic prompt saver - called from Cursor agent to save user prompts in real-time."""

import sys
import json
from pathlib import Path
from datetime import datetime
import subprocess
import os

# Add workspace root to path
workspace_root = Path(__file__).parent.parent
sys.path.insert(0, str(workspace_root))

from core.ministers.memory import MinisterOfMemory, AssistantOfMemory
from core.ministers.storage import FileStore
from core.context_engineering.token_metrics import TokenBudgetTracker, TokenBudget
from core.context_engineering.compress_context import CompressContextManager
from core.context_engineering.config import COMPRESSION_THRESHOLD, CONTEXT_WINDOW_SIZE


def get_current_time_from_mcp(timezone: str = "Europe/Bratislava") -> datetime:
    """Získa aktuálny čas z MCP Time MCP servera.
    
    Args:
        timezone: Časová zóna (default: Europe/Bratislava)
        
    Returns:
        datetime objekt so správnym časom, alebo fallback na datetime.now()
    """
    try:
        # Pokúsi sa získať čas cez MCP Time MCP
        # MCP Time MCP je dostupný cez MCP Docker systém
        # Použijeme subprocess na volanie MCP nástroja cez curl alebo podobne
        # Alebo jednoducho použijeme správnu časovú zónu v Python
        
        # Pre teraz použijeme timezone-aware datetime
        from zoneinfo import ZoneInfo
        return datetime.now(ZoneInfo(timezone))
    except ImportError:
        # Fallback pre staršie Python verzie (< 3.9)
        try:
            import pytz
            tz = pytz.timezone(timezone)
            return datetime.now(tz)
        except ImportError:
            # Ak nie sú dostupné timezone knižnice, použijeme UTC
            return datetime.utcnow()
    except Exception as e:
        # Ak zlyhá, použijeme fallback
        print(f"⚠️ MCP Time error: {e}, using fallback", file=sys.stderr)
        return datetime.now()


def save_prompt(prompt_content: str, metadata: dict = None):
    """Save a user prompt to prompts_log.jsonl.
    
    Args:
        prompt_content: The user prompt text to save.
        metadata: Optional metadata dictionary.
    """
    try:
        prompts_log_path = workspace_root / "development" / "data" / "prompts_log.jsonl"
        file_store = FileStore(prompts_log_path)
        assistant = AssistantOfMemory(store=file_store)
        minister = MinisterOfMemory(assistant=assistant)
        
        # Prepare metadata
        if metadata is None:
            metadata = {}
        
        # Získaj správny čas z MCP Time MCP (alebo použij správnu časovú zónu)
        current_time = get_current_time_from_mcp()
        
        metadata.update({
            'source': 'auto_save',
            'extraction_method': 'real_time_agent_hook',
            'saved_at': current_time.isoformat(),
        })
        
        # Trackuj tokeny pred uložením
        tracker = TokenBudgetTracker(TokenBudget(context_window_size=CONTEXT_WINDOW_SIZE))
        token_count = tracker.estimate_tokens(prompt_content)
        metadata['token_count'] = token_count
        
        # Save prompt so správnym timestampom
        minister.log_event(
            role='user',
            content=prompt_content,
            metadata=metadata,
            timestamp=current_time,  # Použi správny timestamp
        )
        
        # Skontroluj utilization po uložení
        try:
            recent_records = minister.review_context(limit=50)
            if recent_records:
                history_content = "\n".join([r.to_summary() for r in recent_records])
                metrics = tracker.track_usage(history_content=history_content)
                utilization = metrics.utilization_ratio(CONTEXT_WINDOW_SIZE)
                
                # Ak je utilization vysoká, komprimuj automaticky
                if utilization > COMPRESSION_THRESHOLD:
                    compressor = CompressContextManager(file_store)
                    result = compressor.consolidate_memory(
                        limit=20,
                        target_compression_ratio=0.5
                    )
                    print(f"✅ Automatická kompresia: {result.compression_ratio:.2f} ({utilization:.1%} utilization)", file=sys.stderr)
        except Exception as e:
            # Ignoruj chyby pri kompresii - nech to nepreruší ukladanie
            pass
        
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

