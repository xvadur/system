"""
Log Manager - Triple-write systém pre XVADUR logging s Hot/Cold Storage architektúrou

Zapisuje súčasne do:
- XVADUR_LOG.md (Markdown pre človeka)
- XVADUR_LOG.jsonl (Hot Storage - posledných 100 záznamov pre AI)
- archive.db (Cold Storage - SQLite archív pre historické query)

Automatické logovanie:
- Pri zadávaní tasku: log_task_started()
- Pri dokončení tasku: log_task_completed()

Hot/Cold Storage architektúra:
- JSONL = Hot Storage (runtime kontext, posledných 100 záznamov)
- SQLite = Cold Storage (archív, komplexné query, agregácie)

Použitie:
    from scripts.utils.log_manager import add_log_entry, log_task_started, log_task_completed
    log_task_started("Implementácia feature X")
    # ... práca ...
    log_task_completed("Implementácia feature X", files_changed=["file.py"])
    
    # Historické query (Cold Storage)
    from scripts.utils.log_manager import query_archive, get_xp_summary
    results = query_archive(type="task", date_from="2025-12-01")
    summary = get_xp_summary()
"""

import sys
import json
import logging
from pathlib import Path
from datetime import datetime
from typing import List, Optional, Dict, Any

# Add workspace root to path
workspace_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(workspace_root))

# Context Engineering imports (lazy loading)
try:
    from core.context_engineering.token_metrics import TokenBudgetTracker, TokenBudget
    from core.context_engineering.config import (
        CONTEXT_WINDOW_SIZE,
        COMPRESSION_THRESHOLD,
        get_config
    )
    CONTEXT_ENGINEERING_AVAILABLE = True
except ImportError:
    CONTEXT_ENGINEERING_AVAILABLE = False
    CONTEXT_WINDOW_SIZE = 16000
    COMPRESSION_THRESHOLD = 0.8

# SQLite Store import (lazy loading)
try:
    from core.ministers.sqlite_store import SQLiteStore
    SQLITE_AVAILABLE = True
except ImportError:
    SQLITE_AVAILABLE = False

logger = logging.getLogger(__name__)

# === CESTY K SÚBOROM ===
LOG_MD_PATH = workspace_root / "development" / "logs" / "XVADUR_LOG.md"
LOG_JSONL_PATH = workspace_root / "development" / "logs" / "XVADUR_LOG.jsonl"
SQLITE_DB_PATH = workspace_root / "development" / "data" / "archive.db"

# === HOT STORAGE KONFIGURÁCIA ===
HOT_STORAGE_LIMIT = 100  # Max záznamov v JSONL (Hot Storage)

# === SINGLETON PRE SQLITE STORE ===
_sqlite_store: Optional["SQLiteStore"] = None


def _get_sqlite_store() -> Optional["SQLiteStore"]:
    """Vráti singleton inštanciu SQLiteStore (lazy initialization)."""
    global _sqlite_store
    
    if not SQLITE_AVAILABLE:
        return None
    
    if _sqlite_store is None:
        try:
            _sqlite_store = SQLiteStore(SQLITE_DB_PATH)
            logger.debug(f"SQLiteStore inicializovaný: {SQLITE_DB_PATH}")
        except Exception as e:
            logger.error(f"Chyba pri inicializácii SQLiteStore: {e}")
            return None
    
    return _sqlite_store


