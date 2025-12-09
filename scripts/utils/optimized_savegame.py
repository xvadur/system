#!/usr/bin/env python3
"""
Optimalizovaný Save Game Workflow s Context Engineering.

Tento modul integruje:
- TokenBudgetTracker - tracking tokenov
- IsolateContextManager - izolácia relevantného kontextu
- CompressContextManager - kompresia keď utilization > threshold
- Selektívne načítanie súborov (offset/limit)
"""

import sys
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Optional

# Add workspace root to path
workspace_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(workspace_root))

from core.context_engineering.token_metrics import TokenBudgetTracker, TokenBudget
from core.context_engineering.compress_context import CompressContextManager
from core.context_engineering.isolate_context import IsolateContextManager, IsolationConfig
from core.context_engineering.config import (
    COMPRESSION_THRESHOLD,
    TARGET_COMPRESSION_RATIO,
    CONTEXT_WINDOW_SIZE,
    ISOLATION_MAX_TOKENS
)
from core.ministers.memory import MinisterOfMemory, AssistantOfMemory
from core.ministers.storage import FileStore
from scripts.utils.save_conversation_prompts import save_prompts_batch
from core.xp.calculator import calculate_xp, update_xp_file


class OptimizedSaveGame:
    """Optimalizovaný Save Game workflow s context engineering."""
    
    def __init__(self):
        """Inicializuje optimalizovaný save game workflow."""
        self.tracker = TokenBudgetTracker(TokenBudget(context_window_size=CONTEXT_WINDOW_SIZE))
        self.isolation_config = IsolationConfig(
            max_tokens=ISOLATION_MAX_TOKENS,
            max_turns=3,
            pruning_strategy="drop_oldest"
        )
        self.isolator = IsolateContextManager(self.isolation_config)
        
        # Cesty k súborom
        self.save_game_md = workspace_root / "development" / "sessions" / "save_games" / "SAVE_GAME.md"
        self.save_game_json = workspace_root / "development" / "sessions" / "save_games" / "SAVE_GAME_LATEST.json"
        self.xp_md = workspace_root / "development" / "logs" / "XVADUR_XP.md"
        self.xp_json = workspace_root / "development" / "logs" / "XVADUR_XP.json"
        self.log_md = workspace_root / "development" / "logs" / "XVADUR_LOG.md"
        self.log_jsonl = workspace_root / "development" / "logs" / "XVADUR_LOG.jsonl"
        self.prompts_log = workspace_root / "development" / "data" / "prompts_log.jsonl"
        
    def read_file_selective(
        self,
        file_path: Path,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        section: Optional[str] = None
    ) -> str:
        """Selektívne načítanie súboru s token tracking.
        
        Args:
            file_path: Cesta k súboru
            offset: Začiatok načítania (riadok)
            limit: Počet riadkov na načítanie
            section: Názov sekcie (ak je Markdown)
            
        Returns:
            Obsah súboru (alebo jeho časť)
        """
        if not file_path.exists():
            return ""
        
        content = file_path.read_text(encoding='utf-8')
        lines = content.split('\n')
        
        # Ak je zadaná sekcia (pre Markdown)
        if section:
            in_section = False
            section_lines = []
            for i, line in enumerate(lines):
                if line.startswith(f"## {section}") or line.startswith(f"# {section}"):
                    in_section = True
                    section_lines.append(line)
                elif in_section:
                    if line.startswith('##') or line.startswith('#'):
                        break
                    section_lines.append(line)
            content = '\n'.join(section_lines)
        # Ak je zadaný offset/limit
        elif offset is not None or limit is not None:
            start = offset or 0
            end = start + limit if limit else len(lines)
            content = '\n'.join(lines[start:end])
        
        # Trackuj tokeny
        tokens = self.tracker.estimate_tokens(content)
        return content
    
    def get_xp_status(self) -> Dict[str, Any]:
        """Načíta XP status selektívne (len status sekcia)."""
        try:
            # Skús JSON najprv (rýchlejšie)
            if self.xp_json.exists():
                with open(self.xp_json, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return data.get('status', {})
            
            # Fallback na Markdown - len status sekcia
            content = self.read_file_selective(self.xp_md, section="📊 Aktuálny Status")
            # Parsuj len základné hodnoty
            # TODO: Lepšie parsovanie
            return {}
        except Exception as e:
            print(f"⚠️ Chyba pri načítaní XP status: {e}", file=sys.stderr)
            return {}
    
    def get_recent_log_entries(self, limit: int = 5) -> List[Dict[str, Any]]:
        """Načíta posledné záznamy z logu selektívne."""
        entries = []
        
        try:
            # Skús JSONL najprv
            if self.log_jsonl.exists():
                with open(self.log_jsonl, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    # Načítaj posledných N záznamov
                    for line in lines[-limit:]:
                        if line.strip():
                            try:
                                entries.append(json.loads(line))
                            except json.JSONDecodeError:
                                continue
                return entries
            
            # Fallback na Markdown - len posledných N záznamov
            content = self.read_file_selective(self.log_md)
            # Parsuj len posledné záznamy
            # TODO: Lepšie parsovanie Markdown
            return entries
        except Exception as e:
            print(f"⚠️ Chyba pri načítaní logu: {e}", file=sys.stderr)
            return []
    
    def get_latest_save_game_summary(self) -> Dict[str, Any]:
        """Načíta len summary z posledného save game (nie celý súbor)."""
        try:
            if self.save_game_json.exists():
                with open(self.save_game_json, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return {
                        'status': data.get('status', {}),
                        'summary': data.get('narrative', {}).get('summary', ''),
                        'quests': data.get('quests', [])
                    }
            
            # Fallback na Markdown - len posledný záznam
            content = self.read_file_selective(self.save_game_md)
            # Extrahuj len posledný záznam (od posledného "# 💾 SAVE GAME:")
            # TODO: Lepšie parsovanie
            return {}
        except Exception as e:
            print(f"⚠️ Chyba pri načítaní save game: {e}", file=sys.stderr)
            return {}
    
    def save_prompts_optimized(self, prompts: List[Dict[str, Any]]) -> int:
        """Uloží prompty s automatickou kompresiou ak je potrebné."""
        saved_count = save_prompts_batch(prompts)
        
        # Skontroluj utilization po uložení
        if self.prompts_log.exists():
            try:
                file_store = FileStore(self.prompts_log)
                assistant = AssistantOfMemory(store=file_store)
                minister = MinisterOfMemory(assistant=assistant)
                
                recent_records = minister.review_context(limit=50)
                if recent_records:
                    history_content = "\n".join([r.to_summary() for r in recent_records])
                    metrics = self.tracker.track_usage(history_content=history_content)
                    utilization = metrics.utilization_ratio(CONTEXT_WINDOW_SIZE)
                    
                    # Ak je utilization vysoká, komprimuj
                    if utilization > COMPRESSION_THRESHOLD:
                        compressor = CompressContextManager(file_store)
                        result = compressor.consolidate_memory(
                            limit=20,
                            target_compression_ratio=TARGET_COMPRESSION_RATIO
                        )
                        print(f"✅ Kompresia aplikovaná: {result.compression_ratio:.2f}", file=sys.stderr)
            except Exception as e:
                print(f"⚠️ Chyba pri kompresii: {e}", file=sys.stderr)
        
        return saved_count
    
    def calculate_xp_optimized(self) -> Dict[str, Any]:
        """Vypočíta XP s optimalizáciou."""
        if not self.prompts_log.exists() or not self.log_md.exists():
            return {}
        
        # Použi existujúci calculator
        xp_data = calculate_xp(str(self.prompts_log), str(self.log_md))
        
        # Aktualizuj súbory
        update_xp_file(str(self.xp_md), xp_data)
        
        # Ulož JSON
        xp_status = {
            'status': {
                'total_xp': xp_data.get('total_xp', 0),
                'level': xp_data.get('current_level', 1),
                'next_level': xp_data.get('next_level_xp', 10),
                'streak_days': xp_data.get('streak_days', 0)
            },
            'breakdown': xp_data.get('breakdown', {}),
            'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M')
        }
        
        with open(self.xp_json, 'w', encoding='utf-8') as f:
            json.dump(xp_status, f, indent=2, ensure_ascii=False)
        
        return xp_data
    
    def create_save_game_optimized(
        self,
        narrative: str,
        quests: List[Dict[str, Any]],
        instructions: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Vytvorí save game s optimalizáciou tokenov."""
        # Načítaj len potrebné dáta
        xp_status = self.get_xp_status()
        recent_logs = self.get_recent_log_entries(limit=5)
        latest_summary = self.get_latest_save_game_summary()
        
        # Vytvor save game objekt
        save_game = {
            'metadata': {
                'created_at': datetime.now().isoformat(),
                'session_date': datetime.now().strftime('%Y-%m-%d'),
                'session_name': ''
            },
            'status': {
                'rank': xp_status.get('rank', 'AI Developer'),
                'level': xp_status.get('level', 1),
                'xp': xp_status.get('total_xp', 0),
                'xp_next_level': xp_status.get('next_level', 10),
                'xp_percent': 0.0,
                'streak_days': xp_status.get('streak_days', 0)
            },
            'narrative': {
                'summary': narrative,
                'key_decisions': [],
                'key_moments': [],
                'tools_created': [],
                'open_loops': []
            },
            'quests': quests,
            'instructions': instructions
        }
        
        # Vypočítaj percento
        if save_game['status']['xp_next_level'] > 0:
            save_game['status']['xp_percent'] = round(
                (save_game['status']['xp'] / save_game['status']['xp_next_level']) * 100,
                1
            )
        
        return save_game
    
    def execute_optimized_savegame(
        self,
        prompts: List[Dict[str, Any]],
        narrative: str,
        quests: List[Dict[str, Any]],
        instructions: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Hlavná funkcia pre optimalizovaný savegame workflow.
        
        Args:
            prompts: Zoznam promptov na uloženie
            narrative: Naratívny kontext
            quests: Zoznam questov
            instructions: Inštrukcie pre agenta
            
        Returns:
            Dictionary s výsledkami
        """
        results = {
            'prompts_saved': 0,
            'xp_calculated': False,
            'save_game_created': False,
            'token_usage': {},
            'compression_applied': False
        }
        
        # 1. Ulož prompty s kompresiou
        print("📝 Krok 1/4: Ukladanie promptov...", file=sys.stderr)
        results['prompts_saved'] = self.save_prompts_optimized(prompts)
        
        # 2. Vypočítaj XP
        print("🎮 Krok 2/4: Výpočet XP...", file=sys.stderr)
        xp_data = self.calculate_xp_optimized()
        results['xp_calculated'] = bool(xp_data)
        
        # 3. Vytvor save game
        print("💾 Krok 3/4: Vytváranie save game...", file=sys.stderr)
        save_game = self.create_save_game_optimized(narrative, quests, instructions)
        
        # Ulož JSON
        self.save_game_json.parent.mkdir(parents=True, exist_ok=True)
        with open(self.save_game_json, 'w', encoding='utf-8') as f:
            json.dump(save_game, f, indent=2, ensure_ascii=False)
        
        # Append Markdown (len nový záznam)
        # TODO: Implementovať append len nového záznamu
        
        results['save_game_created'] = True
        
        # 4. Trackuj tokeny
        print("📊 Krok 4/4: Tracking tokenov...", file=sys.stderr)
        metrics = self.tracker.get_metrics_summary()
        results['token_usage'] = metrics
        
        return results


if __name__ == "__main__":
    # Test
    optimizer = OptimizedSaveGame()
    print("✅ OptimizedSaveGame inicializovaný")
