# === MODULE_BUILD ===
# id: weave_message_origin_coupling_candidate
#   module_name: message_origin
#   module_kind: candidate
#   summary: message-scoped UCHC-style origin/axis coupling for the eight-circle/two-circle Weave research construction
#   owner: Erin Spencer
#   public_surface: MessageOrigin, CouplingKey, CoupledWitness, construct_origin, encode, public_recover
#   internal_surface: exact key-set phase recurrence and public attack witness
#   auth_boundary: none
#   storage_boundary: none
#   network_boundary: none
#   user_data_boundary: raw bytes supplied by caller only
#   admin_only: false
#   tests: tests.test_message_origin
#   rollout: bounded Weave research candidate only; not the native asymmetric relation
#   rollback: remove this module and its tests without altering eight_circle.py
#   requires: weave_eight_circle_candidate, UCHC origin/axis architecture
#   since: 2026-10-05
#   unresolved: a trapdoor degeneration/lift relation that makes the six omitted circles necessary for efficient inversion remains hmmm
# === END MODULE_BUILD ===

# === CONTRACTS ===
# id: weave_message_is_origin
#   given: one admitted raw-byte message
#   then: exactly one message origin O_M is constructed and every source-bit occurrence participates as a distinct ordered axis at that origin
#   class: correctness
#
# id: weave_axis_occurrence_identity_preserved
#   given: repeated equal bit values in one message
#   then: their source-bit occurrences remain distinct by admission order
#   class: correctness
#
# id: weave_coupling_is_key_set_data
#   given: two different coupling key sets
#   then: no universal circle/space/origin-step law is inferred from either
#   class: boundary
#
# id: weave_public_attack_is_preserved
#   given: this candidate's public pair and coupling data
#   then: public recovery is executable and tested, so this candidate must not be promoted as asymmetric security
#   class: falsification
# === END CONTRACTS ===

