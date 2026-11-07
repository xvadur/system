# Rozhodovanie o edite Fikiho klipu

**Novšie zadanie z 2. novembra 2026:** aktuálny návrh autonómneho výberu, agentovej slučky a obsahom riadeného hľadania/generovania je v [priebežných dohodách](XVADUR_CLIPPING_SYSTEM_DOHODY.md). Tieto novšie rozhodnutia majú prednosť pred nižšími historickými formuláciami o povinnom Adamovom výbere a knižnici ako povinnom prvom kroku. Nižší dátum a dôkazy zostávajú historickým kontextom; nejde o potvrdenie implementácie novej iterácie.

Dátum: 25. 10. 2026. Stav: **plánovaný pracovný predpis pre Codex, súčasť hlavného plánu**. Tento súbor nezavádza nové kanonické kontrakty, nemení implementáciu a neoznačuje žiadnu etapu za dokončenú. Nevznikol kód, render ani nové médium.

Potvrdený režim od Adama 25. októbra: **celý postup funguje v Codexe**. Codex používa dostupné nástroje a lokálne CLI ako vykonávaciu vrstvu. Samostatný externý API orchestrátor nie je cieľom tohto plánu.

## 1. Čo má táto časť systému dokázať

Zo zvolenej pasáže pripraviť konkrétny, významovo súdržný edit bez toho, aby Adam musel agentovi priebežne vysvetľovať každú vetu a vyberať každý GIF. Výber pasáže a finálne tvorivé prijatie zostávajú Adamovi. AI zodpovedá za analýzu, varianty, odporúčanie, získanie/výrobu materiálov, realizáciu a vlastnú konkrétnu kontrolu.

Úspech sa neposudzuje počtom efektov ani tým, že encoder skončil. Výsledok musí mať zrozumiteľný úvod, potrebný kontext, vývoj a pointu; obraz a zvuk majú podporovať konkrétnu reč. Agent dokáže vysvetliť, prečo niečo pridal, ponechal bez efektu alebo odstránil. Prijaté riešenie sa dá dohľadať a účelne použiť znova.

Základ už existuje v `Selection`, `CreativeBrief`, `SemanticMoment`, `EditPlan`, `AssetRequest/Record`, `RecipeRecord`, `UseRecord`, `FeedbackRecord` a `ReviewRecord`. Návrh nižšie tieto pojmy používa ako cieľové väzby; **netvrdí, že ich dnešné vykonávanie už napĺňa všetky opísané tvorivé úlohy**.

## 2. Väzba na hlavný plán

Táto príloha je pracovný predpis pre Codex k etapám P3–P5 [hlavného plánu](../PLAN_IMPLEMENTACIE.md). Nedefinuje ďalší nezávislý systém. Pôvod prevzatých mechanizmov a ich hranice sú v [zdrojovej matici](PODKLADY_PLANU_2026-10-25.md). Výrobu podľa tohto predpisu bude vykonávať Codex s existujúcimi lokálnymi nástrojmi; tento dokument ju ešte neimplementuje.

## 3. Editoriálna formula: zámer → možnosti → pokus → dôkaz → rozhodnutie

### A. Celý klip pred jednotlivými efektmi

Editor nad prijatou pasážou pomenuje jednou vetou: **čo sa na začiatku otvorí, čo musí divák pochopiť a kam sa má význam posunúť na konci**. Zistí, čo je už v pôvodnom obraze/zvuku a nepotrebuje novú ilustráciu. Označí tvrdenia, citácie, iróniu, neistotu a potrebný kontext.

Pracovný hlasový strih sa môže navrhnúť, no nová hranica, poradie alebo vynechanie slova sa stáva aktívnym až cez príslušné Adamovo rozhodnutie/Selection. Nová fotografia, animácia či zoom nemení reč.

Výstup: stručný oblúk klipu, vstupný a výstupný význam, hook/payoff, zamknuté rozhodnutia a otvorené redakčné problémy. Nemusí vzniknúť nový samostatný dokument pre každú drobnosť; údaje majú stabilnú identitu a čitateľný prehľad.

### B. Rozdelenie na významové beaty

Beat je malý krok argumentu alebo situácie, nie každá titulková strana. Nesie zdrojové slová/kontext, funkciu, želaný divácky účinok, dĺžku na pochopenie a vzťah k susedným beatom. Typická funkcia: otázka, orientácia, tvrdenie, vysvetlenie, dôkaz, kontrast, reakcia, stupňovanie, pointa alebo návrat.

