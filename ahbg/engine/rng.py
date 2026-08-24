"""Deterministic randomness for AHBG.

The engine uses an explicit splitmix64 stream so a run is replayable across
Python versions and processes. Named substreams cover the randomness the
README calls out: War, tile prompt-injection rolls, and DM events. The DM may
stay deterministic/seeded for the first implementation; those seeds come from
here.
"""

from __future__ import annotations

import hashlib

from .errors import ValidationError

WAR_DOMAIN = "war"
PROMPT_INJECTION_DOMAIN = "prompt-injection"
DM_DOMAIN = "dm"

_MASK64 = (1 << 64) - 1
_SPLITMIX_MAGIC = 0x9E3779B97F4A7C15
_MIX1 = 0xBF58476D1CE4E5B9
_MIX2 = 0x94D049BB133111EB


def _seed_to_state(seed: int, domain: str) -> int:
    """Derive a 64-bit splitmix state from (seed, domain).

    Hashing the string form keeps derivation stable for arbitrary non-negative
    integer seeds and makes substreams pure functions of their parent seed.
    """
    payload = f"{seed}:{domain}".encode("utf-8")
    digest = hashlib.sha256(payload).digest()
    return int.from_bytes(digest[:8], "big")


def _splitmix64(state: int) -> tuple[int, int]:
    """Return ``(value, next_state)`` for one splitmix64 step."""
    next_state = (state + _SPLITMIX_MAGIC) & _MASK64
    z = next_state
    z = ((z ^ (z >> 30)) * _MIX1) & _MASK64
    z = ((z ^ (z >> 27)) * _MIX2) & _MASK64
    value = (z ^ (z >> 31)) & _MASK64
    return value, next_state


class RngStream:
    """A deterministic 64-bit random stream with named substreams."""

    def __init__(self, seed: int, domain: str = "") -> None:
        if not isinstance(seed, int) or isinstance(seed, bool) or seed < 0:
            raise ValidationError("rng seed must be a non-negative integer")
        if not isinstance(domain, str):
            raise ValidationError("rng domain must be a string")
        self._seed = seed
        self._domain = domain
        self._state = _seed_to_state(seed, domain)

    @property
    def seed(self) -> int:
        return self._seed

    @property
    def domain(self) -> str:
        return self._domain

    def next_u64(self) -> int:
        value, self._state = _splitmix64(self._state)
        return value

    def randbelow(self, n: int) -> int:
        """Uniform integer in ``[0, n)`` without modulo bias."""
        if not isinstance(n, int) or isinstance(n, bool) or n <= 0:
            raise ValidationError("randbelow bound must be a positive integer")
        limit = (-n) % n
        while True:
            value = self.next_u64()
            if value >= limit:
                return value % n

    def choice(self, seq):
        if not seq:
            raise ValidationError("choice requires a non-empty sequence")
        return seq[self.randbelow(len(seq))]

    def substream(self, domain: str) -> "RngStream":
        """Deterministic child stream for a named concern.

        ``rng.substream("war")`` always yields the same child sequence for a
        given parent seed, independent of how many draws the parent has made.
        """
        if not isinstance(domain, str) or not domain:
            raise ValidationError("substream domain must be a non-empty string")
        child_domain = f"{self._domain}/{domain}" if self._domain else domain
        return RngStream(seed=self._seed, domain=child_domain)
