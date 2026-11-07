# Captions — XVADUR

The default Fiki captions are the existing `chocolate-r5-word-pulse@1.0.0` implementation in `system/renderer/src/captions.ts` and `TimelineComposition.tsx`. Read the exact style and font source in the project `brand/BRAND.md`. Keep its uppercase Slovak text, active yellow word, pulse, measured line width and reserved word slots. The bundled neutral `components/Caption.tsx` is optional, not a replacement default.

## Timing and placement

Use the canonical Transcript and Selection; derive output times via the existing compiler. Preserve `wordId` and `spanId`. Measure the real face, mouth and background for this take. Retain the chosen lower caption band unless the actual composition requires a documented adjustment. Check the active pulse at its largest scale and all Slovak glyphs.

Group using the existing measured-width implementation and phrase boundaries. The donor's lowercase, no-pop rule, 17-character limit and fixed microphone position are not project rules. On a layout change ensure the caption remains readable and does not jump awkwardly mid-phrase. Continuous speech across B-roll still shares the same word clock.

For an isolated suspected defect compare actual frames, audio onset and the pinned transcript before changing timing. A new visual insert alone is not a reason to re-transcribe.

## Caption-band diagnostics

`scripts/caption-tone.py` measures the luminance of an explicit pixel region in caption-free render frames. Pass the region and actual scaled dimensions; its sample defaults belong to another take. The measurement is useful evidence for contrast, not an instruction to replace yellow emphasis or switch the existing caption style automatically. Inspect the rendered glyphs and outline too.

## Optional targeted re-timing

The default ASR is the existing project implementation. The supplied `scripts/retime-captions.py` is an optional repair helper when a matching whisper.cpp binary/model is available; it is not required for normal production.

It re-transcribes overlapping short windows, matches the approved words, takes median timing votes and interpolates unmatched words. The configured helper supports Slovak normalization, `--language sk` and the revision's `--fps`. Pass an exported word list with stable IDs and write a **new helper output path**. Validate the actual alignment and use the project's transcript revision operations to adopt a correction. Never overwrite or directly substitute a canonical transcript with the helper's plain array.

After an accepted timing correction, re-derive dependent graphics and sound anchors through the compiler. A numeric waveform check can locate silence/onsets; it does not demonstrate that every word is aligned or that the clip was listened to.