Následne sa systematicky posúdia možnosti. **Posúdenie všetkých možností neznamená povinné použitie všetkých možností.** Nevybrané kanály môžu mať krátke odôvodnenie na úrovni beatu, nie sedem prázdnych povinných formulárov.

| Možnosť | Otázka pred rozhodnutím | Výstup pri použití | Platný dôvod nepoužitia |
|---|---|---|---|
| Hook | Aký konkrétny prísľub udrží prvú vetu a čo ho neskôr splní? | Pôvodná veta/gesto, obrazový prísľub, moment návratu/payoff. | Úvod už sám obsahuje silnú otázku; nový nápis by ju predbehol. |
| Meme/reakcia/humor | Na čo presne reaguje; je absurdnosť už pripravená; stihne sa reálna akcia GIFu? | Setup → reveal → hold → return podľa potreby, konkrétna akcia a trim. | Reakcia by označovala emóciu, ktorú veta ešte nevytvorila, alebo by zmenila tón. |
| B-roll/dokument/archív | Potrebujeme identifikovať, doložiť, ukázať situáciu alebo ilustrovať? | Typ dôkazu/ilustrácie, zdroj, konkrétny výrez a použiteľné okno. | Pôvodný záber už ukazuje potrebný podnet; nová vložka by ho duplikovala. |
| Vlastná scéna/imagegen | Je dôležitý vzťah, fyzická akcia alebo premena, ktorú hotový asset nevysvetlí? | Nadväzujúce stavy, výtvarný svet, rekvizity/postavy, slovné zásahy. | Rozpoznateľný reálny dokument alebo tvár vysvetlí vec priamo. |
| Zvuk/ticho | Ktorá konkrétna akcia alebo dôraz si pýta aký zvuk; kde má zostať priestor? | Súbor, trim, nábeh/tail, gain ako pracovný návrh, anchor a rozsah posluchu. | Hlas alebo pauza už vytvárajú dôraz; ďalší úder by ich zakryl. |
| Tvár/crop/zoom | Kedy je nositeľom významu Fikiho reakcia, gesto alebo prednes? | Bezpečná kompozícia, štart/cieľ pohybu a slovná kotva. | Plný detail je už dostatočný; ďalší zoom nemá nový účel. |
| Prechod | Aký vzťah spája dva stavy: pokračovanie, kontrast, odhalenie, zmena času či návrat? | Konkrétny pohyb/strih, objekt kontinuity, trvanie, prípadný zvuk. | Tvrdý strih vyjadrí vzťah jasne; ozdobný prechod spomalí pointu. |
| Dramatický dôraz | Kde má divák čakať, zmeniť názor, dostať úder alebo vydýchnuť? | Hierarchia 1–3 dominantných momentov podľa klipu a čitateľné medzistavy. | Nie každá veta má byť vrchol; rovnaké údery by zrušili stupňovanie. |

### C. Výber nápadu a overiteľná hypotéza

Na dôležitom/neistom mieste vzniknú zmysluplne odlišné možnosti, nie povinné tri varianty všetkého. Odporúčaná možnosť má vetu: „Keď zaznie X, divák uvidí Y, aby pochopil/pocítil Z; fungovanie overíme podľa W.“ Agent vyberie možnosť v rámci briefu, zaznamená dôvod a otvorenú neistotu. Adam nedostáva otázku ku každej bežnej pomocnej voľbe.

Výsledok: beatový plán s kotvami, konkrétnymi obrazovými a zvukovými udalosťami, návratom k Fikimu, požiadavkami na materiál a overením. Povinný moment má realizáciu alebo viditeľný otvorený problém; čistý A-roll je riadne rozhodnutie.

## 4. Získanie médií, imagegen a autorské scény

Prvé hľadanie ide cez existujúcu knižnicu vrátane minulých použití a zamietnutí. Pri chýbajúcom obsahu nasleduje účelné hľadanie a porovnanie relevantných kandidátov. Register musí zachovať zamýšľaný obsah aj skutočne pozorovanú akciu: rozpoznateľnosť, začiatok akcie, dĺžka, crop, pôvod a dôvod voľby. Dvojsekundový názov „shock“ bez pozretia obsahu nie je riešenie.

