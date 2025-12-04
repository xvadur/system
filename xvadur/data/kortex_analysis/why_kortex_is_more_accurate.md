# ✅ Prečo je Kortex Backup "Pravdivejší" Dataset?

**Vytvorené:** 2025-12-04  
**Účel:** Vysvetlenie, prečo Kortex backup je presnejší obraz tvojich konverzácií

---

## 📊 Kľúčové Zistenia

### Pokrytie Historických Promptov
- **Len 25.2%** textov z Kortex backupu je aj v historických promptoch
- **74.8%** promptov z Kortex backupu NIE JE v historických promptoch
- To znamená, že **3 zo 4 promptov** sa nedostali do historických promptov!

### Časové Pokrytie
- **Historické:** 96 dní
- **Kortex backup:** 126 dní
- **+30 dní** len v Kortex backupe (napr. 7.-10. november 2025)

---

## 🔍 Čo je v Kortex Backupe, Čo NIE JE v Historických?

### 1. **Všetky Konverzácie**
- Kortex backup = priamy export z databázy
- Historické prompty = len tie, ktoré sa dostali do kroniky
- **Výsledok:** 1,335 promptov naviac v Kortex backupe

### 2. **Krátke Prompty**
- **41.4%** promptov v Kortex backupe sú veľmi krátke (< 50 slov)
- Tieto sa často nedostali do kroniky (boli "príliš krátke")
- Ale sú dôležité - ukazujú tvoje rýchle otázky, follow-upy, kontext

### 3. **Nedávne Konverzácie**
- November 2025: 7.-10. november má 56 promptov v Kortex backupe
- Tieto ešte neboli v kronike
- **Kortex backup je aktuálnejší**

### 4. **Kompletný Kontext**
- Kortex backup obsahuje **všetky** konverzácie, nie len "významné"
- Historické prompty boli filtrované/manuálne vybrané
- **Kortex backup = nefiltrovaný obraz**

---

## 💡 Prečo je to "Pravdivejšie"?

### 1. **Kompletnosť**
- **Kortex backup:** 1,801 promptov = všetky konverzácie
- **Historické:** 664 promptov = len vybrané konverzácie
- **Rozdiel:** 1,137 promptov (171% viac!)

### 2. **Nefiltrované**
- Kortex backup = žiadne filtrovanie
- Historické = filtrované podľa `author_guess == "adam"`
- **Kortex backup obsahuje aj konverzácie, ktoré by boli vyfiltrované**

### 3. **Priamy Export**
- Kortex backup = priamo z databázy
- Historické = extrahované z markdown súborov (mohli byť upravené)
- **Kortex backup = originálne dáta**

### 4. **AI Odpovede**
- Kortex backup obsahuje **1,880 AI odpovedí**
- Historické prompty obsahujú **len user prompty**
- **Kortex backup = kompletný dialóg (user + AI)**

---

## 📈 Štatistiky Kortex Backup Promptov

### Rozdelenie podľa Dĺžky
- **Veľmi krátke (< 50 slov):** 746 (41.4%) - rýchle otázky, follow-upy
- **Krátke (50-200 slov):** 425 (23.6%) - štandardné otázky
- **Stredné (200-500 slov):** 267 (14.8%) - komplexnejšie otázky
- **Dlhé (500+ slov):** 363 (20.2%) - hlboké analýzy, kontext

### Obsah
- **S kódom:** 39 (2.2%) - technické prompty
- **S linkami:** 161 (8.9%) - odkazy na zdroje

### Priemerná Dĺžka
- **542.4 slov** na prompt
- **3,611 znakov** na prompt

---

## ✅ Záver

**Kortex backup JE "pravdivejší" dataset, pretože:**

1. ✅ **Kompletný** - obsahuje všetky konverzácie (nie len vybrané)
2. ✅ **Nefiltrovaný** - žiadne manuálne filtrovanie
3. ✅ **Priamy export** - originálne dáta z databázy
4. ✅ **Aktuálnejší** - obsahuje aj nedávne konverzácie
5. ✅ **S AI odpoveďami** - kompletný dialóg, nie len prompty

**Historické prompty sú:**
- ❌ Len 25% pokrytia
- ❌ Filtrované/manuálne vybrané
- ❌ Extrahované z markdown (mohli byť upravené)
- ❌ Bez AI odpovedí

---

## 📝 Odporúčanie

**Pre RAG/finetuning/analýzu používaj:**
- ✅ **Kortex backup** (`xvadur/data/kortex_guaranteed/`)
- ✅ Kompletný, nefiltrovaný, garantovaný bez duplikátov
- ✅ 1,822 konverzačných párov (user prompt + AI odpoveď)

**Historické prompty môžu slúžiť ako:**
- Referencia alebo backup
- Porovnanie s Kortex backupom
- Ale **NIE ako primárny dataset**

