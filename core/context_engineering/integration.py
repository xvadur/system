"""Context Engineering Integration Helper

Centralizovaný helper modul pre integráciu Context Engineering do workflow.
Poskytuje wrapper funkcie pre automatickú optimalizáciu tokenov.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any, Dict, List, Optional

from core.ministers.memory import MemoryRecord, MemoryStore, MinisterOfMemory, AssistantOfMemory
from core.ministers.storage import FileStore
from core.context_engineering.compress_context import CompressContextManager
from core.context_engineering.isolate_context import IsolateContextManager, ContextIsolation
from core.context_engineering.token_metrics import TokenBudgetTracker, TokenBudget, TokenMetrics
from core.context_engineering.config import (
    COMPRESSION_THRESHOLD,
    TARGET_COMPRESSION_RATIO,
    CONTEXT_WINDOW_SIZE,
    ISOLATION_MAX_TOKENS
)

logger = logging.getLogger(__name__)


def load_context_with_optimization(
    save_game_path: Optional[Path] = None,
    log_path: Optional[Path] = None,
    xp_path: Optional[Path] = None,
    profile_path: Optional[Path] = None,
    prompts_log_path: Optional[Path] = None,
    auto_compress: bool = True,
    auto_isolate: bool = True
) -> Dict[str, Any]:
    """Načíta kontext s automatickou optimalizáciou tokenov.
    
    Wrapper pre `/loadgame` command s automatickou optimalizáciou pomocou
    Context Engineering komponentov.
    
    Args:
        save_game_path: Cesta k save game JSON súboru
        log_path: Cesta k log JSONL súboru
        xp_path: Cesta k XP JSON súboru
        profile_path: Cesta k profilu Markdown súboru
        prompts_log_path: Cesta k prompts_log.jsonl
        auto_compress: Automaticky komprimovať ak utilization > threshold
        auto_isolate: Automaticky izolovať kontext pre nové questy
        
    Returns:
        Dictionary s načítaným kontextom a metrikami
    """
    logger.info("Načítavam kontext s optimalizáciou")
    
    # Inicializuj tracker
    tracker = TokenBudgetTracker(TokenBudget(context_window_size=CONTEXT_WINDOW_SIZE))
    
    # Načítaj komponenty
    context_parts = {}
    total_content = ""
    
    # 1. Save Game
    if save_game_path and save_game_path.exists():
        try:
            import json
            with open(save_game_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # Extrahuj len kľúčové informácie
                save_game_content = f"""
