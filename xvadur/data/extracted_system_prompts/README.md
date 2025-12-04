# 🤖 Prompty Vygenerované AI

**Vytvorené:** 2025-12-04 04:16  
**Zdroj:** `xvadur/data/dataset/responses.jsonl`

---

## 📊 Prehľad

- **Celkom extrahovaných promptov:** 50
- **Zdrojových AI odpovedí:** 1,880
- **Formát:** JSONL (jeden prompt na riadok)

---

## 📂 Súbor

- **`extracted_system_prompts.jsonl`** - Všetky extrahované prompty z datasetu

Každý riadok obsahuje JSON objekt s týmito poliami:
- `prompt` - Text promptu
- `prompt_type` - Typ promptu (system_prompt, code_block_prompt, prompt_marker, atď.)
- `source` - Zdroj extrakcie (text_extraction, code_block, marker_extraction)
- `category` - Kategória (system_analysis, system_chat, system_general, template)
- `response_uuid` - UUID AI odpovede, z ktorej bol prompt extrahovaný
- `response_session` - Session ID
- `response_timestamp` - Časová značka odpovede
- `word_count` - Počet slov v prompte
- `char_count` - Počet znakov v prompte

---

## 🔍 Ako to Funguje

Prompty boli extrahované z AI odpovedí pomocou viacerých vzorcov:
- System prompts ("You are", "System:", "ROLE")
- Prompt markery ("[PROMPT START]", "[PROMPT END]")
- Code blocks s promptmi
- Štruktúrované prompty (sekcie: ROLE, OBJECTIVE, CONTEXT, atď.)
- Prompt templates a šablóny

---

## 📈 Kategórie v Datasete

Prompty sú kategorizované podľa typu:
- **system_analysis** - System prompty pre analýzy
- **system_chat** - System prompty pre konverzácie
- **system_general** - Ostatné system prompty
- **template** - Prompt šablóny

---

**Vytvorené:** 2025-12-04 04:16  
**Skript:** `scripts/analysis/extract_generated_prompts_from_ai.py`
