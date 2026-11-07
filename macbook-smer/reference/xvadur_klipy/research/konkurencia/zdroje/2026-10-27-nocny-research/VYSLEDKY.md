# Čo vieme preniesť zo 100 referencií do našej výroby

Nočný výskum 27.–28. októbra 2026. **Najväčší prenos nie je univerzálny balík memov: je to rozdelenie pasáže na otázku, podnet, vysvetlenie a pointu a zmena obrazu práve pri zmene ich funkcie.** V úspešnej vzorke funguje aj jednoduchý portrét s presne vybranou vetou. Náročnejšie obrazy pomáhajú vtedy, keď ukazujú konkrétny predmet, vzťah alebo návrat na pointe. Naše posledné dva edity už túto druhú schopnosť viditeľne majú; ďalšou úlohou je opakovateľný výber a kontrola.

## Rozsah a hranice výsledku

- Pevná hlavná vzorka: **20 rôznych autorov × 5 konkrétnych TikTokov = 100 referencií**. Každý autor má samostatný rozbor nižšie. Pri všetkých vznikol čerstvý obsahový priechod cez skutočne otvorené obrazové dôkazy; pri existujúcich rozboroch sa prebrala overiteľná časť s pôvodom a znovu skontrolovali podstatné detaily.
- Kontrola: **15 starších videí od troch historicky ZLE autorov a 5 našich videí**. Celkom 120 zachovaných médií, 120 vizuálnych priechodov. Pri dvoch nedostupných TikTok účtoch ide o výslovne priradené YouTube náhrady.
- Všetkých 120 má fyzický zdroj, hash a technické metadáta. Dve generácie obrazových dôkazov ostávajú zachované; na presnejšie časy slúžia opravené zdrojové PTS a priame snímky. [Časová oprava a natívne rozmery](EVIDENCIA_CASOVANIA.md).
- **0 videí bolo v tomto výskume celé súvislo prehratých a 0 vypočutých.** Nevyhodnocujeme preto kvalitu mixu, zvukové efekty, plynulosť celého videa ani divácky pocit tempa. Podrobné vzorky dokazujú poradie a podobu konkrétnych zmien, nie úplný pohybový zážitok.
- Vzniklo 120 surových ASR súborov. Minimálnou kontrolou prítomnosti písmen prešlo 119; **to nie je 119 overených významov**. Jeden prepis bol iba interpunkcia, ďalší opakoval text proti viditeľným titulkom a tretí bol prevažne nezrozumiteľný. Čiastočná obnova prvého je zachovaná osobitne. [Kvalita ASR](prepisy-kvalita.json).

Výber autorov vychádza z mediánu views a minimálne desiatich uploadov v zmrazenom zbere 27. októbra. Je to výskumná vzorka úspešných účtov, **nie oficiálne TOP20 podľa kvality**. Metriky, pravidlá výberu a päť presných ID na autora sú v [VYBER.md](VYBER.md) a [vyber-100.json](vyber-100.json). Rozsah nezakladá poradie všetkých 82 ľudí.

## Dvadsať autorov: konkrétna schopnosť a konkrétna rezerva

Každý riadok odkazuje na päť individuálnych máp: hook, kontext, pointa, obrazové rozhodnutia, pôvod vrstiev, obmedzenia a uskutočnenie.

