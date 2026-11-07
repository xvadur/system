# Výrobný postup v Codexe

Tento vstup používaj pri pokračovaní výroby alebo pripomienkach k videu. Rozsah a ľudské rozhodnutia určuje [plán](../PLAN_IMPLEMENTACIE.md). Stav práce čítaj z artefaktov; história chatu pomáha vysvetliť zámer.

**Celé autorské scény od 6. novembra 2026:** pre plný `remotion-reel` používaj [autorskú cestu `autor`](AUTORSKE_SCENY.md). Agent dostane celý skill, môže napísať vlastné TSX/moduly a renderuje cez existujúci produkčný renderer s pripnutou rečou. Riadiaci Codex najprv načíta cyklus; delegovaný autor obnovuje svoje izolované pracovisko cez `autor --akcia stav`. Nižšie opísaný `navrhni --plan` ostáva dostupný pre štruktúrované plány, neobmedzuje možnosti novej kompozície.

**Tvorivý postup od 5. novembra 2026:** používaj [nakonfigurovaný remotion-reel](../../../.agents/skills/remotion-reel/SKILL.md) a [existujúci štýl a referencie](../brand/BRAND.md). Zdrojový skill je prispôsobený Fikiho pop titulkom, samostatnému rozhodovaniu AI a hľadaniu/generovaniu materiálov podľa významu. Autorský kanonický plán môžeš uložiť cez `navrhni --epizoda ID --klip ID --plan /absolutna/cesta/plan.json [--brief /absolutna/cesta/brief.json]`; nejde o automatické načítanie skillu izolovaným modelovým plannerom. Pri oprave zachovaj existujúce zámky a použi nižšie uvedený opravný tok.

## Vstup a obnova