Imagegen je jedna výrobná cesta: transparentný objekt/postava, ilustrácia prostredia, podklad alebo výtvarne zladená séria. Brief určí účel, referencie, kompozíciu, pomer strán, požadovanú transparenciu a čo sa musí medzi scénami zachovať. Pri editovaní sa existujúci cieľ najprv pozrie. Výstup musí byť reálny obrazový súbor, skontrolovaný v cieľovej kompozícii; samotný prompt sa za získaný asset neoznačí. Generovaná ilustrácia nesmie predstierať historický záber, presný dokument alebo identitu. Táto tvorba sa teraz len plánuje, nespúšťa.

Autorská motion scéna vzniká z nápadu, nie z povinného zoznamu kariet. Môže kombinovať React/SVG, lokálne fotografie/GIFy, imagegen materiály a vlastnú časovo riadenú animáciu. Potrebuje:

- stavy a akcie: čo zostáva, čo pribúda, čo mení funkciu a kedy príde pointa;
- jeden výtvarný svet podľa potreby: postavy, rekvizity, perspektíva, mierka, farba, kamera;
- stabilné scene/element IDs a slovné/koncové kotvy;
- editovateľný zdroj, presné verzie a manifest závislostí;
- náhľad v niekoľkých časoch vrátane premeny, nie iba peknú záverečnú snímku.

Čas určuje celú snímku; pri prehrávaní sa svojvoľne nesťahujú médiá. Nová autorská cesta sa v pláne oddelí od dnešných možností `SceneSpec`; nemožno ju vyhlásiť za implementovanú len preto, že sa dá napísať ďalší preset. Prvé prenosy zachovajú vlastný runtime a pripnutý Remotion 4.0.529. Nepotrebuje sa vymieňať renderer za framework z videa.

## 5. Kritika a opravná slučka

Autor odovzdá konkrétny návrh s tým, čo má v každom dôležitom mieste fungovať. Nezávislá kritická rola má prístup k reči/kontextu, plánu, použitým materiálom a skutočnému náhľadu. Nemá hodnotiť iba autorov slovný opis. Roly nemusia znamenať trvalo oddelených desať agentov; hybridný orchestrátor ich rozdelí podľa náročnosti.

Kontrola má vrstvy:

1. **Význam:** zachovaný argument/irónia, adekvátny kontext, pravdivý vzťah čísel, označená ilustrácia a citácia. Grafika nesmie pridávať tvrdenie ako externý dôkaz.
2. **Réžia:** prísľub a pointa, príprava reakcie, stupňovanie, nadväznosť, priestor na rozpoznanie, návrat k tvári, nadbytočné opakovanie.
3. **Skutočný obraz/pohyb:** správny obsah assetu, funkčná akcia vo vybranom trime, čitateľnosť, crop, kolízie, priebeh medzi stavmi.
4. **Skutočný zvuk:** hlas, pauzy, nástupy/taily, primeranosť úderov, čitateľnosť reči. Meranie hlasitosti alebo prepis nie sú posluch.
5. **Technika:** lokálne médiá, decode, časovanie, správne rozmery a presná revízia. Technický pass neuzatvára predchádzajúce vrstvy.

Nález obsahuje revíziu, beat/event/prvok/čas, pozorovanú chybu, dôkaz, dôsledok pre diváka a požadovaný smer opravy. Jeho oprava vedie na novú revíziu, potom na kontrolu dotknutého miesta s okolím. Po zmenách sa znovu pozrie celý klip. Prijatá nedotknutá vrstva sa neprepisuje.

Slučka sa neopakuje pre vymyslené skóre kvality. Pokračuje pri konkrétnej nevyriešenej chybe alebo preukázateľnom zlepšení; ak sa opakuje ten istý neúspešný nápad, zmení sa treatment. Otvorená tvorivá neistota sa predloží s reálnym kandidátom, dôvodom a odporúčaním.

## 6. Výstupy a overenie etáp tejto schopnosti

Nasledujúce body sú kontrolné výstupy jedného editačného priechodu v P3–P5; nie sú ďalšie etapy implementácie. Ich názvy nezakladajú existujúce CLI príkazy ani nový povinný súbor pri každej akcii. Rozsah produkčného overenia určuje P7 hlavného plánu.

