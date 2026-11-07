# Nový Smer edit

`WorkspaceReady` je technická štartovacia karta. Jej rozmery, fps a vzhľad nie sú schválené parametre klipu. Aktuálny zdroj ešte nebol dodaný.

Pred vytvorením klipu načítaj `../../AGENTS.md`, `../../context/SMER_BRIEF.md` a relevantné časti `../../.agents/skills/remotion-reel/SKILL.md`. Zmeraj konkrétny zdroj, ulož vybranú pasáž a slovné časy a vytvor vlastné `Clip.tsx` a súvisiace moduly. Pridaj kompozíciu do `Root.tsx` so skutočnými parametrami. Prepis a reč majú jednu spoločnú časovú os.

`npm run studio` otvorí náhľadový server; `npm run typecheck` skontroluje kód. Export konkrétneho klipu ide cez `npm run render -- COMPOSITION_ID out/clip.mp4`, až keď je daný klip zadaný na výrobu. Samotné stiahnutie tohto balíka nie je zadanie nového renderu.
