# XVADUR UI

Tento repozitár vlastní tokeny, opakovateľné komponenty `@xvadur/ui`, ich register a katalóg. Konkrétny web vlastní obsah, routy a skladbu stránok.

- Pri pridávaní alebo zmene komponentu postupuj podľa [docs/contributing.md](docs/contributing.md). Hotová zmena má zdroj, verejný export, záznam registra, živý príklad a primerané overenie správania.
- Pri integrácii do webu alebo zmene verejného API čítaj [docs/integration.md](docs/integration.md). Zachovaj kompatibilitu alebo výslovne popíš migráciu.
- Pri zmene verzie, tagovaní alebo príprave vydania čítaj [docs/releases.md](docs/releases.md). `version:next` pripravuje súbory; commit, push, tag a nasadenie potrebujú aktuálne používateľské zadanie.
- Nové vizuálne rozhodnutie označ v príklade a dokumentácii ako návrh, kým ho Adam neprijme. Úspešný build ani existencia tokenu neznamenajú schválenie štýlu. `soft` a `neumorphic` sú experimentálne alternatívy.
- Zachovaj samostatnosť balíka: katalóg používa verejné exporty a rovnaké štýly ako spotrebiteľ. Príklady používajú verejné alebo výslovne schválené podklady.
