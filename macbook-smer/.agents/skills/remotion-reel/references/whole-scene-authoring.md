# Whole-scene authorship in Remotion

Adam's instruction, 6 November 2026: use the full remotion-reel method and author complete scenes directly in Remotion. Keep the existing selected speech and exact Fiki captions. The number of objects, effects, source assets or local components follows the scene, not a fixed registry.

## Direct the complete visual action

For every sentence, identify the visible change and how it develops the preceding scene. Name the action of the relevant layers: the source picture docks, an object draws a path, a command changes the result, the camera reveals the larger environment, a mask exposes the next shot. Give the action an actual word anchor, setup, impact and exit. Specify supporting sound or intentionally clean speech. A motionless label and ordinary captions do not implement the sentence's edit.

Use one shared frame clock. A parent camera wrapper moves the whole environment while child elements perform local actions. One property has one owner; put camera motion and local object motion on separate wrappers. SVG masks, video mattes, CSS perspective, canvas, arbitrary React components and frame-driven 3D are available when useful. Select installed dependencies deliberately; keep the project's pinned Remotion runtime.

Connect scenes through a visible relationship. A monitor screen can become the next scene; its drawing can become a transition mask; a moving object can carry the eye into the next shot. When using a continuous movement, match axis, direction and speed on both sides. A deliberate hard cut is also a valid editorial decision. Inspect the outgoing frame, cut and incoming frame. Each long hold should either remain meaningful or develop: staged information, real media action, a consequential camera move or a changing object state.

This adapts the useful directing concepts of [beat-direction](https://github.com/edenfunf/reelmimic/blob/311d835b623e1b6790d8823298dc0d5553661fe2/.claude/skills/hyperframes-creative/references/beat-direction.md) and [motion-doctrine](https://github.com/edenfunf/reelmimic/blob/311d835b623e1b6790d8823298dc0d5553661fe2/.claude/skills/motion-doctrine/SKILL.md). No HyperFrames runtime, mandatory leftward movement, shader quota, easing ban or donor-specific aesthetic is imported. This is newly written project guidance; the source documents remain research material.

## Choose the actual implementation

- **Designed typography:** measured word reflow, large type interacting with a subject, video inside letters, text behind a genuine person matte, character/word-specific movement. Preserve speech captions wherever their function is still needed; make any temporary designed-type replacement intentional.
- **Camera and depth:** source crop, a pan across an actual document, multiple depth layers, common perspective, foreground occlusion, purposeful push/pull and a matched transition.
- **Responsive objects:** actual typing and selection, a changing diagram, code driving its visible result, a stateful physical gag, a screen playing real footage. Implement the action, not just its description.
- **Media composition:** full-screen B-roll under original voice, multiple independently timed videos, reaction with lead-in and payoff, accurate masks, a silhouette with separate background/foreground movement.
- **Material detail:** texture, edge treatment, grounded shadows, lighting and readable geometry appropriate to the idea. These can be code, existing media or generated artwork.
- **Sound:** measure cue onset, connect it to the visual cause, control its level against voice, verify the encoded output. A shared visual timeline does not imply every layer needs a sound.

The donor already provides camera, layout, matte, captions and audio implementation references. Read the specific references needed and use their working mechanics, adapting geometry and taste to Fiki. A copied example is not a finished scene.

## Execute through the authoring workflow

Use `autor priprav` to snapshot the complete skill and pinned inputs, then write `src/Clip.tsx` and local modules in that returned workspace. The component receives the renderer's real `document`. `@xvadur/authoring` provides optional primitives: `SourcePicture`, `ExactCaptions`, `Media`, `mediaAsset`, `wordFrame`, and `TimelineSound`. It does not prescribe a layout. The production shell owns the one original voice track; authored code owns all picture, caption presentation and supporting sound.

Create a manifest for every implementation revision, render a relevant range, inspect and repair, then render and check the whole clip. The manifest pins source code and Timeline hashes; source speech is checked against the parent Selection/Transcript. Follow the current commands in the project's `docs/AUTORSKE_SCENY.md` and CLI help. A technical check is separate from sampled visual review, motion review, listening and Adam's creative acceptance.

For future edits, improve the demonstrated mechanism or replace it when the new content calls for a different scene. Preserve prior revisions and accepted bytes. There is no prerequisite to build a catalogue before creating the first scene.