| Etapa | Konkrétny výstup | Kritérium overenia pred ďalším krokom |
|---|---|---|
| F0: redakčný kontext | Odkaz na prijatú Selection/prepis, oblúk, prísľub/pointa, tvrdenia a uzamknuté požiadavky. | Dá sa vysvetliť celý klip bez izolovaných úryvkov; neistoty a návrh zmeny reči sú viditeľné. |
| F1: beatový treatment | Významové beaty, konkrétne zvolené/nepoužité prostriedky, anchor, očakávaný účinok, spôsob skúšky. | Každý použitý efekt má funkciu; divák má čas pochopiť obraz; plán nemá nezdôvodnené resety. |
| F2: vyriešené materiály a návrh scény | Reálne assety/kandidáti, pozorovaná akcia/trim, pôvod, prípadne výtvarný návrh a autorský zdroj. | Súbor existuje; identita a obsah sedia; prijateľná dĺžka/crop; ilustrácia sa nemýli s dôkazom. Prompt bez výstupu ostáva otvorený. |
| F3: lacný konkrétny náhľad | Kľúčové snímky, časovo ovládateľná kompozícia, potrebný krátky AV úsek. | Overené nástupy, medzistavy a pointa, nielen statický výsledok. Kritický nález má dôkaz a opraviteľný cieľ. |
| F4: oprava a celý kandidát | Nová revízia, záznam vyriešených nálezov, celý prehrateľný klip, rozsah posluchu/technických kontrol. | Oprava funguje s okolím a nepoškodila prijaté vrstvy; neoverené vnímanie je výslovne otvorené. |
| F5: tvorivé prijatie a poučenie | Adamovo rozhodnutie ku konkrétnej revízii, evidované použitia, lokálne/prenosné poznatky. | „Prijaté“ je skutočné Adamovo rozhodnutie; technická kontrola, render a publikácia majú oddelené stavy. |

Preukázanie schopnosti: nový Adamom vybraný moment, agent sám pripraví a dotiahne spracovanie, Adam posúdi celý kandidát. Evidovať počet a povahu potrebných režijných zásahov. Jedna úspešná kompozícia ukáže schopnosť; opakovanie na odlišnom type momentu overí prenos. Počet a rozmanitosť reálnych overení určuje P7 hlavného plánu; tvorivá kvalita sa neurčuje univerzálnym percentuálnym skóre.

## 7. Čo ukladať a čo sa z výsledku môžeme naučiť

| Vrstva poznania | Čo zaznamenať | Čo sa nesmie automaticky zovšeobecniť |
|---|---|---|
| Vlastnosť assetu | Skutočná činnosť, in/out, rozpoznateľný prvý frame, čitateľnosť/crop, pôvod, neistota. | Názov poskytovateľa alebo hľadania nie je obsahová kontrola. |
| Recept/postup | Účel a vhodné spúšťače, kroky/parametre, závislosti, ukážka a obmedzenia. | Jeden úspešný vzhľad nie je povinný formát všetkých ďalších klipov. |
| Konkrétne použitie | Veta/kontext, prečo sa zvolilo, čo sa pozorovalo, prijatie či zamietnutie a dôvod. | To, že sa asset hodil k jednej irónii, neznamená vhodnosť pri každom rovnakom podstatnom mene. |
| Adamov vkus | Presná pripomienka a pôvod, rozsah: tento event/klip, klientsky smer alebo výslovne trvalá preferencia. | „Adamovi sa páčil Gordon tu“ sa nemení na globálne „vždy daj Gordona do hooku“. |
| Prenosná remeselná chyba | Napríklad pointa predbehla slovo; druhá skupina vyzerala ako ďalších 1000; medzery kolidovali pri poskoku. | Pri neznámom dôvode zamietnutia sa nevymýšľa vysvetlenie. |
| Výsledok publika | Platforma/účet, čas merania a od zverejnenia, views; retencia podľa úsekov, ak je dostupná; kontext uploadu. | Views samy nepreukážu účinok GIFu, náročnosti editu ani pravidelnosti publikovania. Bez porovnateľných dát je to hypotéza. |

Knižnica sa má učiť aj negatívne: zamietnutý kandidát a dôvod zostávajú dohľadateľné. Záznam na začiatku ďalšej výroby musí vedieť ovplyvniť hľadanie a rozhodnutie; samotné uloženie poznámky bez následného použitia nie je uzavretá učiaca slučka.

