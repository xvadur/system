# Použiteľný existujúci výskum Fikiho kliperov

Dátum auditu: **27. 10. 2026**, podľa dátumu zadania v Codexe. Rozsah: existujúce lokálne rozbory, referenčné videá, register použití a hooky. Toto je vstup do nočného výskumu, **nie výsledok nového rozboru 20 autorov × 5 videí**. Nevznikli nové obsahové analýzy, sťahovanie médií, rendery ani publikácie. Centrálny index ani runtime sa nemenili.

**Záver:** máme veľký zachovaný a obsahovo použiteľný výskum. Najsilnejšou hotovou časťou sú konkrétne časované obrazové a redakčné postupy. Slabšie dokončená je cesta od pozorovaného cudzieho assetu k samostatnému čistému súboru a overenému použitiu na našej novej pasáži. Nočný výskum má existujúcu prácu využiť, dopĺňať medzery a preverovať schopnosť previesť poznatok do editu.

## 1. Čo je skutočne zachované a overené

Základom fyzickej kontroly bol [index zachovaných médií](../../data/videa.json). Pri audite sa pre každý záznam overila existencia lokálneho súboru, veľkosť a celý SHA-256 voči uloženému indexu.

| Kontrola | Výsledok |
|---|---:|
| Fyzické mediálne záznamy v indexe | **108** |
| Unikátne kombinácie platforma + verejné video ID | **106** |
| Kombinácie účet + platforma s uloženým médiom | **31** |
| Súčet veľkostí 108 fyzických záznamov | **590,17 MiB** |
| Existujúce súbory so zhodnou veľkosťou | **108/108** |
| Zhodné celé SHA-256 | **108/108** |
| Chýbajúce súbory / rozdielne veľkosti / rozdielne hashe | **0 / 0 / 0** |

Index obsahuje 58 fyzických TikTok záznamov, 40 instagramových a 10 facebookových. **Prítomnosť videa neznamená dokončený obsahový rozbor.** Dva fyzické záznamy navyše predstavujú opakované zachovanie už evidovaného videa v ďalšej dávke. Zdrojové cesty a kontrolné súčty sú pri každom konkrétnom súbore v [indexe](../../data/videa.json).

## 2. Koľko podrobných rozborov už máme

Prepočet používa presné verejné ID zo zdrojových URL v dokončených textových sadách. Dedupľuje podľa **platforma + video ID**, nie podľa názvu súboru alebo podobnosti používateľského mena.

| Dokončená sada | Rozobraté položky | Podklad |
|---|---:|---|
| 15. 10.: 30 IG referencií + 9 TikTokov | **39** | [Dekompozícia 39](../2026-10-15-skupina/dekompozicia-39-spaces.md) |
| 16. 10.: TikTok, sedem účtov po tri videá | **21** | [Účty 01/05/07](../2026-10-16-vykon/rozbory-ucty-01-05-07.md), [02/08/09/10](../2026-10-16-vykon/rozbory-ucty-02-08-09-10.md), [03/04/06](../2026-10-16-vykon/rozbory-ucty-03-04-06.md) |
| 16. 10.: päť IG + päť FB účtov, dve videá na účet | **20** | [IG/FB dekompozície](../2026-10-16-vykon/dekompozicie-ig-fb-spaces.md), [stav a hranice výskumu](../2026-10-16-vykon/STAV.md) |
| 21. 10.: desať vybraných Xavierových klipov + Vallo | **11** | [Index výberu](../2026-10-21-fikisulik_klipyy/INDEX.md), [samostatný Vallo](../2026-10-21-fikisulik_klipyy/ROZBOR.md) |
| Súčet po odpočítaní dvoch opakovaných TikTok ID | **89** | Prienik sady 21 a novších 11 obsahuje dve ID; ostatné uvedené sady sa podľa platformy/ID neprekrývajú. |

**89 rôznych podrobne vizuálne rozobratých klipov = 39 TikTok + 40 Instagram + 10 Facebook.** V indexe ich možno priradiť k **23 kombináciám účet + platforma** a všetkých 89 má zachované referenčné médium. Počet nie je tvrdenie o 23 rôznych ľuďoch: viac sietí môže patriť jednému autorovi a podobný názov sám nepotvrdzuje totožnosť. Párovanie rozborov s médiami používa [presné ID](../../data/videa.json).

