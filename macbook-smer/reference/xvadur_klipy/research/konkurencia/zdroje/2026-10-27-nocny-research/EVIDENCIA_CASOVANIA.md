# Časové značky obrazových podkladov: oprava metódy

Pri nočnej kontrole sa zistilo, že pôvodné `whole.jpg` a `hook.jpg` vytvorené cez filter `fps` zobrazujú čas výstupného prevzorkovania. Obraz priradený k tomuto času sa môže od skutočnej zdrojovej pozície líšiť približne o jeden vzorkovací interval. Pri dlhom videu je to viac sekúnd. Označenie `0` v takomto prehľade preto samo nepreukazuje prvú zdrojovú snímku.

Pôvodné súbory a ich hashe zostávajú zachované. Sú použiteľné na prehľad skladby a vzhľadu, **nie na určovanie presnej hranice strihu**. Pri odkaze na ich čas používame približné okno s uvedeným rozsahom vzorkovania.

Opravená revízia je v [evidence-r2.json](evidence-r2.json), jednotlivé obrázky majú názvy `whole-r2.jpg` a `hook-r2.jpg`. Metóda vyberá prvý zdrojový frame a ďalší po dosiahnutí intervalu cez `select`, bez resetovania časovej osi; `drawtext` vypisuje zdrojové PTS pred skladaním do hárka. Aj tieto súbory zostávajú vzorkami, nie plynulým prehratím.

Pre kritický nástup alebo krátku chybu treba použiť priamy seek do zdrojového MP4, hustejšie okolie udalosti alebo časovaný pixelový test. Pre slová používame surové ASR s priznanou neistotou; presné nové výrobné kotvy vyžadujú vlastný overený prepis.

Vlastné výskumné snímky vytvorené analytikmi cez jednotlivé priame seeky sa týmto nálezom automaticky nespochybňujú. Vždy platí metóda uvedená pri konkrétnom dôkaze. Nejde o tvrdenie, že všetky staršie historické rozbory mali tú istú chybu.

## Pomer strán a výskumný padding

Prehľadové bunky majú jednotný portrétový rozmer 270 × 480. Zdroj sa doň vkladá so zachovaným pomerom strán a chýbajúci priestor doplní analytický padding. **Čiernu plochu hárka nesmieme pripísať kliperovi bez kontroly natívneho súboru a jeho rozmerov.** Pri širokom alebo inom neštandardnom zdroji treba otvoriť aj celú samostatnú snímku v jeho skutočnom pomere strán. Rovnako čierne medzery treba merať na zdrojovom videu, nie na hárku.
