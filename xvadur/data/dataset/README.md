# 📂 Kortex Dataset

Tento adresár obsahuje finálny, vyčistený dataset z Kortex AI backupu.
Všetky duplikáty boli odstránené a dáta boli skonsolidované.

## 📄 Súbory

- **`prompts.jsonl`** (1,801 riadkov)
  - Čisté user prompty (otázky od Adama).
  - Garantovane unikátne.
  
- **`responses.jsonl`** (1,880 riadkov)
  - Odpovede AI (Claude/GPT).
  - Obsahuje kompletné znenie odpovedí.

- **`conversations.jsonl`** (1,822 riadkov)
  - Páry `{"prompt": "...", "response": "..."}`.
  - Ideálne pre finetuning alebo RAG.

- **`stats.json`**
  - Štatistiky o procese čistenia a deduplikácie.

## 📊 Pôvod Dát
- **Zdroj:** Kortex AI Backup (JSON export).
- **Proces:** Extrakcia -> Čistenie -> Deduplikácia (Final/Guaranteed).
- **Dátum konsolidácie:** 2025-12-04

## 🔗 Analýza
Detailná analýza tohto datasetu sa nachádza v `xvadur/data/kortex_analysis/KORTEX_ANALYSIS.md`.

