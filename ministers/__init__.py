"""Top-level ministerial facades for Premier orchestration."""

# AETH: Re-export premier-facing ministers for easy discovery.
from ministers.memory import AssistantOfMemory, MemoryIntent, MinisterOfMemory

__all__ = ["AssistantOfMemory", "MemoryIntent", "MinisterOfMemory"]
