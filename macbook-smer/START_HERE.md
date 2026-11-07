# Pokračovanie na MacBooku

Balík prenáša aktuálne zadanie, editorský postup, Remotion skills, zdrojový kód a textové rozbory. Pracovať máš v priečinku `macbook-smer/smer/`. Video pre prvý Smer klip ešte nie je súčasťou balíka.

## Otvorenie

V repozitári `xvadur/system` otvor vetvu `macbook-smer-2026-11-07` a priečinok `macbook-smer`. Ak repozitár na MacBooku ešte nemáš, naklonuj túto vetvu:

```sh
git clone --depth 1 --single-branch --branch macbook-smer-2026-11-07 https://github.com/xvadur/system.git smer-strih
cd smer-strih/macbook-smer
```

Tento priečinok otvor ako projekt v Codexe. Repozitár je verejný na Adamovo výslovné zadanie; klonovanie nevyžaduje prenos prihlasovacích údajov.

Na začiatok stačí Codexu napísať:

> Prečítaj AGENTS.md, context/SMER_BRIEF.md a context/HANDOFF.md. Pokračujeme v samostatnom projekte Smer. Použi pribalené skills a existujúce referencie. Najprv skontroluj miestne nástroje a smer/package.json; potom priprav edit z môjho dodaného zdroja a vybranej pasáže. Nezačínaj nový rozhovor o celkovom štýle.

## Miestne prostredie

Codex najprv overí `node`, `npm`, `python3`, `ffmpeg` a `ffprobe`. `yt-dlp` je potrebný pri získavaní verejného videa z podporovaného odkazu. Ich dostupnosť ani výkon na tomto MacBooku zatiaľ neboli overené. Prípadný ASR alebo generátor sa nastaví podľa konkrétneho vstupu a dostupných nástrojov.

Z koreňa balíka nainštaluje pripnuté závislosti:

```sh
cd smer
npm ci
npm run studio
```

Studio najprv otvorí technickú kartu `WorkspaceReady`. Tá potvrdzuje načítanie pripraveného projektu; nie je to Smer klip ani schválený štýl. Ďalšie príkazy na náhľad, kontrolu kódu a export číta Codex z `smer/package.json`. Inštalácia závislostí nevytvára klip a nemení Remotion verziu. `node_modules` sa obnovuje lokálne z lockfile.

## Prvý klip

1. Dodaj zdrojový súbor alebo konkrétny odkaz a urči pasáž, prípadne požiadaj AI o kandidátov. Zdrojové médiá ostávajú lokálne mimo Gitu.
2. Codex zmeria zdroj, pripraví alebo načíta slovný prepis a uloží presný výber. Rozmery a fps sa určia podľa skutočných médií; predvolená hodnota v ukážke nie je meranie.
3. V `smer/` zapíše treatment, pridá `src/Clip.tsx` a potrebné komponenty a zaregistruje skutočný klip v pripravenom `src/Root.tsx`. `src/index.ts` už existuje. Zachová jeden spoločný čas reči, titulkov a obrazových udalostí; parametre technickej karty nepreberie ako údaje zdroja.
4. Otvorí náhľad, skontroluje ho a vykoná potrebné opravy. Po zadaní výroby odovzdá celý výstup na Adamovo posúdenie.

Pri pokračovaní sa používa existujúca verzia a uložené podklady toho istého klipu. Pokyn k jednej scéne sa nemení na nové pravidlo pre všetky videá.

## Kde hľadať

| Potreba | Miesto |
| --- | --- |
| Aktívne zadanie a hranice | `AGENTS.md`, `context/SMER_BRIEF.md` |
| Čo je prenesené a čo ešte treba urobiť | `context/HANDOFF.md` |
| Celý tvorivý postup a pomocné skripty | `.agents/skills/remotion-reel/` |
| Remotion techniky | ostatné `.agents/skills/remotion-*/` |
| Pracovný kód nového klipu | `smer/src/` |
| Existujúci autorský runtime a príklady | `reference/xvadur_klipy/system/` |
| Rozbory konkrétnych editov | `reference/xvadur_klipy/research/` |

Historické odkazy na druhý Mac môžu pomenúvať nezabalené médiá. Použi [mapu prenesených ciest](context/PATH_MAP.md) a verejný odkaz z rozboru; existencia textového rozboru neznamená, že jeho MP4 alebo kontaktný hárok je v balíku.
