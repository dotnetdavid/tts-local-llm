from __future__ import annotations

import re
import wave
from dataclasses import dataclass
from pathlib import Path

from local_tts.lmstudio_client import GenerationSettings, LMStudioClient


SAMPLE_RATE = 24000
CUSTOM_TOKEN_RE = re.compile(r"<custom_token_(\d+)>")


def prompt_for_voice(text: str, voice: str) -> str:
    clean = " ".join(text.split())
    return f"<|audio|>{voice}: {clean}<|eot_id|>"


def token_ids_from_text(token_text: str) -> list[int]:
    ids: list[int] = []
    frame_index = 0
    for match in CUSTOM_TOKEN_RE.finditer(token_text):
        raw_id = int(match.group(1))
        token_id = raw_id - 10 - ((frame_index % 7) * 4096)
        if token_id > 0:
            ids.append(token_id)
            frame_index += 1
    return ids


def write_wav(path: Path, pcm: bytes, sample_rate: int = SAMPLE_RATE) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(path), "wb") as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(pcm)


def _load_snac_model():
    try:
        import torch
        from snac import SNAC
    except ImportError as exc:
        raise RuntimeError(
            "Audio dependencies are not installed. Install with `pip install -e .[audio]` "
            "or install CPU-only torch plus snac as documented."
        ) from exc

    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = SNAC.from_pretrained("hubertsiuzdak/snac_24khz").eval().to(device)
    return model, device, torch


def _decode_window(model, device: str, torch_module, multiframe: list[int]) -> bytes | None:
    import numpy as np

    if len(multiframe) < 7:
        return None

    num_frames = len(multiframe) // 7
    frame = multiframe[: num_frames * 7]
    codes_0: list[int] = []
    codes_1: list[int] = []
    codes_2: list[int] = []

    for j in range(num_frames):
        i = 7 * j
        codes_0.append(frame[i])
        codes_1.extend([frame[i + 1], frame[i + 4]])
        codes_2.extend([frame[i + 2], frame[i + 3], frame[i + 5], frame[i + 6]])

    code_tensors = [
        torch_module.tensor(codes_0, device=device, dtype=torch_module.int32).unsqueeze(0),
        torch_module.tensor(codes_1, device=device, dtype=torch_module.int32).unsqueeze(0),
        torch_module.tensor(codes_2, device=device, dtype=torch_module.int32).unsqueeze(0),
    ]

    for tensor in code_tensors:
        if torch_module.any(tensor < 0) or torch_module.any(tensor > 4096):
            return None

    with torch_module.inference_mode():
        audio_hat = model.decode(code_tensors)
        audio_slice = audio_hat[:, :, 2048:4096].detach().cpu().numpy()

    audio_int16 = np.clip(audio_slice * 32767, -32768, 32767).astype(np.int16)
    return audio_int16.tobytes()


def decode_tokens_to_pcm(model, device: str, torch_module, token_ids: list[int]) -> bytes:
    chunks: list[bytes] = []
    usable_count = 0
    buffer: list[int] = []

    for token_id in token_ids:
        buffer.append(token_id)
        usable_count += 1
        if usable_count % 7 == 0 and usable_count > 27:
            audio = _decode_window(model, device, torch_module, buffer[-28:])
            if audio:
                chunks.append(audio)

    return b"".join(chunks)


@dataclass
class OrpheusSynthesizer:
    client: LMStudioClient
    settings: GenerationSettings

    def __post_init__(self) -> None:
        self._snac_model = None
        self._snac_device = None
        self._torch = None

    def _ensure_decoder(self) -> None:
        if self._snac_model is None:
            self._snac_model, self._snac_device, self._torch = _load_snac_model()

    def synthesize_to_wav(self, text: str, voice: str, output_path: Path) -> float:
        self._ensure_decoder()
        token_text = self.client.complete(prompt_for_voice(text, voice), self.settings)
        token_ids = token_ids_from_text(token_text)
        pcm = decode_tokens_to_pcm(self._snac_model, self._snac_device, self._torch, token_ids)
        if not pcm:
            raise RuntimeError(f"No audio decoded for voice {voice}; token count={len(token_ids)}")
        write_wav(output_path, pcm)
        return len(pcm) / (SAMPLE_RATE * 2)
