# Rekapitulácia Session: Syntéza Promptov (2025-12-03)

## Cieľ Session

Vytvoriť chronologickú syntézu vývoja myslenia a konania z originálnych promptov pomocou LLM syntézy.

## Čo sa robilo

### 1. **Syntéza z Originálnych Promptov**
- **Skript:** `scripts/synthesize_from_raw_prompts.py`
- **Model:** `tngtech/deepseek-r1t2-chimera:free` (163k token kontext)
- **Vstup:** Originálne prompty z `prompts_split/` a `prompts_log.jsonl`
- **Výstup:** `synthesis_evolution_from_raw.md` (491 riadkov)
- **Status:** ✅ Úspešné, ale neúplné (niektoré fázy prázdne)

### 2. **Syntéza podľa Fáz**
- **Skript:** `scripts/synthesize_from_raw_prompts.py` (funkcia `synthesize_by_phases`)
- **Model:** `tngtech/deepseek-r1t2-chimera:free`
- **Vstup:** Originálne prompty rozdelené do 62 fáz podľa zmien v word_count
- **Výstup:** `synthesis_evolution_by_phases.md` (2562 riadkov)
- **Status:** ⚠️ Čiastočne úspešné
  - 62 fáz celkom
  - ~15-20 úspešných syntéz (24-32%)
  - ~21 prázdnych fáz (34%)
  - ~29 výskytov raw tagov (`<s>`, `[OUT]`, `[/INST]`)
  - 2 kritické chyby (Fáza 33: zacyklenie, Fáza 39: kontextové okno)

### 3. **Konverzia do PDF**
- **Vstup:** `synthesis_evolution_by_phases.md`
- **Výstup:** `synthesis_evolution_by_phases.html` → PDF (manuálne)
- **Problémy:** 
  - `<s>` tagy spôsobovali strikethrough v PDF
  - Opravené odstránením raw tagov
- **Status:** ✅ PDF vytvorené (pomerne úspešné)

## Výsledky

### Úspešné syntézy obsahujú:
- **Analýzu vývoja myslenia:** Témy, otázky, myslenkové vzory, zlomy
- **Analýzu vývoja konania:** Projekty, aktivity, rozhodnutia, produktivita
- **Vzťah myslenia a konania:** Ako sa navzájom ovplyvňovali
- **Temporálne vzorce:** Fázy, cykly, transformačné momenty

### Príklady kvalitných syntéz:
- **Fáza 7** (24.-26. júl): Objav Abacusu - podrobná analýza experimentovania
- **Fáza 24** (19.-21. august): Vytvorenie brandu Xvadur - finančná kríza a adaptácia
- **Fáza 57** (30. október - 2. november): Prekonanie prokrastinácie - kritická reflexia → akcia → úspech

## Problémy a Limity

### 1. **Model Limity**
- `tngtech/deepseek-r1t2-chimera:free` niekedy vracia raw tagy namiesto čistého textu
- Kontextové okno niekedy prekročené (Fáza 39: 35k tokenov, limit 32k)
- Model sa niekedy zacyklí (Fáza 33: stokrát `<s>` tagy)

### 2. **Kvalita Syntéz**
- ~34% fáz je prázdnych alebo neúplných
- Niektoré syntézy sú povrchné
- Raw tagy kazia čitateľnosť

### 3. **Proces**
- Syntéza podľa fáz je experimentálna
- Identifikácia fáz podľa word_count nie je ideálna
- Chýba robustný postup pre opakované použitie

## Čo sa naučilo

1. **Syntéza z originálnych promptov** je lepšia ako z extrahovaných aktivít
2. **Veľké kontextové okno** (163k tokenov) umožňuje syntetizovať dlhšie obdobia
3. **Syntéza podľa fáz** je užitočná, ale potrebuje lepšiu identifikáciu fáz
4. **PDF export** funguje, ale vyžaduje čistenie raw tagov

## Čo potrebuje ujasniť

1. **Čo od syntézy očakávať?**
   - Chronologický naratív?
   - Analýza vzorcov?
   - Identifikácia transformácií?
   - Kombinácia všetkého?

2. **Ako identifikovať fázy?**
   - Podľa word_count (súčasný prístup)?
   - Podľa zmien v témach?
   - Podľa transformačných momentov?
   - Kombinácia viacerých faktorov?

3. **Ako robiť syntézu robustnejšie?**
   - Lepšie prompty pre model?
   - Iný model?
   - Postupné syntézy (najprv krátke, potom dlhšie)?
   - Validácia a oprava chýb?

## Súbory Vytvorené

### Finálne výstupy (PONECHAT):
- `synthesis_evolution_by_phases.md` - Hlavný výstup (2562 riadkov)
- `synthesis_evolution_by_phases.html` - HTML verzia pre PDF
- `synthesis_evolution_from_raw.md` - Syntéza z originálnych promptov (491 riadkov)
- `README_SYNTHESIS.md` - Dokumentácia

### Dočasné/Experimentálne (ZMÁZAŤ):
- `synthesis_by_periods.md` - Staršia verzia syntézy
- `synthesis_by_periods_local.md` - Lokálna verzia
- `synthesis_story_arcs.md` - Staršia verzia
- `synthesis_story_arcs_local.md` - Lokálna verzia
- `synthesis_transformations.md` - Staršia verzia
- `synthesis_transformations_local.md` - Lokálna verzia

### Error Logy (ZMÁZAŤ):
- `data/prompts/categorization_errors.log`
- `data/prompts/extraction_errors.log`
- `data/prompts/nlp4sk_errors.log`

### Dokumentácia (PONECHAT):
- `data/prompts/EXTRACTION_GUIDE.md`
- `data/prompts/LOCAL_NLP_GUIDE.md`
- `data/prompts/NLP4SK_GUIDE.md`
- `data/prompts/README.md`

## Ďalšie Kroky

1. **Ujasniť očakávania:** Čo presne chceš z syntézy?
2. **Vylepšiť proces:** Robustnejší postup pre identifikáciu fáz
3. **Vyčistiť repo:** Zmazať dočasné súbory
4. **Dokumentovať:** Vytvoriť jasný návod pre budúce použitie

---

**Dátum:** 2025-12-03  
**Status:** Čiastočne úspešné - potrebuje ujasnenie očakávaní a vylepšenie procesu

