"""AetheroOS ministerial memory agent.

This module introduces the MinisterOfMemory and its assistant, providing
introspective scaffolding for storing and recalling conversational traces.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
import logging
from typing import Any, Callable, Dict, Iterable, List, Protocol, Optional

logger = logging.getLogger(__name__)

# Context Engineering (lazy import pre Context Engineering)
_CONTEXT_ENGINEERING_AVAILABLE = False
try:
    from core.context_engineering.integration import track_and_optimize_context, isolate_context_for_task
    from core.context_engineering.config import COMPRESSION_THRESHOLD
    _CONTEXT_ENGINEERING_AVAILABLE = True
except ImportError:
    logger.debug("Context Engineering nie je dostupný, používam základné funkcie")


def _get_current_time_with_timezone(timezone: str = "Europe/Bratislava") -> datetime:
    """Získa aktuálny čas so správnou časovou zónou.
    
    Args:
        timezone: Časová zóna (default: Europe/Bratislava)
        
    Returns:
        datetime objekt so správnym časom a časovou zónou
    """
    try:
        # Python 3.9+ má zoneinfo
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
            logger.warning("Timezone libraries not available, using UTC")
            return datetime.utcnow()
    except Exception as e:
        # Ak zlyhá, použijeme UTC
        logger.warning(f"Failed to get timezone-aware time: {e}, using UTC")
        return datetime.utcnow()


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

    def ingest(self, role: str, content: str, metadata: Dict[str, Any] | None = None, timestamp: Optional[datetime] = None) -> MemoryRecord:
        """Record a new memory entry with consistent timestamping.
        
        Args:
            role: Role of the speaker (user/assistant/system)
            content: Content of the message
            metadata: Optional metadata dictionary
            timestamp: Optional timestamp (if None, uses current time with timezone)
        """

        # Použi poskytnutý timestamp alebo získaj aktuálny čas so správnou časovou zónou
        if timestamp is None:
            timestamp = _get_current_time_with_timezone()
        
        record = MemoryRecord(
            timestamp=timestamp,
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

    def log_event(self, role: str, content: str, metadata: Dict[str, Any] | None = None, timestamp: Optional[datetime] = None) -> MemoryRecord:
        """Capture an event into the ministerial memory pipeline.
        
        Args:
            role: Role of the speaker (user/assistant/system)
            content: Content of the message
            metadata: Optional metadata dictionary
            timestamp: Optional timestamp (if None, uses current time with timezone)
        """

        logger.info("Minister logging event for role=%s", role)
        return self.assistant.ingest(role=role, content=content, metadata=metadata, timestamp=timestamp)

    def review_context(self, limit: int = 5) -> List[MemoryRecord]:
        """Inspect the latest memories to inform strategic decisions."""

        logger.info("Minister reviewing context with limit=%d", limit)
        return self.assistant.recall_recent(limit=limit)
    
    def get_context_with_compression(self, limit: int = 20) -> Dict[str, Any]:
        """Získa kontext s automatickou kompresiou ak je utilization vysoká.
        
        Args:
            limit: Počet záznamov na načítanie
            
        Returns:
            Dictionary s kontextom a metrikami kompresie
        """
        if not _CONTEXT_ENGINEERING_AVAILABLE:
            # Fallback na základné review_context
            records = self.review_context(limit=limit)
            return {
                'records': records,
                'compressed': False,
                'message': 'Context Engineering nie je dostupný'
            }
        
        # Získaj záznamy
        records = self.assistant.recall_recent(limit=limit)
        
        if not records:
            return {
                'records': [],
                'compressed': False,
                'message': 'Žiadne záznamy'
            }
        
        # Trackuj a optimalizuj
        try:
            content = "\n".join([r.to_summary() for r in records])
            result = track_and_optimize_context(
                store=self.assistant.store,
                history_content=content
            )
            
            # Ak bola aplikovaná kompresia, načítaj znova záznamy
            if result.get('compression_result', {}).get('compressed'):
                records = self.assistant.recall_recent(limit=limit)
            
            return {
                'records': records,
                'compressed': result.get('compression_result', {}).get('compressed', False),
                'metrics': result.get('metrics'),
                'utilization': result.get('utilization', 0.0)
            }
        except Exception as e:
            logger.warning(f"Chyba pri kompresii kontextu: {e}")
            return {
                'records': records,
                'compressed': False,
                'error': str(e)
            }

    def narrative_brief(self, limit: int = 5) -> str:
        """Produce a concise brief suitable for inter-ministerial coordination."""

        logger.info("Minister producing narrative brief with limit=%d", limit)
        recent = self.assistant.recall_recent(limit=limit)
        return self.assistant.summarize(recent)

    def search_memories(self, matcher: Callable[[MemoryRecord], bool]) -> List[MemoryRecord]:
        """Delegate targeted retrieval using a predicate matcher."""

        logger.info("Minister executing targeted memory search")
        return self.assistant.store.query(matcher)
    
    def isolate_context_for_task(
        self,
        task_id: str,
        task_description: str,
        keywords: Optional[set] = None,
        limit: int = 20
    ) -> Dict[str, Any]:
        """Izoluje kontext pre konkrétnu úlohu.
        
        Args:
            task_id: ID úlohy
            task_description: Popis úlohy
            keywords: Kľúčové slová (voliteľné)
            limit: Počet záznamov na filtrovanie
            
        Returns:
            Dictionary s izolovaným kontextom
        """
        if not _CONTEXT_ENGINEERING_AVAILABLE:
            # Fallback na základné review_context
            records = self.review_context(limit=limit)
            return {
                'task_id': task_id,
                'records': records,
                'isolated': False,
                'message': 'Context Engineering nie je dostupný'
            }
        
        # Získaj záznamy
        records = self.assistant.recall_recent(limit=limit)
        
        if not records:
            return {
                'task_id': task_id,
                'records': [],
                'isolated': False,
                'message': 'Žiadne záznamy'
            }
        
        # Izoluj kontext
        try:
            isolation = isolate_context_for_task(
                task_id=task_id,
                task_description=task_description,
                records=records,
                keywords=keywords
            )
            
            return {
                'task_id': task_id,
                'task_description': task_description,
                'records': isolation.relevant_records,
                'isolated_content': isolation.isolated_content,
                'token_count': isolation.token_count,
                'isolated': True,
                'metadata': isolation.metadata
            }
        except Exception as e:
            logger.warning(f"Chyba pri izolácii kontextu: {e}")
            return {
                'task_id': task_id,
                'records': records,
                'isolated': False,
                'error': str(e)
            }


__all__ = [
    "AssistantOfMemory",
    "InMemoryStore",
    "MemoryRecord",
    "MemoryStore",
    "MinisterOfMemory",
]
