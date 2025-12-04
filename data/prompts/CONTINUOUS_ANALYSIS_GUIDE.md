# 🔍 Kontinuálna Analýza: Founder's Audit Style

**Účel:** Automatizovaná analýza každého dňa v štýle "Founder's Audit" (ako v `xvadur/+/analyza.md`)

**Skript:** `scripts/analyze_day_founder_style.py`

---

## 🎯 Čo je Kontinuálna Analýza?

**Kontinuálna analýza** = Analýza Adama v čase, kde každý deň dostaneš:
- Founder's Audit perspektívu
- Kritický rozbor (nie len pozitívne)
- Identifikáciu vzorcov (Time Compression, Polymath, AI Native, atď.)
- Red Flags (kritické feedbacky)
- Záver s hodnotením

**Cieľ:** Namiesto 600-krát manuálne povedať "sprav analýzu tohto dňa", máš automatizovaný systém, ktorý to urobí za teba.

---

## 🚀 Rýchly Štart

### 1. Analýza Konkrétneho Dňa

```bash
python3 scripts/analyze_day_founder_style.py --date 2025-09-04
```

**Výstup:** `data/prompts/continuous_analysis/analysis_2025-09-04.md`

### 2. Analýza Všetkých Dní

```bash
python3 scripts/analyze_day_founder_style.py --all
```

**Výstup:** Jedna analýza pre každý deň v `data/prompts/continuous_analysis/`

### 3. Batch Mode (Resume Functionality)

```bash
python3 scripts/analyze_day_founder_style.py --all --batch
```

**Výhoda:** Preskočí už existujúce analýzy (môžeš pokračovať po prerušení)

### 4. Limitovaný Počet Dní (Test)

```bash
python3 scripts/analyze_day_founder_style.py --all --limit 10
```

**Výhoda:** Testuješ na prvých 10 dňoch pred spustením na všetko

---

## 📋 Štruktúra Analýzy

Každá analýza obsahuje:

### FOUNDER'S AUDIT: Adam Rudavský (Snapshot: YYYY-MM-DD)

**Verdikt:** [Krátke hodnotenie]

**Kritický rozbor:**

#### 1. [Identifikovaný Vzorec/Téma]
> *[Citácia z promptov]*

**Founderov pohľad:**
[Analýza z pohľadu foundera]

**Analýza:** [Hlbšia analýza vzorca]

#### 2. [Ďalší Vzorec/Téma]
...

### KRITICKÝ FEEDBACK (The "Red Flags")

[Red flags a kritické feedbacky]

### ZÁVER: Kto si?

[Záverečné hodnotenie a odporúčania]

---

## 🔧 Technické Detaily

### Vstupné Dáta

Skript používa:
- `prompts_enriched.jsonl` - metadáta (activity, sentiment, category)
- `prompts_split/` - originálne texty promptov
- `xvadur/data/prompts_log.jsonl` - aktuálne prompty
- `xvadur/data/profile/xvadur_profile.md` - profile context (voliteľné)

### Model & API

- **Model:** `tngtech/tng-r1t-chimera:free` (FREE cez OpenRouter)
- **API:** OpenRouter (nie OpenAI)
- **API Key:** `OPENROUTER_API_KEY` v `.env` súbore

**Nastavenie:**
1. Vytvor `.env` súbor v root adresári
2. Pridaj: `OPENROUTER_API_KEY=sk-or-v1-...`
3. Skript automaticky načíta API key z `.env`

### Rate Limiting

- 1.1s medzi requestmi (60 requests/min)
- Automatické retry pri chybách

### Resume Functionality

Ak skript spadne alebo ho prerušíš:
- `--batch` flag preskočí už existujúce analýzy
- Môžeš pokračovať bez obáv o duplikáty

---

## 📊 Odhadované Náklady

**Pre 600 dní:**
- Model: `tngtech/tng-r1t-chimera:free` (FREE!)
- Odhadované náklady: **$0** (FREE model)
- Čas: ~11-12 hodín (s rate limiting 1.1s)

**Pre 1 deň:**
- Náklady: **$0** (FREE)
- Čas: ~1 minúta

**Poznámka:** Model je FREE, takže náklady sú nulové! 🎉

---

## 💡 Príklady Použitia

### Test na Jednom Dni

