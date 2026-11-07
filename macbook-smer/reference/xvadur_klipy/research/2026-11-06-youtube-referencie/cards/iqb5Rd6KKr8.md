# HyperFrames: konkrétny podklad, prenos interakcie, statická kontrola a doladenie

[Full Tutorial: Make Professional Launch Videos for Free with Hyperframes | Bin Liu & Jake Moran](https://www.youtube.com/watch?v=iqb5Rd6KKr8) — Peter Yang; hostia Bin Liu a Jake Moran

Primárne metriky: 39749 views, 809 likes k 2026-11-06T00:28:18.710400+00:00. Bez baseline autora.

Celý automatický prepis prečítaný; otvorených 15 hárkov. Vzorkovaný obraz, bez súvislého prehratia a počúvania. Päťkrokový návod je prevažne prezentácia a hotové príklady, nie neprerušená nová výroba.

Rozhovor otvára cenou ručnej produkcie a ukážkou videa vytvoreného z webu. Predvedené Studio a otvorený skill vystrieda Jakeov postup s podkladmi, príbehom a komponentmi; jednotlivé kroky vysvetľuje na slidoch a hotových ukážkach. V Studio menia prvok konkrétnej kompozície a vysvetľujú prenos do kódu; neskôr rozlišujú priestorový dizajn od videa v čase.

## 00:00–02:15

Úvod strieda detail tvárí. Neskôr tri tváre v úzkom stĺpci vľavo sprevádzajú veľké UI s kódom, preview a viacvrstvovou timeline.

Reč/funkcia: Úvodná ukážka už hotovej HTML kompozície. Výsledok dáva technickému rozprávaniu konkrétny objekt.

Prenos: Pri návrhu výraznej scény ukázať jej reálnu kompozíciu a mediálne vrstvy. Ukážka frameworku sama nie je dôkaz autonómneho clippingu.

Dôkaz: [hárok](../../../research/2026-11-06-youtube-referencie/evidence/iqb5Rd6KKr8/overview-15s/page-001.jpg).

## 03:50–07:18

Na GitHube je otvorený Website to HyperFrames skill; v Studio ukazujú Spotify obaly, portréty interpretov, rebríčkové karty a záverečné logo. Potom sa vracajú ku krokom zachytenia webu a storyboardu.

Reč/funkcia: Zber reálnych zdrojov a skladanie scén. Zdrojový materiál pred vyrobenou grafikou.

Prenos: Ak reč odkazuje na konkrétny web či objekt, použiť skutočný podklad; zachovať jeho pôvod. Pre Fikiho sa neprenáša výber Spotify ani produktová štruktúra.

Dôkaz: [hárok](../../../research/2026-11-06-youtube-referencie/evidence/iqb5Rd6KKr8/overview-15s/page-001.jpg), [hárok](../../../research/2026-11-06-youtube-referencie/evidence/iqb5Rd6KKr8/overview-15s/page-002.jpg).

## 10:03–12:42

Prezentácia ukazuje Gather Resources, potom prompt Create STORYBOARD.md a tabuľku scén s funkciou, obrazom a dĺžkou. Nevidno v tomto úseku nový modelový beh vytvárajúci celé video.

Reč/funkcia: Podklady a estetický rámec, následne dejové poradie. Oddelenie príbehu od dizajnových rozhodnutí.

Prenos: Použiť existujúci BRAND.md a kanonický CreativeBrief/EditPlan. Do beatu zapísať akciu a použitý podklad; nevytvárať konkurenčnú časovú os zo storyboardovej tabuľky.

Dôkaz: [hárok](../../../research/2026-11-06-youtube-referencie/evidence/iqb5Rd6KKr8/overview-15s/page-003.jpg).

## 13:18–15:41

V 2 s vzorke sa rovnaká promptová interakcia objavuje v krémovej chatovej karte, v editore a v tmavom zelenom rozhraní. Následný slide oddeľuje prevzatý pohyb, layout a interakciu od farieb a písma.

Reč/funkcia: Tri použitia jedného už vytvoreného prompt boxu. Opakovateľná akcia s novým vzhľadom.

Prenos: Preniesť vzťah spúšť → akcia → výsledok. Kód fungujúceho prvku adaptovať na náš obraz a mierku; nekopírovať cudziu paletu ani nemeniteľný prijatý render.

Dôkaz: [hárok](../../../research/2026-11-06-youtube-referencie/evidence/iqb5Rd6KKr8/detail-reuse-798-830/page-001.jpg), [hárok](../../../research/2026-11-06-youtube-referencie/evidence/iqb5Rd6KKr8/overview-15s/page-004.jpg).

## 15:43–17:20

Najprv je viditeľný prompt storyboard.html. Pri 1009–1023 s ukazuje mriežku ôsmich statických návrhov: hook, kontrast, odhalenie, rám, výrazná veta, graf, logo a záver. Potom slide First Pass: Build It.

Reč/funkcia: Kontrola najplnšieho okamihu každej scény pred animovaním. Lacnejšie odhalenie nečitateľnosti a prázdnej scény.

Prenos: AI môže interne skontrolovať najhustejší frame každého plánovaného beatu spolu s existujúcimi titulkami. Je to výrobná kontrola, nie povinné nové kolo Adamových schválení.

Dôkaz: [hárok](../../../research/2026-11-06-youtube-referencie/evidence/iqb5Rd6KKr8/detail-frames-943-980/page-001.jpg), [hárok](../../../research/2026-11-06-youtube-referencie/evidence/iqb5Rd6KKr8/detail-storyboard-1009-1040/page-001.jpg).

## 17:20–18:30

Studio otvorí jednotlivý obal a potom koláž albumov s centrálnym bielym textom. Text sa vo vzorkách premiestni vertikálne; vidno jeho výberový rámik, pravý panel parametrov a neskôr panel kódu.

Reč/funkcia: Inspector na lokálnu zmenu prvku. Oprava konkrétneho objektu v už hotovej scéne.

Prenos: U nás opraviť rovnaký beat v novej revízii a porovnať jeho pred/po snímky. Kvôli jednej polohe textu neprepisovať celý klip ani jeho titulkový komponent.

Dôkaz: [hárok](../../../research/2026-11-06-youtube-referencie/evidence/iqb5Rd6KKr8/detail-finish-1040-1080/page-001.jpg), [hárok](../../../research/2026-11-06-youtube-referencie/evidence/iqb5Rd6KKr8/detail-finish-1040-1080/page-002.jpg), [hárok](../../../research/2026-11-06-youtube-referencie/evidence/iqb5Rd6KKr8/detail-inspector-1060-1110/page-001.jpg), [hárok](../../../research/2026-11-06-youtube-referencie/evidence/iqb5Rd6KKr8/detail-inspector-1060-1110/page-002.jpg).

## 19:30–20:38

Vpravo je exportný panel a vybraná hudobná kompozícia; následne sa obraz vracia na hovoriaceho hostiteľa.

Reč/funkcia: Hostia hovoria aj o samostatnom grafickom exporte. Možnosť používať framework ako dodávateľa jednej vrstvy.

Prenos: Ak raz HyperFrames vyrieši konkrétny obrazový nápad, preniesť hotový overený asset do existujúceho Remotionu s nameranou dĺžkou a kotvami. Tento výskum taký export nevytvoril.

Dôkaz: [hárok](../../../research/2026-11-06-youtube-referencie/evidence/iqb5Rd6KKr8/overview-15s/page-004.jpg), [hárok](../../../research/2026-11-06-youtube-referencie/evidence/iqb5Rd6KKr8/overview-15s/page-005.jpg).

## 25:44–27:29

V tejto časti sú prevažne hovoriace tváre; nejde o zobrazený eval alebo meranie.

Reč/funkcia: Rozdiel statickej estetiky a vedenia pozornosti v čase. Užitočná koncepčná výhrada, nie vizuálny benchmark.

Prenos: Po statickej kontrole musí nasledovať skutočná kontrola nástupu, vrcholu, výstupu a návratu. Dobrý frame nedokazuje dobrý pohyb ani zvuk.

Dôkaz: [hárok](../../../research/2026-11-06-youtube-referencie/evidence/iqb5Rd6KKr8/overview-15s/page-006.jpg).

## 31:34–36:06

Krátko ukazujú katalóg vizuálnych štýlov a upraviteľnú typografickú ukážku. Záver je rozhovor; ďalšie media-use schopnosti sa spomínajú ako budúca práca.

Reč/funkcia: Menšie hotové prvky, ich opakované použitie a ďalšie plány. Zúženie rozsahu tvrdenej automatizácie.

Prenos: Dostupnosť katalógu alebo roadmapy nie je naše prijatie štýlu ani dôkaz dodania 1 200 klipov. Výskumný komponent sa posudzuje na konkrétnej novej scéne.

Dôkaz: [hárok](../../../research/2026-11-06-youtube-referencie/evidence/iqb5Rd6KKr8/overview-15s/page-007.jpg), [hárok](../../../research/2026-11-06-youtube-referencie/evidence/iqb5Rd6KKr8/overview-15s/page-008.jpg).

## Tvrdenia a dostupný kód

- Web a skill stačia na vytvorenie launch videa. **Vidno:** Hotový Spotify príklad a primárny skill sú otvorené na obrazovke. **Neoverené:** Nevidíme celý neprerušený nový beh od prázdneho projektu; čas a počet revízií nemožno odvodiť.
- Kvalitu urýchľuje prevzatie konkrétneho komponentu a kontrola statických obrazov. **Vidno:** Tri štylizácie prompt boxu a8 návrhov storyboardu sú viditeľné. **Neoverené:** Z prezentácie nemožno odmerať zrýchlenie alebo potvrdiť rovnakú kvalitu na inom obsahu.
- Ručná oprava v Studio sa premieta do kódu. **Vidno:** Výber/posun textu, panel parametrov a následný panel kódu. **Neoverené:** Bez runtime testu nepotvrdzujeme úplný round-trip ani kompatibilitu s naším kontraktom.
- Video vyžaduje časovú estetiku a kontrolnú slučku. **Vidno:** Túto časť hostia rozprávajú, evaly neukazujú. **Neoverené:** Benchmark a výsledky interných evalov nie sú predložené.

[Konkrétne launch kompozície](https://github.com/heygen-com/hyperframes-launches) majú uložený commit `d7ac35069d74a3a437780579b3b7fe2f3eeace5f` z2026-09-26T07:36:50Z. Ide o súčasnú dostupnosť, nie preukázaný presný commit z videa. Kód nebol spustený.

## Priame uplatnenie v našom projekte

- Existujúci brand a konkrétne podklady tvoria vstup do významových beatov.
- Použiť mechanizmus z referencie, prispôsobiť vzhľad a predmet.
- Skontrolovať kritický frame každej scény a následne časovanie; lokálnu opravu vyhodnotiť na pred/po.

HyperFrames môže byť voliteľným dodávateľom jedného assetu. Finálna kompozícia, titulky, slovné kotvy a revízie ostávajú v existujúcom Remotione. [Úplná karta](../../../research/2026-11-06-youtube-referencie/cards/iqb5Rd6KKr8.json).