"""Message-scoped origin/axis coupling for Weave research.

Usage:
    origin = construct_origin(raw_bytes)
    coupled = encode(raw_bytes, public_pair, coupling_key)

The module copies the *architecture* already present in UCHC: participants are admitted
as distinct axes at a shared origin by construction order. It does not copy UCHC's
language participants or invent a UCNS cross-origin angle law.

The phase recurrence below is an explicitly bounded Weave candidate. Its stride and
feedback values are concrete key-set data. It exists so the message-origin idea can
fail executable tests rather than remain prose.

Important limitation:
    public_recover() succeeds from the same public information used by encode().
    Therefore message-origin coupling by itself does not create the required asymmetric
    trapdoor. The result is a useful construction/falsification scaffold, not encryption.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Iterable

from .eight_circle import PublicPair, TURN_720, _phase


@dataclass(frozen=True)
class MessageAxis:
    """One raw source-bit occurrence participating at O_M."""

    index: int
    byte_index: int
    bit_index: int

    def __post_init__(self):
        if type(self.index) is not int or self.index < 0:
            raise ValueError("axis index must be a nonnegative integer")
        if type(self.byte_index) is not int or self.byte_index < 0:
            raise ValueError("byte index must be a nonnegative integer")
        if type(self.bit_index) is not int or not 0 <= self.bit_index < 8:
            raise ValueError("bit index must be in [0, 7]")


@dataclass(frozen=True)
class MessageOrigin:
    """One message origin with ordered source-bit axes."""

    identity: str
    byte_length: int
    axes: tuple[MessageAxis, ...]

    def __post_init__(self):
        if self.identity != "O_M":
            raise ValueError("message origin identity must be O_M")
        if type(self.byte_length) is not int or self.byte_length < 0:
            raise ValueError("byte length must be nonnegative")
        if type(self.axes) is not tuple or len(self.axes) != self.byte_length * 8:
            raise ValueError("message origin must contain exactly eight axes per byte")
        if tuple(axis.index for axis in self.axes) != tuple(range(len(self.axes))):
            raise ValueError("message axes must preserve contiguous admission order")


@dataclass(frozen=True)
class CouplingKey:
    """Key-set-specific candidate parameters; no universal rule is asserted."""

    initial_origin: Fraction
    axis_step: Fraction
    feedback_step: Fraction

    def __post_init__(self):
        for name in ("initial_origin", "axis_step", "feedback_step"):
            value = getattr(self, name)
            if type(value) is not Fraction:
                raise TypeError(f"{name} must be an exact Fraction")
            object.__setattr__(self, name, _phase(value))


@dataclass(frozen=True)
class CoupledWitness:
    """Public two-circle witness plus the message-origin axis topology."""

    origin: MessageOrigin
    bits: tuple[int, ...]

    def __post_init__(self):
        if type(self.origin) is not MessageOrigin:
            raise TypeError("origin must be MessageOrigin")
        if type(self.bits) is not tuple or len(self.bits) != len(self.origin.axes) * 2:
            raise ValueError("coupled witness requires two public bits per source-bit axis")
        if any(type(bit) is not int or bit not in (0, 1) for bit in self.bits):
            raise TypeError("witness bits must be integer 0 or 1")


def construct_origin(data: bytes) -> MessageOrigin:
    """Admit raw bytes losslessly as ordered bit-occurrence axes at one O_M."""
    if type(data) is not bytes:
        raise TypeError("raw bytes required")
    axes = tuple(
        MessageAxis(index=byte_index * 8 + bit_index,
                    byte_index=byte_index,
                    bit_index=bit_index)
        for byte_index in range(len(data))
        for bit_index in range(8)
    )
    return MessageOrigin("O_M", len(data), axes)


def _source_bits(data: bytes) -> tuple[int, ...]:
    return tuple((byte >> shift) & 1 for byte in data for shift in range(7, -1, -1))


def _axis_origin(key: CouplingKey, axis: MessageAxis,
                 previous_public_pair: tuple[int, int]) -> Fraction:
    """Bounded candidate: attach each admitted axis to a key-set-specific phase.

    The axis is identified by admission order, matching the UCHC architectural pattern.
    Turning that axis index into a circle phase is *not* asserted as UCNS/UCHC canon;
    it is this candidate's key-set-specific relation and remains replaceable.
    """
    feedback = previous_public_pair[0] + 2 * previous_public_pair[1]
    return _phase(
        key.initial_origin
        + key.axis_step * axis.index
        + key.feedback_step * feedback
    )


def encode(data: bytes, public: PublicPair, key: CouplingKey) -> CoupledWitness:
    """Construct one message-origin trajectory and emit two public bits per source bit."""
    if type(public) is not PublicPair:
        raise TypeError("two-circle public key required")
    if type(key) is not CouplingKey:
        raise TypeError("CouplingKey required")
    origin = construct_origin(data)
    source = _source_bits(data)
    out: list[int] = []
    previous = (0, 0)
    for axis, bit in zip(origin.axes, source):
        phase = _axis_origin(key, axis, previous)
        pair = public.witness(bit, phase)
        zero = public.witness(0, phase)
        one = public.witness(1, phase)
        if zero == one:
            raise ValueError("candidate public degeneration is ambiguous at an admitted axis")
        out.extend(pair)
        previous = pair
    return CoupledWitness(origin, tuple(out))


def public_recover(public: PublicPair, key: CouplingKey,
                   witness: CoupledWitness) -> bytes:
    """Attack witness: recover this candidate using public information only.

    Its existence is a falsification result, not a supported decryption design.
    """
    if type(public) is not PublicPair:
        raise TypeError("two-circle public key required")
    if type(key) is not CouplingKey:
        raise TypeError("CouplingKey required")
    if type(witness) is not CoupledWitness:
        raise TypeError("CoupledWitness required")

    recovered: list[int] = []
    previous = (0, 0)
    for axis in witness.origin.axes:
        offset = axis.index * 2
        observed = witness.bits[offset:offset + 2]
        phase = _axis_origin(key, axis, previous)
        zero = public.witness(0, phase)
        one = public.witness(1, phase)
        if zero == one:
            raise ValueError("candidate public degeneration is ambiguous at an admitted axis")
        if observed == zero:
            recovered.append(0)
        elif observed == one:
            recovered.append(1)
        else:
            raise ValueError("witness is not admitted by this public trajectory")
        previous = observed

    raw = bytearray()
    for offset in range(0, len(recovered), 8):
        value = 0
        for bit in recovered[offset:offset + 8]:
            value = (value << 1) | bit
        raw.append(value)
    return bytes(raw)


def witness_bits(witness: Iterable[int]) -> tuple[int, ...]:
    """Validate a raw witness-bit iterable for callers constructing test fixtures."""
    bits = tuple(witness)
    if any(type(bit) is not int or bit not in (0, 1) for bit in bits):
        raise TypeError("witness bits must be integer 0 or 1")
    return bits
