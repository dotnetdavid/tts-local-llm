# Setup

## Requirements

- Python 3.10 or newer.
- LM Studio with an Orpheus GGUF model loaded.
- `ffmpeg` for later post-processing.
- Enough disk for PyTorch/SNAC dependencies if generating audio.

## Install Text/Dev Tooling

```bash
cd /path/to/tts-local-llm
python3 -m venv .venv
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install -e '.[dev]'
```

## Install Audio Dependencies

Use CPU-only PyTorch by default. The default PyPI `torch` install may pull large CUDA packages.

```bash
.venv/bin/python -m pip install --index-url https://download.pytorch.org/whl/cpu --extra-index-url https://pypi.org/simple '.[audio]'
```

## Verify

```bash
.venv/bin/python -m pytest -q -s
.venv/bin/python -m local_tts.cli --help
```
