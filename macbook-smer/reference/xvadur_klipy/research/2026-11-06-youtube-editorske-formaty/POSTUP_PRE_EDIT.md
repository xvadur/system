# Čo z druhého kola preniesť do editu

Pracovný návrh zo 6. novembra 2026 pre existujúci postup XVADUR. [Sedem hotových klipov](HOTOVE_KLIPY.md) · [Tri návody a verejný kód](NAVODY_A_KOD.md).

## Na začiatku vyber, čo má niesť scénu

| Situácia v reči | Konkrétne rozhodnutie editora | Kontrola výsledku |
| --- | --- | --- |
| Rozhovor, v ktorom odpoveď mení stávky | Ukáž skutočnú reakciu druhého účastníka ešte počas reči, ak je v zdroji súbežný záber. Vráť obraz na autora dôležitej repliky. | Vezmi tú istú vetu pred a po zmene. Rečník je stále identifikovateľný a obraz nikoho neukazuje v reakcii z iného momentu. [Team Coco](HOTOVE_KLIPY.md#1-team-coco--michael-douglas-a-rola-pre-otca) |
| Jedna praktická odpoveď po dlhšom vysvetlení | Daj zmene záberu presný okamih, keď rozprávanie prejde ku konkrétnej ukážke. Po zmene podrž čitateľný obraz cez celú ukážku. | Detail zlepší čitateľnosť rečníka a gestá. Veta, ktorá plní prísľub z úvodu, ostáva celá. [The Diary Of A CEO](HOTOVE_KLIPY.md#2-the-diary-of-a-ceo--otázka-na-konci-pracovného-pohovoru) |
| Reakcia na cudzie slová | Daj originálnemu výroku vlastný obraz s potrebným okolím a zdrojom. Vráť sa na rečníka, keď jeho reakcia začne niesť scénu. Ukonči ju na konkrétnej odpovedi na pôvodný výrok. | Divák rozozná citovaný výrok, interpretačný nápis a odpoveď. V strihu sa zachovala veta, ktorá určuje význam reakcie. [The Daily Show](HOTOVE_KLIPY.md#3-the-daily-show--citácia-reakcia-a-návrat-k-tej-istej-vete) |
| Skutočný viditeľný jav | V úvode ukáž zmenu stavu. V tele ju zopakuj na jednoduchom príklade a potom pomocou detailu alebo modelu ukáž príčinu. | Každý podklad má jasnú úlohu. Predpoklad, hypotéza či ilustračný rez sú označené pri vysvetlení, ku ktorému patria. [Steve Mould](HOTOVE_KLIPY.md#4-steve-mould--miznúca-farba-pokus-a-hypotéza) |
| Gag je v geste alebo rekvizite | Vyber úsek, kde sa činnosť dá prečítať od prípravy po výsledok. Reakciu daj hneď po odhalení, ak mení čítanie situácie. | Vo výreze vidno predmet pred zmenou, činnosť aj jej výsledok. Návrat nechá dohrať repliku alebo uvedie ďalší beat. [Game Changer](HOTOVE_KLIPY.md#5-game-changer--kostým-reakcia-a-výsledok-hlasovania) |
| Spor má viac výhovoriek | Každá ďalšia vložka odpovedá na novú výhovorku. Ak predmet vložky už je v zábere, nadviaž na jeho gesto alebo polohu a až potom otvor detail. | Po každej vložke je jasné, čo sa vyvrátilo a kto teraz reaguje. Záver sa môže vrátiť k pravidlu úvodného vtipu s novým príkladom. [Ryan George](HOTOVE_KLIPY.md#6-ryan-george--spor-eskaluje-cez-ukážky-a-v-závere-sa-zopakuje) |
| Bohatá scéna zahlcuje hlavný údaj | Uprav v prvom kroku jeden vzťah medzi vrstvami. Napríklad z dvoch tabuliek vyber porovnávaný ukazovateľ, podrž jednotku a potrebné obdobie a zvýrazni smer zmeny. | Na páre snímok je vidno, čo prevzalo pozornosť. Menšia hustota nesmie odstrániť podmienku ani zmeniť význam výroku. [Devin Jatho](HOTOVE_KLIPY.md#7-devin-jatho--hustý-edit-v-ktorom-grafika-predvedie-vlastnú-opravu) |

## Čo má byť viditeľné v autorskom pláne

1. **Celá pasáž.** Zapíš otázku alebo prísľub z hooku, potrebný kontext, obrat a vetu, ktorá klip uzatvára. Pomenuj, čo nesie každý medzikrok. Pri čistom obraze rečníka môže byť nositeľom gesta, napätia alebo zmyslu práve jeho tvár.
2. **Prenos jednej konkrétnej akcie.** K vybranému beatu pripoj zdroj a interval. V existujúcom `EditPlan.editorial` sú na to kotvy `spanId` a `wordIds`, zdroj v `axes[].refs`, funkcia a dôvod, `expectedResult` a `test`. Zapíš stav pri vstupe, zmenu na slovnej kotve a podmienku odchodu. Časy referencie pomáhajú vysvetliť mechanizmus. Časy v novom klipe sa odvodia z jeho reči.
3. **Materiál podľa akcie.** Pri skutočnom zdroji hľadaj konkrétny interval a čitateľný kontext. Pri komickej či ilustračnej akcii vyber medzi videom, GIFom, účelovou grafikou a generovaným obrazom podľa toho, čo urobí plánovaný pohyb. Vložku skontroluj s Fikiho titulkovým komponentom a tvárou v najplnšom stave.
4. **Odovzdanie cez existujúci postup.** Keď Adam zadá výrobu, autorský plán ide cez `navrhni --plan`. Tvorba a porovnávanie revízií pokračujú v pripnutom Remotione. [Schéma plánu](../../system/schemas/editorial.ts) · [Výrobný postup](../../docs/CODEX_VYROBNY_POSTUP.md).

## Ako uzavrieť jednu konkrétnu opravu

Príklad pre budúcu pasáž s citáciou. Citovaný človek dohovorí a vložený zdroj ešte zakrýva prvú reakciu moderátora. Nález patrí eventu so zdrojom. V novej revízii posuň výstup zdroja na koniec citovaného výroku a prever, že prvý pohľad aj odpoveď vidno na tvári. Ak sa na vstupe prehráva čitateľná identifikácia zdroja, drž ju do konca citácie. Over predchádzajúcu a novú revíziu na kotvách pred odchodom, pri prvom výraze a pri začiatku odpovede.

- Skontroluj, čo patch mení v pláne a čo sa následne posunulo v Timeline. Pri obrazovej oprave porovnaj pôvodnú reč, titulky a netknuté udalosti podľa kotiev. Podľa potreby otvor aj zhodné snímky za opravovaným úsekom.
- Použi krátky náhľad s oboma hranami eventu a následne celý aktuálny draft. K nálezu ulož dôkaz pred a po v rovnakej fáze akcie. Pri zmene časovania páruj snímky podľa reči a fázy, lebo rovnaká sekunda môže v dvoch verziách patriť inému stavu.
- Výsledok a hranice kontroly zapíš k existujúcej revízii. Až keď sa technika hodí na ďalšie použitie, oddeľ parametre od konkrétneho záberu a over ju samostatne aj v reálnom klipe. Prijatú pripomienku ulož s rozsahom, ku ktorému ju Adam dal. [Kontrola a opravy XVADUR](../../docs/KONTROLA_A_OPRAVY.md) · [Ukážky revízií a kódu](NAVODY_A_KOD.md).

Pri najbližšom zadanom klipe sa dá overiť jedna pozorovateľná vec. Editor sám premietne relevantný mechanizmus do celého kandidáta a pri pripomienke ukáže porovnanie v tom istom momente. Pre cieľ 1 200 klipov mesačne má zmysel zaznamenať čas editora a počet režijných zásahov až na reálnej dávke. Tento výskum meral jednotlivé referencie, takže o výrobnej kapacite zatiaľ nič nevyčíslil.
