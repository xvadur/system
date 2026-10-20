# Integrácia do webu

Web používa označenú verziu `@xvadur/ui`. Zdrojové úpravy spoločného komponentu patria do tohto repozitára; web obsahuje vlastné kompozície a obsah.

## Inštalácia a štýly

Nainštaluj Git tag podľa README a ulož zmenu manifestu aj lockfile spotrebiteľa. Tag sa pri bežnej práci nemení; nové vydanie má nový tag.

V globálnom layoute načítaj štýly v tomto poradí:

```tsx
import '@xvadur/ui/tokens.css';
import '@xvadur/ui/styles.css';
// Voliteľné: pribalené fonty a ich licencie sú súčasťou balíka.
import '@xvadur/ui/fonts.css';
```

Tokeny poskytujú sémantické premenné pre povrch, text, akcent, okraje, rozostupy a pohyb. Kompozície webu môžu používať tie isté premenné. Spoločný token uprav v knižnici a over jeho existujúce použitia v katalógu.

## React a Astro

Komponenty sú React komponenty. Astro projekt potrebuje svoju integráciu React; balík ju do spotrebiteľa nepridáva. V `.astro` súbore sa verejné exporty používajú priamo:

```astro
---
import { Button, ThemeControl } from '@xvadur/ui';
import '@xvadur/ui/tokens.css';
import '@xvadur/ui/styles.css';
---

<Button>Pokračovať</Button>
<ThemeControl storageKey="xvadur-theme" client:load />
```

Statický komponent sa môže vykresliť na serveri. Komponent so stavom alebo obsluhou udalostí potrebuje v Astro hydratáciu, napríklad `client:load`. Funkčné props odovzdávaj v React kompozícii, ktorá sa hydratuje ako celok.

## Téma a materiál

`data-theme` na elemente `<html>` určuje tému. Hodnoty `light` a `dark` sú výslovná voľba; bez atribútu sa použije systémové nastavenie. `ThemeControl` zapisuje výslednú tému do tohto atribútu a pri voľbe „Systém“ reaguje aj na zmenu systému. Ukladanie voľby do localStorage zapína prop `storageKey`; bez neho voľba platí v aktuálnom zobrazení. Pre dokument používaj jeden vlastník tohto nastavenia, aby sa nezávislé ovládače neprepisovali.

`data-material="flat"` je predvolené spracovanie. Hodnoty `soft` a `neumorphic` poskytujú experimentálne mäkké spracovanie vybraných povrchov a ovládacích prvkov. Atribút môže byť na `<html>` alebo na konkrétnom príklade. Varianty môžeš porovnať v katalógu; existencia variantu nie je rozhodnutím použiť ho na celom XVADUR webe.

Pohyb rešpektuje `prefers-reduced-motion`. Kompozícia na webe potrebuje rovnaké pravidlo aj pre vlastné animácie.

## Aktualizácia

1. Prečítaj rozdiel verzií v changelog a prípadnú migračnú poznámku.
2. Nainštaluj nový konkrétny tag a skontroluj zmenu lockfile.
3. Spusti kontroly spotrebiteľa. Otvor dotknuté stránky na desktope a mobile; over fokus, klávesnicu, témy a stavy, ktoré používaš.
4. Zmenu aplikácie odovzdaj na posúdenie s uvedením pôvodnej a novej verzie. Nasadenie webu zostáva samostatným rozhodnutím.

Pred vydaním možno lokálne skúsiť zostavený tarball z `npm pack`. Taká inštalácia slúži na kontrolu; verziovaný web potom pripni na schválený Git tag.
