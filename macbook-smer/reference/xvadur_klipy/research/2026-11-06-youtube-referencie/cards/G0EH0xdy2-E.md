# Brendan Jowett — How I Fully Automated My Video Editing (Claude Code)

[YouTube](https://www.youtube.com/watch?v=G0EH0xdy2-E) · 711.993469s · 180,020 views · stav 2026-11-06T00:27:45.948612+00:00

Užitočný dôkaz opakovaného použitia komponentov a mapovania grafiky na prepis. Titulok fully automated je širší než ukázaný postup: autor stále kontroluje textový strih, skracuje pauzy, vyberá hudbu a prezerá grafiku.

## Stav posúdenia

Prečítaný celý prepis a otvorené obrazové vzorky; neposúdený posluch mixu ani súvislá plynulosť.

Celý obrazový priebeh bol vzorkovaný, kritické ukážky zahustené. Nejde o súvislé prehratie. Views nie sú normalizované voči kanálu.

## Významové úseky

### 0–74s — Sľub postupu a vlastný vizuálny príklad

**Pozorované:** Tvár striedajú biele celoplošné typografické karty s modrým akcentom; na30s zoznam deklarovaných odstránených úkonov, na45s prísľub zapamätaného štýlu.

**Reč / význam:** Čas a náklady editovania; štýl uložený z predošlých videí.

**Prenos:** Uložený štýl musí znamenať konkrétne komponenty a pravidlá; samotný text, že agent štýl pozná, nič neoveruje.

[Zdroj v čase](https://www.youtube.com/watch?v=G0EH0xdy2-E&t=0s) · [obraz 1](../../../research/2026-11-06-youtube-referencie/evidence/G0EH0xdy2-E/overview/sheet-01.jpg) · [obraz 2](../../../research/2026-11-06-youtube-referencie/evidence/G0EH0xdy2-E/overview/sheet-02.jpg) · [obraz 3](../../../research/2026-11-06-youtube-referencie/evidence/G0EH0xdy2-E/overview/sheet-03.jpg) · [obraz 4](../../../research/2026-11-06-youtube-referencie/evidence/G0EH0xdy2-E/overview/sheet-04.jpg)

### 74–162s — Vymedzenie zdrojového strihu

**Pozorované:** Rozhranie Descript, výber uloženého template, nový projekt a nahratie média.

**Reč / význam:** Autor vysvetľuje, že automatické odstránenie opakovaní potrebuje kontrolu.

**Prenos:** Oddeliť kontrolu významu prepisu od pridávania grafiky. Nie je potrebné zaviesť ďalší editor len kvôli tomuto videu.

[Zdroj v čase](https://www.youtube.com/watch?v=G0EH0xdy2-E&t=74s) · [obraz 1](../../../research/2026-11-06-youtube-referencie/evidence/G0EH0xdy2-E/overview/sheet-01.jpg) · [obraz 2](../../../research/2026-11-06-youtube-referencie/evidence/G0EH0xdy2-E/overview/sheet-02.jpg) · [obraz 3](../../../research/2026-11-06-youtube-referencie/evidence/G0EH0xdy2-E/overview/sheet-03.jpg) · [obraz 4](../../../research/2026-11-06-youtube-referencie/evidence/G0EH0xdy2-E/overview/sheet-04.jpg)

### 244–291s — Ľudská revízia rezu

**Pozorované:** Prepis s prečiarknutými opakovaniami vedľa náhľadu; klikanie mení zobrazený bod videa a timeline.

**Reč / význam:** Prečítať celý prepis, odstrániť neželané časti alebo vrátiť potrebné úseky.

**Prenos:** Kontrolovať opakovania aj významové podmienky; pravidlo posledný take je správny nie je univerzálne.

[Zdroj v čase](https://www.youtube.com/watch?v=G0EH0xdy2-E&t=244s) · [obraz 1](../../../research/2026-11-06-youtube-referencie/evidence/G0EH0xdy2-E/cuts/sheet-01.jpg) · [obraz 2](../../../research/2026-11-06-youtube-referencie/evidence/G0EH0xdy2-E/cuts/sheet-02.jpg)

### 291–329s — Samostatná úprava rytmu reči

**Pozorované:** Menu AI tools → Shorten word gaps; okolo300–304s vidno nastavenie0.2s a následne hustejšie úseky waveform.

**Reč / význam:** Skrátiť medzery a opäť skontrolovať zostrih.

**Prenos:** Meranie medzier je pomocný krok;0.2s z tohto autora sa nestáva našou povinnou hranicou.

[Zdroj v čase](https://www.youtube.com/watch?v=G0EH0xdy2-E&t=291s) · [obraz 1](../../../research/2026-11-06-youtube-referencie/evidence/G0EH0xdy2-E/cuts/sheet-01.jpg) · [obraz 2](../../../research/2026-11-06-youtube-referencie/evidence/G0EH0xdy2-E/cuts/sheet-02.jpg)

### 329–409s — Hudba a kontinuita projektu

**Pozorované:** Descript projekt a na360s hudobná knižnica; následne prechod do pretrvávajúceho Claude chatu s predchádzajúcimi pokynmi na grafiku a hlasitosť.

**Reč / význam:** Autor si vyberá hudbu a používa rovnaký pracovný priečinok pre ďalšie videá.

**Prenos:** Uchovávať skutočné opravy, nastavenia a zdrojové súbory pri klipe. Výber hudby podľa reči treba vypočuť.

[Zdroj v čase](https://www.youtube.com/watch?v=G0EH0xdy2-E&t=329s) · [obraz 1](../../../research/2026-11-06-youtube-referencie/evidence/G0EH0xdy2-E/overview/sheet-01.jpg) · [obraz 2](../../../research/2026-11-06-youtube-referencie/evidence/G0EH0xdy2-E/overview/sheet-02.jpg) · [obraz 3](../../../research/2026-11-06-youtube-referencie/evidence/G0EH0xdy2-E/overview/sheet-03.jpg) · [obraz 4](../../../research/2026-11-06-youtube-referencie/evidence/G0EH0xdy2-E/overview/sheet-04.jpg)

### 465–551s — Prepis mapovaný na edit

**Pozorované:** V chate je rozpis stacku a krokov: prepis, mapovanie grafiky, kompozícia, Studio a render.

**Reč / význam:** FFmpeg a Whisper poskytujú prepis s časmi pre React/Remotion grafiky.

**Prenos:** Náš existujúci Transcript→EditPlan→Timeline už zodpovedá princípu. Potrebné je naplniť plán konkrétnymi významovými akciami.

[Zdroj v čase](https://www.youtube.com/watch?v=G0EH0xdy2-E&t=465s) · [obraz 1](../../../research/2026-11-06-youtube-referencie/evidence/G0EH0xdy2-E/overview/sheet-01.jpg) · [obraz 2](../../../research/2026-11-06-youtube-referencie/evidence/G0EH0xdy2-E/overview/sheet-02.jpg) · [obraz 3](../../../research/2026-11-06-youtube-referencie/evidence/G0EH0xdy2-E/overview/sheet-03.jpg) · [obraz 4](../../../research/2026-11-06-youtube-referencie/evidence/G0EH0xdy2-E/overview/sheet-04.jpg)

### 551–613s — Kontrolovateľný prechod od plánu k scéne

**Pozorované:** Príkaz na nový longform, časová mapa obsahu, reakcia autora, potom tabuľka sekcií/typov grafiky a otvorené Remotion Studio s jednotlivými vrstvami.

**Reč / význam:** Najprv plán, potom zostavenie, potom náhľad celej časovej osi.

**Prenos:** U každého významového úseku musí byť viditeľné, ktorá konkrétna scéna ho spracúva; mapa sekcií sama nestačí.

[Zdroj v čase](https://www.youtube.com/watch?v=G0EH0xdy2-E&t=551s) · [obraz 1](../../../research/2026-11-06-youtube-referencie/evidence/G0EH0xdy2-E/preview/sheet-01.jpg) · [obraz 2](../../../research/2026-11-06-youtube-referencie/evidence/G0EH0xdy2-E/preview/sheet-02.jpg) · [obraz 3](../../../research/2026-11-06-youtube-referencie/evidence/G0EH0xdy2-E/preview/sheet-03.jpg)

### 613–665s — Opakované komponenty a konkrétna revízia

**Pozorované:** V náhľade sa objaví zvýraznená veta, trojica kategórií, dvojstĺpcové porovnanie a dva zoznamy; medzi nimi návraty na rečníka. Pri644s sa text v poslednom riadku zalamuje viac než zvyšok.

**Reč / význam:** Autor demonštruje hotové grafiky a pri642–645s pripúšťa zmenšenie textu.

**Prenos:** Opakovane použiteľná je funkcia porovnania alebo postupného zoznamu. Biele kartičky z tohto návodu nenahrádzajú Fikiho B-roll a meme.

[Zdroj v čase](https://www.youtube.com/watch?v=G0EH0xdy2-E&t=613s) · [obraz 1](../../../research/2026-11-06-youtube-referencie/evidence/G0EH0xdy2-E/preview/sheet-01.jpg) · [obraz 2](../../../research/2026-11-06-youtube-referencie/evidence/G0EH0xdy2-E/preview/sheet-02.jpg) · [obraz 3](../../../research/2026-11-06-youtube-referencie/evidence/G0EH0xdy2-E/preview/sheet-03.jpg)

### 665–711.993s — Hranica demonštrácie

**Pozorované:** Záverečný výklad ostáva v rozhraní s náhľadmi už existujúcich scén; záver odkazuje na ďalšie video.

**Reč / význam:** Autor pripúšťa ďalšie kontroly a úpravy pred renderom.

**Prenos:** Nezamieňať ukážku Studio s naším hotovým, vypočutým a tvorivo prijatým výstupom.

[Zdroj v čase](https://www.youtube.com/watch?v=G0EH0xdy2-E&t=665s) · [obraz 1](../../../research/2026-11-06-youtube-referencie/evidence/G0EH0xdy2-E/overview/sheet-01.jpg) · [obraz 2](../../../research/2026-11-06-youtube-referencie/evidence/G0EH0xdy2-E/overview/sheet-02.jpg) · [obraz 3](../../../research/2026-11-06-youtube-referencie/evidence/G0EH0xdy2-E/overview/sheet-03.jpg) · [obraz 4](../../../research/2026-11-06-youtube-referencie/evidence/G0EH0xdy2-E/overview/sheet-04.jpg)

## Tvrdenia a dôkazy

- **Plná automatizácia editovania.** Čiastočne zavádzajúce zovšeobecnenie:74–120s zdôvodňuje Descript kvôli chybám,244–329s kontrolu strihu a medzier,329–372s výber hudby,642–645s opravu grafiky.
- **Relevantné grafiky sa generujú z časovaného prepisu.** V9:12–9:28 je viditeľná mapa obsahu a tabuľka grafík;10:16–11:04 ukážky výsledkov. Úplná implementácia ani ich presnosť na pôvodnom médiu neboli spustené/overené.
- **Štýl sa dá opakovane používať.** Predchádzajúce pokyny a opakovanie rovnakých typov grafiky sú viditeľné. Miera práce medzi videami a deklarovaná časová úspora nie sú zmerané.
- **Autor ponúka bezplatný prehľad postupu vo svojej komunite.** V540,84–551,92s odkazuje na breakdown sheet. Nesľubuje tým verejný repozitár. Vo verejnom YouTube opise sme nenašli priamy overený repozitár alebo samostatný ZIP; obsah komunitného materiálu nebol otvorený.

## Použiť / nepreberať

- Použiť: Kontinuita štýlu a opráv v jednom projekte.
- Použiť: Oddelenie zdrojových strihov od grafiky.
- Použiť: Mapa prepisu na scény a revízia výsledku v Studio.
- Nepreberať: Univerzálne0.2s pauzy alebo posledný take ako vždy správny.
- Nepreberať: Zamieňať generické informačné karty za celý Fiki vizuálny repertoár.
- Nepreberať: Sľubovať plnú autonómiu či1200 prijatých klipov z tejto ukážky.

[Časovaný prepis](../../../research/2026-11-06-youtube-referencie/evidence/G0EH0xdy2-E/transcript-timed.json) · [Manifest obrazov](../../../research/2026-11-06-youtube-referencie/evidence/G0EH0xdy2-E/manifest.json) · [Lokálne video](../../../research/2026-11-06-youtube-referencie/media/G0EH0xdy2-E/source.mp4)
