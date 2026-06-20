# Reaper Workflow

The tool outputs one WAV per chunk plus `manifest.jsonl`.

Suggested Reaper pass:

1. Import all `chunks/*.wav` in manifest order.
2. Trim awkward lead/trail silences.
3. Fix run-ons by returning to the source text and adding `[[pause:...]]` markers.
4. Apply compression/normalization across the assembled narration.
5. Export the final proof-listen MP3/WAV from Reaper.

Do not over-polish the generated chunks before assembly. The point is to keep edits visible and recoverable.

The manifest records source text and chunk filenames so bad takes can be regenerated without guessing.
