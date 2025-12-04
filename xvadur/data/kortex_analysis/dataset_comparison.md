# 📊 Porovnanie Datasetov: Historické Prompty vs. Kortex Backup

**Vytvorené:** 2025-12-04  
**Účel:** Vysvetlenie rozdielu medzi historickými promptmi a Kortex backupom

---

## 📈 Čísla

### Historické Prompty (`data/prompts/prompts_split/`)
- **Celkom:** 664 promptov
- **Bez diakritiky:** 256 promptov (38.6%)
- **S diakritikou:** 408 promptov (61.4%)
- **Zdroj:** Extrahované z kroniky/chronology markdown súborov
- **Filtrovanie:** Podľa `author_guess == "adam"`

### Kortex Backup User Prompty
- **Celkom:** 1,801 promptov
- **Bez diakritiky:** 840 promptov (46.6%)
- **S diakritikou:** 961 promptov (53.4%)
- **Zdroj:** Kompletný backup z Kortex AI
- **Filtrovanie:** Žiadne (všetky user prompty)

---

## 🔍 Rozdiel

### Počet Promptov
- **Rozdiel:** 1,137 promptov naviac v Kortex backupe
- **Percentuálne:** 171% viac!

### Rozdelenie podľa Diakritiky
- **S diakritikou:** +553 promptov v Kortex backupe (961 vs 408)
- **Bez diakritiky:** +584 promptov v Kortex backupe (840 vs 256)

---

## 💡 Vysvetlenie

### Prečo je v Kortex backupe viac promptov?

1. **Kompletný backup:**
   - Kortex backup obsahuje VŠETKY konverzácie z Kortex AI
   - Historické prompty boli extrahované len z kroniky/chronology markdown súborov
   - Nie všetky konverzácie sa dostali do kroniky

2. **Rozdielne zdroje:**
   - Historické prompty: Extrahované z markdown súborov (`data/chronology/`)
   - Kortex backup: Priamy export z Kortex AI databázy

3. **Filtrovanie:**
   - Historické prompty: Filtrované podľa `author_guess == "adam"`
   - Kortex backup: Všetky user prompty (bez filtrovania)

4. **Časové pokrytie:**
   - Historické: 96 dní (2025-07-19 až 2025-11-06)
   - Kortex backup: 126 dní (širšie časové pokrytie)

---

## ✅ Záver

**Kortex backup obsahuje OMNOHO VIAC dát, pretože:**
- Je to kompletný backup všetkých konverzácií
- Nie všetky konverzácie sa dostali do historických promptov
- Obsahuje aj konverzácie, ktoré neboli v kronike

**To je DÓBRÁ VEC!** Máme teraz:
- Kompletný dataset zo všetkých konverzácií
- Všetky user prompty + AI odpovede
- 1,822 konverzačných párov pre finetuning/RAG

---

## 📝 Odporúčanie

**Pre RAG/finetuning použij:**
- ✅ Kortex backup dataset (`xvadur/data/kortex_guaranteed/`)
- ✅ Kompletný, bez duplikátov, garantovaný

**Historické prompty môžu slúžiť ako:**
- Referencia alebo backup
- Porovnanie s Kortex backupom

