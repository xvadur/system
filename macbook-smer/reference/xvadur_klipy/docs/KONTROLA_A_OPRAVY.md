# Kontrola a opravy v Codexe

Implementované rozhranie P5. Codex pripraví skutočné podklady, vykoná osobitný kritický priechod, uloží nálezy a opraví plán. Adam nemusí ručne prepájať JSON. Príkazy nižšie sú nástroje Codexu; prijatie videa stále vyžaduje Adamov verdikt ku konkrétnemu súboru.

## Podklady kritiky

Po `materialy`, celom `nahlad` a `kontrola --bez-vision`:

```sh
python3 system/cli/klipy.py kritika --epizoda EPIZODA --klip KLIP --akcia priprav
```

Výsledok obsahuje cestu k nemennému `packet.json`. Balík viaže aktuálny plán, Timeline, materiály, pôvodné zdroje a hash celého MP4. Pridáva brief, prepis, Adamovo tvorivé zadanie, plány ostatných klipov epizódy a skutočné snímky dekódované z MP4 pri nábehoch, zmenách a návratoch. Opakované vytvorenie rovnakého balíka overí bajty a použije uložený výsledok. Starý master neprebije nový aktuálny draft.

Voliteľné `--volby volby.json` môže určiť napríklad `{"frames":[0,29,30,31,59],"eventIds":["reakcia"]}`. Čísla sú absolútne snímky celej Timeline, nie čas krátkeho preview. Pri explicitnom `frames` sa použije tento zoznam; `eventIds` filtruje automatický výber. Jeden balík má najviac 120 snímok. Viac balíkov toho istého kandidáta sa počíta ako jedno tvorivé kolo.

Kritik musí skutočne pozrieť citované snímky. Posúdi význam, nábeh reakcie, odhalenie pri slove, opakovanie materiálov, kolízie a čitateľnosť. Povinný `enrichmentReview` posúdi zvuk, reakcie, B-roll, vlastný obraz, nevyužité príležitosti a odlišnosť od dodaných kolegov dávky. Adam požaduje bohaté, individuálne spracovanie. Samotný počet efektov jeho latku nepotvrdzuje.

## Presný nález a oprava

Kritický výstup používa `CritiqueSubmissionSchema` v `system/schemas/critique.ts`. Každý nález obsahuje ID, typ, závažnosť, konkrétnu chybu, žiadanú zmenu, očakávanú skúšku a pozorované snímky. Event potrebuje `eventId`, slovo `wordId`, materiál `elementId` rovný request ID. Nie je dovolené odkázať na snímku, ktorú kritik neuviedol medzi prezretými.

```sh
python3 system/cli/klipy.py kritika --epizoda EPIZODA --klip KLIP --akcia prijmi --packet /absolutna/cesta/packet.json --data kritika.json
python3 system/cli/klipy.py uprav --epizoda EPIZODA --klip KLIP --zmeny opravy.json
```

`opravy.json` je pole `{ "feedbackId": "ID_Z_RECEIPTU", "patch": { ... } }`. Viac nálezov pôvodnej revízie sa opraví spolu do jednej novej revízie. Všetky patch objekty sa validujú pred zápisom; neplatný neskorší patch neuloží skoršiu čiastočnú zmenu. Príklad opravy eventu je `{"params":{"box":{"x":260,"y":1210,"width":560,"height":376}}}`. Úprava registrovanej scény môže zmeniť `authored`, vrátane fázových kotiev, iba s platným manifestom, slotmi a parametrami.

Kritik nemôže zmeniť uzamknutý event, jeho materiál, uzamknuté rámovanie alebo zvuk. Nemôže si ani vytvoriť nové ľudské uzamknutie. Zmenu takého rozhodnutia musí podložiť explicitná Adamova pripomienka. Reč a oprava textu majú osobitné existujúce operácie; nenahrádzajú sa obrazovým patchom. Originály a predchádzajúce revízie zostávajú nemenné.

## Overenie nových bajtov

Po zmene znovu vykonať materiály, krátky náhľad s okolím, celý nový draft a technickú kontrolu. Pripraviť nový kritický balík a prezrieť opravený moment aj okolité snímky. Do `RepairObservationSchema` sa zapíše ID nálezu, hash nového balíka, pozorovateľ, verdict, skutočne prezreté snímky a konkrétna poznámka.

```sh
python3 system/cli/klipy.py kritika --epizoda EPIZODA --klip KLIP --akcia over-opravu --packet /absolutna/cesta/novy-packet.json --data pozorovanie.json
python3 system/cli/klipy.py kontrola --epizoda EPIZODA --klip KLIP --pripomienka FEEDBACK_ID --poznamka "Konkrétny výsledok pozorovania novej verzie."
```

Textové tvrdenie o oprave nestačí. Kritický nález sa uzavrie až s pozorovaním aktuálneho plánu/mastera/Timeline a úspešnou technickou kontrolou celého súboru. Pozorovanie eventu musí zahŕňať moment aj jeho okolie. Opakovaný príjem rovnakého pozorovania nevytvorí ďalší záznam.

Najviac dve rozdielne verzie kandidáta môžu dostať interné tvorivé kritické kolo. Tretie nové kolo sa zastaví s konkrétnym problémom na predloženie Adamovi. Rozdelenie snímok jednej verzie do viacerých balíkov tento limit nespotrebúva ani neobchádza.

## Hranice dôkazov a prijatie

Technické dekódovanie a meranie zvuku, pozorovanie snímok, súvislý pohyb a posluch sú oddelené. Časovaná séria snímok môže overiť zobrazenie pred slovom/po slove; nepreukazuje celkový rytmus. Zvuková metrika nie je posluch.

Aktuálny režim kritického balíka uvádza `continuousMotion: not_checked` a `listening: not_listened`. Bez osobitne overenej schopnosti vnímať celé video/zvuk ich uzavrie Adam pri prehratí celého finálneho mastera. Samotné spustenie prehrávača nie je AI percepčný dôkaz. Nové prijatia s protokolom `p5.v1` vyžadujú aj úplné pohybové pokrytie; časované snímky ho nenahradia. Staršie uložené prijatia zostávajú čitateľné podľa ich pôvodného kontraktu.

Kritika ani overenie piatich technických opráv samo neprijíma klip alebo nový štýl. Pred exportom sa znovu overujú presné bajty a aktuálne vstupy. Praktické dôkazy a ich hranice obsahuje [report P5](OVERENIE_P5_2026-10-26.md).
