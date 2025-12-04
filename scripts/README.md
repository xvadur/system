# 📜 Scripts Directory

Organizované skripty pre XVADUR workspace.

## 📂 Štruktúra

```
scripts/
├── rag/                    # RAG systém (vyhľadávanie, indexovanie)
│   ├── build_rag_index.py
│   └── rag_agent_helper.py
│
├── kortex/                 # Kortex dáta (extrakcia, analýza, chronológie)
│   ├── extract_kortex_ai_responses.py
│   ├── clean_kortex_extracted_data.py
│   ├── create_kortex_chronology.py
│   ├── analyze_kortex_monthly_metrics.py
│   ├── analyze_kortex_vs_historical.py
│   ├── compare_kortex_vs_historical_metrics.py
│   └── analyze_kortex_duplicates.py
│
├── analysis/               # Analýzy promptov (metriky, témy, depresia)
│   ├── analyze_prompts_metrics.py
│   ├── analyze_prompts_weekly_metrics.py
│   ├── analyze_prompts_topics_final.py
│   ├── analyze_prompts_nlp4sk.py
│   ├── analyze_depression_prompts.py
│   ├── analyze_depression_causes.py
│   ├── analyze_generated_prompts.py
│   ├── extract_generated_prompts_from_ai.py
│   ├── extract_prompt_activities.py
│   ├── categorize_prompts_granular.py
│   ├── visualize_prompts_analysis.py
│   ├── create_weekly_prompts_pdf.py
│   └── create_temporal_map.py
│
├── duplicates/             # Duplikáty (hľadanie, validácia, odstraňovanie)
│   ├── guarantee_no_duplicates.py
│   ├── validate_no_duplicates.py
│   ├── find_duplicate_text_blocks.py
│   ├── remove_duplicate_text_blocks.py
│   ├── quick_analyze_code_duplicates.py
│   └── analyze_text_similarity_sample.py
│
├── synthesis/              # Syntézy (chronológie, príbehy)
│   ├── synthesize_from_raw_prompts.py
│   └── synthesize_chronological_story.py
│
├── utils/                  # Utility skripty (XP, export, metadata)
│   ├── analyze_day_founder_style.py
│   ├── export_to_log.py
│   ├── merge_prompt_metadata.py
│   ├── metrics_tracker.py
│   ├── prepare_openai_finetuning.py
│   └── save_conversation_prompts.py
│
├── auto_save_prompt.py     # Aktívne používané (volané z .cursorrules)
└── calculate_xp.py         # Aktívne používané (volané z /savegame)
```

## 🚀 Aktívne Používané Skripty

### `auto_save_prompt.py`
Automatické ukladanie promptov do `xvadur/data/prompts_log.jsonl`.  
**Volané z:** `.cursorrules` (pri každej odpovedi agenta)

### `calculate_xp.py`
Automatický výpočet XP z logu a promptov.  
**Volané z:** `.cursor/commands/savegame.md` (pri každom `/savegame`)

## 📋 Kategórie

### RAG (`rag/`)
Skripty pre RAG systém - vyhľadávanie a indexovanie dát.

### Kortex (`kortex/`)
Skripty pre prácu s Kortex dátami - extrakcia AI odpovedí, čistenie dát, vytváranie chronológií.

### Analýzy (`analysis/`)
Skripty pre analýzu promptov - metriky, témy, depresia, vizualizácie.

### Duplikáty (`duplicates/`)
Skripty pre hľadanie, validáciu a odstraňovanie duplikátov.

### Syntézy (`synthesis/`)
Skripty pre syntézu dát - chronológie, príbehy, analýzy.

### Utility (`utils/`)
Pomocné skripty - XP tracking, export, metadata, finetuning.

---

**Poznámka:** Duplicitné verzie skriptov (v2, final, local) boli odstránené. Používa sa len finálna verzia.

