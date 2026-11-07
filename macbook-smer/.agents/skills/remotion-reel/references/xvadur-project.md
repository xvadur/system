# Existing XVADUR runtime

Work in `../../../../reference/xvadur_klipy`. The installed skill is `..`; its references and scripts resolve relative to that folder.

## Resume and author

Read the project's `docs/CODEX_VYROBNY_POSTUP.md`, then query the chosen episode:

```sh
python3 system/cli/klipy.py cyklus --epizoda ID --akcia stav
```

Read the actual current Selection, transcript, analysis, plan and feedback needed for that clip. Source selection and final creative acceptance follow Adam's authorization; a supporting edit does not silently change speech.

For whole-scene authorship use the implemented `autor` workflow, documented in `../../../../reference/xvadur_klipy/docs/AUTORSKE_SCENY.md`. It snapshots this complete skill, brand and canonical speech/Timeline inputs, then accepts arbitrary local TSX components through a hashed manifest. `autor spusti` invokes a toolful Codex author; an already active Codex editor can perform the same prepare → write → manifest → render → inspect loop directly. Render uses the normal media staging, resource gate and verification. `@xvadur/authoring` exposes the source picture, exact captions, asset access and word-frame helpers; the wrapper preserves the original voice once.

The earlier structured-plan route remains available for operations expressible in its schema. Inspect `CreativeBriefSchema` and `EditPlanSchema` in `system/schemas/index.ts`, `system/schemas/editorial.ts` and current CLI help before importing a structured plan:

```sh
python3 system/cli/klipy.py navrhni --epizoda ID --klip ID --plan /absolute/plan.json --brief /absolute/brief.json
```

`--brief` is optional. This imports the first authored plan; later changes use the documented revision/feedback flow (`uprav --zmeny`, or the relevant targeted repair operation), preserving existing locks and parent hashes. Do not rerun a new generic model plan merely to save the editor's already-made decisions.

`system/pipeline/model.ts` is the legacy structured analyst and keeps its isolated profile. Whole-scene editing uses `system/pipeline/authoring.ts`, which loads the complete skill and allows a toolful author to read, write, render, inspect and repair the new composition. Do not route an unrestricted scene idea back through the legacy closed catalogue.

## Runtime and style

- Runtime/lockfile: `system/package.json` and `system/package-lock.json`; keep Remotion **4.0.529**. Use the installed runtime, not an unpinned `npx` installation.
- Canonical composition: `XVADUR` in `system/renderer/src/Root.tsx`, using `TimelineComposition` and metadata from the real RenderDocument.
- Selected speech, voice, captions and image events share the existing Timeline compiler and stable word/span IDs. Frame rates and dimensions belong to that revision. Older references include both 25 and 30 fps.
- Fiki captions: the exact component and font are linked in `brand/BRAND.md`. Existing ProductionPack versions and accepted renders remain immutable; a changed implementation needs a new version.
- New whole-scene/component work uses an authoring manifest and local modules. Existing registry bindings remain available for existing plans; a new visual idea does not need registration in that catalogue. The supplied TSX components are optional source examples.

## Materials and tools

Use the actual tools available in the executing session. Search for source footage/GIFs, retrieve suitable local material, or use the available image generation tool for a made-to-measure illustration. For generation, retain the returned actual image and provenance, then create a valid project material receipt using `docs/NASTROJOVE_ULOHY.md`. A prompt file is not the image. Validate exact people/events when those are requested.

Run the bundled measurement helpers with `../.venv/bin/python`; their isolated dependencies are pinned in `requirements.lock`. The existing project Python environment remains separate. The CLI launcher itself retains its documented invocation above.

Normal ASR uses the existing project implementation. The downloaded skill did not include Whisper binaries, models or `transcribe.mjs`; do not create a new ASR setup as an editing prerequisite. The optional retiming helper requires an explicit existing binary/model and writes a new intermediate file.

`scripts/camera-check.py` still contains the donor's example dimensions and keyframes. To use it, copy it into the clip's work directory and set those values from the actual planned camera. Running the unchanged example does not verify our clip. The hook/caption measurement scripts likewise need actual render frames and dimensions.

## Check and deliver

Render and review through the project production path. Keep check frames and temporary diagnostic files in the clip's work area. Use the current renderer's concurrency settings; the donor's 70-second benchmark and `concurrency=10` are not measurements of this machine or workload.

For audio subtraction supply the voice-only track of the exact selected edit, its fps and actual cue frames. The numerical output is not listening or a verdict on comic rhythm. Report the actual scope of technical, visual, motion and listening review.

This configuration activates a method for the Codex editor. It does not install a background production service, modify accounts, publish content, or prove monthly capacity.
