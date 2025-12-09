"""Token Metrics & Evaluation

Implementácia Metrics & Evaluation pattern z Context-Engineering repozitára.
Tento modul poskytuje tracking a evaluáciu tokenov pre optimalizáciu kontextu.

Inšpirované: external/Context-Engineering/40_reference/token_budgeting.md
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


@dataclass
class TokenMetrics:
    """Metriky pre token tracking."""
    
    total_tokens: int = 0
    input_tokens: int = 0
    output_tokens: int = 0
    system_tokens: int = 0
    history_tokens: int = 0
    current_tokens: int = 0
    timestamp: datetime = field(default_factory=datetime.now)
    
    def utilization_ratio(self, context_window_size: int) -> float:
        """Vypočíta utilization ratio."""
        if context_window_size == 0:
            return 0.0
        return self.total_tokens / context_window_size
    
    def to_dict(self) -> Dict[str, Any]:
        """Konvertuje na dictionary."""
        return {
            "total_tokens": self.total_tokens,
            "input_tokens": self.input_tokens,
            "output_tokens": self.output_tokens,
            "system_tokens": self.system_tokens,
            "history_tokens": self.history_tokens,
            "current_tokens": self.current_tokens,
            "timestamp": self.timestamp.isoformat()
        }


@dataclass
class TokenBudget:
    """Token budget alokácia."""
    
    context_window_size: int = 16000  # Default: 16K tokens
    system_allocation: float = 0.15  # 15% pre system prompt
    history_allocation: float = 0.40  # 40% pre históriu
    current_allocation: float = 0.30  # 30% pre aktuálny input
    reserve_allocation: float = 0.15  # 15% rezerva
    
    def get_system_budget(self) -> int:
        """Vráti budget pre system prompt."""
        return int(self.context_window_size * self.system_allocation)
    
    def get_history_budget(self) -> int:
        """Vráti budget pre históriu."""
        return int(self.context_window_size * self.history_allocation)
    
    def get_current_budget(self) -> int:
        """Vráti budget pre aktuálny input."""
        return int(self.context_window_size * self.current_allocation)
    
    def get_reserve_budget(self) -> int:
        """Vráti rezervný budget."""
        return int(self.context_window_size * self.reserve_allocation)


class TokenBudgetTracker:
    """Tracker pre token budget a metriky."""
    
    def __init__(self, budget: Optional[TokenBudget] = None):
        """Inicializuje tracker.
        
        Args:
            budget: Token budget konfigurácia (default: TokenBudget)
        """
        self.budget = budget or TokenBudget()
        self.metrics_history: List[TokenMetrics] = []
        logger.info("TokenBudgetTracker inicializovaný")
    
    def estimate_tokens(self, text: str) -> int:
        """Odhadne počet tokenov v texte.
        
        TODO: V budúcnosti použiť skutočný tokenizer.
        Momentálne používa približný odhad: 1 token ≈ 4 znaky.
        """
        return len(text) // 4
    
    def track_usage(
        self,
        system_content: str = "",
        history_content: str = "",
        current_content: str = "",
        output_content: str = ""
    ) -> TokenMetrics:
        """Trackuje použitie tokenov.
        
        Args:
            system_content: System prompt obsah
            history_content: História konverzácie
            current_content: Aktuálny user input
            output_content: Output obsah
            
        Returns:
            TokenMetrics s aktuálnymi metrikami
        """
        system_tokens = self.estimate_tokens(system_content)
        history_tokens = self.estimate_tokens(history_content)
        current_tokens = self.estimate_tokens(current_content)
        output_tokens = self.estimate_tokens(output_content)
        
        input_tokens = system_tokens + history_tokens + current_tokens
        total_tokens = input_tokens + output_tokens
        
        metrics = TokenMetrics(
            total_tokens=total_tokens,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            system_tokens=system_tokens,
            history_tokens=history_tokens,
            current_tokens=current_tokens,
            timestamp=datetime.now()
        )
        
        self.metrics_history.append(metrics)
        logger.info(f"Token usage tracked: {total_tokens} tokens")
        
        return metrics
    
    def check_budget(
        self,
        system_content: str = "",
        history_content: str = "",
        current_content: str = ""
    ) -> Dict[str, Any]:
        """Kontroluje, či je obsah v rámci budgetu.
        
        Args:
            system_content: System prompt obsah
            history_content: História konverzácie
            current_content: Aktuálny user input
            
        Returns:
            Dictionary s výsledkami kontroly
        """
        system_tokens = self.estimate_tokens(system_content)
        history_tokens = self.estimate_tokens(history_content)
        current_tokens = self.estimate_tokens(current_content)
        
        system_budget = self.budget.get_system_budget()
        history_budget = self.budget.get_history_budget()
        current_budget = self.budget.get_current_budget()
        
        total_used = system_tokens + history_tokens + current_tokens
        total_budget = self.budget.context_window_size
        
        result = {
            "within_budget": total_used <= total_budget,
            "total_used": total_used,
            "total_budget": total_budget,
            "utilization": total_used / total_budget if total_budget > 0 else 0.0,
            "components": {
                "system": {
                    "used": system_tokens,
                    "budget": system_budget,
                    "within_budget": system_tokens <= system_budget,
                    "utilization": system_tokens / system_budget if system_budget > 0 else 0.0
                },
                "history": {
                    "used": history_tokens,
                    "budget": history_budget,
                    "within_budget": history_tokens <= history_budget,
                    "utilization": history_tokens / history_budget if history_budget > 0 else 0.0
                },
                "current": {
                    "used": current_tokens,
                    "budget": current_budget,
                    "within_budget": current_tokens <= current_budget,
                    "utilization": current_tokens / current_budget if current_budget > 0 else 0.0
                }
            },
            "warnings": []
        }
        
        # Generuj varovania
        if result["utilization"] > 0.9:
            result["warnings"].append("Token budget je takmer vyčerpaný (>90%)")
        
        if not result["components"]["system"]["within_budget"]:
            result["warnings"].append("System prompt presahuje budget")
        
        if not result["components"]["history"]["within_budget"]:
            result["warnings"].append("História presahuje budget - potrebná kompresia")
        
        if not result["components"]["current"]["within_budget"]:
            result["warnings"].append("Aktuálny input presahuje budget")
        
        return result
    
    def get_metrics_summary(self) -> Dict[str, Any]:
        """Vráti sumár metrík."""
        if not self.metrics_history:
            return {"message": "Žiadne metriky"}
        
        latest = self.metrics_history[-1]
        avg_total = sum(m.total_tokens for m in self.metrics_history) / len(self.metrics_history)
        
        return {
            "latest": latest.to_dict(),
            "average_total_tokens": avg_total,
            "total_tracked": len(self.metrics_history),
            "utilization_ratio": latest.utilization_ratio(self.budget.context_window_size)
        }

