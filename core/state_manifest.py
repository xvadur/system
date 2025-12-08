"""State manifest utilities for lightweight save/load orchestration."""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional


@dataclass
class StateManifest:
    """Typed view over ``development/state_manifest.json``.

    The manifest acts as the single entrypoint for save/load logic and trims
    token usage by pointing directly to the minimal files that need to be
    parsed.
    """

    path: Path
    data: Dict[str, Any]

    # AETH: Keep loading deterministic and side-effect free.
    @classmethod
    def load(cls, path: str | Path = "development/state_manifest.json") -> "StateManifest":
        manifest_path = Path(path)
        content = json.loads(manifest_path.read_text(encoding="utf-8"))
        return cls(path=manifest_path, data=content)

    # AETH: Mutations should be explicit to preserve traceability.
    def update(self, **fields: Any) -> None:
        self.data.update(fields)

    # AETH: Refresh the manifest timestamp when persisting orchestrated changes.
    def save(self) -> None:
        self.data["last_updated"] = datetime.utcnow().isoformat()
        self.path.parent.mkdir(parents=True, exist_ok=True)
        serialized = json.dumps(self.data, ensure_ascii=False, indent=2)
        self.path.write_text(serialized, encoding="utf-8")

    # AETH: Centralized path resolution keeps cursor commands consistent.
    def resolve_path(self, key: str) -> Optional[Path]:
        path_value = self.data.get("paths", {}).get(key)
        return Path(path_value) if path_value else None

    # AETH: Provide bounded log reads to protect token budgets.
    def recent_main_log_entries(self) -> List[Dict[str, Any]]:
        log_path = self.resolve_path("log_main")
        if not log_path or not log_path.exists():
            return []
        limit = int(self.data.get("log_window", {}).get("main_last_n", 5))
        entries: List[Dict[str, Any]] = []
        for line in log_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                entries.append(json.loads(line))
            except json.JSONDecodeError:
                continue
        return entries[-limit:]

    # AETH: Surface XP state without reprocessing narratives.
    def xp_status(self) -> Dict[str, Any]:
        xp_path = self.resolve_path("log_xp")
        if not xp_path or not xp_path.exists():
            return {}
        xp_payload = json.loads(xp_path.read_text(encoding="utf-8"))
        return xp_payload.get("status", xp_payload)

    # AETH: Load compact savegame JSON when required for deeper context.
    def savegame_payload(self) -> Dict[str, Any]:
        savegame_path = self.resolve_path("savegame")
        if not savegame_path or not savegame_path.exists():
            return {}
        return json.loads(savegame_path.read_text(encoding="utf-8"))

    # AETH: Provide a terse status block for /status or quick health checks.
    def status_report(self) -> Dict[str, Any]:
        savegame = self.savegame_payload()
        narrative_summary = savegame.get("narrative", {}).get("summary") if isinstance(savegame, dict) else None
        return {
            "last_updated": self.data.get("last_updated"),
            "active_project": self.data.get("active_project"),
            "current_focus": self.data.get("current_focus"),
            "session": self.data.get("session", {}),
            "xp": self.xp_status(),
            "recent_log_entries": self.recent_main_log_entries(),
            "narrative_summary": narrative_summary,
        }


__all__ = ["StateManifest"]
