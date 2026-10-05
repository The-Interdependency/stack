"""Eight-circle / two-circle positional degeneration candidate.

This module implements only the geometry and byte-expansion candidate now specified
for Weave:

* one byte is eight bits;
* one whole + seven derived circles form the full eight-circle key-set state;
* every circle uses an exact 720-degree return represented as rational turns in [0, 2);
* each circle's relation to space is key-set data, not a universal law;
* a degenerate public key exposes exactly two circles from the eight;
* each plaintext bit produces one public sheet bit per exposed circle, so one byte
  produces sixteen transmitted bits.

The construction is deliberately labelled a candidate. The public two-circle map is
small enough to brute-force per bit, and the tests preserve that attack witness. A
message-coupled UCHC origin/axis relation is therefore still required before this can
support an asymmetric-security claim.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Iterable


TURN_720 = Fraction(2, 1)


def _phase(value: Fraction) -> Fraction:
    if type(value) is not Fraction:
        raise TypeError("circle positions must be exact fractions")
    return value % TURN_720


def _bit(value: int) -> int:
    if type(value) is not int or value not in (0, 1):
        raise TypeError("bit must be integer 0 or 1")
    return value


@dataclass(frozen=True)
class Circle:
    """One exact 720-degree circle instance from a concrete key set."""

    identity: str
    space: Fraction
    zero: Fraction
    one: Fraction

    def __post_init__(self):
        if type(self.identity) is not str or not self.identity:
            raise ValueError("circle identity required")
        object.__setattr__(self, "space", _phase(self.space))
        object.__setattr__(self, "zero", _phase(self.zero))
        object.__setattr__(self, "one", _phase(self.one))
        if self.zero == self.one:
            raise ValueError("zero and one positions must remain distinct")

    def position(self, bit: int, origin: Fraction) -> Fraction:
        """Exact key-set position relative to this circle's space attachment."""
        _bit(bit)
        return _phase((self.one if bit else self.zero) - self.space + _phase(origin))

    def public_sheet(self, bit: int, origin: Fraction) -> int:
        """Degenerate 720->two-sheet witness: first or second visible 360-degree return."""
        return 0 if self.position(bit, origin) < 1 else 1


@dataclass(frozen=True)
class FullKeySet:
    """Full/private construction instance: exactly eight circles."""

    circles: tuple[Circle, ...]

    def __post_init__(self):
        if type(self.circles) is not tuple or len(self.circles) != 8:
            raise ValueError("full key set requires exactly eight circles")
        if any(type(circle) is not Circle for circle in self.circles):
            raise TypeError("full key set members must be Circle instances")
        identities = tuple(circle.identity for circle in self.circles)
        if len(set(identities)) != 8:
            raise ValueError("circle identities must be unique")

    def degenerate(self, left: int, right: int) -> "PublicPair":
        if any(type(i) is not int or not 0 <= i < 8 for i in (left, right)):
            raise ValueError("public circle indices must be integers in [0, 7]")
        if left == right:
            raise ValueError("degeneration requires two distinct circles")
        return PublicPair((left, right), (self.circles[left], self.circles[right]))


@dataclass(frozen=True)
class PublicPair:
    """Exactly two circles exposed by one public degeneration."""

    indices: tuple[int, int]
    circles: tuple[Circle, Circle]

    def __post_init__(self):
        if (type(self.indices) is not tuple or len(self.indices) != 2
                or len(set(self.indices)) != 2):
            raise ValueError("public degeneration requires exactly two distinct indices")
        if type(self.circles) is not tuple or len(self.circles) != 2:
            raise ValueError("public degeneration exposes exactly two circles")
        if any(type(circle) is not Circle for circle in self.circles):
            raise TypeError("public circles must be Circle instances")

    def witness(self, bit: int, origin: Fraction) -> tuple[int, int]:
        _bit(bit)
        return tuple(circle.public_sheet(bit, origin) for circle in self.circles)


def encode_byte(public: PublicPair, value: int, origin: Fraction) -> tuple[int, ...]:
    """Encode one byte as sixteen public positional witness bits."""
    if type(public) is not PublicPair:
        raise TypeError("two-circle public key required")
    if type(value) is not int or not 0 <= value <= 255:
        raise ValueError("value must be one byte")
    out: list[int] = []
    for shift in range(7, -1, -1):
        bit = (value >> shift) & 1
        zero = public.witness(0, origin)
        one = public.witness(1, origin)
        if zero == one:
            raise ValueError("two-circle degeneration is ambiguous at this origin")
        out.extend(public.witness(bit, origin))
    return tuple(out)


def decode_byte(full: FullKeySet, public_indices: tuple[int, int],
                witness: Iterable[int], origin: Fraction) -> int:
    """Recover one byte with the full key-set object.

    Current candidate recovery consults the same selected circles. This is intentional:
    the accompanying attack test demonstrates that this baseline does not yet require
    the six hidden circles and therefore cannot establish the intended asymmetric
    property.
    """
    if type(full) is not FullKeySet:
        raise TypeError("full eight-circle key set required")
    if type(public_indices) is not tuple or len(public_indices) != 2:
        raise ValueError("exactly two public indices required")
    public = full.degenerate(*public_indices)
    bits = tuple(witness)
    if len(bits) != 16 or any(type(bit) is not int or bit not in (0, 1) for bit in bits):
        raise ValueError("byte witness must contain exactly sixteen integer bits")

    value = 0
    zero = public.witness(0, origin)
    one = public.witness(1, origin)
    if zero == one:
        raise ValueError("two-circle degeneration is ambiguous at this origin")
    for offset in range(0, 16, 2):
        pair = bits[offset:offset + 2]
        if pair == zero:
            bit = 0
        elif pair == one:
            bit = 1
        else:
            raise ValueError("witness is not admitted by this key-set projection")
        value = (value << 1) | bit
    return value


def encode(data: bytes, public: PublicPair, origin: Fraction) -> tuple[int, ...]:
    """Raw bytes -> exactly twice as many transmitted bits as source bits."""
    if type(data) is not bytes:
        raise TypeError("raw bytes required")
    return tuple(bit for byte in data for bit in encode_byte(public, byte, origin))


def decode(full: FullKeySet, public_indices: tuple[int, int],
           witness: Iterable[int], origin: Fraction) -> bytes:
    bits = tuple(witness)
    if len(bits) % 16:
        raise ValueError("ciphertext witness length must be a multiple of sixteen bits")
    return bytes(decode_byte(full, public_indices, bits[i:i + 16], origin)
                 for i in range(0, len(bits), 16))
