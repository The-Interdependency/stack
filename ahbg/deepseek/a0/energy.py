"""A0 energy layer — pluggable provider abstraction.

A0 treats an LLM as interchangeable *energy*, never as identity. This module:

- defines a minimal provider spec (name, base URL, key env var, model);
- ships an OpenAI-compatible chat-completions HTTP client using only stdlib;
- registers DeepSeek as the default energy (key read from ``.env`` via
  ``DEEPSEEK_API_KEY``), with OpenAI and xAI as additional examples;
- fails closed to :class:`EnergyUnavailable` when a provider or key is
  missing, so callers always fall back to the deterministic planner.

No API key is ever logged or serialized.
"""

from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Protocol

DEFAULT_ENV_PATH = Path("/home/wayseer_interdependentway_org/.env")


class EnergyUnavailable(RuntimeError):
    """Raised when a requested energy provider or its credential is unavailable."""


@dataclass(frozen=True)
class ProviderSpec:
    """Static description of one energy provider."""

    name: str
    base_url: str
    api_key_env: str
    model: str
    timeout_s: float = 30.0

    def api_key(self) -> str | None:
        value = os.environ.get(self.api_key_env)
        if value:
            return value
        return None


@dataclass(frozen=True)
class EnergyResult:
    """One completed energy call, with real resource observables."""

    ok: bool
    text: str = ""
    prompt_tokens: int = 0
    completion_tokens: int = 0
    latency_ms: float = 0.0
    error: str = ""


class EnergyClient(Protocol):
    """The only interface A0 needs from an energy provider."""

    spec: ProviderSpec

    def complete(self, messages: list[dict[str, str]], max_tokens: int = 256) -> EnergyResult: ...


def load_env(path: Path | None = None) -> None:
    """Load ``.env`` into ``os.environ`` without logging values.

    Idempotent: existing environment variables are never overwritten.
    """
    target = path or DEFAULT_ENV_PATH
    if not target.is_file():
        return
    for raw in target.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


class HttpEnergyClient:
    """OpenAI-compatible chat-completions client (stdlib only)."""

    def __init__(self, spec: ProviderSpec) -> None:
        self.spec = spec

    def complete(self, messages: list[dict[str, str]], max_tokens: int = 256) -> EnergyResult:
        key = self.spec.api_key()
        if not key:
            return EnergyResult(ok=False, error=f"missing API key env {self.spec.api_key_env}")
        payload = {
            "model": self.spec.model,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": 0,
        }
        request = urllib.request.Request(
            f"{self.spec.base_url.rstrip('/')}/chat/completions",
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {key}",
            },
            method="POST",
        )
        started = time.monotonic()
        try:
            with urllib.request.urlopen(request, timeout=self.spec.timeout_s) as response:
                body = json.loads(response.read().decode("utf-8"))
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
            return EnergyResult(
                ok=False,
                latency_ms=(time.monotonic() - started) * 1000.0,
                error=f"{type(exc).__name__}: {exc}",
            )
        latency_ms = (time.monotonic() - started) * 1000.0
        try:
            choice = body["choices"][0]["message"]["content"]
            usage = body.get("usage", {})
            return EnergyResult(
                ok=True,
                text=str(choice),
                prompt_tokens=int(usage.get("prompt_tokens", 0)),
                completion_tokens=int(usage.get("completion_tokens", 0)),
                latency_ms=latency_ms,
            )
        except (KeyError, IndexError, TypeError, ValueError) as exc:
            return EnergyResult(
                ok=False,
                latency_ms=latency_ms,
                error=f"malformed completion response: {type(exc).__name__}: {exc}",
            )


# -- registry ---------------------------------------------------------------

DEEPSEEK_SPEC = ProviderSpec(
    name="deepseek",
    base_url="https://api.deepseek.com",
    api_key_env="DEEPSEEK_API_KEY",
    model="deepseek-chat",
)

OPENAI_SPEC = ProviderSpec(
    name="openai",
    base_url="https://api.openai.com/v1",
    api_key_env="OPENAI_API_KEY",
    model=os.environ.get("A0_OPENAI_MODEL", "gpt-4o-mini"),
)

XAI_SPEC = ProviderSpec(
    name="xai",
    base_url="https://api.x.ai/v1",
    api_key_env="XAI_API_KEY",
    model=os.environ.get("A0_XAI_MODEL", "grok-2-latest"),
)

_REGISTRY: dict[str, ProviderSpec] = {
    DEEPSEEK_SPEC.name: DEEPSEEK_SPEC,
    OPENAI_SPEC.name: OPENAI_SPEC,
    XAI_SPEC.name: XAI_SPEC,
}


def register_provider(spec: ProviderSpec) -> None:
    """Register an arbitrary energy provider at runtime."""
    _REGISTRY[spec.name] = spec


def provider_names() -> tuple[str, ...]:
    return tuple(sorted(_REGISTRY))


def resolve_energy(name: str | None = None, env_path: Path | None = None) -> EnergyClient:
    """Resolve an energy client.

    Defaults to DeepSeek. Loads ``.env`` first so keys are present without
    polluting the environment or logging their values.
    """
    load_env(env_path)
    spec = _REGISTRY.get(name or DEEPSEEK_SPEC.name)
    if spec is None:
        raise EnergyUnavailable(f"unknown energy provider {name!r}; registered: {provider_names()}")
    if not spec.api_key():
        raise EnergyUnavailable(
            f"energy provider {spec.name!r} has no {spec.api_key_env}; set it in .env"
        )
    return HttpEnergyClient(spec)
