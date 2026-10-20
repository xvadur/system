# XVADUR UI

Verziovaný dizajnový systém pre weby a nástroje XVADUR. Repozitár obsahuje zdrojové komponenty balíka `@xvadur/ui`, tokeny, register a živý katalóg. Web si vyberie konkrétnu verziu; ďalší komponent pribudne sem a môže sa použiť aj v inom projekte.

Prvé vydanie je pracovný základ. Vizuálny štýl vychádza z doterajšej ukážky, ďalšie rozhodnutia sa overujú na skutočných obrazovkách. Nastavenie `flat` je predvolené; `soft` a `neumorphic` sú experimentálne alternatívy na porovnanie v katalógu.

## Spustenie katalógu

Použi Node.js 24 a npm. Po klonovaní repozitára:

```sh
npm ci
npm run dev
```

Produkčný náhľad:

```sh
npm run build:catalog
python3 -m http.server 4390 --directory catalog-dist --bind 127.0.0.1
```

Katalóg bude na [localhost:4390](http://127.0.0.1:4390). Má ukazovať aj stavové a interaktívne správanie komponentov, aby sa zmeny dali posúdiť pred použitím na webe.

## Použitie na webe

Po vytvorení release tagu nainštaluj presnú verziu zo súkromného GitHub repozitára. Prístup používa tvoje existujúce SSH oprávnenie:

```sh
npm install @xvadur/ui@git+ssh://git@github.com/xvadur/design-system.git#v0.1.0
```

Git inštalácia spustí `prepare`, ktorý zostaví knižnicu zo zdrojov. Vyžaduje Node.js a npm a počas prípravy potrebuje aj vývojové závislosti balíka. Nie je potrebný npm registry ani publikovanie balíka na npm.

```tsx
import '@xvadur/ui/tokens.css';
import '@xvadur/ui/styles.css';
import { Button } from '@xvadur/ui';

export function Example() {
  return <Button>Pokračovať</Button>;
}
```

Voliteľný import `@xvadur/ui/fonts.css` pridá pribalené fonty Geist a Instrument Serif. Pri vlastných fontoch ho vynechaj. Podrobnosti k Astro, témam a aktualizácii verzie sú v [integrácii](docs/integration.md).

## Pridanie komponentu a vydanie

Komponent patrí do zdrojov, verejného exportu, registra a katalógu. Potrebuje príklad použitia, zdokumentované varianty a kontrolu relevantného správania. Postup je v [príspevkoch](docs/contributing.md).

```sh
npm run verify
npm run version:next -- patch "Opravený fokus tlačidla"
```

Druhý príkaz upraví verziu v manifeste, lockfile a changelog. Nevytvára commit, tag ani push. Pravidlá vydávania a prepojenie vydania s webom sú v [releases](docs/releases.md).

CI overuje zdroje, zostaví knižnicu aj katalóg a uloží tarball s katalógom ako artefakty. Nasadenie webu a publikovanie balíka majú samostatný krok.
