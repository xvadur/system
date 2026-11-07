# Nezávislá kontrola nočného výskumu

Kontrola vykonaná 28. 10. 2026 v rámci už zadaného nočného výskumu. Je to kontrola dôkazov a primeranosti záverov, nie druhé kompletné hodnotenie všetkých 120 videí. Nevznikol nový render, získanie ďalších konkurenčných videí ani zmena runtime alebo STAV.

**Výsledok:** v preverenej reprezentatívnej vzorke sa nenašlo tvrdenie o vykonanom posluchu, vymyslený hotový čistý asset ani zásadná zámena výskumného paddingu za export autora. Konkrétne grafické a kompozičné pozorovania nižšie majú oporu v otvorených obrazoch. Našiel sa ďalší sémanticky nepoužiteľný surový ASR napriek prítomnosti písmen. Preto sa automatický počet prepisov nesmie premeniť na počet overených významov.

## Rozsah skutočne vykonanej QA

- **12 rôznych klipov** bolo opätovne porovnaných so skutočne otvorenými obrazovými dôkazmi a príslušným surovým ASR: rootov rozbor, naše kontrolné videá, ZLE, bloky B/C/E/F a skorší fiki.extra.
- V tomto QA priechode bolo skutočne otvorených **19 obrazových hárkov alebo sekvencií klipov a dve samostatné fotografie NASA**, spolu 21 obrazov. Nie všetky boli celé source-frame extrakcie; časové hranice sa čítali podľa príslušného manifestu.
- Rozbory vlastných blokov A/D sa nanovo nehodnotili. Skorší fiki.extra pôvodne písal tento istý analytik; jeho preverenie preto nie je nezávislé druhé autorstvo. Zvyšné vybrané rozbory pochádzajú od iných analytikov/roota.
- Snímky, ASR, manifesty a správy sa čítali ako dôkazy. **Zvuk nebol vypočutý a celé videá sa súvisle neprehrali.** Táto QA nevypĺňa AV medzeru.
- Pri finálnej kontrole existovalo **22 správ v rozbory/** a všetkých **568 lokálnych Markdown odkazov** smerovalo na existujúce cesty. Pri kontrole sa odstránil iba koncový riadkový lokátor `:číslo` a prípadný fragment. Toto overuje existenciu odkazu, nie správnosť každého tvrdenia v každej správe.
- Rootov [frajer.fiki.proof.json](rozbory/frajer.fiki.proof.json) mal všetkých desať zapísaných hashov hárkov zhodných so súbormi. Deväť listových seekov je zapísaných v samostatnej [evidencii](evidence/blok-root/list-cues/sampling.json); skutočne otvorený zložený hárok obsahuje všetkých deväť.
- V čase uzavretia existovali aj všetky tri nové F správy a ich proof súbory. Vzorkovaná QA F pokrýva dve konkrétne videá fiki.nahrad, nie každé video F.

## 1. P2 — Minimum písmen nie je overená použiteľnosť ASR

**Dotknutý klip:** TikTok fiki.unrealized / emus_iik, `7689781792898960662`, jedlo v natívnom širokom formáte.

[Obrazový prehľad](evidence/zle-detail/7689781792898960662/overview.jpg) ukazuje pri 0,5–1 s „strašne veľký kus“, pri 2,5 s „skoro som sa zadusila“ a pri 15 s „to je extrém“. [Surový ASR](prepisy/5559c2a158ede0804d09f584e8fc03676e2299f5b416d845dc3aaab2a4f3633d.json) namiesto toho deväťkrát opakuje presnú vetu „Čo je to naši.“ a obsahuje podobné nespoľahlivé fragmenty aj počas záverečnej CTA. Má 11 segmentov a 101 abecedných znakov; to nestačí na obsahovú rekonštrukciu.

[prepisy.json](prepisy.json) ho eviduje ako `orientationCandidate: true`, ale zároveň správne ponecháva `semanticAccuracyVerified: false` a `listening: not_listened`. **Samotné tieto metadáta neklamú o overenej presnosti.** Chybná by bola následná syntéza „119 použiteľných prepisov“ iba z počtu súborov s písmenami. Už máme konkrétny protipríklad.

**Správne vyjadrenie rozsahu:** základná 120-položková vzorka má 120 surových ASR záznamov; 119 prešlo iba minimálnou kontrolou prítomnosti písmen. Dodatočné recovery súbory sa vedú osobitne. Tento počet nie je sémantická akceptácia. Pri tomto jedle zostáva celý slovný význam otvorený a existujúci ZLE rozbor ho tak správne uvádza.

**Odporúčanie:** zachovať pôvodné ASR, pridať sémantický dôvod nepoužiteľnosti pri tomto ID a pred výrobným strihom opraviť prepis alebo vykonať posluch. Táto QA nespúšťala náhradný ASR.

Pôvodný interpunkčný neúspech `fikiclips1/7699900569116249366` tým nie je spätne označený za použiteľný. Jeho nový recovery je samostatný podklad spracovávaný rootom; nebol predmetom tejto QA.

## 2. P3 — ZLE má úplné vizuálne pokrytie, nie rovnaké obsahové overenie ako každá TOP vzorka

Táto pripomienka zachytáva stav pri prvom QA čítaní. Následný doplnkový ASR priechod ZLE sa má hodnotiť podľa jeho vlastného uloženého rozsahu; neprepisuje pôvodný obsah tejto kontroly na vykonaný posluch.

[Kontrola ZLE](rozbory/kontrola-zle.md) poctivo uvádza vizuálny rozsah a viacero slovných oblúkov ponecháva otvorených. Pri vybranom `qUFvPLP0wQs` však už existuje [orientačne čitateľný ASR](prepisy/159a2af64731620711e73ed114c6d7fd1901b14320705bcece85cedb805ba81c.json): úvodný komentár → citovaný podnet → spresňujúca odpoveď → záver. Viditeľné červené titulky a zmena osoby na [strane 1](evidence/zle-detail/qUFvPLP0wQs/page-1.jpg) tento základný oblúk podporujú.

Nie je preto správne premeniť „neoverené“ na slabé skóre hooku, kontextu alebo pointy a potom ho sčítať proti TOP rozborom, ktoré ASR čítali. Ide o **rozdiel rozsahu**, nie o zistenie, že ZLE správa obsahuje nepravdivý obrazový opis. Pri jedle je naopak ASR nepoužiteľné, takže tam je otvorený význam nevyhnutný.

**Odporúčanie pre syntézu:** porovnávať spoločné skutočne doložené vlastnosti — mierku, titulky, prítomnosť podnetu, čistotu exportu — a ostatné nechať otvorené. Vizuálnych 15/15 nie je 15 úplných AV rozborov ani 15 prijatých sémantických prepisov.

## 3. Časovanie a padding: preverované citlivé prípady sú v podstatnom rozsahu správne ohraničené

### frajer.fiki — trojbodový komentár, `7691709827600403734`

[Správa](rozbory/frajer.fiki.md), [celkový hárok r1](evidence/tiktok/7691709827600403734/whole.jpg), [priame čísla](evidence/blok-root/list-cues/list-cues.jpg), [časy seekov](evidence/blok-root/list-cues/sampling.json), [ASR](prepisy/54982cc2885f9d23cc8b380832c77e177963437a7137fc28d11f5f53c2340a06.json).

Na priamych 22,8 / 38,8 / 60,8 s sú skutočne veľké čísla 1 / 2 / 3. ASR obsahuje tri príslušné časti. Starý whole-r1 umiestňuje obraz prvého čísla pod výstupný čas 19,7 s; **tento údaj by nebol správna presná zdrojová kotva**. Správa však r1 neistotu priznáva a pri listových bodoch používa priame seeky. Nenašlo sa nepodložené tvrdenie, že z troch snímok poznáme prvý frame alebo plynulosť animácie.

### ZLE — široké jedlo, `7689781792898960662`

[Správa](rozbory/kontrola-zle.md), [prehľad](evidence/zle-detail/7689781792898960662/overview.jpg), [technická evidencia](acquisition.json).

Zdrojové rozmery sú **1282 × 720**. Veľké tmavé plochy pod jednotlivými širokými obrazmi doplnil výskumný hárok. Správa túto výnimku výslovne pomenúva; **nepripisuje jej vypálené vertikálne čierne pásy**. Rozlíšenie od ostatných emusových 720 × 1280 exportov je správne. Široký formát možno hodnotiť voči cieľovému použitiu, nie ako chybu fiktívneho portrétového súboru.

### fiki.sama — čierna medzera, `7692369532815428886`

[Správa](rozbory/fiki.sama.md), [whole-r1](evidence/tiktok/7692369532815428886/whole.jpg), [priame PTS](evidence/blok-c/7692369532815428886-source-pts.jpg), [detekcia](evidence/blok-c/7692369532815428886-blackdetect.txt), [ASR](prepisy/da8b7749a31e2574c4cdafe17dd6faf5ab667a38ea678da86f28cf2ce71bc646.json).

Snímky 31,8 / 32,1 / 32,3 s sú čierne. Uložený zdrojový blackdetect uvádza **29,9333–32,6333 s, 2,7 s** pri explicitnom prahu. Táto dĺžka teda nie je vymyslená iba z jednej čiernej vzorky whole. Správa správne nevyvodzuje zvukové ticho ani konkrétnu príčinu chyby. QA detekciu nanovo nespúšťala; čítala log a otvorila priame obrazové dôkazy.

## 4. Ďalšie reprezentatívne obsahové kontroly

| Klip a správa | Skutočne otvorený obrazový dôkaz | Prečítaný ASR | Výsledok QA |
|---|---|---|---|
| Naše Vajanského `7699180240068791574`, [správa](rozbory/nase-porovnanie.md) | [erb 11,8–15,8 s](evidence/own-detail/7699180240068791574-crest-detail.jpg) | [ASR](prepisy/37a2871aadeab815c0fbc8331ce25f5031fafaf082e41404033e1c4b8c16058e.json) | Tri fázy zásahu/rozpadu sú viditeľné. Záver o zlepšenej konkrétnej obrazovej réžii má oporu; celý rytmus a zvuk naďalej neoverené. |
| Naša Električka `7699178497893207318`, [správa](rozbory/nase-porovnanie.md) | [návrat objektu 41,2–42,3 s](evidence/own-detail/7699178497893207318-tram-callback-detail.jpg) | [ASR](prepisy/ec260f03daac374d4f8c50639402a7f815e79ace49c42734dbc3f70a298a7c47.json) | Ten istý objekt mení polohu/mierku pri dokončení električkového výroku. Doložené stavy nie sú dôkaz plynulej shake animácie; správa to odlišuje. |
| ZLE skokan `qUFvPLP0wQs`, [správa](rozbory/kontrola-zle.md) | [strana 1](evidence/zle-detail/qUFvPLP0wQs/page-1.jpg), [strana 2](evidence/zle-detail/qUFvPLP0wQs/page-2.jpg) | [ASR](prepisy/159a2af64731620711e73ed114c6d7fd1901b14320705bcece85cedb805ba81c.json) | Veľký portrét, citovaná žena, návrat k rečníkovi a Dubs značka sú skutočné. Výnimka z plošného „nič nevie“ je dobre podložená. |
| fikiframe `7693225215526161667`, [správa](rozbory/fikiframe.md) | [whole-r1](evidence/tiktok/7693225215526161667/whole.jpg), [hook-r1](evidence/tiktok/7693225215526161667/hook.jpg) | [ASR](prepisy/96b419eb8c5eef96dfd893ea41c98fcb27ea79b91ac2d6753492fcd577a4b4b1.json) | Fonetické titulky sú odlišné od normalizovaného ASR. Upozornenie neopravovať vtip slepo automatickým prepisom je oprávnené. Historické obrázky sú vo vloženej citácii; správa ich neprisvojuje ako samostatné nové assety klipera. |
| fiki.extra `7691063927878421783`, [správa](rozbory/fiki.extra.md) | [husté reakčné zmeny](evidence/fiki-extra-detail/7691063927878421783/detail/detail-contact.jpg) | [ASR](prepisy/d0bc233e5dfaf2eac30a435b6a7c7b3b221c781513d60c922fa10c4e5c5738f3.json) | Odchod, návrat a ďalšie prerušenia telefónu sú skutočne viditeľné; nie jeden jediný prechod. Manifest dáva deklarovaných 36+58+48+40+42 = **224 rôznych časových pozícií** za celú päťku. Táto QA neotvorila všetkých 224 nanovo. |
| fikimentalita `7699773085968321795`, [správa](rozbory/fikimentalita.md) | [whole-r1](evidence/tiktok/7699773085968321795/whole.jpg) | [ASR](prepisy/698037961b704274b302c207bdecce5753cce6ee4c02917824b23d33cf171e04.json) | Rohatá parodická postava, doplnené odpovedajúce repliky a návraty Fikiho sú viditeľné/textovo doložené. Správa správne nedokazuje konkrétny model, pôvod hlasu ani lip-sync. |
| fiki.bossik `7699517556289260822`, [správa](rozbory/fiki.bossik.md) | [whole-r2](evidence/tiktok/7699517556289260822/whole-r2.jpg), [priama negácia](evidence/blok-e/7699517556289260822-caption/direct.jpg) | [ASR](prepisy/13168158bd9fe5e1d4f68efc2e3fa3c70a9dc7fa1e8ecb7be2d1c5d7c19f4f5a.json) | 9,9/10,2 s majú ASI NIE, potom 10,5/10,8 s JE ÚPLNE VOĽBA. Správa oprávnene odmieta domnelé vynechanie negácie z jednej riedkej snímky. |
| fiki.nahrad `7691070069740195094`, [správa](rozbory/fiki.nahrad.md) | [whole-r2](evidence/tiktok/7691070069740195094/whole-r2.jpg), [koniec](evidence/blok-f/7691070069740195094-detail-source-pts.jpg) | [ASR](prepisy/663e62cb092de6f0c137a527cd82071d0e3f2c34245d5e704dcd7b3c892308d4.json) | Delenie slov je viditeľné, CTA nastupuje po fráze končiacej rokom. Podozrenie na neuzavretú vetu je oprávnené ako signál, nie definitívny verdikt o počutom zvukovom reze. |
| fiki.nahrad `7699166697009204502`, [správa](rozbory/fiki.nahrad.md) | [whole-r2](evidence/tiktok/7699166697009204502/whole-r2.jpg), [PR 195–209 s a koniec](evidence/blok-f/7699166697009204502-detail-source-pts.jpg) | [ASR](prepisy/e3edf3fb55f9adf12145751a82e982e9ddce4cee0930534f7957db0f8fe01f33.json) | PR časť skutočne prekrýva časť našej Električky. Správa správne odlišuje zhodnú časť výroku od rovnakého celého výberu a od experimentu príčin views. |

Frajer, široké jedlo a fiki.sama boli podrobnejšie rozpísané v predchádzajúcej sekcii. Spolu s touto tabuľkou ide o 12 rôznych klipov; tabuľka nie je druhý prírastok do ich počtu.

## 5. NASA — dve fotografie obsahovo a technicky preverené

Oba originálne JPG boli v tejto QA skutočne otvorené. Pillow overil dekódovanie JPEG, rozmery, bajty a SHA-256 proti uloženým metadátam:

| Súbor | Rozmery / bajty | SHA-256 | Pozorovaný obsah |
|---|---|---|---|
| [earth-apollo17-blue-marble.jpg](podklady/nasa/earth-apollo17-blue-marble.jpg) | 1920 × 1920; 350623 B | `36dad3314b64319ea75465c4293719eb131d943566eb462e8bac3281e02c3bd4` | Celá Zem, Afrika, Arabský polostrov, oblaky a čierne okolie; bez konkurenčnej CTA alebo titulkov. |
| [apollo11-astronaut-flag.jpg](podklady/nasa/apollo11-astronaut-flag.jpg) | 1856 × 1920; 496516 B | `a6072e0138f0823418a1fd122ddf2f424e7e791017c863f9982585bf984d7f3b` | Astronaut, americká vlajka, mesačný povrch, stopy a časť modulu vľavo; bez konkurenčnej grafiky. |

Živé oficiálne NASA API bolo v tejto QA načítané bez ukladania ďalších súborov. Pri oboch ID sa našla presne jedna zodpovedajúca položka a jej opis sa zhodoval s uloženými JSON metadátami:

- [NASA AS17-148-22727](https://images-api.nasa.gov/search?q=AS17-148-22727&media_type=image) identifikuje Zem z Apollo 17, 7. decembra 1972; [miestny záznam](podklady/nasa/earth-apollo17-blue-marble.json).
- [NASA AS11-40-5875](https://images-api.nasa.gov/search?q=AS11-40-5875&media_type=image) identifikuje Edwina Aldrina pri vlajke, 20. júla 1969; [miestny záznam](podklady/nasa/apollo11-astronaut-flag.json).

Webový nástroj nedokázal tieto dva pôvodne otvorené zdroje načítať; kontrola API následne prešla priamym read-only HTTP načítaním. Nešlo o nový výskum konkurenta ani o získanie ďalších médií.

**Stav:** reálne čisté výskumné fotografie so zhodnými technickými údajmi a primárnou identitou. [README](podklady/nasa/README.md) ich správne neoznačuje za presný asset konkurenta, univerzálny licenčný súhlas ani už registrovaný prijatý produkčný AssetRecord. Výber správnej slovnej kotvy, konkrétny crop a produkčná registrácia zostávajú ďalšou prácou. Tieto dve fotografie netreba znova získavať iba preto, že nie sú GIF.

## 6. Záverečná syntéza

Prečítané boli aj [VYSLEDKY.md](VYSLEDKY.md) a [POROVNANIE_KVALITY.md](POROVNANIE_KVALITY.md). Ich hlavné závery zostávajú primerane úzke: konkrétny posun našej obrazovej réžie, nie dokázané celkové prvenstvo; 100 hlavných referencií a 20 kontrolných médií, nie 120 nových čistých assetov; nulový nový posluch a súvislý playback; výrobná kapacita piatich prijatých klipov denne sa nesľubuje. VYSLEDKY už výslovne odlišujú minimálnych 119 textov s písmenami od 119 overených významov, čím je riziko zo sekcie 1 na úrovni tejto syntézy ošetrené.

**P3 — slovný rozsah porovnania nahrad:** pri čítaní POROVNANIE bola spoločná pasáž opísaná ako „Viem, že vyzerá dobre…“ a prisvojenie zásluh. Presný ASR nahrad pri 195–212 s obsahuje vzhľad/marketing/PR, potom prejde na dve výzvy k voľbám. Neobsahuje električkový ceremoniál ani predchodcov z našej ďalšej časti. Odporúčané je označiť doslovný prekryv iba ako vzhľad/marketing/PR a širšiu tému zásluh uviesť ako interpretáciu, aby sa nerozšíril rozsah zhodných viet. Na hlavnom porovnaní obrazového spracovania skutočne spoločnej PR časti sa tým nič nemení. Pripomienka bola odovzdaná rootovi bez zásahu do jeho dokumentu.

Finálne počty manifestov a všetkých proof záznamov uzatvára root samostatne. Táto QA nepreberá budúce finálne technické overenie ako už vykonaný vlastný test.

## 7. Finálna kontrola ôsmich výrobných receptov

Samostatne bol prečítaný celý nový [RECEPTY_NA_VYROBU.md](RECEPTY_NA_VYROBU.md). Obsahuje presne osem odlíšených postupov R1–R8 a všetkých **41 lokálnych odkazov** smeruje na existujúce súbory. Pri každom je oddelený spúšťač, realizovateľný princíp, skutočný materiál a chýbajúci vstup alebo komponent.

**Závažná opraviteľná chyba sa nenašla.** Dokument výslovne označuje osem postupov za výskumné recepty, nie osem implementovaných komponentov. Odkazované dva uložené produkčné JSON súbory majú identity media-reveal-action-return a pas-continuing-situation; production pack skutočne uvádza calibration, verzia 0.2.0. R5/R6 výslovne ponechávajú novú parametrickú grafiku/editovateľnú scénu nedokončenú; R2/R7 priznávajú chýbajúci čistý podnet/fotografiu a neisté autorstvo časti pohybu.

Pri štyroch reakčných MP4 v R4 boli opätovne overené fyzické súbory, zhoda obsahu s hashovým názvom a trvanie. Bean má 2,2 s, triaška 1,89 s a Jon Stewart 2 s; Ramsay má celý súbor 1,67 s, takže citovaný anotovaný rozsah 0–1,28 s sa doň zmestí. Recept ho neprezentuje ako celé trvanie súboru. Táto kontrola nanovo neprehrávala ich akciu a nedáva im nový pohybový alebo posluchový súhlas.

Vajce/sliepka zostávajú kandidátmi s potrebným výrezom, fotografie NASA výskumnými súbormi s pôvodom bez nového AssetRecord/use a električka správne AI štylizovaným objektom, nie archívom. NASA identita a technické údaje zodpovedajú už vykonanej kontrole v sekcii 5; pri tomto poslednom priechode sa nič ďalšie nesťahovalo. Nebol nájdený prevod hotového cudzieho exportu na deklarovaný čistý asset.

Audio výhrady sú prítomné pri odovzdaní citácie, reakcii, zvukových kandidátoch, vysvetľujúcej grafike aj záverečnom tvorivom prijatí. Názov SFX ani existujúci súbor sa nezamieňa za vypočutý mix. Referenčné časy sa výslovne neprepisujú na nové kotvy. Nová Selection a kontrola konkrétnej revízie zostávajú pred výrobou/prijatím.

Pri kontrolných odkazoch zodpovedajú Bekimove 5,1/5,4 s, Grinchove 10,7/11 s aj staršie telefónne/porovnávacie príklady uvedeným zdrojovým rozborom. Chyba symbolu $20 pri eurách má oporu v basedfiky; nejde o vymyslenú všeobecnú výstrahu. Tieto detaily boli pri tomto poslednom priechode porovnané s uloženými správami, nie nanovo prehraté ako ďalšie klipy.

**Rozsah finálnej kontroly:** čítanie receptov, materiálových záznamov a citovaných textových dôkazov; test existencie odkazov, hashov a trvania štyroch reakcií. Žiadna nová výroba, nové sťahovanie, posluch, súvislé prehratie ani zmena produkčných komponentov.

## Čo táto kontrola povoľuje tvrdiť

Nočný výskum má skutočne otvorené a citované obrazové dôkazy, použiteľné konkrétne postupy a pomenované materiálové medzery. Reprezentatívna kontrola podporila trojbodové medzníky, návrat jedného predmetu, stupňovanú scénu a presný citovaný podnet ako reálne pozorované možnosti.

Nepovoľuje tvrdiť, že všetky surové prepisy sú významovo správne, všetky videá boli vypočuté, poznáme plynulý rytmus celej vzorky, vieme autorstvo každej vložky alebo máme hotovú výrobnú šablónu každého pozorovaného postupu. Žiadny z týchto otvorených bodov sa nemá premeniť na nulové skóre, automatické poradie kvality či dôvod na vyradenie zo skupiny.

**Zmenený bol iba tento QA dokument.** Ostatné správy, proof súbory, prepisy, médiá, indexy a STAV zostali tejto kontrole iba na čítanie.

