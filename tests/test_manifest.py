import json

from local_tts.manifest import ManifestEntry, write_manifest_jsonl


def test_write_manifest_jsonl_records_chunk_metadata(tmp_path):
    path = tmp_path / "manifest.jsonl"
    entries = [
        ManifestEntry(
            index=1,
            kind="text",
            voice="tara",
            text="Hello.",
            output_file="chunk_001.wav",
            duration_seconds=1.25,
            source_file="story.txt",
        ),
        ManifestEntry(
            index=2,
            kind="pause",
            voice="tara",
            text="",
            output_file="chunk_002_pause.wav",
            duration_seconds=0.5,
            source_file="story.txt",
            pause_milliseconds=500,
        ),
    ]

    write_manifest_jsonl(path, entries)

    lines = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]
    assert lines[0]["output_file"] == "chunk_001.wav"
    assert lines[1]["pause_milliseconds"] == 500
