"""AetheroOS ministerial memory agent.

This module introduces the MinisterOfMemory and its assistant, providing
introspective scaffolding for storing and recalling conversational traces.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
import logging
from typing import Any, Callable, Dict, Iterable, List, Protocol

logger = logging.getLogger(__name__)


# AETH: Define the atomic memory unit to preserve traceability across agents.
@dataclass
class MemoryRecord:
    """Structured memory unit shared across AetheroOS ministers."""

    timestamp: datetime
    role: str
    content: str
    metadata: Dict[str, Any] = field(default_factory=dict)

    # AETH: Provide a deterministic summary for orchestration pipelines.
    def to_summary(self) -> str:
        """Return a compact textual summary for lightweight routing."""

        return f"[{self.timestamp.isoformat()}] ({self.role}) {self.content}"


# AETH: Formalize the contract for interchangeable memory backends.
class MemoryStore(Protocol):
    """Protocol describing storage behavior for ministerial memories."""

    def store(self, record: MemoryRecord) -> MemoryRecord:
        """Persist a memory record and return the stored instance."""

    def query(self, predicate: Callable[[MemoryRecord], bool]) -> List[MemoryRecord]:
        """Retrieve records matching the provided predicate."""

    def latest(self, limit: int = 10) -> List[MemoryRecord]:
        """Return the newest records up to the requested limit."""


# AETH: Provide a lightweight default store for early-stage orchestration.
class InMemoryStore:
    """Volatile implementation of :class:`MemoryStore` for bootstrapping."""

    def __init__(self) -> None:
        # AETH: Store records in insertion order to preserve narrative flow.
        self._records: List[MemoryRecord] = []

    def store(self, record: MemoryRecord) -> MemoryRecord:
        logger.debug("Storing memory record for role=%s", record.role)
        self._records.append(record)
        return record

    def query(self, predicate: Callable[[MemoryRecord], bool]) -> List[MemoryRecord]:
        logger.debug("Querying %d records with predicate", len(self._records))
        return [record for record in self._records if predicate(record)]

    def latest(self, limit: int = 10) -> List[MemoryRecord]:
        logger.debug("Fetching latest %d records", limit)
        return list(self._records[-limit:])


# AETH: Design assistant to handle tactical memory operations on behalf of the Minister.
class AssistantOfMemory:
    """Assistant responsible for day-to-day memory ingestion and retrieval."""

    def __init__(
        self,
        store: MemoryStore | None = None,
        summarizer: Callable[[Iterable[MemoryRecord]], str] | None = None,
    ) -> None:
        # AETH: Default to in-memory persistence to enable fast boot without dependencies.
        self.store = store or InMemoryStore()
        # AETH: Allow pluggable summarization to adapt to evolving narrative needs.
        self.summarizer = summarizer or self._default_summarizer

    def ingest(self, role: str, content: str, metadata: Dict[str, Any] | None = None) -> MemoryRecord:
        """Record a new memory entry with consistent timestamping."""

        record = MemoryRecord(
            timestamp=datetime.utcnow(),
            role=role,
            content=content,
            metadata=metadata or {},
        )
        logger.debug("Assistant ingested memory for role=%s", role)
        return self.store.store(record)

    def recall_recent(self, limit: int = 5) -> List[MemoryRecord]:
        """Retrieve the most recent memory entries."""

        logger.debug("Assistant recalling %d recent memories", limit)
        return self.store.latest(limit)

    def summarize(self, records: Iterable[MemoryRecord] | None = None) -> str:
        """Summarize the provided records or the latest context."""

        selected = list(records) if records is not None else self.recall_recent()
        logger.debug("Assistant summarizing %d records", len(selected))
        return self.summarizer(selected)

    def _default_summarizer(self, records: Iterable[MemoryRecord]) -> str:
        """Fallback summarizer preserving ordering and timestamps."""

        return " | ".join(record.to_summary() for record in records)


# AETH: The Minister orchestrates policy for memory governance and delegation.
class MinisterOfMemory:
    """Premier-aligned minister overseeing memory strategy and integrity."""

    def __init__(
        self,
        assistant: AssistantOfMemory | None = None,
    ) -> None:
        # AETH: Delegate operational tasks to an assistant to respect hierarchy.
        self.assistant = assistant or AssistantOfMemory()

    def log_event(self, role: str, content: str, metadata: Dict[str, Any] | None = None) -> MemoryRecord:
        """Capture an event into the ministerial memory pipeline."""

        logger.info("Minister logging event for role=%s", role)
        return self.assistant.ingest(role=role, content=content, metadata=metadata)

    def review_context(self, limit: int = 5) -> List[MemoryRecord]:
        """Inspect the latest memories to inform strategic decisions."""

        logger.info("Minister reviewing context with limit=%d", limit)
        return self.assistant.recall_recent(limit=limit)

    def narrative_brief(self, limit: int = 5) -> str:
        """Produce a concise brief suitable for inter-ministerial coordination."""

        logger.info("Minister producing narrative brief with limit=%d", limit)
        recent = self.assistant.recall_recent(limit=limit)
        return self.assistant.summarize(recent)

    def search_memories(self, matcher: Callable[[MemoryRecord], bool]) -> List[MemoryRecord]:
        """Delegate targeted retrieval using a predicate matcher."""

        logger.info("Minister executing targeted memory search")
        return self.assistant.store.query(matcher)


__all__ = [
    "AssistantOfMemory",
    "InMemoryStore",
    "MemoryRecord",
    "MemoryStore",
    "MinisterOfMemory",
]
