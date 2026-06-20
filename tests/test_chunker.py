from local_tts.chunker import chunk_segments
from local_tts.pause_markup import PauseSegment, TextSegment


def test_chunk_segments_splits_text_by_word_budget():
    segments = [
        TextSegment(text="one two three four five"),
        TextSegment(text="six seven"),
    ]

    chunks = chunk_segments(segments, max_words=5)

    assert [chunk.text for chunk in chunks] == ["one two three four five", "six seven"]


def test_chunk_segments_preserves_pause_as_own_chunk():
    segments = [
        TextSegment(text="one two"),
        PauseSegment(milliseconds=500),
        TextSegment(text="three four"),
    ]

    chunks = chunk_segments(segments, max_words=10)

    assert chunks[0].text == "one two"
    assert chunks[1].pause_milliseconds == 500
    assert chunks[2].text == "three four"
