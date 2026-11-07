# Audio

XVADUR adaptation: use the current Timeline fps instead of the example 30 fps
below. Sound choices are delegated when Adam asks for an edit; offer alternatives
first only in an explicitly requested pitch. Numerical checks are diagnostics,
not evidence of listening. Keep originals and use new, traceable derived assets.

## Music beds

**Use the creator's original file and trim in code.** Never write trimmed or
loudnormed copies into the music pack (he asked, 2026-10-08). `trimBefore`
plays the original from any point (verified on Remotion 4.0.475):

```tsx
<Audio src={staticFile("music pack/Original Song.mp3")}
  trimBefore={Math.round(START_S * 30)}                      // where in the track to start
  volume={(f) => GAIN * interpolate(f, [0, 5, DUR - 36, DUR - 1], [0, 1, 1, 0],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" })} />
```

Choose where in the track to start by profiling it, not by starting at zero:

```bash
ffmpeg -v error -i track.mp3 -ac 1 -ar 8000 -f s16le - | python3 -c "...0.5s RMS envelope..."
```

Many tracks open with a sparse intro that vanishes under a voice. Starting on the
full-band downbeat usually serves a reel better; to land a drop on a cut,
`START_S = dropTime - cutFrame / 30`.

If the chosen window swings in level (one track moved 17 dB across 50 seconds),
even it out with the `volume` curve (keyframes from the measured envelope)
rather than a loudnormed copy.

**Target the bed at roughly 15 to 18 dB under the voice**, which lands around
-31 dB when the voice sits near -15 dB. Set the gain from the measured mean of the window you
use rather than guessing:

```
gain = 10 ** ((targetDb - measuredMeanDb) / 20)
```

## Sound effects

Measure whether a sound file has silence or a buildup before its intended hit.
That lead may be zero. Start each cue by the measured lead so its hit lands on
the intended frame:

```tsx
type Cue = { at: number; f: string; v: number };
const LEAD: Record<string, number> = { "pop.mp3": 6, "woosh 2.mp3": 3, "mouseclick.mp3": 2 };

const Sfx = () => (
  <>{CUES.map((c, i) => {
    const from = Math.max(0, c.at - (LEAD[c.f] ?? 0));
    return (
      <Sequence key={i} from={from} durationInFrames={DUR - from}>
        <Audio src={staticFile(`sound pack/${c.f}`)} volume={c.v} />
      </Sequence>
    );
  })}</>
);
```

Measure the lead off the waveform rather than trusting a table:

```python
pk = np.max(np.abs(a))
onset = np.argmax(np.abs(a) > pk * 0.12) / sr      # lead, in seconds
```

If a stock file is too quiet to carry its moment, make a louder copy rather than
pushing `volume` past 1:

```bash
ffmpeg -y -i quiet.mp3 -af "volume=14dB,alimiter=limit=0.89" -c:a libmp3lame -b:a 256k loud.mp3
```

Choose cues with actual word/action anchors and measured lead-ins. Inspect their
combination with voice and music. If Adam requests a proposal, show those choices
before building; otherwise complete the sound layer and submit the result.

## Verification

Never assume a bed or a cue made it into the render. Subtract a voice-only track
of the exact selected edit from the render and inspect the residual with
`scripts/verify-audio.py --fps FPS voice-edit.wav render.mp4 frame:label`.
The full uncut episode is not a matching reference for a reassembled clip.

The method: find the encoder delay by correlating the first few seconds (AAC
typically 2048 samples, sometimes 2032), scale the source to best fit, subtract,
and what remains is everything you added.

The donor's diagnostic reference levels follow. Apply them as starting points,
with intentional voice processing and the actual mix taken into account:

- **voice gain about 1.0.** Anything else means the voice was altered.
- **bed 15 to 18 dB below the voice**, steady across the video.
- **every cue visible as a peak** 9 to 20 dB above the bed, at its frame.
- **render mean within 0.1 dB of the source mean**, and no new clipping.
