# Nástroje pre 1 200 rôznych klipov mesačne

Overené 6. 11. 2026 z primárnych dokumentácií a verejných repozitárov. Ide o výskum, nie produkčný benchmark. Nič sa neinštalovalo, nerenderovalo ani nepublikovalo.

## Cieľ a hranica záveru

Adam v tomto chate spresnil cieľ: **1 200 rôznych videí mesačne, 600 Fiki a 600 Smer**, distribuovaných v každej vetve medzi osem účtov. Pri 30 dňoch to znamená 40 hotových videí denne, 20 na vetvu. Počet účtov neznižuje potrebný počet originálnych videí. Toto spresnenie samo nemení existujúcu konfiguráciu jediného klienta fiki.

**Následné spresnenie v tom istom chate:** rôzne hotové videá môžu byť samostatné štýlové spracovania tej istej obsahovej pasáže. Adamov príklad: 40-minútový zdroj → približne 20 kandidátov → všetky použiteľné klipy → ďalšie spracovania v inom štýle. Cieľ nevyžaduje 1 200 rozdielnych tém ani pasáží. AI má vychádzať z existujúcich referencií; Adam môže pri konkrétnom kandidátovi nadiktovať réžiu. Konkrétne prepojenie existujúcich častí opisuje [návrh dávkovej výroby a variantov](2026-11-06-davkova-vyroba-varianty.md).

Najnovšie projektové smerovanie podľa rodičovského auditu zostáva Remotion a existujúci výtvarný smer. Náš záver: zachovať hlavný renderer a hľadať konkrétne chýbajúce výrobné mechanizmy. Ďalší renderer sám nevyrieši výber pasáže, dobrý strih ani prijatie výsledku. Žiadny z nižšie uvedených zdrojov nedokazuje 1 200 Adamom prijateľných slovenských klipov mesačne.

## Čo jednotlivé nástroje skutočne dodávajú

| Nástroj | Doložená schopnosť | Úloha v našej zostave |
| --- | --- | --- |
| yt-dlp | Sťahovanie zdrojov; `--download-archive` eviduje už stiahnuté ID. | Vstup a opakovateľné získanie zdroja. Nevyberá významové pasáže. |
| FFmpeg + ffprobe | Prevod, strih, filtrovanie; `loudnorm`, `silencedetect`, `blackdetect`. | Technická príprava, export a signály pre kontrolu. Ticho či čierny obraz sú technické signály, nie automatický dôkaz zlého strihu. |
| Whisper / faster-whisper | Slovenčina `sk`; faster-whisper poskytuje slovné časy a dávkové spracovanie. | Prepis urobiť raz na zdroj, uchovať slová aj segmenty. Názvy osôb, negácie a čísla stále treba overovať. |
| WhisperX | Zarovnanie prepisu na zvuk; aktuálny `alignment.py` obsahuje explicitný slovenský model `comodoro/wav2vec2-xls-r-300m-sk-cv8`. | Kandidát na presnejšie hranice slov. Je to doložená dostupnosť modelu, nie meranie presnosti na Fikim. |
| Remotion | Programové kompozície, náhľady a render. Oficiálne skills sú návody a odporúčania pre agenta; Lambda rozdeľuje render na paralelné úseky. | Hlavný obrazový a titulkový renderer; opakovateľné komponenty a dátový plán namiesto znovupísania celej kompozície pre každý klip. |
| HyperFrames od HeyGen | HTML/CSS/médiá a seekovateľné animácie renderuje do MP4; CLI, agent skills, katalóg prvkov; Node 22+ a FFmpeg; Apache-2.0. | Voliteľný výrobca grafických vložiek, diagramov a typografie. Súbežná migrácia celého editora nie je podmienkou kapacity. |

