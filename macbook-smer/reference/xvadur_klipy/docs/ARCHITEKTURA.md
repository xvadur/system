# Architektúra XVADUR Clipping System

Aktuálny návrh od 4. novembra 2026 pre spoločný build podľa [plánu C0–C6](../PLAN_IMPLEMENTACIE.md#aktívne-implementačné-etapy-c0c6) a [dohôd 10.15](XVADUR_CLIPPING_SYSTEM_DOHODY.md#1015-aktuálny-prevádzkový-kontrakt-cloudflare-drive-mac-cli--oprava-4-novembra). Cloudflare Workers + static frontend + D1 riadia web a stav, Google Drive uchováva médiá, Mac vykonáva Codex CLI a mediálnu výrobu. **Ide o rozpracovanú implementáciu, nie potvrdenie nasadenia, migrácie alebo úspešného integračného testu.** Prevádzková SQLite zostáva autoritou do overeného cutover.

## Aktuálny prevádzkový model

~~~text
Adamov browser → Cloudflare static frontend + API → D1
                    │                              │
                    │ súkromné médiá/prenos         │ claim, heartbeat, commit
                    ↓                              ↓
                Google Drive ← overené prenosy → Mac polling worker
                                                   │
                                  cache + Codex CLI + ASR + Remotion/FFmpeg
~~~

Web je skutočne hostovaný na Cloudflare a zostane dostupný pri vypnutom Macu. Mac sa pripája odchádzajúcimi autentifikovanými požiadavkami; verejný tunel na lokálny Node server nie je cieľová architektúra. Živý stav, komentáre a fronta prežijú výpadok vykonávateľa. Výroba a ešte nevykonané API úlohy môžu čakať; nevyžaduje sa Linux server ani pokračovanie renderu pri vypnutom Macu.

Nové epizódy majú prioritu pri uvoľnení kapacity. Príprava médií beží dopredu; pripravený klip sa nesmie zastaviť na nesúvisiacej potrebe suseda. Jeden náročný zostavovací/renderovací job zdieľa rozpočet CPU/RAM/disku s prepisom, proxy a dekódovaním. Tvoriví agenti, provideri a ťažké lokálne procesy majú samostatné limity. Počet účtov ani kandidátov neurčuje počet agentov.

## Jedna autorita stavu a nemenné artefakty

| Vrstva | Čo vlastní | Čo nevlastní |
| --- | --- | --- |
| D1 po cutover | Účty, klipy, verzie, epizódy, upload sessions, komentáre, joby/pokusy/leases, aktuálne revízne hlavičky, závislosti, receipts, stavy nálezov, prijatia, publikácie, merania a register médií/lokácií. | Neuchováva veľké video bajty ani lokálne renderové procesy. |
| Nemenné kanonické payloady | Transcript, Selection, EditPlan, Timeline, ReviewRecord, FeedbackRecord a auditné prílohy so schémou/revíziou/hashom. Menšie payloady možno uložiť priamo do D1; väčšie cez nemenný Drive objekt. D1 určuje ich aktuálnu referenciu a stav. | Nevytvárajú paralelnú frontu ani vlastné cloudové latest pointery. |
| Google Drive | Originály, knižničné médiá, náhľady, masters, zdrojové snapshoty scén a veľké nemenné artefakty s overenými lokáciami. | Nie je synchronizačný mechanizmus SQLite, živého registra alebo schválení. |
| Mac cache | Materializované súbory podľa hashov, aktívne a semiaktívne kópie, pracovné adresáre pokusov, lokálne logy a denník výsledkov čakajúcich na potvrdenie. | Neurčuje centrálny head, prijatie, publikáciu ani dokončenie jobu. |
| Webové projekcie | Zoznamy, dashboard, filtre, súhrny, stav dostupnosti workera a prehrávač presnej verzie. | Nezakladajú vlastné identity, druhú Selection/Timeline alebo schválenie bez doménovej operácie. |

Autorita konkrétneho údaja sa nemení podľa toho, kde sa práve nachádza jeho kópia. Starý prijatý JSON, médium alebo master ostáva nemenný; nová lokácia sa eviduje samostatne. Nové polia sa nevkladajú spätne do pôvodných payloadov a nemenia ich hashe. Knižničný index, thumbnail a lokálny latest.json sú obnoviteľné projekcie; aktuálnu revíziu po cutover určuje D1.

Kontrakty výroby naďalej vychádzajú zo system/schemas/. Workplace/shared/production.ts je spoločná verejná projekcia epizód, uploadov a jobov pre API/UI; nie ďalšia autorita časovania. Výpočty času zostávajú v TimelineCompiler. SourceRecord/Transcript určujú pôvod a slová, Selection strih reči, EditPlan zámer, AssetRecord konkrétne bajty a použitie, ProductionPack/AuthoredBinding verzie vykonateľných scén.

## Hranice modulov a rozpracované miesta

| Modul | Zodpovednosť | Miesto integrácie a stav |
| --- | --- | --- |
| Cloudové pracovisko | Overenie používateľa, doménové API, D1 stavy, atomické zmeny, verejné projekcie. | workplace/cloud/ sa implementuje nad D1 kompatibilným rozhraním. Neprenáša node:sqlite/fs operácie do Worker requestu. |
| Spoločný kontrakt | Verejné typy epizódy/uploadu/jobov a produktové pravidlá. | workplace/shared/production.ts; citlivé údaje a interný lease zostávajú mimo projekcie. |
| Migrácia | Konzistentný export/import pôvodných entít, JSON bajtov, vzťahov a metadát s reportom. | Nový exporter/importer nad dnešným workplace/server/store.ts a cloudovými migráciami; produkčný cutover nevykonaný. |
| Mediálne úložisko | Obnoviteľný prenos, overenie objektu, lokácie, autorizované streamovanie a Range/seek. | Drive adaptér a stream proxy sa implementujú; Drive autorizácia a živý prenos zostávajú neoverené. |
| Lokálny vykonávateľ | Poll/claim, izolované procesy, dostupné nástroje, cache, heartbeat a odovzdanie výsledku. | Napojenie na existujúce system/pipeline moduly. Starý workplace/worker/worker.mjs má loopback/edit obmedzenie a sám nie je novým cloudovým workerom. |
| Redakcia a materiály | Mapa celku, kandidáti, AI Selection, tvorivý plán, konkrétne materiálové úlohy a receipts. | analysis.ts, planner.ts, fulfillment.ts, providers/ a explicitné CLI profily; zmena profilov nenahrádza vykonávač generovania. |
| Výroba a kontrola | Compile, overené materiály, render, kritika, oprava a presná verzia. | runner.ts, cycle.ts, renderer/, review/critique/repairs a workplace bridge. Streaming hash/cache, modelové roly a master preset sú rozpracované. |
| Používateľské pracovisko | Tmavé štúdio, Prehľad, Videá, Na kontrolu, Výroba a časované pripomienky. | Existujúce workplace/src/ sa integruje; analytics-app/ nevytvára ďalší produkčný register. |
| Sociálne operácie | Schválený balík, plánovanie, API stav/ID, merania a obnova nejasného výsledku. | Zachovať existujúce workplace/social-api/ a social-connect/ ochrany, doplniť chýbajúce vykonávanie. Read 8/8 nie je overený upload. |

## Operácie, fronta a obnova

Každá meniaca operácia identifikuje operationId, typ operácie, relevantnú epizódu/klip, vstupný hash a očakávaný parent/head. Worker navyše predkladá identitu pokusu a platný fencing token. Tieto údaje sú návrhový kontrakt; konkrétne implementované endpointy a podporované polia dokumentuje ich kód a testy, nie samotná táto tabuľka.

| Operácia | Požadovaný invariant |
| --- | --- |
| Založenie uploadu/epizódy | Opakovanie tej istej požiadavky vráti rovnakú identitu; rovnaký operationId s iným vstupom je konflikt. |
| Claim | Atomicky rezervuje iba vhodnú pripravenú úlohu a nový pokus. Zohľadní závislosti, prioritu, dostupnosť vykonávateľa a kapacitnú triedu. |
| Heartbeat | Predĺži len stále platný vlastný pokus. Expirovaný alebo nahradený pokus nemôže obnoviť vlastníctvo. |
| Commit revízie/výsledku | Overí vstupný hash, parent/head, pokus a receipt; uloží revíziu, výsledok a odomknutie závislostí v jednej kontrolovanej zmene. |
| Opakované doručenie | Ten istý potvrdený vstup a výsledok vrátia pôvodný receipt. Starý výsledok nesmie dokončiť nový plán alebo nový text komentára. |
| Nejasný externý výsledok | Uchová provider/transfer ID a stav unknown; najprv dohľadá výsledok. Nevytvorí druhú platbu alebo upload slepým retry. |

Dnešný synchrónny Store.transaction nad BEGIN IMMEDIATE sa nesmie zameniť za nezávislý read a následný write cez sieť. D1 implementácia musí otestovať podmienené zápisy a výsledky dávky na skutočnom konkurenčnom správaní. Revízne číslo a aktuálny head sa prideľujú pod tou istou centrálnou kontrolou; lokálne nextRevision vypočítané z adresára nestačí. Pôvodné zámky chránia lokálne IO, nie globálny claim.

Výrobný job pred prvým renderom nepotrebuje existujúce versionId. Rozšírený kontrakt rozlišuje epizódové fázy, klipové fázy, materiálovú úlohu, opravu a publikovanie; nepodsúva falošnú verziu do historického edit jobu. Každý krok viaže presné vstupné revízie, kit, implementáciu a výsledné hashe. Nová revízia zneplatní dotknuté závislosti; prepis a nesúvisiace overené materiály sa neopakujú.

Mediálny krok ukladá lokálny výsledok a dôkaz pred odovzdaním. Potom nasleduje overený vzdialený prenos a podmienený commit do D1. Pád po uložení/úspešnom uploadovaní, ale pred potvrdením v D1, sa obnoví z lokálneho denníka a uloženého transfer ID. Nepotvrdený výsledok sa nesmie zobraziť ako hotová centrálna verzia. Potenciálne osirelé vzdialené objekty sa evidujú pre neskoršie bezpečné upratanie.

Polling/heartbeat musí zostať schopný komunikovať aj počas renderu; ťažké úlohy bežia v oddelených procesoch. Po strate lease môže worker bezpečne dokončiť lokálny zápis už rozpracovaného výstupu, ale nesmie ho commitnúť ako výsledok cudzieho nového pokusu ani začať nový externý vedľajší účinok. Po návrate najprv overí aktuálny stav a podľa neho znovu priradí použiteľný výsledok.

## Médiá, cache a pripravenosť balíka

Register rozlišuje mediaId, SHA-256/veľkosť/MIME, logický pôvod, vzdialený Drive file/revision identifikátor a dátum overenia. Absolútna lokálna cesta patrí do cache mapovania. Existujúce media ID, pôvodné cesty a hashe sa pri migrácii zachovajú; media_locations rozšíri lokácie bez prepisu historického média.

Obnoviteľný ZIP upload zapisuje veľké bajty do Drive a do API stav/identitu. Prípadný chunk proxy prenáša ohraničený stream; celý ZIP sa nenačítava do Worker pamäte ani aplikačného JSON. Prerušenie, expirácia session, odchýlka offsetu a nejasné potvrdenie posledného chunku majú explicitnú obnovu. Dokončený prenos sa nezamieňa s obsahovým overením ingestu; až skutočná kontrola súboru potvrdí hash, čitateľnosť a vlastnosti zdroja.

Súkromný prehrávač potrebuje autorizovanú mediálnu cestu s Range požiadavkami a seekom. Drive odkaz sám túto schopnosť nepreukazuje. Prístupové poverenia a upload session URL nepatria do bežnej verejnej projekcie, logov alebo modelového zadania. Živá brána musí overiť prehrávanie z Cloudflare pri nedostupnom Macu.

Stav ready_for_edit znamená úplný obsahový balík: presná Selection a prepis, platný plán a kit, všetky povinné overené materiály a splnené závislosti. Dostupnosť na Drive je oddelená od lokálnej pripravenosti konkrétneho workera; pred compile/render sa potrebné súbory hydratujú a overia v cache. Vyhľadávací link alebo prompt nie je hotový asset.

Hashovanie veľkých médií má byť streamingové. Jedna overená nemenná kópia zdroja sa zdieľa medzi klipmi; staging nesmie bez potreby znovu kopírovať celú 4K epizódu. Výmena cesty nesmie zmeniť payload/hash historickej Timeline. Lokálna pracovná kópia sa uvoľní až po potvrdení vzdialených bajtov a po zániku aktívnych závislostí. Stav prijatého mastera, naplánovaný upload a otvorené pripomienky sú dôvody zachovať potrebnú sadu.

## Modely, tvorba a render

Astra dostáva ohraničený tvorivý koncept a rozhodovanie, 6.1 konkrétnu realizačnú úlohu. Profily definujú povolené nástroje, výstupnú schému, čas/náklady a potrebný kontext. Dnešný analytický model.ts má zámerne obmedzené schopnosti; nové vykonávacie profily sa pridávajú osobitne. Skutočný prístup CLI ku generovaniu obrázkov, SFX a discovery sa preukáže reálnym výstupom príslušného adaptéra, nie zoznamom nástrojov desktopového chatu.

Jedna mapa celej epizódy predchádza banke kandidátov. Plánovači používajú spoločný verziovaný kit, presné pasáže s kontextom a relevantný prehľad ďalších klipov. Súbeh nesmie stratiť kontrolu opakovanej pointy alebo tvorivej rozmanitosti. Materiálové požiadavky možno zdieľať iba pri kompatibilnom význame a technických parametroch; požiadavka, konkrétne bajty a použitie v klipe zostávajú odlišné identity.

Jednu novú Timeline zostavuje jeden vlastník revízie. Nové autorské scény vznikajú v izolovanom balíku a do verzovaného registra sa prijímajú kontrolovane. Paralelní agenti neprepisujú spoločný Root.tsx, kit alebo rovnakú revíziu. Reč, titulkové slová a eventy používajú pôvodné stabilné slovné kotvy; obrazový zásah potichu nemení Selection.

Remotion zostáva 4.0.529 so samostatnými presnými závislosťami a lockfile. Nové masters majú 2160 × 3840; staré revízie zachovajú vlastné rozmery/fps. Ľahší náhľad používa rovnaký obsahový balík a časovanie. Jeden render job a vnútorné Remotion concurrency sú odlišné limity; zvyšovanie súbehu vyžaduje meranie. Samotný preset 4K nepreukazuje kvalitu zdroja, kontrolu mixu ani výkon osem klipov denne.

## Pripomienky, prijatie a publikácia

Pôvodný komentár vlastní workplace/D1: commentId, verzia, text, čas/rozsah a bodyHash. Výrobná interpretácia vytvára presný mapping na FeedbackRecord. Stavy open/applied/verified/rejected patria tej istej kanonickej evidencii a do UI sa premietnu až po potvrdení. Označenie komentára v UI samo nevyrieši blokujúci výrobný nález. Zmena textu komentára je nový vstup, ktorý starý pokus nesmie uzavrieť.

Historické prijatia master bajtov sa nemenia. Nový tok prijatia náhľadu potrebuje nemenný bundle: Selection/Transcript, EditPlan/Timeline, kit, implementácie scén, médiá, relevantné runtime/renderové nastavenia a dôkazy. Prijatie identifikuje presne tento balík a skutočný rozsah Adamovej kontroly; následný master pridá hash finálnych bajtov a technické overenie zhody. Ak sa zmení obsahový vstup, vzniká nová verzia na kontrolu. Živý Player sa ponúkne iba pri vernej podpore konkrétneho bundle; inak je referencia MP4 náhľad.

Kontrola rozlišuje techniku, skutočné obrazové snímky, pohyb a posluch. Snímková sekvencia môže overiť konkrétny nástup alebo polohu; neznamená celý súvislý AV zážitok. Chýbajúca automatická schopnosť zostáva viditeľná a príslušný rozsah posúdi Adam. Limit tvorivých kôl nevytvorí prijatie chybného výsledku; technické retry má vlastný limit a stav.

Publikačný zámer viaže prijatú presnú verziu, jeden účet, text/obálku a konkrétny termín. Stabilný kľúč a provider ID sa zachovajú aj pri neistom výsledku alebo presune slotu. API prijatie úlohy nie je potvrdený post; TikTok draft nie je publikácia. Po výpadku Macu sa zmeškané položky presunú podľa politiky, bez nárazového odoslania celej dávky. Zber o 07:00 Europe/Bratislava uchová skutočný observedAt; chýbajúce meranie sa spätne nevymyslí. Automatické odpovedanie, DMs a staré automatizácie sa touto migráciou neaktivujú.

## Migrácia a integračné brány

1. **C0 — inventár a vernosť dát.** Export zahŕňa všetky existujúce entity, nielen owned účty. Pôvodné JSON bajty, ID, dedupe kľúče, prijatia, publikácie a merania sa porovnajú pred/po na izolovanej kópii. Pôvodný workspace/path sa ponechá ako historický údaj; nové lokácie sa mapujú. Metadata sa rozdelia na trvácne doménové údaje, súkromné ciphertexty a neaktuálny runtime stav.
2. **C1 — konkurencia a fencing.** Súbežné claimy, expirovaný pokus, duplicitný výsledok, zmenený parent a zlyhanie uprostred commit dávky musia zachovať jednu autoritu a konzistentné závislosti. SQLite test double nenahrádza overenie nasadeného D1.
3. **C2 — prenos a prehrávanie.** Prerušené uploady/downloady, checksum mismatch, cache miss a súkromný seek sa overia na skutočných médiách. Drive autorizácia a živá skúška sú samostatné od syntetického HTTP testu.
4. **C3–C4 — vykonanie a obnova.** Pád po ASR, po generovaní a po renderi pred potvrdením obnoví už hotový krok. Nezávislý klip pokračuje pri chýbajúcom médiu iného klipu. Jeden skutočný balík prejde od slovných kotiev k 4K masteru a presnej kontrole.
5. **C5 — round-trip webu.** Presná verzia sa prehrá, komentár vytvorí dohľadateľnú opravu a zmenený bodyHash zneplatní starý výsledok. Dashboard pracuje so skutočnými entitami; neznáme metriky sú null/nedostupné.
6. **C6 — cutover a reálny výsledok.** Zastaviť staré zápisy, vytvoriť konzistentný export, overiť D1 import a až potom odovzdať autoritu. Starý server už nezapisuje. Overiť vypnutie/návrat Macu, reálny schválený upload s ID/URL, pilot #105 a následne prvých 16 výsledkov. Každý úspech má vlastný dôkaz.

Šifrované socialApi.secret položky sú dnes v metadata SQLite; všeobecný metadata endpoint by bol nesprávna verejná projekcia. Kľúč ostáva iba u oprávneného vykonávateľa, ciphertext zachová account/provider/purpose väzbu. Migrácia stavu sama nevyžaduje zopakovať už udelený login a nesmie predstierať chýbajúce upload scopes. Pri obnovovaní po cutover sa nové D1 zápisy musia rekonciliovať; starý SQLite snapshot a DNS prepnutie samotné nie sú dátovým rollbackom.

## Historická príloha: lokálna architektúra P0–P7

Nasledujúci blok uchováva pôvodný lokálny návrh a jeho dôkazy. Staré výroky o pracovisku/SQLite ako konečnej autorite, povinnom Adamovom predvýbere, výrobe iba v otvorenom Codex chate a čisto lokálnych cestách neplatia pre aktuálny prevádzkový kontrakt. Podrobnosti kanonických schém, slovných kotiev, scén, receipts a technických dôkazov zostávajú referenciou, pokiaľ neodporujú aktuálnym častiam vyššie. Historické stavy sa spätne neoznačujú za novú cloudovú implementáciu.

<details>
<summary>Historická architektúra z 25.–26. októbra a neskoršie orientačné poznámky</summary>


**Najnovšia aktualizácia smeru 4. novembra 2026:** nižší opis zachytáva architektúru a dôkazy októbrovej lokálnej verzie. Pre ďalšiu implementáciu majú prednosť [aktuálne dohody, najmä časť 10.15](XVADUR_CLIPPING_SYSTEM_DOHODY.md#1015-aktuálny-prevádzkový-kontrakt-cloudflare-drive-mac-cli--oprava-4-novembra): existujúci web/API a centrálne stavy sa prispôsobia prevádzke na Cloudflare; médiá budú na Google Drive a aktívne kópie na SSD Macu. Codex CLI, ASR, Remotion a FFmpeg bežia na Macu. Pri vypnutí môže výroba čakať a po návrate sa obnoví. Prenajatý Linux server ani nepretržitá výroba pri vypnutom Macu sa nevyžadujú. Kandidátov vyberá AI a Adam prijíma výsledok, materiály sa pripravujú do trvácnej fronty a finál má prioritu najvyššej kvality. Jedna dátová autorita zachová existujúce identity/históriu a kanonické kontrakty cez overenú migráciu; navrhovaná cloudová databáza je D1, nie druhý nezávislý register. Tento zápis nie je dôkazom nasadenia ani dokončeného prepojenia.

Revízia 25. októbra 2026. Táto architektúra je technická príloha [hlavného plánu P0–P7](../PLAN_IMPLEMENTACIE.md). **Stav po P0–P3:** import/anotácie/LibraryContext, kalibračný ProductionPack a AuthoredBinding cez spoločný compiler/renderer sú implementované; P2 čaká na Adamovo vizuálne prijatie. P3 pripája k EditPlan povinný rozhodovací priechod nových návrhov, presný LibraryContext a hash analýzy; implementuje klientské kontroly a uloženú prípravu dávky oddelenú od spustenia výroby. Rozsah, testy a obmedzenia sú v [reporte P3](OVERENIE_P3_2026-10-25.md). P4 implementuje trvácne úlohy, overené receipts, providedSources a ďalšiu autorskú scénu. [Overenie P4](OVERENIE_P4_2026-10-26.md). P5 implementuje kritické balíky skutočných snímok, skupinové opravy, ochranu zámkov a overenie nových bajtov; [päť renderových prípadov a hranice schopností](OVERENIE_P5_2026-10-26.md). P6 implementuje spoločný cyklus, obnovu revízií, round-trip pracoviska, scoped poučenia a výsledkové snapshots. [Overenie a hranice P6](OVERENIE_P6_2026-10-26.md), [pracovný vstup Codexu](CODEX_VYROBNY_POSTUP.md). Reálna kvalita a kapacita P7 zostávajú otvorené. [Presný implementačný rozsah a dôkazy](OVERENIE_P0_P2_2026-10-25.md). Súčasný kód a jeho syntetické technické dôkazy ostávajú zachované. Predchádzajúci opis kontraktov je dostupný v [historickej architektúre](historia/2026-10-25-pred-zjednotenim-planu/docs/ARCHITEKTURA.md).

## 1. Prevádzkový model

Adam potvrdil: celý postup funguje v Codexe. Codex je riadiaci a tvorivý vykonávateľ. CLI/TypeScript, lokálne súbory, Remotion a existujúce workplace sú jeho nástroje a evidencia. Neplánuje sa nový externý autonómny produkt.

~~~text
Adam v Codexe → načítanie uloženého stavu a pracovného predpisu
             → celá epizóda → kandidáti → Adamov výber/Selection
                                         ↓
spoločná knižnica → LibraryContext → oblúk klipu + rozhodovanie po momentoch
                                         ↓
                           EditPlan + potreby celej dávky
                                         ↓
             lokálna knižnica / discovery / imagegen / autorská scéna
                                         ↓ skutočné lokálne výsledky
                              compile → náhľad → kritika
                                         ↑         ↓
                                         └── oprava konkrétnej revízie
                                                   ↓
                       celý master → Adamovo prijatie → lokálny export
                                                   ↓
                workplace presná verzia + použitia/recepty/poučenia
                                                   ↓
                     ďalší klip dostane relevantnú uloženú skúsenosť
~~~

Dostupnosť nástroja v tomto chate nie je jeho dostupnosťou v samostatnom procese. Dnešný model.ts používa obmedzené textové/vision/research profily; webový worker má vlastný izolovaný editor. Imagegen alebo nový tvorivý kód preto dostanú explicitnú úlohu vykonanú Codexom a overený návrat do rovnakého záznamu.

## 2. Autority a kompatibilita

| Údaj | Autorita | Čo zostáva odvodené |
| --- | --- | --- |
| Originál a časované slová | SourceRecord, Transcript a ich presné revízie | Prehľady a pracovné náhľady |
| Hlasový strih | Selection viazaná na Transcript hash; Adamov výber | Všetky zostavené časy a framing |
| Zámer a rozhodnutia obrazu | CreativeBrief + EditPlan s odkazmi na momenty a dôkazy | Storyboard tabuľka/HTML |
| Lokálne médium | AssetRecord a hash pôvodných/odvodených bajtov | Vyhľadávací index, thumbnail |
| Recept alebo autorská scéna | Verzovaná implementácia, schéma parametrov a manifest závislostí | Predpripravené ukážky |
| Snímková skladba | TimelineCompiler a Timeline | Renderové props a frameRange |
| Oprava a prijatie | FeedbackRecord/ReviewRecord pre konkrétne revízie a hashe | Stavové prehľady |
| Klip v pracovisku | Existujúci clip/version register workplace s väzbou na produkčný hash | Dlaždice, filtre, odvodené súčty |
| Publikácia a meranie | Existujúce post/account/measurement záznamy s pôvodom | Graf a odporúčanie ďalšieho pokusu |

Knižničná anotácia neprepisuje AssetRecord; register pracoviska nevytvára druhú Selection ani Timeline. Import ich prepája stabilnými ID a hashmi. Schémy zostávajú v system/schemas/index.ts. Rozšírenia sa verzujú a existujúce revízie zostávajú čitateľné; povinné nové polia sa nevkladajú spätne do prijatých artefaktov.

## 3. Moduly a malé rozhrania

Klientské pravidlá sú explicitný verzovaný vstup: klient.json → doložená runtime migrácia/revízie → pravidlá použité analýzou, Selection a exportom. Negatívny test musí preveriť zakázaný zdroj/tému aj výnimku a platný rozsah plateného materiálu.

Technické názvy Module, Interface a Implementation označujú jeden modul, jeho verejné rozhranie a vnútorné vykonávanie. Nasledujúce názvy opisujú modulové rozhrania; verejným riadeným vstupom P6 je cyklus v CLI.

| Module | Interface pre volajúceho | Implementation a miesto zásahu |
| --- | --- | --- |
| EpisodeWorkflow | Pripraviť epizódu, pripraviť dávku, pokračovať v práci, vyrobiť pripravené klipy, opraviť, prijať/exportovať. Vždy vrátiť stav a konkrétne otvorené potreby. | Existujúci runner/store/CLI; pracovný návod pre Codex načíta stav a vyberie ďalšiu oprávnenú operáciu. |
| EditorialPlanning | Selection + kontext epizódy + LibraryContext + pravidlá → konkrétny plán a rozhodnutia. | Existujúca analýza/planner, doplnený editoriálny predpis a validácia referencií. |
| ProductionLibrary | Vyhľadať relevantné možnosti, pripraviť kontext, uložiť skutočné použitie/poučenie. | library.ts, anotácie a obnoviteľný index; lokálne médiá a recepty. |
| CreativeFulfillment | Prijať presne definovanú materiálovú alebo autorskú potrebu; overene dodať výsledok. | Existujúce acquisition/discovery plus úlohy pre nástroje Codexu; žiadny implicitný imagegen bridge. |
| ClipProduction | EditPlan + resolved materiály + scene bindings → Timeline → náhľad/master. | Compiler, renderer adapter a register autorských scén; Remotion 4.0.529. |
| ReviewAndDelivery | Overiť konkrétny výsledok, zapísať nálezy, overiť opravu, doručiť presnú verziu. | review.ts, autor/kritik, AV dôkazy a idempotentný workplace adapter. |

Projektový [pracovný návod pre Codex](CODEX_VYROBNY_POSTUP.md) obsahuje vstupné podmienky, poradie rozhodnutí, možné ďalšie operácie podľa uloženého stavu, hranice nástrojov, referenčné príklady a kontrolné kritériá. Jeho nástroje používajú dnešné schémy a store; úspech sa preberá z artefaktov, nie z textového vyhlásenia agenta. Konkrétne názvy a registrácia skillu sa overia v implementovanej verzii Codexu.

Dnešné detailné CLI operácie zostávajú dostupné technicky; Adam ich nemusí poznať. Nevytvára sa samostatný plánovací systém v Pythone vedľa TypeScript autority. Konkrétny nový wrapper/príkaz sa do docs/POUZIVANIE.md zapíše až s implementáciou.

## 4. Rozšírenia kontraktov

| Navrhnutý údaj | Minimálny obsah a väzby | Invariant |
| --- | --- | --- |
| ProductionPack | packId/version/hash, typografické úlohy a zóny, scény/recepty a registry refs, kamera/pohyb/prechody, spracovanie médií, zvuková paleta, CTA, povolené varianty a referencie. | EditPlan pripne presnú verziu; asset mení obsah, nie svojvoľne spoločný jazyk. |
| EditorialDecision (P3 implementované v EditPlan.editorial) | analysisHash, libraryContextHash, momentId, zdrojové wordId/spanId, funkcia, účel pre diváka; posúdené editačné osi; zvolený treatment a dôvody; alternatívy; očakávaný výsledok a skúška; event/request refs. | Každá os má použiť/nepoužiť/otvorené. Všetky nové časy sa odvodia z tých istých kotiev. |
| LibraryAnnotation | mediaHash, AssetRecord refs, sk/en aliasy, entity, viditeľná akcia, funkcia/tón, použiteľné trimy/crop, nábeh reakcie, zdroj a rozsah pozorovania. | Nepridáva druhý stav resolved ani nevymýšľa prezretie/posluch. |
| LibraryContext | Malý relevantný výber médií, postupov, príkladov a zamietnutí; revízie a dôvody relevancie. | Planner dostane skutočnú dostupnú výbavu, nie celý adresár alebo iba neurčité názvy. |
| BatchPreparation (P3 implementované) | clip IDs + Selection/plan hashes, pokrytie epizódy, spoločné potreby, stavy pripravenosti, otvorené schopnosti, rozmanitosť a ciele dávky. | Pripravená časť sa nevydáva za celú dávku; príprava sama nespustí master render. |
| FulfillmentRequest | parent request/event, vstupné hashe, druh potreby, účel, kritériá, capability, stav, výsledné lokálne refs a dôkazy. | Je pracovná úloha, nie AssetRecord, schválenie ani druhá časová os. |
| AuthoredBinding | sceneId/version, implementationHash, validované parametre, asset sloty a fázové kotvy. | Neobsahuje spustiteľný modelový kód alebo ľubovoľný import path. |
| ScopedLearning | Konkrétne použitie/feedback, poznatok, rozsah asset/use/recipe/client, dôkaz a istota. | Jedno miestne zamietnutie sa automaticky nestáva globálnym zákazom. |

ProductionPack sa odkazuje z briefu/plánu a jeho hash vstupuje do compile/render/review závislostí. Existujúci klientský štýl je migrované východisko; nová verzia balíka sa neaplikuje spätne na prijaté klipy.

EditorialDecision môže byť validovaná príloha existujúceho EditPlan; nemusí vzniknúť súbor pre každú checkbox voľbu. RecipeRecord sa rozšíri tak, aby rozlišoval deklaratívnu scénu, registrovaný autorský postup a dramaturgický/hook referenčný príklad. Existujúce SceneSpec recepty dostanú čitateľný migračný adaptér; nové diskriminované vetvy sa nebudú skrývať v neoverenom voľnom texte params.

## 5. Knižnica a obsahový výber

Rozhrania knižnice a poučení sú implementované v providers/library.ts, production-library.ts a learning.ts; schematický prehľad:

~~~ts
searchLibrary(query, clientScope) -> LibraryMatch[]
buildLibraryContext(selection, analysis, brief, batch) -> LibraryContext
chooseLibraryMatch(request, matches, evidence) -> MatchDecision
verifyMatch(request, match, decision) -> AssetRecord | FulfillmentRequest
recordOutcome(exactRevision, uses, review, scopedLearning) -> Receipt
~~~

LibraryMatch nesie stabilný ID/hash, dôvod zhody, použiteľné rozsahy, náhľady a relevantnú históriu. Textový planner dostane popisy a dôkazové odkazy; obrazové posúdenie dostane skutočné pixely náhľadov a vhodných sekvencií. Metadáta nie sú náhradou za pozretie materiálu.

Resolver zachová exact fingerprint ako rýchlu cache, ale ostatné lokálne zhody zaradí medzi obsahových kandidátov. Lokálny kandidát sa neodosiela HTTP downloaderu. Pri novej požiadavke sa overí nová funkcia, presnosť, dĺžka a trim; stará kontrola akcie pomáha, no neznamená automatické prijatie nového použitia. Až po neúspešnom lokálnom výbere sa dohľadáva alebo tvorí nový materiál.

Prvý index použije text, aliasy, entity, akcie, funkcie a technické filtre. Embeddingy majú zmysel až podľa doložených neúspešných dotazov. Originál sa deduplikuje podľa hashov; derivát má odkaz na rodiča. Rovnaká fotografia s iným cropom preto zostane rozpoznateľná ako rovnaký zdroj. Návrat motívu môže byť zámerný a odlišuje sa od nechcenej duplicity.

### Migrácia existujúcej práce

Importer najprv vytvorí dry-run inventár podporovaných konkrétnych manifestov; potom hash/decode, anotácie, pôvody a presné použitia. Začne Vajanského, Električkou a vybranými prijatými #105 scénami. Výskumné celé videá sa nepovažujú za čisté assety. Do médií sa plošne neimportujú QA screenshoty, cache ani opakované rendery.

Historický pôvod anotácie ostane doložený presným súborom/JSON pointerom. Chýbajúci náhľad sa môže pri implementácii vytvoriť nanovo a označiť novým dátumom. Neúplné historické prijatie alebo neznámy autor rozhodnutia sa nedoplní domnienkou. Poučenie bez kanonického starého plánu sa uloží ako legacy referencia; nevyrába sa falošný ReviewRecord ani selectedBy: Adam.

Opakovaný import a obnova po páde nesmú pridávať nové kópie originálu alebo UseRecord. Doložené minulé prijatie komponentu je referencia; jeho nová parametrická verzia potrebuje vlastné overenie.

## 6. Nástrojové úlohy v Codexe a imagegen

Druhy FulfillmentRequest sú obtain-media, generate-image, implement-scene a review-required. Codex vidí konkrétnu potrebu a použije svoj dostupný nástroj. Úloha obsahuje príslušný brief, presné referencie, požadovaný výsledok, spôsob kontroly a obmedzenia; nemá poverenie meniť uzamknutú reč alebo publikovať.

~~~text
open → in_progress → output_received → verified/fulfilled
                  ↘ failed / needs_input
~~~

Cieľová prijímacia operácia je receiveFulfillment(taskId, parentInputHash, outputs[path, sha256, mediaType], evidence) → FulfillmentReceipt. Receipt identifikuje pôvodnú úlohu, nemenný výsledný súbor a rozsah overenia. Nezapisuje dodatočne localPath do pôvodného AssetRequest, pretože by tým zmenila hash požiadavky, ktorú vybavuje.

materials()/resolveAssets() dostanú overené receipts cez samostatný proposed argument providedSources: Map<AssetRequestId, VerifiedLocalSource>. Acquisition použije tento lokálny zdroj oddelene od pôvodného obsahového requestu. AssetRecord bude viazať pôvodný request hash aj receipt a výsledné bajty; až jeho obsahové a technické vyriešenie uzavrie fulfilled. Menia sa vykonávacie vstupy, nie význam alebo parent identita plánu. Toto rozhranie je implementované v P4; nemení pôvodný localPath requestu. Presné operácie a obnova sú v [nástrojovom návode](NASTROJOVE_ULOHY.md).

Výstup sa preberá proti aktuálnemu parent requestu a vstupným hashom. Opakované doručenie má rovnaký receipt. Stará úloha po zmene plánu nemôže označiť nový plán za vybavený. Pri nejasnom výsledku sa najprv dohľadá existujúci výstup; drahá generácia sa slepo neopakuje.

**Imagegen:** určiť účel a vrstvy, výtvarné referencie, pomer strán, kompozíciu, potrebnú transparenciu a konzistenciu objektov. Pri úprave existujúci obrázok najprv pozrieť. Použiť skutočný dostupný nástroj Codexu; výsledný súbor identifikovať z jeho odpovede, skopírovať do projektu a hashom priradiť k úlohe. Uložiť prompt/referencie/pôvod generovania, rozmery, kontrolu a rodičovskú revíziu. Prompt sidecar bez obrázka zostáva nevyriešený.

Generovaná bitmapa môže byť pozadie, výrez, postava, rekvizita alebo séria stavov; časovanie a pohyb riadi kompozícia. Presná historická udalosť/dokument zostáva požiadavkou na reálny zdroj. Prvé navrhované obmedzenie je najviac dve obrazové iterácie na jeden materiál a dve interné tvorivé kolá na klip; po prekročení Codex zmení treatment alebo predloží konkrétny problém. Tieto limity sú plánovacie voľby na kalibráciu, nie údaj o schopnosti či cene nástroja.

## 7. Autorská scéna ako súčasť spoločného renderu

Dnešný SceneSpec ostane vhodný pre jednoduché deklaratívne grafiky. Nový dej môže Codex naprogramovať ako samostatnú React/SVG scénu. Zdrojový kód vznikne v izolovanej pracovnej kópii, prejde typecheckom, kontrolou závislostí a kľúčových stavov a až potom sa zaregistruje ako presná verzia.

Navrhnuté miesta: renderer/src/authored/registry.tsx pre statické importy známych komponentov; scenes/catalog.ts pre schémy parametrov, sloty, kotvy, obmedzenia a implementačné hashe. P2 registre sú zmrazené pre MediaStage 1.0.0. P4 ich rozširuje cez scenes/registry.ts a authored/extended-registry.tsx o JourneyStage 1.0.0, bez prepisu starého manifestu. Príslušné bindingy doplnia dnešné schema/compiler/adapter/scenes; samotný názov params.renderer z workshopu sa nespustí.

~~~ts
type AuthoredBinding = {
  sceneId: string;
  version: string;
  implementationHash: string;
  parameters: ValidatedParameters;
  assetSlots: Record<string, AssetRequestId>;
  phaseAnchors: Record<string, Anchor>;
};
~~~

Compiler preloží sloty na vyriešené assety a kotvy na snímky. Komponent dostane event-local čas, rozmery/fps, lokálne asset URL, schválené parametre a fázové snímky. Zvuky zostanú v spoločných audio trackoch. Náhľad aj master použijú rovnaký balík a props.

Modelový plán nevykonáva JSX/eval ani neurčuje cestu importu. Voľnosť tvorby je v osobitnom autorskom kroku Codexu, ktorý môže vytvoriť novú implementáciu a validovať ju. Registry teda nie je uzavretý zoznam vopred povolených nápadov. Pridanie novej scény musí skončiť spoločným bindingom a evidenciou, nie ďalšou epizódnou kompozíciou mimo runnera.

Neznáma verzia, zmenený implementationHash, chýbajúci slot, nepovolený import alebo neplatné parametre sú konkrétna chyba pred renderom. Pri nezmenenom recepte musí druhý obsah meniť iba jeho parametre/sloty/kotvy, nie implementačný kód.

## 8. Časovanie a obrazové vrstvy

Zdrojové aj logické časy sú celočíselné ms v polootvorených intervaloch. Slovná kotva nesie wordId, spanId, hranu start/end a offset; verziu prepisu viaže Selection. Pri opakovanom výskyte zdrojového úseku má span vlastnú identitu.

~~~text
clipTimeMs = span.startMs + word.startMs - span.sourceStartMs + offsetMs
frame = round(clipTimeMs * fps / 1000)
~~~

Pri konci slova sa použije word.endMs. Koncové snímky sa počítajú z absolútneho konca, nie súčtom osobitne zaokrúhlených dĺžok. Rozmery a fps patria konkrétnej revízii; 25fps Vallo a 30fps existujúce jadro sa nesmú potichu zamieňať.

Oddelené tracky sú voice, aroll, cutaway/graphics, captions, SFX, music a CTA. A-roll pri samostatnom voice tracku je stlmený. Vložka neprerušuje hlas; jej vlastný zvuk sa povoľuje výslovne v pláne. Výmena obrázka nemení hlasový zostrih. CTA tail je explicitný v Timeline a určí sa pred kotvami na clipEnd.

Krátky náhľad zachová absolútny čas kompozície a okolité zábery. Interný rozsah [a,b) sa pri potrebe prevedie na inkluzívny [a,b-1]. Prehrávanie a export musia zdieľať rovnakú kompozíciu; full-frame/split/PiP sa skladajú nad pôvodným zdrojom pred vypálením titulkov.

## 9. Dávka, obnova a pracovisko

P3 davka ukladá iba prípravu; vyrob-davku spotrebuje presný pripravený hash. P6 cyklus stav/priprav/pokracuj vedie Codex cez uloženú vybranú dávku, konkrétne nástrojové potreby a pripravené lokálne kroky. Priprav nerenderuje; pokracuj obnoví rozpracované revízne transakcie a vie pokračovať pripraveným klipom aj pri otvorenej potrebe suseda. Podrobný postup a hranice sú v pracovnom návode.

Spoločné requesty uchovajú väzby na všetky klipy, ale iba kompatibilné významové a technické požiadavky sa zlúčia. Fronta ukáže všetky vybraté klipy, ich stav a chýbajúce vstupy. Predvolená súbežnosť vychádza zo súčasných dvoch clip jobs a jedného renderu; zvýšenie vyžaduje meranie. Dokončenie jedného klipu nezastaví nezávislú prípravu ostatných.

Každá fáza ukladá vstupný hash, výsledok, chybu a presné závislosti. Výmena fotografie opakuje iba príslušné materiálové/compile/render/review kroky; nezopakujú sa import/ASR celej epizódy. Zmena anotácie/receptu ovplyvní nové plánovanie, nie bajty starého prijatého mastera. Zmena implementácie je nová verzia a nový kandidát.

Workplace adapter importuje manifest výslednej verzie idempotentne a prenesie časovanú pripomienku späť na konkrétny clip/event/word alebo čas. Ak zmenený strih posunie čas, pôvodná pripomienka zostáva naviazaná na starú revíziu a mapovanie sa odvodí z kotiev. Live Player sa ponúkne iba pre podporovaný presný scene bundle; MP4 je vždy výstupná referencia. Prevzatie lease, opakovanie doručenia a nový hash zachovajú dnešné ochrany workera.

### Autorita pripomienok a prijatia medzi pracoviskom a výrobou

Workplace vlastní pôvodný comment ID, text, čas a verziu, ku ktorej Adam komentoval. Po odoslaní pripomienok do výroby vznikne presný mapping originRef(commentId, versionId, bodyHash) → jeden alebo viac FeedbackRecord. Kanonický FeedbackRecord vlastní výrobné stavy open/applied/verified/rejected a príslušné opravné revízie. UI stav je projekcia potvrdeného výsledku; ručné označenie komentára v UI samo neuzatvára blokujúci výrobný nález.

Príjem výsledku opravy vracia idempotentný receipt s pôvodným comment ID a všetkými od neho odvodenými nálezmi. „Vyriešené“ sa v pracovisku zobrazí až po uzavretí všetkých požadovaných nálezov overením alebo explicitným zdôvodneným odmietnutím. Zmena textu/rozsahu komentára vytvorí nový vstupný hash; starý pokus nesmie vybaviť nový komentár. Komentár bez žiadosti o úpravu sa automaticky netvári ako výrobný blok.

Prijatie presného mastera povoľuje kanonická accept operácia po vyriešení relevantných nálezov a skutočnom Adamovom verdikte. Pracovisko uloží väzbu na ReviewRecord/receipt; samotný lokálny UI status accepted túto operáciu nenahrádza. Pri nedoručenom receipt zostane synchronizácia čakajúca, nie falošne prijatá. Existujúce lease fencing a idempotencia sa zachovajú.

## 10. Kontrolné dôkazy

P5 má implementované rozhranie `kritika priprav/prijmi/over-opravu` a `uprav --zmeny`; [presný pracovný postup](KONTROLA_A_OPRAVY.md). Kritika sa viaže na aktuálny celý render a skutočné pixely, bez predstierania posluchu alebo celkového pohybu.

Technická kontrola meria/dekóduje celý súbor. Vision posudzuje skutočné snímky s uloženým časom a hashom. Pohyb má capability režim: (a) časovaná sekvencia skutočných snímok plus deterministické výpočty overia konkrétne fázy/pozície/nástupy, (b) skutočne overený video adaptér môže posúdiť súvislý priebeh vo svojom doloženom rozsahu, (c) bez neho celkový pohyb a rytmus preverí Adam pri prehratí mastera. Samotný prehrateľný súbor ani niekoľko snímok nepreukazujú plynulosť alebo komický rytmus. Review uloží použitý režim, rozsah a zostávajúcu neistotu. Posluch sa zaznamená iba pri skutočnom poslucháčovi/schopnosti a rozsahu. Pri chýbajúcom audio adaptéri v Codexe má finálny celý posluch Adam.

Kritik dostane kontext, zámer, použité médiá a skutočný výstup. Nález má konkrétny cieľ a dôkaz, nie iba skóre. Oprava vytvorí novú revíziu; verification musí ukazovať opravené miesto s okolím aj relevantnú kontrolu celého klipu. Presné prijatie viaže všetky hashe vrátane kódu, médií a plánu. Export presne skopíruje prijaté bajty.

## 11. Konkrétne testy priradené k P etapám

| Etapa | Test správania cez rozhranie | Očakávaný dôkaz |
| --- | --- | --- |
| P1 | Dva manifesty toho istého súboru, opakovaný import a pád pred indexom. | Jeden originál, zachované pôvody, bez duplicitného použitia po obnove. |
| P1/P3 | Zima / človek sa trasie / cold reaction; nová request formulácia. | Vhodný lokálny kandidát bez presného fingerprintu; jeho konkrétny trim a dôvod. |
| P1/P4 | Nesprávna osoba, príliš krátky klip, zamenené bajty, iný klient. | Odmietnutie alebo otvorená potreba, nikdy tichý resolved. |
| P2/P4 | Rovnaká scéna s dvoma obsahmi; neznáma verzia či chýbajúci slot. | Dva výstupy cez spoločnú Timeline; negatívny prípad zastavený pred renderom. |
| P3 | Zakázaný zdroj/video/téma, filmový Oscar verzus zakázaná osoba, prekročený platený rozsah. | Odmietnutie podľa presnej revízie pravidiel; výnimka nevyrobí nesprávny zákaz. |
| P3 | Moment bez posúdenia zvuku/humoru/obrazu; povinná potreba otvorená. | Čitateľný neúplný plán; schéma ani placeholder nezakryjú medzeru. |
| P4 | Skutočný imagegen výsledok, opakované doručenie, stará úloha pre nový plán. | Jedna overená lokálna referencia; žiadne slepé opakovanie generovania; starý plán sa nerozváže. |
| P5 | Pointa pred slovom, reakcia mimo trimu, kolízia, duplicitná fotka, nečitateľný súčet. | Konkrétny nález, nová revízia a overenie opravy. Zámerný callback sa nezakáže automaticky. |
| P5 | Snímky a waveform bez AV posluchu. | Pravdivý rozsah review; listened sa nevymyslí. |
| P6 | UI comment resolved, ale otvorený FeedbackRecord; zmenený bodyHash. | Výrobný guard naďalej blokuje prijatie; starý výsledok neuzavrie nový komentár. |
| P6 | Pád po renderi pred doručením; opakovaný import výsledku. | Ten istý výsledok a jedna workplace verzia bez nového renderu. |
| P6/P7 | Nový klip B po prijatom klipe A na odlišnú tému. | Relevantná nová položka/poučenie z A sa dostane do B a použitie je doložené. |

Presné testovacie súbory a príkazy sa doplnia pri implementácii. Tieto prípady nie sú tvrdením o už spustených kontrolách. Záverečné tvorivé a kapacitné kritériá sú výhradne v P7 hlavného plánu.

</details>
