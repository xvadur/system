# Používanie lokálneho systému

Jediný vstup je `python3 system/cli/klipy.py`. Príkaz bez argumentov vypíše dostupné operácie. Všetky príkazy sa spúšťajú z `..`; samotný dispatcher tento pracovný priečinok nastaví aj pri spustení absolútnou cestou.

Od P6 používa Codex nad vybranou dávkou `cyklus --epizoda ID --akcia stav|priprav|pokracuj`. Výrobu, obnovu, pracovisko a konkrétne vetvy vedie [výrobný postup v Codexe](CODEX_VYROBNY_POSTUP.md). Detailné operácie nižšie zostávajú nástroje tohto postupu.

Funkcie M0–M8 sú implementované. [Živý syntetický E2E fixture](../system/tests/output/live-e2e/finished.json) má dva skontrolované mastery a lokálny export; všetky jeho prijatia sú testovacie a ostávajú `not_listened`. Rozsah vykonaných kontrol a ďalších behov vynechaných na Adamov pokyn je v [overovacom reporte](OVERENIE_M0_M8_2026-10-17.md). Tento návod neoznačuje #105 za spracovanú ani prijatú.

Systém teraz používa existujúce prihlásenie Codex CLI. `system/runtime.json` určuje provider, timeout, samostatný ASR model, výstup a súbežnosť. Claude adaptér ostáva podporovaný; overovací beh Claude vrátil organizačnú chybu 403. Prihlásenie ani účty sa kvôli tomu nemenili. Konkrétny názov modelu sa nevymýšľa, ak ho CLI vo výsledku neoznámi.

## Príprava a kontrola

```sh
python3 system/bootstrap.py --check
python3 system/cli/klipy.py doctor --hash-model --test-mlx --test-model
```

Pri čistej inštalácii `python3 system/bootstrap.py` vytvorí samostatný runtime z vlastných lockfiles. Python lock cieli na Python 3.14 a lokálny MLX runtime na Mac s Apple Silicon; Remotion je presne 4.0.529. Modelové váhy treba poskytnúť podľa `system/models/manifest.json`; `python3 system/bootstrap.py --download-model` získa presnú revíziu a overí jej hash. Runtime nevytvára prepojenie na starý projekt.

Lokálne spustenie MLX a Chromium vyžaduje prístup k Metal a lokálnemu renderovaciemu serveru. Renderer používa nainštalovaný Chrome/Chromium; jeho cestu možno zadať cez `CHROME_PATH`, prehliadač automaticky nesťahuje. Obmedzený sandbox môže tieto schopnosti odmietnuť; `doctor` uvádza skutočnú chybu. `--hash-model` kontroluje bajty modelu, `--test-mlx` vykoná skutočný import a `--test-model` nové textové modelové volanie. Oznámené prihlásenie samotné nepreukazuje fungujúce API; doctor uvádza nakonfigurovaný provider a samostatné uložené text/vision/research dôkazy.

## Epizóda a Adamov výber

```sh
python3 system/cli/klipy.py import --epizoda TEST --zdroj /absolutna/cesta/video.mp4 --nazov "Pracovná epizóda" --ciel-klipov 3 --min-ms 30000 --max-ms 90000
python3 system/cli/klipy.py zdroj-pravidla --epizoda TEST --metadata /absolutna/cesta/zdroj-pravidla.json
python3 system/cli/klipy.py prepis --epizoda TEST
python3 system/cli/klipy.py analyzuj --epizoda TEST
python3 system/cli/klipy.py stav --epizoda TEST --report
python3 system/cli/klipy.py vyber --epizoda TEST --klip prvy --kandidat candidate-ID
```

Od P3 sa k aktuálnemu zdroju ukladá aj jeho doložený pôvod. Súbor `zdroj-pravidla.json` má napríklad tvar:

```json
{
  "sourceNames": ["Skutočný názov programu"],
  "access": "public",
  "evidence": "Konkrétny zdroj, z ktorého je pôvod a režim overený."
}
```

