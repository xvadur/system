# Vývoj komponentov

Nový komponent má riešiť konkrétne opakovateľné použitie. Kompozícia jednej stránky môže zostať vo webe; do knižnice prenes spoločné správanie alebo prvok, ktorý už chceme používať opakovane.

## Postup

1. Pomenuj použitie, props a potrebné stavy. Pri zmene existujúceho exportu urč, či sa mení jeho verejné správanie.
2. Pridaj alebo uprav zdroj v `src/components/` a verejný export v `src/index.ts`. Použi sémantické tokeny z `src/styles/tokens.css` a natívne HTML tam, kde poskytuje správne ovládanie.
3. Aktualizuj `registry.json`. Záznam má pomenovať zdroj, stav a príklad zhodný s implementáciou; `npm run check` overuje jeho väzby.
4. Pridaj živý príklad do `catalog/components/Catalog.tsx`. Použi verejný export balíka a produkčné štýly. Ukáž relevantné varianty, dlhší slovenský text a príslušné interaktívne stavy.
5. Over správanie. Test má zachytiť kontrakt alebo chybu: napríklad prepojenie popisu s inputom, zmenu stavu alebo výber správneho HTML elementu. Vykreslenie porovnaj pri úzkej aj širokej obrazovke, v oboch témach a pri obmedzenom pohybe, ak komponent animuje.
6. Spusti `npm run verify`. Pri pripravenom vydaní doplň verziu a popis zmeny podľa [releases](releases.md).

Zmena je pripravená na posúdenie, keď zdroj, export, register a príklad opisujú rovnaké API a kontroly prešli. Vizuálne prijatie sa posudzuje na vykreslenom príklade.

## Pravidlá rozhrania

- Props používajú bežné HTML/React pomenovania. Natívne atribúty a `ref` zachovaj, keď to význam komponentu umožňuje.
- Komponent si necháva obsah od spotrebiteľa. Skutočné ceny, sľuby a súkromné projektové údaje patria do schváleného obsahu konkrétneho webu.
- Interaktívny prvok má viditeľný fokus, dostupný názov a príslušné stavy. Ikona bez textu potrebuje dostupný názov od spotrebiteľa.
- Variant sa pridáva ako pomenovaná voľba s príkladom. Náhodné odlišnosti rovnakého komponentu na jednotlivých stránkach sa vracajú do spoločného rozhodnutia.
- Pri zmene, ktorá vyžaduje zásah spotrebiteľa, prilož krátky príklad pôvodného a nového použitia do changelog alebo samostatnej migračnej poznámky.