| Autor / rozsah | Čo je užitočné preniesť | Čo nekopírovať bez kontroly |
|---|---|---|
| [fikinko.shorts — 5/5](rozbory/fikinko.shorts.md) | Krátka otázka alebo téza, oddelená odpoveď, frázové titulky; často stačí samotný rečník. | Malý citovaný príspevok s UI; opakované čítanie nie je automaticky dobrý vtip. |
| [fiki.extra — 5/5](rozbory/fiki.extra.md) | Podnet v telefóne → plná plocha pre reakciu → návrat toho istého podnetu. Dobre rozdelené úlohy priestoru. | Drobné cudzie titulky a prudké textové výmeny; identita osoby nie je overená iba nápisom. |
| [fiki.hlasky — 5/5](rozbory/fiki.hlasky.md) | Aktívny rečník veľký; split, keď je dôležitý aj poslucháč. Portrét iba pri mene. | Príliš tesný alebo naopak malý zdroj, dlhá samostatná CTA. |
| [fikiclips1 — 5/5](rozbory/fikiclips1.md) | Pri fyzickej ukážke zachovať telo a priestor, pri reakcii potrebný podnet. | Dlhé malé podnetové okno, bledé titulky a obsahové opakovanie; chybný ASR nemožno prijať automaticky. |
| [fikisulik_klipyy — 5/5](rozbory/fikisulik_klipyy.md) | Jeden spoločný obraz → pomenovaný referent → návrat; SOWA a presná citácia s reakciou. | Erb cez tvár, slabá mierka živého výkonu, čierna koncová karta. Nie každý pohyb fotografie patrí kliperovi. |
| [fikirealtalk — 5/5](rozbory/fikirealtalk.md) | Argument má otázku, princíp a príklad; jedna krátka fráza vie nahradiť sériu dekorácií. | Predohra nesmie zmeniť význam; veľká URL nemá zabrať poslednú vetu. |
| [fikiframe — 5/5](rozbory/fikiframe.md) | Kontrast v jednej osi a krátky adresný portrét. Dobré vizuálne rozhodnutie môže trvať iba zlomok sekundy. | Nejasný kontext osoby; politický ilustračný obraz nie je doklad tvrdenia. |
| [fiki.sama — 5/5](rozbory/fiki.sama.md) | Pri zmene hovoriaceho meniť dominanciu obrazu; jednoduchý portrét aj doslovná metafora majú miesto. | Overená 2,7 s čierna medzera, delenie slova, sľub tabuľky bez doloženého naplnenia v prezretej vzorke. |
| [fiki.clipz — 5/5](rozbory/fiki.clipz.md) | Otázka sa po prečítaní uvoľní, citácia a odpoveď preberajú celú plochu, dva objekty pri vajci/sliepke. | Záver odpovede pod CTA; zbytočný meme by tu pridal prácu bez novej funkcie. |
| [fikimentalita — 5/5](rozbory/fikimentalita.md) | Pripravená neskoršia pointa, prirodzený dialóg a konzistentná parodická postava. | Z cudzej ilustrácie a replík nemožno odvodiť hotový lip-sync alebo pôvod hlasu. |
| [frajer.fiki — 5/5](rozbory/frajer.fiki.md) | Trojbodový argument má viditeľné čísla 1/2/3 na skutočných hraniciach; krátka identifikácia športovca pred ukážkou. | Doslovné emoji a ilustračná fotografia môžu vytvoriť neoverenú asociáciu; CTA zostáva samostatnou kontrolou. |
| [fikiprezident — 5/5](rozbory/fikiprezident.md) | Predmet → ilustrácia → návrat; pri vajci zachovať aj vysvetlenie predchodcu a pri Mesiaci obrátenie argumentu. | Malé titulky, koláže bez čistých zdrojov, čierny/CTA úsek počas pokračovania reči. |
| [fikiclips10 — 5/5](rozbory/fikiclips10.md) | Jedno konkrétne podstatné meno dostane obraz; bližší crop pri pointe. Električka umožňuje porovnanie s našou pasážou. | Identitu fasády ani výšku nájmu nepotvrdzuje ilustračná vložka; mierka a titulky kolíšu. |
| [fiki.kliky — 5/5](rozbory/fiki.kliky.md) | Abstraktný argument možno rozdeliť na štyri jednotné karty s rovnakými ikonami a farbami. | Súbeh nadpisu, prepisu, spodného textu a CTA; piktogramy nemajú predstierať overené dáta. |
| [_fiki.unchained_ — 5/5](rozbory/_fiki.unchained_.md) | Otázková karta, protiklad a vybraná veta z tela pasáže ako predohra. | Malá Fikiho odpoveď po politickej citácii; neurčitý úvod nezachráni samotný efekt. |
| [fiki.bossik — 5/5](rozbory/fiki.bossik.md) | Skutočná akcia/ochutnávka a krátke adresné vložky; rovnakú Q&A možno skrátiť inak. | Jedna titulková karta nemusí niesť celú negáciu: hustá kontrola vyvrátila podozrenie na obrátený význam. |
| [fiki.sulikclips3 — 5/5](rozbory/fiki.sulikclips3.md) | Kratší výber rovnakého argumentu, otázka a grafický vzťah, miesto na prvý referent. | Doložený chybný zlom BRATISLAVČANOC / H; 20/80 je hypotetický model, nie výsledok merania. |
| [fiki.nahrad — 5/5](rozbory/fiki.nahrad.md) | Jasná otázka, dominantná tvár a návrat jednej vizuálnej metafory. | Dĺžka, konce odpovedí a delenie slov; dlhý Vallo sa s naším klipom zhoduje iba v časti PR pasáže. |
| [best.of.fiki — 5/5](rozbory/best.of.fiki.md) | Dve hierarchie textu a ukážka, ktorá umožní porovnať kritiku s predmetom. | Overená približne 0,792 s čierna medzera; otázka cez tvár a neidentifikovaný dokumentárny B-roll. |
| [basedfiky — 5/5](rozbory/basedfiky.md) | Konkrétne vizuálne referenty a zrozumiteľný protiklad v reči; variant toho istého širšieho Vallo zdroja. | Skontrolovať koncovú URL: v Matovičovi je viditeľné fiky.sk. Rozsah prísľubu treba porovnať s tým, čo klip naozaj dopovie. |

