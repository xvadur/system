# Odovzdávka pre MacBook

Stav balíka k 7. novembru 2026. Cieľom je umožniť Adamovi a Codexu pokračovať v samostatnom Smer projekte s existujúcim know-how. Aktívne pokyny sú v [AGENTS.md](../AGENTS.md) a [SMER_BRIEF.md](SMER_BRIEF.md).

## Čo už máme

- Celý prispôsobený `remotion-reel`: práca s významom pasáže, slovné kotvy, vlastné TSX scény, médiá podľa nápadu, obrazová a zvuková kontrola, opravy. Python prostredie sa obnovuje lokálne; jeho cache nie je zdroj skillu.
- Oficiálne Remotion skills a pripnutý základ projektu `smer/` s registračným vstupom, `Root.tsx` a technickou kartou `WorkspaceReady`. Balík prenáša zdroje a lockfile, nie nainštalované závislosti. Karta slúži na overenie načítania Studia a neurčuje Smer štýl.
- Textové syntézy a karty konkurenčných aj zahraničných referencií. Nezačíname nový zber stoviek videí ani rozhovor o vkuse. Pre konkrétny edit stačí vybrať relevantné mechanizmy a podľa potreby otvoriť zdrojový úsek.
- Zdrojový kód Fikiho systému vrátane novej autorskej cesty `autor`. Je to referenčný kód na selektívne použitie v samostatnom projekte.

## Aktuálna technická voľba

Renderujeme v Remotione. Užitočné režijné princípy HyperFrames sa prenášajú do frame-driven TSX kompozície. FFmpeg/ffprobe slúžia na meranie, prípravu a technické kontroly médií; yt-dlp podľa potreby na získanie zdroja. Editor smie napísať celý obraz, lokálne komponenty, animáciu, masky a podporný zvuk.

`reference/xvadur_klipy/docs/AUTORSKE_SCENY.md` opisuje implementované `autor priprav → manifest → over → render → kontrola`. Tento runtime používa Remotion 4.0.529 s vlastným lockfile a zachováva pripnutú reč. Jeho existujúci klientský kontext však stále povoľuje Fiki a príprava očakáva jeho kanonické Source/Transcript/Selection/Timeline. Samotná prítomnosť kódu preto neznamená hotovú Smer CLI. Na MacBooku začni v `smer/`; prenos konkrétnych helpers alebo adaptácia pipeline má byť samostatná overiteľná zmena.

Staršie poznámky o izolovanom JSON plánovači opisujú staršiu vetvu. Nepoužívaj ich ako strop tvorivých schopností celej súčasnej autorskej cesty. Najnovšie zdroje sú `docs/AUTORSKE_SCENY.md`, `system/pipeline/authoring.ts` a skillové `references/whole-scene-authoring.md` v prenesenej kópii.

## Referencie na začiatok

Cesty sú relatívne ku `reference/xvadur_klipy/`:

| Potreba | Zdroj |
| --- | --- |
| Striedmy rozhovor, presný návrat na reakciu, citácia | `research/2026-11-06-youtube-editorske-formaty/HOTOVE_KLIPY.md` a `POSTUP_PRE_EDIT.md` |
| Porovnania, meniaci sa stav, čísla a pointa | `research/konkurencia/zdroje/2026-11-06-top100-remotion-reel/POSTUPY_PRE_EDIT.md` a príslušné `cards/` |
| Širší repertoár Fiki kliperov | `research/konkurencia/ZISTENIA.md` a `zdroje/2026-10-27-nocny-research/VYSLEDKY.md` |
| Hustý strih a jasné vedenie pozornosti | `research/2026-11-05-husty-strih-zahranicne-referencie.md` |
| Celé scény a konkrétne opravy | `research/2026-11-06-youtube-referencie/POSTUPY_PRE_EDIT.md` a karty |

Korpus obsahuje dokončené obrazovo-významové rozbory aj staršie výbery a metriky; dávky sa prekrývajú. Rozbory používajú vzorkované snímky a prepisy a výslovne uvádzajú hranice posluchu a pohybu. Použi ich konkrétne pozorované mechanizmy. Médiá, snímky a historické absolútne cesty nie sú automaticky dostupné na MacBooku; [mapa balíka](PATH_MAP.md) určuje, čo sa prenieslo.

## Čo potrebuje prvý Smer edit

Aktuálny zdroj a Adamom zvolená pasáž ešte nie sú dodané. Keď prídu, over miestne nástroje, zmeraj médium, priprav spoločné časovanie reči a titulkov a vytvor treatment a TSX v `smer/`. Nepredpokladaj fps, rozmery ani správnosť surového ASR. Ak Adam požiada o výber, priprav čitateľných kandidátov z celku.

Prvý klip a jeho náhľad majú overiť konkrétny výsledok. Balík sám nedokladá funkčnú inštaláciu na MacBooku, hotový Smer edit ani mesačnú kapacitu. Neobsahuje sociálne prístupy, produkčnú databázu, pôvodné médiá ani publikačný stav; úloha na MacBooku je editovanie.