Toto je formát, nie tvrdenie o konkrétnej epizóde. `access` môže byť `public`, `paid` alebo `unknown`. Pri platenom zdroji historické pravidlo uvádza 180 sekúnd, ale neurčuje rozsah limitu. Doložené spresnenie sa ukladá ako `paidLimitScope: "clip"` alebo `"batch"`; bez neho zostáva kontrola otvorená. Pri `batch` sa pri dávke/exporte počíta únia všetkých vybratých úsekov aktuálnej dávky. Predchádzajúce externé publikácie nie sú súčasťou tohto počítadla. Nový import s inými bajtmi zneplatní väzbu na staré metadáta.

Kandidáti dostávajú kontrolu presných zákazov zdrojov, video ID, tém a doložených aliasov. Kontrola sa opakuje pri Selection a exporte. Samotné krstné meno znamená neistotu; filmová cena Oscar sa automaticky nemení na Oskara Baramiho. Deterministická kontrola nenahrádza redakčné posúdenie významu, irónie a vzťahov.

Zdroj môže byť aj podporovaná verejná HTTPS URL. Import uloží nezávislú lokálnu kópiu a jej hash. Prepis obsahuje segmenty, slová a pôvodný ASR text. Technický obrazový index má časované snímky; modelový priechod ich skutočne číta. Analýza pracuje po blokoch s kontextovým prekrytím a kontrolou pokrytia. Kandidát obsahuje pointu, kontext, hranice a konkrétne tvorivé momenty. Analýza môže oznámiť nedostatok vhodných kandidátov.

`--nazov`, `--ciel-klipov`, `--min-ms` a `--max-ms` ukladajú názov a Episode.target (`clipCount`, `minDurationMs`, `maxDurationMs`). Čísla v ukážke sú iba príklad, nie zadanie #105. Cieľové hodnoty vstupujú do analýzy a prehľadu; nezaručujú, že epizóda obsahuje toľko vhodných samostatných pasáží. Pri zmene cieľa možno zopakovať import rovnakého zdroja s novými hodnotami: hotový zdroj sa použije znova a metadáta dostanú vlastnú revíziu. CTA sa určuje v klientskom zadaní a CreativeBrief; historické outro pravidlo ju samo nepotvrdzuje.

`vyber` zaznamená Adamovo rozhodnutie. Viaceré ID oddelené čiarkou zachovajú zadané poradie v jednom klipe. Presné hranice možno zadať cez `--od-ms` a `--do-ms`; opakované alebo viaceré úseky cez `--intervaly cesta.json`, napríklad:

```json
[
  {"id":"uvod","startMs":1000,"endMs":5000},
  {"id":"pointa","startMs":12000,"endMs":18000}
]
```

Časy sú milisekundy v pôvodnom zdroji. Hranica nesmie preseknúť slovo. Každý výskyt úseku má vlastné ID. Obrazový plán nemôže tieto rečové intervaly zmeniť.

## Storyboard, materiály a výroba

```sh
python3 system/cli/klipy.py navrhni --epizoda TEST --klip prvy
python3 system/cli/klipy.py materialy --epizoda TEST --klip prvy
python3 system/cli/klipy.py nahlad --epizoda TEST --klip prvy
python3 system/cli/klipy.py kontrola --epizoda TEST --klip prvy
python3 system/cli/klipy.py stav --epizoda TEST --report
```

Voliteľný `--brief cesta.json` odovzdá kanonický CreativeBrief vrátane uzamknutých požiadaviek. Planner dostane skutočný LibraryContext s hashmi médií, pozorovaním, obmedzeniami, históriou použitia a receptmi. Vypracuje konkrétne obrazy, materiály, slová a fázy. `EditPlan.editorial` obsahuje oblúk klipu, kontrolu kontextu a rozhodnutie použiť/nepoužiť/otvorené pre všetkých 11 editačných osí pri každom výskyte významového momentu. Chýbajúca os, reč bez rozboru alebo povinná otvorená potreba zablokujú výrobu; lokálny kandidát ešte nie je schválený materiál. Čitateľný plán vzniká v `klipy/ID/planovanie/`, dávkový prehľad v `davky/`. Každý významový moment má udalosť, odôvodnený čistý A-roll alebo otvorený problém. Vlastná grafika má úplnú deklaratívnu SceneSpec; samotný prompt nepredstavuje hotový materiál.

