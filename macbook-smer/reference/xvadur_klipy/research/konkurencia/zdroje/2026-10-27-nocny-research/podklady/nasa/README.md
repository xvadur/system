# Dva získané čisté obrazové podklady

Získané počas noci 27./28. októbra 2026 z oficiálneho NASA Image and Video Library API. Obe skutočné fotografie boli otvorené cez `view_image` a rozmermi overené cez `ffprobe`. Nemajú cudzie titulky ani CTA. Ide o nové vlastné získanie, nie dôkaz presného súboru použitého konkurenčným kliperom.

| Podklad | Skutočný súbor | Obsah a využitie | Pôvod |
| --- | --- | --- | --- |
| Zem, Apollo 17 | [earth-apollo17-blue-marble.jpg](earth-apollo17-blue-marble.jpg), 1920 × 1920 | Celý zemský disk, Afrika, Arabský polostrov, oblaky a čierne pozadie. Identifikácia planéty pri pomenovaní Zeme, prípadne samostatný historický fotografický panel. | [NASA API, AS17-148-22727](https://images-api.nasa.gov/search?q=AS17-148-22727&media_type=image), [oficiálny opis fotografie](https://svs.gsfc.nasa.gov/30613), [miestne metadáta a hash](earth-apollo17-blue-marble.json) |
| Astronaut pri vlajke, Apollo 11 | [apollo11-astronaut-flag.jpg](apollo11-astronaut-flag.jpg), 1856 × 1920 | Astronaut na mesačnom povrchu vedľa americkej vlajky, modul naľavo, stopy v popredí. Konkrétna historická fotografická referencia pri pomenovaní programu Apollo alebo príslušnej udalosti. | [NASA API, AS11-40-5875](https://images-api.nasa.gov/search?q=AS11-40-5875&media_type=image), [miestne metadáta a hash](apollo11-astronaut-flag.json) |

Identifikácia udalostí je z primárnych metadát NASA; fotografia AS17-148-22727 je opísaná aj na [stránke NASA SVS](https://svs.gsfc.nasa.gov/30613). Fotografia neoveruje všetky výroky, ktoré pri nej môže hovoriaci vysloviť.

Praktický prenos: vlastný hovoriaci → krátka identifikovaná fotografia pri skutočnej zmienke → návrat na tvár. Pri porovnaní alebo tierliste fotografia iba identifikuje položku; nevymýšľa jej hodnotenie či poradie. Rovnaký súbor možno použiť v celku aj detaile, pokiaľ sa zachová jeho historická identita.

Zdroj a kredit sú uložené pri súboroch. Pravidlá ďalšieho použitia uvádza [NASA Images and Media Usage Guidelines](https://www.nasa.gov/nasa-brand-center/images-and-media/); nejde o plošnú licenčnú garanciu pre každý marketingový kontext. Súbory sa nemenili, nevznikol generovaný fotorealistický obraz ani nový Fiki render. V produkcii ešte treba vytvoriť konkrétny AssetRequest/AssetRecord, vhodný výrez a časovú kotvu; tento výskumný obsahový check nie je Adamovo tvorivé prijatie.
