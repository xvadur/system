# Kontrolná vzorka historicky ZLE autorov — prvý obsahový priechod

Zadanie a osnovu určuje [ZADANIE.md](../../../../../research/konkurencia/zdroje/2026-10-27-nocny-research/ZADANIE.md). Výber je nemenná [kontrolna-vzorka.json](../../../../../research/konkurencia/zdroje/2026-10-27-nocny-research/kontrolna-vzorka.json). Historická kategória pochádza zo 7. októbra a nie je súčasným tvorivým verdiktom. Hodnotenie nižšie vychádza zo skutočne otvorených snímok; views sa používajú až ako oddelený kontext.

**Skutočné obsahové pokrytie tohto priechodu: 15/15 vybraných videí od všetkých troch autorov.** Bolo pripravených 15 sád časovaných snímok; skutočne vizuálne otvorených bolo 21 kontaktných hárkov alebo ich strán s celkovo **321 snímkami**. Audio nebolo vypočuté; súvislý pohyb a rytmus neboli prehratím overené. Ide o dokončený prvý vizuálny priechod pevnej kontrolnej vzorky, nie úplný audiovizuálny rozbor ani tvorivé poradie troch autorov.


**Doplnenie 28. 10. — význam reči:** následne bolo prečítaných **15/15 surových lokálnych ASR**. Trinásť poskytuje aspoň orientačný obsah; jedlo `7689781792898960662` a scénka `7689787906009074967` nemajú spoľahlivý obsahový prepis. Nová sekcia 13 dopĺňa hook, kontext a pointu a spresňuje staršie „neoverené“ v sekciách 3–10. Pôvodné vizuálne pozorovania a ich rozsah zostávajú zachované. **Posluch ani súvislé prehratie sa tým nezmenili: neprebehli.**

## 1. Identita a dostupnosť

| Historicky hodnotený človek | Presne priradený skúmaný účet | Vybraných videí | Skutočne vizuálne vzorkovaných | Výsledok dostupnosti |
|---|---|---:|---:|---|
| `@k_skokan1` | YouTube `@fikiballing` | 5 | **5** | Presne priradený YouTube namiesto nedostupného TikToku; všetkých päť MP4 získaných a vizuálne vzorkovaných. |
| `@emus_iik` | TikTok `@fiki.unrealized` | 5 | **5** | Päť konkrétnych súborov stiahnutých; obsahové nálezy sú nižšie. |
| `@tomassykorawhysteve` | YouTube `@the_best_of_fiki` | 5 | **5** | Presne priradený YouTube namiesto nedostupného TikToku; všetkých päť MP4 získaných a vizuálne vzorkovaných. |

Zmena platformy zostáva viditeľná; z YouTube editov sa automaticky nevyvodzuje rovnaké spracovanie na TikToku. Predchádzajúca chyba získania formátu bola v akvizičnej vrstve opravená; tento hodnotiteľ helper ani akvizičný manifest nemenil. Pôvodný čiastkový stav 5/15 je týmto rozšírením nahradený skutočne prezretou vzorkou 15/15.

## 2. Dôkazy a spôsob čítania

[Evidencia extrakcie](../../../../../research/konkurencia/zdroje/2026-10-27-nocny-research/evidence/zle-detail/frame-extraction.json) obsahuje zdrojové cesty, SHA-256 celých MP4, rozmery, skutočné trvanie, časy, cesty a hashe jednotlivých snímok. Vzorky sú 0,1 / 0,5 / 1 / 1,5 / 2,5 / 4 / 6 / 8 / 10 / 12 s, potom po piatich sekundách a dve snímky pri konci. Dlhšie medzery medzi vzorkami zostávajú obsahovo neoverené.

**Dôležitá oprava interpretácie rozloženia:** v emusovej vzorke sú štyri súbory 720 × 1280 s malým vodorovným obrazovým pásom a čiernymi plochami priamo v súbore. Video `7689781792898960662` je však natívne **1282 × 720**. Tmavý priestor pod jeho širokými snímkami na kontaktnom hárku doplnil výskumný layout; tento priestor sa nesmie pripísať kliperovi. Jeho vlastnosťou je široký formát, nie dokázaný vertikálny export s vypálenými čiernymi pásmi. Rozmery ďalších desiatich YouTube súborov sú zaznamenané pri ich rozbore a v evidencii extrakcie.

## 3. `7691372489355627798` — komentár ku Kuciakovi