```bash
# Test na konkrétnom dni
python3 scripts/analyze_day_founder_style.py --date 2025-09-04

# Skontroluj výstup
cat data/prompts/continuous_analysis/analysis_2025-09-04.md
```

### Batch Processing (Odporúčané)

```bash
# Spusti na všetkých dňoch s resume functionality
python3 scripts/analyze_day_founder_style.py --all --batch

# Môžeš prerušiť (Ctrl+C) a pokračovať neskôr
# Skript automaticky preskočí už existujúce analýzy
```

### Postupné Spracovanie

```bash
# Najprv test na 10 dňoch
python3 scripts/analyze_day_founder_style.py --all --limit 10 --batch

# Ak je to OK, spusti na všetkom
python3 scripts/analyze_day_founder_style.py --all --batch
```

---

## 📁 Výstupná Štruktúra

```
data/prompts/continuous_analysis/
├── analysis_2025-07-19.md
├── analysis_2025-07-20.md
├── analysis_2025-07-21.md
├── ...
└── analysis_2025-12-03.md
```

Každý súbor obsahuje kompletnú analýzu dňa v Founder's Audit štýle.

---

## 🔄 Workflow

1. **Extrahuj aktivity** → `prompts_activities.jsonl`
2. **NLP analýza** → `prompts_nlp4sk.jsonl`
3. **Kategorizácia** → `prompts_categorized.jsonl`
4. **Konsolidácia** → `prompts_enriched.jsonl`
5. **Kontinuálna analýza** → `continuous_analysis/analysis_*.md` ⭐ **TU SME**

---

## 🎯 Ďalšie Možnosti

### Syntéza Všetkých Analýz

Po vytvorení všetkých denných analýz môžeš vytvoriť syntézu:

```bash
# Vytvor syntézu všetkých analýz
python3 scripts/synthesize_continuous_analysis.py
```

**Výstup:** `continuous_analysis_synthesis.md` - chronologická syntéza všetkých analýz

### Temporálne Vzorce

Identifikácia vzorcov naprieč časom:
- Kedy sa objavujú red flags?
- Ako sa mení "Operating Clock Speed"?
- Kedy prichádza "The Dip"?

---

## 📝 Príklad Výstupu

```markdown
# FOUNDER'S AUDIT: Analýza Dňa 2025-09-04

### FOUNDER'S AUDIT: Adam Rudavský (Snapshot: 2025-09-04)

**Verdikt:** Pozerám sa na "High-Variance Individual" v momente zrýchlenia.

**Kritický rozbor:**

#### 1. Fenomén "Time Compression"
> *"1.7 odchadzam... 1.8 slub Teslovi... 22.8 svadba... 4.9 biznis call."*

**Founderov pohľad:**
Toto je nenormálne. A myslím to ako kompliment.
...

### KRITICKÝ FEEDBACK (The "Red Flags")

**1. Riziko "God Complex"**
...

### ZÁVER: Kto si?

**Si "Founder-in-Training" s extrémne vysokým stropom.**
...
```

---

## 🐛 Troubleshooting

### Chyba: "OPENROUTER_API_KEY nie je nastavený"
```bash
# Vytvor .env súbor v root adresári
echo "OPENROUTER_API_KEY=sk-or-v1-..." > .env

# Alebo nastav environment variable
export OPENROUTER_API_KEY='sk-or-v1-...'
```

### Chyba: "Rate limit exceeded"
- Skript automaticky čaká medzi requestmi (1.1s)
- Ak stále zlyhá, zvýš čas medzi requestmi v kóde
- OpenRouter FREE modely môžu mať rate limits

### Chyba: "Žiadne prompty pre dátum"
- Skontroluj, či dátum existuje v `prompts_enriched.jsonl`
- Skontroluj formát dátumu (YYYY-MM-DD)

### Chyba: "Model nie je dostupný"
- Skontroluj, či model `tngtech/tng-r1t-chimera:free` je dostupný na OpenRouter
- Môžeš zmeniť model v skripte (riadok 41)

---

## 💡 Tipy

1. **Začni s testom** - Najprv analyzuj 1-2 dni, skontroluj kvalitu
2. **Použi batch mode** - Vždy používaj `--batch` pre resume functionality
3. **Postupne** - Začni s `--limit 10`, potom rozšír
4. **FREE model** - Model je FREE, takže náklady sú nulové! 🎉

---

**Vytvorené:** 2025-12-04  
**Status:** ✅ Pripravené na použitie


