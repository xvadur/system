# Validácia 100 referenčných rozborov

Čas dokončenia (UTC): 2026-11-06T00:23:06.917412+00:00

**Výsledok: prešla kontrola artefaktov a väzieb na dôkazy.** Toto nie je tvorivé prijatie Adamom ani kompletná audiovizuálna kontrola.

| Kontrola | Výsledok |
|---|---|
| Vybraných jedinečných ID / JSON / MD | 100 / 100 / 100 |
| Karty, ktoré prešli | 100 / 100 |
| Konkrétne analytické beaty | 415 |
| Deklarované otvorené obrázky, jedinečné súbory | 260 |
| Husté source-PTS vzorky v manifestoch | 3051 |
| Čerstvý hash a ffprobe zdrojových MP4 | 100 / 100 |
| Karty s celou hustou sadou v openedImages | 100 / 100 |
| Chyby / evidenčné poznámky | 0 / 8 |

Overenie porovnalo finálnych 100 ID v candidates.json so štyrmi dávkami, kartami, obrazovými manifestmi a finálnym transcripts.json. Každá karta má aspoň tri beaty s pozorovaním, slovnou kotvou, funkciou a prenosom. Všetky uvedené intervaly sa kontrolovali voči novej hodnote ffprobe, bez tolerovania presahu za koniec. Kontrola úvodu a konca znamená prítomnosť analytického beatu, nie súvislé sledovanie každej sekundy.

Znovu sa prečítali bajty všetkých MP4 a vypočítal SHA-256. Pri obrázkoch sa overila existencia, JPEG/PNG signatúra a čerstvý hash; dostupné hashe z dávkových manifestov sa porovnali. ASR súbory sú čitateľné JSON s neprázdnymi segmentmi a zodpovedajú finálnemu manifestu. Toto neoveruje správnosť slov ani významu prepisu.

Podrobnosti pre každý klip, čerstvé hashe médií, kariet, prepisov a obrázkov sú vo [validation.json](<../../../../research/konkurencia/zdroje/2026-11-06-top100-remotion-reel/validation.json>).

## Hranice výsledku

- Artifact validation only: presence and provenance checks do not establish creative quality or Adam’s acceptance.
- The validator did not reopen every image; openedImages records are the analysts’ declared review inventory. It checked current files, image signatures and hashes.
- Dense source-PTS frames are sampled at about 2-second intervals; short edits/actions between samples may be absent. Extra detail sampling exists only where an analyst added it.
- No continuous playback or audio listening was performed in this review. SFX, music, mixing, vocal performance and exact transitions remain unverified.
- Raw ASR is available but is not a verbatim or semantically verified transcript. Specific omissions/repetition failures are documented in individual cards.
- Beat intervals are analytical ranges, not frame-exact edit boundaries. Opening/end coverage checks do not establish continuous coverage of all events.
- Historical performance measurements are a selection signal, not causal proof of editing effectiveness or proof of the speaker’s claims.
- These cards provide examples and transfer hypotheses. Successful plain talking heads do not replace Adam’s chosen dense meaningful meme/effect direction for Fiki.

## Doplňujúce obrazové dôkazy

Tieto doplnkové obrázky sú uvedené v kartách a ich aktuálne súbory/hash boli overené. Nie sú položkami štandardných výstupov príslušného evidence-N.json, preto ich tento audit nepovažuje za porovnanie s pôvodným dávkovým hashom:

- 7690230294305066262: Additional declared image is not listed in this batch evidence outputs; existence/signature/hash recorded: ../../../../research/konkurencia/zdroje/2026-11-06-top100-remotion-reel/evidence/7690230294305066262/detail-38-43-step025/page-001.jpg
- 7694220059346013462: Additional declared image is not listed in this batch evidence outputs; existence/signature/hash recorded: ../../../../research/konkurencia/zdroje/2026-11-06-top100-remotion-reel/evidence/7694220059346013462/detail-44-60-05s.jpg
- 7692317747530714401: Additional declared image is not listed in this batch evidence outputs; existence/signature/hash recorded: ../../../../research/konkurencia/zdroje/2026-11-06-top100-remotion-reel/evidence/7692317747530714401/detail-46-52-05s.jpg
- 7693277737947106582: Additional declared image is not listed in this batch evidence outputs; existence/signature/hash recorded: ../../../../research/konkurencia/zdroje/2026-11-06-top100-remotion-reel/evidence/7693277737947106582/detail-batch2/16-20-half-second.jpg
- 7692805590359379223: Additional declared image is not listed in this batch evidence outputs; existence/signature/hash recorded: ../../../../research/konkurencia/zdroje/2026-11-06-top100-remotion-reel/evidence/7692805590359379223/detail-batch2/20-26-half-second.jpg
- 7696100146953637142: Additional declared image is not listed in this batch evidence outputs; existence/signature/hash recorded: ../../../../research/konkurencia/zdroje/2026-11-06-top100-remotion-reel/evidence/7696100146953637142/detail-batch2/50-59-half-second.jpg
- 7691343843693825312: Additional declared image is not listed in this batch evidence outputs; existence/signature/hash recorded: ../../../../research/konkurencia/zdroje/2026-11-06-top100-remotion-reel/evidence/7691343843693825312/8b4f7b6f39f73537/detail-root/49-58-0.5.jpg
- 7695348663014477088: Additional declared image is not listed in this batch evidence outputs; existence/signature/hash recorded: ../../../../research/konkurencia/zdroje/2026-11-06-top100-remotion-reel/evidence/7695348663014477088/936b17ec172058a6/detail-root/21-28-0.5.jpg

## Rozdelenie práce

| Analytik | Karty |
|---|---|
| /root/pripomienky_klipu | 25 |
| extrakcia_kontext | 25 |
| extrakcia_vyroba | 25 |
| root | 25 |

Kontrola nemenila karty, médiá, snímky ani originálne prepisy. Technické opravy intervalov vykonali vlastní autori pred týmto finálnym auditom. Výskumné podklady ostávajú oddelené od produkčného prijatia.