def add_log_entry(
    action_name: str, 
    status: str, 
    files_changed: Optional[List[str]] = None, 
    xp_estimate: Optional[float] = None,
    entry_type: str = "task",
    completed: Optional[List[str]] = None,
    results: Optional[Dict[str, Any]] = None,
    decisions: Optional[List[str]] = None,
    quest_id: Optional[int] = None
):
    """Pridá nový záznam do všetkých storage vrstiev (triple-write).

    Zapisuje do:
    1. XVADUR_LOG.md (Markdown pre človeka)
    2. XVADUR_LOG.jsonl (Hot Storage - runtime kontext)
    3. archive.db (Cold Storage - SQLite archív)

    Args:
        action_name: Názov akcie (napr. "Implementácia session rotationu").
        status: Status akcie (napr. "started", "completed", "in_progress").
        files_changed: Zoznam zmienených súborov (voliteľné).
        xp_estimate: Odhad XP za dokončenie akcie (voliteľné).
        entry_type: Typ záznamu ("task", "session", "quest_created", "quest_closed", "analysis", "savegame").
        completed: Zoznam dokončených položiek (voliteľné).
        results: Slovník s výsledkami (voliteľné).
        decisions: Zoznam kľúčových rozhodnutí (voliteľné).
        quest_id: ID GitHub Issue (voliteľné).
    """
    now = datetime.now()
    current_time = now.strftime('%H:%M')
    current_date = now.strftime('%Y-%m-%d')
    iso_timestamp = now.isoformat()

    # Vytvor entry dictionary (použité pre JSONL aj SQLite)
    entry = {
        "timestamp": iso_timestamp,
        "date": current_date,
        "time": current_time,
        "title": action_name,
        "type": entry_type,
        "status": status
    }
    
    # Pridaj voliteľné polia len ak existujú
    if files_changed:
        entry["files_changed"] = files_changed
    if xp_estimate is not None:
        entry["xp_estimate"] = xp_estimate
    if completed:
        entry["completed"] = completed
    if results:
        entry["results"] = results
    if decisions:
        entry["decisions"] = decisions
    if quest_id is not None:
        entry["quest_id"] = quest_id

    # === 1. MARKDOWN ZÁZNAM ===
    _write_markdown_entry(action_name, status, files_changed, xp_estimate, current_time)

    # === 2. JSONL ZÁZNAM (Hot Storage) ===
    _write_jsonl_entry(entry)

    # === 3. SQLITE ZÁZNAM (Cold Storage) ===
    _write_sqlite_entry(entry)
    
    # === 4. AUTOMATICKÁ ARCHIVÁCIA ===
    _check_and_archive()


def _write_markdown_entry(
    action_name: str, 
    status: str, 
    files_changed: Optional[List[str]], 
    xp_estimate: Optional[float],
    current_time: str
):
    """Zapíše záznam do Markdown logu."""
    log_entry = f"[{current_time}] 🔹 {action_name}\n"
    if files_changed:
        log_entry += "  - *Zmenené súbory:*\n"
        for f in files_changed:
            log_entry += f"    - {f}\n"
    log_entry += f"  - *Status:* {status}\n"
    if xp_estimate is not None:
        log_entry += f"  - *XP:* {xp_estimate}\n"

    try:
        # Načítaj existujúci obsah
        if LOG_MD_PATH.exists():
            content = LOG_MD_PATH.read_text(encoding='utf-8')
        else:
            content = "# 🧠 XVADUR LOG\n\n**Účel:** Záznam vykonanej práce a zmien v projekte\n\n---\n"
        
        # Nájdi pozíciu po hlavičke (po prvom "---")
        if "---" in content:
            parts = content.split("---", 1)
            new_content = parts[0] + "---\n" + log_entry + "\n" + parts[1] if len(parts) > 1 else parts[0] + "---\n" + log_entry
        else:
            new_content = content + "\n" + log_entry
        
        LOG_MD_PATH.write_text(new_content, encoding='utf-8')
    except Exception as e:
        print(f"Error writing to XVADUR_LOG.md: {e}", file=sys.stderr)


def _write_jsonl_entry(entry: Dict[str, Any]):
    """Zapíše záznam do JSONL logu (Hot Storage)."""
    try:
        # Append do JSONL súboru
        with open(LOG_JSONL_PATH, 'a', encoding='utf-8') as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    except Exception as e:
        print(f"Error writing to XVADUR_LOG.jsonl: {e}", file=sys.stderr)


def _write_sqlite_entry(entry: Dict[str, Any]):
    """Zapíše záznam do SQLite databázy (Cold Storage)."""
    store = _get_sqlite_store()
    if store is None:
        logger.debug("SQLite nie je dostupný, preskakujem Cold Storage zápis")
        return
    
    try:
        store.insert(entry)
    except Exception as e:
        logger.error(f"Chyba pri zápise do SQLite: {e}")


def _count_jsonl_entries() -> int:
    """Spočíta počet záznamov v JSONL súbore."""
    if not LOG_JSONL_PATH.exists():
        return 0
    
    try:
        with open(LOG_JSONL_PATH, 'r', encoding='utf-8') as f:
            return sum(1 for line in f if line.strip())
    except Exception as e:
        logger.error(f"Chyba pri počítaní JSONL záznamov: {e}")
        return 0


