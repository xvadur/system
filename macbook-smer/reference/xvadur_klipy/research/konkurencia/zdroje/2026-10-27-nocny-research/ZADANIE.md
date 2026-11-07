# Nočný výskum: od rozborov ku schopnosti vyrobiť klip

Zadané Adamom v tomto chate 27. októbra 2026. Cieľom je zlepšiť remeslo a pripraviť skutočné podklady na nasledujúcu výrobu. Odhad vyradenia zo skupiny je vedľajší.

## Potvrdené zadanie

- Najprv využiť existujúci výskum a reálne médiá; neopakovať dokončené rozbory bez dôvodu.
- Rozšíriť výber z troch na päť videí od každého z dvadsiatich autorov.
- Skontrolovať aj troch ľudí v historickej kategórii ZLE: či ich konkrétne edity tieto slabiny ešte vykazujú.
- Rovnakými kritériami posúdiť naše staršie videá a posledné Vajanského/Električku; odlíšiť zlepšenie našich posledných editov od bežného staršieho výkonu.
- Pri užitočnom postupe určiť, či máme potrebné podklady a vieme z neho vyrobiť vlastný klip, alebo čo presne chýba.
- Celý postup prebieha v Codexe. Výber novej pasáže a finálne tvorivé prijatie zostávajú Adamovi.

## Záväzné vstupy

- `AUDIT_EXISTUJUCEHO.md`: overené existujúce rozbory a konkrétne postupy.
- `PODKLADY_NA_VYROBU.md`: fyzické materiály, recepty a skutočné hranice kontroly.
- `vyber-100.json` a `VYBER.md`: pevná vzorka 20 autorov × 5 rôznych TikTokov, s existujúcimi súbormi a rozbormi.
- `kontrolna-vzorka.json`: historická ZLE skupina a naše porovnávacie videá. Neprístupnosť nie je nula ani dôkaz slabej kvality.
- `../2026-10-27-riziko/analysis.json`, `tiktok-snapshot.json`, `rating-live.json`: zmrazené metriky a historické kategórie.
- `../../data/videa.json` a príslušné pôvodné rozbory: referenčné médiá a pôvod.
- `EVIDENCIA_CASOVANIA.md` a `evidence-r2.json`: opravené časové podklady so zdrojovými PTS a pravidlo odlíšenia analytického paddingu od natívneho obrazu. Pôvodná revízia zostáva zachovaná, ale nemá slúžiť na presné hranice.

Výber dvadsiatich podľa mediánu a aspoň desiatich uploadov je pravidlo výberu na výskum, nie oficiálne poradie kvality. Nezamieňať profily s podobným názvom ani účty na rôznych sieťach. Historický rating a adresár nepreukazujú aktuálne členstvo.

## Výrobná otázka pri každej referencii

1. Aký je zdrojový moment, hook, kontext a pointa? Čo už bolo vo Fikiho zdroji a čo pridal kliper?
2. Čo presne sa mení v obraze pri ktorých slovách? Zaznamenať nástup, podržanie, akciu a návrat.
3. Akú funkciu majú fotografie, meme/GIF, B-roll, vlastná grafika, titulky, crop, zoom a prechod? Zaznamenať aj účelné ponechanie A-rollu.
4. Aké zvukové rozhodnutie bolo naozaj počuté? Bez posluchu uviesť neoverené; ASR, waveform a názov súboru neposkytujú takýto dôkaz.
5. Vieme postup vykonať zo skutočných existujúcich súborov? Ktoré materiály majú obsah, vhodný trim, pôvod a potrebnú mierku? Referenčné hotové video nie je čistý asset.
6. Ak niečo chýba, ide o konkrétne dohľadanie, vlastnú grafiku, imagegen, alebo autorskú scénu? Zapísať presný ďalší krok a získané súbory oddeliť od návrhov.

## Rovnaká kontrola remesla pre silných, ZLE aj nás

Najprv čítať reálne video a konkrétne dôkazy, nepreberať starú známku ani počet views ako tvorivý verdikt. Pri prvom obsahovom priechode neposkytovať hodnotiteľovi metriky ani historický rating, ak sa dajú od podkladov oddeliť; neprisudzovať tomu úplné zaslepenie, keď je účet viditeľný vo videu.

Samostatne hodnotiť:

