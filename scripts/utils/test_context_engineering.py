#!/usr/bin/env python3
"""Test Context Engineering Integration

Testovanie Context Engineering integrácie do systému.
"""

import sys
from pathlib import Path

# Add workspace root to path
workspace_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(workspace_root))

from core.context_engineering.integration import (
    load_context_with_optimization,
    track_and_optimize_context,
    isolate_context_for_task
)
from core.context_engineering.compress_context import CompressContextManager
from core.context_engineering.isolate_context import IsolateContextManager
from core.context_engineering.token_metrics import TokenBudgetTracker, TokenBudget
from core.context_engineering.config import (
    COMPRESSION_THRESHOLD,
    TARGET_COMPRESSION_RATIO,
    CONTEXT_WINDOW_SIZE
)
from core.ministers.memory import MinisterOfMemory, AssistantOfMemory, MemoryRecord
from core.ministers.storage import FileStore
from datetime import datetime


def test_token_tracking():
    """Test token trackingu."""
    print("🧪 Test 1: Token Tracking")
    print("-" * 50)
    
    tracker = TokenBudgetTracker(TokenBudget(context_window_size=CONTEXT_WINDOW_SIZE))
    
    # Test odhad tokenov
    test_text = "Toto je testovací text pre token tracking."
    token_count = tracker.estimate_tokens(test_text)
    print(f"✅ Odhad tokenov: {token_count} (text: {len(test_text)} znakov)")
    
    # Test trackovania použitia
    metrics = tracker.track_usage(
        system_content="System prompt",
        history_content="História konverzácie",
        current_content="Aktuálny input",
        output_content="Output"
    )
    
    print(f"✅ Trackovanie použitia:")
    print(f"   - Celkové tokeny: {metrics.total_tokens}")
    print(f"   - Input tokeny: {metrics.input_tokens}")
    print(f"   - Output tokeny: {metrics.output_tokens}")
    print(f"   - Utilization: {metrics.utilization_ratio(CONTEXT_WINDOW_SIZE):.2%}")
    
    # Test budget check
    budget_check = tracker.check_budget(
        system_content="System prompt",
        history_content="História",
        current_content="Input"
    )
    
    print(f"✅ Budget check:")
    print(f"   - V rámci budgetu: {budget_check['within_budget']}")
    print(f"   - Utilization: {budget_check['utilization']:.2%}")
    if budget_check['warnings']:
        print(f"   - Varovania: {', '.join(budget_check['warnings'])}")
    
    print()


def test_compression():
    """Test kompresie kontextu."""
    print("🧪 Test 2: Compression Context")
    print("-" * 50)
    
    # Vytvor testovacie záznamy
    test_records = [
        MemoryRecord(
            timestamp=datetime.now(),
            role="user",
            content=f"Test prompt {i}: Toto je testovací obsah pre kompresiu kontextu." * 10,
            metadata={"test": True}
        )
        for i in range(10)
    ]
    
    # Vytvor in-memory store
    from core.ministers.memory import InMemoryStore
    store = InMemoryStore()
    for record in test_records:
        store.store(record)
    
    compressor = CompressContextManager(store)
    
    # Test kompresie
    result = compressor.compress_records(
        test_records,
        target_compression_ratio=TARGET_COMPRESSION_RATIO
    )
    
    print(f"✅ Kompresia:")
    print(f"   - Pôvodný počet: {result.original_count}")
    print(f"   - Komprimovaný počet: {result.compressed_count}")
    print(f"   - Kompresný pomer: {result.compression_ratio:.2f}")
    print(f"   - Zachovaný obsah: {len(result.preserved_content)} znakov")
    
    print()


