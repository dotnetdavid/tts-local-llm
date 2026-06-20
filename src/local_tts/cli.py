from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

import yaml

from local_tts.audio_export import write_silence_wav
from local_tts.chunker import Chunk, chunk_segments
from local_tts.lmstudio_client import DEFAULT_BASE_URL, DEFAULT_MODEL, GenerationSettings, LMStudioClient
from local_tts.manifest import ManifestEntry, write_manifest_jsonl
from local_tts.orpheus_decoder import OrpheusSynthesizer
from local_tts.pause_markup import parse_pause_markup
from local_tts.pronunciation import apply_pronunciations, load_pronunciation_rules


def _load_yaml(path: Path | None) -> dict[str, Any]:
    if path is None:
        return {}
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    return data or {}


def _prepare_text(source: Path, config: dict[str, Any]) -> str:
    text = source.read_text(encoding="utf-8")
    rules = load_pronunciation_rules(config.get("pronunciations", []))
    return apply_pronunciations(text, rules)


def _build_settings(args: argparse.Namespace, config: dict[str, Any]) -> GenerationSettings:
    generation = config.get("generation", {})
    return GenerationSettings(
        max_tokens=args.max_tokens or generation.get("max_tokens", 2600),
        temperature=args.temperature if args.temperature is not None else generation.get("temperature", 0.6),
        top_p=args.top_p if args.top_p is not None else generation.get("top_p", 0.9),
        repeat_penalty=(
            args.repeat_penalty if args.repeat_penalty is not None else generation.get("repeat_penalty", 1.1)
        ),
        timeout=args.timeout or generation.get("timeout", 240),
    )


def _client_from_args(args: argparse.Namespace, config: dict[str, Any]) -> LMStudioClient:
    lmstudio = config.get("lmstudio", {})
    base_url = args.base_url or lmstudio.get("base_url", DEFAULT_BASE_URL)
    model = args.model or lmstudio.get("model", DEFAULT_MODEL)
    return LMStudioClient(base_url=base_url, model=model)


def _chunk_output_name(prefix: str, chunk: Chunk) -> str:
    suffix = "pause" if chunk.kind == "pause" else "text"
    return f"{prefix}_{chunk.index:04d}_{suffix}.wav"


def generate(args: argparse.Namespace) -> int:
    config = _load_yaml(args.config)
    output_dir = args.output_dir
    chunks_dir = output_dir / "chunks"
    manifest_path = output_dir / "manifest.jsonl"
    chunks_dir.mkdir(parents=True, exist_ok=True)

    prepared_text = _prepare_text(args.source, config)
    segments = parse_pause_markup(prepared_text)
    chunks = chunk_segments(segments, max_words=args.max_words)

    synthesizer: OrpheusSynthesizer | None = None
    if not args.dry_run:
        synthesizer = OrpheusSynthesizer(
            client=_client_from_args(args, config),
            settings=_build_settings(args, config),
        )

    entries: list[ManifestEntry] = []
    for chunk in chunks:
        text_file = chunks_dir / f"{args.prefix}_{chunk.index:04d}.txt"
        text_file.write_text(chunk.text, encoding="utf-8")

        output_file = _chunk_output_name(args.prefix, chunk)
        output_path = chunks_dir / output_file

        if chunk.kind == "pause":
            duration = (chunk.pause_milliseconds or 0) / 1000.0
            if not args.dry_run:
                duration = write_silence_wav(output_path, chunk.pause_milliseconds or 0)
        else:
            duration = 0.0
            if not args.dry_run:
                assert synthesizer is not None
                duration = synthesizer.synthesize_to_wav(chunk.text, args.voice, output_path)

        entries.append(
            ManifestEntry(
                index=chunk.index,
                kind=chunk.kind,
                voice=args.voice,
                text=chunk.text,
                output_file=str(output_path),
                duration_seconds=duration,
                source_file=str(args.source),
                pause_milliseconds=chunk.pause_milliseconds,
            )
        )
        print(f"{chunk.index:04d} {chunk.kind}: {output_file} ({duration:.2f}s)")

    write_manifest_jsonl(manifest_path, entries)
    print(f"manifest: {manifest_path}")
    if args.dry_run:
        print("dry run: no audio generated")
    return 0


def check_lmstudio(args: argparse.Namespace) -> int:
    config = _load_yaml(args.config)
    client = _client_from_args(args, config)
    data = client.list_models(timeout=args.timeout)
    print(yaml.safe_dump(data, sort_keys=False))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Local LM Studio + Orpheus TTS workbench.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    generate_parser = subparsers.add_parser("generate", help="Generate chunk WAVs and a manifest.")
    generate_parser.add_argument("source", type=Path, help="Input UTF-8 text file.")
    generate_parser.add_argument("--output-dir", type=Path, required=True, help="Output job directory.")
    generate_parser.add_argument("--config", type=Path, help="YAML config file.")
    generate_parser.add_argument("--voice", default="tara")
    generate_parser.add_argument("--prefix", default="chunk")
    generate_parser.add_argument("--max-words", type=int, default=85)
    generate_parser.add_argument("--base-url")
    generate_parser.add_argument("--model")
    generate_parser.add_argument("--max-tokens", type=int)
    generate_parser.add_argument("--temperature", type=float)
    generate_parser.add_argument("--top-p", type=float)
    generate_parser.add_argument("--repeat-penalty", type=float)
    generate_parser.add_argument("--timeout", type=int)
    generate_parser.add_argument("--dry-run", action="store_true", help="Write chunk text and manifest only.")
    generate_parser.set_defaults(func=generate)

    check_parser = subparsers.add_parser("check-lmstudio", help="Check LM Studio /v1/models.")
    check_parser.add_argument("--config", type=Path)
    check_parser.add_argument("--base-url")
    check_parser.add_argument("--model")
    check_parser.add_argument("--timeout", type=int, default=5)
    check_parser.set_defaults(func=check_lmstudio)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
