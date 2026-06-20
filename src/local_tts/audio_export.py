from __future__ import annotations

import subprocess
import wave
from pathlib import Path


SAMPLE_RATE = 24000


def write_silence_wav(path: Path, milliseconds: int, sample_rate: int = SAMPLE_RATE) -> float:
    if milliseconds < 0:
        raise ValueError("milliseconds must be non-negative")
    frames = int(sample_rate * (milliseconds / 1000.0))
    path.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(path), "wb") as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(b"\x00\x00" * frames)
    return frames / float(sample_rate)


def wav_duration_seconds(path: Path) -> float:
    with wave.open(str(path), "rb") as wav_file:
        return wav_file.getnframes() / float(wav_file.getframerate())


def normalize_to_mp3(input_path: Path, output_path: Path, loudnorm: str = "I=-18:LRA=11:TP=-1.5") -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-hide_banner",
            "-loglevel",
            "error",
            "-i",
            str(input_path),
            "-af",
            f"loudnorm={loudnorm}",
            "-codec:a",
            "libmp3lame",
            "-b:a",
            "128k",
            str(output_path),
        ],
        check=True,
    )
