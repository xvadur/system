#!/usr/bin/env python3
"""Load Context Optimized - Python implementácia optimalizovaného načítania kontextu.

Tento skript poskytuje Python funkcie pre optimalizované načítanie kontextu
s automatickou kompresiou a izoláciou pomocou Context Engineering komponentov.
"""

import sys
import json
from pathlib import Path
from typing import Dict, Any, Optional, List

# Add workspace root to path
workspace_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(workspace_root))

from core.context_engineering.integration import (
    load_context_with_optimization,
    track_and_optimize_context,
    isolate_context_for_task,
    get_optimized_context_summary
)
from core.ministers.memory import MinisterOfMemory, AssistantOfMemory
from core.ministers.storage import FileStore
from scripts.utils.log_manager import get_optimized_log_context


def load_save_game_optimized(
    save_game_path: Optional[Path] = None,
    auto_compress: bool = True
) -> Dict[str, Any]:
    """Načíta save game s automatickou kompresiou.
    
    Args:
        save_game_path: Cesta k save game JSON súboru
        auto_compress: Automaticky komprimovať ak utilization > threshold
        
    Returns:
        Dictionary s načítaným save game a metrikami
    """
    if save_game_path is None:
        save_game_path = workspace_root / "development" / "sessions" / "save_games" / "SAVE_GAME_LATEST.json"
    
    if not save_game_path.exists():
        return {
            'error': f'Save game súbor neexistuje: {save_game_path}',
            'loaded': False
        }
    
    try:
        result = load_context_with_optimization(
            save_game_path=save_game_path,
            auto_compress=auto_compress
        )
        
        return {
            'loaded': True,
            'save_game': result.get('context_parts', {}).get('save_game', ''),
            'metrics': result.get('metrics', {}),
            'utilization': result.get('utilization', 0.0),
            'compressed': result.get('compressed', False)
        }
    except Exception as e:
        return {
            'error': str(e),
            'loaded': False
        }


def load_log_entries_optimized(
    log_path: Optional[Path] = None,
    limit: int = 5,
    auto_isolate: bool = True,
    task_description: Optional[str] = None,
    use_compression: bool = False
) -> Dict[str, Any]:
    """Načíta log entries s automatickou optimalizáciou pomocou Context Engineering.
    
    Používa get_optimized_log_context z log_manager.py pre token-efektívne načítanie.
    
    Args:
        log_path: Cesta k log JSONL súboru (ignorované, používa sa default z log_manager)
        limit: Počet záznamov na načítanie
        auto_isolate: Automaticky izolovať kontext pre úlohu (použité pre compression threshold)
        task_description: Popis úlohy pre izoláciu (voliteľné)
        use_compression: Použiť kompresiu ak je utilization vysoká
        
    Returns:
        Dictionary s načítanými log entries a metrikami
    """
    try:
        # Použi optimalizovaný log context z log_manager
        optimized_context = get_optimized_log_context(
            limit=limit,
            use_compression=use_compression or auto_isolate
        )
        
        if not optimized_context.get('entries'):
            return {
                'error': 'Žiadne log entries na načítanie',
                'loaded': False
            }
        
        # Konvertuj entries na text pre kompatibilitu
        log_content = "\n".join([
            f"[{e.get('date', '')} {e.get('time', '')}] {e.get('title', '')}"
            for e in optimized_context['entries']
        ])
        
        return {
            'loaded': True,
            'log_entries': log_content,
            'entries': optimized_context['entries'],
            'token_metrics': optimized_context.get('token_metrics'),
            'utilization': optimized_context.get('utilization', 0.0),
            'optimized': optimized_context.get('optimized', False)
        }
    except Exception as e:
        return {
            'error': str(e),
            'loaded': False
        }


def load_context_summary(
    prompts_log_path: Optional[Path] = None,
    limit: int = 10,
    include_compression: bool = True
) -> str:
    """Vráti optimalizovaný sumár kontextu pre AI.
    
    Args:
        prompts_log_path: Cesta k prompts_log.jsonl
        limit: Počet záznamov na sumarizáciu
        include_compression: Použiť kompresiu ak je potrebná
        
    Returns:
        Optimalizovaný sumár kontextu ako string
    """
    if prompts_log_path is None:
        prompts_log_path = workspace_root / "development" / "data" / "prompts_log.jsonl"
    
    if not prompts_log_path.exists():
        return "Žiadny prompts log na sumarizáciu."
    
    try:
        store = FileStore(prompts_log_path)
        summary = get_optimized_context_summary(
            store=store,
            limit=limit,
            include_compression=include_compression
        )
        return summary
    except Exception as e:
        return f"Chyba pri sumarizácii: {e}"


def main():
    """Main entry point - demonštrácia použitia."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Načíta optimalizovaný kontext')
    parser.add_argument('--save-game', action='store_true', help='Načíta save game')
    parser.add_argument('--log', action='store_true', help='Načíta log entries')
    parser.add_argument('--summary', action='store_true', help='Vráti sumár kontextu')
    parser.add_argument('--task', type=str, help='Popis úlohy pre izoláciu')
    parser.add_argument('--limit', type=int, default=10, help='Počet záznamov')
    parser.add_argument('--json', action='store_true', help='Výstup v JSON formáte')
    
    args = parser.parse_args()
    
    results = {}
    
    if args.save_game:
        result = load_save_game_optimized()
        results['save_game'] = result
    
    if args.log:
        result = load_log_entries_optimized(
            limit=args.limit,
            task_description=args.task
        )
        results['log'] = result
    
    if args.summary:
        summary = load_context_summary(limit=args.limit)
        results['summary'] = summary
    
    if args.json:
        print(json.dumps(results, indent=2, ensure_ascii=False, default=str))
    else:
        for key, value in results.items():
            print(f"\n=== {key.upper()} ===")
            if isinstance(value, str):
                print(value)
            else:
                print(json.dumps(value, indent=2, ensure_ascii=False, default=str))


if __name__ == "__main__":
    main()

