"""Cognitive Tools: Modular Reasoning

Implementácia Cognitive Tools pattern z Context-Engineering repozitára.
Tento modul poskytuje modulárne reasoning tools pre lepšie riešenie problémov.

Inšpirované: external/Context-Engineering/20_templates/prompt_program_template.py
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, List, Optional

logger = logging.getLogger(__name__)


class StepType(Enum):
    """Typy krokov v prompt programe."""
    INSTRUCTION = "instruction"
    CONDITION = "condition"
    LOOP = "loop"
    VARIABLE = "variable"
    FUNCTION = "function"
    ERROR = "error"


@dataclass
class ProgramStep:
    """Jeden krok v prompt programe."""
    
    content: str
    step_type: StepType = StepType.INSTRUCTION
    metadata: Dict[str, Any] = field(default_factory=dict)
    substeps: List[ProgramStep] = field(default_factory=list)
    
    def format(self, index: Optional[int] = None, indent: int = 0) -> str:
        """Formátuje krok ako string."""
        indent_str = "  " * indent
        
        if index is not None:
            header = f"{indent_str}{index}. "
        else:
            header = f"{indent_str}- "
        
        if self.step_type == StepType.INSTRUCTION:
            formatted = f"{header}{self.content}"
        elif self.step_type == StepType.CONDITION:
            condition = self.metadata.get("condition", "IF condition")
            formatted = f"{header}IF {condition}:"
        elif self.step_type == StepType.LOOP:
            loop_var = self.metadata.get("variable", "item")
            loop_iterable = self.metadata.get("iterable", "items")
            formatted = f"{header}FOR EACH {loop_var} IN {loop_iterable}:"
        elif self.step_type == StepType.VARIABLE:
            var_name = self.metadata.get("name", "variable")
            formatted = f"{header}SET {var_name} = {self.content}"
        elif self.step_type == StepType.FUNCTION:
            func_name = self.metadata.get("name", "function")
            formatted = f"{header}CALL {func_name}({self.content})"
        elif self.step_type == StepType.ERROR:
            formatted = f"{header}ON ERROR: {self.content}"
        else:
            formatted = f"{header}{self.content}"
        
        # Pridaj substeps
        if self.substeps:
            substep_str = "\n".join(
                substep.format(i+1, indent+1) 
                for i, substep in enumerate(self.substeps)
            )
            formatted = f"{formatted}\n{substep_str}"
        
        return formatted


@dataclass
class CognitiveTool:
    """Kognitívny nástroj - modulárny reasoning tool."""
    
    name: str
    description: str
    steps: List[ProgramStep] = field(default_factory=list)
    variables: Dict[str, Any] = field(default_factory=dict)
    error_handlers: List[ProgramStep] = field(default_factory=list)
    
    def format(self) -> str:
        """Formátuje tool ako string pre použitie v prompte."""
        parts = [
            f"# Cognitive Tool: {self.name}",
            f"## Description: {self.description}",
            ""
        ]
        
        if self.steps:
            parts.append("## Steps:")
            for i, step in enumerate(self.steps):
                parts.append(step.format(i+1))
        
        if self.error_handlers:
            parts.append("")
            parts.append("## Error Handling:")
            for handler in self.error_handlers:
                parts.append(handler.format())
        
        if self.variables:
            parts.append("")
            parts.append("## Variables:")
            for name, value in self.variables.items():
                if isinstance(value, str):
                    parts.append(f"- {name} = \"{value}\"")
                else:
                    parts.append(f"- {name} = {value}")
        
        return "\n".join(parts)
    
    def add_step(
        self,
        content: str,
        step_type: StepType = StepType.INSTRUCTION,
        metadata: Optional[Dict[str, Any]] = None
    ) -> ProgramStep:
        """Pridá krok do toolu."""
        step = ProgramStep(content, step_type, metadata or {})
        self.steps.append(step)
        return step


class PromptProgram:
    """Prompt program - štruktúrovaný program pre LLM reasoning."""
    
    def __init__(
        self,
        description: str,
        variables: Optional[Dict[str, Any]] = None
    ):
        """Inicializuje prompt program.
        
        Args:
            description: Popis programu
            variables: Počiatočné premenné
        """
        self.description = description
        self.variables = variables or {}
        self.steps: List[ProgramStep] = []
        self.error_handlers: List[ProgramStep] = []
        logger.info(f"PromptProgram vytvorený: {description}")
    
    def add_step(
        self,
        content: str,
        step_type: StepType = StepType.INSTRUCTION,
        metadata: Optional[Dict[str, Any]] = None
    ) -> ProgramStep:
        """Pridá krok do programu."""
        step = ProgramStep(content, step_type, metadata or {})
        self.steps.append(step)
        return step
    
    def add_condition(
        self,
        condition: str,
        true_step: str,
        false_step: Optional[str] = None
    ) -> ProgramStep:
        """Pridá podmienku do programu."""
        condition_step = self.add_step(
            condition,
            StepType.CONDITION,
            {"condition": condition}
        )
        
        # Pridaj true branch
        true_branch = ProgramStep(true_step, StepType.INSTRUCTION)
        condition_step.substeps.append(true_branch)
        
        # Pridaj false branch ak je poskytnutý
        if false_step:
            false_branch = ProgramStep(false_step, StepType.INSTRUCTION)
            condition_step.substeps.append(false_branch)
        
        return condition_step
    
    def add_error_handler(self, handler: str) -> ProgramStep:
        """Pridá error handler."""
        step = ProgramStep(handler, StepType.ERROR)
        self.error_handlers.append(step)
        return step
    
    def format(self) -> str:
        """Formátuje program ako string."""
        parts = [
            f"# {self.description}",
            ""
        ]
        
        if self.steps:
            parts.append("## Steps:")
            for i, step in enumerate(self.steps):
                parts.append(step.format(i+1))
        
        if self.error_handlers:
            parts.append("")
            parts.append("## Error Handling:")
            for handler in self.error_handlers:
                parts.append(handler.format())
        
        if self.variables:
            parts.append("")
            parts.append("## Initial Context:")
            for name, value in self.variables.items():
                if isinstance(value, str):
                    parts.append(f"- {name} = \"{value}\"")
                else:
                    parts.append(f"- {name} = {value}")
        
        return "\n".join(parts)
    
    def to_cognitive_tool(self, name: str) -> CognitiveTool:
        """Konvertuje program na cognitive tool."""
        return CognitiveTool(
            name=name,
            description=self.description,
            steps=self.steps,
            variables=self.variables,
            error_handlers=self.error_handlers
        )


# Preddefinované cognitive tools
def create_analysis_tool() -> CognitiveTool:
    """Vytvorí cognitive tool pre analýzu."""
    tool = CognitiveTool(
        name="analyze",
        description="Analyzuje problém krok za krokom"
    )
    
    tool.add_step("Identifikuj hlavné komponenty problému")
    tool.add_step("Extrahuj relevantné informácie")
    tool.add_step("Identifikuj vzťahy medzi komponentmi")
    tool.add_step("Vyhodnoť dôležitosť jednotlivých aspektov")
    tool.add_step("Sformuluj závery a odporúčania")
    
    return tool


def create_problem_solving_tool() -> CognitiveTool:
    """Vytvorí cognitive tool pre riešenie problémov."""
    tool = CognitiveTool(
        name="solve",
        description="Rieši problém systematicky"
    )
    
    tool.add_step("Definuj problém jasne a presne")
    tool.add_step("Identifikuj koreňové príčiny")
    tool.add_step("Generuj možné riešenia")
    tool.add_step("Vyhodnoť každé riešenie")
    tool.add_step("Vyber najlepšie riešenie")
    tool.add_step("Implementuj riešenie")
    tool.add_step("Over úspešnosť riešenia")
    
    return tool


def create_decision_making_tool() -> CognitiveTool:
    """Vytvorí cognitive tool pre rozhodovanie."""
    tool = CognitiveTool(
        name="decide",
        description="Pomáha s rozhodovaním"
    )
    
    tool.add_step("Definuj rozhodnutie, ktoré treba urobiť")
    tool.add_step("Identifikuj všetky možnosti")
    tool.add_step("Definuj kritériá pre hodnotenie")
    tool.add_step("Vyhodnoť každú možnosť podľa kritérií")
    tool.add_step("Porovnaj možnosti")
    tool.add_step("Urob rozhodnutie")
    
    return tool

