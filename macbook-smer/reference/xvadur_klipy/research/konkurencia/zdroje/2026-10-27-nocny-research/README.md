# Fiki: výsledok nočného výskumu 27.–28. októbra

**Hotový je obsahový výskumný blok 20 autorov × 5 referencií, 15 historicky ZLE ukážok a 5 našich klipov.** Všetkých 120 má skutočne prezreté obrazové dôkazy a individuálny rozbor v zodpovedajúcej správe. Surové prepisy dopĺňajú orientáciu tam, kde sú zrozumiteľné. Žiadne video nebolo v tomto výskume celé súvislo prehraté ani vypočuté; zvuk a úplná pohybová kvalita zostávajú otvorené.

**Čo z toho vyplýva:** naše posledné Vajanského/Električka majú doložený posun v obrazovej réžii a v tejto vlastnosti sa medzi skúmanými referenciami nestrácajú. Silné jednoduché výbery konkurencie ukazujú, kde zložitá animácia nie je potrebná. Máme materiálový základ na ďalšie konkrétne videá; nemáme ešte preukázanú samostatnú kapacitu piatich prijatých klipov denne.

## Začni týmito troma výsledkami

| Čo potrebuješ vedieť | Výstup |
|---|---|
| Čo konkrétne robí všetkých dvadsať autorov a čo z toho prevziať | **[VYSLEDKY.md](VYSLEDKY.md)** — rozcestník 20 rozborov, prenosné schopnosti a podklady |
| Kde stojíme oproti úspešným a historicky ZLE | **[POROVNANIE_KVALITY.md](POROVNANIE_KVALITY.md)** — rovnaké kritériá, staršie verzus posledné dva a podobné zdrojové pasáže |
| Ako z nasledujúcej pasáže spraviť edit | **[RECEPTY_NA_VYROBU.md](RECEPTY_NA_VYROBU.md)** — 8 výskumných postupov, spúšťače, fázy, reálne súbory, chýbajúce vstupy a kontrola |

## Čo je naozaj hotové

- **100/100 hlavných referencií**, 20 samostatných autorských správ; plus [15/15 historicky ZLE](rozbory/kontrola-zle.md) a [5/5 našich](rozbory/nase-porovnanie.md). Hodnotenie neudeľuje celkové poradie 82 členov.
- 120 dostupných referenčných médií; overené zdrojové hashe, individuálne dôkazy a opravené časové snímky. [Pokrytie každej položky](pokrytie-120.json).
- 120 surových ASR súborov; 3 známe obsahové zlyhania, pri jednom čiastočná obnova. Minimálnych 119 súborov s písmenami sa neoznačuje za 119 správnych prepisov. [Kontrola ASR](prepisy-kvalita.json).
- [Nezávislá kontrola](KONTROLA_VYSKUMU.md): 12 reprezentatívnych klipov, konkrétne sporné detaily, materiálová pripravenosť a záverečné recepty. Bez predstierania nového posluchu.
- Dve novo získané a prezreté [čisté NASA fotografie s pôvodom](podklady/nasa/README.md). Sú výskumné podklady; nepočítať ich ako už prijaté produkčné použitie.
- **0 nových finálnych klipov, 0 publikácií, 0 zmien produkčného runtime.** Ďalšia výroba potrebuje Adamovu Selection.

## Vstupy, dôkazy a stav

| Úloha | Zdroj |
|---|---|
| Presné zadanie a hranice | [ZADANIE.md](ZADANIE.md) |
| Dokončenie, medzery, ďalší krok a automatizácia | [STAV.json](STAV.json) |
| Technické overenie finálnych výstupov | [overenie-vysledkov.json](overenie-vysledkov.json), opakovateľný [over_vysledky.py](over_vysledky.py) |
| Starý výskum: 89 unikátnych podrobných rozborov | [AUDIT_EXISTUJUCEHO.md](AUDIT_EXISTUJUCEHO.md) |
| Existujúce médiá, dva produkčné recepty a zvukové medzery | [PODKLADY_NA_VYROBU.md](PODKLADY_NA_VYROBU.md) |
| Pravidlá a zmrazené metriky výberu | [VYBER.md](VYBER.md), [vyber-100.json](vyber-100.json) |
| Kontrolná vzorka a YouTube náhrady | [kontrolna-vzorka.json](kontrolna-vzorka.json) |
| Získanie referencií | [acquisition.json](acquisition.json), [stav prípravy](priprava.pid.json) |
| PTS oprava a natívny formát verzus analytický padding | [EVIDENCIA_CASOVANIA.md](EVIDENCIA_CASOVANIA.md), [evidence-r2.json](evidence-r2.json) |
| Surové ASR a jeho rozsah | [prepisy.json](prepisy.json), [prepisy-kvalita.json](prepisy-kvalita.json), [stav procesu](prepis.pid.json) |

VYBER, pôvodný audit a akvizičné/evidenčné manifesty zachovávajú stav svojho vzniku; ich pôvodné `not_reviewed` neprepisujeme spätne. Aktuálne dokončenie spája [pokrytie-120.json](pokrytie-120.json) so správami a STAV. Stiahnuté hotové referencie nie sú databáza čistých produkčných assetov.

Nasledujúci krok: vybrať jednu uzavretú pasáž, priradiť jeden z ôsmich postupov, doplniť iba adresné chýbajúce vstupy a overiť novú revíziu obrazom, pohybom aj posluchom. To overí opakovateľnosť remesla, ktorú samotný výskum ešte nepreukázal.
