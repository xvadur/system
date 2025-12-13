# Save Game Template (JSON Format)

**Lokácia:** `development/sessions/save_games/SAVE_GAME.json`

**Formát:** Pracovný JSON (nie naratívny)

```json
{
  "last_updated": "YYYY-MM-DDTHH:MM:SS+00:00",
  "current_task": "[Konkrétna úloha]",
  "status": "in_progress|completed|blocked",
  "last_10_tasks": [
    {
      "time": "HH:MM",
      "task": "[Názov tasku]",
      "files": ["cesta/k/súboru.py"],
      "status": "completed|in_progress"
    }
  ],
  "files_changed": ["cesta/k/súboru.py"],
  "next_steps": [
    "Konkrétny krok 1",
    "Konkrétny krok 2"
  ],
  "blockers": [
    "Blokátor 1",
    "Blokátor 2"
  ]
}
```

**KRITICKÉ:**
- `last_updated` získavať cez MCP Time (`mcp_MCP_DOCKER_get_current_time`) s timezone
- Formát: ISO 8601 s timezone (napr. `2025-12-10T14:30:00+01:00`)
- Pracovný formát (nie naratívny) - len konkrétne dáta
