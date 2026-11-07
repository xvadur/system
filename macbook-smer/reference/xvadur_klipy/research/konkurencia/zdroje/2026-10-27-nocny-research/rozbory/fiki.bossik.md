# fiki.bossik — päť obsahovo a vizuálne preverovaných klipov

Nový priechod 28. 10. 2026, blok E. **5/5 klipov, skutočne prezretých 10/10 listov whole-r2+hook-r2 a prečítaných 5/5 surových ASR.** Rozhodujúce detaily dopĺňajú nižšie uvedené priame zdrojové snímky. [Pracovný balík](../../../../../research/konkurencia/zdroje/2026-10-27-nocny-research/pracovne/blok-e.json) neobsahuje views, roly ani historický rating; identita účtu je viditeľná, nejde o plne zaslepený experiment.

## Metóda, čas a hranice

Listy **revízie 2 majú pôvodné zdrojové PTS**. Tabuľka spája naozaj videný obraz s časovaným surovým ASR; presný nástup medzi riedkymi snímkami ostáva približný. Whole interval je približne dĺžka/16 a hook približne 0,5 s. Približné okná nie sú meranie pohybu na každú snímku. Detaily označené ako priame snímky boli z MP4 vybrané `ffmpeg -ss`, s odchýlkou približne jedného zdrojového snímku. Nové kontakty zachovávajú pomer strán a dopĺňajú výskumný čierny padding; ten sa nesmie zameniť s obsahom videa.

**Nebolo súvislé prehratie ani posluch:** hlasová kvalita, hudba, SFX a plynulosť sú `not_listened`/neoverené, nie slabé skóre. ASR je pomoc pre význam, nie overený fonetický prepis ani dôkaz zvuku. S viditeľnými titulkami sme ho porovnali vo vzorkovaných miestach; neprebehla kompletná slovná korektúra. Závažné/politické či zdravotné tvrdenia v pasážach opisujeme ako obsah hovoriaceho, nie overené fakty.

Celú Fikiho pôvodnú epizódu sme neporovnávali. Viditeľnú citovanú vrstvu oddeľujeme od reakcie, ale autorstvo pipu, masky, strihu alebo cropu bez originálu nepoznáme. Hotová referencia nie je čistý produkčný asset. [Dôkazový súpis](../../../../../research/konkurencia/zdroje/2026-10-27-nocny-research/rozbory/fiki.bossik.proof.json) uvádza otvorené obrázky, prepisy a overené hashe; [priama extrakcia](../../../../../research/konkurencia/zdroje/2026-10-27-nocny-research/evidence/blok-e/direct-evidence.json) obsahuje zdrojové časové pozície. Nová Selection, výroba ani publikovanie nevznikli.


## 7699193650374364438 — Vallo: adresné vložky pri konkrétnych slovách

