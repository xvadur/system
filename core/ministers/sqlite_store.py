"""SQLite Storage Backend pre Cold Storage architektúru.

Tento modul poskytuje SQLiteStore - persistentný backend pre archiváciu
log záznamov. Slúži ako "Cold Storage" pre historické dáta, zatiaľ čo
JSONL zostáva "Hot Storage" pre runtime kontext.

Výhody SQLite:
- Indexované vyhľadávanie (O(log n))
- SQL query pre komplexné analýzy
- Agregácie (SUM, COUNT, GROUP BY)
- Neobmedzená kapacita

Použitie:
    from core.ministers.sqlite_store import SQLiteStore
    
    store = SQLiteStore("development/data/archive.db")
    store.insert(entry)
    results = store.query(type="task", limit=10)
"""

from __future__ import annotations

import json
import logging
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)


class SQLiteStore:
    """SQLite backend pre Cold Storage - archivácia log záznamov.
    
    Poskytuje:
    - Persistentné úložisko pre všetky log záznamy
    - Indexované vyhľadávanie podľa timestamp, type, quest_id
    - SQL query pre komplexné analýzy
    - Agregácie pre metriky a reporty
    """
    
    # SQL schéma pre log_entries tabuľku
    SCHEMA = """
    CREATE TABLE IF NOT EXISTS log_entries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT NOT NULL,
        date TEXT NOT NULL,
        time TEXT NOT NULL,
        title TEXT NOT NULL,
        type TEXT NOT NULL,
        status TEXT NOT NULL,
        files_changed TEXT,
        xp_estimate REAL,
        completed TEXT,
        results TEXT,
        decisions TEXT,
        quest_id INTEGER,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    );
    
    CREATE INDEX IF NOT EXISTS idx_timestamp ON log_entries(timestamp);
    CREATE INDEX IF NOT EXISTS idx_type ON log_entries(type);
    CREATE INDEX IF NOT EXISTS idx_quest_id ON log_entries(quest_id);
    CREATE INDEX IF NOT EXISTS idx_date ON log_entries(date);
    CREATE INDEX IF NOT EXISTS idx_status ON log_entries(status);
    """

    def __init__(self, db_path: str | Path) -> None:
        """Inicializuje SQLiteStore s cestou k databáze.
        
        Args:
            db_path: Cesta k SQLite databázovému súboru.
                     Adresár bude vytvorený ak neexistuje.
        """
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Inicializuj schému
        self._init_schema()
        logger.info(f"SQLiteStore inicializovaný: {self.db_path}")

    def _get_connection(self) -> sqlite3.Connection:
        """Vytvorí nové spojenie s databázou.
        
        Returns:
            sqlite3.Connection objekt s row_factory nastavenou na sqlite3.Row
        """
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        return conn

    def _init_schema(self) -> None:
        """Inicializuje databázovú schému ak neexistuje."""
        try:
            with self._get_connection() as conn:
                conn.executescript(self.SCHEMA)
                conn.commit()
            logger.debug("Databázová schéma inicializovaná")
        except sqlite3.Error as e:
            logger.error(f"Chyba pri inicializácii schémy: {e}")
            raise

    def insert(self, entry: Dict[str, Any]) -> int:
        """Vloží nový záznam do databázy.
        
        Args:
            entry: Dictionary s log záznamom (rovnaký formát ako JSONL)
            
        Returns:
            ID vloženého záznamu
        """
        # Serializuj JSON polia
        files_changed = json.dumps(entry.get('files_changed')) if entry.get('files_changed') else None
        completed = json.dumps(entry.get('completed')) if entry.get('completed') else None
        results = json.dumps(entry.get('results')) if entry.get('results') else None
        decisions = json.dumps(entry.get('decisions')) if entry.get('decisions') else None
        
        sql = """
        INSERT INTO log_entries (
            timestamp, date, time, title, type, status,
            files_changed, xp_estimate, completed, results, decisions, quest_id
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        
        params = (
            entry.get('timestamp', datetime.now().isoformat()),
            entry.get('date', datetime.now().strftime('%Y-%m-%d')),
            entry.get('time', datetime.now().strftime('%H:%M')),
            entry.get('title', ''),
            entry.get('type', 'task'),
            entry.get('status', 'unknown'),
            files_changed,
            entry.get('xp_estimate'),
            completed,
            results,
            decisions,
            entry.get('quest_id')
        )
        
        try:
            with self._get_connection() as conn:
                cursor = conn.execute(sql, params)
                conn.commit()
                row_id = cursor.lastrowid
                logger.debug(f"Vložený záznam ID={row_id}: {entry.get('title')}")
                return row_id
        except sqlite3.Error as e:
            logger.error(f"Chyba pri vkladaní záznamu: {e}")
            raise

    def insert_batch(self, entries: List[Dict[str, Any]]) -> int:
        """Vloží viacero záznamov naraz (efektívnejšie pre migráciu).
        
        Args:
            entries: Zoznam log záznamov
            
        Returns:
            Počet vložených záznamov
        """
        if not entries:
            return 0
        
        sql = """
        INSERT INTO log_entries (
            timestamp, date, time, title, type, status,
            files_changed, xp_estimate, completed, results, decisions, quest_id
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        
        params_list = []
        for entry in entries:
            files_changed = json.dumps(entry.get('files_changed')) if entry.get('files_changed') else None
            completed = json.dumps(entry.get('completed')) if entry.get('completed') else None
            results = json.dumps(entry.get('results')) if entry.get('results') else None
            decisions = json.dumps(entry.get('decisions')) if entry.get('decisions') else None
            
            params_list.append((
                entry.get('timestamp', datetime.now().isoformat()),
                entry.get('date', datetime.now().strftime('%Y-%m-%d')),
                entry.get('time', datetime.now().strftime('%H:%M')),
                entry.get('title', ''),
                entry.get('type', 'task'),
                entry.get('status', 'unknown'),
                files_changed,
                entry.get('xp_estimate'),
                completed,
                results,
                decisions,
                entry.get('quest_id')
            ))
        
        try:
            with self._get_connection() as conn:
                conn.executemany(sql, params_list)
                conn.commit()
                logger.info(f"Vložených {len(params_list)} záznamov")
                return len(params_list)
        except sqlite3.Error as e:
            logger.error(f"Chyba pri batch vkladaní: {e}")
            raise

    def query(
        self,
        type: Optional[str] = None,
        status: Optional[str] = None,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None,
        quest_id: Optional[int] = None,
        limit: int = 100,
        offset: int = 0,
        order_by: str = "timestamp DESC"
    ) -> List[Dict[str, Any]]:
        """Vyhľadá záznamy podľa filtrov.
        
        Args:
            type: Filter podľa typu (task, session, quest_created, atď.)
            status: Filter podľa statusu (started, completed, atď.)
            date_from: Filter od dátumu (YYYY-MM-DD)
            date_to: Filter do dátumu (YYYY-MM-DD)
            quest_id: Filter podľa quest ID
            limit: Maximálny počet výsledkov
            offset: Offset pre stránkovanie
            order_by: Zoradenie (default: timestamp DESC)
            
        Returns:
            Zoznam záznamov ako dictionary
        """
        conditions = []
        params = []
        
        if type:
            conditions.append("type = ?")
            params.append(type)
        
        if status:
            conditions.append("status = ?")
            params.append(status)
        
        if date_from:
            conditions.append("date >= ?")
            params.append(date_from)
        
        if date_to:
            conditions.append("date <= ?")
            params.append(date_to)
        
        if quest_id is not None:
            conditions.append("quest_id = ?")
            params.append(quest_id)
        
        where_clause = " AND ".join(conditions) if conditions else "1=1"
        
        sql = f"""
        SELECT * FROM log_entries
        WHERE {where_clause}
        ORDER BY {order_by}
        LIMIT ? OFFSET ?
        """
        params.extend([limit, offset])
        
        try:
            with self._get_connection() as conn:
                cursor = conn.execute(sql, params)
                rows = cursor.fetchall()
                
                # Konvertuj na dictionary a deserializuj JSON polia
                results = []
                for row in rows:
                    entry = dict(row)
                    # Deserializuj JSON polia
                    if entry.get('files_changed'):
                        entry['files_changed'] = json.loads(entry['files_changed'])
                    if entry.get('completed'):
                        entry['completed'] = json.loads(entry['completed'])
                    if entry.get('results'):
                        entry['results'] = json.loads(entry['results'])
                    if entry.get('decisions'):
                        entry['decisions'] = json.loads(entry['decisions'])
                    results.append(entry)
                
                logger.debug(f"Query vrátil {len(results)} záznamov")
                return results
        except sqlite3.Error as e:
            logger.error(f"Chyba pri query: {e}")
            raise

    def count(
        self,
        type: Optional[str] = None,
        status: Optional[str] = None,
        quest_id: Optional[int] = None
    ) -> int:
        """Spočíta záznamy podľa filtrov.
        
        Args:
            type: Filter podľa typu
            status: Filter podľa statusu
            quest_id: Filter podľa quest ID
            
        Returns:
            Počet záznamov
        """
        conditions = []
        params = []
        
        if type:
            conditions.append("type = ?")
            params.append(type)
        
        if status:
            conditions.append("status = ?")
            params.append(status)
        
        if quest_id is not None:
            conditions.append("quest_id = ?")
            params.append(quest_id)
        
        where_clause = " AND ".join(conditions) if conditions else "1=1"
        
        sql = f"SELECT COUNT(*) FROM log_entries WHERE {where_clause}"
        
        try:
            with self._get_connection() as conn:
                cursor = conn.execute(sql, params)
                return cursor.fetchone()[0]
        except sqlite3.Error as e:
            logger.error(f"Chyba pri count: {e}")
            raise

    def aggregate(
        self,
        field: str,
        agg_func: str = "SUM",
        group_by: Optional[str] = None,
        type: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Vykoná agregáciu nad dátami.
        
        Args:
            field: Pole pre agregáciu (napr. "xp_estimate")
            agg_func: Agregačná funkcia (SUM, COUNT, AVG, MIN, MAX)
            group_by: Pole pre GROUP BY (napr. "type", "date")
            type: Filter podľa typu
            
        Returns:
            Zoznam agregovaných výsledkov
        """
        # Validuj agg_func
        valid_funcs = ["SUM", "COUNT", "AVG", "MIN", "MAX"]
        if agg_func.upper() not in valid_funcs:
            raise ValueError(f"Neplatná agregačná funkcia: {agg_func}")
        
        # Validuj field (ochrana pred SQL injection)
        valid_fields = ["xp_estimate", "id", "quest_id"]
        if field not in valid_fields:
            raise ValueError(f"Neplatné pole pre agregáciu: {field}")
        
        # Validuj group_by
        valid_group_by = ["type", "status", "date", "quest_id", None]
        if group_by not in valid_group_by:
            raise ValueError(f"Neplatné group_by pole: {group_by}")
        
        conditions = []
        params = []
        
        if type:
            conditions.append("type = ?")
            params.append(type)
        
        where_clause = " AND ".join(conditions) if conditions else "1=1"
        
        if group_by:
            sql = f"""
            SELECT {group_by}, {agg_func.upper()}({field}) as value
            FROM log_entries
            WHERE {where_clause}
            GROUP BY {group_by}
            ORDER BY value DESC
            """
        else:
            sql = f"""
            SELECT {agg_func.upper()}({field}) as value
            FROM log_entries
            WHERE {where_clause}
            """
        
        try:
            with self._get_connection() as conn:
                cursor = conn.execute(sql, params)
                rows = cursor.fetchall()
                return [dict(row) for row in rows]
        except sqlite3.Error as e:
            logger.error(f"Chyba pri agregácii: {e}")
            raise

    def get_xp_summary(self) -> Dict[str, Any]:
        """Vráti sumár XP zo všetkých záznamov.
        
        Returns:
            Dictionary s XP štatistikami
        """
        try:
            with self._get_connection() as conn:
                # Celkové XP
                total = conn.execute(
                    "SELECT SUM(xp_estimate) as total FROM log_entries WHERE xp_estimate IS NOT NULL"
                ).fetchone()
                
                # XP podľa typu
                by_type = conn.execute("""
                    SELECT type, SUM(xp_estimate) as xp
                    FROM log_entries
                    WHERE xp_estimate IS NOT NULL
                    GROUP BY type
                    ORDER BY xp DESC
                """).fetchall()
                
                # XP podľa dňa (posledných 7 dní)
                by_day = conn.execute("""
                    SELECT date, SUM(xp_estimate) as xp
                    FROM log_entries
                    WHERE xp_estimate IS NOT NULL
                    GROUP BY date
                    ORDER BY date DESC
                    LIMIT 7
                """).fetchall()
                
                return {
                    "total_xp": total[0] if total[0] else 0,
                    "by_type": [dict(row) for row in by_type],
                    "by_day": [dict(row) for row in by_day]
                }
        except sqlite3.Error as e:
            logger.error(f"Chyba pri XP summary: {e}")
            raise

    def get_quest_summary(self, quest_id: int) -> Dict[str, Any]:
        """Vráti sumár pre konkrétny quest.
        
        Args:
            quest_id: ID questu
            
        Returns:
            Dictionary so sumárom questu
        """
        try:
            with self._get_connection() as conn:
                entries = conn.execute(
                    "SELECT * FROM log_entries WHERE quest_id = ? ORDER BY timestamp",
                    (quest_id,)
                ).fetchall()
                
                if not entries:
                    return {"quest_id": quest_id, "found": False}
                
                total_xp = sum(e['xp_estimate'] or 0 for e in entries)
                statuses = [e['status'] for e in entries]
                
                return {
                    "quest_id": quest_id,
                    "found": True,
                    "entry_count": len(entries),
                    "total_xp": total_xp,
                    "statuses": statuses,
                    "first_entry": dict(entries[0]),
                    "last_entry": dict(entries[-1])
                }
        except sqlite3.Error as e:
            logger.error(f"Chyba pri quest summary: {e}")
            raise

    def delete_before(self, date: str) -> int:
        """Vymaže záznamy staršie ako zadaný dátum.
        
        Args:
            date: Dátum (YYYY-MM-DD), záznamy pred týmto dátumom budú vymazané
            
        Returns:
            Počet vymazaných záznamov
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.execute(
                    "DELETE FROM log_entries WHERE date < ?",
                    (date,)
                )
                conn.commit()
                deleted = cursor.rowcount
                logger.info(f"Vymazaných {deleted} záznamov pred {date}")
                return deleted
        except sqlite3.Error as e:
            logger.error(f"Chyba pri mazaní: {e}")
            raise

    def vacuum(self) -> None:
        """Optimalizuje databázu (uvoľní miesto po DELETE operáciách)."""
        try:
            with self._get_connection() as conn:
                conn.execute("VACUUM")
            logger.info("Databáza optimalizovaná (VACUUM)")
        except sqlite3.Error as e:
            logger.error(f"Chyba pri VACUUM: {e}")
            raise


# Export
__all__ = ["SQLiteStore"]

