# Playable review in Codex

Deliver the full clip. When Adam requests a storyboard, or multiple beats benefit from separate review, provide playable excerpts with their actual speech, sound, time range and a short description of the intended action. Keep the entire clip available so isolated moments are judged in context.

Use the existing workplace review path when available, or local MP4 previews in Codex with absolute paths. Notes can refer to the beat number and timecode. Review can distinguish keep, change and remove without making Adam choose every material before production.

For a correction, preserve approved beats, revise the requested part and its dependencies, then deliver the new complete version plus the changed excerpt. Keep the old revision and its notes linked to their original bytes.

The supplied `components/storyboard-review.html` is the donor's Claude Artifact implementation. It calls `window.claude.use("db")` and `window.claude.use("user")`. This is **not** a functioning Codex review backend; do not present its buttons as connected here. Its visual layout can be adapted if a review UI is explicitly needed. Building or publishing that UI is not a prerequisite for producing a clip.

Use the actual Timeline fps when cutting excerpts; the donor's `/30` examples do not apply to every clip. Playback of a generated file is not evidence that the agent listened to it.