## 8. Vyplnený príklad A — Vajanského: historická rekonštrukcia rozhodnutí

**Status:** ide o čítanie zachovanej výroby r7–r12, nie nový návrh ani súčasné sledovanie celého videa. Finál má 21 s pri 25 fps: 16 s hlasovej zostavy a 5 s CTA. 44 časovaných slov je uložených v [word-captions.motion.r0006.json](<../fiki/epizody/vallo-2026-10-21/praca/vajanskeho-r1/word-captions.motion.r0006.json>). Tieto staršie word captions nesú vlastný vtedajší draft status; neskoršie prijatie sa dokladá stavom r12.

**Oblúk, naša redakčná interpretácia:** rozhorčená otázka o účele cyklopruhu → konkrétne miesto a kontrast čakania/prázdneho pruhu → časová frustrácia → úderný hodnotiaci záver. Fotografia/mapa orientujú; samy nedokazujú Fikiho tvrdenie o polhodine alebo neprítomnosti bicyklov.

| Beat a hlasová kotva | Historické riešenie | Funkcia/hypotéza a čo sa kontroluje |
|---|---|---|
| 0–2,4 s: úvodná otázka; „cyklopruh“ od 1,12 s | Otvárací reveal, Fiki, Gordon 1,2–2,4 s. | Podčiarknuť už vyslovené rozhorčenie. Reakcia nesmie predbehnúť pochopiteľnú otázku; tvár a slová musia zostať čitateľné. |
| 2,4–7,88 s: „Vajanského“, „v zápche“, „vedľa teba… cyklopruh“ | Mapa 2,4–3,72; skutočná archívna ulica 3,72–4,48; side-eye 4,48–5,24; detail ulice/cyklopruhu 5,24–7,88. | Orientácia → situácia → reakcia → konkrétny predmet porovnania. Mapa bola skrátená z 5,48 s na 1,32 s. Overovať vzťah k miestnej identite a nepredstierať dopravné meranie. |
| 7,88–11,44 s: „pol hodinu… v tej zápche“, „neprejde ani jeden bicykel“ | Office Space vodič 7,88–9,72; Mr Bean hodinky 9,72–11,44. | Dve fázy frustrácie: hnev a čakanie. Trim musí obsahovať skutočnú akciu; hodinky ilustrujú čas, nie historický dôkaz. |
| 11,44–16 s: finálny hodnotiaci výrok | Tri kopy a stupne poškodenia erbu: 12,2 / 13,6 / 15,0 s. Tretí úder na „zničenie“. | Príprava → trhlina → čiastočný rozpad → plný zásah. Zvuk má rovnaké kotvy. Skontrolovať, že eskalácia je viditeľná a záver ostáva Fikiho satirickým hodnotením. |
| 16–21 s | CTA podľa prijatého konkrétneho klipu. | Nezamieňať dnešný plán s automatickým prijatím historickej CTA pre všetky nové klipy. |

**Doložené Adamove zásahy:** r7 eviduje odstránenie druhého opakovania polhodiny; ponechanie Gordona po pochvale prvého GIFu; nahradenie cudzej dopravy skutočnou mapou; odstránenie horného FIKI/KOMENTÁR; zachovanie opening reveal/prechodov/word animácie. [STAV.r0007](<../fiki/epizody/vallo-2026-10-21/praca/vajanskeho-r1/STAV.vajanskeho.r0007.json>).

**Čo je doložené bez jasného pôvodcu nápadu:** r8 skrátenie mapy a skladba; r10 tri progresívne kopy a presné zvuky. Neprisudzujeme ich samostatnému agentovi ani Adamovi bez ďalšieho dôkazu. [r8](<../fiki/epizody/vallo-2026-10-21/praca/vajanskeho-r1/STAV.vajanskeho.r0008.json>), [r10](<../fiki/epizody/vallo-2026-10-21/praca/vajanskeho-r1/STAV.vajanskeho.r0010.json>).

**Poučenie:** prenosné sú dramaturgia trojfázového zásahu, krátka miestna orientácia a oddelenie archívu od ilustrácie. Gordon a konkrétna bojová metafora zostávajú prijatým použitím v tomto klipe, nie univerzálnou formulou. Finálny r12 má technické pass a doložené Adamovo prijatie/pokyn na publikovanie, ale `listening: not_listened`; neoznačujeme ho za dôkaz samostatného úplného senzorického hodnotenia AI. [r12](<../fiki/epizody/vallo-2026-10-21/praca/vajanskeho-r1/STAV.vajanskeho.r0012.json>).

