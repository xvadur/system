"""Context Engineering Configuration

Centralizovaná konfigurácia pre Context Engineering komponenty.
Umožňuje užívateľské prepísanie cez JSON konfiguračný súbor.
"""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Dict, Any

logger = logging.getLogger(__name__)

# Default hodnoty
DEFAULT_CONFIG = {
    # Context Engineering
    "compression_threshold": 0.8,  # 80% utilization
    "target_compression_ratio": 0.5,  # 50% redukcia
    "context_window_size": 16000,  # 16K tokens
    "isolation_max_tokens": 800,  # Max tokenov pre izoláciu
    "compression_max_iterations": 3,
    "compression_improvement_threshold": 0.1,
    "isolation_max_turns": 3,
    "isolation_pruning_strategy": "drop_oldest",
    
    # Hot/Cold Storage
    "hot_storage_limit": 100,  # Max záznamov v JSONL (Hot Storage)
    "sqlite_db_path": "development/data/archive.db",  # Cesta k SQLite databáze
    "auto_archive_enabled": True,  # Automatická archivácia
}

# Konfiguračný súbor
CONFIG_FILE = Path("development/data/context_engineering_config.json")

# Načítaj konfiguráciu
_config: Dict[str, Any] = {}


def load_config() -> Dict[str, Any]:
    """Načíta konfiguráciu z JSON súboru alebo použije default hodnoty."""
    global _config
    
    if _config:
        return _config
    
    # Skús načítať z JSON súboru
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                user_config = json.load(f)
                _config = {**DEFAULT_CONFIG, **user_config}
                logger.info(f"Načítaná konfigurácia z {CONFIG_FILE}")
                return _config
        except Exception as e:
            logger.warning(f"Chyba pri načítaní konfigurácie: {e}, používam default hodnoty")
    
    # Použi default hodnoty
    _config = DEFAULT_CONFIG.copy()
    return _config


def get_config(key: str, default: Any = None) -> Any:
    """Získa hodnotu konfigurácie podľa kľúča."""
    config = load_config()
    return config.get(key, default)


def save_config(config: Dict[str, Any]) -> None:
    """Uloží konfiguráciu do JSON súboru."""
    CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    
    global _config
    _config = config
    logger.info(f"Konfigurácia uložená do {CONFIG_FILE}")


# Export konfiguračných hodnôt
config = load_config()

# Context Engineering
COMPRESSION_THRESHOLD = get_config("compression_threshold", 0.8)
TARGET_COMPRESSION_RATIO = get_config("target_compression_ratio", 0.5)
CONTEXT_WINDOW_SIZE = get_config("context_window_size", 16000)
ISOLATION_MAX_TOKENS = get_config("isolation_max_tokens", 800)
COMPRESSION_MAX_ITERATIONS = get_config("compression_max_iterations", 3)
COMPRESSION_IMPROVEMENT_THRESHOLD = get_config("compression_improvement_threshold", 0.1)
ISOLATION_MAX_TURNS = get_config("isolation_max_turns", 3)
ISOLATION_PRUNING_STRATEGY = get_config("isolation_pruning_strategy", "drop_oldest")

# Hot/Cold Storage
HOT_STORAGE_LIMIT = get_config("hot_storage_limit", 100)
SQLITE_DB_PATH = get_config("sqlite_db_path", "development/data/archive.db")
AUTO_ARCHIVE_ENABLED = get_config("auto_archive_enabled", True)

