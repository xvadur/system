"""Persistent storage implementations for MinisterOfMemory.

This module provides FileStore, a persistent implementation of MemoryStore
that saves records to JSONL files for long-term storage.
"""

from __future__ import annotations

import json
import logging
import fcntl
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Dict, List

from ministers.memory import MemoryRecord, MemoryStore

logger = logging.getLogger(__name__)


class FileStore:
    """Persistent implementation of MemoryStore using JSONL files.
    
    Stores MemoryRecord objects in JSONL format (one JSON object per line).
    Thread-safe operations using file locking.
    """

    def __init__(self, filepath: str | Path) -> None:
        """Initialize FileStore with a file path.
        
        Args:
            filepath: Path to JSONL file for storing records.
                     Directory will be created if it doesn't exist.
        """
        self.filepath = Path(filepath)
        self.filepath.parent.mkdir(parents=True, exist_ok=True)
        
        # Cache for loaded records (lazy loading)
        self._records: List[MemoryRecord] | None = None
        self._lock_file = self.filepath.with_suffix('.lock')

    def _load_records(self) -> List[MemoryRecord]:
        """Load all records from JSONL file.
        
        Returns:
            List of MemoryRecord objects loaded from file.
        """
        if self._records is not None:
            return self._records
        
        records = []
        if self.filepath.exists():
            try:
                with open(self.filepath, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        if not line:
                            continue
                        try:
                            data = json.loads(line)
                            # Deserialize timestamp
                            timestamp = datetime.fromisoformat(data['timestamp'])
                            record = MemoryRecord(
                                timestamp=timestamp,
                                role=data['role'],
                                content=data['content'],
                                metadata=data.get('metadata', {})
                            )
                            records.append(record)
                        except (json.JSONDecodeError, KeyError, ValueError) as e:
                            logger.warning(f"Failed to parse line in {self.filepath}: {e}")
                            continue
            except IOError as e:
                logger.error(f"Failed to read {self.filepath}: {e}")
        
        self._records = records
        logger.debug(f"Loaded {len(records)} records from {self.filepath}")
        return records

    def _acquire_lock(self, file_handle) -> None:
        """Acquire file lock for thread-safe operations.
        
        Args:
            file_handle: File handle to lock.
        """
        try:
            fcntl.flock(file_handle, fcntl.LOCK_EX)
        except (IOError, OSError) as e:
            logger.error(f"Failed to acquire lock: {e}")
            raise

    def _release_lock(self, file_handle) -> None:
        """Release file lock.
        
        Args:
            file_handle: File handle to unlock.
        """
        try:
            fcntl.flock(file_handle, fcntl.LOCK_UN)
        except (IOError, OSError) as e:
            logger.error(f"Failed to release lock: {e}")

    def store(self, record: MemoryRecord) -> MemoryRecord:
        """Persist a memory record to JSONL file.
        
        Args:
            record: MemoryRecord to store.
            
        Returns:
            The stored MemoryRecord instance.
        """
        # Ensure records are loaded
        self._load_records()
        
        # Append to in-memory cache
        if self._records is not None:
            self._records.append(record)
        
        # Append to file (thread-safe)
        try:
            with open(self.filepath, 'a', encoding='utf-8') as f:
                self._acquire_lock(f)
                try:
                    # Serialize record to JSON
                    data = {
                        'timestamp': record.timestamp.isoformat(),
                        'role': record.role,
                        'content': record.content,
                        'metadata': record.metadata
                    }
                    f.write(json.dumps(data, ensure_ascii=False) + '\n')
                    f.flush()  # Ensure data is written immediately
                finally:
                    self._release_lock(f)
            
            logger.debug(f"Stored memory record for role={record.role}")
        except IOError as e:
            logger.error(f"Failed to store record to {self.filepath}: {e}")
            # Remove from cache if write failed
            if self._records and record in self._records:
                self._records.remove(record)
            raise
        
        return record

    def query(self, predicate: Callable[[MemoryRecord], bool]) -> List[MemoryRecord]:
        """Retrieve records matching the provided predicate.
        
        Args:
            predicate: Function that takes MemoryRecord and returns bool.
            
        Returns:
            List of MemoryRecord objects matching the predicate.
        """
        records = self._load_records()
        matching = [record for record in records if predicate(record)]
        logger.debug(f"Query returned {len(matching)} records from {len(records)} total")
        return matching

    def latest(self, limit: int = 10) -> List[MemoryRecord]:
        """Return the newest records up to the requested limit.
        
        Args:
            limit: Maximum number of records to return.
            
        Returns:
            List of most recent MemoryRecord objects.
        """
        records = self._load_records()
        result = list(records[-limit:]) if len(records) > limit else list(records)
        logger.debug(f"Returning {len(result)} latest records (limit={limit})")
        return result

    def clear_cache(self) -> None:
        """Clear the in-memory cache, forcing reload on next access."""
        self._records = None
        logger.debug("Cleared FileStore cache")

    def get_record_count(self) -> int:
        """Get total number of records in storage.
        
        Returns:
            Number of records stored.
        """
        records = self._load_records()
        return len(records)


__all__ = ["FileStore"]

