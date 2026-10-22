# XVADUR Stack / Brand book

Vlastný rozpracovaný dizajnový systém XVADUR a jeho spoločný Astro brand book. Zdrojový repozitár: [xvadur/system](https://github.com/xvadur/system).

## Spustenie

Node.js 24 a npm:

```sh
npm ci
npm run dev
```

Otvoriť **http://127.0.0.1:4390/**. Celý brand book beží v jednej Astro aplikácii; nepotrebuje Python, ďalšie servery, súkromný priečinok fotografií ani internetové fonty. `npm run dev:stack` je alias toho istého príkazu.

| Sekcia | Adresa | Obsah |
| --- | --- | --- |
| Design language | `/` | Rozpracovaný vizuálny smer, materiál, farby a stav rozhodnutí |
| Komponenty a tokeny | `/komponenty/` | 14 živých komponentov, varianty, stavy a použitie |
| Fonty | `/fonty/` | 48 dvojíc zo štyroch kôl, deväť prenesených favoritov, skúšobný text |
| Fotky | `/obrazky/` | 54 optimalizovaných náhľadov, filtre, označovanie a detail |

## Výbery a médiá

Fontoví favoriti pozorovaní pri migrácii sú v `catalog/data/font-favorites.json`. Uložený fotovýber sa preniesol z pôvodnej galérie; pri migrácii bol prázdny. Nové označenia sa ukladajú do localStorage aktuálneho prehliadača. **Export JSON / Import výberu** prenáša výber medzi prehliadačmi a zariadeniami; podporuje aj pôvodné JSON exporty galérie a fontových kandidátov. Zmena výberu sama nevytvára Git commit ani cloudovú synchronizáciu.

Obrázky v `public/brand/photos/` sú optimalizované náhľady. Originály zostávajú na Macu v `xvadur_fotky` a nie sú súčasťou repozitára. Fonty sú lokálne WOFF2 so zdrojovými licenciami v `public/brand/licenses/`. Fotografie sa smú použiť iba v rozsahu práv ich vlastníka; samotná dostupnosť v tomto repozitári neudeľuje tretej strane licenciu na ich ďalšie použitie.

Staré porovnania a lokálne referencie zostávajú zachované v pracovnom priečinku, ale sú ignorované Gitom. `scripts/import-brand-assets.py` dokumentuje jednorazový import z týchto lokálnych podkladov; pri inštalácii, vývoji ani builde sa nespúšťa. Všetky potrebné výsledné dáta a súbory sú commitované.

## Stav systému

XVADUR Stack má umožniť používať rôzne vizuálne štýly v rôznych projektoch. Teraz dokončujeme smer XVADUR: neumorfizmus, výrazný technický dojem, oranžový akcent a výber typografie. Referenciou je Yanis Schweizer / Strade a jeho [Design System Interviewer](https://www.strade.tech/free/design-system-interviewer). Odpovede sú v `design/interview/INTERVIEW.md`.

Existencia tokenov, katalógu ani úspešný build neznamená finálne prijatie vzhľadu. Nasleduje dokončenie vizuálnych rozhodnutí a overenie na jednej obrazovke. Potom vznikne Lab ako prvé reálne použitie systému; následne v Labe hero a ďalšie sekcie webov. Rift bol preskúmaný ako možný zdroj hotovej implementácie a zatiaľ nie je nainštalovaný.

## Build a overenie

```sh
npm run verify
npm run build
npm run preview
```

Statický brand book sa vytvorí v `catalog-dist/`. Môže sa obsluhovať na bežnom statickom hostingu z koreňa domény. GitHub repozitár a nasadenie webu sú samostatné veci; tento repozitár zatiaľ nemá nastavený verejný hosting.

CI pri push do `main` a pri pull requeste overí knižnicu, Astro stránky, testy a použitie balíka v samostatnom spotrebiteľovi. Katalóg a tarball uloží ako artefakty behu.

## Použitie komponentov

```tsx
import '@xvadur/ui/tokens.css';
import '@xvadur/ui/styles.css';
import { Button } from '@xvadur/ui';

export function Example() {
  return <Button>Pokračovať</Button>;
}
```

Aktuálna pracovná verzia je `0.1.0`; prvý publikovaný release tag ešte nie je vytvorený. Po pripravenom vydaní si spotrebiteľ pripne jeho konkrétny tag. Fonty Geist a Instrument Serif zo základnej ukážky sú voliteľný import `@xvadur/ui/fonts.css`; tým sa neurčuje finálna typografia systému.

- [Vývoj komponentov](docs/contributing.md)
- [Integrácia](docs/integration.md)
- [Vydávanie](docs/releases.md)
