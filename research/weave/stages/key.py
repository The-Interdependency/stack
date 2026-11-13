"""Public/private setup boundary; no substitute key generator.

Usage: call keygen(explicit_native_law, private_gonol, material, randomness).
The explicit law owns the mathematical public/private relation (Q2, Q7, Q8).
No network, persistence, private-key logging or conventional crypto fallback.
"""
from dataclasses import dataclass, field
from typing import Any, Callable
from .api import Blocked, PublicContext, PrivateContext


@dataclass(frozen=True)
class PublicKey:
    """Public-side declaration only; contains no private key reference."""
    value: Any = field(repr=False)
    law_identity: str
    relation_identity: str
    fixture: bool = False


@dataclass(frozen=True)
class PrivateKey:
    value: Any = field(repr=False)
    law_identity: str
    relation_identity: str
    fixture: bool = False


@dataclass(frozen=True)
class KeyPair:
    public: Any = field(repr=False)
    private: Any = field(repr=False)
    law_identity: str
    relation_identity: str
    fixture: bool = False

    def __post_init__(self):
        if any(type(x) is not str or not x.strip()
               for x in (self.law_identity, self.relation_identity)):
            raise ValueError('KeyPair requires law and relation identities')
        if self.public is None or self.private is None:
            raise ValueError('KeyPair requires both key sides')
        if type(self.fixture) is not bool:
            raise TypeError('key fixture flag must be Boolean')

    def public_context(self, **kwargs):
        """Export only the public side; identities are declarations, not proofs."""
        return PublicContext(PublicKey(self.public, self.law_identity,
                                      self.relation_identity, self.fixture), **kwargs)

    def private_context(self, **kwargs):
        return PrivateContext(self.public_context().public_key,
                              PrivateKey(self.private, self.law_identity,
                                         self.relation_identity, self.fixture), **kwargs)


def relation(context):
    """Validate the exported pair boundary before any data operator executes."""
    public = getattr(context, 'public_key', None)
    if (type(public) is not PublicKey or public.value is None
            or any(type(x) is not str or not x.strip()
                   for x in (public.law_identity, public.relation_identity))
            or type(public.fixture) is not bool):
        raise Blocked('key: source-identified KeyPair public relation required')
    identity = (public.law_identity, public.relation_identity, public.fixture)
    if type(context) is PrivateContext:
        private = context.private_key
        if (type(private) is not PrivateKey or private.value is None
                or type(private.fixture) is not bool
                or (private.law_identity, private.relation_identity, private.fixture) != identity):
            raise Blocked('key: private side must belong to the same declared KeyPair relation')
    return identity


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
