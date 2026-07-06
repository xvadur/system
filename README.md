# xvadur.system

Osobný systém na sledovanie života a práce — Astro web appka so slovenským UI.

## Moduly

| Stránka | Čo robí |
|---|---|
| **Prehľad** (`/`) | Štatistiky za posledných 7 dní (kalórie, spánok, cvičenie, meditácia), stav projektov, posledné poznámky |
| **Denník** (`/dennik`) | Denný záznam: kalórie, spánok, cvičenie, meditácia, poznámka k dňu + história |
| **Poznámky** (`/poznamky`) | Markdown poznámky s tagmi a fulltextovým vyhľadávaním |
| **Projekty** (`/projekty`) | Jakub a Netopier — ďalší krok, work log odpracovaného času |

## Dáta

Všetko sa ukladá ako obyčajné súbory v `data/` — žiadna databáza, plná kontrola, história cez git:

```
data/
├── dennik/2026-07-06.json     # jeden JSON na deň
├── poznamky/*.md              # Markdown s frontmatterom (nazov, datum, tagy)
├── projekty/*.md              # Markdown s frontmatterom (nazov, status, dalsi_krok)
└── worklog.json               # záznamy o práci na projektoch
```

Zapísané dáta commitni, keď ich chceš mať zálohované:

```sh
git add data && git commit -m "denník" && git push
```

## Spustenie

```sh
npm install
npm run dev        # http://localhost:4321
```

Produkčný build (Node server):

```sh
npm run build
npm start
```

## Deploy na Cloudflare (xvadur.com)

Appka beží v server móde cez `@astrojs/node`. Pre Cloudflare Pages/Workers vymeň adaptér:

```sh
npm install @astrojs/cloudflare
```

a v `astro.config.mjs` nahraď `node(...)` za `cloudflare()`. Pozor: na Cloudflare
nie je zapisovateľný filesystem — formuláre tam fungovať nebudú, kým sa úložisko
neprepne na KV/D1/R2 alebo kým sa zápis nerieši cez git (napr. GitHub API).
Odporúčaný postup: lokálne zapisuješ, commituješ, a Cloudflare slúži ako read-only
dashboard z posledného commitu.
