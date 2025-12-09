"""Isolate Context: Task-Based Isolation

Implementácia Isolate Context pattern z Context-Engineering repozitára.
Tento modul poskytuje izoláciu kontextu podľa úloh pre efektívnejšie využitie tokenov.

Inšpirované: external/Context-Engineering/20_templates/minimal_context.yaml
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional, Set

from core.ministers.memory import MemoryRecord

logger = logging.getLogger(__name__)


@dataclass
class ContextIsolation:
    """Izolovaný kontext pre konkrétnu úlohu."""
    
    task_id: str
    task_description: str
    relevant_records: List[MemoryRecord]
    isolated_content: str
    token_count: int
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class IsolationConfig:
    """Konfigurácia pre izoláciu kontextu."""
    
    max_tokens: int = 800  # Cieľový maximálny počet tokenov
    max_turns: int = 3  # Maximálny počet výmen v histórii
    pruning_strategy: str = "drop_oldest"  # drop_oldest, summarize, prioritize
    include_examples: bool = False
    include_metadata: bool = True


class IsolateContextManager:
    """Manažér pre izoláciu kontextu podľa úloh.
    
    Tento manažér implementuje Isolate Context pattern z Context-Engineering,
    ktorý umožňuje vytvoriť minimálny, úlohou-špecifický kontext.
    """
    
    def __init__(self, config: Optional[IsolationConfig] = None):
        """Inicializuje manažéra izolácie.
        
        Args:
            config: Konfigurácia izolácie (default: IsolationConfig)
        """
        self.config = config or IsolationConfig()
        logger.info("IsolateContextManager inicializovaný")
    
    def isolate_for_task(
        self,
        task_id: str,
        task_description: str,
        records: List[MemoryRecord],
        keywords: Optional[Set[str]] = None
    ) -> ContextIsolation:
        """Izoluje kontext pre konkrétnu úlohu.
        
        Args:
            task_id: ID úlohy
            task_description: Popis úlohy
            records: Zoznam záznamov na filtrovanie
            keywords: Kľúčové slová pre relevanciu (voliteľné)
            
        Returns:
            ContextIsolation s izolovaným obsahom
        """
        logger.info(f"Izolujem kontext pre úlohu: {task_id}")
        
        # Filtruj relevantné záznamy
        relevant_records = self._filter_relevant_records(
            records, task_description, keywords
        )
        
        # Aplikuj pruning stratégiu
        pruned_records = self._apply_pruning(relevant_records)
        
        # Vytvor izolovaný obsah
        isolated_content = self._build_isolated_content(
            task_description, pruned_records
        )
        
        # Odhadni počet tokenov (približne: 1 token ≈ 4 znaky)
        token_count = len(isolated_content) // 4
        
        return ContextIsolation(
            task_id=task_id,
            task_description=task_description,
            relevant_records=pruned_records,
            isolated_content=isolated_content,
            token_count=token_count,
            metadata={
                "original_count": len(records),
                "filtered_count": len(relevant_records),
                "pruned_count": len(pruned_records),
                "config": self.config.__dict__
            },
            timestamp=datetime.now()
        )
    
    def _filter_relevant_records(
        self,
        records: List[MemoryRecord],
        task_description: str,
        keywords: Optional[Set[str]] = None
    ) -> List[MemoryRecord]:
        """Filtruje relevantné záznamy pre úlohu.
        
        Args:
            records: Zoznam záznamov
            task_description: Popis úlohy
            keywords: Kľúčové slová (voliteľné)
            
        Returns:
            Filtrovaný zoznam záznamov
        """
        if not records:
            return []
        
        # Ak nie sú kľúčové slová, extrahuj ich z popisu úlohy
        if keywords is None:
            keywords = self._extract_keywords(task_description)
        
        relevant = []
        for record in records:
            # Skontroluj relevanciu
            if self._is_relevant(record, task_description, keywords):
                relevant.append(record)
        
        return relevant
    
    def _extract_keywords(self, text: str) -> Set[str]:
        """Extrahuje kľúčové slová z textu.
        
        TODO: V budúcnosti použiť NLP pre lepšiu extrakciu.
        """
        # Jednoduchá heuristika: slová s veľkými písmenami alebo dôležité slová
        words = text.lower().split()
        # Filtruj stop words a krátke slová
        stop_words = {"the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "of", "with", "by"}
        keywords = {w for w in words if len(w) > 3 and w not in stop_words}
        return keywords
    
    def _is_relevant(
        self,
        record: MemoryRecord,
        task_description: str,
        keywords: Set[str]
    ) -> bool:
        """Kontroluje, či je záznam relevantný pre úlohu."""
        # Skontroluj obsah záznamu
        content_lower = record.content.lower()
        
        # Ak obsahuje kľúčové slová
        if any(keyword in content_lower for keyword in keywords):
            return True
        
        # Skontroluj metadáta
        if record.metadata:
            metadata_str = str(record.metadata).lower()
            if any(keyword in metadata_str for keyword in keywords):
                return True
        
        return False
    
    def _apply_pruning(self, records: List[MemoryRecord]) -> List[MemoryRecord]:
        """Aplikuje pruning stratégiu na záznamy."""
        if not records:
            return []
        
        strategy = self.config.pruning_strategy
        
        if strategy == "drop_oldest":
            # Zachovať len najnovšie záznamy
            return records[-self.config.max_turns:]
        
        elif strategy == "prioritize":
            # Prioritizovať záznamy podľa dôležitosti
            # TODO: Implementovať prioritizáciu na základe metadát
            return records[-self.config.max_turns:]
        
        elif strategy == "summarize":
            # TODO: Implementovať sumarizáciu
            # Momentálne len zachovať najnovšie
            return records[-self.config.max_turns:]
        
        else:
            # Default: zachovať všetky
            return records
    
    def _build_isolated_content(
        self,
        task_description: str,
        records: List[MemoryRecord]
    ) -> str:
        """Vytvorí izolovaný obsah pre úlohu."""
        parts = []
        
        # Pridaj popis úlohy
        parts.append(f"# Task: {task_description}\n")
        
        # Pridaj relevantné záznamy
        if records:
            parts.append("## Relevant Context:\n")
            for record in records:
                timestamp_str = record.timestamp.strftime("%Y-%m-%d %H:%M")
                parts.append(f"[{timestamp_str}] {record.role}: {record.content}")
                
                # Pridaj metadáta ak je to povolené
                if self.config.include_metadata and record.metadata:
                    parts.append(f"  Metadata: {record.metadata}")
                parts.append("")
        
        return "\n".join(parts)
    
    def create_minimal_context(
        self,
        task_description: str,
        records: List[MemoryRecord],
        max_tokens: Optional[int] = None
    ) -> str:
        """Vytvorí minimálny kontext pre úlohu.
        
        Args:
            task_description: Popis úlohy
            records: Zoznam záznamov
            max_tokens: Maximálny počet tokenov (voliteľné)
            
        Returns:
            Minimálny kontext ako string
        """
        if max_tokens is None:
            max_tokens = self.config.max_tokens
        
        # Izoluj kontext
        isolation = self.isolate_for_task(
            task_id="minimal",
            task_description=task_description,
            records=records
        )
        
        # Ak je to stále príliš veľa, zníž ešte viac
        if isolation.token_count > max_tokens:
            # Zníž počet záznamov
            reduction_ratio = max_tokens / isolation.token_count
            target_count = int(len(isolation.relevant_records) * reduction_ratio)
            
            # Vytvor novú izoláciu s menším počtom záznamov
            pruned_records = isolation.relevant_records[-target_count:]
            isolation = self.isolate_for_task(
                task_id="minimal",
                task_description=task_description,
                records=pruned_records
            )
        
        return isolation.isolated_content

