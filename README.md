# 🧠 XVADUR Workspace

**Magnum Opus: Architektúra Osobného Kognitívneho Systému**

Tento workspace slúži ako centrálny hub pre transformáciu Adama ("Sanitár") na "AI Architekta" (Human 3.0). Obsahuje kompletnú pamäť, nástroje na analýzu a systémy pre RAG.

---

## 🚀 Hlavné Komponenty

### 1. 🧠 MinisterOfMemory (`ministers/`)
Autonómny pamäťový systém, ktorý zabezpečuje, že žiadna myšlienka sa nestratí.
- **Real-time Capture:** Automatické ukladanie promptov pri každej odpovedi.
- **Storage:** JSONL databáza v `xvadur/data/prompts_log.jsonl`.
- **Architektúra:** Modulárny systém (`MinisterOfMemory`, `AssistantOfMemory`, `FileStore`).
- **Dokumentácia:** [`xvadur/docs/MEMORY_SYSTEM.md`](xvadur/docs/MEMORY_SYSTEM.md)

### 2. 📊 Kortex Dataset (`xvadur/data/dataset/`)
"Single Source of Truth" - kompletná história konverzácií s AI (Kortex Backup).
- **Obsah:** 1,822 konverzačných párov (User + AI).
- **Rozsah:** 976,917 slov, 126 aktívnych dní.
- **Kvalita:** Garantovane bez duplikátov a vyčistené.
- **Štruktúra:**
  - `prompts.jsonl` (User vstupy)
  - `responses.jsonl` (AI odpovede)
  - `conversations.jsonl` (Páry pre RAG/Finetuning)

### 3. 🔎 RAG & Analýza (`scripts/`)
Nástroje na dolovanie významu z dát.
- **Semantic Search:** Vyhľadávanie v histórii podľa významu.
- **Chronológia:** Generovanie denných/mesačných prehľadov (`xvadur/data/kortex_chronology/`).
- **Human 3.0 Evaluácia:** (V pláne) Objektívne hodnotenie transformácie.

---

## 📁 Štruktúra Adresárov

```
xvadur-workspace/
├── ministers/                  # Memory System logika (Python package)
├── scripts/                    # Automatizačné a analytické skripty
│   ├── auto_save_prompt.py     # Hook pre .cursorrules
│   ├── analysis/               # Analytické nástroje (NLP, metrics)
│   ├── kortex/                 # Spracovanie Kortex backupu
│   ├── rag/                    # RAG implementácia
│   └── utils/                  # Pomocné nástroje (vizualizácie, export)
│
├── xvadur/                     # Dátová vrstva
│   ├── data/                   # Všetky dáta
│   │   ├── dataset/            # Kortex final dataset
│   │   ├── sessions/           # Denné session dokumenty
│   │   └── kortex_analysis/    # Výstupy analýz
│   │
│   ├── docs/                   # Dokumentácia systému
│   ├── logs/                   # Operačné logy (XP, activity)
│   └── save_games/             # Checkpointy pre kontinuitu
│
├── .cursorrules                # Systémový prompt pre Cursor
└── requirements.txt            # Python závislosti
```

---

## 🛠️ Rýchly Štart

### 1. Inštalácia
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Konfigurácia
Vytvor `.env` súbor pre RAG funkcionalitu:
```bash
OPENAI_API_KEY=sk-...
```

### 3. Bežná Práca (Workflow)
Systém je navrhnutý pre **Cursor IDE**.
- **Pamäť:** Funguje automaticky na pozadí (`.cursorrules` volá `auto_save_prompt.py`).
- **Ukončenie práce:** Spusti príkaz `/savegame` (uloží kontext a vytvorí checkpoint).
- **Začiatok práce:** Spusti príkaz `/loadgame` (načíta posledný checkpoint).

---

## 📈 Metriky Transformácie

- **Celkový výkon (Kortex):** 976,917 slov
- **Aktuálny Level:** 2.5 (Synthesist) -> Cieľ 3.0
- **Dominantný Mód:** "Operational Excellence" (Efektivita)

---

**Vytvorené:** 2025-12-04  
**Status:** ✅ Aktívny & Stabilný
