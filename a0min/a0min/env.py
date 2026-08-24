# ratios: loc_comments=53:15 imports_exports=4:4 calls_definitions=15:6
"""Minimal provider-key loader for a0min.

Reads provider API keys from a local ``.env`` file without hardcoding them and
without ever emitting key values.

When an explicit path is given, only that file is read. Otherwise the search
order is ``./.env`` (current working directory) then ``~/.env`` (user home),
first match wins per provider.

Supported provider keys: ``OPENAI_API_KEY``, ``DEEPSEEK_API_KEY``,
``XAI_API_KEY``. Raw key material is returned only to in-process callers on
request; summaries expose presence only.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Mapping

PROVIDER_KEY_NAMES = ("OPENAI_API_KEY", "DEEPSEEK_API_KEY", "XAI_API_KEY")

_PROVIDER_BY_KEY = {
    "OPENAI_API_KEY": "openai",
    "DEEPSEEK_API_KEY": "deepseek",
    "XAI_API_KEY": "xai",
}

_PROVIDER_ORDER = ("openai", "deepseek", "xai")


def _parse_env_file(path: Path) -> dict[str, str]:
    """Parse KEY=VALUE lines from a .env file; never logs values."""
    values: dict[str, str] = {}
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        values[key.strip()] = value.strip().strip('"').strip("'")
    return values


def _candidate_paths(
    explicit: str | os.PathLike[str] | None = None,
) -> list[Path]:
    if explicit:
        return [Path(explicit)]
    return [Path.cwd() / ".env", Path.home() / ".env"]


def load_provider_keys(
    explicit: str | os.PathLike[str] | None = None,
) -> dict[str, str]:
    """Return ``provider -> key`` for every supported key found."""
    found: dict[str, str] = {}
    for path in _candidate_paths(explicit):
        if not path.is_file():
            continue
        for key, value in _parse_env_file(path).items():
            provider = _PROVIDER_BY_KEY.get(key)
            if provider and value and provider not in found:
                found[provider] = value
    return found


def provider_key(
    provider: str,
    explicit: str | os.PathLike[str] | None = None,
) -> str | None:
    """Return one provider key, or None when not configured."""
    return load_provider_keys(explicit).get(provider)


def available_providers(
    explicit: str | os.PathLike[str] | None = None,
) -> tuple[str, ...]:
    """Configured provider names in stable order."""
    found = load_provider_keys(explicit)
    return tuple(provider for provider in _PROVIDER_ORDER if provider in found)


def presence(
    explicit: str | os.PathLike[str] | None = None,
) -> Mapping[str, bool]:
    """Presence map for every supported provider; values never contain keys."""
    found = load_provider_keys(explicit)
    return {provider: provider in found for provider in _PROVIDER_ORDER}
# ratios: loc_comments=53:15 imports_exports=4:4 calls_definitions=15:6