Aktuálny plán sa znovu používa iba pre zodpovedajúci výber a plánovací kontext. Nový explicitný brief, zmenené pravidlá, analýza alebo konfigurácia modelu vyvolajú nový návrh. Rozhodovací záznam P3 je pripnutý aj na hash významovej analýzy. Po oprave slova treba obnoviť rozbor a rozhodovací priechod pred ďalšou výrobou; záznam opravy a pôvodné revízie zostávajú zachované. Ručne uzamknuté udalosti, framing, audio a materiálové požiadavky zostávajú chránené; výmena fotografie alebo oprava grafiky nespustí nový prepis epizódy.

Pred novým plánom systém zahustí obrazové snímky vo vybraných zdrojových intervaloch, predvolene po jednej sekunde. Zachová kontext celého obrazového indexu a už overené snímky, doplní iba chýbajúce a vision dostane iba nové alebo neoverené vybrané snímky. Spoločná epizóda sa kvôli každému klipu znovu neprepisuje ani celá neskenuje na zmeny záberu. Výsledok je oddelený v klipových artefaktoch `observation-selected` a `observation-selected-technical`, takže klipy si nevytláčajú anotácie.

Resolver najprv skúsi knižnicu, potom dostupné vyhľadávanie alebo import. Výsledok uchová kandidátov, dôvod výberu, pôvod, licenciu, obsahovú kontrolu a skutočný súbor. Presný archív nenahradí prvým všeobecným stockom. Povinný nevyriešený materiál zablokuje kompiláciu a uvedie dôvod. `--volby cesta.json` umožňuje explicitný výber kandidáta alebo doloženú kontrolu lokálneho materiálu podľa rozhrania ResolveAssetsOptions.

Kompozícia má oddelený hlas a obraz. Prestrih, meme ani grafika neposúva reč; zvuk vloženého videa je štandardne stlmený. Titulky vychádzajú z časovaných slov. Tail má explicitné trvanie a nepredlžuje pôvodný hlas. Predvolený master je 1080 × 1920, 30 fps, H.264/AAC.

Od P3 `davka` **iba pripraví** všetky už vybraté klipy, uloží jednotlivé plány, prehľad a spoločné potreby. Samostatná výroba vyžaduje presný hash tejto prípravy:

```sh
python3 system/cli/klipy.py davka --epizoda TEST --klipy prvy,druhy
python3 system/cli/klipy.py vyrob-davku --epizoda TEST --priprava HASH_Z_VYSLEDKU --kvalita draft
```

`davka --ulozene-plany` overí už uložené plány bez nového modelového návrhu. Žiadny z prípravných režimov nespúšťa získavanie médií ani render. Stará kombinácia `davka --kvalita master` sa odmietne s vysvetlením nového príkazu.

Výroba najprv overí vstupy celej dávky, potom zabezpečí materiály pre všetky klipy a až následne renderuje. Nevolá `propose` a nemení výber. Zmenený plán, prepis, analýza, Selection, miestny súbor alebo klientské pravidlá vyžadujú novú prípravu. Neúplná dávka ostane uložená s konkrétnymi príčinami; chybný klip nezmaže plány ostatných. Materiálové požiadavky sa zdieľajú iba pri zhodnom obsahu a kritériách, s osobitnou väzbou na každé použitie. Samotné zoskupenie ešte nepreukazuje vhodný trim ani získané médium. Výroba zatiaľ spracúva klipy postupne; kapacitná optimalizácia a meranie patria ďalším etapám.

