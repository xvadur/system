# XVADUR — nastavenie remotion-reel

Nastavené 5. novembra 2026 podľa Adamových priamych požiadaviek, existujúcich komponentov a uložených rozborov. Je to pracovná konfigurácia editora; nový klip aj naďalej podlieha Adamovmu tvorivému posúdeniu.

## Režim práce

Predvolený klient tohto projektu je **Fiki**. Pokračujeme v existujúcom **Remotione**. Pri zadaní editovania AI samostatne vyberá podporné médiá, obrazové nápady, pohyb a zvuk podľa významu. Ak Adam žiada najprv návrh, dokonči tento návrh pred výrobou. Konfigurácia skillu sama nespúšťa render.

Pripravená knižnica nie je vstupná podmienka výroby ani povinná prvá brána. Existujúci asset sa použije, keď sedí na nový obsah. Nové vyhľadanie, imagegen a autorská scéna sú rovnocenné možnosti podľa potrieb scény. Knižnica sa dopĺňa z konkrétnej práce.

**Referencie už poskytujú základnú predstavu.** Začni ich existujúcimi rozbormi a konkrétnymi opravenými/prijatými prvkami. Namiesto nového rozhovoru o vkuse prenes relevantný mechanizmus do ďalšieho editu. Rozbor má viesť ku konkrétnemu obrazu, načasovaniu alebo rozhodnutiu.

## Fiki — tvorivý smer

- Celý klip má silný nástup, zrozumiteľný vývoj a pointu. Zachovaj význam a potrebný kontext zdroja.
- Výrazný, bohatý edit: meme, GIFy, B-roll, účelné zoomy, kompozícia, prechody, pohyb a zvuk. Vhodnosť sa posudzuje podľa konkrétnej reči a obrazovej akcie.
- Ťažisko je v B-rolle, GIFoch a meme. Vlastná ilustrácia či animácia rieši konkrétny nápad; nie je povinnou náhradou reálneho videa.
- Spresnenie 6. novembra: AI má vedieť napísať celé prepracované scény priamo v Remotione a koordinovať všetky ich prvky. Rozsiahla animácia je riadna možnosť podľa významu; staršia preferencia médií neurčuje jej strop. Používaj celý `remotion-reel` a autorskú cestu `autor`; užitočnú réžiu z HyperFrames/ReelMimic prenes do Remotionu bez druhého renderera.
- Spracuj každú vetu kandidáta podľa pravidla nižšie. Počet vrstiev a dĺžku scén určuje obsah; pokrytie musí zahŕňať celý kandidát.
- Pôvodný hlas môže pokračovať cez celoplošné meme/B-roll. Striedaj vhodné formáty podľa deja, nie podľa pevného pomeru tváre a vložiek.
- Meme vyber podľa gesta, situácie a pointy v skutočnom použitom intervale. Pri návrate rovnakého motívu rozvíjaj jeho funkciu; dostupnosť súboru sama nie je dôvodom na opakovanie.
- Použi imagegen na obraz na mieru, keď to vyrieši významový obraz alebo gag. Pri ilustrovaní konkrétnej skutočnej udalosti odlišuj ilustráciu od dokumentárneho podkladu.
- Zvuk priprav ako súčasť konkrétnej akcie. Vhodné hotové SFX sú bežná voľba, generovanie podľa potreby. Hudbu a zvuk nezamieňaj za vypočuté len preto, že existuje súbor.
- CTA text v popisoch: „viac na fiki.sk“. Dĺžku koncovej obrazovky nepridávaj automaticky.

## Fiki — edit každej vety

Adamovo spresnenie zo 6. novembra 2026: **„na kandidáta na každú vetu bol proste edit“**. Požiadavka sa vzťahuje na celý vybraný kandidát, vrátane vysvetľujúcich a spojovacích viet.

