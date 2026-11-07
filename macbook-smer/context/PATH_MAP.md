# Cesty a hranice prenosu

Aktívny koreň je priečinok `macbook-smer`, kde leží jeho `AGENTS.md`. Lokálne používateľské meno ani cesta na MacBooku nemusia byť rovnaké ako na domácom Macu.

| Pôvod | Prenesené miesto |
| --- | --- |
| Domáci `xvadur_klipy` | `reference/xvadur_klipy/` — vybraný zdrojový a dokumentačný snapshot |
| Domáci `.codex/skills/remotion-reel` | `.agents/skills/remotion-reel/` — celý zdroj skillu bez Python prostredia |
| Projektové Remotion skilly | `.agents/skills/remotion-*/` |
| Nová lokálna Smer práca | `smer/` |

Vybrané Markdown odkazy v exportnej kópii sú upravené na relatívne cesty. Historické odkazy na videá, kontaktné hárky, staré chaty a chýbajúce projektové prílohy sú podklady na domácom Macu, nie sľub, že boli prenesené. Referenčné karty zachovávajú verejné URL. Potrebný obrazový materiál sa získa cielene pre konkrétny edit.

Zdrojové súbory kanonického autora ostali byte-identické; jeho pôvodná príprava pracoviska ešte očakáva Fiki dáta a niektoré domáce nastavenia. `reference/xvadur_klipy/system/cli/klipy.py` je úzky autorský snapshot, nie kompletná všeobecná CLI. Pre nový Smer klip používaj aktívny samostatný Remotion projekt. Prípadný prenos kanonického ingestu/evidencie je ďalšia implementácia.

V tomto balíku nie sú heslá, účty, cookies, produkčná databáza, existujúce publikačné joby, zdrojové videá, modelové váhy ani node_modules. Pôvodný autorský lockfile je zachovaný v reference; v smer/ má rovnaké dependency verzie, nové meno projektu a miestne scripts.

`EXPORT_SOURCES.json` zaznamenáva pôvod a pôvodné hashe. `EXPORT_MANIFEST.json` zaznamenáva presné bajty odovzdaného balíka po úprave prenosných ciest. Pôvodný skillový source-manifest dokladá pôvod donor materiálu, nie totožnosť adaptovaných Markdown súborov.

Verejná odovzdávka v `xvadur/system` vynecháva z výskumných dokumentov interné skupinové správy, odkazy na neverejné adresáre a párovanie súkromných identít s verejnými účtami. Verejné referencie a poznatky o editovaní zostávajú zachované.
