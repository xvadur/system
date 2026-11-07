# Výskum konkurenčných kliperov

**Spoločný priečinok všetkých nájdených lokálnych rozborov Fikiho kliperov.** Upratané 22. 10. 2026; pôvodné pozorovania sú z 26. 9. až 21. 10. 2026. Tento dátum upratania neznamená nové meranie výkonu ani nový obsahový rozbor videí.

## Kde začať

| Potrebujem | Otvoriť |
|---|---|
| Vedieť, čo sme sa naučili a čo vieme použiť pri výrobe | **[ZISTENIA.md](ZISTENIA.md)** — dramaturgia, výber pasáže, obrazové vložky, titulky, crop, animácia, CTA a limity metrík |
| Nájsť konkrétneho klipera a jeho rozbory | **[UCTY.md](UCTY.md)** — účty podľa hĺbky analýzy, platformy a užitočného postupu |
| Nájsť asset podľa situácie v reči | **[ASSETY.md](ASSETY.md)** — tematický vstup do konkrétnych príkladov a registra použití |
| Otvoriť pôvodný výskum z určitého dátumu | **[ZDROJE.md](ZDROJE.md)** — chronológia, rozsah, prekryvy a pôvod |
| Pozrieť zachované zdrojové video | **[VIDEA.md](VIDEA.md)** — lokálne videá, verejné odkazy a príslušná výskumná dávka |
| Pokračovať v najnovšom rozbore `@fikisulik_klipyy` | [Prehľad 10 videí + Vallo](zdroje/2026-10-21-fikisulik_klipyy/INDEX.md) · [115 použití assetov](zdroje/2026-10-21-fikisulik_klipyy/ASSETY.md) · [samostatný Vallo](zdroje/2026-10-21-fikisulik_klipyy/ROZBOR.md) |

## Čo je tu uložené

```text
research/konkurencia/
├── README.md          vstup do celého výskumu
├── ZISTENIA.md        spoločná syntéza s odkazmi na dôkazy
├── UCTY.md            prehľad účtov a vykonaných rozborov
├── ASSETY.md          obrazové postupy podľa významu a situácie
├── ZDROJE.md          dátované dávky a ich obmedzenia
├── VIDEA.md           index zachovaných videí
├── data/              strojovo čitateľný index videí
├── zdroje/            pôvodné rozbory, dáta, metadáta a najnovšie videá
├── metodika/          pôvodný návrh katalógu assetov
└── evidencia/         pôvod súborov, presun, odstránenie snímok a kontrola
```

Staršie texty a dáta sa zozbierali zo starého projektu `xvadur_workspace/projekty/klipy`. **252 zdrojových súborov** je prenesených bez zmeny obsahu vrátane 97 súborov video metadát. Najnovší výskum z 21. 10. sa presunul z pôvodného referenčného priečinka v tomto projekte. Dva výňatky zo starších odovzdávok zachovávajú tvoje korekcie zadania. Presný pôvod a kontrolné súčty sú v [evidencii presunu](evidencia/migration.json).

Historické rozbory sú ponechané ako dátované podklady. Nové prehľady vyššie ich prepájajú a upozorňujú na neúplné práce, neskoršie opravy a rozpory. Staré návrhy, príkazy a prevádzkové pokyny v zdrojoch sú historický materiál.

## Čo sme z toho získali

Spoločným použiteľným postupom je **vybrať ucelenú myšlienku a dať obrazu konkrétnu úlohu v konkrétnom mieste reči**. Portrét identifikuje človeka, porovnanie usporiada položky, filmový obraz rozvinie prirovnanie a návrat na hovoriaceho ponechá priestor reakcii. Podrobné príklady aj protiklady sú v [syntéze](ZISTENIA.md).

- **Počty dávok sa nesčítavajú na unikátne videá.** Výskumy opakovane používajú tie isté ID; tridsať IG rozborov je už zahrnutých v súhrne 39. Novší rozbor môže pridať nové poznatky o tom istom klipe.
- **115 záznamov znamená použitia v 11 referenčných videách**, vrátane titulkov, prechodov, CTA a vrstiev prevzatého zdroja. Nie je to knižnica 115 získaných čistých assetov.
- **Audio nemá overenie posluchom.** Názvy zvukov, merania signálu a pomocný ASR sa takto aj čítajú; konkrétnu hudbu, SFX a mix ešte treba posúdiť.
- **Výkon je historické pozorovanie.** Vyšší počet views sám nepotvrdzuje, že ho spôsobil konkrétny efekt, asset alebo dĺžka. Aktuálne metriky sa pri uprataní nezbierali.

## Snímky a zachované médiá

Na tvoje zadanie sa z výskumných priečinkov odstránilo **1 813 odvodených obrázkov a kontaktných hárkov, spolu približne 83,14 MiB**. Sú obnoviteľne presunuté do macOS Koša; zoznam pôvodných ciest a hashov je v [zázname čistenia](evidencia/screenshot-cleanup.json). Odkazy v najnovších rozboroch vedú na zachované video a približný čas.

Zachované sú všetky zdrojové MP4: 11 v najnovšej dávke a 97 starších mediálnych súborov na pôvodných miestach, na ktoré vedie [index videí](VIDEA.md). Sú to fyzické súbory, nie tvrdenie o 108 unikátnych alebo rovnako dôkladne rozobratých videách. Staršie videá sa nekopírovali druhýkrát.

Zostali aj oba získané čisté podklady — oficiálny erb Bratislavy a múzejná reprodukcia Sokratovej smrti — a dátové snímky metrík `snimky/*.json`. Produkčné médiá epizód zostali mimo čistenia.

Staré cesty `fiki/referencie/konkurencia/` majú kompatibilné relatívne odkazy do tohto priečinka. Existujúce importy a recepty tak môžu ďalej čítať rovnaké súbory. Podrobnosti sú v [evidencii](evidencia/README.md).

## Ako pridať ďalší účet

1. Vytvoriť novú dátovanú dávku v `zdroje/` a zapísať profil, čas zberu, pravidlo výberu a verejné ID videí.
2. Rozlišovať metriky, vybrané/stiahnuté médiá a dokončený obsahový rozbor. Existujúce ID prepojiť s predchádzajúcim výskumom.
3. Pri každom použití evidovať **čo → čas → spúšťaciu vetu alebo pojem → významovú funkciu → spracovanie → pôvod**. Ukážkou je [register z 21. 10.](zdroje/2026-10-21-fikisulik_klipyy/assety-register.json).
4. Aktualizovať `UCTY.md`, `ZISTENIA.md`, `ASSETY.md` a `ZDROJE.md` iba o skutočne vykonanú prácu. Čisté získané médiá odlíšiť od neoverených stôp.

Toto je výskumná knižnica. Výber pasáže, nové výrobné zadanie a tvoje tvorivé prijatie zostávajú samostatné kroky.