Primárne zdroje: [yt-dlp README](https://github.com/yt-dlp/yt-dlp#usage-and-options), [FFmpeg](https://ffmpeg.org/ffmpeg.html), [FFmpeg filtre](https://ffmpeg.org/ffmpeg-filters.html), [Whisper jazyky](https://github.com/openai/whisper/blob/main/whisper/tokenizer.py), [faster-whisper implementácia](https://github.com/SYSTRAN/faster-whisper/blob/master/faster_whisper/transcribe.py), [WhisperX slovenské zarovnanie](https://github.com/m-bain/whisperX/blob/main/whisperx/alignment.py), [Remotion skills](https://www.remotion.dev/docs/ai/skills), [Remotion renderMedia](https://www.remotion.dev/docs/renderer/render-media), [Remotion Lambda](https://www.remotion.dev/docs/lambda), [HyperFrames](https://github.com/heygen-com/hyperframes).

## Cudzie projekty: konkrétne mechanizmy na skúšku

**[I Hate Editing](https://github.com/ranahaani/i-hate-editing)**, MIT. Autor dokumentuje opätovný prepis krátkeho okna pri každom šve, jazykovú kontrolu titulkov, načasovanie počuteľného vrcholu SFX, záznam opráv v `taste.md` a Remotion grafiku. Užitočný je najmä princíp: kontrolovať výsledný strih, nielen vstupný prepis. Doložený je opis autora a existencia repozitára; tento prieskum nespustil jeho kód ani neoveril slovenský výsledok. Projekt je koncipovaný aj na surové opakované talking-head zábery, čo nie je identické s hotovým viacúčastníkovým podcastom.

**[jameselle/clipper](https://github.com/jameselle/clipper)**, MIT. Dokumentuje Claude Code výber pasáží, FFmpeg/whisper.cpp, kontrolu výsledného zvuku a obrazu, zachovania slov a lokálnu stránku na pripomienky s konkrétnym časom, titulkami a snímkou. Zaujímavé je, že poznámka smeruje na presnú chybu vo videu a prepisuje sa editačný plán. Autorovo pravidlo zachovať aspoň 90 % slov nie je automaticky vhodné pre politický obsah: jediná odstránená negácia môže zmeniť význam. Ani jeho výstup nie je v tomto výskume otestovaný.

**[opensource-clipping](https://github.com/NaufalRizqullah/opensource-clipping)**, [MIT](https://github.com/NaufalRizqullah/opensource-clipping/blob/main/LICENSE). README popisuje Faster-Whisper, Gemini výber, face tracking, karaoke titulky, rozdelený obraz a prepínanie rečníka; zvuková diarizácia vyžaduje ďalší model/prístup. Je kandidátom na dávkový porovnávací test, nie dôkazom lepšieho Fiki výsledku. Už existujúci projektový audit v `docs/ZDROJE_A_REUSE.md` zaznamenal riziká náhodného/prvého výberu B-rollu; nové README ich samo nevyvracia.

**[AutoClip](https://github.com/artbyjazi/autoclip)** uvádza prepis, výber, sledovanie rečníka, review a export. Sám výslovne označuje rámovanie proti pevnému referenčnému súboru ako zatiaľ neoverené. Takéto rozlíšenie je užitočný vzor aj pre naše reportovanie: existujúci kód nie je prijatá tvorivá kvalita.

## Čo z toho vyplýva pre výrobu

Odporúčanie výskumu je jedna hlavná cesta: **zdroj → prepis a slovné kotvy → navrhnuté pasáže s kontextom → Adamov výber → dátový plán → Remotion → technická a obsahová kontrola → prijatý výsledok**. FFmpeg a yt-dlp sú podporné nástroje; WhisperX sa má porovnať s existujúcim prepisom; HyperFrames je voliteľná grafická dielňa. Doplniť sa má najmä opakovateľný kontrolný a opravný cyklus, nie počet nainštalovaných skillov.

Kapacita sa musí počítať z **prijatých videí**, času človeka vrátane opráv a počtu použiteľných pasáží na hodinu zdroja. Napríklad 40 prijatých videí za deň pri 5 minútach ľudskej práce na video znamená 200 minút denne; pri 15 minútach už 10 hodín. To je aritmetický scenár, nie predikcia výkonu. Aj render možno paralelizovať, ale jeho zrýchlenie nedokazuje zrýchlenie tvorivého rozhodovania.

Pred výberom novej závislosti potrebujeme rovnaké vstupy a pevné meranie: koľko výsledkov Adam prijal bez opravy, koľko minút zabralo posúdenie a opravy, prečo boli odmietnuté a koľko stál beh. Skúška má porovnať konkrétny prínos nového mechanizmu proti existujúcemu Remotion jadru. Z tohto výskumu nevznikol súhlas s migráciou ani s opätovným spustením výroby.

## Vedľajšie SaaS porovnanie

Pre úplnosť boli overené aj [OpusClip API a skills](https://github.com/opus-pro/opus-skills/blob/main/skills/opusclip/references/api-reference.md), [OpusClip slovenská podpora](https://opusclip.canny.io/changelog/20-languages-support) a [Klap API](https://docs.klap.app/). OpusClip explicitne uvádza slovenčinu, starší changelog ju označuje beta; Klap deklaruje 99+ jazykov bez tu doloženého slovenského benchmarku. Sú referenciou možných schopností, nie odporúčaním nahradiť náš systém službou.

[Klap API cenník](https://docs.klap.app/pricing) aktuálne uvádza 0,44 USD/vstup, 0,32 USD/vygenerovaný klip a 0,48 USD/export. Ilustračne 1 200 vygenerovaných a raz exportovaných klipov = 960 USD plus vstupy; odmietnuté klipy a opakované exporty menia sumu. Toto nie je rozpočet XVADUR ani cenová ponuka.