def _check_and_archive():
    """Skontroluje či je potrebná archivácia a vykoná ju."""
    count = _count_jsonl_entries()
    
    if count > HOT_STORAGE_LIMIT:
        logger.info(f"JSONL má {count} záznamov (limit: {HOT_STORAGE_LIMIT}), spúšťam archiváciu")
        archive_old_entries()


def archive_old_entries():
    """Archivuje staré záznamy - ponechá len posledných HOT_STORAGE_LIMIT v JSONL.
    
    Táto funkcia:
    1. Načíta všetky záznamy z JSONL
    2. Ponechá posledných HOT_STORAGE_LIMIT záznamov
    3. Prepíše JSONL len s týmito záznamami
    
    Poznámka: Záznamy sú už v SQLite (Cold Storage), takže sa nestrácajú.
    """
    if not LOG_JSONL_PATH.exists():
        return
    
    try:
        # Načítaj všetky záznamy
        entries = []
        with open(LOG_JSONL_PATH, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    entries.append(json.loads(line))
        
        if len(entries) <= HOT_STORAGE_LIMIT:
            logger.debug(f"Archivácia nie je potrebná ({len(entries)} <= {HOT_STORAGE_LIMIT})")
            return
        
        # Ponechaj len posledných HOT_STORAGE_LIMIT
        keep_entries = entries[-HOT_STORAGE_LIMIT:]
        archived_count = len(entries) - len(keep_entries)
        
        # Prepíš JSONL
        with open(LOG_JSONL_PATH, 'w', encoding='utf-8') as f:
            for entry in keep_entries:
                f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        
        logger.info(f"Archivované {archived_count} záznamov, ponechaných {len(keep_entries)} v Hot Storage")
        
    except Exception as e:
        logger.error(f"Chyba pri archivácii: {e}")


def get_recent_log_entries(limit: int = 5) -> List[Dict[str, Any]]:
    """Načíta posledných N záznamov z JSONL logu (Hot Storage).
    
    Args:
        limit: Počet záznamov na načítanie (default: 5)
    
    Returns:
        Zoznam posledných N log záznamov
    """
    if not LOG_JSONL_PATH.exists():
        return []
    
    entries = []
    try:
        with open(LOG_JSONL_PATH, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    entries.append(json.loads(line))
        return entries[-limit:]
    except Exception as e:
        print(f"Error reading XVADUR_LOG.jsonl: {e}", file=sys.stderr)
        return []


def log_task_started(task_name: str, task_description: Optional[str] = None) -> None:
    """Automaticky zaloguje začiatok tasku.
    
    Args:
        task_name: Názov tasku
        task_description: Voliteľný popis tasku
    """
    add_log_entry(
        action_name=f"Task: {task_name}",
        status="started",
        entry_type="task",
        results={"description": task_description} if task_description else None
    )
    logger.info(f"Task started: {task_name}")


def log_task_completed(
    task_name: str,
    files_changed: Optional[List[str]] = None,
    xp_estimate: Optional[float] = None,
    completed: Optional[List[str]] = None,
    results: Optional[Dict[str, Any]] = None,
    decisions: Optional[List[str]] = None
) -> None:
    """Automaticky zaloguje dokončenie tasku.
    
    Args:
        task_name: Názov tasku
        files_changed: Zoznam zmienených súborov
        xp_estimate: Odhad XP
        completed: Zoznam dokončených položiek
        results: Výsledky tasku
        decisions: Kľúčové rozhodnutia
    """
    # Trackuj tokeny ak je Context Engineering dostupný
    token_metrics = None
    if CONTEXT_ENGINEERING_AVAILABLE:
        try:
            tracker = TokenBudgetTracker(TokenBudget(context_window_size=CONTEXT_WINDOW_SIZE))
            # Odhad tokenov pre tento záznam
            entry_text = f"{task_name} {json.dumps(results or {})}"
            token_count = tracker.estimate_tokens(entry_text)
            token_metrics = {
                "token_count": token_count,
                "context_window_size": CONTEXT_WINDOW_SIZE
            }
        except Exception as e:
            logger.warning(f"Chyba pri trackovaní tokenov: {e}")
    
    # Pridaj token metriky do results
    if results is None:
        results = {}
    if token_metrics:
        results["token_metrics"] = token_metrics
    
    add_log_entry(
        action_name=f"Task: {task_name}",
        status="completed",
        files_changed=files_changed,
        xp_estimate=xp_estimate,
        entry_type="task",
        completed=completed,
        results=results,
        decisions=decisions
    )
    logger.info(f"Task completed: {task_name}")


def get_optimized_log_context(limit: int = 5, use_compression: bool = False) -> Dict[str, Any]:
    """Načíta optimalizovaný kontext z logu pomocou Context Engineering.
    
    Používa Hot Storage (JSONL) pre rýchle načítanie.
    
    Args:
        limit: Počet záznamov na načítanie
        use_compression: Použiť kompresiu ak je utilization vysoká
    
    Returns:
        Dict s optimalizovaným kontextom a metrikami
    """
    entries = get_recent_log_entries(limit=limit * 2)  # Načítaj viac pre optimalizáciu
    
    if not entries:
        return {"entries": [], "token_metrics": None, "optimized": False}
    
    # Konvertuj na text pre token tracking
    entries_text = "\n".join([json.dumps(e, ensure_ascii=False) for e in entries])
    
    if CONTEXT_ENGINEERING_AVAILABLE:
        try:
            tracker = TokenBudgetTracker(TokenBudget(context_window_size=CONTEXT_WINDOW_SIZE))
            metrics = tracker.track_usage(history_content=entries_text)
            utilization = metrics.utilization_ratio(CONTEXT_WINDOW_SIZE)
            
            # Ak je utilization vysoká a je požadovaná kompresia, aplikuj ju
            optimized_entries = entries
            if use_compression and utilization > COMPRESSION_THRESHOLD:
                # Zjednodušená kompresia - vezmi len najnovšie a najdôležitejšie
                optimized_entries = entries[-limit:]
                logger.info(f"Kompresia logu: {len(entries)} -> {len(optimized_entries)} záznamov")
            
            return {
                "entries": optimized_entries[-limit:],
                "token_metrics": metrics.to_dict(),
                "utilization": utilization,
                "optimized": len(optimized_entries) < len(entries)
            }
        except Exception as e:
            logger.warning(f"Chyba pri optimalizácii logu: {e}")
    
    return {
        "entries": entries[-limit:],
        "token_metrics": None,
        "optimized": False
    }


# =============================================================================
# COLD STORAGE API (SQLite Query Functions)
# =============================================================================

def query_archive(
    type: Optional[str] = None,
    status: Optional[str] = None,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
    quest_id: Optional[int] = None,
    limit: int = 100
) -> List[Dict[str, Any]]:
    """Vyhľadá záznamy v Cold Storage (SQLite archív).
    
    Args:
        type: Filter podľa typu (task, session, quest_created, atď.)
        status: Filter podľa statusu (started, completed, atď.)
        date_from: Filter od dátumu (YYYY-MM-DD)
        date_to: Filter do dátumu (YYYY-MM-DD)
        quest_id: Filter podľa quest ID
        limit: Maximálny počet výsledkov
        
    Returns:
        Zoznam záznamov ako dictionary
    """
    store = _get_sqlite_store()
    if store is None:
        logger.warning("SQLite nie je dostupný, query_archive vracia prázdny zoznam")
        return []
    
    try:
        return store.query(
            type=type,
            status=status,
            date_from=date_from,
            date_to=date_to,
            quest_id=quest_id,
            limit=limit
        )
    except Exception as e:
        logger.error(f"Chyba pri query_archive: {e}")
        return []


def get_archive_count(
    type: Optional[str] = None,
    status: Optional[str] = None,
    quest_id: Optional[int] = None
) -> int:
    """Spočíta záznamy v Cold Storage.
    
    Args:
        type: Filter podľa typu
        status: Filter podľa statusu
        quest_id: Filter podľa quest ID
        
    Returns:
        Počet záznamov
    """
    store = _get_sqlite_store()
    if store is None:
        return 0
    
    try:
        return store.count(type=type, status=status, quest_id=quest_id)
    except Exception as e:
        logger.error(f"Chyba pri get_archive_count: {e}")
        return 0


def get_xp_summary() -> Dict[str, Any]:
    """Vráti sumár XP zo všetkých záznamov v Cold Storage.
    
    Returns:
        Dictionary s XP štatistikami:
        - total_xp: Celkové XP
        - by_type: XP rozdelené podľa typu
        - by_day: XP rozdelené podľa dňa (posledných 7 dní)
    """
    store = _get_sqlite_store()
    if store is None:
        return {"total_xp": 0, "by_type": [], "by_day": []}
    
    try:
        return store.get_xp_summary()
    except Exception as e:
        logger.error(f"Chyba pri get_xp_summary: {e}")
        return {"total_xp": 0, "by_type": [], "by_day": []}


def get_quest_summary(quest_id: int) -> Dict[str, Any]:
    """Vráti sumár pre konkrétny quest z Cold Storage.
    
    Args:
        quest_id: ID questu
        
    Returns:
        Dictionary so sumárom questu
    """
    store = _get_sqlite_store()
    if store is None:
        return {"quest_id": quest_id, "found": False}
    
    try:
        return store.get_quest_summary(quest_id)
    except Exception as e:
        logger.error(f"Chyba pri get_quest_summary: {e}")
        return {"quest_id": quest_id, "found": False}


def aggregate_xp(group_by: str = "type") -> List[Dict[str, Any]]:
    """Agreguje XP podľa zadaného poľa.
    
    Args:
        group_by: Pole pre GROUP BY (type, status, date, quest_id)
        
    Returns:
        Zoznam agregovaných výsledkov
    """
    store = _get_sqlite_store()
    if store is None:
        return []
    
    try:
        return store.aggregate("xp_estimate", agg_func="SUM", group_by=group_by)
    except Exception as e:
        logger.error(f"Chyba pri aggregate_xp: {e}")
        return []


def get_storage_stats() -> Dict[str, Any]:
    """Vráti štatistiky o Hot a Cold Storage.
    
    Returns:
        Dictionary so štatistikami:
        - hot_storage_count: Počet záznamov v JSONL
        - cold_storage_count: Počet záznamov v SQLite
        - hot_storage_limit: Limit pre Hot Storage
        - sqlite_available: Či je SQLite dostupný
    """
    hot_count = _count_jsonl_entries()
    
    store = _get_sqlite_store()
    cold_count = store.count() if store else 0
    
    return {
        "hot_storage_count": hot_count,
        "cold_storage_count": cold_count,
        "hot_storage_limit": HOT_STORAGE_LIMIT,
        "sqlite_available": SQLITE_AVAILABLE and store is not None
    }


if __name__ == "__main__":
    # Príklad použitia triple-write
    print("=" * 60)
    print("LOG MANAGER - HOT/COLD STORAGE TEST")
    print("=" * 60)
    
    # Test triple-write
    add_log_entry(
        action_name="Test Hot/Cold Storage systému",
        status="completed",
        files_changed=["scripts/utils/log_manager.py"],
        xp_estimate=5.0,
        entry_type="task",
        completed=["Implementácia triple-write", "Pridanie SQLite podpory"],
        results={"md_write": "OK", "jsonl_write": "OK", "sqlite_write": "OK"}
    )
    print("✅ Triple-write test: Záznam pridaný do MD, JSONL aj SQLite")
    
    # Ukáž storage stats
    stats = get_storage_stats()
    print(f"\n📊 Storage Stats:")
    print(f"   - Hot Storage (JSONL): {stats['hot_storage_count']} záznamov")
    print(f"   - Cold Storage (SQLite): {stats['cold_storage_count']} záznamov")
    print(f"   - Hot Storage Limit: {stats['hot_storage_limit']}")
    print(f"   - SQLite Available: {stats['sqlite_available']}")
    
    # Ukáž posledné záznamy z Hot Storage
    recent = get_recent_log_entries(3)
    print(f"\n📋 Posledné 3 záznamy z Hot Storage (JSONL):")
    for entry in recent:
        print(f"   - [{entry.get('time')}] {entry.get('title')}")
    
    # Ukáž XP summary z Cold Storage
    if stats['sqlite_available']:
        xp_summary = get_xp_summary()
        print(f"\n💰 XP Summary z Cold Storage (SQLite):")
        print(f"   - Total XP: {xp_summary.get('total_xp', 0)}")
        print(f"   - By Type: {xp_summary.get('by_type', [])}")
