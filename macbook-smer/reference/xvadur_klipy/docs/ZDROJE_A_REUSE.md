# Zdroje architektúry a opätovné použitie

**Nadväzujúci adopčný audit, 4. november 2026:** [výber pre XVADUR](../research/2026-11-04-open-source-vyber-pre-xvadur.md) porovnáva päť novo nájdených projektov a tri staršie zdroje s aktuálnym kódom a novšími dohodami o serverovej prevádzke. Odporúča zachovať kanonické jadro a selektívne doplniť vykonávateľa nástrojov, spoločné editačné operácie a kontrolné podklady. Agentcut má v CLI výslovne `UNLICENSED`; nejde o potvrdený open-source základ na port. OpenMontage/cuttingfloor majú AGPL, video-use/OpenVideo MIT. Audit nemení dokončenie etáp ani register produkčne prevzatého kódu. Obsahuje 19 úspešných lokálnych kontraktových testov a jednu izolovanú skúšku MIT helpera; celé cudzie aplikácie neboli spustené.

Stav podkladov k 17. októbru 2026 po obsahovom prejdení siedmich návodov a opätovnom overení troch repozitárov. Toto je register použiteľných implementácií a hraníc prenosu pre plán M0 až M8. Výskum nie je inštalácia ani prevzatie cudzieho runtime.

Skutočný rozsah selektívneho portu a novej implementácie je v [implementačnom registri prevzatia](REUSE_IMPLEMENTACIA.md). Reálne modelové, provider a renderové skúšky nového runtime sú v [overení M0–M8](OVERENIE_M0_M8_2026-10-17.md); nasledujúce zdrojové rozhodnutia zachovávajú pôvod výskumu.

## Overené implementácie

