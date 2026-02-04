# 🏛️ ARCHITECTURE.md - THE MONOLITH v1.0

## 1. Vision & Strategy
The Monolith is a sovereign AI infrastructure designed for XVADUR. It serves as a complex capture system, business orchestrator, and real-time intelligence hub.

**Core Principles:**
- **Local-First:** Data stays in `/Users/_xvadur/clawd/`.
- **Hybrid Brain:** Clawdbot as the Orchestrator between Local FS, Notion, and Cloud Models.
- **Context Management:** Tiered memory (Local Markdown -> Notion -> Long-term MEMORY.md).
- **Proactive Intelligence:** Automated morning briefings and background research.

## 2. Technical Stack
- **Orchestrator:** Clawdbot (running on macOS).
- **Primary Interface:** Telegram / Webchat.
- **Data Layers:**
  - **Notion:** Business Metrics, CRM (BNI), Task Tracking.
  - **Local FS:** Project code, raw logs (`/memory/`), and architectural manifests.
  - **Memory:** `MEMORY.md` (Self-reflecting long-term memory).
- **Tooling:** Brave Search API, YouTube Scraper (browser tool), n8n (automation), Cron (scheduling).

## 3. Workflows

### A. Morning Briefing (The Oracle)
- **Time:** 07:00 (Configured via `cron`).
- **Steps:**
  1. Deep Search (Brave) on defined sources (`SOURCES.md`).
  2. Scan Notion Inbox & Projects.
  3. Synthesize "State of the World vs. State of Identity".
  4. Deliver 1-page report to Adam.

### B. Capture & Logging (The Scribe)
- **Trigger:** End of conversation or specific `/log` command.
- **Action:** 
  1. Extract `wins`, `loss`, `insights`, and `tasks`.
  2. Update daily log in `/memory/YYYY-MM-DD.md`.
  3. Sync structured data to Notion.
  4. Update `MEMORY.md` if significant identity shifts occur.

### C. Intelligence Gathering (The Scout)
- **Action:** Recurring scans for specific keywords (Epstein Files, AI Swarms, SK Politics).
- **Output:** Briefings populated into a dedicated "Intelligence" database in Notion.

## 4. Hardware Roadmap
1. **Current:** MacBook Air M3 (Local orchestration).
2. **Target:** Dedicated Linux Box (Server) with high-end GPU for running Open Source models (Llama 3, DeepSeek) to achieve full privacy and zero token cost.

---
*Created on 2026-02-03 | Author: Clawdbot (for XVADUR)*