## Čo sa naozaj opakuje

1. **Úvod má hneď predmet.** Otázka, konkrétny človek, citovaný moment alebo silná téza. Vizuálny efekt je až druhé rozhodnutie. Otázku možno ukázať a potom odstrániť, aby pri odpovedi nezmenšovala tvár.
2. **Veľkosť obrazu má funkciu.** Reakcia potrebuje mimiku, fyzická ukážka celé potrebné telo, citovaný detail čitateľnú citáciu. Jeden automatický crop nevyrieši všetky tri.
3. **Obraz mení významový stav.** Meno dostane portrét; dva údaje dostanú spoločné porovnanie; čakanie dostane akciu čakania. Doplnený obraz má mať pomenovateľnú úlohu a odchod.
4. **Silné sú aj lacnejšie formáty.** Q&A, dialóg a portrét s presným dôrazom nevyžadujú nové externé médium. Databáza pomáha, ale nesmie sa stať dôvodom odkladať vhodnú jednoduchú pasáž.
5. **Náročnejšie scény držia identitu.** Jeden predmet alebo postava sa vracia pri ďalšej vete. Naše Električka a Vajanského sú konkrétny vlastný dôkaz tohto princípu. Náhodne striedané fotky by jeho funkciu rozbili.
6. **Aj úspešné účty majú obyčajné chyby.** Čierne medzery, prekrývanie tváre, rozbité slovo a CTA pred pointou. Úspech nie je dôvod tieto chyby kopírovať ani dôkaz, že konkrétny trik spôsobil dosah.

## Čo je zajtra reálne použiteľné

[RECEPTY_NA_VYROBU.md](RECEPTY_NA_VYROBU.md) rozpisujú osem postupov na konkrétne spúšťače, kroky, materiály a kontrolu. Štyri majú materiálový základ pre vhodnú vybranú pasáž už teraz: portrétová Q&A, krátka adresná reakcia, miestna orientácia a návrat rovnakého objektu. Pri sliepke/vajci máme fotografie, ale ešte treba výrezy a nové kotvy. Trojbodový argument a dvojica hodnôt nepotrebujú stiahnutý stock; potrebujú vlastnú správnu grafiku. Komplexná hovoriaca postava zatiaľ pripravená nie je.

Existujúca výbava je v [PODKLADY_NA_VYROBU.md](PODKLADY_NA_VYROBU.md): 15 rôznych evidovaných vizuálov, 15 ďalších vizuálnych kandidátov, dva uložené produkčné recepty a 109 OGG bez posluchového prijatia. V tejto noci pribudli **dve čisté originálne fotografie NASA s pôvodom a skontrolovaným obsahom**, [Zem a astronaut pri vlajke](podklady/nasa/README.md); sú výskumné podklady, ešte nie kanonicky registrované produkčné použitie. Referenčných 120 hotových klipov sa k čistým assetom nepripočítava.

Nasledujúci výrobný krok je jedna Adamom vybraná úplná pasáž → jeden konkrétny recept → chýbajúce adresné materiály → skúška → kontrola obrazu, pohybu a posluchu → prijatie. Výskum nevytvoril nový finálny klip ani neoveril kapacitu piatich prijatých klipov denne. Samostatné [porovnanie kvality](POROVNANIE_KVALITY.md) vysvetľuje, v čom sa už naše edity držia a čo ešte treba preveriť.

## Kontrola výsledku

[KONTROLA_VYSKUMU.md](KONTROLA_VYSKUMU.md) obsahuje nezávislé preverenie reprezentatívnych dôkazov a materiálov. [STAV.json](STAV.json) a [overenie-vysledkov.json](overenie-vysledkov.json) uvádzajú finálne počty, otvorené medzery a technickú kontrolu odkazov. Hranice posluchu, súvislého prehratia, čistého pôvodu niektorých cudzích vrstiev a tvorivého prijatia ostávajú otvorené aj po uzavretí tohto nočného výskumného bloku.
