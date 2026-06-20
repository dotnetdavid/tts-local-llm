from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Mapping


@dataclass(frozen=True)
class PronunciationRule:
    source: str
    replacement: str


def load_pronunciation_rules(rows: Iterable[Mapping[str, str]]) -> list[PronunciationRule]:
    rules: list[PronunciationRule] = []
    for row in rows:
        source = row.get("source", "").strip()
        replacement = row.get("replacement", "").strip()
        if not source:
            raise ValueError("Pronunciation rule is missing a source phrase")
        if not replacement:
            raise ValueError(f"Pronunciation rule for {source!r} is missing a replacement")
        rules.append(PronunciationRule(source=source, replacement=replacement))
    return rules


def apply_pronunciations(text: str, rules: Iterable[PronunciationRule]) -> str:
    rendered = text
    for rule in rules:
        rendered = rendered.replace(rule.source, rule.replacement)
    return rendered
