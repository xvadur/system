# Verzie a vydania

Verzia balíka a Git tag označujú spoločnú podobu zdrojov, tokenov aj komponentov. Spotrebiteľ si pripína konkrétny tag; prijatie novej verzie systému a nasadenie webu sú samostatné kroky.

## Voľba verzie

Počas vývoja `0.x` používame:

| Zmena | Verzia | Poznámka |
| --- | --- | --- |
| Oprava bez zmeny používania komponentu | `patch` | Napríklad fokus alebo oprava existujúceho stavu. |
| Nový komponent, variant alebo verejné API | `minor` | Spotrebiteľ dostane nové možnosti. |
| Nekompatibilná zmena počas `0.x` | `minor` | Povinná migračná poznámka; číslo `0.x` nesľubuje stabilné API. |
| Prechod na stabilné API alebo jeho neskoršia nekompatibilná zmena | `major` | Výslovné rozhodnutie a opísaná migrácia. |

Aj vizuálna zmena tokenu môže zasiahnuť viac komponentov. Pred verziou ju posúď podľa dopadu na spotrebiteľa; samotný počet upravených riadkov neurčuje druh vydania.

## Príprava vydania

```sh
npm run verify
npm run version:next -- minor "Pridaný komponent s migračnou poznámkou"
npm run verify
npm pack
```

`version:next` vyžaduje `patch`, `minor` alebo `major` a krátky konkrétny popis. Podporuje aj `--message "Popis"` a kontrolný `--dry-run`. Overí zhodu verzie v manifeste a lockfile, upraví iba ich koreňové verzie a pridá datovanú sekciu do changelog. Závislostiam verzie nemení.

Príkaz nevykonáva Git operácie, sieťové požiadavky ani npm publish. Zmenu si prezri v diff a podľa potreby doplň migračnú poznámku do vytvorenej sekcie. Tarball z `npm pack` môže spotrebiteľ overiť lokálne.

## GitHub vydanie

Po schválení konkrétneho vydania:

1. Ulož zmenu verzie, changelog a zdroje do commitu, ktorý prešiel CI.
2. Vytvor označený tag `vX.Y.Z` presne na tomto commite a odošli ho spolu s commitom.
3. Na GitHub release uveď relevantnú časť changelog, migračnú poznámku a výsledok overenia. Už zverejnený tag neposúvaj na iný commit.
4. V spotrebiteľovi nainštaluj nový tag podľa [integrácie](integration.md).

GitHub Actions pri push alebo pull requeste spustí kontroly a zostaví knižnicu aj katalóg. Uloží tarball a statický katalóg ako artefakty behu. Workflow nič nenasadzuje a nepublikuje na npm.

Súkromný repozitár vyžaduje prístup aj pri inštalácii v CI spotrebiteľa. Pri jeho nastavovaní použi existujúce spravované oprávnenie a tajomstvá úložiska; prístupové údaje nepatria do Git URL v manifestoch.
