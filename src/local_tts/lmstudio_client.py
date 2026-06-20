from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import requests


DEFAULT_BASE_URL = "http://127.0.0.1:1234/v1"
DEFAULT_MODEL = "orpheus-3b-0.1-ft"


@dataclass(frozen=True)
class GenerationSettings:
    max_tokens: int = 2600
    temperature: float = 0.6
    top_p: float = 0.9
    repeat_penalty: float = 1.1
    timeout: int = 240


class LMStudioClient:
    def __init__(self, base_url: str = DEFAULT_BASE_URL, model: str = DEFAULT_MODEL) -> None:
        self.base_url = base_url.rstrip("/")
        self.model = model

    def list_models(self, timeout: int = 5) -> dict[str, Any]:
        response = requests.get(f"{self.base_url}/models", timeout=timeout)
        response.raise_for_status()
        return response.json()

    def complete(self, prompt: str, settings: GenerationSettings) -> str:
        payload = {
            "model": self.model,
            "prompt": prompt,
            "max_tokens": settings.max_tokens,
            "temperature": settings.temperature,
            "top_p": settings.top_p,
            "repeat_penalty": settings.repeat_penalty,
            "stream": False,
        }
        response = requests.post(
            f"{self.base_url}/completions",
            json=payload,
            timeout=settings.timeout,
        )
        response.raise_for_status()
        data = response.json()
        try:
            return data["choices"][0]["text"]
        except (KeyError, IndexError, TypeError) as exc:
            raise RuntimeError(f"Unexpected LM Studio response: {data!r}") from exc
