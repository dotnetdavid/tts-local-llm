from __future__ import annotations

import re
from dataclasses import dataclass


PAUSE_RE = re.compile(r"\[\[pause:(\d+)\]\]")
PAUSE_LIKE_RE = re.compile(r"\[\[pause:[^\]]+\]\]")


@dataclass(frozen=True)
class TextSegment:
    text: str


@dataclass(frozen=True)
class PauseSegment:
    milliseconds: int


Segment = TextSegment | PauseSegment


def parse_pause_markup(text: str) -> list[Segment]:
    invalid = PAUSE_LIKE_RE.search(text)
    if invalid and not PAUSE_RE.fullmatch(invalid.group(0)):
        raise ValueError(f"Invalid pause marker: {invalid.group(0)}")

    segments: list[Segment] = []
    cursor = 0
    for match in PAUSE_RE.finditer(text):
        before = text[cursor : match.start()].strip()
        if before:
            segments.append(TextSegment(text=before))
        segments.append(PauseSegment(milliseconds=int(match.group(1))))
        cursor = match.end()

    after = text[cursor:].strip()
    if after:
        segments.append(TextSegment(text=after))
    return segments