## 9. Vyplnený príklad B — nový hypotetický moment s animovanou situáciou

**Status:** syntetický príklad, žiadny vybraný Fikiho úsek, prepis, faktické tvrdenie ani zadaná výroba. Pracovné relatívne časy sú iba návrh tempa. V reálnom zdroji sa nahradia wordId a overeným prednesom; nevymýšľame preň zdrojové kotvy.

**Syntetická reč:** „Traja ľudia postavia dom. Štvrtý príde, keď treba dotiahnuť poslednú skrutku. Potom stojí pred kamerou a hovorí: celé som to postavil ja.“

**Oblúk:** divák najprv vidí skutočný pomer práce, potom drobný posledný zásah, nakoniec absurdné privlastnenie zásluh. Hlavný vtip je vzťah medzi vykonanou prácou a tvrdením. Nepridávame vopred „podvodník“ alebo politickú identitu.

| Pracovné okno / beat | Zvolené spracovanie a materiály | Vedome nepoužité možnosti | Overiteľná hypotéza |
|---|---|---|---|
| približne 0–3,5 s: „Traja… postavia dom“ | Fiki otvorí vetu; horná scéna odhalí rovnakých troch staviteľov pri jednom dome. Rýchlo, ale čitateľne sa doplnia hlavné časti. Jemné dva stavebné zvuky; kamera zostáva stabilná. | Úvodný cudzí meme: ešte nemáme pripravený dôvod na reakciu. Dramatický whoosh ku každému slovu by zrovnal dôležitosť všetkých akcií. | Divák rozpozná, že väčšinu práce urobili títo traja, ešte pred príchodom štvrtého. |
| približne 3,5–7 s: „Štvrtý príde… poslednú skrutku“ | Tá istá scéna. Štvrtá postava príde do hotovej situácie a urobí jediný drobný pohyb nástrojom; jeden krátky klik na „skrutku“. Ostatní aj hotový dom zostávajú viditeľní. | Nová fotografia iného domu; číslo „99 %“ bez podkladu; zoom do tváre, ktorý by skryl pomer práce. | Bez vysvetľujúceho odseku sa dá odlíšiť malý posledný zásah od predchádzajúcej práce. |
| približne 7–10 s: „Potom stojí pred kamerou“ | Štvrtý sa presunie pred rovnaký dom; do popredia vstúpi ilustračná kamera. Pôvodní stavitelia ostanú v zadnom pláne, mierne ustúpia v dominancii. | Samostatná generická PR karta bez väzby na dom; nový prechod pre každé podstatné meno. | Presun vyjadrí privlastnenie viditeľnosti, pričom divák nestratí pamäť situácie. |
| približne 10–13 s: „celé som to postavil ja“ | Na „ja“ krátky push-in štvrtého alebo návrat na Fikiho podľa prednesu; v priestore obrázka sa objaví malá „MOJA PRÁCA“ značka, ktorá komicky prisvojí aj dom. Jediný hlavný zvukový zásah. | Povinný potlesk + Snoop + laugh track naraz; tie by opakovali už hotový vtip. Ako záložný variant možno skúsiť krátky Snoop až po vete, ak prednes potrebuje dobeh. | Pointa príde pri vyslovení, nie pred ním. Je čitateľná aj bez meme znalosti a pôsobí ironicky, nie ako potvrdenie autorstva. |

**Výtvarná výroba:** pred výrobou zvoliť jeden výtvarný smer a náhľad celého javiska. Varianta A: autorská SVG/React scéna s konzistentnými postavami a domom. Varianta B: imagegen vytvorí ilustrované pozadie a transparentné postavy/rekvizity v jednotnom štýle; následný pohyb a vrstvenie riadi autorská kompozícia. Nevyrobíme štyri nezávislé obrázky, v ktorých sa mení dom, oblečenie a perspektíva. Návrh by mal podľa dostupnosti médií odporučiť A alebo B; generovanie sa teraz nespúšťa.

**Prvý pokus:** kľúčové snímky pred príchodom štvrtého, po jeho drobnom zásahu, pri prevzatí kamery a na slove „ja“; navyše náhľad prechodu medzi poslednými dvoma stavmi. Ak divák neprečíta rozdiel práce, opravuje sa mierka alebo dej; nepridáva sa len ďalší nápis.

