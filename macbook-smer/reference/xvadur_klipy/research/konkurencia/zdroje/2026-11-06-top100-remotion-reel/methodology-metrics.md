# Metrický inventár a výber 100 referencií

Vytvorené 2026-11-06T00:01:42.769729+00:00. Výskumný výber nad uloženými verejnými metrikami; pri tomto kroku neprebehol nový zber metrík, sťahovanie ani obsahová analýza.

## Zdroje a členstvo

- Najbohatší úplný TikTok inventár: [snapshot27.10.](../2026-10-27-riziko/tiktok-snapshot.json), 1 723 unikátnych postov zo 75 zisťovaných profilov, meraných 27. 10. 2026 približne 22:04–22:05 UTC. Všetky majú views, likes, comments, timestamp a trvanie; priame webpage_url chýbajú a verejný odkaz sa skladá z presného handle a native ID.
- Členstvo: presný handle → jeden historický autor a neprázdne historické hodnotenie v [analýze historickej identity](../2026-10-27-riziko/analysis.json), zároveň presne zhodný autor, `directoryMember=true` a `owned=false` v [adresári a účtovom súhrne24.10.](../2026-10-24-vyhodnotenie/account-summary.json). Označenia TOP/OK/MID/ZLE nie sú súčasný verdikt kvality; použili sa iba na doloženie identity v historickej skupine.
- Toto je historicky doložená nová skupina; zdroje výslovne neoverujú členstvo k dnešnému dňu. Vlastný účet a celý Instagram vrátane vonkajšej referencie fikisulik777 sú vylúčené.
- Prevádzková `workplace/data/workplace.sqlite` bola otvorená iba v SQLite `mode=ro`: 312 účtov, 2 470 publikácií a 3 885 meraní. Konkurenčné jednotlivé publikácie v nej sú iba 2 360 IG/FB Reels z 16. 10.; 24. 10. import pridal 304 účtových agregátov, nie nový video inventár. Konkurenčné DB metriky nemajú likes ani dátum publikácie, preto nie sú základom tohto shortlistu.

## Kvalifikácia a poradie

1. Použi iba presne priradených nevlastných členov vyššie.
2. K dátumu konkrétneho snapshotu musí byť post starý aspoň 7 × 24 hodín; budúce/novšie posty nevstupujú ani do baseline.
3. Autor potrebuje aspoň 10 zrelých postov so známymi views. Medián aj Q3 sa počítajú z tejto istej vzorky; Q3 používa nearest-rank `ceil(0.75*n)-1`.
4. Kandidát je striktne nad mediánom a zároveň má aspoň dvojnásobok mediánu a aspoň Q3 autora. Nula a neznáma hodnota sa nezamieňajú.
5. Poradie: násobok vlastného mediánu zostupne; iba pri presnej zhode násobku má prednosť existujúce lokálne MP4, potom views a native ID. Vybraných je prvých100 bez kvóty na autora. Neznižuje sa výkonnostný prah kvôli dostupnosti.
6. `selected100` obsahuje plných 100 vybraných záznamov a `top100Ids` ich ID; všetkých258 silných kandidátov, baseline a celý kompaktný inventár obsahuje `candidates.json`. Žiadna mediánová či spodná kontrola nevyplňuje stovku.

## Výsledok

| Položka | Počet |
| --- | ---: |
| `snapshotAccounts` | 75 |
| `snapshotPosts` | 1723 |
| `snapshotUniqueNativeIds` | 1723 |
| `exactHistoricallyMappedMemberAccounts` | 62 |
| `baselineEligibleAccounts` | 57 |
| `baselineMaturePosts` | 1284 |
| `aboveMedian` | 630 |
| `atLeast2xMedian` | 285 |
| `atOrAboveAuthorQ3AndAboveMedian` | 360 |
| `strongCandidates` | 258 |
| `strongCandidateAccounts` | 55 |
| `strongWithLocalMp4` | 63 |
| `strongWithRawAsr` | 40 |
| `strongWithContactSheets` | 40 |
| `selected` | 100 |
| `selectedAccounts` | 36 |
| `selectedWithLocalMp4` | 45 |
| `selectedWithRawAsr` | 32 |
| `selectedWithContactSheets` | 32 |