Stav `prepared` znamená úplný plán pre materiálovú fázu, nie hotové video. Stav `review_required` po výrobe znamená výsledok na hodnotenie, nie tvorivé prijatie.

`kontrola` najprv skontroluje celý skutočný súbor a potom vybrané snímky dekódované z tohto mastera. Vision review v3 dostáva plán, brief, opis/účel/kritériá materiálov a najviac osem hashom overených referenčných PNG/JPG obrázkov. Referencie sa nezamieňajú za snímky výstupu. Hodnotí sa presná fáza setup/reveal/hold/return: zámerná príprava pred odhalením nie je chýbajúci materiál. Ilustračný či štylizovaný panel sa posudzuje podľa zadania; pri požadovanej presnej osobe alebo udalosti sa naďalej overuje konkrétna identita a médium. Vzorkované snímky nepreukazujú súvislé prehratie alebo posluch.

## Pripomienka a oprava

```sh
python3 system/cli/klipy.py pripomienka --epizoda TEST --klip prvy --typ event --event event-ID --nalezenie "Grafika zakrýva titulky." --zmena "Posunúť kartu vyššie."
python3 system/cli/klipy.py uprav --epizoda TEST --klip prvy --pripomienka feedback-ID --patch oprava.json
python3 system/cli/klipy.py materialy --epizoda TEST --klip prvy
python3 system/cli/klipy.py nahlad --epizoda TEST --klip prvy --event event-ID
python3 system/cli/klipy.py nahlad --epizoda TEST --klip prvy --kvalita master
python3 system/cli/klipy.py kontrola --epizoda TEST --klip prvy
python3 system/cli/klipy.py kontrola --epizoda TEST --klip prvy --pripomienka feedback-ID --poznamka "Opravená karta je nad titulkami v novej verzii."
```

Eventový patch mení `params`, kotvy, fázy alebo vrstvu konkrétnej udalosti. Udalosť sa následne uzamkne pred ďalším modelovým návrhom. Crop patch používa polia Framing; materiálový patch má `requestId` a nové polia požiadavky; mix patch obsahuje `sfx` alebo `music`. Oprava slova používa feedback typu `word`, `--slovo word-ID` a patch `{"text":"opravené slovo"}`. Vytvorí nový prepis bez nového ASR, zachová pôvodný text a čas a prenesie nezmenené rečové rozhodnutia na novú revíziu. Obsahová analýza ostáva označená ako staršia voči novému prepisu. Zmena hraníc alebo poradia reči ide cez nový `vyber`.

Pri oprave hlasového strihu typu `speech` zvolí nové úseky Adam a výber výslovne spojí s pripomienkou:

```sh
python3 system/cli/klipy.py vyber --epizoda TEST --klip prvy --od-ms 1000 --do-ms 18000 --pripomienka feedback-ID
```

Rovnako možno použiť `--kandidat` alebo `--intervaly`. Príkaz uloží nemenný `speech-repair-selection` audit s presným výberom, prepisom a pôvodnou pripomienkou. Nasleduje `navrhni`, `materialy`, celý `nahlad`, `kontrola` a výslovné overenie pripomienky. Až kompatibilný nový plán a skontrolovaný celý výstup umožnia stav `verified`; iná neskoršia Selection ani starý check ho nenahradia. Samotný výber ešte nepredstiera opravený render.

Krátky náhľad zachováva čas celej kompozície. Pred prijatím sa kontroluje celý nový master. Staré revízie ostávajú nemenné. Úspešná kontrola nevynuluje automaticky pripomienky; overenie opravy má vlastný záznam.

Technické a modelové nálezy z `kontrola` sa automaticky uložia aj do feedbacku, s konkrétnou cieľovou revíziou. Otvorené alebo iba aplikované závažné nálezy treba pred prijatím overiť. Ak je nález chybný, napríklad hodnotil zámerný setup ako chýbajúce odhalenie, možno ho výslovne odmietnuť s konkrétnym dôvodom:

```sh
python3 system/cli/klipy.py kontrola --epizoda TEST --klip prvy --pripomienka feedback-ID --verdikt rejected --poznamka "Nález hodnotil setup; skontrolovaná následná snímka po odhalení obsahuje objednaný panel."
```

Výsledkom je `rejected` pre tento konkrétny nález, nie globálne vypnutie pravidla alebo prijatie celého klipu. `--verdikt verified` je predvolený verdikt pri overení aplikovanej opravy. Odmietnutie nálezu neprepisuje uložené zlyhané dôkazy: aktuálny master stále potrebuje zodpovedajúcu úspešnú kontrolu.

## Kritický priechod P5

Na presné nálezy z reálnych snímok, viac opráv jednej revízie a pozorovanie výsledku slúžia `kritika` a `uprav --zmeny`. [Úplný postup, formáty a hranice schopností](KONTROLA_A_OPRAVY.md). Kritika kontroluje aj bohaté spracovanie a odlišnosť klipov podľa Adamovho tvorivého zadania. Oprava nie je tvorivé prijatie.

## Prijatie a lokálny export

```sh
python3 system/cli/klipy.py nahlad --epizoda TEST --klip prvy --kvalita master
python3 system/cli/klipy.py kontrola --epizoda TEST --klip prvy
python3 system/cli/klipy.py prijmi --epizoda TEST --klip prvy --pozrete --vypocute --poznamka "Pozrel a vypočul som celý tento master; výsledok prijímam."
python3 system/cli/klipy.py export --epizoda TEST --klipy prvy
```

`--pozrete` a `--vypocute` sú explicitné Adamove vyjadrenia o celom súbore. Automatická kontrola rozlišuje dekódovanie/meranie, skutočne prezreté snímky a posluch. Text, snímky ani metrika hlasitosti sa neoznačia za vypočutie. Bez reálneho posluchového záznamu produkčné prijatie neprejde. Nový protokol `p5.v1` vyžaduje aj úplný dôkaz súvislého pohybu; samotné snímky alebo vznik MP4 nestačia.

ReviewRecord viaže konkrétne bajty mastera, plán, materiály, Timeline aj zdroje. Export všetko znovu overí a skopíruje presne prijatý master. Nový encode, vymenená fotografia alebo tvorivá revízia vyžadujú nové prijatie. Výsledok je lokálny manifest prijatých súborov.

Prijatie aj export kontrolujú aktuálnu Selection, Transcript a Source; staré navzájom zhodné artefakty neprejdú po novom výbere alebo zmene zdroja. Otvorený storyboard moment a závažný nevybavený feedback blokujú prijatie. Produkčné prijatie nemá testovaciu výnimku pre nevypočutý zvuk.

## Uložené výsledky

Spoločné revízie epizódy sú v `fiki/epizody/TEST/artefakty/<kind>/r0001.json` s kontrolovaným `latest.json`; jednotlivé klipy majú vlastné `klipy/<clipId>/artefakty/`. Behy a cache sú v `behy/`, modelové requesty/odpovede v `modelove-behy/`, renderové médiá a ich manifesty v `klipy/<clipId>/rendery/<runId>/`. Neprepájajú sa ručne medzi fázami.

`stav --report` vytvorí `prehlady/stav.json`, `stav.md` a `stav.html` s lokálnymi odkazmi na médiá, kandidátmi, storyboardom, pôvodom materiálov a nálezmi. Autoritatívne sú kanonické artefakty; prehľad je z nich odvodený. Prijatý export je v `fiki/epizody/TEST/export/<hash>/manifest.json` spolu s presne prijatými MP4 súbormi. Priečinok `fiki/vystupy/` súčasný runner automaticky nenapĺňa.

## Technické testy a #105

