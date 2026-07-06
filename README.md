# xvadur.system

Osobný **read-only control panel** — Astro web so slovenským UI. Sidebar s tabmi,
obsah v strede. Appka nič nezapisuje: zobrazuje markdown súbory z `data/`,
zapisuje sa úpravou súborov v repe (Codex, editor...).

## Taby

| Tab | Čo zobrazuje |
|---|---|
| **Prehľad** | Štatistiky za 7 dní (kalórie, spánok, cvičenie, meditácia), dnešný deň, projekty, posledné poznámky |
| **Denník** | Všetky denné záznamy — metriky ako chipy + voľný text dňa |
| **Poznámky** | Markdown poznámky s tagmi a klientským filtrovaním |
| **Jakub / Netopier** | Každý projekt ako živý dokument: status, ďalší krok, log práce |

## Dáta = markdown súbory

```
data/
├── dennik/
│   ├── _sablona.md            # skopíruj ako RRRR-MM-DD.md
│   └── 2026-07-06.md          # frontmatter: kalorie, spanok, cvicenie, meditacia + voľný text
├── poznamky/*.md              # frontmatter: nazov, datum, tagy
└── projekty/
    ├── jakub.md               # frontmatter: nazov, status, dalsi_krok + ## Log
    └── netopier.md
```

Súbory začínajúce `_` sa nezobrazujú (šablóny, koncepty).

Zápis = úprava súboru + commit:

```sh
git add data && git commit -m "denník 2026-07-06" && git push
```

## Spustenie

```sh
npm install
npm run dev        # http://localhost:4321 — číta data/ naživo
```

## Deploy (Cloudflare / xvadur.com)

Appka je čisto statická — `npm run build` vygeneruje `dist/`, ktorý sa dá
nasadiť na Cloudflare Pages bez adaptéra a bez servera. Panel vždy zobrazuje
stav z posledného buildu/commitu; po pushi nových dát stačí rebuild
(Cloudflare Pages to pri napojení na repo robí automaticky).