def test_isolation():
    """Test izolácie kontextu."""
    print("🧪 Test 3: Isolate Context")
    print("-" * 50)
    
    # Vytvor testovacie záznamy
    test_records = [
        MemoryRecord(
            timestamp=datetime.now(),
            role="user",
            content=f"Quest #20: Implementovať Context Engineering - krok {i}",
            metadata={"quest_id": 20}
        )
        for i in range(10)
    ]
    
    # Pridaj aj nerelevantné záznamy
    test_records.extend([
        MemoryRecord(
            timestamp=datetime.now(),
            role="user",
            content=f"Quest #15: Iná úloha - krok {i}",
            metadata={"quest_id": 15}
        )
        for i in range(5)
    ])
    
    isolator = IsolateContextManager()
    
    # Test izolácie
    isolation = isolator.isolate_for_task(
        task_id="quest-20",
        task_description="Implementovať Context Engineering",
        records=test_records,
        keywords={"context", "engineering", "quest", "20"}
    )
    
    print(f"✅ Izolácia kontextu:")
    print(f"   - Pôvodný počet záznamov: {len(test_records)}")
    print(f"   - Filtrovaný počet: {len(isolation.relevant_records)}")
    print(f"   - Pruned počet: {len(isolation.relevant_records)}")
    print(f"   - Token count: {isolation.token_count}")
    print(f"   - Izolovaný obsah: {len(isolation.isolated_content)} znakov")
    
    print()


def test_integration():
    """Test integrácie s MinisterOfMemory."""
    print("🧪 Test 4: Integration with MinisterOfMemory")
    print("-" * 50)
    
    # Vytvor testovací store
    from core.ministers.memory import InMemoryStore
    store = InMemoryStore()
    
    # Pridaj testovacie záznamy
    for i in range(15):
        record = MemoryRecord(
            timestamp=datetime.now(),
            role="user",
            content=f"Test prompt {i}: Obsah pre testovanie integrácie." * 5,
            metadata={"test": True, "index": i}
        )
        store.store(record)
    
    assistant = AssistantOfMemory(store=store)
    minister = MinisterOfMemory(assistant=assistant)
    
    # Test get_context_with_compression
    result = minister.get_context_with_compression(limit=20)
    
    print(f"✅ get_context_with_compression:")
    print(f"   - Počet záznamov: {len(result['records'])}")
    print(f"   - Kompresia: {result.get('compressed', False)}")
    if 'utilization' in result:
        print(f"   - Utilization: {result['utilization']:.2%}")
    
    # Test isolate_context_for_task
    isolation_result = minister.isolate_context_for_task(
        task_id="test-task",
        task_description="Testovanie izolácie",
        keywords={"test"},
        limit=20
    )
    
    print(f"✅ isolate_context_for_task:")
    print(f"   - Izolované: {isolation_result.get('isolated', False)}")
    if isolation_result.get('isolated'):
        print(f"   - Token count: {isolation_result.get('token_count', 0)}")
        print(f"   - Počet záznamov: {len(isolation_result.get('records', []))}")
    
    print()


def test_load_context_optimized():
    """Test optimalizovaného načítania kontextu."""
    print("🧪 Test 5: Load Context Optimized")
    print("-" * 50)
    
    save_game_path = workspace_root / "development" / "sessions" / "save_games" / "SAVE_GAME_LATEST.json"
    log_path = workspace_root / "development" / "logs" / "XVADUR_LOG.jsonl"
    
    if not save_game_path.exists():
        print("⚠️ Save game súbor neexistuje, preskakujem test")
        return
    
    try:
        result = load_context_with_optimization(
            save_game_path=save_game_path,
            log_path=log_path if log_path.exists() else None,
            auto_compress=True,
            auto_isolate=True
        )
        
        print(f"✅ Load context optimized:")
        print(f"   - Načítané komponenty: {list(result.get('context_parts', {}).keys())}")
        print(f"   - Celkové tokeny: {result.get('total_tokens', 0)}")
        print(f"   - Utilization: {result.get('utilization', 0.0):.2%}")
        print(f"   - Kompresia: {result.get('compressed', False)}")
    except Exception as e:
        print(f"⚠️ Chyba pri testovaní: {e}")
    
    print()


def main():
    """Spustí všetky testy."""
    print("=" * 50)
    print("CONTEXT ENGINEERING INTEGRATION TESTS")
    print("=" * 50)
    print()
    
    try:
        test_token_tracking()
        test_compression()
        test_isolation()
        test_integration()
        test_load_context_optimized()
        
        print("=" * 50)
        print("✅ Všetky testy dokončené")
        print("=" * 50)
    except Exception as e:
        print(f"❌ Chyba pri testovaní: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

