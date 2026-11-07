# Celé autorské scény cez remotion-reel

Implementované 6. novembra 2026 podľa Adamovho zadania: agent používa celý remotion-reel a píše kompletnú kompozíciu v Remotione. HyperFrames runtime sa nepoužíva; užitočné režijné postupy sú prenesené do [whole-scene-authoring.md](../../../.agents/skills/remotion-reel/references/whole-scene-authoring.md).

## Čo táto cesta vlastní

`autor` vytvorí nové pracovisko konkrétneho klipu. Pripne aktuálny SourceRecord, Transcript, Selection a Timeline, ich hashe, celý zdroj skillu vrátane referencií/scripts/components a brand. Nový TSX dostane skutočný `RenderDocument` a vlastní celý obraz, rozloženie, kameru, masky, typografiu, titulkové režimy aj podporné audio. Produkčný obal vloží pôvodný vybraný hlas presne raz. Autorská cesta používa samostatný Remotion 4.0.529 a Zod 3.25.76 s vlastným presným lockfile; nezávisí od súbežných zmien balíkov hlavného projektu.

Starý JSON planner a register scén ostávajú pre svoje existujúce plány. Nový autor cez ne nemusí vyjadriť každý prvok ani registrovať novú scénu. Autorské moduly majú samostatný manifest, presné hashe a revízie; historický `Root.tsx`, prijaté videá a kanonická reč sa nemenia.

## Príprava a obnova

Riadiaci Codex pred prvou prípravou načíta [výrobný postup](CODEX_VYROBNY_POSTUP.md), skill, brand a `cyklus --akcia stav`. Izolovaný autorský proces potom obnovuje svoje pripnuté pracovisko cez `autor --akcia stav`; nemusí znovu spúšťať epizódový cyklus mimo svojho rozsahu zápisu.

```sh
python3 system/cli/klipy.py autor --epizoda ID --klip ID --akcia priprav --nazov nova-kompozicia
```

Výsledok obsahuje absolútny `workspace`; v ďalších príkazoch nižšie ho predstavuje `WORKSPACE`. Pracovisko obsahuje `inputs.json`, `authoring.json`, `AGENTS.md`, `AUTHORING.md`, `.agents/skills/remotion-reel/`, `BRAND.md` a `src/`.

Ak sa mení obrazová Timeline, pack, materiály alebo koncovka, možno pripraviť novú odvodenú Timeline cez `--timeline /absolutna/derived-timeline.json`. Zachová pôvodný výber, hlasovú stopu, slovné časy, fps a trvanie reči; úprava obrazu či koncovky sa pripne spolu s parent Timeline hashom. Pôvodný aktuálny artefakt ostáva nemenný. Pracovisko naďalej používa existujúcu schému Timeline, nie druhý nezávislý strihový kontrakt.

## Autorstvo

Aktívny Codex môže vykonať celý postup priamo. Pre samostatný nástrojový proces:

```sh
python3 system/cli/klipy.py autor --epizoda ID --klip ID --akcia spusti --autor-dir WORKSPACE
```

Toto je nástrojový `codex exec` s vlastným pracoviskom a čítaním skillu, nie pôvodný izolovaný JSON-only model. Výsledok procesu má log nástrojov a deklarovaný/skutočne ohlásený model; keď CLI model neohlási, záznam ponechá `unreported`.

Autor najprv zapíše `TREATMENT.md`: každá veta, jej word/span kotvy, obrazová akcia a vrstvy, konkrétny materiál, zvuk, odhalenie/dopad/odchod. Potom vytvorí `src/Clip.tsx` a ľubovoľné lokálne moduly. Obraz môže byť celý vlastný React/SVG/CSS/canvas/Remotion kód.

```tsx
import React from 'react';
import {useCurrentFrame} from 'remotion';
import {SourcePicture, ExactCaptions, wordFrame,
  type AuthoredSceneProps} from '@xvadur/authoring';

export default function Clip({document}: AuthoredSceneProps) {
  const frame = useCurrentFrame();
  // Vlastná kompozícia, slovné fázy a pohyb používajú tento skutočný clock.
  return <><SourcePicture document={document}/><ExactCaptions document={document}/></>;
}
```

Príklad iba demonštruje vstup. Samotný A-roll a titulky nespĺňajú tvorivé zadanie. Voliteľné helpers sú `SourcePicture` (vždy muted), `ExactCaptions` (presný existujúci komponent), `Media` (vrátane transparentného videa), `mediaAsset`, `wordFrame` a `TimelineSound`. Autor môže celé rozloženie navrhnúť sám. `TimelineSound` sa pridá len vedome; obal automaticky nepridáva staré grafiky ani staré SFX.

Materiály majú skutočné bajty a AssetRecord. Nový materiál znamená odvodenú Timeline a nové pripnuté pracovisko; detailný postup je v jeho `AUTHORING.md`. Pôvodné vstupy sa neupravujú na mieste.

## Manifest, render a oprava

