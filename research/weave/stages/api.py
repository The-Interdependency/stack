"""Operator contracts; native objects retain their owners and identities.

Usage: supply source-identified Operator instances to assembly.Pipeline. A transport
candidate cannot earn a whole-Weave classification. Contexts are in-memory inputs,
not ciphertext headers. No network, storage or key generation occurs here.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any, Callable, Mapping


class Blocked(RuntimeError):
    """An enabled operation or required input is unresolved."""


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
    """Exact bit lanes, not a replacement gonol or secret-sharing construction."""
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
    forward: Callable[[Any, PublicContext], Any] = field(repr=False)
    inverse: Callable[[Any, PrivateContext], Any] = field(repr=False)
    identity: str
    fixture: bool = False
    scope: str = 'native'

    def __post_init__(self):
        if not callable(self.forward) or not callable(self.inverse):
            raise TypeError('both operator directions must be callable')
        if type(self.identity) is not str or not self.identity.strip():
            raise ValueError('an explicit law/source identity is required')
        if type(self.fixture) is not bool:
            raise TypeError('fixture flag must be Boolean')
        if self.scope not in ('native', 'transport'):
            raise ValueError('operator scope must be native or transport')


@dataclass(frozen=True)
class Step:
    name: str
    questions: tuple[str, ...]
    purpose: str
    required: bool = True
    builtin: Operator | None = None


@dataclass(frozen=True)
class Transition:
    """Working state only: inverse controls must be reconstructed independently."""
    payload: Any = field(repr=False)
    parameters: Mapping[str, Any] = field(default_factory=dict, repr=False)