```sh
cd system
npm run typecheck
npm test
RUN_LOCAL_ASR=1 node --import tsx --test tests/integration/ingest.test.ts
node --import tsx --test tests/integration/renderer.test.ts
KLIPY_LIVE_MODEL=1 KLIPY_MODEL_PROVIDER=codex KLIPY_LIVE_FULL=1 node --import tsx --test tests/integration/model-provider.test.ts
RUN_ORCHESTRATION=1 node --import tsx --test tests/integration/orchestration.test.ts
node --import tsx tests/e2e-live.ts
node --import tsx tests/e2e-finish.ts
```

Testy používajú izolované syntetické vstupy a označené fixture rozhodnutia. `e2e-finish.ts` nadväzuje na pripravený živý fixture; nejde o príkaz pre produkčnú epizódu. Fixture prijatie mechaniky exportu výslovne zachováva `not_listened`; nevytvára Adamovo tvorivé prijatie. Finálne počty a výsledky kontrol patria do [overovacieho reportu](OVERENIE_M0_M8_2026-10-17.md), nie do predpokladu, že samotné spustenie testu znamená úspech.

Epizóda **105 má v runneri zákaz spracovania**, kým nezačne samostatne autorizovaný spoločný test M9. Jej existujúci prípravný obsah zostáva samostatný. Starý projekt je iba zdrojom doloženého selektívneho prenosu; nový runtime ho nepoužíva.


## Knižnica a kalibračné scény P1–P2

Overené 25. 10. 2026; [stav a ukážky](OVERENIE_P0_P2_2026-10-25.md). Hlavný vstup zostáva rovnaký:

```sh
python3 system/cli/klipy.py kniznica --akcia search --dotaz "človek sa trasie"
python3 system/cli/klipy.py kniznica --akcia dry-run --manifest work/implementation-p0-p2/p1/import-canonical.json
python3 system/cli/klipy.py kniznica --akcia rebuild
```

`--akcia import --manifest JSON` vykoná konkrétny overený import. Historické migračné manifesty v tomto behu boli použité v poradí a prípadné opravy majú supersedes väzby; nie sú globálnym automatickým skenerom všetkých priečinkov. Import zachová pôvodné bajty, náhľady uloží do knižnice a opakovanie nevytvorí druhý originál. Výstup search je LibraryContext s mediálnymi kandidátmi a relevantnými receptmi. Nie je to schválený nový edit.

`materialy --volby JSON` prijíma aj `localDecisions` podľa `LocalMatchDecision` v `system/providers/production-library.ts`: presný requestHash, mediaHash, annotationHash, rozhodnutie, dôvod, pozorovateľ, overenie presného kontextu a trim videa. Vyhľadanie samo neznamená obsahové vyriešenie. Explicitná URL/vybraný externý kandidát sa nenahrádza voľnou lokálnou zhodou.

Nový plán môže mať `productionPack: {id, version, hash}` a udalosť `scene: "Authored"` s typed `authored` bindingom. Runner načíta presný balík z `fiki/kniznica/production-packs`; compiler a renderer overia scenárové sloty, kotvy a implementačný hash. Zmenený balík vyžaduje novú verziu/plán. Staré plány bez balíka zachovajú starú cestu. V P2 je dostupná scéna `media-stage@1.0.0` a balík `fiki-editorial@0.1.0` so stavom calibration.

Registrácia novej implementácie je explicitná údržbová operácia s kontrolou zdrojov, parametrov a testami. Nie je to ľubovoľný import path z modelového plánu. Automatické plánovanie celej dávky, nové nástrojové fulfillment úlohy a pracovný skill P6 zatiaľ nevznikli.


## Nástrojové úlohy (P4)

Príkaz `uloha` pripravuje, preberá a overuje výsledky dohľadávania, imagegenu a autorského kódu. Presné argumenty, JSON vstupy, obnova a obmedzenia sú v [NASTROJOVE_ULOHY.md](NASTROJOVE_ULOHY.md). Skutočné použitie obrázka a novej scény dokladá [overenie P4](OVERENIE_P4_2026-10-26.md).
