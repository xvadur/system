# Dávková výroba: pasáže, spracovania a objem

Dátum: 6. november 2026. Stav: konkrétny návrh prepojenia po prečítaní kódu, nie implementácia alebo doklad kapacity. V tomto kroku nevznikol render ani publikácia.

## Adamovo aktuálne zadanie

- Cieľ je 1 200 samostatných hotových videí mesačne: 600 Fiki, 600 Smer. Fiki má osem účtov, Smer má mať približne ďalších osem.
- Rovnaká pasáž môže dostať viac samostatných obrazových spracovaní a tie sa rátajú do objemu. Nevyžaduje sa 1 200 rozdielnych pasáží.
- Zo zdroja sa využijú všetci použiteľní kandidáti. Príklad 40 minút → 20 kandidátov je Adamov modelový príklad, nie nameraná výťažnosť.
- Východiskom tvorby sú už dodané referencie, rozbory a nakonfigurovaný remotion-reel. Adam môže tiež pozrieť kandidáta a nadiktovať konkrétnu réžiu. Obe cesty používajú tú istú výrobu.
- Pravidelnosť a objem sú prevádzkový cieľ. Výroba pod Adamovým vedením môže fungovať počas dopĺňania automatizácie; úplná autonómia nie je podmienkou každého ďalšieho klipu.
- Ďalšie spresnenie: spoločným tvorivým základom má byť Remotion vrátane skillov, balíkov a opakovane použiteľných scén. Adam navrhol viac editačných kitov: raw + titulky, rapid cut, Fiki core, meme a explainer s grafmi. Hustota Fiki core sa preto nemá plošne vnucovať raw alebo ostatným zámerne odlišným variantom.
- Adam otvoril možnosť trvalo dostupného Remotion pracoviska na subdoméne. Ide o návrh prevádzky na posúdenie, nie vykonané nasadenie alebo obstaranie servera.

## Editačné kity nad jedným Remotion základom

Kit združuje vykonateľné komponenty/scény, editorské postupy, relevantné referencie, parametre a ukážky správneho výsledku. Agent vyberá a skladá konkrétne použitie podľa pasáže. Nový kit neznamená nový renderer, prepis ani celý samostatný projekt. Už existujúce balíky a komponenty sa vyberajú podľa konkrétnej funkcie a kompatibility s pripnutým runtime.

| Kit navrhnutý Adamom | Hlavná práca | Podklad, ktorý už máme |
| --- | --- | --- |
| Raw + titulky | Výber reči, rámovanie, čitateľné titulky, dokončená myšlienka | Jednoduché rozhovorové formáty; Diary of a CEO v `research/2026-11-06-youtube-editorske-formaty/HOTOVE_KLIPY.md` |
| Rapid cut | Obrazový rytmus, výrezy, detaily, zmeny dominantného záberu, prechody a zvukové akcenty | Sulan v `research/2026-11-05-husty-strih-zahranicne-referencie.md`; pohyb podľa konkrétnej reči |
| Fiki core | Existujúce pulzné žlto-biele titulky, identifikácia ľudí/predmetov, reakcie, kompozícia, B-roll | `brand/BRAND.md`, Čokolády, Vajanského, Pas, fiki.extra |
| Meme | Príprava prirovnania, samotná akcia, pointa, návrat na rečníka; návrat motívu v novej situácii | Mor ho!, Detroit, SOWA; konkrétne postupy v `research/konkurencia/zdroje/2026-11-06-top100-remotion-reel/POSTUPY_PRE_EDIT.md` |
| Explainer / grafy | Postupné porovnanie, čísla s jednotkami, zmena stavu, diagramy a podklady | Denko, ukazovateľ rizika, ceny/produkty, Devin Jatho a Steve Mould v existujúcich rozboroch |

Korpus už poskytuje konkrétne mechanizmy a latku. Nový blok zo 6. novembra obsahuje 100 príspevkov/36 účtov/415 beatov a nadväzuje na staršie detailné rozbory; nie je dôvod začínať nový všeobecný prieskum vkusu. Pri príprave kitu sa z existujúcich rozborov vyberú konkrétne príklady a prevedú na vykonateľné scény a rozhodovacie pravidlá. Rozsah audio/pohybovej kontroly jednotlivých referencií zostáva podľa pôvodnej evidencie.

## Trvalo dostupné pracovisko na subdoméne