- Každá veta dostane konkrétny realizovaný obrazový zásah alebo konkrétny vývoj už bežiacej scény. B-roll, meme, GIF, ilustrácia, koláž, grafika, typografická pointa či práca so zdrojovým záberom musia vyjadrovať význam tejto vety. Samotné priebežné titulky sa za jej edit nepovažujú.
- Spoločná scéna môže pokryť viac viet: pri každej urč jej ďalšiu akciu, odhalenie, zmenu vzťahu alebo načasované držanie a dopad reakcie. Návrat na Fikiho je konkrétne načasovaný záber na repliku, gesto či výraz. Všeobecné označenie „A-roll“, „zoom“ alebo nezmenený obrázok bez funkcie pre danú vetu pokrytie nedokladá.
- Ku každej vete urč aj zvukové spracovanie: konkrétny SFX a jeho dopad, pokračovanie alebo zmenu hudby, ruch vložky či zámerne čistý pôvodný hlas. Zvuk podporuje obrazovú akciu a zrozumiteľnosť reči.
- Pred výrobou interne prejdi kandidáta vetu po vete. V existujúcom CreativeBrief/EditPlan zachyť rozsah skutočných slov, význam, obrazovú akciu, konkrétne médium alebo scénu, zvuk a nástup/dopad/výstup. Prepájaj vety so zodpovedajúcimi udalosťami; zachovaj jednu kanonickú časovú os. Túto prácu robí editor, Adam nemusí zadávať jednotlivé zásahy.
- Pri kontrole prejdi rovnaké vety vo výslednom renderi. Každá musí mať zodpovedajúce realizované spracovanie; chýbajúce miesto je nedokončená práca. Over aj nadväznosť medzi vetami, hook, rozvinutie a pointu. Úplnosť plánu sama nepreukazuje úplnosť ani kvalitu výsledku.

## Fiki — presný existujúci titulkový základ

Použi implementáciu, nie vizuálnu napodobeninu napísanú od nuly:

- Variant: `chocolate-r5-word-pulse@1.0.0`.
- [Pulz, geometria a meranie](../system/renderer/src/captions.ts), [ChocolateCaptions](../system/renderer/src/TimelineComposition.tsx).
- [Existujúci production pack a font](../fiki/kniznica/production-packs/fiki-default-0.1.0.json). Pack má stav `calibration`; jeho použitie neznamená prijatie všetkých scén alebo zvukov v ňom.
- Slovenské uppercase, Arial Black 900 z pripnutého font súboru; aktívne slovo `#FFE45C`, ostatné biele.
- Geometria pri 1080 × 1920: veľkosť 78 px, top 1450 px, obrys 6 px, medzera 20 px; vo vyššom výstupe sa škáluje. Skontroluj reálnu tvár, obraz a čitateľnosť.
- Pop aktívneho slova `.88 → 1.12 → .99 → 1` v `0 / 80 / 200 / 320 ms`; merané miesto zabraňuje horizontálnemu poskakovaniu susedných slov.
- Zachovaj existujúce zoskupovanie podľa meranej šírky a fráz. Univerzálny limit 17 znakov, lowercase a zákaz popu zo zdrojového skillu sa nepoužívajú.

Žltý akcent a titulkový základ držia rozpoznateľnosť. Ostatnú grafiku a materiál prispôsob situácii; nie je schválená univerzálna „krabičková“ grafika pre každý význam.

## Smer — uložený tvorivý smer

Adam aktuálne plánuje aj Smer: zdržanlivejší, jednoduchší edit, výborná štruktúra, silný hook a úderné jadro. Rozvíjaj argument a kontext, používaj konkrétne podklady a striedmejšie obrazové/zvukové akcenty.

Toto je smer pre zadanie Smer, nie schválená paleta, logo alebo titulkový komponent. Fikiho gagy a hustotu neprenášaj automaticky. Aktuálny runtime projektu má klienta Fiki; vznik klienta Smer a jeho konkrétna výbava sú samostatná implementácia pri zadaní výroby preň.

Objemový cieľ pre oba smery je 1 200 mesačne, rozdelenie nebolo určené. Milión videní je Adamov výkonnostný cieľ, nie vlastnosť šablóny alebo overená kapacita systému.

## Referencie, z ktorých editor už má čerpať

