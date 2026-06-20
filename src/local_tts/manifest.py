from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class ManifestEntry:
    index: int
    kind: str
    voice: str
    text: str
    output_file: str
    duration_seconds: float
    source_file: str
    pause_milliseconds: int | None = None


def write_manifest_jsonl(path: Path, entries: list[ManifestEntry]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for entry in entries:
            handle.write(json.dumps(asdict(entry), ensure_ascii=False) + "\n")