Dĺžka 55.05 s. [MP4](../../../../../research/konkurencia/zdroje/2026-10-27-nocny-research/media/tiktok/7699193650374364438/source.mp4) · [verejná referencia](https://www.tiktok.com/@fiki.bossik/video/7699193650374364438) · [whole r2](../../../../../research/konkurencia/zdroje/2026-10-27-nocny-research/evidence/tiktok/7699193650374364438/whole-r2.jpg) · [hook r2](../../../../../research/konkurencia/zdroje/2026-10-27-nocny-research/evidence/tiktok/7699193650374364438/hook-r2.jpg) · [surové ASR](../../../../../research/konkurencia/zdroje/2026-10-27-nocny-research/prepisy/0ee268d86fa3fc22cc91bc2abf55d618236fc6e31a3c035a48957095e6c81c95.json)

[priame snímky: fiki.bossik-bounds](../../../../../research/konkurencia/zdroje/2026-10-27-nocny-research/evidence/blok-e/fiki.bossik-bounds/direct.jpg)

Úvodné hodnotenie primátora má odfarbeného Fikiho a identifikačný portrét. Farebná časť pripustí dobrý vzhľad a marketing, potom príde výzva pomenovať pravdu a ísť voliť. ASR uzatvára politickým varovaním cez Paríž. Viditeľné vložky sledujú pomenované objekty: portrét pri mene/vzhľade, Vallo v okne pri „videjkách“, mestská panoráma pri Bratislave a neskôr dav s ohňom pri reči o Paríži. Bielo-zelené krátke titulky zostávajú pri Fikiho hrudi.

**Silné remeslo:** krátke vložky sa vracajú na tvár a nemenia každý výrok na celoplošnú montáž. Horný hovoriaci ostáva pri doplnkovom spodnom paneli. **Zmiešané:** záver obsahuje politické kauzálne tvrdenia, ktoré samotný obraz nepodkladá. Dav s ohňom nemá z náhľadu overené miesto, dátum ani aktérov a dúhová vlajka pri politických pomenovaniach je asociácia, nie dôkaz o zodpovednosti zobrazovanej skupiny. Túto významovú chybu nemožno preniesť ako „dobrý B-roll“ len preto, že súvisí s vysloveným slovom. Samostatný čierny zaoblený CTA blok nad rozostreným Fikim dobehne po prejave. **Neoverené:** posluch, presný charakter pohybu, zdroj Vallo záberov a spor o politické tvrdenia. ASR deformuje meno aj miestami výzvu; titulky úvodu podporujú identitu a tému, nie faktickú správnosť obvinení.

| Zdrojový čas / rozsah | Kotva alebo význam surového ASR | Skutočne pozorovaný obraz a funkcia |
|---|---|---|
| 0–2,1 s | ASR: úvodné hodnotenie primátora. | Odfarbený portrét Fikiho, Vallo cutout vľavo dole; pri mene identifikácia. |
| 2,3–8 s | ASR: vzhľad, videá, marketing. | Farebný návrat; iný portrét pri vzhľade, Vallo v okne v spodnom paneli pri videách, ďalší detail pri sebaprezentácii. |
| ≈12–26,3 s | ASR: dve veci a výzva ísť voliť/vrátiť mesto. | Fiki a titulky, krátko plná panoráma pri vyslovenej Bratislave (snímka 24,267 s). |
| ≈30–42,9 s | ASR: varovanie cez Paríž a politické pomenovania. | Návrat k tvári; spodný oheň/dav okolo 38,133 s a neskôr vlajka. Miesto/udalosť/aktéri nie sú overení. |
| ≈43–50 s; potom ≈50–55,05 s | ASR: politické varovanie do uzáveru. | Tvár a dôraz, potom rozostrený portrét s malou čiernou CTA kartou; koniec potvrdený pri 54,854 s. |

**Prenos:** meno/miesto → správny krátky obraz → späť na tvár; [media-stage](../../../../../fiki/kniznica/recepty/73e3f076fedd5ed432bd95bb901655247397fe4360fa458634c2bee1abbe4f47.json) máme. [Eurovea](../../../../../fiki/kniznica/originaly/d773903ee55f2201d01aed90e5c7ddb588d19d142fb9b26d4fb3c9b027f546ea.mp4) je reálny dostupný bratislavský záber, nie táto panoráma hradu/Mosta SNP. Konkrétne Vallo video a čisté portréty chýbajú. Nepreberieme neidentifikovaný dav ako potvrdenie politickej príčiny; treba dohľadať správnu udalosť alebo vložku vynechať.


## 7689885220899753238 — Alkohol a partnerka: prirodzený dialóg bez meme vrstvy

Dĺžka 48.09 s. [MP4](../../../../../research/konkurencia/zdroje/2026-10-27-nocny-research/media/tiktok/7689885220899753238/source.mp4) · [verejná referencia](https://www.tiktok.com/@fiki.bossik/video/7689885220899753238) · [whole r2](../../../../../research/konkurencia/zdroje/2026-10-27-nocny-research/evidence/tiktok/7689885220899753238/whole-r2.jpg) · [hook r2](../../../../../research/konkurencia/zdroje/2026-10-27-nocny-research/evidence/tiktok/7689885220899753238/hook-r2.jpg) · [surové ASR](../../../../../research/konkurencia/zdroje/2026-10-27-nocny-research/prepisy/83da0ff8ba010e0edb90973709a2067af45bb2ac70933a5ee8b7856bcad1cfab.json)

[priame snímky: fiki.bossik-bounds](../../../../../research/konkurencia/zdroje/2026-10-27-nocny-research/evidence/blok-e/fiki.bossik-bounds/direct.jpg)

Prvá veta „som ženatý muž“ a „kontrolný orgán“ nastaví vzťahový vtip. Namiesto ilustračnej svadby nasleduje skutočná replika partnerky mimo obrazu: rozhovor o prvom rande a pití. Záver sa vráti ku konkrétnej ďalšej objednávke a časovému obmedzeniu. Humor je vo výmene replík a Fikiho výrazoch, nie v kolekcii cudzích GIFov. Jednoduché biele titulky držia aj hlas osoby, ktorú nevidíme.

**Silné:** setup → odpoveď druhej osoby → návrat k pôvodnému kontrolnému orgánu. Zdrojová situácia sama poskytuje reakciu aj pointu, takže zachovanie dialógu je podstatnejšie než pridávanie vrstiev. **Zmiešané:** široký stredový obraz je tmavý a okolité rozostrené predĺženie spotrebuje veľa plochy vertikálneho MP4. Tvár je menšia než v portrétoch pri stole; hlas partnerky nie je označený stabilným odlíšením hovoriaceho vo vzorke. **Neoverené:** skutočné striedanie hlasov a časovanie komických prestávok, pretože posluch neprebehol. ASR silne deformuje poslednú repliku, kým titulok pri 42,467 s zrozumiteľne uvádza lietadlo; posledné slová treba opraviť skutočným posluchom. Názov „alkoholik“ a repliky postáv nie sú klinická diagnóza. Bez plnej epizódy nevieme, či je zmena širokého výrezu zdrojová alebo kliperova; pri prenose treba zachovať orientáciu na hovoriacich a nezostrihnúť polovicu odpovede.

| Zdrojový čas / rozsah | Kotva alebo význam surového ASR | Skutočne pozorovaný obraz a funkcia |
|---|---|---|
| 0–6,7 s | ASR: ženatý muž a kontrolný orgán. | Tmavší široký A-roll v stredovom páse, jednoduché biele vetné titulky pod ním. |
| ≈6,8–13,5 s | ASR: ďalšia objednávka a otázka partnerke o prvom rande. | Fiki sa otočí mimo kameru; zdrojový pohľad smeruje k druhému hovoriacemu. |
| ≈13,6–25 s | ASR: dialóg o pití a prvom rande. | Zachované reakčné tváre a texty replík, bez cudzích reakčných assetov v prezretých snímkach. |
| ≈25–37,9 s | ASR: osobná reakcia a ďalšia otázka partnerke. | Portrét v širokom páse, gestá; základ vtipu pokračuje v reči. |
| ≈38–43 s; potom ≈44–48,09 s | ASR: časovanie ďalšej objednávky; záver veľmi chybový. | Posledný viditeľný text vysvetľuje lietadlo; potom rozostrený obraz a jednoduchá URL, potvrdená pri 47,888 s. |

**Pripravený princíp:** skutočný dialóg → priestor na repliku → reakčný návrat. Žiadny nový asset netreba, potrebujeme zvolený zdroj, presný prepis oboch hlasov a počuteľný spoj. [Q&A obrúčky](../../../../../fiki/kniznica/baliky/qna-106-2026-10-26/materialy.r0001.json) existujú ako kandidát, ale v tejto situácii by len doslovne ilustrovali úvodné slovo a mohli zavadzať skutočnému partnerskému vtipu.


## 7699517556289260822 — Tá istá Q&A: pointa v predohre a skrátená odpoveď

Dĺžka 34.34 s. [MP4](../../../../../research/konkurencia/zdroje/2026-10-27-nocny-research/media/tiktok/7699517556289260822/source.mp4) · [verejná referencia](https://www.tiktok.com/@fiki.bossik/video/7699517556289260822) · [whole r2](../../../../../research/konkurencia/zdroje/2026-10-27-nocny-research/evidence/tiktok/7699517556289260822/whole-r2.jpg) · [hook r2](../../../../../research/konkurencia/zdroje/2026-10-27-nocny-research/evidence/tiktok/7699517556289260822/hook-r2.jpg) · [surové ASR](../../../../../research/konkurencia/zdroje/2026-10-27-nocny-research/prepisy/13168158bd9fe5e1d4f68efc2e3fa3c70a9dc7fa1e8ecb7be2d1c5d7c19f4f5a.json)

[priame snímky: 7699517556289260822-caption](../../../../../research/konkurencia/zdroje/2026-10-27-nocny-research/evidence/blok-e/7699517556289260822-caption/direct.jpg) · [priame snímky: fiki.bossik-bounds](../../../../../research/konkurencia/zdroje/2026-10-27-nocny-research/evidence/blok-e/fiki.bossik-bounds/direct.jpg) · [detail v zdrojovom rozlíšení](../../../../../research/konkurencia/zdroje/2026-10-27-nocny-research/evidence/blok-e/full/7699517556289260822-10.5.jpg)

Odfarbený úvod vytiahne záverečnú vetu, potom príde otázková karta a farebná odpoveď. ASR končí rovnakou vetou ako predohra; máme teda doložený vzor pointa z tela → otázka → kratšie vysvetlenie → návrat. Rovnaká otázka a prostredie sú v dlhšej referencii _fiki.unchained_ 7698798442960768278; tu má výsledok 34,34 s a vynecháva viacero jej argumentačných častí. Rozdiel v rozsahu nie je dôkazom úspechu ani automaticky lepšej vernosti významu.

**Silné:** karta dopovie kontext po provokatívnom úvode, tvár zostáva veľká; svadobný obraz pri rodine a piktogramy sú adresné. **Zmiešané:** doslovné sexuálne emoji pridávajú akcent, ale nie vysvetlenie. Dôležitá obsahová kontrola: jedna riedka snímka ukazuje „JE ÚPLNE VOĽBA“, čo by samo vyzeralo opačne voči ASR. Hustejšie priame snímky však pri 9,9–10,2 s ukazujú „ASI NIE“, potom 10,5–10,8 s pokračovanie. Negácia nezmizla; je rozdelená medzi titulkové karty. Prenos by mal celú zápornú významovú jednotku držať spolu. **Neoverené:** hladkosť výberu viet, presný zvuk a významové vynechania oproti plnej epizóde. Hovorené zovšeobecnenia o orientácii a rase nie sú naším faktickým záverom. Čistý svadobný obraz ani jeho osoby nie sú v referencii identifikované.

| Zdrojový čas / rozsah | Kotva alebo význam surového ASR | Skutočne pozorovaný obraz a funkcia |
|---|---|---|
| 0–2,6 s | ASR: veta použitá aj v závere. | Odfarbený teaser zodpovedajúci pointovej vete; veľká tvár bez samostatnej otázkovej karty. |
| 2,7–4,3 s | ASR: čítanie pôvodnej otázky. | Farebný návrat a biela karta dole; kontext sa dopovie pred odpoveďou. |
| ≈4,4–9,8 s | ASR: prvá odpoveď a spresnenie. | Tvár a krátke zeleno-biele titulky; symboly a krátke sexuálne emoji pri doslovnom výraze. |
| 9,9–10,2 / 10,5–10,8 s, priame snímky | ASR 9,78–10,84 s: „asi nie je úplne voľba“. | ASI NIE → JE ÚPLNE VOĽBA. Negácia je prítomná na predošlej karte, nie chybne vynechaná. |
| ≈13–29,2 s | ASR: hypotetická rodina a návrat k úvodnej odpovedi. | Svadobný obraz pri rodine/svadbe, neskôr symbol; návraty na tvár. |
| ≈29,5–34,34 s | Záver reči podľa ASR pred kartou. | Rozostrený portrét a malý čierny CTA blok, potvrdený pri 34,142 s. |

**Prenos:** teaser musí mať dopovedanú otázku a vysvetlenie; titulkovú negáciu nezostrihnúť na samostatný opačný výrok. [media-stage](../../../../../fiki/kniznica/recepty/73e3f076fedd5ed432bd95bb901655247397fe4360fa458634c2bee1abbe4f47.json) dá obraz k vete. [Vlastné Q&A obrúčky](../../../../../fiki/kniznica/baliky/qna-106-2026-10-26/materialy.r0001.json) sú dostupný kandidát na ilustračnú rodinnú vetu, nie presne táto svadba ani Fikiho rodina. Nové piktogramy nie sú potrebné na základný formát. Pre význam sporného krátenia treba posluch a plný zdroj.


## 7690679697570630914 — Sandwich: očakávanie a skutočná ochutnávka

Dĺžka 42.45 s. [MP4](../../../../../research/konkurencia/zdroje/2026-10-27-nocny-research/media/tiktok/7690679697570630914/source.mp4) · [verejná referencia](https://www.tiktok.com/@fiki.bossik/video/7690679697570630914) · [whole r2](../../../../../research/konkurencia/zdroje/2026-10-27-nocny-research/evidence/tiktok/7690679697570630914/whole-r2.jpg) · [hook r2](../../../../../research/konkurencia/zdroje/2026-10-27-nocny-research/evidence/tiktok/7690679697570630914/hook-r2.jpg) · [surové ASR](../../../../../research/konkurencia/zdroje/2026-10-27-nocny-research/prepisy/6ca6201932824873aefffb5ea293c8ea160d88e9cf63f66ce030f473866b501d.json)

[priame snímky: fiki.bossik-bounds](../../../../../research/konkurencia/zdroje/2026-10-27-nocny-research/evidence/blok-e/fiki.bossik-bounds/direct.jpg)

Prvá veta dá krátke hodnotenie a v ruke je hneď skutočný sandwich. Potom ASR vysvetlí japonskú cestu, očakávanie zo sledovaných videí a 7-Eleven; záver hodnotí produkt v kategórii baleného jedla a jeho konzistenciu. Nejde o graficky vyrobenú reklamu, pointu dodáva samotná ochutnávka. Krátka silueta Japonska pri 1,5 s identifikuje miesto, zvyšok väčšinou nesie Fiki a predmet v jeho rukách.

**Silné:** reč, obal aj jedlo sú v tom istom zdrojovom deji; divák nepotrebuje externú fotografiu na každé pomenované sústo. Okolo 10,667 s vidno detail obalu a pri 37,333 s opäť reálny sandwich. Vzorky pri 24 s zachytávajú prelínajúce sa stavy medzi zábermi. **Zmiešané:** obraz je vo vertikálnom MP4 pomerne úzky, nad a pod ním je veľa rozostreného predĺženia; tvár i detail produktu by zniesli presnejšiu kompozíciu podľa daného momentu. Začiatočné „je to“ nemá ešte slovne uvedený produkt, hoci obraz ho naznačí. **Neoverené:** meno spomínaného šéfkuchára a jeho skutočná návšteva; v reči ho nemožno z nejasného ASR doplniť na známu celebritu. ASR skomolí úvod aj niekoľko jedálenských výrazov, titulky pomáhajú, ale zvuk nebol vypočutý. Mapa a font nie sú doložené ako získané samostatné súbory.

| Zdrojový čas / rozsah | Kotva alebo význam surového ASR | Skutočne pozorovaný obraz a funkcia |
|---|---|---|
| 0–1 s | ASR: krátke hodnotenie; úvod chybový. | Fiki so skutočným jedlom v ruke, jednoduché biele titulky; široký obraz v rozostrenom predĺžení. |
| 1–5 s | ASR: pred cestou do Japonska a asi 15 videí. | Malá japonská silueta/červený bod pri 1,5 s → opäť čistá tvár. |
| ≈7,8–12 s | ASR: egg salad sandwich z 7-Eleven. | Detail skutočného obalu v ruke okolo 10,667 s; produkt dostane konkrétny referent. |
| ≈12,4–23 s | ASR: očakávania podľa šéfkuchára/videí. | Tvár a gestá, externá citácia šéfkuchára vo vzorke nie je. |
| ≈24–37,4 s | ASR: hodnotenie v kategórii baleného jedla, chlieb a nátierka. | Prelínajúce sa zábery, reálna ochutnávka a návrat k predmetu pri závere. |
| ≈38–42,45 s | Výzva po poslednom obsahovom hodnotení. | Rozostrený obraz a jednoduché viac na fiki.sk; potvrdené pri 42,246 s. |

**Pripravený princíp:** predmet musí byť čitateľný, keď sa pomenuje, potom ukázať skutočnú akciu/reakciu a dopovedať hodnotenie. Pri pasáži so zdrojovým predmetom netreba ďalšie produktové foto. Čistá mapa Japonska chýba; možno vytvoriť korektnú vlastnú jednoduchú mapu po výbere. [Vajce/sliepka z Q&A](../../../../../fiki/kniznica/baliky/qna-106-2026-10-26/materialy.r0001.json) nie sú náhrada skutočného japonského sandwichu. Pohyb/crop a zvuk sú ešte na kontrolu.


## 7697404240188230934 — Napodobnenie kritika: teaser, kontext a adresné portréty

Dĺžka 35.32 s. [MP4](../../../../../research/konkurencia/zdroje/2026-10-27-nocny-research/media/tiktok/7697404240188230934/source.mp4) · [verejná referencia](https://www.tiktok.com/@fiki.bossik/video/7697404240188230934) · [whole r2](../../../../../research/konkurencia/zdroje/2026-10-27-nocny-research/evidence/tiktok/7697404240188230934/whole-r2.jpg) · [hook r2](../../../../../research/konkurencia/zdroje/2026-10-27-nocny-research/evidence/tiktok/7697404240188230934/hook-r2.jpg) · [surové ASR](../../../../../research/konkurencia/zdroje/2026-10-27-nocny-research/prepisy/deb7783ab70fec07098ef04735d031e8b9fb26ea2358cf7d0f89368314368a09.json)

[priame snímky: fiki.bossik-bounds](../../../../../research/konkurencia/zdroje/2026-10-27-nocny-research/evidence/blok-e/fiki.bossik-bounds/direct.jpg)

Úvodná odfarbená veta je napodobnením citovanej výčitky; potom farebná časť dopovie, na aký vlastný výstup Fiki reaguje. Neskôr tú istú výčitku zopakuje, pridá ďalšiu otázku a zahrá reakciu komentárov. ASR podporuje predohru z tela a návrat k nej, obraz veľkej tváre a meniace sa výrazy držia humor. Dva krátke výrezy ľudí približne pri 5,5–7 s a 9 s identifikujú osoby spomínané v reči.

**Silné:** vložky majú konkrétny pomenovaný referent a nebránia neskoršej hereckej reakcii Fikiho. Odfarbenie odlíši úvodný citovaný/napodobnený výrok od vlastného výkladu. **Zmiešané:** bez pôvodného sporu divák nedostane skutočné vyjadrenie druhej osoby, len Fikiho interpretáciu a imitáciu. Portrét pri závažnom obvinení nič nedokazuje; pravdivosť tvrdení o sexuálnom násilí ani o motiváciách menovaných ľudí nebola zisťovaná a audit ich nepotvrdzuje. Záverečná kategorizácia skupín je hovorený názor, nie výrobný fakt. **Neoverené:** identita výrezov len podľa vzhľadu, intonácia napodobenia a zvuk; ASR výrazne deformuje meno ženy aj záverečné spojenie. Viditeľné titulky poskytujú oporu pre čítanie mien, ale treba ich overiť pred ďalším použitím. Po poslednom prejave je rozostrená tvár s malým čiernym CTA blokom.

| Zdrojový čas / rozsah | Kotva alebo význam surového ASR | Skutočne pozorovaný obraz a funkcia |
|---|---|---|
| 0–3,3 s | ASR: napodobnená výčitka. | Odfarbený veľký portrét, krátke bielo-zelené titulky; nie pôvodný záznam kritika. |
| 3,4–7,5 s | ASR: Fikiho kontext vlastného videa. | Farebný návrat, výraz/gestá, krátky ženský cutout pri mene; nedokazuje hovorené obvinenie. |
| 7,6–10,1 s | ASR: príchod menovaného kritika. | Mužský výrez dole okolo 8,933 s, potom odstránenie; identifikačná funkcia. |
| ≈10–17,3 s | ASR: zopakovanie výčitky a ďalšia otázka. | Tvár a výrazné artikulačné stavy, nie ďalšia externá vložka. |
| ≈17,4–30,2 s | ASR: reakcia komentárov a vlastné hodnotenie kritika. | Fikiho hraná reakcia v rôznych mierkach, zelené slovné dôrazy; potom návrat do pokojnejšej tváre. |
| ≈31–35,32 s | Výzva po obsahovej časti. | Rozostrený A-roll s čiernou CTA kartou, potvrdený pri 35,117 s. |

**Prenos:** rozlíšiť citáciu/imitáciu, dopovedať predmet a nechať tvári priestor na pointu. [media-stage](../../../../../fiki/kniznica/recepty/73e3f076fedd5ed432bd95bb901655247397fe4360fa458634c2bee1abbe4f47.json) vloží overený portrét, ale obaja čistí identifikovaní ľudia v produkčnej pätnástke chýbajú. Treba správny zdroj a meno; pri spore je vhodná aj samotná overená pôvodná citácia. Obraz osoby nie je dôkaz obvinenia. Reakčný GIF je voliteľný a tu by pravdepodobne duplikoval Fikiho vlastnú reakciu.


## Záver autora a vykonateľné formuly

Vzorka je **silná v adresnosti krátkej vložky a veľkej reakcii tváre**, pričom food a partnerský rozhovor ukazujú, že zdrojový dej môže niesť klip takmer sám. Čiernobiela predohra, farebné telo, bielo-zelené frázy a rozostrený CTA blok vytvárajú pri stolových videách opakovaný systém. Presný font/plugin ani zvukový preset neboli identifikované.

1. **Skutočný predmet/partner v zdroji → reakcia → pointa.** Materiálovo najjednoduchšie; netreba nový meme balík. Potrebujeme vybranú pasáž a počuť aj odpoveď osoby mimo obrazu.
2. **Meno → krátky správny portrét → návrat.** media-stage je pripravený; identifikované čisté portréty chýbajú. Vyrezať človeka z hotovej referencie nie je ten istý vstup.
3. **Pointa z tela → otázka → odpoveď.** Q&A porovnanie poskytuje konkrétny vzor. Obsahová skratka sa nesmie stať zmenou postoja. Priama kontrola ukázala, že zdanlivo chýbajúca negácia bola prítomná na predošlej karte; samostatný screenshot nestačí na obvinenie z chyby.

Neprenášať neoverený dav/požiar ako dôkaz politickej príčiny a neprisudzovať fotografii dôkaz obvinenia osoby. To sú konkrétne významové hranice média, nie dôvod na automatický zákaz ilustračnej práce. Audio/mix/pohyb ostávajú neprehraté. Nový produkčný výsledok ani prijatie nevznikli.


Skutočná materiálová pripravenosť: [PODKLADY_NA_VYROBU](../../../../../research/konkurencia/zdroje/2026-10-27-nocny-research/PODKLADY_NA_VYROBU.md). Dve uložené produkčné receptúry a evidované médiá nezakladajú nové Adamovo tvorivé prijatie.
