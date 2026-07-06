---
nazov: Vitaj v systéme
datum: 2026-07-06
tagy: systém
---

Toto je read-only control panel — appka len **zobrazuje** to, čo je v `data/`.
Zapisuješ úpravou súborov (Codex, editor, čokoľvek) a commitom do repa.

## Ako zapisovať

- **Denník** — nový deň = nový súbor `data/dennik/RRRR-MM-DD.md` (skopíruj `_sablona.md`).
  Vo frontmatteri metriky (kalórie, spánok, cvičenie, meditácia), pod ním voľný text.
- **Poznámky** — nový súbor `data/poznamky/nieco.md` s frontmatterom `nazov`, `datum`, `tagy`.
- **Projekty** — `data/projekty/jakub.md` a `netopier.md` sú živé dokumenty:
  vo frontmatteri `status` a `dalsi_krok`, do sekcie `## Log` píš, na čom si robil.

Súbory začínajúce podčiarkovníkom (`_sablona.md`) sa v paneli nezobrazujú.
