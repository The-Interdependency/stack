"""Deterministic pulse stream. SHA-256 of seed:domain:index. Not splitmix64."""

from __future__ import annotations

import hashlib


def pulse(seed: int, domain: str, index: int) -> int:
    raw = hashlib.sha256(f"grok-ahbg:{seed}:{domain}:{index}".encode("utf-8")).digest()
    return int.from_bytes(raw[:8], "big")
