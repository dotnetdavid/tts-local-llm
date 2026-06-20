# Local TTS Workbench Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a reusable local TTS workbench for LM Studio + Orpheus that generates small, editable audio chunks for Reaper.

**Architecture:** The tool separates text preparation from model inference and audio export. Text processors handle pronunciation rules, pause markup, and chunking; the Orpheus path calls LM Studio for tokens, decodes with SNAC, writes WAV chunks, and emits a manifest.

**Tech Stack:** Python 3.10+, `requests`, `numpy`, `torch`, `snac`, `PyYAML`, `ffmpeg`, `pytest`.

---

## File Map

- `src/local_tts/pronunciation.py`: ordered pronunciation substitution rules.
- `src/local_tts/pause_markup.py`: parse `[[pause:500]]` markers into typed segments.
- `src/local_tts/chunker.py`: split parsed segments into small generation chunks.
- `src/local_tts/manifest.py`: write JSONL manifests for Reaper/provenance.
- `src/local_tts/lmstudio_client.py`: LM Studio completions client.
- `src/local_tts/orpheus_decoder.py`: Orpheus custom-token parsing and SNAC WAV decode.
- `src/local_tts/audio_export.py`: silence WAV generation and ffmpeg normalization helpers.
- `src/local_tts/cli.py`: command-line interface.
- `tests/`: test text preparation and manifest behavior without needing LM Studio.
- `docs/`: setup, workflow, pronunciation, Reaper, and troubleshooting documentation.

## Tasks

- [x] Create project skeleton and implementation plan.
- [x] Add failing tests for pronunciation, pause markup, chunking, and manifest output.
- [x] Implement text-processing modules until tests pass.
- [x] Add LM Studio client and Orpheus decoder from the proven initial Orpheus experiment.
- [x] Add CLI and config example.
- [x] Add detailed docs.
- [x] Initialize git locally and verify no generated audio, venvs, caches, or local config are tracked.
- [x] Run tests and CLI help as final verification.

## Verification Notes

- Text test suite: `8 passed`.
- CLI help: verified for root and `generate`.
- Dry run: verified pronunciation replacement, pause chunking, chunk text output, and manifest output.
- LM Studio check: verified `/v1/models` returns `orpheus-3b-0.1-ft`.
- Audio smoke test: verified one real Tara WAV chunk generated through LM Studio using the existing audio-capable venv.