1. Urči epizódu a Adamom vybranú dávku. Existujúca `Selection` je autorita reči. Pri chýbajúcom výbere priprav čitateľných kandidátov podľa [používania](POUZIVANIE.md#epizóda-a-adamov-výber); výroba počká na Adamov výber.
2. Spusti `python3 system/cli/klipy.py cyklus --epizoda ID --akcia stav`. Pri prvom použití možno určiť `--klipy ID,ID`; ďalšie vstupy zachovávajú uloženú dávku. Prečítaj `record.clips` a iba podklady relevantné k uvedenému ďalšiemu kroku.
3. `--akcia priprav` uloží potreby a aktuálny prehľad bez výroby videa. `--akcia pokracuj` najprv obnoví rozpracované transakcie opráv a vykoná pripravené lokálne kroky. Výsledok zapisuje do `artefakty/production-cycle/` a `cyklus.md` epizódy. Každý klip má vlastný stav; chyba suseda ho nezastaví.

Cyklus sám nevytvára Selection ani nový tvorivý plán. Nevybavenú potrebu vracia Codexu na konkrétnu nástrojovú prácu. Príkazy, súbory s voľbami a náhľady obsluhuje Codex; Adam dostáva kandidátov, prehrateľné výsledky a skutočné otvorené otázky.

| Stav | Práca Codexu | Kritérium ďalšieho kroku |
| --- | --- | --- |
| `planning_required` | Použi aktuálnu analýzu a knižnicu; vytvor plán operáciou `navrhni`. Čítaj [rozhodovanie o edite](ROZHODOVANIE_O_EDITE.md). | Každý moment a všetky osi majú doložené rozhodnutie; reč zodpovedá vybranej Selection. |
| `preparation_required` | Vyrieš uvedené osi, klientské pravidlá alebo konkrétne úlohy. | P3 posúdenie je pripravené a klientské pravidlá povoľujú aktuálnu dávku. |
| `materials_required` | Prezri lokálne alternatívy; dohľadaj, vytvor a over potrebné médiá cez [nástrojové úlohy](NASTROJOVE_ULOHY.md). | Povinné materiály majú presné vyriešené záznamy a dôkazy; zmenu zámeru ulož ako novú revíziu. |
| `ready_for_production`, `check_required` | Pokračuj cyklom. | Existuje celý aktuálny render a úspešná technická kontrola jeho bajtov. |
| `critique_required` | Vykonaj samostatný kritický priechod podľa [kontroly a opráv](KONTROLA_A_OPRAVY.md). | Každý nález má cieľ, dôkaz, zmenu a spôsob overenia. |
| `repair_required`, `verification_required` | Oprav konkrétne nálezy, vyrob novú revíziu a over zmenu na nových bajtoch s okolím. | Požadované nálezy sú overené alebo výslovne zdôvodnene odmietnuté. |
| `review_required` | Odovzdaj Adamovi presný návrh s hranicami AV kontroly. Pre finálne prijatie priprav `--kvalita master`. | Adam posúdil celý aktuálny master; jeho prijatie patrí iba týmto bajtom. |
| `needs_input`, `blocked` | Rozlíš chýbajúce ľudské rozhodnutie od odstrániteľnej technickej chyby. | Konkrétny problém je vyriešený alebo je Adamovi položená konkrétna otázka s podkladmi. |

## Materiály po prerušení

Každá vrátená úloha obsahuje ID, parent, stav a ďalší krok. Pri `output_received` načítaj uložený súbor a dokonči overenie. Pri `in_progress`/neistom výsledku najprv dohľadaj existujúci výstup. Úspešný receipt sa používa opakovane. Skutočné generovanie vykonáva dostupný nástroj Codexu, nie textový headless planner.

`cyklus --volby JSON` prijíma mapu `clipId →` voľby resolvera. Pri lokálnom médiu dodaj skutočné `contentReviews`, pri knižničnej alternatíve `localDecisions` s hashmi a trimom. Pri imagegene dodaj a over receipt podľa nástrojového návodu. Cyklus automaticky nespúšťa nové hľadanie či generovanie za chýbajúci výsledok. Uložené AssetRecord a celé nezmenené rendery sa použijú znovu.

## Pripomienka z pracoviska

Pri úlohe typu `codex` postupuj cez `pracovisko` v CLI. Dostupné argumenty poskytuje `help`.

1. `prevziat --job ID --vlastnik TEXT`: prevezmi konkrétnu úlohu. Uložený lease súbor je interný pracovný doklad; používateľovi vráť názov klipu a problém. Počas práce obnovuj lease cez `heartbeat` (predvolená platnosť 10 minút).
2. Z pôvodných komentárov vytvor `CommentInterpretation[]` podľa `system/pipeline/workplace.ts`. Každý obsahuje nezmenené `commentId`, `bodyHash` a konkrétne nálezy s jedinečnými ID. Nejasnú reč/uzamknuté rozhodnutie objasni s Adamom. `pripomienky --lease JSON --data JSON` založí presné FeedbackRecord; komentár bez žiadosti o úpravu zostáva iba komentárom.
3. Opravy odovzdaj spolu cez `uprav --zmeny JSON`. Zámer, plán, feedback a rozdielový doklad tvoria obnoviteľnú transakciu. Pri konflikte parent hashov zachovaj obe revízie a vyjasni aktuálny cieľ.
4. Pokračuj výrobou a overením podľa tabuľky. `dokonci --lease JSON` uzavrie komentáre až po overení všetkých odvodených nálezov na aktuálnom kandidátovi. Nová verzia zostane v tom istom klipe. Retry nevytvorí druhú verziu.

Pracovisko prijíma finálny master cez kanonické prijatie s potvrdením pozretia a posluchu. Draft je určený na pripomienky. Live preview sa ponúka iba pre presný podporovaný bundle; ostatné verzie používajú presný MP4. Export používaj až po overenom prijatí. Publikovanie nie je súčasťou cyklu.

## Poučenie a výsledky

Po významnej overenej oprave vytvor `poucenie --klip ID --data JSON` podľa `LearningInputSchema` v `system/schemas/learning.ts`: nález, konkrétny poznatok, scope `use/asset/recipe/client`, tagy, `observed/hypothesis` a skutočné dôkazy. Asset/recipe musí byť v presne posúdenom pláne. Ďalší LibraryContext vyhľadá relevantné poučenie. Má `context_only`: lokálne zamietnutie nie je nový klientský zákaz; pravidlo vyžaduje Adamovo samostatné rozhodnutie.

`pracovisko --akcia vysledky --verzia ID` zaznamená existujúce publikácie a dátované merania spojené s presným hashom verzie a účtom. Neznáma hodnota zostáva `null`. Záznam nepublikuje, neupravuje staré príspevky a netvrdí príčinu výkonu.

Technické dôkazy a hranice tohto postupu: [overenie P6](OVERENIE_P6_2026-10-26.md). Pri skúške reálnej prenosnosti a dennej kapacity pokračuj kritériami P7 v hlavnom pláne.
