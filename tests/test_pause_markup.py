import pytest

from local_tts.pause_markup import PauseSegment, TextSegment, parse_pause_markup


def test_parse_pause_markup_splits_text_and_pause_segments():
    segments = parse_pause_markup("First line. [[pause:750]] Second line.")

    assert segments == [
        TextSegment(text="First line."),
        PauseSegment(milliseconds=750),
        TextSegment(text="Second line."),
    ]


def test_parse_pause_markup_keeps_multiple_pauses_in_order():
    segments = parse_pause_markup("A[[pause:250]]B[[pause:1000]]C")

    assert segments == [
        TextSegment(text="A"),
        PauseSegment(milliseconds=250),
        TextSegment(text="B"),
        PauseSegment(milliseconds=1000),
        TextSegment(text="C"),
    ]


def test_parse_pause_markup_rejects_non_numeric_pause():
    with pytest.raises(ValueError, match="Invalid pause marker"):
        parse_pause_markup("A [[pause:slow]] B")
