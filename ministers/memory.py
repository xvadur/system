"""Premier-level memory minister facade for AetheroOS.

This module provides a constitutional wrapper around the core
`core.ministers.memory` implementations so the Premier can orchestrate
memory duties while keeping persistent storage configuration explicit.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
import logging
from pathlib import Path
from typing import Any, Callable, Dict, Iterable, List, Optional

from core.ministers.memory import (
    AssistantOfMemory as CoreAssistantOfMemory,
    InMemoryStore,
    MemoryRecord,
    MemoryStore,
    MinisterOfMemory as CoreMinisterOfMemory,
)
from core.ministers.storage import FileStore

logger = logging.getLogger(__name__)


# AETH: Capture the intent that drives ministerial orchestration.
@dataclass
class MemoryIntent:
    """Declarative intent for configuring the minister's storage."""

    persistent_path: Optional[Path] = None
    summarize_limit: int = 10
    metadata: Dict[str, Any] = field(default_factory=dict)


# AETH: Extend the assistant to expose architecture cues for orchestration.
class AssistantOfMemory(CoreAssistantOfMemory):
    """Assistant enriched with self-description for orchestration traces."""

    def __init__(
        self,
        store: MemoryStore | None = None,
        summarizer: Callable[[Iterable[MemoryRecord]], str] | None = None,
        audit_log: List[str] | None = None,
    ) -> None:
        # AETH: Favor explicit store injection to keep state management observable.
        super().__init__(store=store or InMemoryStore(), summarizer=summarizer)
        self.audit_log: List[str] = audit_log or []

    # AETH: Keep a lightweight note for every tactical decision.
    def note(self, message: str) -> None:
        timestamp = datetime.utcnow().isoformat()
        entry = f"[{timestamp}] {message}"
        logger.debug("Assistant audit note: %s", entry)
        self.audit_log.append(entry)

    # AETH: Expose the current storage implementation for routing transparency.
    def describe_store(self) -> str:
        return type(self.store).__name__


# AETH: Premier-level minister that binds storage intent to execution.
class MinisterOfMemory(CoreMinisterOfMemory):
    """Premier facade that wires storage intent to the core minister logic."""

    def __init__(
        self,
        intent: MemoryIntent | None = None,
        assistant: AssistantOfMemory | None = None,
    ) -> None:
        self.intent = intent or MemoryIntent()
        # AETH: Determine the storage backend based on declared intent.
        if assistant is None:
            store = self._resolve_store(self.intent)
            assistant = AssistantOfMemory(store=store)
            assistant.note("Initialized assistant via Premier facade")
        super().__init__(assistant=assistant)

    # AETH: Centralize storage selection for clarity and future MCP hooks.
    def _resolve_store(self, intent: MemoryIntent) -> MemoryStore:
        if intent.persistent_path:
            logger.info("Minister selecting FileStore at %s", intent.persistent_path)
            return FileStore(intent.persistent_path)
        logger.info("Minister selecting volatile InMemoryStore")
        return InMemoryStore()

    # AETH: Provide a concise architectural snapshot for diagnostics.
    def architecture_snapshot(self) -> Dict[str, Any]:
        store = self.assistant.store
        snapshot: Dict[str, Any] = {
            "store_type": type(store).__name__,
            "intent": {
                "persistent_path": str(self.intent.persistent_path) if self.intent.persistent_path else None,
                "summarize_limit": self.intent.summarize_limit,
                "metadata": self.intent.metadata,
            },
            "audit_entries": list(getattr(self.assistant, "audit_log", [])),
        }

        # AETH: Surface record counts when the backend supports it.
        if isinstance(store, FileStore):
            snapshot["records"] = store.get_record_count()
        elif hasattr(store, "_records"):
            snapshot["records"] = len(getattr(store, "_records", []))
        return snapshot

    # AETH: Lightweight state export without heavy context tokens.
    def export_recent(self, limit: int | None = None) -> List[Dict[str, Any]]:
        records = self.assistant.recall_recent(limit=limit or self.intent.summarize_limit)
        return [
            {
                "timestamp": record.timestamp.isoformat(),
                "role": record.role,
                "content": record.content,
                "metadata": record.metadata,
            }
            for record in records
        ]


__all__ = ["AssistantOfMemory", "MemoryIntent", "MinisterOfMemory"]
