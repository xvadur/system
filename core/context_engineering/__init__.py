"""Context Engineering Integration Module

Tento modul integruje praktiky z Context-Engineering repozitára:
- Compress Context (recursive memory consolidation)
- Isolate Context (task-based isolation)
- Cognitive Tools (modular reasoning)
- Metrics & Evaluation (token tracking)
"""

from .compress_context import CompressContextManager
from .isolate_context import IsolateContextManager
from .cognitive_tools import CognitiveTool, PromptProgram
from .token_metrics import TokenBudgetTracker, TokenMetrics
from .integration import (
    load_context_with_optimization,
    track_and_optimize_context,
    isolate_context_for_task,
    get_optimized_context_summary
)
from .config import (
    COMPRESSION_THRESHOLD,
    TARGET_COMPRESSION_RATIO,
    CONTEXT_WINDOW_SIZE,
    ISOLATION_MAX_TOKENS
)

__all__ = [
    "CompressContextManager",
    "IsolateContextManager",
    "CognitiveTool",
    "PromptProgram",
    "TokenBudgetTracker",
    "TokenMetrics",
    "load_context_with_optimization",
    "track_and_optimize_context",
    "isolate_context_for_task",
    "get_optimized_context_summary",
    "COMPRESSION_THRESHOLD",
    "TARGET_COMPRESSION_RATIO",
    "CONTEXT_WINDOW_SIZE",
    "ISOLATION_MAX_TOKENS",
]

