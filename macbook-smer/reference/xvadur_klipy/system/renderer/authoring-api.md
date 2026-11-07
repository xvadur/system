# Whole-scene Remotion authoring API

The authored component owns the complete picture, camera, masks, media, typography, caption placement and supporting sound. It is ordinary React/Remotion TSX, not a list of preset scenes. The production shell mounts the original selected voice once, using the existing compiled `RenderDocument`. It does not automatically mount A-roll, captions, SFX or music.

Use Remotion **4.0.529** from the separate [authoring runtime](../runtime/authoring-4.0.529/README.md), whose exact dependencies and lockfile live in `system/runtime/authoring-4.0.529/`. Restore its disposable installation with `python3 system/cli/provision_author_runtime.py`; the normal `python3 system/cli/klipy.py autor …` entry selects it before loading TypeScript. The shared `system/package-lock.json` is not this route's dependency authority. HyperFrames is not used by this route.

## Component and helpers

```tsx
import React from 'react';
import {AbsoluteFill, useCurrentFrame} from 'remotion';
import {
  SourcePicture, ExactCaptions, TimelineSound, wordFrame,
  type AuthoredSceneProps,
} from '@xvadur/authoring';

export default function Clip({document}: AuthoredSceneProps) {
  const frame = useCurrentFrame();
  // Use a real id from inputs.json -> timeline.tracks.captions.
  const hit = wordFrame(document, 'actual-word-id', 'start', 'actual-span-id');
  return <AbsoluteFill>
    <SourcePicture document={document}/>
    {/* Write the real layered visual action here, driven by frame and hit. */}
    <ExactCaptions document={document} hidden={false}/>
    <TimelineSound document={document}/>
  </AbsoluteFill>;
}
```

This example only demonstrates the API. A talking head with ordinary captions is not a completed Fiki edit. Plan and implement every sentence's visual action, supporting sound and transitions using the configured skill and brand.

| Export | Contract |
| --- | --- |
| `AuthoredSceneProps` | `{document: RenderDocument}`. The runtime deep-freezes a copy; do not modify its speech, words or assets. Create derived visual props locally. |
| `SourcePicture` | `{document, framing?, style?}`. Renders the selected source picture **muted**. `framing` is a `Framing` value or `(span: RenderSpan) => Framing`. Wrap it in your own moving/clipped/masked elements as needed. |
| `ExactCaptions` | `{document, top?, hidden?}`. Uses the exact existing caption implementation and staged pinned font. Call once, conditionally change its placement/visibility, or filter a derived visual document for a deliberate typographic interval. Preserve the original spoken words and times. |
| `Media` | `{asset, sourceStartMs?, sourceEndMs?, framing?, transparent?, muted?, gain?, loop?, hold?, style?}`. Staged image/video in a transparent container; `transparent: true` enables video alpha. `muted` defaults to true. |
| `mediaAsset` | `mediaAsset(document, assetId)` returns a real staged asset and fails when absent. |
| `wordFrame` | `wordFrame(document, wordId, edge = 'start', spanId?)`. Returns an exact absolute output frame. A repeated source word needs `spanId`, or pass its full occurrence `id`. Ambiguous and missing words fail. |
| `TimelineSound` | `{document}`. Explicitly renders the existing Timeline SFX/music, once. The shell does **not** also add them. Omit it when authoring a replacement sound treatment. |

Use normal Remotion `Sequence`, `spring`, `interpolate`, `Img`, `OffthreadVideo`, audio and React/SVG/Canvas where useful. Supporting audio can be written directly using a staged asset URL, or can reuse `TimelineSound`. Do not replay the source voice: the shell already provides it. Source picture helpers are silent for this reason.

`document` contains staged assets (`url` usable with `staticFile`), source spans, event phases, caption words, fps, dimensions and the full duration. All source offsets have already been remapped if the production renderer made a compatible source derivative. Do not replace them with guessed times or assume the staged video begins at episode time zero.

## Code manifest and renderer

`AuthoredCompositionManifestSchema` is defined in `system/schemas/authored-composition.ts`:

```ts
{
  schemaVersion: 'authored-composition.v1',
  id: 'clip-id',
  revision: 1,
  parentManifestHash?: string,
  timelineHash: string, // hashArtifact of the exact input Timeline
  entryPath: string,    // normalized project-relative TSX/JS path
  exportName: 'default',
  files: [{path: string, hash: string}], // every local imported code/JSON file
  remotionVersion: '4.0.529'
}
```

The authoring CLI creates this manifest from actual bytes. Every relative import must be pinned in `files`; ordinary package imports must belong to the installed pinned runtime dependencies. `@xvadur/authoring` resolves to the production helper module. Media does not belong in the code manifest: acquire it with provenance and add it to a validated derived Timeline. The authoring CLI checks that the derived Timeline preserves the original selected voice and caption clock.

`verifyAuthoredComposition(projectRoot, manifest, timeline)` validates the revision binding, source bytes and local import graph. `renderTimeline(timeline, {...options, authoredComposition: manifest})` uses the normal resource gate, verified media cache/staging, source compatibility handling, font staging, browser lifecycle and technical output checks. It snapshots authored code into the render directory and generates a private composition entry. It never edits the shared `Root.tsx` or a historical video composition.

The render receipt identifies the authored manifest and implementation hashes alongside the existing renderer snapshot, input props, output hash and technical result. A new code or input revision requires a new manifest. A completed render is not Adam's creative acceptance and does not claim listening or continuous motion review.