- [Verejný klip](https://www.tiktok.com/@fiki.unrealized/video/7691372489355627798)
- [Skutočné MP4](../../../../../research/konkurencia/zdroje/2026-10-27-nocny-research/media/tiktok/7691372489355627798/source.mp4)
- [Otvorený časovaný hárok — 18 snímok](../../../../../research/konkurencia/zdroje/2026-10-27-nocny-research/evidence/zle-detail/7691372489355627798/overview.jpg)
- Technicky: 44,675 s, 720 × 1280. Posluch: **neoverené**. Súvislé prehratie: **neoverené**.

**Pozorované:** v 0,1–1,5 s je čiernobiely Fiki pri bazéne a vľavo vložený portrét. V 2,5 / 4 / 6 s už zostáva Fiki bez portrétu. V 8 / 10 / 12 / 15 / 20 / 25 / 30 / 35 s je viditeľná farebná verzia rovnakého širokého prostredia. Vzorkované snímky neobsahujú priebežný prepis reči. V 40 / 42,675 / 44,425 s je zelená karta `FIKI UNCHAINED / VIAC NA FIKI.SK`.

**Silné:** úvodný portrét dáva konkrétny vizuálny referent; tvár hovoriaceho nie je prekrytá súťažou viacerých textov. CTA má čitateľnú adresu.

**Slabé:** vlastný portrétový súbor využíva na dej iba malý vodorovný stredový pás, približne tretinu výšky. Fikiho tvár je preto relatívne malá. V prezretých miestach chýba prístup k obsahu reči cez titulky a po úvodnom portréte vzorka neukazuje ďalšie významové obrazové rozvinutie. Štyri a viac sekúnd pred koncom už vidíme iba CTA; presný začiatok karty nebol vymedzený.

**Verdikt remesla:** obrazová adaptácia pre portrét je **slabá**; identifikácia témy **zmiešaná**. Samostatnosť argumentu, správnosť výberu, humor, pointa a hlas sú **neoverené**, pretože klip nemá čitateľný prepis vo vzorke a audio nebolo vypočuté. Samotná absencia ďalších efektov nie je chybou bez znalosti reči.

**Čo by sme vedeli spraviť lepšie:** väčší výrez s tvárou a potrebným gestom, čitateľný prepis, portrét na presnú slovnú kotvu a primerane krátky koniec. Zväčšenie môže byť vykonateľné z obrazového zdroja; konkrétny hlasový strih sa nesmie navrhnúť iba podľa týchto snímok.

## 4. `7689781792898960662` — situácia pri jedení

- [Verejný klip](https://www.tiktok.com/@fiki.unrealized/video/7689781792898960662)
- [Skutočné MP4](../../../../../research/konkurencia/zdroje/2026-10-27-nocny-research/media/tiktok/7689781792898960662/source.mp4)
- [Otvorený časovaný hárok — 16 snímok](../../../../../research/konkurencia/zdroje/2026-10-27-nocny-research/evidence/zle-detail/7689781792898960662/overview.jpg)
- Technicky: 35,339 s, **1282 × 720, natívne široký formát**. Posluch a súvislý pohyb: **neoverené**.

**Pozorované:** v 0,1–4 s vidíme čiernobiely detail ženy pri jedle. V 0,5 / 1 s je biely text „strašne veľký kus“, v 2,5 s „skoro som sa zadusila“. V 6 s je farebný detail rúk/predmetov pri stole, v 8 / 10 / 12 / 15 s Fiki, v 15 s text „to je extrém“. V 20 / 25 s opäť žena. V 30 / 33,339 / 35,089 s je zelená CTA karta.

**Silné:** je tu konkrétna situácia, viditeľný predmet a striedanie účastníkov; text sprístupňuje aspoň časť replík. Skladba má vizuálne čitateľné podnety a reakčné tváre bez nutnosti dopĺňať náhodné GIFy. Toto je **protipríklad tvrdenia, že historicky ZLE znamená úplnú absenciu funkčného remesla**.

**Zmiešané/slabé:** široký formát nevyužíva celý portrétový priestor; crop sa však musí rozhodovať podľa potrebného jedla, rúk a tvárí. Vypálené biele titulky nie sú prítomné na každej vzorke. CTA tvorí aspoň záverečných päť pozorovaných sekúnd bez viditeľného pokračovania situácie; bez posluchu nehodnotím jej zvukový dobeh ani presný strih.

**Pôvod vrstiev:** nemožno zatiaľ prisúdiť kliperovi všetky zmeny záberov alebo biele titulky; môžu byť už v pôvodnom IRL zdroji. Potrebné je priame porovnanie s pôvodnou epizódou. Výskumný kontaktný hárok sám vytvára tmavú plochu pod širokou snímkou; nejde o chybu exportu autora.

**Verdikt remesla:** viditeľná situačná skladba je **zmiešaná až funkčná**; portrétové využitie je **zmiešané**. Úplnosť pointy, presné načasovanie repliky, humor a zvuk sú **neoverené**. Nedostatky nepotvrdzujú celoplošný verdikt „nevie strihať“.

**Čo sa dá prevziať:** ponechať skutočný podnet a reakčnú tvár; pri jedle neodrezať predmet a ruky iba kvôli väčšej hlave. Potrebný je samostatný situačný formát, nie povinná ilustrácia každej vety.

## 5. `7689787906009074967` — „Ten jeden kamoš, ktorý sa vrátil z erazmu“

- [Verejný klip](https://www.tiktok.com/@fiki.unrealized/video/7689787906009074967)
- [Skutočné MP4](../../../../../research/konkurencia/zdroje/2026-10-27-nocny-research/media/tiktok/7689787906009074967/source.mp4)
- [Otvorený časovaný hárok — 16 snímok](../../../../../research/konkurencia/zdroje/2026-10-27-nocny-research/evidence/zle-detail/7689787906009074967/overview.jpg)
- Technicky: 34,2 s, 720 × 1280. Posluch a súvislý pohyb: **neoverené**.

**Pozorované:** úvod 0,1–4 s je čiernobiely detail Fikiho tváre, pod ktorým je tenký zelený situačný nadpis. V 6 s je v sampled snímke takmer čierny obraz s ponechaným zeleným nadpisom; z jednej snímky nemožno určiť dĺžku alebo účel tohto prechodu. V 8–15 s je farebná tvár, v 20 / 25 s širší pohľad na gestá a postavu. Nadpis zostáva rovnaký; nejde o postupný prepis replík. V 30 / 32,2 / 33,95 s je CTA.

**Silné:** prvý obraz má zrozumiteľnú situačnú premisu, ktorá divákovi vysvetľuje typ scénky. Zmena medzi detailom a gestom môže zachovať informáciu už natočenú v zdroji. Text neprekrýva tvár.

**Slabé:** obraz je opäť malý vodorovný pás v portrétovom súbore; zelený jednoriadkový nadpis je na celej ploche veľmi malý. Vo vzorke nie je čitateľný priebežný prepis reči. Čierny stav v 6 s treba preveriť v hustejšom okolí alebo prehratím, kým sa označí za zbytočnú pauzu či chybu.

**Verdikt remesla:** premise/hook **silný v obmedzenom vizuálnom zmysle**, mobilná čitateľnosť **slabá**, ostatná dramaturgia a zvuk **neoverené**. Toto video ukazuje prítomný nápad aj slabšie finálne vyhotovenie; stará kategória nepopisuje každú jeho vlastnosť.

**Čo sa dá prevziať:** stabilný nadpis môže založiť scénku. U nás by potreboval väčšiu mierku a úlohu oddelenú od titulkov; prijatie konkrétnej interpretácie nadpisu musí vychádzať z reči.

## 6. `7691643187244387606` — komentár pri bazéne

- [Verejný klip](https://www.tiktok.com/@fiki.unrealized/video/7691643187244387606)
- [Skutočné MP4](../../../../../research/konkurencia/zdroje/2026-10-27-nocny-research/media/tiktok/7691643187244387606/source.mp4)
- [Otvorený časovaný hárok — 21 snímok](../../../../../research/konkurencia/zdroje/2026-10-27-nocny-research/evidence/zle-detail/7691643187244387606/overview.jpg)
- Technicky: 56,748 s, 720 × 1280. Posluch a súvislý pohyb: **neoverené**.

**Pozorované:** rovnaké bazénové prostredie. V 0,1–6 s je obraz čiernobiely; od vzorky 8 s farebný. V 10–50 s vzorky ukazujú rečníka a jeho gestá, bez viditeľného priebežného titulkovania, doplnkovej obrazovej vrstvy alebo zmeny základného rozloženia. V 54,748 / 55 / 56,498 s je CTA.

**Silné:** dostatok priestoru pre gestá, žiadna pozorovaná kolízia titulkov s tvárou, konzistentná identifikačná karta.

**Slabé:** portrétový súbor opäť necháva veľkú časť výšky čiernu; v malom stredovom páse je tvár drobná. Chýba vizuálny vstup do obsahu v podobe nadpisu alebo prepisu. Samotný prechod z čiernobielej do farebnej podoby nepomenúva predmet komentára; bez reči nevieme overiť jeho funkciu.

**Verdikt remesla:** vizuálna orientácia a využitie rámu **slabé**; tematický výber, držanie argumentu, pointa, skutočný rytmus a zvuk **neoverené**. Čistý A-roll môže byť správnou voľbou; problémom doloženým snímkami je najmä mierka a nízka dostupnosť významu bez posluchu.

**Vykonateľná oprava:** veľkosť tváre podľa gest, presný čitateľný prepis a konkrétny úvodný význam. Pridať B-roll až vtedy, keď poznáme vetu, ktorú má vysvetliť.

## 7. `7692132409495653654` — komentár k novinárom

- [Verejný klip](https://www.tiktok.com/@fiki.unrealized/video/7692132409495653654)
- [Skutočné MP4](../../../../../research/konkurencia/zdroje/2026-10-27-nocny-research/media/tiktok/7692132409495653654/source.mp4)
- [Otvorený časovaný hárok — 17 snímok](../../../../../research/konkurencia/zdroje/2026-10-27-nocny-research/evidence/zle-detail/7692132409495653654/overview.jpg)
- Technicky: 39,402 s, 720 × 1280. Posluch a súvislý pohyb: **neoverené**.

**Pozorované:** čiernobiely úvod 0,1–6 s; od 8 s farebný Fiki pri bazéne. V 10 / 12 / 15 / 20 / 25 / 30 s rečník používa ruky a pozerá sa rôznymi smermi. Základný malý vodorovný pás ostáva rovnaký; vzorky nemajú priebežný prepis alebo ilustračný podnet. V 35 / 37,402 / 39,152 s je CTA.

**Silné:** tvár a ruky zostávajú vnútri aktívneho obrazu; nič pozorované ich nezakrýva. Grafický koniec má zhodný štýl ako ostatné videá.

**Slabé:** veľmi malé využitie portrétového formátu, žiadny čitateľný úvodný predmet vo vlastnom obraze a aspoň štyri posledné pozorované sekundy na rovnakej CTA. Bez posluchu nedokážeme posúdiť, či výrok začína samostatne alebo je vytrhnutý z nadväznosti.

**Verdikt remesla:** rámovanie a prístup k reči cez text **slabé**; samostatnosť pasáže, pointa a zvuk **neoverené**. Žiadna snímka sama nepreukazuje, že videu chýba vtip alebo že hovorí niečo nezrozumiteľné.

## 8. @k_skokan1 / YouTube @fikiballing — päť skutočne prezretých videí

Všetkých päť súborov je presne spojených s výberovými ID. Všetky časované strany nižšie boli skutočne otvorené. Pôvodné zdrojové epizódy nie sú paralelne prezreté, preto viditeľné hotové titulky, rozloženie alebo efekty nemusia byť celé novou prácou klipera. Zvuk a plynulosť neboli posúdené.

### A. `yu2pUUBNoZs` — Fikiho aktuálna forma

[Verejný klip](https://www.youtube.com/shorts/yu2pUUBNoZs) · [MP4](../../../../../research/konkurencia/zdroje/2026-10-27-nocny-research/media/youtube/yu2pUUBNoZs/source.mp4) · [otvorených 16 snímok](../../../../../research/konkurencia/zdroje/2026-10-27-nocny-research/evidence/zle-detail/yu2pUUBNoZs/page-1.jpg). 31,681 s, 720 × 1280; upload podľa získaného `source.info.json` 1. 10. 2026.

**Pozorované:** 0,1 s je rozmazaný stav, 0,5–2,5 s váha s chodidlami a kurzorový grafický prvok, v 6–8 s pohľad do zrkadla, v 10 s výrazný nápis `game over`, v 12 s menší otočený/perspektívny panel a veľká ruka-kurzor. V 15–20 s je detail trupu. V 25 s je dvojriadková výzva, že divák videl iba polovicu a zvyšok je na fiki.sk. V 29,681 / 30 / 31,431 s vidíme logo CapCut na čiernej.

**Silné:** konkrétny predmet — váha — sprístupňuje fyzickú tému aj bez zvuku. Mierka sa mení podľa predmetu a zrkadla. Je tu aspoň rozpoznateľný vizuálny vtip s `game over`.

**Slabé/zmiešané:** veľa plochy vypĺňa rozmazané opakovanie; kurzor a otočený panel zaberajú priestor, no ich význam voči reči nebol doložený. Na konci zostalo cudzie editačné outro. Nepreberáme to ako nový klientsky štandard. **Verdikt:** nápad a orientácia **zmiešané**, čistota finálneho exportu **slabá**, slovný hook a pointa **neoverené**.

### B. `JVWXlJMkesg` — titulok kanála o manželke; obraz pri fľaši a nakupovaní

[Verejný klip](https://www.youtube.com/shorts/JVWXlJMkesg) · [MP4](../../../../../research/konkurencia/zdroje/2026-10-27-nocny-research/media/youtube/JVWXlJMkesg/source.mp4) · [otvorených 19 snímok](../../../../../research/konkurencia/zdroje/2026-10-27-nocny-research/evidence/zle-detail/JVWXlJMkesg/page-1.jpg). 49,521 s, 720 × 1280; upload 1. 10. 2026.

**Pozorované:** rovnaký rozmazaný/kurzorový úvod; 1–15 s je ruka s priehľadnou fľašou Voss, v 20 s grafický novinový rám s portrétom, v 25 s nákupný vozík, v 30–40 s obchodné regály a nápoje. V 45 s výzva na web; v 47,521 / 49,271 s CapCut logo. Vo vzorkách nie je priebežný čitateľný prepis.

**Silné:** konkrétne predmety a prostredie majú potenciál niesť vysvetlenie; novinový rám je samostatný grafický nápad. **Slabé:** predmet zostáva v malom vodorovnom páse s rozmazanými rezervami, prepis chýba vo vzorke a outro prezrádza nedotiahnutý export. Z rozdielu medzi názvom a predmetmi sa **nevyvodzuje nesúlad**: bez reči nevieme, či hovorenie o manželke sprevádza tieto zábery. **Verdikt:** vizuálne dokončenie **slabé/zmiešané**, významový súlad **neoverený**.

### C. `Ep-D-TkGlKY` — Nikdy si nenechaj skákať po hlave

[Verejný klip](https://www.youtube.com/shorts/Ep-D-TkGlKY) · [MP4](../../../../../research/konkurencia/zdroje/2026-10-27-nocny-research/media/youtube/Ep-D-TkGlKY/source.mp4) · [otvorených 19 snímok](../../../../../research/konkurencia/zdroje/2026-10-27-nocny-research/evidence/zle-detail/Ep-D-TkGlKY/page-1.jpg). 50,661 s, 720 × 1280; upload 3. 10. 2026.

**Pozorované:** malý vodorovný Fikiho štúdiový záber, rozmazané horné a dolné výplne, drobný biely postupne meniaci sa text pod rečníkom. V 0,1–2,5 s je navyše viditeľná horná lišta s položkami typu `Artist` a pri viacerých snímkach značka `Captions by Dubs`. Telo 4–40 s zostáva na rečníkovi. V 45 s veľké CTA prekrýva menší pokračujúci text; v 48,661 / 50,411 s CapCut outro.

**Silné:** na rozdiel od predchádzajúcich príkladov existuje priebežný prepis, ktorý sprístupňuje argument. Gestá a tvár nie sú vyrezané. **Slabé:** čítanie trpí malou mierkou, cudzími UI/značkami a súbehom CTA s prepisom. Presnosť prepisu bez posluchu nie je potvrdená. **Verdikt:** sprístupnenie reči **zmiešané**, finálna čistota **slabá**, argument a pointa **neoverené**.

### D. `7aswyut_8ko` — Sú to neschopní ľudia

[Verejný klip](https://www.youtube.com/shorts/7aswyut_8ko) · [MP4](../../../../../research/konkurencia/zdroje/2026-10-27-nocny-research/media/youtube/7aswyut_8ko/source.mp4) · [otvorená strana 1, 20 snímok](../../../../../research/konkurencia/zdroje/2026-10-27-nocny-research/evidence/zle-detail/7aswyut_8ko/page-1.jpg) · [otvorená strana 2, 1 snímka](../../../../../research/konkurencia/zdroje/2026-10-27-nocny-research/evidence/zle-detail/7aswyut_8ko/page-2.jpg). 59,701 s, 720 × 1270; upload 7. 10. 2026.

**Pozorované:** v 0,1 / 0,5 s veľká explózia, v 1 / 1,5 s dym. Od 2,5 s sa číta rečník pri notebooku, vľavo stojaca postava a pod obrazom dvojriadkový červený prepis. Pozadie opakuje zväčšený rozmazaný zdroj. Značka `Captions by Dubs` ostáva hore. V 55 s je ohnivá grafika a zároveň text reči/CTA; v 57,701 / 59,451 s iba web na čiernej.

**Silné:** konkrétny obraz a priebežné frázy umožňujú sledovať aspoň časť argumentu; dve textové riadky majú čitateľnejšiu mierku než v C. **Slabé:** explózia zakrýva vstupný predmet aj tvár, červený text prechádza cez pestrý podklad a koniec kombinuje niekoľko vrstiev. Funkcia explózie voči prvej vete nie je doložená. **Verdikt:** obsahové vrstvy **zmiešané**, úvod a čistota hierarchie **slabé**; neoznačuje sa za dôkaz, že chýba akýkoľvek edit.

### E. `qUFvPLP0wQs` — To nie je nič nové pre nich

[Verejný klip](https://www.youtube.com/shorts/qUFvPLP0wQs) · [MP4](../../../../../research/konkurencia/zdroje/2026-10-27-nocny-research/media/youtube/qUFvPLP0wQs/source.mp4) · [otvorená strana 1, 20 snímok](../../../../../research/konkurencia/zdroje/2026-10-27-nocny-research/evidence/zle-detail/qUFvPLP0wQs/page-1.jpg) · [otvorená strana 2, 1 snímka](../../../../../research/konkurencia/zdroje/2026-10-27-nocny-research/evidence/zle-detail/qUFvPLP0wQs/page-2.jpg). 60,967 s, 720 × 1270; upload 7. 10. 2026.

**Pozorované:** explózia/dym v 0,1–1,5 s, potom výrazne väčšia portrétová tvár a notebook v 2,5–20 s. Červený prepis sa mení po frázach. V 25 / 30 s je iná hovoriaca žena ako citovaný podnet; v 35–55 s sa vracia Fiki. V 58,967 / 60,717 s je jednoduché CTA. Hore je `Captions by Dubs`.

**Silné:** oveľa lepšie využitý portrét než v A–C; tvár je veľká, reč má priebežný text a vzorka ukazuje konkrétny podnet → návrat ku komentáru. Toto je **konkrétny protipríklad príliš plošnej známky ZLE**: niektoré základné editorské operácie autor preukázateľne robí.

**Slabé/zmiešané:** všeobecná explózia odďaľuje identifikáciu hovoriaceho, červené titulky môžu mať slabší kontrast na rukách/notebooku a zostáva cudzia značka. To, či zachoval presnú logiku citácie, treba preveriť z reči. **Verdikt:** rámovanie a viditeľná skladba **zmiešané až funkčné**, dokončenie **zmiešané**, zvuk a presný slovný kontext **neoverené**.

**Záver k autorovi:** vzorka podporuje kritiku finálneho exportu, konzistencie a účelnosti šablón. Nepodporuje tvrdenie, že nevie použiť titulky, zmeniť kompozíciu alebo ukázať podnet. Rozdiel medzi E a prvými videami je viditeľný aj bez hodnotenia views. Videá sú z 1.–7. októbra; nevypovedajú o aktuálnom posune po historickom hodnotení.

## 9. @tomassykorawhysteve / YouTube @the_best_of_fiki — päť skutočne prezretých videí

### A. `EVe-STAzvzo` — Ako fungoval Epstein?

[Verejný klip](https://www.youtube.com/shorts/EVe-STAzvzo) · [MP4](../../../../../research/konkurencia/zdroje/2026-10-27-nocny-research/media/youtube/EVe-STAzvzo/source.mp4) · [otvorená strana 1, 20 snímok](../../../../../research/konkurencia/zdroje/2026-10-27-nocny-research/evidence/zle-detail/EVe-STAzvzo/page-1.jpg) · [otvorená strana 2, 17 snímok](../../../../../research/konkurencia/zdroje/2026-10-27-nocny-research/evidence/zle-detail/EVe-STAzvzo/page-2.jpg). 139,001 s, 720 × 1280; upload 5. 10. 2026.

**Pozorované:** 0,1 / 0,5 s portrét v kontexte názvu videa, 1 / 1,5 s Fiki na gauči, 2,5 / 4 s reakčný výrez The Rock, potom návrat na rečníka. V 40 s je snímka e-mailového dokumentu; v 80 s detail tváre, väčšina ďalších sampled miest zostáva na širšom gauči. V 125 / 130 s je viditeľné prekrývanie stavov obrazu; jeho presná plynulosť a funkcia nie sú overené. V 135 / 137,001 / 138,751 s CTA. Priebežný prepis vo vzorkách chýba.

**Silné:** autor používa identifikáciu osoby, reakčný obraz, konkrétny dokument a zmenu mierky. Nejde o video bez obrazových nápadov. **Slabé:** všetko ostáva v malom vodorovnom páse uprostred portrétového súboru. Dlhé úseky významovo nemožno sledovať bez zvuku a dokument v tejto mierke neprenáša čitateľnú podrobnosť na malom náhľade. Pravdivosť dokumentu a tvrdení sa tu neoverovala. **Verdikt:** nápad **zmiešaný**, mobilná čitateľnosť **slabá**, úplnosť dlhého argumentu a význam reakcie **neoverené**.

### B. `TRodq0pMkJ8` — Že vraj ultimátny hlupák?

[Verejný klip](https://www.youtube.com/shorts/TRodq0pMkJ8) · [MP4](../../../../../research/konkurencia/zdroje/2026-10-27-nocny-research/media/youtube/TRodq0pMkJ8/source.mp4) · [otvorených 17 snímok](../../../../../research/konkurencia/zdroje/2026-10-27-nocny-research/evidence/zle-detail/TRodq0pMkJ8/page-1.jpg). 40,701 s, 720 × 1280; upload 27. 9. 2026.

**Pozorované:** 0,1–15 s vľavo dva malé citované/reakčné panely a vpravo väčší Fiki pri notebooku; v ľavom paneli je viditeľný titulok k téme. V 20 / 25 / 30 s zostáva iba Fiki. V 35 / 38,701 / 40,451 s CTA. Priebežný prepis hlavnej reči nie je viditeľný.

**Silné:** podnet a reakcia sú najprv súčasne dostupné, potom sa kompozícia zjednoduší na hovoriaceho. **Slabé:** v už malom stredovom páse sú vložené ešte menšie tváre/text; pri pohľade na celú portrétovú plochu vzniká veľmi nízka čitateľnosť. **Pôvod:** tento split mohol byť už v zdrojovej epizóde; bez nej nemožno celú skladbu pripísať novému kliperovi. **Verdikt:** viditeľná skladba **zmiešaná**, mierka **slabá**, presnosť citácie a pointa **neoverené**.

### C. `ogENGkwt5rQ` — Smutná realita

[Verejný klip](https://www.youtube.com/shorts/ogENGkwt5rQ) · [MP4](../../../../../research/konkurencia/zdroje/2026-10-27-nocny-research/media/youtube/ogENGkwt5rQ/source.mp4) · [otvorená strana 1, 20 snímok](../../../../../research/konkurencia/zdroje/2026-10-27-nocny-research/evidence/zle-detail/ogENGkwt5rQ/page-1.jpg) · [otvorená strana 2, 2 snímky](../../../../../research/konkurencia/zdroje/2026-10-27-nocny-research/evidence/zle-detail/ogENGkwt5rQ/page-2.jpg). 63,221 s, 720 × 1280; upload 29. 9. 2026.

**Pozorované:** 0,1–20 s Fiki pri bazéne; v 25 s prekrývanie prechodu, v 30 / 35 / 40 / 45 / 50 s rôzne filmové/postavové motívy vrátane klaunovskej postavy. V 55 / 60 / 61,221 / 62,971 s CTA. Priebežný prepis vo vzorkách chýba.

**Silné:** existuje vedomý kontrast komentára a filmovej montáže, nie iba statická šablóna. **Slabé/otvorené:** obraz stále používa iba malý vodorovný pás; z fotografických stavov nevieme, či filmové motívy rozvíjajú konkrétne slová alebo ide o náladovú montáž. Bez hudby/hlasu nemožno hodnotiť rytmus ani vhodnosť skladby. **Verdikt:** obrazový nápad **zmiešaný**, čitateľnosť **slabá**, významová účelnosť montáže **neoverená**.

### D. `H3-pZIM8Kx8` — Fiki rage core

[Verejný klip](https://www.youtube.com/shorts/H3-pZIM8Kx8) · [MP4](../../../../../research/konkurencia/zdroje/2026-10-27-nocny-research/media/youtube/H3-pZIM8Kx8/source.mp4) · [otvorená strana 1, 20 snímok](../../../../../research/konkurencia/zdroje/2026-10-27-nocny-research/evidence/zle-detail/H3-pZIM8Kx8/page-1.jpg) · [otvorená strana 2, 4 snímky](../../../../../research/konkurencia/zdroje/2026-10-27-nocny-research/evidence/zle-detail/H3-pZIM8Kx8/page-2.jpg). 74,341 s, 720 × 1280; upload 6. 10. 2026.

**Pozorované:** sampled miesta 0,1–45 s ukazujú rôzne výrazné gestá a tváre Fikiho pri stole. V 50 / 60 s je farebný televízny testovací obraz, v 55 / 65 s návrat na Fikiho; v 70 / 72,341 / 74,091 s CTA. Titulky nie sú vo vzorke viditeľné.

**Silné:** výber výraznej mimiky a gest má vizuálny potenciál aj bez ďalších fotografií. **Slabé:** malá aktívna plocha v portrétovom súbore, chýbajúce sprístupnenie replík; testovací obraz bez prehratia nepotvrdzuje dobrú komickú interpunkciu. **Verdikt:** potenciál fyzickej reakcie **zmiešaný**, finálna mierka **slabá**, komický rytmus a zásah do kontextu **neoverené**.

### E. `h_jEqNqqsx8` — True Feminizmus

[Verejný klip](https://www.youtube.com/shorts/h_jEqNqqsx8) · [MP4](../../../../../research/konkurencia/zdroje/2026-10-27-nocny-research/media/youtube/h_jEqNqqsx8/source.mp4) · [otvorená strana 1, 20 snímok](../../../../../research/konkurencia/zdroje/2026-10-27-nocny-research/evidence/zle-detail/h_jEqNqqsx8/page-1.jpg) · [otvorená strana 2, 17 snímok](../../../../../research/konkurencia/zdroje/2026-10-27-nocny-research/evidence/zle-detail/h_jEqNqqsx8/page-2.jpg). 137,2 s, 720 × 1280; upload 3. 10. 2026.

**Pozorované:** Fiki pri notebooku 0,1–2,5 s, v 4 s priehľadnejší meme panel s nápisom `the voices`, v 20 s iná scéna v bielej vypolstrovanej miestnosti. Väčšina ďalších 5-sekundových vzoriek do 90 s ukazuje pôvodný štúdiový rám, v 95 s detail tváre. V 100 s je čierna snímka, v 105 / 110 s filmové titulky `Executive Producer`, v 115–125 s späť Fiki. V 130 / 135 / 135,2 / 136,95 s CTA.

**Silné:** aspoň dva doplnkové obrazové nápady, zmena mierky a rozpoznateľný záverečný titulkový vtip. **Slabé/otvorené:** takmer celý dlhý klip používa malý stredový pás bez viditeľného prepisu. Titulkový vtip je vložený pred ďalším návratom na reč; bez posluchu nevieme, či vytvára účelnú pauzu alebo zbytočne preruší argument. **Verdikt:** nápad **zmiešaný**, mobilná čitateľnosť **slabá**, účelnosť dĺžky, humor a pointa **neoverené**.

**Záver k autorovi:** všetkých päť ukážok preukazuje opakovaný problém veľkosti aktívneho obrazu a slabý prístup k reči bez posluchu. Niektoré zároveň obsahujú reálne vlastné alebo prevzaté obrazové nápady, dokument, reakčný meme, citovaný podnet a filmovú montáž. Záver preto je „slabšie finálne spracovanie mobilnej plochy“, nie „nemá žiadne nápady“. Vzorka je z 27. 9.–6. 10.; nepreukazuje dnešnú kvalitu nových editov po historickom ratingu.

## 10. Súhrn piatich TikTokov @emus_iik podľa rovnakej osnovy

| Kritérium | Pozorovaný výsledok v piatich dostupných videách | Čo zostáva otvorené |
|---|---|---|
| Samostatnosť výberu a kontext | Situačný nadpis pri scénke a jedlo v IRL klipe dávajú viditeľný kontext. Bazénové komentáre ho bez zvuku sprístupňujú slabo. | Orientačný význam troch komentárov dopĺňa sekcia 13; presná korektúra, jedlo/scénka a plný zdroj potrebujú ďalšiu kontrolu. |
| Hook, vývoj, pointa | Viditeľný nápad pri „kamošovi z erazmu“, konkrétny podnet a reakčné tváre pri jedle. | ASR dopĺňa oblúk troch komentárov vrátane dvoch opakovaných teaserov (sekcia 13). Jedlo a scénka zostávajú významovo neoverené; úplný posluch všetkých chýba. |
| Význam vložiek a humor | Pri Kuciakovi úvodný portrét; pri ostatných vzorka prevažne využíva už natočený dej. | Portrétova presná identita/autorstvo a slovná kotva; či je humor v hovorení alebo pridanom strihu. |
| Čitateľnosť, crop, titulky | Opakovaný slabý bod: malá šírková vložka v štyroch portrétových súboroch. Jedno video je natívne široké; jeho padding je iba na našom hárku. Priebežný prepis nie je v troch bazénových vzorkách viditeľný; scénka má iba stály malý nadpis. | Zväčšenie treba skúšať s gestami a potrebnými objektmi, nie slepo orezať všetko na hlavu. |
| Pohyb a rytmus | Zaznamenané odlišné stavy, gestá a zmeny záberu. | Plynulosť, presný strih a rytmus ostávajú neoverené; kontakt nie je prehratie. |
| Hlas, hudba, SFX | **Neoverené.** | Päť súborov obsahuje audio stream, ale nebolo vypočuté. |
| Vlastný nápad a opakovateľnosť | Konzistentná zelená CTA, čiernobiely/farebný úvod, situačný nadpis a jednoduchý portrét. | Pôvodná epizóda nie je paralelne otvorená, preto editora nemožno označiť za autora všetkých titulkov alebo záberov. |

**Záver emusovej konkrétnej vzorky:** vidíme opakované slabiny finálnej mobilnej kompozície a titulkov, ktoré dávajú starému negatívnemu hodnoteniu určitú oporu v týchto vlastnostiach. Zároveň vidíme funkčný situačný nápad a konkrétne reakčné tváre. Nemáme podklad na tvrdenie, že každý edit autora je zlý. Vysoký či nízky počet views sa pri tomto verdikte nepoužil ako kritérium remesla. Zvyšných dvoch autorov už pokrývajú samostatné skutočné pozorovania v sekciách 8 a 9.

## 11. Výkon a staré hodnotenie ako oddelený kontext

Tieto údaje boli známe z existujúcich meraní pred čítaním; tento priechod sa preto **neoznačuje za plne zaslepený experiment**. Samotné obsahové nálezy vyššie sú naviazané na otvorené snímky a ich časy.

| TikTok @fiki.unrealized | Views pri zbere 27. 10. | Starší výberový dôvod |
|---|---:|---|
| `7691372489355627798` | 6 310 | Maximum |
| `7689781792898960662` | 5 016 | Druhý silný výsledok |
| `7689787906009074967` | 768 | Video vybrané pri mediáne |
| `7691643187244387606` | 280 | Nižší kvartil |
| `7692132409495653654` | 283 | Posledný upload |

Celý účet mal v zbere desať videí, 15 225 views, medián 525,5 a posledný upload z 2. októbra. Čerstvé načítanie teda neznamená čerstvé videá po historickom hodnotení. Týchto päť starších uploadov **nevie overiť, či sa autor remeselne zlepšil po 7. októbri**. Dve z videí majú tisíce views aj s doloženými slabinami rámovania; to je ďalší dôvod neprevádzať views priamo na známku kvality alebo na dôkaz účinku určitého efektu.

## 12. Spoločný férový záver a ďalší krok

Pri všetkých troch autoroch vidíme konkrétne spracovateľské slabiny. U emusa a tomassykorawhysteve najmä opakovaný malý široký obraz v portrétovom súbore a slabé sprístupnenie reči cez text; u skokana navyše zvyšné exportové/tool značky a málo zdôvodnené šablónové úvody. **Historické označenie ZLE má oporu v niektorých pozorovaných vlastnostiach týchto konkrétnych starších exportov. Nemá oporu ako tvrdenie, že nevedia nič alebo že sú dnes automaticky slabší v každom aspekte.** Skokanov portrétový klip E a emusova situačná ukážka sú konkrétne protiklady plošného znehodnotenia.

Všetkých 15 skúmaných uploadov pochádza spred historického ratingu alebo z rovnakého dňa. Skontrolovali sme ich skutočné edity v zachovaných verejných súboroch; **neskontrolovali sme tým žiadne nové video publikované po 7. októbri**. Ak účty nemajú dostupné novšie uploady, ich neskorší remeselný posun zostáva neoverený, nie automaticky nulový.

1. Orientačný význam z dostupného ASR už dopĺňa sekcia 13: 15 súborov prečítaných, 13 aspoň čiastočne použiteľných, dva nespoľahlivé. Zostáva opravený presný prepis a pôvodný Fikiho kontext; oddeliť editorove vrstvy od už hotového zdroja. ASR nie je dôkaz posluchu.
2. Pohybové alebo zvukové závery doplniť až po skutočnej príslušnej kontrole.
3. Porovnať rovnaké vlastnosti s našou vzorkou a úspešnými autormi: mierku tváre/objektu, funkciu titulkov, kontext vstupu, významovú kotvu vložky a čistotu výstupu. Neprideľovať univerzálne skóre za počet efektov.
4. Tento prvý vizuálny priechod sám nezakladá rebríček celej skupiny ani odhad vyradenia. Pre nasledujúcu výrobu poskytuje konkrétne chyby, ktoré dokážeme kontrolovať a opravovať aj na vlastných klipoch.

Tento výstup je samostatný prvý obsahový priechod. `STAV.json`, výberové manifesty, akvizičný helper a médiá neboli týmto hodnotiteľom zmenené; vznikli iba výskumné snímky v `evidence/zle-detail/` a tento rozbor.

## 13. Doplnenie významu zo surového ASR — 28. 10. 2026

Tento doplnok **neopakuje vizuálny audit** a nepridáva posluch. Všetkých 15 dostupných ASR súborov bolo teraz prečítaných vrátane časovaných segmentov. Trinásť má aspoň orientačne použiteľný význam; pri jedle a scénke z Erasmu je automatický prepis na rekonštrukciu pointy nespoľahlivý. Slovná dôvera v tabuľke hodnotí čitateľnosť textového prepisu, nie pravdivosť Fikiho tvrdení ani kvalitu hlasu. Časové kotvy sú surové ASR, nie ručne overený strih.

Výsledky nižšie spresňujú skoršie „samostatnosť/pointa neoverené“: teraz sa dá v trinástich prípadoch aspoň orientačne pomenovať téma a vývoj, pri časti aj uzáver. Skutočný posluch, presná korektúra, pravdivosť tvrdení a porovnanie s celou epizódou stále chýbajú. Nula alebo nepresný segment nie sú dôkaz ticha či chyby editora. Obrazový podnet môže byť už v zdrojovej epizóde; ani dobrá významová väzba automaticky nedokazuje nové autorstvo klipera.


### @k_skokan1 — význam a úprava pôvodného verdiktu

| Klip / surový zdroj | Rozsah dôvery | Hook → kontext → pointa podľa ASR | Väzba na už prezretý obraz, neistota a prenos |
|---|---|---|---|
| [yu2pUUBNoZs](../../../../../research/konkurencia/zdroje/2026-10-27-nocny-research/prepisy/e6a83647eb93a1fb72e5109a6359e60ef9552946f0e53810041abe30677b950c.json) | Orientačne použiteľný, miestami výrazne chybný. | 0–5,32 s: reakcia na hodnotu 100,8 na váhe; konkrétny predmet je hneď jasný. 5,64–23,02 s: vzhľad postavy, ketóny a časový komentár, viaceré slová sú skomolené. 26,44–28,92 s: odbočenie ku vzhľadu/vlasom; nie úplne jednoznačne dopovedaná pôvodná váhová pointa. | Váha a zrkadlo významovo súvisia s rečou; game over môže byť reakčný akcent, jeho presný vtip bez posluchu nepotvrdíme. UI/kurzor zostáva slabo zdôvodnený. Prítomný konkrétny začiatok spresňuje staré neoverené; zvukové zakončenie ostáva otvorené. |
| [JVWXlJMkesg](../../../../../research/konkurencia/zdroje/2026-10-27-nocny-research/prepisy/020d85be80adf4f9dc20e21135b60e55ad8ed8002edf5c1c811e6363e943ba0e.json) | Orientačne použiteľný; replika o kariére je chybná. | 0–15,8 s: drahá voda ako dopriatie počas pôstu a menovanie značiek. 15,92–26,36 s: krátka otázka o kariére a odpoveď druhej osoby, v ASR silno deformovaná. 26,36–41,86 s: návrat k výberu vôd; posledná veta 44,2–46,54 s je nespoľahlivá. | Názov o manželke nie je úplne bez súvislosti: ASR zachytí krátku kariérnu vsuvku a pri 20 s je už pozorovaný novinový rám. Celok však prevažne rozvíja nákup vôd. Nevyhlasujeme úplný nesúlad ani celú manželkinej tému za dopovedanú. Pôvod vsuvky/novinového rámu je neistý. |
| [Ep-D-TkGlKY](../../../../../research/konkurencia/zdroje/2026-10-27-nocny-research/prepisy/7b4a85444ce0577327c1437c645efbc538de243cab01e4be8e1d4eb8d0d2cc3a.json) | Použiteľný na hlavnú myšlienku do ≈42,9 s; koniec slabý. | 0–7,44 s: ľudia môžu utláčať, treba sa vedieť brániť. 7,56–34,18 s: fyzická, slovná a právna obrana, séria schopností. 34,34–42,86 s: návrat k ústrednej zásade nenechať so sebou zametať. Posledná veta 42,96–48,74 s je poškodená a nemožno ju presne zhrnúť. | Má rozvinutie aj návrat k téze, preto argument už nie je celý neoverený. Autorov výber môže fungovať ako monológ bez B-rollu; zistené UI/značky, mierka a CTA kolízia ostávajú reálne slabiny. Ide o obsah hovoreného postoja, nie audit zákonov alebo odporúčanie použiť násilie. |
| [7aswyut_8ko](../../../../../research/konkurencia/zdroje/2026-10-27-nocny-research/prepisy/dbf0157a274cefd558ac8a769c7c4bf291c16c8ba8b9ee1c0ec736a682e4b1a1.json) | Orientačne použiteľný; názov skupiny a časť záveru chybné. | 0–9,26 s: hodnotenie vzhľadu určitého človeka, prvé jeho predpokladá referent. 9,64–37,62 s: generalizácia skupiny na slabosť, potrebu regulácií a EÚ. 37,82–55,68 s: príklady reakcie na humor a návrat k označeniu danej skupiny. | Vľavo už pozorovaná postava môže poskytovať referent prvého jeho, identita však nie je potvrdená. Výbuch v 0,1–1,5 s nevyplýva z úvodnej témy vzhľadu; vo vzorke je dekoratívny a zakrýva referent, presný zvuk nepoznáme. Rozbor nepreberá skupinové urážky ako fakty. |
| [qUFvPLP0wQs](../../../../../research/konkurencia/zdroje/2026-10-27-nocny-research/prepisy/159a2af64731620711e73ed114c6d7fd1901b14320705bcece85cedb805ba81c.json) | Použiteľné telo ≈1,14–56,38 s; koncové opakované ďakujem vyradené. | 1,14–16,22 s: predstavenie influencerky a obvinenie z nepresného kontextu. 16,52–23,46 s: pomenovanie údajného zákonného tvrdenia. 23,58–29,74 s: citovaná replika, potom 30,66–55,36 s Fikiho výklad rozdielu medzi chôdzou a jazdou na chodníku. 55,72–56,38 s: krátky uzáver. | Konkrétna citácia → návrat ku komentáru je obsahovo podložená, nielen vizuálne naznačená. Spresňuje to pozitívny protipríklad autorovej skladby. Mená a právna správnosť sú neoverené; hlasový prechod nemožno určovať len ASR. Terminálne ďakujem v desiatkach nulových segmentov je chyba, nie počutá CTA. |

### @emus_iik — význam a úprava pôvodného verdiktu

| Klip / surový zdroj | Rozsah dôvery | Hook → kontext → pointa podľa ASR | Väzba na už prezretý obraz, neistota a prenos |
|---|---|---|---|
| [7691372489355627798](../../../../../research/konkurencia/zdroje/2026-10-27-nocny-research/prepisy/9941d658dc1823fbee0f4ed9911a64c8c9dbedde956f3f6c9fd35c883d365a01.json) | Použiteľná hlavná argumentácia; mená a faktické tvrdenia neoverené. | 0–6,4 s: prísľub kontroverzného názoru o Kuciakovi. 7,1–20,24 s: Fiki definuje vlastný pojem hrdinstva. 20,36–39,56 s: tvrdí, že dotyčný nepredpokladal smrteľné nebezpečenstvo, a vracia sa k svojej definícii. | Hook má pomenovaný predmet aj prísľub, úvodný portrét preto má konkrétnu slovnú kotvu. Nie je fér označiť celý výber za významovo neprístupný len preto, že nemá titulky. Malá mobilná mierka a chýbajúci vizuálny prepis sa nemenia. Hovorené historické tvrdenia audit nepotvrdzuje. |
| [7689781792898960662](../../../../../research/konkurencia/zdroje/2026-10-27-nocny-research/prepisy/5559c2a158ede0804d09f584e8fc03676e2299f5b416d845dc3aaab2a4f3633d.json) | Nepoužiteľný na spoľahlivý význam. | ASR opakuje Čo je to naši aj cez koniec; nezhoduje sa s už videnými titulkami strašne veľký kus / skoro som sa zadusila. Ani ojedinelé slovo pripomínajúce sushi neoprávňuje rekonštruovať celú konverzáciu. Z ASR neurčujeme hook, presnú reakciu ani pointu. | Zostáva pôvodný vizuálny opis konkrétneho jedla a striedania účastníkov; nepreberá sa halucinovaná replika. Potrebný je skutočný posluch a opravený prepis, bez nového automatického ASR behu v tomto audite. Pôvod titulkov a zmien záberu je stále neistý. |
| [7689787906009074967](../../../../../research/konkurencia/zdroje/2026-10-27-nocny-research/prepisy/3c0479dbfaa7e75a791c26e232a1f19bc16ca2569225ad2fac7afabade83575b.json) | Nespoľahlivý pre presný význam a pointu; iba niekoľko rozpoznateľných motívov. | V 0–23,2 s má ASR prevažne nezrozumiteľné slabiky; možno rozoznať motívy drift king a zvukovo podobný Fast and Furious, nie dôveryhodný súvislý prepis. Koniec obsahuje opakovanie tej istej frázy a množstvo nulových segmentov. Z cudzojazyčne pôsobiacich slabík nevyrábame preklad. | Situačný hook zostáva doložený iba už prečítaným nadpisom o kamarátovi po Erasme. ASR nepotvrdzuje jeho príbeh ani dopovedanie. Čierny stav pri 6 s tiež nevysvetlí. Kontrola zvuku je skutočný ďalší krok, nie nový automatický kvalitný verdikt podľa názvu. |
| [7691643187244387606](../../../../../research/konkurencia/zdroje/2026-10-27-nocny-research/prepisy/72aebf48f04c50bdb0ecf38d6b6fff17d92624c8ee4481c267aed461bd5c5201.json) | Použiteľný obsahovo, názov básne/roky/meno potrebujú opravu. | 0–6,36 s: verš a znevažujúca reakcia. 6,72–20,9 s: školské učenie literatúry a uvedenie Mor ho!. 21,06–31,82 s: citovanie veršov; 32–36,06 s zopakovanie úvodnej reakcie, potom 36,12–51,48 s hodnotenie diela a obdobia. | Opakovaný verš a reakcia podporujú zámerný teaser z neskoršieho tela pred farebným kontextom. To je konkrétne pozitívne remeslo, ktoré z obrázkov nebolo možné pomenovať. Chýba čitateľná citácia básne/titulky; výrok o literárnej hodnote zostáva Fikiho názor, nie faktické overenie. |
| [7692132409495653654](../../../../../research/konkurencia/zdroje/2026-10-27-nocny-research/prepisy/e56c873d2b532ad629417d9240b0309e48a394aee9c18b180de2f9e0b7886bd6.json) | Použiteľný hlavný oblúk; technologický názov v ASR chybný. | 0–6,34 s: otázka, čo je investigatívne na Google vyhľadávaní. 6,8–12,18 s: všeobecná téza o novinároch. 12,34–18,86 s: zopakovaná úvodná veta, potom 19–32,22 s kontrast s vyšetrovaním a príklad zmlúv/AI. 33,16–34,12 s: záverečné pomenovanie. | Aj tu ASR podporuje vyzdvihnutú vetu → kontext → opakovanie, nie len náhodný odfarbený úvod. Téma a pointa sú orientačne dostupné. Ilustrácia dokumentu by mohla pomôcť, ale nie je nutné ju vymyslieť ako dôkaz novinárovej skutočnej práce. Zvuk ani úplný zdroj nie sú skontrolované. |

### @tomassykorawhysteve — význam a úprava pôvodného verdiktu

| Klip / surový zdroj | Rozsah dôvery | Hook → kontext → pointa podľa ASR | Väzba na už prezretý obraz, neistota a prenos |
|---|---|---|---|
| [EVe-STAzvzo](../../../../../research/konkurencia/zdroje/2026-10-27-nocny-research/prepisy/ae87aaf439e9e53ff9fa06904c27948e739359814ce7f20780330744b486f0d2.json) | Použiteľný naratív; mená, dokument a závažné tvrdenia neoverené. | 0–24,78 s: predstavenie vplyvnej spoločenskej siete. 24,86–41,62 s: rozprávanie o údajnom e-maile. 42,84–81,54 s: hypotetická situácia diplomata, potom 84,42–115,38 s dve možnosti reakcie. 116,44–133,2 s: špekulatívny záver o vydieraní/nahrávaní. | Pozorovaný dokument pri 40 s má obsahovú väzbu na práve rozprávaný e-mail; jeho pravosť a tvrdenia o osobách tým nie sú dokázané. Scenár s diplomatom je v reči hypotetický a nepreberáme ho ako zistenie o konkrétnom človeku. Dlhý oblúk má záver, no malá mierka a nečitateľný dokument zostávajú. |
| [TRodq0pMkJ8](../../../../../research/konkurencia/zdroje/2026-10-27-nocny-research/prepisy/6c4d680085918dd262636ca650e118a1f6f104b6bef99314ee08836d502b65e8.json) | Použiteľná citácia a odpoveď, presné hlasy neoverené. | 0,46–16,14 s: kritika Fikiho kvôli hlúposti/pozornosti. 16,52–27,7 s: Fiki preformuluje domnelý rozpor kritiky. 27,88–32,8 s: zhrnie, že výhrada sa aj tak vracia k ragebaitu. | Má kompaktnú citáciu → rozbor → poslednú odpoveď; podporuje funkciu úvodných viacerých panelov a ich následného zjednodušenia. Netvrdíme správnosť jeho logickej interpretácie ani vernosť plnej kritike. Pôvod panelov môže byť vo Fikiho zdroji; mobilná mierka ostáva slabá. |
| [ogENGkwt5rQ](../../../../../research/konkurencia/zdroje/2026-10-27-nocny-research/prepisy/6cfb89991f84962cf535957648ecb43b1c5e8753d42d1240ba86448674900b22.json) | Použiteľný myšlienkový oblúk, meno v ASR neoverené. | 0–19,18 s: provokatívna otázka a téza o viditeľnom/neviditeľnom trápení. 19,28–45,1 s: hypotetický príklad človeka s rodinným bremenom a porovnanie uznania. 45,32–54,78 s: návrat k pôvodnej téze. | Filmová montáž od ≈30 s sa môže vzťahovať k neviditeľnému trápeniu, ale nie je skutočným záznamom opísaného devätnásťročného človeka ani jeho rodiny. Nepripisujeme jej faktickú dôkaznú funkciu. Úvod a uzáver sú orientačne dopovedané; účel hudby, tempovanie montáže a prisúdenie identity stále chýbajú. |
| [H3-pZIM8Kx8](../../../../../research/konkurencia/zdroje/2026-10-27-nocny-research/prepisy/6a5e193e5dabd54e49fdd0e7de2c4e5e43fa787f6f8e5a7381ccba668421d35d.json) | Použiteľný spor/argument, mená a presné repliky chybové. | 0–11,36 s: námietka voči údajným dvom uhlom pohľadu, bez pomenovania dvojice. 11,84–30,76 s: dve noci v Bratislave a vypnutá poloha. 31,74–59,5 s: zosmiešňujúca rekonštrukcia vysvetlenia, potom 61,36–69,18 s návrat k opakovanému obvineniu z rovnakej výpovede. | Výrazné gestá už majú obsahový konflikt, ale kto sú obaja a čo presne povedali, nový divák bez citácie nevie. Testovací obraz pri 50/60 s môže byť interpunkcia/cenzúrny vtip, ASR ani snímka však nepotvrdzujú bleep alebo hudbu. Zvukový humor ostáva neoverený. |
| [h_jEqNqqsx8](../../../../../research/konkurencia/zdroje/2026-10-27-nocny-research/prepisy/e4035121f3f1986cb586b9768b817b0bbf4631f2a501a43ed9ef5527685481a4.json) | Použiteľná hlavná argumentácia; meno a závažné tvrdenia neoverené. | 0–44,76 s: hypotetický vlastný postoj pri strate kontroly a ublížení blízkym. 44,9–64,18 s: komentár k konkrétnej žene, ktorého skutkový podklad nebol kontrolovaný. 64,38–99,86 s: údajný spoločenský rozpor; 109,66–130,36 s: záverečné buď/alebo. | Meme k hlasom pri 4 s a vypolstrovaná miestnosť pri 20 s doslovne reagujú na reč o poruche/zavretí, no nejde o klinický obraz ani potvrdenie viny. Filmové credits okolo 105/110 s sú pri obsahovom prelome k záveru, nie definitívnym koncom. Ide o Fikiho sporné postoje; diagnózy a skupinové tvrdenia nepreberáme ako fakty. |

### Čo sa tým zmenilo a čo máme prevziať

- **Emus má dva konkrétne významové hooky z tela pasáže:** Mor ho! a Novinári opakujú úvodnú vetu neskôr v širšom kontexte. Preto je férový záver „slabšia mobilná mierka a dostupnosť reči, ale prítomný výber a predohra“, nie „nemá žiadnu dramaturgiu“.
- **Skokanov qUFvPLP0wQs má podložený oblúk citácia → odpoveď.** Aj jeho Ep-D-TkGlKY drží jednu tézu a príklady; cudzie UI/outro a malá mierka sú samostatné problémy. Oprava týchto vecí nepotrebuje ďalšiu databázu GIFov.
- **Tomášove TRodq0pMkJ8 a ogENGkwt5rQ majú z prepisu čitateľný uzáver.** Dokument v Epsteinovi patrí do konkrétneho rozprávaného úseku, no treba z neho spraviť čitateľný a overený podklad. Nie je to prázdny obrázok bez významu; jeho pravdivosť ostáva otvorená.
- **Pri jedle/scénke si význam nevymýšľame.** Hoci existuje súbor ASR, dve položky neprešli ani základnou textovou dôveryhodnosťou. Fyzická dostupnosť a počet prepisov sa nesmú vykázať ako rovnaký počet pochopených klipov.
- **Výrobná pripravenosť:** vlastný portrét, opraviteľné titulky, správne zachovaný citát a teaser z tej istej pasáže sú prenosné postupy. Konkrétne dokumenty, čisté citácie a správne identity treba dohľadať/oddeliť od hotových referencií. Nie každý opísaný výskumný vizuál je registrovaný produkčný asset.

Pôvodný férový záver sa nemení na nové poradie kvality: staré ZLE má oporu v konkrétnych slabinách výstupu, ale poznáme aj funkčnú obsahovú skladbu. Všetky tieto uploady stále predchádzajú ratingu alebo sú z jeho dňa. Doplnenie ASR nepreukazuje dnešné zlepšenie po 7. októbri, účinok pravidelnosti, zvukové remeslo ani Adamovo tvorivé prijatie.

