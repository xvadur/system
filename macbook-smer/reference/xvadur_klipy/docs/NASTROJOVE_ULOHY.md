# Nástrojové úlohy P4

Codex vykonáva nástrojovú prácu; lokálne CLI ukladá požiadavku, prijíma súbor a overuje jeho väzby. Headless planner ani workplace worker tým nezískavajú nástroj imagegen.

## ElevenLabs — priame API

Adamov explicitný pokyn zo 4. novembra 2026: hudbu a SFX z ElevenLabs získavať cez API. Browser nie je predvolená výrobná cesta. Už vytvorené súbory sa použijú ďalej; zmena prístupu sama nie je dôvod opakovať platené generovanie.

Oficiálne endpointy sú `POST /v1/sound-generation` a `POST /v1/music`. Kľúč patrí do súkromnej konfigurácie vykonávateľa; nepatrí do promptu, logov, receiptov ani zdrojových súborov. Ukladať skutočný request bez poverení, provider ID, výstupné bajty a hash. Po nejasnom výsledku najprv dohľadať pôvodný výsledok, nie slepo generovať znovu. Tento predpis sám nepotvrdzuje nakonfigurovaný ani otestovaný API adaptér.

Lokálne pripojenie overené 4. novembra 2026: Adamom dodaný kľúč je mimo projektu v `/Users/xvadur_mac/.config/xvadur/elevenlabs-api-key` (súbor `0600`, adresár `0700`). Nástroj ho načíta priamo do pamäte a použije iba ako hlavičku `xi-api-key` voči `https://api.elevenlabs.io`; nesmie ho vypísať ani interpolovať do shell príkazu. `GET /v1/user/subscription` aj `GET /v1/models` vrátili HTTP 200. To potvrdzuje autentifikáciu a tieto čítacie oprávnenia; živé generovanie SFX/hudby cez API zatiaľ nebolo testované. Existujúce médiá pilota #110 sa negenerovali znovu.

## Postup

1. Načítať aktuálny EditPlan a pripraviť úlohy cez `uloha --akcia priprav`. Pre požiadavku na priehľadný výrez sa v `--volby` zadá `{ "request-alebo-need-id": { "transparent": true } }`. Referencie majú lokálnu cestu, SHA-256 a vysvetlenie. Ich bajty sa kontrolujú pred prevzatím aj prijatím výsledku.
2. Prevziať jednu úlohu cez `uloha --akcia prevziat --task HASH --vlastnik TEXT`. Externý nástroj sa vykoná iba pri `execute: true`. `execute: false` nie je pokyn zopakovať generovanie. Stav `output_received` znamená pokračovať kontrolou uloženého súboru.
3. Pri imagegene použiť skutočný nástroj Codexu. Výstup skopírovať z cesty v odpovedi do projektu; zachovať pôvodný obrázok. Prompt, identifikátor volania a referenčné hashe patria do provenance. Fotografia presnej udalosti sa nesmie nahradiť vymysleným obrázkom.
4. Cez `uloha --akcia prijmi --data JSON` odovzdať `taskId`, lease `token`, `parentHash` (kanonický hash `task.parent`), zoznam `outputs` a `provenance`. Výstup má `path`, `hash`, `mediaType` a `role`. Prijatie ešte neznamená obsahové overenie.
5. Výsledok skutočne prezrieť alebo vykonať príslušnú kontrolu. Cez `uloha --akcia over --data JSON` odovzdať `taskId`, `token`, `evidence` a konkrétny `reason`. Každý dôkaz uvádza `kind`, `observer`, `notes` a skutočné `artifacts: [{path,hash}]`. Podporované režimy sú `image-observation`, `sampled-video`, `listening`, `scene-validation`, `context-review`. Vzorkované video nie je súvislé prehratie ani posluch.
6. `materialy` načíta overené výsledky samostatným argumentom `providedSources`. Pôvodný AssetRequest ani jeho hash sa nemení. Výstupný AssetRecord obsahuje väzbu na task, receipt, overenie a pôvodnú požiadavku.

Všetky operácie majú spoločné `--epizoda ID`, prípadne `--fixture --workspace system/tests/work/NAME`. Stav konkrétnej úlohy číta `uloha --akcia stav --task HASH`. Adam tieto JSON súbory ručne nepripravuje; ide o rozhranie pre Codex.

## Obnova a revízie

Úlohy sú pod `epizoda/fulfillment/tasks/HASH`. Task, revízie stavu, receipts, výsledné súbory a overenia sú nemenné; `state.json` je overovaná aktuálna projekcia. Opakované doručenie toho istého výsledku vracia rovnaký receipt. Zamenené bajty, iná identita, referencie alebo aktuálny parent sú chyba.

Vypršaný `in_progress` má neznámy výsledok. Systém ho presunie do `needs_input` a nevráti oprávnenie na ďalšie generovanie. Codex najprv dohľadá pôvodný výstup. `obnov-vystup` vydá lease na príjem existujúceho výsledku, stále s `execute: false`. Samotné vypršanie pozorovania nie je dôkaz zlyhania nástroja.

Po zmene plánu vznikne nová úloha. Starý receipt sa nepremenuje na nový. Ak existujúci materiál stále vyhovuje, Codex ho explicitne prevezme do novej úlohy so zachovaným pôvodom a novým obsahovým zdôvodnením. Nové generovanie nie je potrebné. Príklad je v `work/completion-2026-10-26/p4/revision-2-fulfillments.json`.

## Otvorené potreby

`editorial.openNeeds` môže cez `assetRequestId` spojiť potrebu materiálu s existujúcou požiadavkou; nevznikajú dve nezávislé generácie. `eventId` pripája implementáciu scény ku konkrétnemu Authored eventu. Overený výsledok uzavrie iba potrebu presného aktuálneho plánu a iba pri skutočnom pripojení výstupu do udalosti alebo audio stopy. Väzby vstupujú aj do hashov prípravy dávky.

Otvorená os, chýbajúci event, neznáma scéna či nevyriešený význam zostávajú otvorené aj po prijatí súboru. Codex musí urobiť výslovnú novú revíziu plánu. Receipt sám nemení reč, obrazové rozhodnutie ani Adamovo prijatie.

## Nová autorská scéna

Kód a schéma vznikajú v samostatnej pracovnej kópii. Po typechecku a kontrole závislostí sa pridajú do statického registra, ktorý rozširuje pôvodný zmrazený P2 register. Manifest pripína presné zdrojové súbory. Nový ProductionPack zapne konkrétnu verziu scény bez úpravy starého balíka.

Prvý taký prírastok je `JourneyStage 1.0.0`: odhalenie, začiatok pohybu, príchod a návrat. Všetky štyri fázy prekladá spoločný compiler; renderer nepovoľuje import cesty ani spustiteľný kód z modelového plánu. Po prijatí manifestu sa vykoná reálny render a porovnanie rovnakých absolútnych snímok krátkeho a celého videa. Statická kontrola manifestu sa nevydáva za vizuálne prijatie.

Register je miesto pre ďalšie verzované implementácie, nie povinná sada kartičiek pre každý obsah. Ďalší nápad dostane vlastný kód, parametre, fázy, manifest, overenie a spoločný binding.
