# Ako majú vyzerať klipy — spoločný podklad na doprecizovanie

**Stav: extrakcia Adamových požiadaviek z chatov, 5. november 2026.** Nie je to nový schválený skill ani ďalší implementačný plán. Priame zadania sú oddelené od AI návrhov. Podrobné citácie, chronológia a všetky dostupné dialógové správy sú v [indexe zdrojov](INDEX.md).

## Základ, ktorý už je povedaný

Chceme určiť použiteľný štýl a pracovný postup, podľa ktorého AI samostatne vyrobí bohatý edit. V reči nájde významové momenty, priradí vhodný obraz/GIF/meme/B-roll, upraví kompozíciu a pohyb, pridá titulky a zvuk a skontroluje výsledok. Adam udáva vkus, smer a finálny úsudok; nemusí vyberať každý súbor ani ručne vykonávať edit. [Najnovšie spresnenie A03](DOPLNENIA_Z_TOHTO_CHATU.md#A03), [výrobný chat M0047](spravy/01a1a6ef-49f9-7aa2-b18b-6d58f22e1d14.md#M0047), [Upratať PC… M0102](spravy/01a1a7cd-9816-77b3-b07c-7dfc275bd904.md#M0102).

**Najnovšie rozhodnutie: pokračovať v Remotione a v štýle, ktorý sme v ňom už robili. Edits odkladáme.** Toto je Adamov priamy pokyn počas extrakcie a má prednosť pred historickým skúšaním editorov. [A04](DOPLNENIA_Z_TOHTO_CHATU.md#A04).

**Najnovšie rozlíšenie tvorivých smerov:** Fiki má zostať výrazný, s rozumne použitými efektmi a významovo vhodnými médiami. Smer má mať zdržanlivejší, jednoduchší edit s výbornou štruktúrou, silným hookom a úderným obsahom. Oba smery patria do aktuálneho plánovania k cieľu 1 200 mesačne; rozdelenie objemu zostáva otvorené. [A05](DOPLNENIA_Z_TOHTO_CHATU.md#A05).

**Najnovšia oprava postupu:** nakonfigurovať konkrétny `Downloads/remotion-reel` podľa už dostupných referencií. Budovanie knižnice vopred nie je podmienkou ďalšieho klipu; materiály sa hľadajú alebo generujú na mieru významu. Minulý asset sám neurčuje ďalšiu scénu. [A06](DOPLNENIA_Z_TOHTO_CHATU.md#A06), [aktívne nastavenie](../../brand/BRAND.md).

## Čo má byť na výsledku vidieť a počuť

| Požiadavka | Doložené znenie / význam | Zdroj |
|---|---|---|
| **Bohatý, výrazný edit** | „preplacane efektami ktore sa tam hodia“; obsahovo vhodné efekty, prechody, meme a pohyb majú byť skutočne viditeľné. | [Výroba M0097](spravy/01a1a6ef-49f9-7aa2-b18b-6d58f22e1d14.md#M0097) |
| **Ťažisko v B-rolle, GIFoch a meme** | „menej na animaciach“. Vlastné animácie ostávajú možnosťou pre konkrétny účel. Dlhá statická postavička nebola žiadaný smer. | [Upratať PC… M0087](spravy/01a1a7cd-9816-77b3-b07c-7dfc275bd904.md#M0087), [Výroba M0023/M0036](spravy/01a1a6ef-49f9-7aa2-b18b-6d58f22e1d14.md#M0036) |
| **Význam reči spojený s obrazovou akciou** | Vybrať vhodnú reakciu, gesto, situáciu či predmet podľa konkrétneho významu. Adam chce, aby toto rozhodovanie robila AI. | [Výroba M0047](spravy/01a1a6ef-49f9-7aa2-b18b-6d58f22e1d14.md#M0047), [Návrh systému M0042](spravy/01a19c8c-b846-71a1-a878-189a2b457ee1.md#M0042) |
| **Posúdiť celý klip po významových úsekoch** | Kandidát má vety/sekcie; pri každej sa vyberajú vhodné vrstvy. „Každý frame“ má byť kurátorovaný. | [Výroba M0057](spravy/01a1a6ef-49f9-7aa2-b18b-6d58f22e1d14.md#M0057), [M0104](spravy/01a1a6ef-49f9-7aa2-b18b-6d58f22e1d14.md#M0104) |
| **Vrstvy sa môžu kombinovať a prekrývať** | Spoločná paleta obsahuje titulky, médiá, kompozíciu/zoom, pohyb, efekty, prechody, SFX a hudbu. „Nie vždy musia byť všetky.“ Úplný katalóg možností ešte nie je uzavretý. | [Výroba M0057](spravy/01a1a6ef-49f9-7aa2-b18b-6d58f22e1d14.md#M0057), [M0061](spravy/01a1a6ef-49f9-7aa2-b18b-6d58f22e1d14.md#M0061), [Upratať PC… M0089](spravy/01a1a7cd-9816-77b3-b07c-7dfc275bd904.md#M0089) |
| **Zachovať rozpoznateľné titulky** | „titulky dole, popup na slovo, zlte.. v tom potrebujem pokracovat“. Presný komponent treba prevziať z existujúceho výsledku. | [Upratať PC… M0102](spravy/01a1a7cd-9816-77b3-b07c-7dfc275bd904.md#M0102) |
| **Skúšať viac obrazových formátov** | Fikiho hlas môže pokračovať nad B-rollom. Žiada kombinovať meme, rôzne formáty a kity. Tvár nemusí byť nepretržite hlavným obrazom. | [Upratať PC… M0089](spravy/01a1a7cd-9816-77b3-b07c-7dfc275bd904.md#M0089), [M0102](spravy/01a1a7cd-9816-77b3-b07c-7dfc275bd904.md#M0102) |
| **Zvuk je plnohodnotná vrstva** | Pracovať so SFX a hudbou. Použiteľné hotové zvuky možno sťahovať; generovať netreba každý zvuk. ElevenLabs podľa potreby cez API. | [Výroba M0013–M0014](spravy/01a1a6ef-49f9-7aa2-b18b-6d58f22e1d14.md#M0013), [M0057](spravy/01a1a6ef-49f9-7aa2-b18b-6d58f22e1d14.md#M0057) |

„Kurátorovaný každý frame“ tu vykladáme ako vedomé spracovanie celej dĺžky. Adam nikde neurčil povinnosť pridávať nový efekt v každom snímku. „30 strihov/editov“ bola orientačná predstava hustoty; „40 parametrov“ označovalo neuzavretý návrh AI. Ani jedno číslo nie je prijatá univerzálna kvóta.

## Ako má AI pracovať

- **Použiť existujúce rozbory a konkrétne funkčné mechanizmy.** Rozbor má zachytiť, čo sa deje, kedy a prečo to funguje. Záznam typu „je tam vlajka“ je nedostatočný. [Výroba M0054](spravy/01a1a6ef-49f9-7aa2-b18b-6d58f22e1d14.md#M0054).
- **Skutočne preberať postupy z referencií a zabezpečiť materiál podľa významu.** Rozbor sa má prejaviť v ďalšom edite. Pripravené podklady sú možnosťou; A06 výslovne odmieta budovanie knižnice dopredu ako povinnú prípravu a pripomína hľadanie aj imagegen na mieru. [A05](DOPLNENIA_Z_TOHTO_CHATU.md#A05), [A06](DOPLNENIA_Z_TOHTO_CHATU.md#A06).
- **Prevziať použiteľné skilly a diely.** Adam výslovne žiada pozrieť, ako funguje Herkov edit a iné GitHub projekty; samotný zoznam editorov problém nerieši. [Porovnaj Risa… M0021](spravy/01a1acdd-3c74-7a32-beba-9df4a6d67466.md#M0021).
- **Pripravovať nezávislé vrstvy paralelne.** Cieľ je šetriť čas pri zachovaní dokumentácie a kontroly výsledku. Pevný počet agentov nebol prijatý. [Výroba M0054](spravy/01a1a6ef-49f9-7aa2-b18b-6d58f22e1d14.md#M0054), [M0101](spravy/01a1a6ef-49f9-7aa2-b18b-6d58f22e1d14.md#M0101).
- **Materiály získavať podľa potreby obsahu.** Knižnica pomáha a rozrastá sa; nevyžaduje sa najprv vyčerpať všetko lokálne. [Návrh systému M0042](spravy/01a19c8c-b846-71a1-a878-189a2b457ee1.md#M0042).
- **Rozlišovať dohadovanie a výrobu.** Keď Adam žiada najprv prejsť možnosti a konkrétny návrh, agent má túto prácu dokončiť pred renderom. Neskoršie výslovné zadanie výroby platí pre danú úlohu. [Výroba M0099](spravy/01a1a6ef-49f9-7aa2-b18b-6d58f22e1d14.md#M0099).
- **Zachovať rozhodnutia medzi chatmi.** Referencie, pripomienky a výsledky musia byť dohľadateľné; Adam ich nemá opakovane vysvetľovať. [Savegame M0009](spravy/01a18984-424f-7112-8c01-5ecd0b8aafeb.md#M0009), [aktuálne zadanie A02](DOPLNENIA_Z_TOHTO_CHATU.md#A02).

## Konkrétne body, o ktoré sa môžeme oprieť

| Referencia | Čo máme skutočne potvrdené |
|---|---|
| **Zoom na Fikiho obraz Boha pri „kto som ja aby som hodnotil“** | Priama pochvala: „to je vyborne, to by ma ani nenapadlo“. Pozitívny príklad významového využitia pôvodného záberu. [Výroba M0109](spravy/01a1a6ef-49f9-7aa2-b18b-6d58f22e1d14.md#M0109). |
| **Rossovo gesto** | „Áno, to je fajn“ ako základ úseku; Adam následne žiada spracovať ďalšie vrstvy. Nie je tým prijatá ľubovoľná kompozícia GIFu. [Výroba M0057](spravy/01a1a6ef-49f9-7aa2-b18b-6d58f22e1d14.md#M0057). |
| **Lokálny remotion-reel** | Adam ho označuje za presný príklad toho, čo si predstavoval pod systémom na klipovanie. Je to referencia pracovného postupu, nie automatické prijatie každého štýlu v balíku. [Upratať PC… M0058](spravy/01a1a7cd-9816-77b3-b07c-7dfc275bd904.md#M0058). |
| **Svedomie r5, publikovaná V1 a Edits r1** | Publikácia/povolenie pokusu boli nasledované kritikou. Tieto výsledky nemožno vyhlásiť za všeobecne prijatú latku. [Výroba M0087/M0097](spravy/01a1a6ef-49f9-7aa2-b18b-6d58f22e1d14.md#M0097), [Upratať PC… M0099/M0102](spravy/01a1a7cd-9816-77b3-b07c-7dfc275bd904.md#M0102). |
| **Vajanského, Električka, Pas, Čokolády, Detroit, SOWA, fiki.extra, Rišo** | Historické vlastné a cudzie referencie. Ich role a doloženie prijatia sa líšia; podrobnosti a cesty sú v [registri referencií](REFERENCIE.md). |

## Neskoršie opravy, ktoré majú prednosť

1. **„Hodnotím“ je príklad, nie celé zadanie.** Adam výslovne žiada prejsť dostupné vrstvy a ich použitie na celom kandidátovi. Jeden rozpracovaný gag nesmie nahradiť zvyšok. [Výroba M0106](spravy/01a1a6ef-49f9-7aa2-b18b-6d58f22e1d14.md#M0106).
2. **Najprv kvalitná výroba, potom napojenie na web.** Novšia požiadavka oddeľuje pracovisko editovania od webu. Existujúci web sa tým neruší; jeho budovanie nemá odsúvať samotný klip. [Upratať PC… M0041](spravy/01a1a7cd-9816-77b3-b07c-7dfc275bd904.md#M0041).
3. **Edits je odložený; pokračuje Remotion s existujúcim štýlom.** Nová priama voľba [A04](DOPLNENIA_Z_TOHTO_CHATU.md#A04) uzatvára skoršiu otázku editora. Historické skúšky zostávajú dôkazom požiadaviek a chýb, nie aktuálnym smerom výroby.
4. **Objemový cieľ je teraz 1 200 mesačne pre plánovanie Fikiho aj Smeru.** Najnovšie spresnenie výslovne uvádza oba smery; ich číselné rozdelenie zostáva otvorené. Historicky spomínal 600 + obdobnú ambíciu pre Smer. Cieľ neznamená dosiahnutú kapacitu. [A01](DOPLNENIA_Z_TOHTO_CHATU.md#A01), [A05](DOPLNENIA_Z_TOHTO_CHATU.md#A05), [Výroba M0104](spravy/01a1a6ef-49f9-7aa2-b18b-6d58f22e1d14.md#M0104).
5. **Technická prevádzka bola opravená na Mac + CLI, Cloudflare web a Drive.** Starší požadovaný externý server nie je posledným rozhodnutím. Neskoršie oddelenie editovania od webu mení prioritu a usporiadanie, nie je samo o sebe novým výberom hostingu. [Návrh systému M0163](spravy/01a19c8c-b846-71a1-a878-189a2b457ee1.md#M0163).

Konkrétne jednorazové zadanie portrétovej r2 Svedomia z 5. novembra je zachované v [prevádzkovom rozbore](rozbory/prevadzka-a-najnovsie-opravy.md). Odstránenie určitých meme v tejto jednej verzii sa nestáva všeobecným zákazom meme. Jeho vtedajší výber Edits prekonáva aktuálna voľba Remotionu v A04.

## Čo spolu ešte doprecizujeme na existujúcich ukážkach

Nechýba odpoveď na otázku, či Adam chce GIFy, efekty, bohatý edit alebo samostatnú prácu AI. Toto už povedal.

Zostávajú štyri konkrétne úlohy pri ukážkach:

1. **Zachovať presný titulkový vzhľad:** z existujúceho výsledku vybrať komponent, ktorý zodpovedá spodným žltým slovným pop titulkom.
2. **Ukázať želanú hustotu a energiu:** na krátkom úseku označiť, ktoré súčasné vrstvy a ich časovanie tvoria dobrý výsledok; porovnať s odmietnutým úsekom.
3. **Zvoliť pracovné formáty:** tvár s reakciou, celoplošné meme/B-roll s pôvodným hlasom, kombinovaná kompozícia a ďalšie vhodné varianty. Presné pomery sa nemajú vymyslieť bez opory v ukážkach.
4. **Z dostupných postupov urobiť krátke vykonateľné pravidlá:** kedy ktorú možnosť použiť a ako overiť jej výsledok. Remotion-reel a doložené kliperské mechanizmy sú pripravené zdroje na túto prácu.

Podrobné stopy zostávajú v prílohách. Na spoločné doprecizovanie stačí tento dokument a konkrétne dostupné ukážky.
