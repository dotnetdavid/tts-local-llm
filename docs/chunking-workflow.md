# Chunking Workflow

This tool is designed for small chunks because local Orpheus generation can produce volume jumps, odd pauses, and run-ons.

Recommended workflow:

1. Add pronunciation rules to `config/local.yaml`.
2. Add explicit pause markers to a TTS working copy of the text.
3. Run a dry run.
4. Inspect `chunks/*.txt`.
5. Generate WAV chunks.
6. Assemble and master in Reaper.

Dry run:

```bash
.venv/bin/python -m local_tts.cli generate story.txt \
  --output-dir jobs/story-dry-run \
  --config config/local.yaml \
  --voice tara \
  --max-words 85 \
  --dry-run
```

Audio generation:

```bash
.venv/bin/python -m local_tts.cli generate story.txt \
  --output-dir jobs/story-tara \
  --config config/local.yaml \
  --voice tara \
  --max-words 85
```

Use a smaller `--max-words` value when Orpheus rushes dialogue or eats pauses.
