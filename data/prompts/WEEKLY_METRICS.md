# 📊 Týždenné Metriky Promptov

**Vytvorené:** 2025-12-04  
**Skript:** `scripts/analyze_prompts_weekly_metrics.py`  
**Účel:** Kvantitatívne analýzy promptov podľa týždňov (ISO týždeň)

---

## 📈 Prehľad

**Celkom týždňov:** 18  
**Celkom promptov:** 737  
**Celkom slov:** 255,463  
**Celkom viet:** 12,108  

**Priemer:**
- 40.9 promptov za týždeň
- 14,192 slov za týždeň
- 672 viet za týždeň

---

## 📋 Týždenné Metriky

| Týždeň | Počet Promptov | Word Count | Priem. Words/Prompt | Počet Viet | Median Viet | Aktívnych Dní |
|--------|---------------|------------|---------------------|------------|-------------|---------------|
| W29 2025 (19-20.07) | 34 | 6,084 | 178.9 | 294 | 5.0 | 2 |
| W30 2025 (21-27.07) | 82 | 12,473 | 152.1 | 636 | 5.0 | 7 |
| W31 2025 (28.07-03.08) | 59 | 10,230 | 173.4 | 483 | 6 | 7 |
| W32 2025 (04-10.08) | 75 | 17,000 | 226.7 | 679 | 5 | 7 |
| W33 2025 (11-15.08) | 21 | 3,760 | 179.0 | 129 | 4 | 2 |
| W34 2025 (19-24.08) | 27 | 7,365 | 272.8 | 396 | 10 | 5 |
| W35 2025 (25-31.08) | 40 | 18,133 | 453.3 | 918 | 8.0 | 5 |
| W36 2025 (01-07.09) | 53 | 24,690 | 465.8 | 1,136 | 10 | 7 |
| W37 2025 (08-14.09) | 40 | 18,327 | 458.2 | 781 | 10.0 | 6 |
| W38 2025 (15-21.09) | 68 | 40,840 | 600.6 | 1,955 | 10.0 | 7 |
| W39 2025 (22-28.09) | 40 | 30,481 | 762.0 | 1,222 | 10.5 | 7 |
| W40 2025 (29.09-05.10) | 37 | 21,236 | 573.9 | 1,058 | 14 | 7 |
| W41 2025 (06-12.10) | 23 | 11,733 | 510.1 | 651 | 13 | 7 |
| W42 2025 (14-19.10) | 20 | 8,487 | 424.4 | 371 | 9.0 | 5 |
| W43 2025 (20-26.10) | 21 | 8,468 | 403.2 | 498 | 11 | 6 |
| W44 2025 (27.10-02.11) | 18 | 8,930 | 496.1 | 476 | 10.5 | 6 |
| W45 2025 (03-06.11) | 6 | 4,119 | 686.5 | 204 | 23.0 | 3 |
| W49 2025 (02-04.12) | 73 | 3,107 | 42.6 | 221 | 1 | 3 |

---

## 📊 Trendy

### Najvyššie hodnoty:
- **Najviac promptov:** W30 (82), W38 (68), W49 (73)
- **Najviac slov:** W38 (40,840), W39 (30,481), W36 (24,690)
- **Najvyšší priemer slov/prompt:** W39 (762.0), W45 (686.5), W38 (600.6)
- **Najviac viet:** W38 (1,955), W39 (1,222), W36 (1,136)
- **Najvyšší median viet:** W45 (23.0), W40 (14), W41 (13)

### Najnižšie hodnoty:
- **Najmenej promptov:** W45 (6), W44 (18), W42 (20)
- **Najmenej slov:** W45 (4,119), W33 (3,760), W49 (3,107)
- **Najnižší priemer slov/prompt:** W49 (42.6), W30 (152.1), W31 (173.4)
- **Najmenej viet:** W33 (129), W45 (204), W49 (221)
- **Najnižší median viet:** W49 (1), W33 (4), W32 (5)

### Vzorce:
- **W38 (15-21.09):** Peak týždeň - najviac promptov (68), najviac slov (40,840), najviac viet (1,955)
- **W39 (22-28.09):** Najvyšší priemer slov/prompt (762.0) - dlhšie, komplexnejšie prompty
- **W45 (03-06.11):** Najvyšší median viet (23.0) - veľmi dlhé prompty, ale málo ich (6)
- **W49 (02-04.12):** Veľa promptov (73), ale krátke (priemer 42.6 slov) - rýchle interakcie

---

## 💡 Pozorovania

1. **Týždenné cykly:**
   - W30-W32: Vysoká aktivita (82, 59, 75 promptov)
   - W33: Pokles (21 promptov) - možno pauza
   - W35-W40: Konzistentná aktivita (40-68 promptov)
   - W41-W45: Pokles aktivity (6-23 promptov)
   - W49: Návrat k vysokej aktivite (73 promptov)

2. **Dĺžka promptov:**
   - W39: Najdlhšie prompty (priemer 762 slov)
   - W49: Najkratšie prompty (priemer 42.6 slov)
   - Trend: Od W35 sa priemer zvyšuje (453 → 762), potom klesá

3. **Komplexnosť (median viet):**
   - W40-W41: Najkomplexnejšie prompty (median 14, 13 viet)
   - W45: Extrémne komplexné (median 23 viet), ale len 6 promptov
   - W49: Veľmi jednoduché prompty (median 1 veta)

---

## 🔄 Použitie

**Aktualizácia metrík:**
```bash
python3 scripts/analyze_prompts_weekly_metrics.py > data/prompts/WEEKLY_METRICS.md
```

**Porovnanie s mesiacmi:**
- Týždenné metriky poskytujú viac dátových bodov (18 vs 6 mesiacov)
- Lepšie zachytávajú týždenné cykly a trendy
- Užitočné pre identifikáciu vzorcov produktivity

---

**Posledná aktualizácia:** 2025-12-04