## Rozloženie podľa autora

| TikTok | Baseline ≥7d | Medián views | Q3 | Nad mediánom | Silní kandidáti | V TOP100 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| @fiki.sulik58 | 92 | 823.5 | 1854 | 46 | 24 | 9 |
| @fikimentalita | 69 | 1804 | 9503 | 34 | 18 | 13 |
| @fikisulik_klipyy | 44 | 2207.5 | 7418 | 22 | 12 | 5 |
| @best.of.fiki | 37 | 959 | 2692 | 18 | 10 | 6 |
| @fiki_cliparts | 38 | 849.5 | 1801 | 19 | 10 | 4 |
| @_fiki_clips_ | 34 | 683 | 1367 | 17 | 9 | 1 |
| @maestrofiki | 31 | 785 | 3839 | 15 | 8 | 4 |
| @fikiclips1 | 31 | 2877 | 5442 | 15 | 7 | 2 |
| @svet.filipa.sulika | 55 | 859 | 1100 | 27 | 7 | 1 |
| @fikiclips8 | 24 | 657.5 | 1326 | 12 | 7 | 0 |
| @fiki.kliky | 21 | 1108 | 7239 | 10 | 6 | 5 |
| @fikiframe | 22 | 1808 | 9271 | 11 | 6 | 4 |
| @fiki_momentss | 20 | 1092.5 | 2306 | 10 | 6 | 3 |
| @basedfiky | 24 | 964.5 | 1889 | 12 | 6 | 2 |
| @fiki.sulik.raw | 28 | 925 | 1449 | 14 | 6 | 2 |
| @fiki.extra | 17 | 5590 | 21500 | 8 | 5 | 2 |
| @fikithegoat_ | 24 | 866 | 1675 | 12 | 5 | 1 |
| @_fiki.unchained_ | 22 | 1137.5 | 1899 | 11 | 5 | 2 |
| @fiki.nahrad | 17 | 962 | 5657 | 8 | 5 | 4 |
| @fikisulik_bestof | 16 | 377 | 838 | 8 | 5 | 2 |
| @fiki.clips.27 | 17 | 378 | 1275 | 8 | 5 | 1 |
| @fikiprezident | 18 | 1356 | 2420 | 9 | 4 | 4 |
| @fikirealtalk | 13 | 2428 | 10600 | 6 | 4 | 3 |
| @fiki_daily1 | 16 | 645 | 959 | 8 | 4 | 2 |
| @frajer.fiki | 22 | 1306.5 | 2144 | 11 | 4 | 2 |
| @fiki.sulikclips3 | 20 | 980 | 1128 | 10 | 4 | 2 |
| @fiki.clipz | 13 | 1205 | 5744 | 6 | 4 | 1 |
| @fikiclipss8 | 12 | 946.5 | 3042 | 6 | 4 | 2 |
| @fiki.goat11 | 17 | 819 | 1274 | 8 | 4 | 1 |
| @fiki.highlights | 23 | 782 | 1048 | 11 | 4 | 0 |
| @fiki.clips45 | 22 | 1126 | 1775 | 11 | 4 | 0 |
| @fikinko.shorts | 12 | 13401.5 | 19800 | 6 | 3 | 0 |
| @fiki.sama | 13 | 1541 | 2592 | 6 | 3 | 1 |
| @fiki.bossik | 14 | 1032.5 | 1755 | 7 | 3 | 2 |
| @fiki.king1 | 32 | 930 | 1033 | 15 | 3 | 1 |
| @fiki.cl1pss | 20 | 822.5 | 882 | 10 | 3 | 0 |
| @fikisulik4 | 17 | 417 | 582 | 8 | 3 | 0 |
| @fiki.kazdyden | 11 | 466 | 1107 | 5 | 3 | 0 |
| @fikiclipz | 24 | 836.5 | 1052 | 12 | 2 | 1 |
| @fikiclips10 | 22 | 1148 | 1401 | 11 | 2 | 1 |
| @senseifiki | 10 | 756.5 | 929 | 5 | 2 | 1 |
| @fiki.hlasky | 10 | 4391 | 8385 | 5 | 2 | 0 |
| @fikinoklipy | 26 | 841.5 | 926 | 13 | 2 | 0 |
| @fiki.unrealized | 10 | 525.5 | 983 | 5 | 2 | 2 |
| @fiki.rawclipz | 15 | 971 | 1682 | 7 | 2 | 0 |
| @fiki.goat.one | 16 | 758.5 | 857 | 8 | 2 | 0 |
| @unchained.clips1 | 18 | 798 | 1141 | 9 | 1 | 1 |
| @fikisulikthegoatt | 14 | 924 | 955 | 7 | 1 | 0 |
| @fiki_shorts3 | 16 | 485.5 | 780 | 8 | 1 | 0 |
| @absolute_fiki | 14 | 708 | 913 | 7 | 1 | 0 |
| @fikitherealone | 16 | 842.5 | 874 | 8 | 1 | 0 |
| @fikiunstricted | 19 | 441 | 533 | 9 | 1 | 0 |
| @_fiki_goat | 13 | 408 | 681 | 6 | 1 | 0 |
| @fikidabest | 14 | 321 | 407 | 7 | 1 | 0 |
| @fikichamp | 17 | 99 | 112 | 8 | 1 | 0 |
| @fiki._clips | 21 | 586 | 827 | 10 | 0 | 0 |
| @fiki.shorts2 | 11 | 752 | 1270 | 5 | 0 | 0 |

