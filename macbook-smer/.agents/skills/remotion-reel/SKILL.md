---
name: remotion-reel
description: Analyze references and edit or revise XVADUR short clips in Remotion, using the existing Fiki style and the Smer editorial direction. Use for clip planning, contextual memes and B-roll, generated visuals, captions, sound, and review of a specific edit.
---

# Remotion Reel — XVADUR

Portable export for the MacBook: read `context/SMER_BRIEF.md` from the package root first. The referenced Fiki project is a source snapshot; its Fiki-only CLI is not a ready Smer client. For Smer, author the composition in the local `smer/` Remotion project with the same measured speech timing. Fiki-specific density and caption rules apply only to Fiki. The full directing references and components remain available below.

Adaptation of Adam's local `Downloads/remotion-reel` bundle. Preserve its working method: measure the take, read the story, give each moment a job, build against real word anchors, and inspect the result. Source file hashes are in `source-manifest.json`; the Downloads original is unchanged.

## Start with the existing brief

Project: `../../../reference/xvadur_klipy`.

Read [the project's brand sheet](../../../reference/xvadur_klipy/brand/BRAND.md) at the start of an edit. It contains the chosen caption implementation, creative direction, reference paths and material policy. Adam has already supplied the style and extensive examples; use those before asking for more taste descriptions.

- **Configure or analyze:** complete the requested configuration or reference analysis. A request to configure this skill does not start a video render.
- **Edit / “urob klip”:** choose and execute the supporting edit autonomously within the selected passage and current brief. Show the resulting clip for creative judgment. Routine asset, effect and layout choices do not require a pitch round.
- **“Najprv návrh / pitch”:** prepare concrete alternatives grounded in the passage and references; wait for the requested choice before producing them.
- **Revise:** load the actual latest version and requested correction. Preserve working and locked parts; create a new revision and compare the changed passage with its previous version.

For production or resumption, read [project integration](references/xvadur-project.md). The coordinating editor runs `cyklus --akcia stav` before preparing an authoring workspace; inside an already prepared workspace use `autor --akcia stav` and its pinned inputs to resume. Use the `autor` workflow for whole-scene authorship: it snapshots this entire skill and the canonical speech inputs, accepts your TSX/modules, and renders them through the production renderer. The legacy JSON planner remains a separate limited route; it does not represent this skill's creative capabilities.

## 1. Ingest and measure

Probe the real media, fps, duration and streams. Reuse unchanged source and transcript artifacts. Use the existing project ingest/ASR; this bundle does not ship the `scripts/transcribe.mjs` mentioned by its original author.

Inspect source cuts, baked-in captions/graphics and several actual frames. Record face/eyes/mouth/mic and usable overlay areas for this take. A scene-change threshold such as 0.05 is a candidate detector, not proof of every cut. Confirm relevant boundaries visually.

When a decoding problem requires H.264 normalization, produce a separate normalized asset and verify its duration and time mapping. Preserve the source and the revision's fps; do not globally force 30 fps. Dimensions and frame numbers come from the real Timeline.

## 2. Read the story and the references

Read [motion graphics and editorial treatment](references/motion-graphics.md). Identify hook, necessary context, development, turn and payoff across the **whole passage**. A CTA is included only when requested by the brief.

Use the existing performance/reference analyses listed in the brand sheet. For a new reference or a disputed mechanism, follow [reference analysis](references/reference-analysis.md). Extract what the edit does at the relevant moment and transfer that behavior into this passage. An asset name or a written label for a scene does not implement its action.

The existing material is sufficient for an initial edit direction. Reopen only the specific reference detail needed to decide or verify the current treatment; avoid restarting the whole research exercise.

## 3. Edit every sentence of the selected candidate

For Fiki, apply [edit každej vety](../../../reference/xvadur_klipy/brand/BRAND.md#fiki--edit-každej-vety): cover every sentence, including connective and explanatory speech. Map each sentence to its concrete visual action or development of a continuing scene, material, sound treatment and actual speech anchors in the existing CreativeBrief/EditPlan. Ordinary captions alone do not satisfy this requirement. Make these choices autonomously. Density and treatment follow the client's brief; preserve continuity across sentences.

Select a concrete action or visual relationship, not just a literal keyword. A reaction has a usable lead-in, an action, its peak and an exit. Original speech can continue over full-screen media. Use the existing source image when its detail already carries the joke.

Acquire material to serve the idea: existing media, new search, image generation, or a purpose-built Remotion scene are ordinary choices. The library grows from actual production. Having a chicken from an earlier clip neither requires its reuse nor settles how to illustrate a new passage. Image generation is available for made-to-measure illustration; a generated image is not evidence of a real event.

If an asset is essential and missing, obtain it or report the concrete unresolved need. A stock placeholder, prompt sidecar or empty text card is not a completed visual.

## 4. Map the edit to speech

Map setup, reveal, visual hit, sound hit and return to actual `wordId` / `spanId` anchors or measured boundaries. The project compiler derives frames. Include the source trim and the reaction/SFX onset inside that trim; a file's first frame need not be its payoff.

Preserve the selected speech, meaning and context. A supporting visual operation does not silently change the Selection. For long-episode candidate selection use the existing episode analysis workflow; this skill's original bundle begins with a short take and is not an automatic long-video clip selector.

Store the treatment in the canonical CreativeBrief/EditPlan, including relevant reference and material decisions. Avoid creating a second independently timed timeline.

## 5. Build in the existing Remotion runtime

Use the project renderer and lockfile. Keep the existing Fiki caption component pinned by the brand sheet. The bundled neutral `components/Caption.tsx` is an optional donor component, not the Fiki default.

Read [whole-scene authorship](references/whole-scene-authoring.md) before implementing a clip. Write the composition and local components the idea needs. Own the whole picture: source framing, environment, foreground, media, masks, typography, camera, transitions and supporting sound share the real word clock. Existing catalogue entries are optional implementations; a new scene does not require registering every object or extending a universal JSON language. Complete ordinary creative decisions autonomously and inspect their actual render.

Read references only for the operations needed:

| Operation | Reference |
| --- | --- |
| Graphic/meme treatment | [motion-graphics.md](references/motion-graphics.md) |
| Captions and timing repair | [captions.md](references/captions.md) |
| Camera, split and optional silhouette | [layouts.md](references/layouts.md), [screen-recordings.md](references/screen-recordings.md), [split-screen-from-full-frame.md](references/split-screen-from-full-frame.md), [background-removal.md](references/background-removal.md) |
| Optional text hook | [text-hook.md](references/text-hook.md) |
| Music/SFX | [audio.md](references/audio.md) |
| Whole-scene code and coordinated motion | [whole-scene-authoring.md](references/whole-scene-authoring.md) |

Donor layout coordinates, palettes, tool paths and platform crop estimates are examples. The measured source, current output geometry and project brand take precedence. Current instruction (6 November): render in Remotion. Transfer useful HyperFrames/ReelMimic directing principles into frame-driven Remotion; do not add a second renderer for capabilities Remotion already provides. The retained hyperframes-hybrid document is historical optional reference, not a production prerequisite.

Independent media preparation can run in parallel. One owner assembles a coherent revision. Reuse approved material/implementations without modifying the old accepted composition or its bytes.

## 6. Inspect and repair

For Fiki, compare every sentence in the candidate with its mapped events in the actual render using the brand sheet's sentence coverage rule. Repair uncovered sentences and transitions before delivery; a completed planning entry is not proof that its edit was implemented.

Inspect actual render frames around entrances, reveals, cuts, caption changes and exits. Use one short range render for nearby events where practical; check mobile readability, real image action, overlaps and reaction timing. A contact sheet establishes sampled visual evidence, not continuous motion or listening.

Render through the existing production path. Verify that the intended music/SFX is actually in the output. The bundled `scripts/verify-audio.py` is a numerical diagnostic: compare against the **voice-only track of the exact selected edit**, pass its fps, and inspect the residual. Record genuine listening separately.

Compare the new result with the reference mechanism and, on revision, with the prior clip. Fix regressions in crop, caption style, speech, sound and already-working beats before delivery. Report the actual scope of AV review rather than claiming abilities that were not used.

## 7. Deliver and retain the correction

Deliver the complete playable clip and a changed excerpt when that helps evaluate a specific note. Describe the meaningful changes and their timecodes. Use [storyboard review](references/storyboard.md) when per-beat review is useful or requested; building a new review app is not a prerequisite for editing.

Apply a note to its real scope: this use, this asset, this technique or an explicit client rule. Preserve the useful correction for the next relevant clip. Adam makes final creative acceptance; exporting or publishing an earlier version is not blanket acceptance of its style.
