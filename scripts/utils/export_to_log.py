"""Export prompts from MinisterOfMemory to XVADUR_LOG.md.

This script synchronizes prompts stored in the memory system with
the markdown log file for human-readable format.
"""

import logging
import sys
from datetime import datetime
from pathlib import Path

# Add workspace root to path
workspace_root = Path(__file__).parent.parent
sys.path.insert(0, str(workspace_root))

from core.ministers.memory import AssistantOfMemory, MinisterOfMemory
from core.ministers.storage import FileStore
from core.context_engineering.compress_context import CompressContextManager
from core.context_engineering.isolate_context import IsolateContextManager

logger = logging.getLogger(__name__)


def export_prompts_to_log(
    prompts_log_path: Path,
    log_file_path: Path,
    limit: int = 50,
    append: bool = True,
) -> None:
    """Export prompts from MinisterOfMemory to markdown log.
    
    Args:
        prompts_log_path: Path to prompts_log.jsonl file.
        log_file_path: Path to XVADUR_LOG.md file.
        limit: Maximum number of prompts to export.
        append: If True, append to existing log. If False, create new section.
    """
    if not prompts_log_path.exists():
        logger.warning(f"Prompts log not found: {prompts_log_path}")
        return
    
    # Initialize memory system
    file_store = FileStore(prompts_log_path)
    assistant = AssistantOfMemory(store=file_store)
    minister = MinisterOfMemory(assistant=assistant)
    
    # Get recent prompts
    recent_prompts = minister.review_context(limit=limit)
    
    if not recent_prompts:
        logger.info("No prompts to export")
        return
    
    # Optimalizuj pomocou Compress Context ak je promptov veľa
    if len(recent_prompts) > 30:
        try:
            compressor = CompressContextManager(file_store)
            compression_result = compressor.compress_records(
                recent_prompts,
                target_compression_ratio=0.6  # Menej agresívna kompresia pre export
            )
            logger.info(f"Kompresia aplikovaná pre export: {compression_result.compression_ratio:.2f}")
        except Exception as e:
            logger.warning(f"Chyba pri kompresii pre export: {e}")
    
    # Použi Isolate Context pre relevantný kontext
    try:
        isolator = IsolateContextManager()
        # Izoluj kontext pre "export" úlohu
        isolation = isolator.isolate_for_task(
            task_id="export_to_log",
            task_description="Export promptov do logu",
            records=recent_prompts[-20:],  # Použi posledných 20 pre izoláciu
            keywords={"prompt", "export", "log"}
        )
        # Použi izolované záznamy ak sú dostupné
        if isolation.relevant_records:
            recent_prompts = isolation.relevant_records
            logger.info(f"Izolovaný kontext: {len(recent_prompts)} relevantných záznamov")
    except Exception as e:
        logger.warning(f"Chyba pri izolácii kontextu: {e}")
    
    # Generate log entry
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    log_entry = f"\n## [{timestamp}] 🔹 Prompty z MinisterOfMemory\n\n"
    log_entry += f"**Kontext:** Export promptov z pasívneho memory systému.\n\n"
    log_entry += f"**Počet promptov:** {len(recent_prompts)}\n\n"
    log_entry += "**Posledné prompty:**\n\n"
    
    for i, record in enumerate(recent_prompts[-10:], 1):  # Show last 10
        log_entry += f"{i}. **[{record.timestamp.strftime('%Y-%m-%d %H:%M')}]** ({record.role})\n"
        log_entry += f"   {record.content[:200]}{'...' if len(record.content) > 200 else ''}\n\n"
    
    log_entry += "---\n"
    
    # Append to log file
    log_file_path.parent.mkdir(parents=True, exist_ok=True)
    
    if append and log_file_path.exists():
        with open(log_file_path, 'a', encoding='utf-8') as f:
            f.write(log_entry)
    else:
        # Create new section at the end
        with open(log_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        with open(log_file_path, 'w', encoding='utf-8') as f:
            f.write(content)
            f.write(log_entry)
    
    logger.info(f"Exported {len(recent_prompts)} prompts to {log_file_path}")


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Export prompts to log')
    parser.add_argument(
        '--prompts-log',
        type=Path,
        default=workspace_root / 'xvadur' / 'data' / 'prompts_log.jsonl',
        help='Path to prompts log file',
    )
    parser.add_argument(
        '--log-file',
        type=Path,
        default=workspace_root / 'xvadur' / 'logs' / 'XVADUR_LOG.md',
        help='Path to log file',
    )
    parser.add_argument(
        '--limit',
        type=int,
        default=50,
        help='Maximum number of prompts to export',
    )
    args = parser.parse_args()
    
    logging.basicConfig(level=logging.INFO)
    
    export_prompts_to_log(
        prompts_log_path=args.prompts_log,
        log_file_path=args.log_file,
        limit=args.limit,
    )


if __name__ == "__main__":
    main()

