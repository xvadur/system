"""Compress Context: Recursive Memory Consolidation

Implementácia Compress Context pattern z Context-Engineering repozitára.
Tento modul poskytuje rekurzívne konsolidáciu pamäte pre efektívnejšie využitie tokenov.

Inšpirované: external/Context-Engineering/20_templates/recursive_context.py
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional, Protocol

from core.ministers.memory import MemoryRecord, MemoryStore

logger = logging.getLogger(__name__)


@dataclass
class CompressionResult:
    """Výsledok kompresie kontextu."""
    
    original_count: int
    compressed_count: int
    compression_ratio: float
    preserved_content: str
    metadata: Dict[str, Any]
    timestamp: datetime


class CompressionStrategy(Protocol):
    """Protocol pre kompresné stratégie."""
    
    def compress(self, records: List[MemoryRecord], target_ratio: float) -> CompressionResult:
        """Komprimuje záznamy podľa cieľového pomeru."""
        ...


class RecursiveCompressionStrategy:
    """Rekurzívna kompresná stratégia - iteratívne zlepšuje kompresiu."""
    
    def __init__(self, max_iterations: int = 3, improvement_threshold: float = 0.1):
        """Inicializuje rekurzívnu kompresiu.
        
        Args:
            max_iterations: Maximálny počet iterácií
            improvement_threshold: Minimálne zlepšenie pre pokračovanie
        """
        self.max_iterations = max_iterations
        self.improvement_threshold = improvement_threshold
    
    def compress(self, records: List[MemoryRecord], target_ratio: float) -> CompressionResult:
        """Rekurzívne komprimuje záznamy.
        
        Args:
            records: Zoznam záznamov na kompresiu
            target_ratio: Cieľový kompresný pomer (0.0-1.0)
            
        Returns:
            CompressionResult s komprimovaným obsahom
        """
        if not records:
            return CompressionResult(
                original_count=0,
                compressed_count=0,
                compression_ratio=1.0,
                preserved_content="",
                metadata={},
                timestamp=datetime.now()
            )
        
        original_count = len(records)
        current_content = self._records_to_text(records)
        best_ratio = 1.0
        best_content = current_content
        
        for iteration in range(self.max_iterations):
            # Aplikuj kompresiu
            compressed = self._apply_compression(current_content, target_ratio)
            compressed_ratio = len(compressed) / len(current_content) if current_content else 1.0
            
            # Ak sme dosiahli cieľový pomer, skonči
            if compressed_ratio <= target_ratio:
                best_content = compressed
                best_ratio = compressed_ratio
                break
            
            # Ak sa zlepšenie znížilo pod threshold, skonči
            improvement = best_ratio - compressed_ratio
            if improvement < self.improvement_threshold:
                break
            
            current_content = compressed
            best_ratio = compressed_ratio
            best_content = compressed
        
        compressed_count = len(best_content.split())  # Približný počet slov
        
        return CompressionResult(
            original_count=original_count,
            compressed_count=compressed_count,
            compression_ratio=best_ratio,
            preserved_content=best_content,
            metadata={
                "iterations": iteration + 1,
                "strategy": "recursive",
                "target_ratio": target_ratio
            },
            timestamp=datetime.now()
        )
    
    def _records_to_text(self, records: List[MemoryRecord]) -> str:
        """Konvertuje záznamy na text."""
        parts = []
        for record in records:
            parts.append(f"[{record.role}] {record.content}")
        return "\n".join(parts)
    
    def _apply_compression(self, content: str, target_ratio: float) -> str:
        """Aplikuje kompresiu na obsah.
        
        TODO: V budúcnosti integrovať s LLM pre inteligentnú kompresiu.
        Momentálne používa jednoduchú heuristiku.
        """
        # Jednoduchá heuristika: zachovať kľúčové informácie
        lines = content.split("\n")
        
        # Prioritizuj riadky s dôležitými informáciami
        important_lines = []
        for line in lines:
            # Zachovať riadky s metadátami, dátumami, kľúčovými slovami
            if any(keyword in line.lower() for keyword in ["quest", "task", "decision", "result", "error"]):
                important_lines.append(line)
            elif len(line.strip()) > 50:  # Zachovať dlhšie riadky
                important_lines.append(line)
        
        # Ak je to stále príliš veľa, zníž počet
        target_lines = int(len(lines) * target_ratio)
        if len(important_lines) > target_lines:
            important_lines = important_lines[:target_lines]
        
        return "\n".join(important_lines)


class CompressContextManager:
    """Manažér pre kompresiu kontextu.
    
    Tento manažér implementuje Compress Context pattern z Context-Engineering,
    ktorý umožňuje rekurzívnu konsolidáciu pamäte pre efektívnejšie využitie tokenov.
    """
    
    def __init__(
        self,
        store: MemoryStore,
        strategy: Optional[CompressionStrategy] = None
    ):
        """Inicializuje manažéra kompresie.
        
        Args:
            store: MemoryStore pre prístup k záznamom
            strategy: Kompresná stratégia (default: RecursiveCompressionStrategy)
        """
        self.store = store
        self.strategy = strategy or RecursiveCompressionStrategy()
        logger.info("CompressContextManager inicializovaný")
    
    def consolidate_memory(
        self,
        limit: int = 20,
        target_compression_ratio: float = 0.5
    ) -> CompressionResult:
        """Konsoliduje pamäť pomocou kompresie.
        
        Args:
            limit: Počet záznamov na konsolidáciu
            target_compression_ratio: Cieľový kompresný pomer (0.0-1.0)
            
        Returns:
            CompressionResult s komprimovaným obsahom
        """
        logger.info(f"Konsolidujem pamäť: limit={limit}, ratio={target_compression_ratio}")
        
        # Získaj záznamy
        records = self.store.latest(limit=limit)
        
        if not records:
            logger.warning("Žiadne záznamy na konsolidáciu")
            return CompressionResult(
                original_count=0,
                compressed_count=0,
                compression_ratio=1.0,
                preserved_content="",
                metadata={},
                timestamp=datetime.now()
            )
        
        # Aplikuj kompresiu
        result = self.strategy.compress(records, target_compression_ratio)
        
        logger.info(
            f"Konsolidácia dokončená: {result.original_count} -> {result.compressed_count} "
            f"(ratio: {result.compression_ratio:.2f})"
        )
        
        return result
    
    def compress_records(
        self,
        records: List[MemoryRecord],
        target_compression_ratio: float = 0.5
    ) -> CompressionResult:
        """Komprimuje konkrétne záznamy.
        
        Args:
            records: Zoznam záznamov na kompresiu
            target_compression_ratio: Cieľový kompresný pomer
            
        Returns:
            CompressionResult s komprimovaným obsahom
        """
        logger.info(f"Komprimujem {len(records)} záznamov")
        return self.strategy.compress(records, target_compression_ratio)