```sh
python3 system/cli/klipy.py autor --epizoda ID --klip ID --akcia manifest --autor-dir WORKSPACE --entry src/Clip.tsx --files src/Clip.tsx,src/Scene.tsx --revizia 1
python3 system/cli/klipy.py autor --epizoda ID --klip ID --akcia over --autor-dir WORKSPACE --manifest WORKSPACE/manifest.json
python3 system/cli/klipy.py autor --epizoda ID --klip ID --akcia render --autor-dir WORKSPACE --manifest WORKSPACE/manifest.json --kvalita draft
python3 system/cli/klipy.py autor --epizoda ID --klip ID --akcia kontrola --autor-dir WORKSPACE
```

Do `--files` patria všetky lokálne importované implementačné súbory. Manifest zároveň pripne aktuálny `TREATMENT.md` do nemennej revízie `treatment.rNNNN.md`; vlastnú cestu možno uviesť cez `--treatment`. Pri oprave vznikne manifest s vyššou revíziou a odkazom na parent. Rozsah `--frames OD,DO` používa polootvorený interval; celý klip sa kontroluje z celého renderu. `--kvalita master` zachová plné rozmery Timeline, draft používa polovicu rozmerov. Každý výsledok má vlastné kódové, mediálne a výstupné hashe.

Po každej obsahovej zmene znovu over dotknuté scény a ich spoje. Technická kontrola nie je tvorivé prijatie ani posluch. Zapisuj skutočný rozsah vzorkovaného obrazu, pohybu a zvuku; Adamovi odovzdaj prehrateľný celý klip. Táto cesta sama nepublikuje ani nezavádza kapacitný prísľub.

## Izolácia pri súbežnej práci

Stabilné závislosti a vlastný lockfile sú v [`system/runtime/authoring-4.0.529`](../system/runtime/authoring-4.0.529/README.md). Pri chýbajúcej cache ich obnoví `python3 system/cli/provision_author_runtime.py`: nainštaluje uzamknuté balíky do dočasného priečinka, overí ich a atomicky sprístupní runtime. Existujúci runtime iba overí; nepreinštaluje bežiace balíky ani spoločný projekt.

Python launcher rozpozná príkaz `autor` pred načítaním hlavnej TypeScript CLI. Overí deklarované, uzamknuté aj nainštalované verzie v `system/.cache/authored-runtime/4.0.529`, vytvorí hashovaný nemenný snapshot autorského kódu a spustí úzku `author.ts`. Originálny projekt zostáva dátovým koreňom cez `XVADUR_PROJECT_ROOT`; médiá sa nekopírujú do snapshotu kódu. Receipt obsahuje identitu snapshotu, package, lockfile aj presné závislosti. Chýbajúca alebo zmenená závislosť spôsobí zrozumiteľnú chybu, nie tichý prechod na spoločné balíky.

Nový autorský modul používa pre lokálne snímky Remotion `/proxy` pamäťové vytvorenie Blob z rovnakých bajtov. Pri overenom 4K zdroji pôvodný sieťový `response.blob()` končil EPIPE, zatiaľ čo `arrayBuffer()` a následný Blob dekódovali ten istý snímok. Oprava nemení obraz, čas ani node_modules a nezasahuje iné URL alebo historické kompozície. Príčina konkrétneho interného limitu Chrome nebola zmeraná.

Pripnutý Remotion 4.0.529 má doložené AAC encoder oneskorenie 2048 vzoriek pri ceste `libfdk_aac → ADTS → MP4`. Nový autor ho po renderi kompenzuje presným MP4 edit listom, pred výpočtom výsledného hashu a receipt. Overí verziu, encoder, sample rate, pôvodné časovanie a neprítomnosť už aplikovanej kompenzácie. Zhodné packet hashe dokazujú, že obraz ani zvuk neboli znova komprimované; obrazové časy sa nemenia. Receipt uchováva detail `audioPriming`. Ďalšie ručné posúvanie zvuku na takto kompenzovanom výstupe by bolo chybou.

## Dôkazy a hranice

Samostatné unit testy overujú nemennosť vstupov, celý snapshot skillu, voľnú obrazovú Timeline pri zamknutej reči, manifest/importy/revízie a obnovu. Skutočný renderovací integračný test overuje vlastný vrstvený TSX/SVG, presný Fiki caption komponent, zmenu na slovnej kotve, rovnaký frame pri celom/rozsahovom renderi a pôvodný hlas bez duplikácie. Živý Codex smoke prečítal skill a referenciu a nástrojom vytvoril súbor.

Timeout a prekročenie limitu výstupu nástrojového autora uchovávajú redigovaný čiastočný audit aj neúspešný stav; nevytvoria úspešný výsledok. Reálne krátke subprocess testy preverujú obe prerušenia. Samostatný AAC integračný test reprodukuje 2048-vzorkový posun, overí jeho odstránenie, nezmenené kódované dáta a bezpečné opakované volanie.

Ukážka a jej finálne dôkazy sa zapisujú do pracoviska klipu. Tento dokument sám nevyhlasuje dokončenie celých etáp C0–C6, autonómnu mesačnú kapacitu, prijatie videa ani publikovanie.