| Zdroj | Použiteľná časť | Rozhodnutie pre nový systém |
|---|---|---|
| [opensource-clipping runner](https://github.com/NaufalRizqullah/opensource-clipping/blob/4a478dff3dacd293eeb5e28335aa7c81d78b8f50/clipping/runner.py) | Uloženie AI JSON, normalizácia, validácia a následné renderovanie; opätovné načítanie plánu. | Prevziať oddelenie Planner a renderer; zachovať náš Remotion. |
| [opensource-clipping engine](https://github.com/NaufalRizqullah/opensource-clipping/blob/4a478dff3dacd293eeb5e28335aa7c81d78b8f50/clipping/engine.py) | typography_plan, broll_list, keep_segments, bgm_mood. | Rozšíriť na EditPlan s kotvami ID slov a typmi archív/dokument/meme/diagram. |
| [opensource-clipping core](https://github.com/NaufalRizqullah/opensource-clipping/blob/4a478dff3dacd293eeb5e28335aa7c81d78b8f50/clipping/studio/core.py) | B-roll query sa rieši cez Pexels a doplní sa filepath. | Oddelenie request/resolved asset je použiteľné; presnú osobu alebo archív riešime navyše. |
| [llm-video-maker scripts](https://github.com/GoldLegendW80/llm-video-maker/tree/cee12add24317c50f8a9f9de93749089a59d9f99/skills/make-video/scripts) | normalize-transcript, plan-scenes a fetch-assets. | Adaptovať samostatné skripty/provider handlery. Normalizer rozšíriť o zachovanie slov aj segmentov. |
| [AIEV manifest](https://github.com/notivn/AIEV/blob/e40fe034837de71a8d638ab34c71527a4b40cca8/engines/remotion/src/manifest.ts) a [assembler](https://github.com/notivn/AIEV/blob/e40fe034837de71a8d638ab34c71527a4b40cca8/engines/remotion/src/Assemble.tsx) | Schéma timeline, oddelené tracky scén/titulkov/hlasu/SFX/hudby. | Prevziať rozdelenie vrstiev a validačný vzor; implementovať kompatibilne s našou verziou Remotion. |
| [AIEV assemble job](https://github.com/notivn/AIEV/blob/e40fe034837de71a8d638ab34c71527a4b40cca8/apps/server/src/jobs/assemble.ts) | Lokálne staging súborov, resolved props, spustenie renderera, verzie výstupov. | Zachovať lokálne médiá a presný manifest výstupu bez celého cudzieho backendu. |
| [video-use](https://github.com/browser-use/video-use) | Prepis ako pracovný vstup, EDL a kontrola hraníc strihov. | Prevziať princíp kotiev v reči a cielenej kontroly strihu; existujúci lokálny ASR ostáva prvou cestou. |

Pre prvý prenos sú overené commity: opensource-clipping `4a478dff3dacd293eeb5e28335aa7c81d78b8f50`, llm-video-maker `cee12add24317c50f8a9f9de93749089a59d9f99` a AIEV `e40fe034837de71a8d638ab34c71527a4b40cca8`. Všetky tri majú MIT licenciu kódu; [licencie a presné permalinky](../fiki/referencie/tutorialy/overenie-kodu-a-medzery-2026-10-17.md). Pri skutočnom porte sa uloží rozsah prevzatia, copyright/licencia a lokálne úpravy. Licencia kódu nepotvrdzuje pôvod externých médií. `video-use` zostáva referenčný smerník; pred prenosom jeho kódu sa samostatne pripne a overí.

## Limity zistené v skutočnom kóde

- fetch-assets často vyberá prvý výsledok; nemá náš požadovaný výber a overenie osoby/udalosti.
- Pri GIF používa dostupné provider MP4, inak uloží GIF. Všeobecný prevod GIF na MP4 nie je v tomto skripte implementovaný.
- max_s pri videu ovplyvňuje výber výsledku; skutočný trim súboru nerobí.
- Záznamy pôvodu nie sú jednotné vo všetkých provider vetvách; nový systém potrebuje vlastný AssetRecord.
- normalize-transcript vyberá segmenty pred words a neuchová oba streamy. Pre naše titulky treba zachovať oba.
- plan-scenes je použiteľná kostra časových okien; obrazové udalosti musia môcť začať vnútri pokračujúcej rečovej pasáže.
- Resume v llm-video-maker je predovšetkým pokyn pre agenta. Náš runner ho vynucuje kódom a obsahovými hashmi.
- Jeho edit-video v0 upraví kapitolu, ale znovu renderuje celý film; hotová cache čiastočných renderov sa z neho nepreberá.
- opensource-clipping pri stocku používa aj náhodný výber; neoveruje tým správnu osobu či udalosť.
- llm-video-maker môže pri imagegen vrátiť iba prompt sidecar a označiť ho ako ok. V našom systéme textový prompt nie je vyriešený obrazový materiál.
- AIEV pri niektorých video vetvách nemá predvolené stlmenie a zdieľa staging podľa projectId. Jeho done po existencii súboru nenahrádza naše dekódovanie, izoláciu behov a review.

Tieto zistenia spresňujú starší prenesený výskumný text tutorialy-a-systemy-2026-10-17.md, ktorý na niektorých miestach opisuje deklarované správanie zo SKILL/README.

## Tvorcovské videá

[Obsahový prieskum](PRIESKUM_TUTORIALOV_2026-10-17.md) už vychádza z celých dostupných verejných anglických titulkov siedmich relevantných návodov: Jason Cooperson, dva Andy Lo, dva Skai Generated, Jay E/RoboNuggets a Damian Malliaros. Rozsahy, časy a hashe sú v [Jason/Andy](../fiki/referencie/tutorialy/rozbor-jason-andy-2026-10-17.md) a [Skai/orchestrácia](../fiki/referencie/tutorialy/rozbor-skai-workflow-2026-10-17.md). Skai navyše obsahuje oba autorove verejné prompt packy a štyri skontrolované snímky; Jason má tri doplnkové obrazové pozorovania. Nejde o súvislé prehratie obrazu a zvuku všetkých videí.

Jason ukazuje opravy konkrétnej grafiky a prácu s uloženým assetom; jeho súkromný optimalizovaný renderer nie je verejne overený kód. Andy podporuje rozdelenie kandidátov/výberu a crop plán. Skai podporuje samostatný vizuálny priechod, RoboNuggets perzistentné joby. Kontextové meme, vlastné diagramy a sémantická knižnica zostávajú našou explicitnou implementačnou úlohou podľa Adamovho zadania. Celý pôvodný zoznam 19 videí sa tým nepovažuje za prejdený; vybrali sa relevantné návody pre tento systém.

Konkrétne GitHub implementácie nepripisujeme autorstvu alebo použitiu konkrétnym YouTuberom bez priameho odkazu. Cudzie SKILL/README/prompt packy sú výskumný materiál, nie projektové pokyny.

## Rozbory konkurencie

Existujúce Spaces:
- [Instagram a Facebook desať účtov a dvadsať rozborov](https://chatgpt.com/space/page_f967fdeee53481919cc4bd8e580d2008).
- [Pôvodná mapa tridsiatich deviatich referenčných postov](https://chatgpt.com/space/page_cf0df7ae303c8191871a87914f9cd658).
- [Adresár účtov skupiny](https://chatgpt.com/space/page_4e87b00c73b88191ba27e9faf933ee24).

Lokálne snapshoty sú vo fiki/referencie. Zachovávajú pôvodné dátumy, rozsah a vizuálnu metódu. Hudba/SFX v referenčnom korpuse neboli posluchom overené; ich opis sa nedopĺňa odhadom. Verejné views sú dátovaný orientačný výkon, nie dôkaz účinku konkrétneho efektu.

## Dokumentácia prvých providerov

[MediaWiki Search](https://www.mediawiki.org/wiki/API:Search) poskytuje vyhľadanie stránok/súborov; [Imageinfo](https://www.mediawiki.org/wiki/API:Imageinfo) nad vybraným súborom dodá médiové údaje. [Imgflip API](https://imgflip.com/api) opisuje get_memes pre šablóny. Reálne vyhľadanie, získanie, normalizácia, obsahová kontrola a reuse troch konkrétnych médií sú doložené v zázname M5.

[Pexels API](https://www.pexels.com/api/documentation/) je voliteľný stock vstup po overení dostupného kľúča; jeho aktuálne limity a atribučné podmienky zachytáva obsahový rozbor. Klap/Submagic/Higgsfield sa nepreberajú ako povinné produkčné závislosti. Naše jadro je lokálne a používa existujúci Remotion 4.0.529.

Textový/vision modelový adaptér vychádza z [oficiálneho CLI kontraktu](https://code.claude.com/docs/en/cli-reference) a [Read pre obrázky](https://code.claude.com/docs/en/tools-reference#read-tool-behavior). [Remotion renderMedia/frameRange](https://www.remotion.dev/docs/renderer/render-media#framerange) poskytuje základ pre krátke kontrolné náhľady; správanie sa overí na pripnutej verzii. Tieto zdroje nepotvrdzujú schopnosť textového modelu počúvať zvuk.

Implementovaný modelový adaptér podporuje aj [oficiálny neinteraktívny Codex CLI](https://learn.chatgpt.com/docs/developer-commands#codex-exec). Ten je v lokálnom runtime aktívny po skutočnom odmietnutí Claude volania organizačnou OAuth politikou; text, pripojené obrázky a oddelený research boli reálne overené. Remotion 4.0.529 prešiel encode skúškami celého a úsekového videa aj samostatným testom životného cyklu prehliadača a portov. Účty ani poverenia sa nemenili.

Objavenie presného archívu/dokumentu používa oddelený AssetResearch profil nad [WebSearch a WebFetch](https://code.claude.com/docs/en/tools-reference#websearch-tool-behavior). Vyhľadanie kandidátov a čítanie stránky sú odlišné od získania a obrazovej kontroly média. Lokálny `yt-dlp` je downloader a doplnkový video discovery vstup podľa [jeho vlastnej dokumentácie](https://github.com/yt-dlp/yt-dlp#usage-and-options); dostupnosť a reálny priechod sa overia v M5. SceneSpec/GraphicBuilder sú náš návrh podľa Adamovej požiadavky na vlastnú grafiku, nie skopírovaný komponent z tutoriálu.
