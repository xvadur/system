# 🤖 Prompty Vygenerované AI

**Vytvorené:** 2025-12-04 04:16  
**Zdroj:** `xvadur/data/kortex_guaranteed/ai_responses_guaranteed.jsonl`

---

## 📊 Prehľad

- **Celkom extrahovaných promptov:** 50
- **Zdrojových AI odpovedí:** 1880
- **Priemer promptov na odpoveď:** 0.03

---

## 📁 Kategórie

- **system_analysis:** 23 promptov
- **system_chat:** 2 promptov
- **system_general:** 24 promptov
- **template:** 1 promptov

---

## 📂 Súbory

- `all_prompts.jsonl` - Všetky extrahované prompty
- `by_category/` - Prompty zoskupené podľa kategórií
  - `system_analysis.jsonl` - System prompty pre analýzy
  - `system_chat.jsonl` - System prompty pre konverzácie
  - `system_general.jsonl` - Ostatné system prompty
  - `template.jsonl` - Prompt šablóny
  - `instructions.jsonl` - Inštrukčné prompty
  - `format_spec.jsonl` - Formátové špecifikácie
  - `other.jsonl` - Ostatné prompty

---

## 🔍 Ako to Funguje

Skript identifikuje prompty pomocou viacerých vzorcov:
- System prompts ("You are", "System:", "ROLE")
- Prompt markery ("[PROMPT START]", "[PROMPT END]")
- Code blocks s promptmi
- Štruktúrované prompty (sekcie: ROLE, OBJECTIVE, CONTEXT, atď.)
- Prompt templates a šablóny

---

**Automaticky vygenerované:** 2025-12-04 04:16
