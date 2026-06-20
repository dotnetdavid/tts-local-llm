from __future__ import annotations

from dataclasses import dataclass

from local_tts.pause_markup import PauseSegment, Segment, TextSegment


@dataclass(frozen=True)
class Chunk:
    index: int
    kind: str
    text: str = ""
    pause_milliseconds: int | None = None


def _word_count(text: str) -> int:
    return len(text.split())


def _split_text_to_word_chunks(text: str, max_words: int) -> list[str]:
    words = text.split()
    if len(words) <= max_words:
        return [text.strip()] if text.strip() else []
    return [" ".join(words[i : i + max_words]) for i in range(0, len(words), max_words)]


def chunk_segments(segments: list[Segment], max_words: int) -> list[Chunk]:
    if max_words < 1:
        raise ValueError("max_words must be at least 1")

    chunks: list[Chunk] = []
    pending: list[str] = []
    pending_words = 0

    def flush_pending() -> None:
        nonlocal pending, pending_words
        if pending:
            chunks.append(Chunk(index=len(chunks) + 1, kind="text", text=" ".join(pending)))
            pending = []
            pending_words = 0

    for segment in segments:
        if isinstance(segment, PauseSegment):
            flush_pending()
            chunks.append(
                Chunk(
                    index=len(chunks) + 1,
                    kind="pause",
                    pause_milliseconds=segment.milliseconds,
                )
            )
            continue

        for text_piece in _split_text_to_word_chunks(segment.text, max_words):
            piece_words = _word_count(text_piece)
            if pending and pending_words + piece_words > max_words:
                flush_pending()
            pending.append(text_piece)
            pending_words += piece_words
            if pending_words >= max_words:
                flush_pending()

    flush_pending()
    return chunks