| Zdroj | Prenos do ďalšieho klipu |
| --- | --- |
| [Druhé kolo YouTube referencií](../research/2026-11-06-youtube-editorske-formaty/HOTOVE_KLIPY.md) a [pracovný postup](../research/2026-11-06-youtube-editorske-formaty/POSTUP_PRE_EDIT.md) | Sedem Shorts mimo Fikiho a tri návody. Vyber podľa funkcie scény, napríklad reakcia poslucháča, čitateľná citácia, fyzický gag alebo postupná oprava obrazovej hierarchie. Pri oprave porovnaj rovnakú fázu akcie v oboch revíziách. Podklady odlišujú snímky, prepis a numerické meranie zvuku. |
| [YouTube: 7 Shorts + 6 návodov — 6. 11. 2026](../research/2026-11-06-youtube-referencie/REFERENCIE.md) a [konkrétne použitie pri edite](../research/2026-11-06-youtube-referencie/POSTUPY_PRE_EDIT.md) | 13 videí, 102 časových úsekov. Rišo: rozklad scény na aktívne vrstvy; Ryan: referencia / stará verzia / nová verzia; Aidan a Nate: cielená oprava pri zachovaní funkčného zvyšku; Max, Johnny, Cleo a Colin/Samir: významový B-roll, jedna vyvíjajúca sa scéna a uzavretá pointa. Pri prenose pomenuj konkrétnu akciu a ukáž, kde sa prejavila vo výsledku. Prepisy a vzorkovaný obraz; posluch a súvislé prehratie neboli posúdené. |
| [100 výkonnostných referencií — nový rozbor 6. 11. 2026](../research/konkurencia/zdroje/2026-11-06-top100-remotion-reel/REFERENCIE.md) a [12 konkrétnych postupov](../research/konkurencia/zdroje/2026-11-06-top100-remotion-reel/POSTUPY_PRE_EDIT.md) | 100 príspevkov od 36 historicky doložených skupinových účtov, 415 časových beatov. Výber podľa výkonu voči vlastnému mediánu k 27. 10. 2026. Pri novom edite vyber podľa funkcie 2–3 konkrétne karty, otvor príslušný úsek a prenes spúšť → obrazovú akciu → pointu → návrat. Vzorkovaný obraz a ASR; SFX, hudba ani súvislé prehratie nie sú potvrdené. |
| [Čokolády r5](../fiki/epizody/108/praca/reference-r5/rendery/Fiki108-Cokolady-reference-r5-1080.mp4) a existujúci kód titulkov | Presný titulkový vzhľad a slovný pulz. FPS konkrétnej referencie sa nemení plošne na 30. |
| [Pas r4](../fiki/epizody/105/praca/pas-pilot/rendery/Fiki105-Pas-r0004.mp4) | Súvislá situácia a vrstvy sa vyvíjajú s jednotlivými vetami; spoločná scéna udržuje nadväznosť ich spracovania. |
| [Vajanského r12](../fiki/epizody/vallo-2026-10-21/praca/vajanskeho-r1/render/vajanskeho-r0012.mp4) | Konkrétny referent, situácia a načasovaná reakcia. |
| [Detroit — rozbor](../research/konkurencia/zdroje/2026-10-21-fikisulik_klipyy/videa/7693174026734177559/ROZBOR.md) | Viacvrstvové spracovanie a návrat s novou pointou; adaptovať mechanizmus na nový obsah. |
| [SOWA — rozbor](../research/konkurencia/zdroje/2026-10-21-fikisulik_klipyy/videa/7693962715596868886/ROZBOR.md) | Konkrétny obrazový referent, zámena a návrat. |
| [fiki.extra — detail](../research/2026-11-02-fiki-extra-detail/ROZBOR.md) | Načasovanie telefónu/fotografie, pohyb a súbeh titulkov. |
| [Priame pochvaly a opravy](../research/2026-11-05-fiki-chaty/AKO_MAJU_VYZERAT_KLIPY.md) | Zoom na pôvodný obraz pri výroku a Rossovo gesto sú prijaté konkrétne nápady. „Hodnotím“ je príklad, nie celé zadanie. |
| [Svedomie #110 — prijatý 27-sekundový náhľad](../fiki/epizody/110/praca/svedomie-rezia-r1/Fiki110-Svedomie-rezia-r2.mp4) | Adam 6. 11. 2026 pochválil prechody, zvuky a animácie. „Kto som ja?“ má obrazový detail, „čo som dokázal“ skutočnú akciu s následkom a „všetko“ príde po stíšení ako odhalenie. Pri V2 tohto klipu výslovne žiadal viac boxu, dramatickejšiu hudbu a väčšiu hustotu. |

[Register referencií](../research/2026-11-05-fiki-chaty/REFERENCIE.md) zachováva pôvod, dostupnosť a hranice ich posúdenia. Svedomie r5/V1 a Edits r1 sú aj negatívne referencie; publikovanie sa nerovná všeobecnému prijatiu štýlu. Staré záznamy o views sú dátované pozorovania, nie dôkaz, že výsledok spôsobil jeden efekt.

## Pri oprave

Uprav požadované miesto a jeho závislosti. Zachovaj funkčný zvyšok, konkrétny titulkový variant, hlasový strih a uzamknuté rozhodnutia. Výsledok porovnaj s predchádzajúcou verziou aj s použitou referenciou. Krátky gag alebo nový komponent nenahrádza spracovanie zvyšku klipu.
