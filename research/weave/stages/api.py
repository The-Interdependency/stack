"""Typed operator contracts, not cryptographic constructions.

Usage: supply explicit Operator(forward, inverse, identity) instances to Pipeline.
No network or storage. Native payloads pass unchanged except through selected operators.
Roll back by removing this assembly; no producer code is changed.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any, Callable, Mapping


class Blocked(RuntimeError):
    """An enabled law/input is missing; execution must not silently bypass it."""


@dataclass(frozen=True)
class PublicContext:
    public_key: Any = field(repr=False)
    parameters: Mapping[str, Any] = field(default_factory=dict, repr=False)
    randomness: bytes = field(default=b'', repr=False)
    public_material: Mapping[str, bytes] = field(default_factory=dict, repr=False)

    def __post_init__(self):
        object.__setattr__(self, 'parameters', MappingProxyType(dict(self.parameters)))
        object.__setattr__(self, 'public_material', MappingProxyType(dict(self.public_material)))


@dataclass(frozen=True)
class PrivateContext:
    public_key: Any = field(repr=False)
    private_key: Any = field(repr=False)
    parameters: Mapping[str, Any] = field(default_factory=dict, repr=False)
    private_material: Mapping[str, bytes] = field(default_factory=dict, repr=False)
    public_material: Mapping[str, bytes] = field(default_factory=dict, repr=False)
    randomness: bytes = field(default=b'', repr=False)

    def __post_init__(self):
        object.__setattr__(self, 'parameters', MappingProxyType(dict(self.parameters)))
        object.__setattr__(self, 'private_material', MappingProxyType(dict(self.private_material)))
        object.__setattr__(self, 'public_material', MappingProxyType(dict(self.public_material)))


@dataclass(frozen=True)
class Streams:
    """Exact bit streams; not a gonol, key or native thread-generation law."""
    lanes: tuple[tuple[int, ...], ...] = field(repr=False)

    def __post_init__(self):
        if type(self.lanes) is not tuple or not self.lanes:
            raise TypeError('lanes must be a nonempty tuple')
        if any(type(lane) is not tuple for lane in self.lanes):
            raise TypeError('each lane must be an immutable tuple')
        if any(type(bit) is not int or bit not in (0, 1)
               for lane in self.lanes for bit in lane):
            raise TypeError('each bit must be integer 0 or 1, not bool/coerced data')


@dataclass(frozen=True)
class Operator:
    """A real transformation pair plus provenance; fixture is never full evidence."""
    forward: Callable[[Any, PublicContext], Any] = field(repr=False)
    inverse: Callable[[Any, PrivateContext], Any] = field(repr=False)
    identity: str
    fixture: bool = False

    def __post_init__(self):
        if not callable(self.forward) or not callable(self.inverse):
            raise TypeError('both operator directions must be callable')
        if type(self.identity) is not str or not self.identity.strip():
            raise ValueError('an explicit law/source identity is required')
        if type(self.fixture) is not bool:
            raise TypeError('fixture flag must be Boolean')


@dataclass(frozen=True)
class Step:
    name: str
    questions: tuple[str, ...]
    purpose: str
    required: bool = True
    builtin: Operator | None = None


@dataclass(frozen=True)
class Transition:
    """A stage may pass derived working parameters to later stages, not ciphertext.

    This preserves coupled, message-dependent constructions. The inverse key law
    must independently make whatever reverse parameters are needed available.
    Updates are not copied into receipts and do not supply a missing private law.
    """
    payload: Any = field(repr=False)
    parameters: Mapping[str, Any] = field(default_factory=dict, repr=False)