Status: {data.get('status', {})}
Summary: {data.get('narrative', {}).get('summary', '')[:500]}
Active Quests: {len(data.get('quests', []))}
"""
                context_parts['save_game'] = save_game_content
                total_content += save_game_content
        except Exception as e:
            logger.warning(f"Chyba pri načítaní save game: {e}")
    
    # 2. Log entries
    if log_path and log_path.exists():
        try:
            import json
            entries = []
            with open(log_path, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        entries.append(json.loads(line))
            
            # Vezmi posledných 5
            recent_entries = entries[-5:] if len(entries) > 5 else entries
            log_content = "\n".join([
                f"[{e.get('date', '')} {e.get('time', '')}] {e.get('title', '')}"
                for e in recent_entries
            ])
            context_parts['log'] = log_content
            total_content += log_content
        except Exception as e:
            logger.warning(f"Chyba pri načítaní logu: {e}")
    
    # 3. XP Status
    if xp_path and xp_path.exists():
        try:
            import json
            with open(xp_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                xp_content = f"XP Status: {data.get('status', {})}"
                context_parts['xp'] = xp_content
                total_content += xp_content
        except Exception as e:
            logger.warning(f"Chyba pri načítaní XP: {e}")
    
    # 4. Profil (voliteľné)
    if profile_path and profile_path.exists():
        try:
            content = profile_path.read_text(encoding='utf-8')
            # Extrahuj len sekciu "IV. SÚČASNÝ PROFIL"
            profile_start = content.find("## IV. SÚČASNÝ PROFIL")
            if profile_start != -1:
                profile_end = content.find("##", profile_start + 1)
                profile_content = content[profile_start:profile_end] if profile_end != -1 else content[profile_start:]
                context_parts['profile'] = profile_content[:1000]  # Limit na ~1000 znakov
                total_content += profile_content[:1000]
        except Exception as e:
            logger.warning(f"Chyba pri načítaní profilu: {e}")
    
    # 5. Prompts z MinisterOfMemory (voliteľné)
    if prompts_log_path and prompts_log_path.exists():
        try:
            store = FileStore(prompts_log_path)
            assistant = AssistantOfMemory(store=store)
            minister = MinisterOfMemory(assistant=assistant)
            
            recent_prompts = minister.review_context(limit=10)
            if recent_prompts:
                prompts_content = "\n".join([
                    f"[{r.timestamp.isoformat()}] {r.role}: {r.content[:100]}"
                    for r in recent_prompts
                ])
                context_parts['prompts'] = prompts_content
                total_content += prompts_content
        except Exception as e:
            logger.warning(f"Chyba pri načítaní promptov: {e}")
    
    # Trackuj tokeny
    metrics = tracker.track_usage(
        system_content="",  # System prompt nie je súčasťou kontextu
        history_content=total_content,
        current_content="",
        output_content=""
    )
    
    utilization = metrics.utilization_ratio(CONTEXT_WINDOW_SIZE)
    
    # Automatická kompresia ak je utilization vysoká
    compressed = False
    if auto_compress and utilization > COMPRESSION_THRESHOLD:
        logger.info(f"Utilization {utilization:.2%} > {COMPRESSION_THRESHOLD:.2%}, komprimujem...")
        
        if prompts_log_path and prompts_log_path.exists():
            try:
                store = FileStore(prompts_log_path)
                compressor = CompressContextManager(store)
                result = compressor.consolidate_memory(
                    limit=20,
                    target_compression_ratio=TARGET_COMPRESSION_RATIO
                )
                logger.info(f"Kompresia dokončená: {result.compression_ratio:.2f}")
                compressed = True
            except Exception as e:
                logger.warning(f"Chyba pri kompresii: {e}")
    
    return {
        'context_parts': context_parts,
        'metrics': metrics.to_dict(),
        'utilization': utilization,
        'compressed': compressed,
        'total_tokens': metrics.total_tokens,
        'context_window_size': CONTEXT_WINDOW_SIZE
    }


def track_and_optimize_context(
    store: MemoryStore,
    system_content: str = "",
    history_content: str = "",
    current_content: str = "",
    output_content: str = ""
) -> Dict[str, Any]:
    """Trackuje a optimalizuje kontext automaticky.
    
    Args:
        store: MemoryStore pre prístup k záznamom
        system_content: System prompt obsah
        history_content: História konverzácie
        current_content: Aktuálny user input
        output_content: Output obsah
        
    Returns:
        Dictionary s metrikami a optimalizačnými výsledkami
    """
    logger.info("Trackujem a optimalizujem kontext")
    
    # Inicializuj tracker
    tracker = TokenBudgetTracker(TokenBudget(context_window_size=CONTEXT_WINDOW_SIZE))
    
    # Trackuj použitie
    metrics = tracker.track_usage(
        system_content=system_content,
        history_content=history_content,
        current_content=current_content,
        output_content=output_content
    )
    
    utilization = metrics.utilization_ratio(CONTEXT_WINDOW_SIZE)
    
    # Skontroluj budget
    budget_check = tracker.check_budget(
        system_content=system_content,
        history_content=history_content,
        current_content=current_content
    )
    
    # Automatická kompresia ak je utilization vysoká
    compression_result = None
    if utilization > COMPRESSION_THRESHOLD:
        logger.info(f"Utilization {utilization:.2%} > {COMPRESSION_THRESHOLD:.2%}, komprimujem...")
        
        compressor = CompressContextManager(store)
        compression_result = compressor.consolidate_memory(
            limit=20,
            target_compression_ratio=TARGET_COMPRESSION_RATIO
        )
        logger.info(f"Kompresia dokončená: {compression_result.compression_ratio:.2f}")
    
    return {
        'metrics': metrics.to_dict(),
        'utilization': utilization,
        'budget_check': budget_check,
        'compression_result': {
            'compressed': compression_result is not None,
            'compression_ratio': compression_result.compression_ratio if compression_result else None,
            'original_count': compression_result.original_count if compression_result else None,
            'compressed_count': compression_result.compressed_count if compression_result else None
        } if compression_result else None
    }


def isolate_context_for_task(
    task_id: str,
    task_description: str,
    records: List[MemoryRecord],
    keywords: Optional[set] = None,
    max_tokens: Optional[int] = None
) -> ContextIsolation:
    """Izoluje kontext pre konkrétnu úlohu.
    
    Args:
        task_id: ID úlohy
        task_description: Popis úlohy
        records: Zoznam záznamov na filtrovanie
        keywords: Kľúčové slová (voliteľné)
        max_tokens: Maximálny počet tokenov (voliteľné)
        
    Returns:
        ContextIsolation s izolovaným obsahom
    """
    logger.info(f"Izolujem kontext pre úlohu: {task_id}")
    
    isolator = IsolateContextManager()
    
    if max_tokens is None:
        max_tokens = ISOLATION_MAX_TOKENS
    
    isolation = isolator.isolate_for_task(
        task_id=task_id,
        task_description=task_description,
        records=records,
        keywords=keywords
    )
    
    # Ak je to stále príliš veľa, zníž ešte viac
    if isolation.token_count > max_tokens:
        reduction_ratio = max_tokens / isolation.token_count
        target_count = int(len(isolation.relevant_records) * reduction_ratio)
        
        pruned_records = isolation.relevant_records[-target_count:]
        isolation = isolator.isolate_for_task(
            task_id=task_id,
            task_description=task_description,
            records=pruned_records,
            keywords=keywords
        )
    
    return isolation


def get_optimized_context_summary(
    store: MemoryStore,
    limit: int = 10,
    include_compression: bool = True
) -> str:
    """Vráti optimalizovaný sumár kontextu.
    
    Args:
        store: MemoryStore pre prístup k záznamom
        limit: Počet záznamov na sumarizáciu
        include_compression: Použiť kompresiu ak je potrebná
        
    Returns:
        Optimalizovaný sumár kontextu ako string
    """
    logger.info(f"Generujem optimalizovaný sumár kontextu (limit={limit})")
    
    # Získaj záznamy
    records = store.latest(limit=limit)
    
    if not records:
        return "Žiadny kontext na sumarizáciu."
    
    # Trackuj tokeny
    tracker = TokenBudgetTracker()
    content = "\n".join([r.to_summary() for r in records])
    metrics = tracker.track_usage(history_content=content)
    
    utilization = metrics.utilization_ratio(CONTEXT_WINDOW_SIZE)
    
    # Komprimuj ak je utilization vysoká
    if include_compression and utilization > COMPRESSION_THRESHOLD:
        compressor = CompressContextManager(store)
        result = compressor.compress_records(
            records,
            target_compression_ratio=TARGET_COMPRESSION_RATIO
        )
        return result.preserved_content
    
    # Inak vráť normálny sumár
    return "\n".join([r.to_summary() for r in records])