Staršie stručné prieskumy a proxy merania sa nepripočítali ako ďalšie plnohodnotné dekompozície. Deväť pripravených TikTokov z nedokončených trojíc sa neoznačilo za dokončené len preto, že boli stiahnuté; tento limit výslovne uvádza [stav zo 16. 10.](../2026-10-16-vykon/STAV.md).

## 3. Osem konkrétnych prenosných postupov

Nižšie „použiteľné“ znamená, že poznáme konkrétnu redakčnú a obrazovú operáciu a máme referenciu. **Neznamená to hotový produkčný komponent, presné slovné kotvy pre nový klip ani Adamovo prijatie novej realizácie.** Uvedené časy sú približné časy referenčného editu, nie pôvodnej epizódy.

### A. Podnet v telefóne → celá plocha pre reakciu

- **Referencia:** TikTok `fiki.extra`, `7695478964013239574`, 36,12 s. [Verejné video](https://www.tiktok.com/@fiki.extra/video/7695478964013239574), [zachované lokálne video](/Users/xvadur_mac/xvadur_workspace/projekty/klipy/fiki/praca/105/uspesne-ucty-2026-10-16/media/fiki.extra_7695478964013239574.mp4), [podrobný rozbor](../2026-10-16-vykon/rozbory-ucty-02-08-09-10.md).
- **Konkrétne rozhodnutie:** približne **25–26 s** telefón odíde nadol a Fikiho reakcia dostane celý portrét; titulky sa presunú na hrudník. Približne od **30 s** príde krátka horná notifikácia s webom. Koniec zostáva na živom portréte.
- **Prenositeľný recept:** súčasne ukázať potrebný podnet a mimiku → pri prevzatí komentára odstrániť podnet → uvoľniť priestor reakcii → CTA držať ako vlastnú krátku vrstvu.
- **Pripravené:** referencia, časový priebeh a explicitný replikačný recept.
- **Doplniť pre nový klip:** náš zdrojový podnet, Fikiho pasáž a vlastný rám/maska. Nový externý b-roll nie je technickou podmienkou tohto postupu.

### B. Veľká úvodná téza → menšie titulky → samostatný významový akcent

- **Referencia:** TikTok `fikimentalita`, Mor ho, `7691022886672370966`, 47,042 s. [Verejné video](https://www.tiktok.com/@fikimentalita/video/7691022886672370966), [lokálne video](/Users/xvadur_mac/xvadur_workspace/projekty/klipy/fiki/praca/prieskum-2026-10-07/davka-2/fikimentalita_7691022886672370966.mp4), [rozbor č. 31](../2026-10-15-skupina/dekompozicia-39-spaces.md).
- **Konkrétne rozhodnutie:** horná dvojriadková téza drží približne **0–4,75 s**, potom ustúpi menším priebežným titulkám. Meno dostane samostatný akcent približne **18,5–19,5 s**. Rečník, telefón a potrebné gestá zostávajú čitateľné.
- **Prenositeľný recept:** povedať predmet od prvej snímky → stiahnuť úvod po orientácii → nechať argument niesť tvárou a titulkami → veľký text znovu použiť len pri skutočnej zmene významu.
- **Pripravené:** hierarchia, časová mapa, návratové pravidlo a konkrétne upozornenie na nadbytočné zdvojovanie textu v súvisiacom klipe č. 32.
- **Doplniť:** presný nový nadpis, opravené titulky a kotvy podľa vlastnej reči. Tento postup možno skúsiť s vlastným A-rollom bez hľadania novej sady GIFov.

### C. Porovnanie dvoch hodnôt v stabilných stranách

- **Referencia:** TikTok `fiki.kliky`, vysoké školy/dane, `7693614011916537110`, 48,9 s. [Verejné video](https://www.tiktok.com/@fiki.kliky/video/7693614011916537110), [lokálne video](/Users/xvadur_mac/xvadur_workspace/projekty/klipy/fiki/praca/105/uspesne-ucty-2026-10-16/media/fiki.kliky_7693614011916537110.mp4), [rozbor](../2026-10-16-vykon/rozbory-ucty-01-05-07.md).
- **Konkrétne rozhodnutie:** približne **14–18,5 s** sú položky a príslušné čísla na opačných stranách; okolité grafické vstupy majú vlastné úlohy a medzi nimi sa vracia Fiki.
- **Prenositeľný recept:** prvá položka → druhá položka → spoločné kritérium → čitateľný vzťah, bez vynucovania obrázka pri každom slove.
- **Pripravené:** pomenovanie vrstiev, poradie, kontext a časovanie referencie.
- **Doplniť:** vlastné správne hodnoty/jednotky a čisté obrázky, ak ich nové porovnanie vyžaduje. Základný vzťah možno realizovať vlastnou textovou/číselnou grafikou. Obrázky z referencie zatiaľ nie sú samostatne získaný balík.

### D. Jeden fotografický celok ako mapa komentára

- **Referencia:** TikTok `fikisulik_klipyy`, SOWA, `7693962715596868886`, 29,4 s. [Verejné video](https://www.tiktok.com/@fikisulik_klipyy/video/7693962715596868886), [zachované video](../2026-10-21-fikisulik_klipyy/videa/7693962715596868886/source.mp4), [podrobný register výrezov](../2026-10-21-fikisulik_klipyy/videa/7693962715596868886/ROZBOR.md).
- **Konkrétne rozhodnutie:** približne **0,2–23,77 s** celok → jednotliví ľudia → dvojice/skupina → návrat na celok a opakovaný detail. Krátka meme zámena je samostatná vložka približne **10,47–11,3 s**.
- **Prenositeľný recept:** udržať jeden spoločný obraz ako priestorovú pamäť a meniť relevantný výrez podľa referentu v reči; po reakcii vrátiť pôvodný predmet.
- **Pripravené:** 15 konkrétnych záznamov použití s funkciami a približnými hranicami.
- **Doplniť:** čistý správny fotografický celok alebo jeho zdroj z epizódy. Treba zistiť, čo už obsahovala pôvodná epizóda; nie všetky výrezy a pohyby možno automaticky pripísať kliperovi.

### E. Doslovný predmet → popkultúrna asociácia pri pomenovaní

- **Referencia:** TikTok `fikisulik_klipyy`, polícia/advokát, `7695391580169030934`. [Verejné video](https://www.tiktok.com/@fikisulik_klipyy/video/7695391580169030934), [lokálne video](../2026-10-21-fikisulik_klipyy/videa/7695391580169030934/source.mp4), [rozbor](../2026-10-21-fikisulik_klipyy/videa/7695391580169030934/ROZBOR.md).
- **Konkrétne rozhodnutie:** polícia približne **1,6–2,7 s**, postava právnika vizuálne identifikovaná ako Saul Goodman približne **9–10,5 s** pri zmienke o advokátovi.
- **Prenositeľný recept:** konkrétne podstatné meno najprv identifikovať obrazom; vhodnú profesijnú/popkultúrnu skratku použiť iba pri skutočnom významovom spúšťači.
- **Pripravené:** úloha, spúšťač, približný čas a smer hľadania.
- **Doplniť:** samostatný čistý obrázok alebo zvolený vlastný ekvivalent. Presný použitý originál a editorov zdroj policajnej fotografie/portrétu neboli získané. Identifikácia postavy nie je vyriešený produkčný asset.

### F. Vracajúci sa vtip s novou vrstvou

- **Referencia:** TikTok `fikisulik_klipyy`, Detroit, `7693174026734177559`, 29,7 s. [Verejné video](https://www.tiktok.com/@fikisulik_klipyy/video/7693174026734177559), [lokálne video](../2026-10-21-fikisulik_klipyy/videa/7693174026734177559/source.mp4), [rozbor](../2026-10-21-fikisulik_klipyy/videa/7693174026734177559/ROZBOR.md).
- **Konkrétne rozhodnutie:** mesto/vlajka/busta/vyrezaný Fiki približne **4,3–5,9 s**; návrat vlajky a busty s novým pasom **8,5–9,5 s**; orol **18,6–19,4 s**; konkrétna mapa **20,3–21,8 s**. Vložené mená medzi návratmi dostávajú samostatný obraz.
- **Prenositeľný recept:** zaviesť vizuálny motív → pri ďalšej vete ho rozpoznať a vrátiť → pridať novú informáciu → vyvrcholiť, bez náhodnej výmeny celého sveta.
- **Pripravené:** presný sled prvkov, návraty a kontext. [Sokratova smrť](../2026-10-21-fikisulik_klipyy/podklady/david-death-of-socrates-met-open-access.jpg), použitá v medziľahlej mennej sérii, je samostatne získaná čistá múzejná reprodukcia.
- **Doplniť:** ostatné konkrétne čisté vrstvy a masku vlastného hovoriaceho. Ostatné hľadacie frázy v registri sú otvorené stopy. Pre nový vtip treba navrhnúť vlastný súdržný balík; mechanika nevyžaduje opakovať americké identity alebo rovnakú tému.

### G. Infografika skladaná v poradí argumentu

- **Referencia:** Facebook Fiki CLIPS, Apollo, `1534672798682477`, 46,37 s. [Verejné video](https://www.facebook.com/reel/1534672798682477/), [lokálne video](/Users/xvadur_mac/xvadur_workspace/projekty/klipy/fiki/praca/105/uspesne-ucty-2026-10-16/media-ig-fb/fb_filipfikisulik_1534672798682477.mp4), [rozbor](../2026-10-16-vykon/dekompozicie-ig-fb-spaces.md).
- **Konkrétne rozhodnutie:** približne **12–23 s** sa skladá nadpis → jednotlivé štítky → spoločná časová spojka → zmena schémy a výsledok. Návrat do štúdia príde po tejto vysvetľujúcej úlohe.
- **Prenositeľný recept:** ukázať položky v poradí reči, spoločný vzťah až po ich zavedení a výsledok odhaliť pri príslušnej vete. Jeden stabilný grafický priestor môže niesť viac krokov.
- **Pripravené:** celý postup a viditeľné stavy kompozície; využiteľné ako predloha novej vlastnej vysvetľujúcej scény.
- **Doplniť:** vlastné správne údaje, slovné kotvy a konkrétnu implementáciu. Obraz ilustruje argument; samotný rozbor neoveruje interpretáciu vesmírneho programu ani nepreukazuje hotový produkčný komponent.

### H. Obrazový vtip na fyzické gesto

- **Referencia:** Instagram `fikiprezident`, herná paródia `DeJsf0hsgMX`, 15,86 s. [Verejné video](https://www.instagram.com/fikiprezident/reel/DeJsf0hsgMX/), [lokálne video](/Users/xvadur_mac/xvadur_workspace/projekty/klipy/fiki/praca/105/uspesne-ucty-2026-10-16/media-ig-fb/ig_fikiprezident_DeJsf0hsgMX.mp4), [rozbor](../2026-10-16-vykon/dekompozicie-ig-fb-spaces.md).
- **Konkrétne rozhodnutie:** objekty prichádzajú ku gestám boxera a odlietajú približne **2,5–6,5 s**; posledné kolo **7,5–8 s**; farebný zásah, rotácia a výsledok približne **12,8–14,2 s**.
- **Prenositeľný recept:** ustanoviť jedno pravidlo obrazovej hry → opakovať ho pri skutočných gestách → odlíšiť poslednú fázu → nechať posledný zásah vyústiť do výsledku.
- **Pripravené:** opis vstupov, kontaktu, odletov, finálnej rotácie a textového vyvrcholenia.
- **Doplniť:** vhodný gestický zdroj a vlastné čisté objekty/postavy. Presné politické či osobné identity zo vzoru nie sú technickou podmienkou tohto postupu. Treba overiť priebeh pohybu, nie iba koncové snímky.

## 4. Ďalšie konkrétne použiteľné vrstvy

### Hooky

Historická [knižnica hookov z 26. 9.](../2026-09-26-trendy/hooky.md) obsahuje **13 pomenovaných Fiki foriem F1–F13** a v oddiele všeobecných hookov **31 vzorov 1–31**. Ide o repertoár úvodných mechaník s rôznou dôkazovou váhou, nie potvrdenú súčasnú výkonnostnú normu. Súbor rozlišuje overené príklady, odhady a šablóny bez výsledkov.

Pre výrobu sú použiteľné napríklad absurdný podnet → reakcia, porovnanie s cenou/číslom, priama otázka, konkrétna životná situácia či vlastný názor s jasným predmetom. Staré tvrdenia o univerzálnej dĺžke, hashtagových pravidlách, kódoch a CTA sa nemajú automaticky preberať ako aktuálne zadanie; pôvodný súbor je dátovaný výskumný materiál.

### Štruktúrovaný register použití

[Register z 21. 10.](../2026-10-21-fikisulik_klipyy/assety-register.json) má **115 záznamov v 11 videách**: 18 prechodov, 37 zdrojových citácií, 11 textových vrstiev, 9 emoji, 11 CTA, 3 meme, 16 foto/video použití a 10 cutoutov. Obsahuje čas, spúšťač, funkciu, vzhľad, referenčné video a návrh ďalšieho kroku. Je to použiteľná mapa rozhodovania **čo → kedy → pri čom → prečo**, nie hotová knižnica 115 externých médií.

**Všetkých 115 záznamov stále uvádza `sourceStatus: exact_unknown` a `sourceUrl: null`.** To znamená neznámy presný originálny editorov súbor. Neskôr získaný oficiálny ekvivalent či identifikované dielo majú vlastný záznam pôvodu a nemenia spätne toto tvrdenie o pôvodnom súbore. Stav získavania rozpisuje [zdrojový register](../2026-10-21-fikisulik_klipyy/ZDROJE_NA_ZISKANIE.md).

### Samostatné čisté obrazové podklady z tohto výskumu

| Podklad | Overené v zachovanej evidencii | Čo ešte neznamená |
|---|---|---|
| [Oficiálny erb Bratislavy](../2026-10-21-fikisulik_klipyy/podklady/bratislava-erb-oficialny-ekvivalent.png) | Oficiálny ekvivalent, 2000 × 2000 px; [metadáta pôvodu](../2026-10-21-fikisulik_klipyy/podklady/bratislava-erb-oficialny-ekvivalent.metadata.json). | Má biele pozadie; nie je hotový transparentný výrez ani dokázaný pôvodný súbor klipera. |
| [Sokratova smrť](../2026-10-21-fikisulik_klipyy/podklady/david-death-of-socrates-met-open-access.jpg) | Identifikované dielo a nová čistá reprodukcia Met Open Access, 4000 × 2663 px; [metadáta](../2026-10-21-fikisulik_klipyy/podklady/david-death-of-socrates-met-open-access.metadata.json). | Nie je overené editorovo miesto stiahnutia, jeho konkrétny súbor ani hotový vlastný crop. |

Tieto **dva podklady patria iba k tejto výskumnej sade**. Nejde o súčet celej produkčnej knižnice projektu. Vlastné GIFy, reakcie, b-rolly, zvuky a ilustrácie z výroby majú samostatnú evidenciu a samostatný audit.

## 5. Hranice dôkazu a použitie v nočnom výskume

1. **Obraz:** dokončené historické rozbory sú prevažne časované snímky cez celé video, s hustejším vzorkovaním zmien. Dokazujú viditeľné stavy a približné intervaly. Veľmi krátky zásah medzi snímkami sa môže stratiť; nepreukazujú úplné plynulé hodnotenie pohybu a rytmu. Rozsah uvádzajú [metóda Xavierovho rozboru](../2026-10-21-fikisulik_klipyy/videa/7693174026734177559/ROZBOR.md) a [stav IG/FB](../2026-10-16-vykon/STAV.md).
2. **Zvuk:** audio nebolo vypočuté. Viditeľný titulok, pomocný ASR, názov zvuku alebo technické meranie nie sú overený posluch hudby, SFX, intonácie a mixu. Nový výskum musí skutočný rozsah posluchu pomenovať; neoverenému efektu nedávať vymyslený názov.
3. **Autorstvo vrstiev:** bez porovnania s celou zdrojovou epizódou nie je isté, že všetko viditeľné pridal kliper. Zdrojové citácie, rámiky, titulky, kurzor či koláž môžu byť zdedené.
4. **Výkon:** počty views sú dátované verejné počítadlá. Z úspešného videa nemožno samotným opisom odvodiť príčinu v GIFe, efektoch ani pravidelnom uploade. Skúmať aj typické a slabšie video autora, pokiaľ možno podobného veku.
5. **Nová výroba:** približný čas referencie nahradiť presnou kotvou v našej vybranej pasáži. Výber pasáže a finálne tvorivé prijatie zostávajú Adamovi.

**Praktická priorita:** postupy A, B a C možno najrýchlejšie skúsiť na vhodných vlastných pasážach, pretože nevyžadujú rozsiahlu sadu nových externých materiálov. D, F, G a H poskytujú silné predlohy významovej obrazovej práce, ale potrebujú konkrétne čisté vrstvy a overenie pohybu. E ukazuje významový spúšťač pre meme; samostatný asset ešte treba vyriešiť.

Nočný výskum má pri novom výbere najprv pripojiť existujúce presné ID a zistenia. Pri opakovanom videu doplniť konkrétnu chýbajúcu vrstvu, napríklad zdrojový kontext, čistý asset, detail pohybu či posluch. **Nových 100 videí ani 100 hotových rozborov tento audit netvrdí.**
