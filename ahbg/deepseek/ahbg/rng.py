"""DeepSeek AHBG realization — deterministic randomness.

Independent implementation: a counter-mode SHA-256 stream. For a given
``(seed, domain, counter)`` the output is a pure function, so named substreams
(war, prompt-injection, dm) are stable and replayable without sharing state.
"""

from __future__ import annotations

import hashlib

WAR_DOMAIN = "war"
PROMPT_INJECTION_DOMAIN = "prompt-injection"
DM_DOMAIN = "dm"


class DeterministicRng:
    """Counter-mode SHA-256 random stream with named domains."""

    def __init__(self, seed: int, domain: str = "") -> None:
        if isinstance(seed, bool) or not isinstance(seed, int) or seed < 0:
            raise ValueError("rng seed must be a non-negative integer")
        if not isinstance(domain, str):
            raise ValueError("rng domain must be a string")
        self._seed = seed
        self._domain = domain
        self._counter = 0

    @property
    def seed(self) -> int:
        return self._seed

    @property
    def domain(self) -> str:
        return self._domain

    def _digest(self, counter: int) -> bytes:
        payload = f"{self._seed}:{self._domain}:{counter}".encode("utf-8")
        return hashlib.sha256(payload).digest()

    def next_u64(self) -> int:
        value = int.from_bytes(self._digest(self._counter)[:8], "big")
        self._counter += 1
        return value

    def randbelow(self, n: int) -> int:
        if isinstance(n, bool) or not isinstance(n, int) or n <= 0:
            raise ValueError("randbelow bound must be a positive integer")
        limit = (1 << 64) % n
        while True:
            value = self.next_u64()
            if value >= limit:
                return value % n

    def choice(self, seq):
        if not seq:
            raise ValueError("choice requires a non-empty sequence")
        return seq[self.randbelow(len(seq))]

    def substream(self, domain: str) -> "DeterministicRng":
        if not isinstance(domain, str) or not domain:
            raise ValueError("substream domain must be non-empty text")
        child_domain = f"{self._domain}/{domain}" if self._domain else domain
        return DeterministicRng(seed=self._seed, domain=child_domain)
