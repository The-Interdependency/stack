"""Public/private setup boundary; no substitute key generator.

Usage: call keygen(explicit_native_law, private_gonol, material, randomness).
The explicit law owns the mathematical public/private relation (Q2, Q7, Q8).
No network, persistence, private-key logging or conventional crypto fallback.
"""
from dataclasses import dataclass, field
from typing import Any, Callable
from .api import Blocked


@dataclass(frozen=True)
class KeyPair:
    public: Any = field(repr=False)
    private: Any = field(repr=False)
    law_identity: str


def keygen(law: Callable[..., KeyPair] | None, *, private_gonol: Any,
           material: Any, randomness: bytes, enabled: bool = True) -> KeyPair | None:
    if type(enabled) is not bool:
        raise TypeError("key switch must be Boolean")
    if not enabled:
        return None
    if law is None:
        raise Blocked('key: Q2/Q7/Q8 require an actual native KeyGen relation')
    result = law(private_gonol=private_gonol, material=material, randomness=randomness)
    if (not isinstance(result, KeyPair) or type(result.law_identity) is not str
            or not result.law_identity.strip()):
        raise TypeError('KeyGen must return a source-identified KeyPair')
    if result.public is None or result.private is None:
        raise ValueError('KeyGen returned an absent key side')
    return result
