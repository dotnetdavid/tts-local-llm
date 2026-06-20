# Local TTS Workbench

Reusable local TTS tooling for LM Studio + Orpheus. The goal is not to make one polished audiobook file in a single pass. The goal is to generate many small, editable WAV clips with a manifest so they can be assembled, trimmed, compressed, and mastered in Reaper.

## What It Solves

- Generates small narration chunks instead of one giant brittle file.
- Supports pronunciation substitutions such as `Mara Vey` -> `Mara Vay`.
- Supports explicit pause markers such as `[[pause:750]]`.
- Writes a JSONL manifest for provenance and Reaper assembly.
- Keeps manuscripts, generated audio, local config, model caches, and virtual environments out of git by default.

## Current Backend

- LM Studio OpenAI-compatible completions endpoint.
- Orpheus GGUF model loaded in LM Studio.
- SNAC decoder locally converts Orpheus custom tokens to WAV.

This is a local tool. It does not upload story text unless you point it at a remote endpoint.

## Quick Start

```bash
cd /path/to/tts-local-llm
python3 -m venv .venv
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install -e '.[dev]'
```

For real audio generation, install the audio dependencies. Prefer CPU-only PyTorch unless you intentionally want GPU support:

```bash
.venv/bin/python -m pip install --index-url https://download.pytorch.org/whl/cpu --extra-index-url https://pypi.org/simple '.[audio]'
```

Check LM Studio:

```bash
.venv/bin/python -m local_tts.cli check-lmstudio --config config/example.yaml
```

Prepare chunks without generating audio:

```bash
.venv/bin/python -m local_tts.cli generate story.txt \
  --output-dir jobs/story-dry-run \
  --config config/example.yaml \
  --voice tara \
  --max-words 85 \
  --dry-run
```

Generate WAV chunks:

```bash
.venv/bin/python -m local_tts.cli generate story.txt \
  --output-dir jobs/story-tara \
  --config config/example.yaml \
  --voice tara \
  --max-words 85
```

## Input Markup

Use explicit pauses where Orpheus tends to run on:

```text
The room went quiet. [[pause:750]] Then the clicking started again.
```

Use pronunciation rules in YAML instead of distorting the manuscript:

```yaml
pronunciations:
  - source: "Mara Vey"
    replacement: "Mara Vay"
```

## Output

Each job directory contains:

- `chunks/*.txt`: exact text used for each generated chunk.
- `chunks/*.wav`: generated text chunks and silence pause chunks.
- `manifest.jsonl`: ordered chunk metadata.

## Development

Run tests:

```bash
.venv/bin/python -m pytest -q -s
```

`-s` avoids a local shell-startup output/capture issue in this environment.

## Documentation

- [Setup](docs/setup.md)
- [LM Studio + WSL](docs/lm-studio-wsl.md)
- [Chunking Workflow](docs/chunking-workflow.md)
- [Pronunciation Rules](docs/pronunciation.md)
- [Reaper Workflow](docs/reaper-workflow.md)
- [Troubleshooting](docs/troubleshooting.md)
- [GitHub Setup](docs/github.md)