## Médiá, ASR, kontaktné hárky a deduplikácia

- Lokálne mapovanie spája `research/konkurencia/data/videa.json` (108 fyzických súborov, dnes existujú všetky) a `../2026-10-27-nocny-research/acquisition.json` (120 fyzických záznamov, dnes existujú všetky). Ich zjednotenie má 206 unikátnych ID naprieč platformami; dostupnosť sa pri shortlistu posudzuje na konkrétnom TikTok ID.
- `rawAsr` a `contactSheets` odkazujú iba na dnes existujúce súbory. ASR nie je potvrdený posluch ani spoľahlivý prepis každého výroku; prenesené príznaky známych významových chýb zostali zachované. Hárky sú revízia r2 so zdrojovým PTS.
- `priorReport` dokladá starší rozbor; nový rozbor podľa remotion-reel ostáva nevykonaný. Starý `vyber-100.json` úmyselne obsahoval aj mediánové a Q1 kontroly, preto jeho stovka nie je premenovaná na výkonnostnú stovku.
- Kľúč publikácie je `(platform, native ID)`; viac dátovaných pozorovaní toho istého ID nie sú ďalšie klipy. Naprieč platformami sa identické editované video zlúči až podľa rovnakých bajtov alebo overenej audiovizuálnej zhody; podobný názov, účet či rovnaká zdrojová pasáž nestačia. Views naprieč platformami sa nesčítajú na unikátny dosah.

## Praktické limity

- Sedemdňová hranica odstráni čerstvé videá, ale nevyrovná vek všetkých videí; násobok mediánu je nadvýkon v historickom pozorovanom inventári, nie výsledok za rovnakých prvých sedem dní.
- Výber podľa views nedokazuje príčinu výkonu, retenciu ani kvalitu editu. Tie sa skúmajú na konkrétnom videu.
- Metriky sú z 27. 10., nie z 6. 11.; čerstvý zber by bol novou dátovanou vrstvou.

