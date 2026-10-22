# Interview s Adamom — 20. 10. 2026

Podkladom je Adamom dodaný Design System Interviewer od Yanisa Schweizera. Existujúca knižnica a ukážky zostávajú zachované; nové rozhodnutia sa prijímajú v rozhovore a až následne sa prenesú do dizajnového systému. Tento dokument zaznamenáva odpovede, nie schválenie celého výsledku.

## Potvrdené odpovede

- **Materiál:** D — neumorphism.
- **Dojem:** „výrazne a technicky“.
- **Farby:** A — zachovať oranžovú z doterajšej ukážky ako hlavný akcent a nájsť k nej ostatné farby. Súčasná hodnota v pracovnom základe je `#ff4b24`; ostatná paleta zatiaľ nebola samostatne vybraná.
- **Písmo:** Adam žiada ukázať aspoň 12 dvojíc v HTML. Výber zostáva otvorený. [Porovnanie](fonty/fonty.html) obsahuje 12 dvojíc so skutočne vloženými písmami, úpravou skúšobného nadpisu a lokálnym označením favoritov.
- **Druhé kolo písiem:** po prvej strane Adam píše „nechj ten jeden a daj mi dalsiu stranu 12“. Pracovný výklad je ponechať 01 — Geist + Instrument Serif ako kandidáta a ukázať ďalších 12 možností. [Druhá strana](fonty/fonty-2.html) má čísla 13–24 a samostatný výber favoritov; pôvodný HTML súbor zostáva nezmenený. Nejde o konečné schválenie fontov.

- **Tretie kolo písiem:** Adam žiada vyradiť neoznačené, ponechať označené a pridať ďalších 12. Z označených tlačidiel v otvorených porovnaniach sú prevzaté **03 — Sora + Source Sans 3**, **14 — League Spartan + Source Serif 4**, **24 — Urbanist + Hanken Grotesk**. [Aktuálny prehľad](fonty/fonty-3.html) obsahuje iba tieto tri z predošlých kôl a 12 nových dvojíc **25–36**. Jednotka už nie je kandidátom v aktuálnom prehľade; najnovší pokyn ponechať iba označené nahrádza starší pracovný výklad. Výber zostáva otvorený. Staršie súbory sú zachované ako história.

- **Štvrté kolo písiem — experiment:** Adam označil ďalšie dvojice a žiada „12 výrazne odlišných, experimentuj“. Z tretieho kola prenášame označené **03, 14, 24, 33 — Rubik + Mulish a 36 — Dosis + Domine**. [Experimentálny prehľad](fonty/fonty-4.html) ponecháva týchto päť a pridáva **37–48**: bodkový displej, stencil, blackletter, mäkký ťažký serif, kontrastnú kurzívu, obrys, rukopis, glitch, hranaté sci-fi, farebné 3D, retro tieň a stekajúcu farbu. Extrémne rezy sú vedomé skúšky na Adamov pokyn; nejde o prijaté písmo systému. Farby a povrchy porovnania zostávajú rovnaké, Nabla má vlastnú farebnú kresbu ako súčasť fontu.

## Známy kontext

Web používa Astro/React. Strade zostáva hlavnou referenciou dizajnu, pohybu, vystavenia projektov a podania ponuky. XVADUR zahŕňa Adama, čítanie, projekty, obchod a spoluprácu.

## Zostáva zistiť

Konkrétne fonty a ich roly; podporná paleta; svetlý/tmavý režim; tvary ovládania; hustota rozloženia. Následná ukážka má tieto rozhodnutia overiť na skutočnej obrazovke. Nastavenie podkladu v porovnaní fontov je iba pomôcka na porovnanie.

## Spoločný pracovný katalóg — 20. 10. 2026

XVADUR Stack je názov vytváraného dizajnového systému; cieľový GitHub repozitár je `xvadur/system`. Katalóg na `http://127.0.0.1:4390/` prepája komponenty a tokeny, všetky štyri kolá fontov na `/fonty/` a galériu 54 obrázkov na `/obrazky/`. Ide o lokálne pracovné prostredie rozpracovaného systému.

Pri kontrole skutočne označených tlačidiel v štvrtom kole bol zachytený výber **03, 14, 24, 33, 36, 37, 39, 46 a 47**. Snímka aktuálnych favoritov je v `fonty/round-4/current-selection.json`. Tento záznam nenahrádza ďalšie zmeny v prehliadači a neznamená konečné prijatie typografie.

Adam spresnil poradie: **najprv spojiť galériu fotografií a fontové výbery; potom dokončiť dizajnový systém XVADUR Stack; potom z neho postaviť Lab; následne v Labe tvoriť hero sekcie.** Spoločná navigácia aktuálne slúži na prístup k existujúcim pracovným podkladom.


## Spresnenie rozsahu Stacku — 20. 10. 2026

XVADUR Stack je vlastný rozšíriteľný dizajnový systém, z ktorého chce Adam skladať rôzne vizuálne štýly, weby a nástroje. Teraz sa sústreďujeme na smer XVADUR a chceme sa vizuálnym spracovaním priblížiť Yanisovi / Strade. Neumorphism a oranžový akcent sú doterajšie rozhodnutia tohto smeru; neurčujú automaticky každý budúci projekt alebo všetky možnosti Stacku.

Lab bude prvým reálnym použitím a overením nášho Stacku pred stavbou webu. Výber cudzieho hotového UI frameworku nebol zadaním ani prijatým rozhodnutím. Predchádzajúce odporúčanie asistenta vybrať shadcn alebo Mantine ako hlavný základ nevystihovalo Adamov zámer. Výskum má hľadať použiteľné podklady pre vlastný systém a konkrétne spracovanie Yanisovej referencie, pri zachovaní rozpracovaných výberov fontov a obrázkov.

## Zlúčenie do Astro brand booku — 22. 10. 2026

Adam požiadal uložiť rozpracovaný systém na GitHub a mať dizajnový jazyk, komponenty, fonty a fotografie v jednom Astro webe. Tento krok zjednocuje podklady pred pokračovaním návrhu.

- `/` obsahuje prehľad rozpracovaného dizajnového jazyka a otvorených rozhodnutí.
- `/komponenty/` zachováva živé príklady 14 komponentov a tokeny.
- `/fonty/` obsahuje všetkých 48 dvojíc, filtre štyroch kôl a prenesených 9 favoritov.
- `/obrazky/` obsahuje 54 optimalizovaných náhľadov. Originály nie sú súčasťou repozitára.
- Stránky sú natívne súčasti jedného Astro projektu, bez iframe a pomocných Python serverov. Výbery sa ukladajú v prehliadači a prenášajú cez JSON export/import. Zmeny výberov sa automaticky neodosielajú do GitHubu.

Zdrojové dáta a médiá pre brand book sú v `catalog/data/` a `public/brand/`; pôvodné lokálne štúdie zostávajú zachované ako história. Rift sa neinštaloval. Vizuálne rozhodnutia a budovanie Labu nasledujú neskôr podľa prijatého poradia.
