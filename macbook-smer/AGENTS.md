# Smer — pracovisko na MacBooku

Tento balík je samostatný pracovný priestor pre Adamove klipy Smer. Aktívny projekt je `smer/`; `reference/xvadur_klipy/` obsahuje prenesené podklady a zdrojový kód Fikiho systému. Jeho historické pokyny neurčujú klienta ani štýl tohto projektu.

## Začiatok práce

1. Pri prvom otvorení čítaj [zadanie Smer](context/SMER_BRIEF.md) a [odovzdávku](context/HANDOFF.md). Inštaláciu a orientáciu na MacBooku opisuje [START_HERE.md](START_HERE.md).
2. Pri návrhu, edite alebo oprave čítaj celý [.agents/skills/remotion-reel/SKILL.md](.agents/skills/remotion-reel/SKILL.md) a jeho `references/whole-scene-authoring.md`. Používaj Smer brief; pravidlá výslovne označené Fiki patria referenčnému projektu.
3. Podľa potrebnej operácie načítaj miestne Remotion skills. Pri preberaní cudzieho kódu čítaj `reference/xvadur_klipy/docs/ZDROJE_A_REUSE.md` a zachovaj jeho pôvod a licenciu.

## Výroba

- Adam vyberá pasáž a tvorivo prijíma celý výsledok. AI navrhuje kandidátov a samostatne rieši rutinný obraz, médiá, kompozíciu a zvuk. Ak Adam žiada najprv návrh, odovzdaj návrh pred výrobou.
- Pre aktuálny klip najprv nájdi dodaný zdroj a výber. Ak chýbajú, vyžiadaj iba zdroj/pasáž potrebnú na začatie; tvorivý smer už je v briefe.
- Zmeraj skutočné médiá cez `ffprobe`. Rozmery, fps, trvanie, zvukové stopy a slovné časy odvoď zo zdroja a zvoleného výstupu. Zachovaj zdroj a pôvodnú reč; zmeny výberu rob výslovne.
- Píš celé scény a vlastné komponenty v TSX. Remotion 4.0.529 je pripnutý cez `smer/package.json` a lockfile. Užitočnú réžiu HyperFrames prenášaj do Remotionu; renderovanie ostáva v Remotione.
- Udržuj jeden časovaný prepis a jeden výber reči pre obsahovú pasáž. Obrazové a zvukové udalosti viaž na jej slová. Výber, plán, implementácia a export musia odkazovať na rovnaké vstupy.
- Materiály hľadaj alebo generuj podľa konkrétnej obrazovej úlohy. Využi existujúce rozbory; otvor relevantné referenčné úseky, keď ich detail ovplyvní edit. Knižnica rastie z vykonanej práce.
- Pred implementáciou zapíš stručný `TREATMENT.md`: oblúk pasáže, obrazové akcie, použité médiá, slovné kotvy, zvuk a návraty. Pri Smer môže scénu niesť samotná tvár, gesto a presný strih, ak to slúži konkrétnej vete.
- Rozlišuj obsahovú pasáž, jej samostatné štýlové varianty a opravy jednotlivého variantu. Každý hotový variant má vlastnú identitu; oprava zvyšuje jeho revíziu. Pôvodný zdroj a prepis sa zdieľajú.

## Kontrola a odovzdanie

Over skutočný náhľad vrátane čitateľnosti na mobile, časovania, orezov, konca reči a zvuku. Pri oprave porovnaj rovnakú vetu alebo fázu akcie pred a po zmene a zachovaj funkčný zvyšok. Adamovi odovzdaj celý prehrateľný klip a stručne uveď rozsah kontroly. Snímky, waveform a úspešný render nie sú dokladom posluchu ani súvislého prehratia.

Pracuj v `smer/`; pôvodné prenesené podklady používaj ako referenciu. Zdrojové médiá, pracovné rendery, prístupy a účty nepatria do Gitu. Publikovanie, úprava účtov ani nasadenie nie sú súčasťou tohto zadania. Samotné otvorenie alebo klonovanie balíka nespúšťa výrobu.