Oficiálna dokumentácia podporuje [Remotion Studio na VPS](https://www.remotion.dev/docs/studio/deploy-server): bežiaci Node/Chrome proces poskytne náhľad aj render. Táto možnosť existuje od verzie 4.0.46, samotný hosting preto nevyžaduje automatický upgrade nášho runtime. Druhá cesta je [Remotion Player](https://www.remotion.dev/docs/player) v existujúcom pracovisku: kandidáti, kity, varianty, poznámky a náhľady nad spoločnou výrobou.

Pre XVADUR dáva zmysel súkromné pracovisko na existujúcej subdoméne alebo jej časti a samostatne bežiaca výroba. Aby práca pokračovala aj pri vypnutom Macu, server musí vykonávať tvorivé úlohy, prípravu médií aj render; samotné hostovanie statického náhľadu túto schopnosť nepridá. Remotion má [Node/Docker/serverové renderovanie](https://www.remotion.dev/docs/ssr); jeden trvalo bežiaci worker je konkrétna možnosť. Presný hosting a dimenzovanie zostávajú rozhodnutím po porovnaní nárokov, nie tvrdením o aktuálnom nasadení.

Pri Linuxovom vykonávateľovi treba nahradiť Apple MLX ASR kompatibilným adaptérom so zachovaním kontraktu prepisu a overiť dostupnosť médií aj nástrojov agenta. Nový cloudový worker sa nezamieňa s už overeným lokálnym behom. [Cloudflare Containers](https://www.remotion.dev/docs/cloudflare-containers) je ďalšia oficiálna cesta, ale jej pripojená ukážka je výslovne proof of concept bez hotovej fronty, autentifikácie a reportovania; nie hotová výrobná služba.

## Jednotka výroby

Epizóda má jeden zdroj, prepis a mapu obsahu. Kandidát je obsahová pasáž. Zvolená pasáž môže mať viac súrodeneckých spracovaní. Každé spracovanie má vlastný klip, brief, plán, materiálové použitia, render a tvorivé prijatie. Revízia opravuje jedno spracovanie; nie je ďalším samostatným štýlom.

Príklad identít, nie nové existujúce CLI prepínače:

```text
epizóda E / kandidát C01
  C01-reakcia / r1 → r2 (oprava)
  C01-situacia / r1
  C01-podklady / r1
```

Názvy predstavujú príklady rôznych editov, nie prijatú povinnú trojicu štýlov. Počet a spôsob spracovaní vychádzajú z obsahu a zadania dávky. Spoločný titulkový základ môže zostať zachovaný.

Pri modelovej výťažnosti 20 kandidátov: 2 spracovania = 40 videí z epizódy; 3 spracovania = 60 videí. Pre 600 videí jednej vetvy by to bolo 15, respektíve 10 takýchto epizódových dávok za mesiac. Je to aritmetika scenára, nie výrobná predikcia.

## Kde sa to pripojí k dnešnému systému

| Krok | Existujúci základ | Potrebné spojenie alebo doplnenie |
| --- | --- | --- |
| Zdroj a prepis raz | `import`, `prepis`, epizódové artefakty v `system/pipeline/store.ts` | Zdieľať tie isté zdrojové bajty a prepis vo všetkých klipoch; nevytvárať kópiu epizódy pre každý štýl. |
| Mapa a kandidáti | `analyzuj`, `episode-map.ts` | Zachovať kontext celku a deduplikáciu obsahových kandidátov. |
| Výber pasáže | `vyber`, `select()` v `runner.ts:150` | Uchovať skutočný pôvod výberu; AI návrh nie je automaticky Adamovo prijatie. |
| Rozdelenie na spracovania | Lokálne možno vybrať ten istý kandidát pod inými `clipId` | Doplniť explicitné skupinovanie pasáže a variantov za výberom. Automatický `cloud-editorial.ts:209–225` dnes vytvára iba jeden klip na hranice slov. |
| Tvorivý editor | `remotion-reel`, `brand/BRAND.md`, existujúce rozbory, nástroje Codexu | Editor musí skutočne načítať tieto vstupy, zvoliť obrazové spracovanie, získať a prezrieť materiál a pripraviť vykonateľný plán. Izolovaný textový plánovač túto prácu nevykonáva. |
| Odovzdanie plánu | `navrhni --plan JSON --brief JSON`, `saveAuthoredPlan()` | Použiť existujúci kanonický plán a slovné kotvy. Nepridávať druhú nezávislú časovú os. |
| Získanie materiálu | `uloha` s receipts; `workplace/media-tools/runtime.ts` | Prepojiť tvorivý výber s konkrétnym získaním súboru, výrezom a obsahovou kontrolou. Existujú imagegen/SFX vykonávače; všeobecný výber meme a B-rollu nie je uzavretý. |
| Skladanie a render | `materialy`, `nahlad`, Remotion, FFmpeg, `cyklus` | Hotové plány spracúvať z dávky; nezávislé materiálové úlohy môžu pokračovať počas renderu. |
| Kontrola a oprava | `kontrola`, `kritika`, `pripomienka`, `uprav --zmeny` | Povinne prejsť cez kontrolu presnej verzie. Opraviť konkrétny variant, zachovať fungujúci zvyšok a súrodencov. |
| Prijatie a publikácia | Existujúce prijatie a publikačné záznamy | Každé schválené spracovanie má vlastnú identitu. Publikačné retry nesmie vyrobiť ďalší post. Tento návrh nič nepublikuje. |

### Identita variantov a opakovanie práce

Nový spoločný kľúč pasáže má vychádzať z presného prepisu a usporiadaných intervalov/slovných kotiev. Samostatná identita spracovania pridáva identitu tvorivého variantu. Presný názov a uloženie nových polí treba uzavrieť pri implementácii, nie ich spätne vkladať do starých nemenných payloadov.

Selection obsahuje `clipId`, preto súrodenecké spracovania nemajú totožný Selection hash. Zdieľajú prepis a presné intervaly; každý dostane vlastný malý Selection záznam. Kompilátor už kontroluje jeho väzbu na plán (`system/pipeline/compiler.ts:26`).

Súčasný cloudový výber odvodzuje `clipId` iba z prepisu a hraníc slov (`workplace/worker/cloud-editorial.ts:209–215`). Rozvetvenie má prísť až po deduplikácii banky kandidátov. `batch.ts:46` prekrývanie iba hlási; zámerné súrodenecké spracovania sa majú rozpoznať podľa skupiny. Ochrana proti náhodnému duplicitnému jobu a opakovanému uploadu zostáva.

## Jeden editor, dva zdroje réžie

**AI návrh:** editor dostane pasáž s kontextom, konkrétne relevantné referencie, klientsky smer a zadanie variantu. Vyberá médiá podľa významu, pozerá skutočný interval a zostaví celý edit. Existujúce rozbory sa používajú priamo pri rozhodovaní; nevzniká nová všeobecná rešerš pred každým klipom.

**Adamova réžia:** Adam pozrie kandidáta a povie napríklad „pri tejto vete daj reakciu poroty, potom prejdi na celoplošný záber a pri pointe sa vráť“. Zachová sa pôvodný pokyn; editor ho prevedie na brief, presné slovné kotvy a materiálové požiadavky. Adam nemusí vytvárať JSON, hľadať súbory ani udávať každý technický parameter. Jeho pokyn má prednosť pred AI návrhom.

Oprava, nový variant a všeobecné pravidlo sú odlišné úmysly. „Tento GIF sem nesedí“ neoprávňuje globálne zakázať daný GIF alebo všetky meme. „Sprav aj iné spracovanie“ vytvorí súrodenca, neprepíše už hotový klip.

## Tvorivý editor a mediálne nástroje

Obmedzený analytický proces v `system/pipeline/model.ts:188–204` zostáva vhodný na štruktúrovanú analýzu. Nemá sa plošne odomknúť a vydávať za hotového editora. Samostatný vykonávací beh editora musí mať skutočne dostupné skilly, relevantné súbory a mediálne nástroje a odovzdať výstup cez existujúce autorské rozhranie.

V aktuálnom Codex chate môže agent vykonávať vyhľadanie, získanie, vizuálne prezretie, prípravu a uloženie materiálov cez existujúce úlohy. Pre beh bez chatu treba overiť rovnaké schopnosti v konkrétnom CLI profile.

V `workplace/media-tools/runtime.ts` už existujú `generate-image`, `generate-sfx`, `obtain-media`, `reuse-sfx`, `download-sfx`; nie je správne tvrdiť, že vykonávače chýbajú úplne. Automatický materiálový krok však potrebuje konkrétne `materialRoutes` a stiahnutie `obtain-media` je teraz obmedzené na `upload.wikimedia.org` (`runtime.ts:206–209`). Rozšírenie získavania meme/B-rollu a odovzdanie výsledku z tvorivého editora je konkrétna integračná práca. Existencia funkcie nie je dôkaz jej živého úspešného behu.

Vedľa tohto úzkeho adaptéra už `system/providers/resolver.ts` a `acquisition.ts` obsahujú širšie získavanie cez Commons, Imgflip, YouTube/yt-dlp a voliteľný Pexels, výskum, stiahnutie, výrez a normalizáciu. Túto existujúcu schopnosť treba pripojiť k tvorivému výberu a úlohám; netreba písať nový všeobecný downloader. Obrazové posúdenie resolvera používa päť vzoriek a nepredstavuje celý pohyb ani posluch. Pre samostatný media-tools imagegen je doložený capability probe a fixture, nie nový živý úspešný beh; ElevenLabs adaptér vyžaduje správne runtime prostredie. `workplace/media-tools/README.md` obsahuje tieto hranice.

Remotion zostáva hlavný renderer s existujúcim pripnutým runtime. FFmpeg pripravuje a spracúva médiá; yt-dlp získava vhodné zdroje. HyperFrames môže dodať konkrétnu vyrenderovanú vložku. Nemusí byť spustený pri každom klipe. Generovanie nových scén a médií sa robí podľa nápadu; pripravená knižnica nie je vstupná podmienka dávky.

## Dávka, súbeh a pravidelnosť

Koordinátor rozdelí zvolených kandidátov na konkrétne varianty a udrží ich stav. Každý editor má ohraničený klipový kontext a vlastní jednu rozpracovanú revíziu. Spoločná mapa epizódy a relevantné referencie sa zdieľajú; celá dávka sa nedrží iba v histórii jedného rastúceho chatu.

Aktuálny `system/runtime.json` už deklaruje dva klipové joby a jeden render. To je vhodné východisko pre skúšku vykonávajúceho editora, nie namerané optimum ani dôkaz dvoch samostatných tvorivých behov. Ťažké ASR, dekódovanie a render zdieľajú rozpočet stroja. Materiál pre ďalší klip sa pripravuje dopredu; čakanie jedného variantu nezastaví ostatné.

Výstup, ktorý už vznikol, sa po prerušení dohľadá podľa uloženého stavu. Neopakovať prepis epizódy, hotové platené generovanie ani celý nezmenený render. Pravidelná publikácia čerpá zo zásoby prijatých videí; nemusí čakať na tvorbu konkrétneho videa tesne pred termínom.

## Ako sa bude zlepšovať samostatnosť

Používateľovo „časom sa to naučíme“ sa prevedie na konkrétne uložené príklady: pasáž a kontext, pôvodný návrh, Adamov pokyn, výsledná oprava, prijaté použitie a jeho dôkaz. Pri novom klipe sa načítajú relevantné príklady, nie celé všetky historické chaty.

Existujúci `poucenie` ukladá rozsah use/asset/recipe/client a dôkazy z uzavretej opravy (`system/providers/learning.ts`, `system/schemas/learning.ts`). Je to prenos skúseností cez kontext; neznamená samovoľný tréning váh modelu. Nové všeobecné pravidlo nesmie vzniknúť z jednorazovej výhrady. Prínos sa overí ďalším podobným klipom.

## Konkrétne implementačné poradie

1. **Varianty dávky:** pridať spoločnú skupinu pasáže, samostatné identity spracovaní a ich briefs; overiť, že opakované spustenie nevytvorí ďalšie joby a oprava jedného variantu neprepíše druhý. Zdieľať zdroj, prepis a použiteľné pozorovania.
2. **Vykonávací editor:** pripojiť existujúci skill, referencie a nástroje ku konkrétnemu klipovému zadaniu; dodať autorský plán a reálne médiá existujúcou cestou. AI návrh a Adamova réžia používajú rovnaké rozhranie.
3. **Dokončenie a opravy:** získať render, vykonať skutočnú kontrolu, opraviť nález a odovzdať presný výsledok. Technické, snímkové, pohybové a zvukové dôkazy pomenovať pravdivo. Chýbajúca automatická schopnosť nemá predstierané prijatie.
4. **Súbeh a obnova dávky:** pripraviť ďalšie varianty počas renderu, obnoviť nedokončené kroky, zmerať čas a náklady vrátane Adamovej réžie. Ručne riadená tvorivá časť nebráni automatizovať vykonanie.
5. **Druhý klient:** doplniť Smer ako samostatnú klientsku konfiguráciu nad rovnakou výrobou. Dnešný runtime je explicitne fiki-only; premenovanie briefu samo nepridá druhého klienta. Smer preberie spoločné technické schopnosti a vlastný tvorivý smer.

Prvá malá integračná skúška má používať viac kandidátov a aspoň dva súrodenecké edity jednej pasáže, aby preukázala práve nové zadanie. Následná celá epizódová dávka preverí objem. Počet zdrojových pasáží, samostatných hotových spracovaní a potvrdených publikácií sa eviduje oddelene; všetky prijaté štýlové spracovania sa rátajú do Adamovho cieľa 1 200 videí.