- samostatnosť výberu, kontext a zrozumiteľnosť prvej vety;
- úvodný prísľub, vývoj a dopovedanú pointu;
- významový súlad vložiek a načasovanie humoru;
- čitateľnosť, crop, titulky, kolízie a konzistenciu obrazu;
- skutočne pozorovaný pohyb a rytmus;
- skutočne počutý hlas, hudbu a efekty;
- vlastný nápad a náročnosť potrebnú na jeho opakovanie.

Používať slovné závery silné / zmiešané / slabé / neoverené, vždy s videom a časom. Neoverený zvuk alebo pohyb sa nesmie zmeniť na nulové skóre. Jedna ukážka nie je verdikt o celom autorovi. Po obsahovej kontrole pripojiť views, vek, pravidelnosť a historickú kategóriu ako samostatný kontext.

## Nočný postup a trvalý stav

1. Prečítať `STAV.json`, skontrolovať existujúce rozpracované výstupy a živý zber. Nespustiť duplicitné sťahovanie ani opakované generovanie.
2. Najprv uzavrieť dostupnosť vzorky, potom pracovať po menších skupinách autorov. Starý dokončený rozbor môže byť prevzatý s pôvodom; nové pozorovanie a jeho rozsah sa zapisujú samostatne.
3. Nové referenčné médiá ukladať iba do `media/` v tomto priečinku, pomocné snímky do `evidence/`, rozbory do `rozbory/`. Použiť verejný zdroj a existujúce oprávnené prístupy; nezískavať cookies či poverenia.
4. Pri nedostupnom TikToku skúsiť správne presne priradený profil na ďalšej sieti. Takúto náhradu výslovne označiť; nedosadiť iného človeka. Ak nemáme médium, zaznamenať otvorený bod a pokračovať nezávislou prácou.
5. Skutočne prezrieť snímky/úseky, ktoré sú dôkazom. Stiahnutie, prepis alebo vyrobený kontakt nie sú dokončenou obsahovou analýzou. Pri potrebe pohybového detailu pripraviť hustejšie okolie udalosti a uviesť rozsah overenia.
   Pre význam reči používaj aj dostupné `prepisy.json` a `prepisy/`: surové lokálne ASR s časovanými slovami, vždy označené ako neoverené. Proces a jeho stav sú v `prepis.pid.json`; pri živom procese nevytvárať druhý ASR beh. V prípade potreby sa obnovuje príkazom `system/.venv/bin/python research/konkurencia/zdroje/2026-10-27-nocny-research/prepis_media.py` z koreňa projektu. ASR dopĺňa kontext, nenahrádza posluch, overenie mien ani určenie hudby/SFX. Neponechávaj obsahový význam zbytočne neoverený iba preto, že na snímke nie sú titulky, ak už existuje použiteľný prepis.
6. Doplniť kontrolnú ZLE vzorku a našich päť videí; všetkých posudzovať tou istou osnovou.
7. Spísať vykonateľné postupy a materiálovú pripravenosť. Uprednostniť niekoľko kompletne podložených postupov pred stovkami neurčitých nápadov.
8. Po každom bloku aktualizovať trvalý stav, počet dokončených/neoverených položiek a presný ďalší krok. Samostatná recenzia skontroluje reprezentatívne dôkazy, duplicity a tvrdenia o kvalite.

Toto zadanie povoľuje prieskum a prípravu podkladov. Nemení runtime, staré publikácie, účty, poverenia ani automatizácie publikovania. Nová výroba Fikiho klipu sa nezačína bez platnej Selection. Platené externé video/audio generovanie nie je súčasťou zadania.

## Ranné výstupy

- `VYSLEDKY.md`: čo konkrétne robia úspešní kliperi a čo vieme prevziať.
- `POROVNANIE_KVALITY.md`: silní / historicky ZLE / naše staršie a posledné klipy; konkrétne dôkazy a hranice záveru.
- `RECEPTY_NA_VYROBU.md`: pre každý užitočný postup spúšťač v reči, referencia/čas, uskutočnenie, skutočné materiály a stav pripravené / chýba konkrétny vstup / neoverené.
- `STAV.json`: presné pokrytie zo 100 referencií a kontrolných vzoriek, použité staré rozbory, nové analýzy a zostávajúce medzery.

Skúmanie nemá dokazovať, že pravidelnosť alebo konkrétny GIF spôsobili views. Má dať Adamovi pravdivú odpoveď, z akých pripravených podkladov vieme na nasledujúci deň vyrábať a ktorú tvorivú schopnosť ešte treba nacvičiť.