Podklad historického hodnotenia: [dátovaný presný výpis skupinovej tabuľky](../2026-10-27-riziko/rating-live.json). Nevydáva sa za nové hodnotenie ani čerstvo overené členstvo.

## Doložená náhrada nedostupnej obrazovej referencie

Po získavaní médií sa ukázalo, že TikTok `7695801657711480086` (@fiki.sulik.raw, pôvodný metrický rank12) poskytol cez použitý zber iba MP3 s jediným audio-only formátom (`vcodec=none`); [presný metadátový doklad](media/tiktok/7695801657711480086/source.info.json) neobsahuje videoformát. Stav je `unavailable_visual`, bez tvrdenia o zmazaní alebo type pôvodného príspevku.

Slot12 výskumnej stovky aj batch-0 preto nahrádza najvyššia kvalifikovaná rezerva `7692825927243287830` (@senseifiki), pôvodný metrický rank101. `candidateRank` zostal pôvodný; `selectedRank` označuje stabilný slotassignmentu. Ostatné dávky sa nemenili. Obidva záznamy a dôvod náhrady zostávajú v `candidates.json` pod `selectionSubstitutions`; nejde o zníženie výkonnostnej kvalifikácie.


## Finálne metrické overenie po získaní médií (6. 11. 2026)

Tento dodatok opisuje finálny výber a lokálnu dostupnosť. Pôvodná tabuľka dostupnosti vyššie (`selectedWithLocalMp4=45`, `selectedWithRawAsr=32`, `selectedWithContactSheets=32`) je **stav pri vytvorení shortlistu pred touto akvizíciou**. Rovnako pôvodná poznámka o ešte nevykonanej novej analýze patrí k tomuto skoršiemu kroku. Nové metriky výkonu sa nezbierali.

Základné metriky všetkých 100 finálnych klipov boli znova porovnané s raw snapshotom z 27. 10. Medián a Q3 boli prepočítané z rovnakých zrelých postov, bez používania novších views. Všetkých 100 má presné historické členstvo, vek aspoň 7 dní, baseline aspoň 10 postov, striktne nadmediánový výkon, aspoň 2× medián a aspoň Q3 autora; všetkých 258 silných kandidátov sa reprodukovalo bez rozdielu.

Finálna stovka zahŕňa **36 TikTok účtov / 36 presne priradených historických autorov**. Views: minimum **5,016**, medián **25,750**, maximum **175,200**. Násobok vlastného mediánu: minimum **8.6913×**, medián **16.6939×**, maximum **175.2540×**. Ide o historický nadvýkon, nie dôkaz príčiny ani aktuálny dosah.

Doložená náhrada uvedená vyššie zostáva jedinou zmenou: audio-only `7695801657711480086` (pôvodný rank 12) nahradil `7692825927243287830` (pôvodný rank 101) v rovnakom slote. Každý si ponecháva `candidateRank`; náhradník spĺňa rovnakú kvalifikáciu. Finálna množina presne zodpovedá pôvodným prvým 100 mínus vylúčený záznam plus táto rezerva.

Po akvizícii existuje **100/100 médií s obrazovou stopou, 100/100 raw ASR a 100/100 sád hustých kontaktných hárkov**. Akvizícia uvádza 45 prevzatých lokálnych súborov a 55 stiahnutých; starý počet 45 preto neznamená 55 stále chýbajúcich médií. Lokálne médiá majú podľa evidence spolu **6004.729727 s = 100.079 min**. Počet existujúcich JSON/MD kariet v okamihu overenia je 100/100; prítomnosť súboru sama neznamená súvislé prehratie či posluch.

Presné výpočty, rozloženie po účtoch, kontrola každého ID a cesty k lokálnym dôkazom sú v [metrics-final.json](metrics-final.json). Všetky karty používajú samostatne doložený rozsah obsahového rozboru; tento dodatok z nich nerobí audio analýzu.
