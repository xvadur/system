# 🧠 XVADUR Konverzačný Režim

**Status:** ✅ Implementovaný  
**Režim:** Filozofický, Reflexívny, Kreatívny  
**Účel:** Dokumentácia transformácie, mapovanie cesty, identifikácia vzorcov

---

## 📋 Prehľad

Xvadur režim je **úplne oddelený** od oficiálneho workflow. Tu sa **nekóduje ani nepracuje na konkrétnych dátach**, ale rozpráva sa, filozofuje a vymýšľa.

### Kľúčové Charakteristiky

- **Prítomný čas:** Adam rozpráva v prítomnom čase
- **Odkazovanie na minulosť:** Pre pochopenie budúcnosti
- **Rekurzívne mapovanie:** Vracanie sa k udalostiam života
- **Analytická dokumentácia:** Objektívne, bez obalu
- **Backlinking:** Automatické vytváranie `[[]]` linkov
- **Knowledge Graph:** Mapovanie vzťahov medzi dokumentmi

---

## 📁 Štruktúra

```
xvadur_obsidian/xvadur/
├── XVADUR_LOG.md          # Chronologický log (aktualizuje sa pri každom /xvadur)
├── XVADUR_XP.md           # Vlastný XP tracking systém
├── metrics/               # Kvantitatívne metriky
│   ├── daily_metrics.json
│   └── session_metrics.json
├── sessions/              # Individuálne session dokumenty
└── synthesis/             # Syntetizované analýzy
```

---

## 🚀 Použitie

### Spustenie Režimu

V Cursor agentovi použite command:
```
/xvadur
```

### Workflow

1. **Štart Session:** Agent načíta kontext z `XVADUR_LOG.md`
2. **Počas Konverzácie:** 
   - Dokumentuje hlavné myšlienky
   - Extrahuje entity a vytvára backlinky
   - Identifikuje vzorce
   - Používa RAG na požiadanie
3. **Koniec Session:**
   - Aktualizuje `XVADUR_LOG.md`
   - Vypočíta XP
   - Aktualizuje `XVADUR_XP.md`
   - Vytvorí backlinky

---

## 🔗 Backlinking Systém

### Automatické Linkovanie

Systém automaticky vytvára `[[]]` linky na relevantné dokumenty:

- **Projekty:** "Recepčná" → `[[Recepcia]]`
- **Chronológie:** odkaz na minulosť → `[[CHRONOLOGICAL_MAP_2025]]`
- **Checkpointy:** aktuálny stav → `[[CHECKPOINT_LATEST]]`
- **Profily:** identita → `[[xvadur_profile]]`
- **Atlas:** koncepty → `[[Atlas/Dots/Statements/...]]`
- **Milestones:** dôležité udalosti → `[[milestones/...]]`

### Python Skripty

**Backlinking systém:**
```
xvadur_obsidian/xvadur/scripts/xvadur_backlinking.py
```
**Použitie:**
```bash
cd xvadur_obsidian/xvadur/scripts
python3 xvadur_backlinking.py "textový obsah"
```

**Vizualizácie:**
```
xvadur_obsidian/xvadur/scripts/xvadur_visualizations.py
```
**Použitie:**
```bash
cd xvadur_obsidian/xvadur/scripts
python3 xvadur_visualizations.py
```

Generuje:
- Progress bary (ASCII)
- Metriky dashboard (ASCII tabuľka)
- Timeline vizualizácie
- Knowledge graph (ASCII)
- Activity heatmap

---

## 📊 XP Systém

### Metriky

- **Introspektívna Hĺbka:** Word count × complexity score
- **Transformačný Insight:** Temporal references × sentiment score
- **Kreatívna Syntéza:** RAG queries × synthesis quality
- **Vulnerability Bonus:** Negatívne sentimenty = vyšší bonus
- **Pattern Recognition:** Recursive depth × pattern identification

### Bonusy (Kalibrované na Baseline 0)

- 100+ words = 0.5 XP (max 2.0 XP)
- 5+ prompts = 0.4 XP (max 1.0 XP)
- Complexity > 5/10 = 0.1 XP za každý bod nad 5 (max 1.0 XP)
- Temporal references = 0.3 XP za každý (max 1.5 XP)
- Recursive depth > 2 = 0.4 XP za každý level (max 2.0 XP)
- Negatívny sentiment = 1.0 XP (vulnerability bonus)
- RAG queries = 0.2 XP za každý (max 1.0 XP)

**Typická session:** 1.0 - 5.0 XP (nie stovky)

---

## 🔍 RAG Integrácia

RAG systém sa používa **na požiadanie**:

- Keď Adam odkazuje na minulosť
- Keď explicitne požiada o RAG query
- Pre syntézy na základe citácií

**Použitie:**
```python
query_rag_with_synthesis("čo som hovoril o inferiorite")
```

---

## 📝 Formát Logu

Každý záznam v `XVADUR_LOG.md` obsahuje:

```markdown
## [YYYY-MM-DD HH:MM] Téma/Reflexia

**Kontext:** [Čo viedlo k tejto reflexii]
**Hlavné myšlienky:** [Extrahované kľúčové body]
**Syntéza:** [Vysvetľujúca syntéza na základe citácií]
**Vzorce:** [Identifikované vzorce správania/myslenia/chcenia]

**Kvantitatívne metriky:**
- Word count: [počet]
- Prompt count: [počet]
- Complexity: [1-10]
- Temporal references: [počet]
- Recursive depth: [počet]
- Sentiment: [pozitívny/negatívny/neutrálny]

**XP získané:** [vypočítané XP]
**RAG queries:** [počet]
**Citácie:** [Linky na relevantné dokumenty]

**Knowledge Graph:**
- [[RelevantDocument1]] - [dôvod]
- [[RelevantDocument2]] - [dôvod]
```

---

## 🔗 Súvisiace Dokumenty

- [[CHECKPOINT_LATEST]] - Aktuálny checkpoint
- [[CHRONOLOGICAL_MAP_2025]] - Chronologická mapa
- [[xvadur_profile]] - Profil
- [[Recepcia]] - Projekt Recepčná

---

## 📚 Dokumentácia

- **System Prompt:** `.cursor/commands/xvadur.md` (originál) + `config/xvadur_command.md` (kópia)
- **Backlinking Script:** `scripts/xvadur_backlinking.py`
- **Vizualizácie Script:** `scripts/xvadur_visualizations.py`
- **XP Tracking:** `logs/XVADUR_XP.md`
- **Log:** `logs/XVADUR_LOG.md`
- **Štruktúra:** `STRUCTURE.md`

---

## 📁 Tree Root

Všetky súbory súvisiace s xvadur sú v jednom tree root:
```
xvadur_obsidian/xvadur/
```

Pozri `STRUCTURE.md` pre kompletný prehľad.