**Kritika a oprava:** kritik môže nájsť „štvrtý je viditeľný už pri stavbe, preto vyzerá ako spoluautor“. Nález sa viaže na event príchodu; oprava ho odloží až na príslušnú vetu, bez prepisovania hlasu a zvyšku sveta. Po oprave sa pozrie úsek s okolím a celý klip s hlasom.

**Poučenie:** prenosný recept je „veľká práca → drobný posledný krok → privlastnenie zásluh“, s kontinuitou jedného predmetu a presným odhalením. Konkrétny dom, kamera, farba a dĺžka sú parametre použitia. Adamova prípadná preferencia ilustrovaných postáv sa uloží s rozsahom. Hypotetické vyššie views sa teraz nevymýšľajú.

## 10. Prečo sa to opiera aj o Pas a Električku

Pas je doložený tvorivý smer: Adam prijal „Fiki rozpráva a hore sa odohráva animovaný príbeh“, ale nezrozumiteľnú ulicu z čiar žiadal opraviť. R2 nahradila izolované symboly konzistentnou ulicou, postavou, zohnutím/zdvihnutím pasu a fyzickým podaním cez policajný pult. Animácia r2 bola prijatá; neskoršie titulky r4 sa opravili samostatne bez zmeny prijatých scén. Toto je vzor pokračujúcej situácie a izolovanej opravy, nie len vyššej hustoty overlayov. [Adamov feedback](<../fiki/epizody/105/praca/pas-pilot/ADAM_2026-10-18.md>), [plán r2](<../fiki/epizody/105/praca/pas-pilot/PLAN.r0002.md>), [realizácia r4](<../fiki/epizody/105/praca/pas-pilot/REALIZACIA.r0004.md>), [finálne tvorivé prijatie](<../fiki/epizody/105/praca/pas-pilot/DOKONCENE_2026-10-18.md>). Starší záznam prijatia nepreukazuje sám neskorší render/upload ani posluch AI.

Električka ukazuje konkrétnu režijnú prácu: Adam žiadal návrat Fikiho pred SpongeBobom, odlišné skutočné PR fotografie, rýchle významové reakcie a čitateľný neorezaný Snoop. [BASELINE r12](<../fiki/epizody/vallo-2026-10-21/praca/refine-r12/BASELINE.r0012.json>). Drahá scéna domu sa napokon vynechala: 71,16 s → 48 s, používateľ zvolil verziu bez domu. [r14 porovnanie](<../fiki/epizody/vallo-2026-10-21/praca/house-r14/REVIEW.r0014.json>), [r15 prijatý základ](<../system/workshops/vallo-2026-10-21/creative-r15/source-manifest.r0015.json>). Hodnota remesla neospravedlňuje nadbytočnú scénu; aj nový hypotetický dom vyššie sa musí zhodnotiť voči celku.

Magistrát je dôkaz chybného významového podania aj pri dobrých materiáloch: Adamov feedback „assety máš dobre ale nedáva to zmysel“; prvá oprava grafov potom stratila pohyb/zvukovú energiu. Kritik musí kontrolovať význam aj réžiu súčasne. [ASTRA brief](<../fiki/epizody/vallo-2026-10-21/praca/magistrat-astra-r10/ASTRA-BRIEF-r10.md>), [ďalšia revízia](<../fiki/epizody/vallo-2026-10-21/praca/magistrat-astra-r10/ASTRA-REVIZIA-r10-3.md>).

## 11. Vykonanie v Codexe

Pri stavbe sa tento postup zabalí do jedného projektového pracovného návodu pre Codex s odkázanými formulármi a nástrojmi. Pred novou prácou Codex načíta uložený stav epizódy/klipu a príslušný LibraryContext; po každom kroku uloží rozhodnutie a skutočný výsledok. Adam nemá ručne spúšťať jednotlivé technické operácie ani prepájať súbory.

Krok sa považuje za vykonaný iba s konkrétnym výsledkom alebo viditeľným otvoreným problémom. Záznam o plánovanom imagegene nie je obrázok; zdrojový kód nie je prezretá animácia; technický pass nie je tvorivé prijatie. Implementačné etapy, závislosti a celkové kritériá sú výhradne v hlavnom pláne P0–P7.
