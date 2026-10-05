# === MODULE_BUILD ===
# id: weave_byte_circle_structure
#   module_name: eight_circle
#   module_kind: schema
#   summary: byte-scoped bit placements and whole-plus-one key views, without a substitute cipher
#   owner: Erin Spencer
#   public_surface: Circle, PublicPair, FullKeySet, BitPlacement, ByteConstruction, construct_byte
#   internal_surface: strict input validation
#   auth_boundary: none
#   storage_boundary: none
#   network_boundary: none
#   user_data_boundary: read
#   admin_only: false
#   tests: tests/test_eight_circle.py
#   rollout: replaces the incorrect PR 73 per-bit sheet encoder
#   rollback: revert this repair as one transaction; do not reactivate the rejected cipher
#   unresolved: approved native positional transform and ciphertext serialization
# === END MODULE_BUILD ===
# === CONTRACTS ===
# id: weave_byte_has_eight_circle_placements
#   given: one byte and an explicit bit-to-circle assignment
#   then: each source bit occurs exactly once among G0 through G7
#   class: correctness
# id: weave_public_pair_always_contains_whole
#   given: a full eight-circle key-set record
#   then: every public view is G0 plus exactly one of G1 through G7
#   class: correctness
# id: weave_positions_are_not_bit_codes
#   given: exact key-set and placement coordinates
#   then: their 720-degree coordinates are retained without converting each source bit into two sheet bits
#   class: boundary
# === END CONTRACTS ===
"""Byte structure, not a cipher or a replacement UCNS Gonol constructor.

Usage: construct_byte(0xA5, full, positions, origin_id="message-1", byte_index=0).
The caller supplies eight exact positions and an explicit bit-to-circle assignment.
Positions are data in turns (360 degrees); 720 degrees is the complete return.
No formula deriving positions, native geometry, or ciphertext is invented here.
PublicPair is a key-view boundary, never a two-bit encoding of each source bit.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from fractions import Fraction

TURN_720 = Fraction(2)


def _index(value: int, upper: int, name: str) -> None:
    if type(value) is not int or not 0 <= value < upper:
        raise ValueError(f"{name} must be an integer in [0, {upper - 1}]")


def _identity(value: str) -> None:
    if type(value) is not str or not value.strip():
        raise ValueError("a nonempty identity is required")


def _phase(value: Fraction) -> Fraction:
    if type(value) is not Fraction:
        raise TypeError("positions must be exact Fraction values")
    return value % TURN_720


def _assignment(values: tuple[int, ...]) -> None:
    if type(values) is not tuple or len(values) != 8:
        raise ValueError("an explicit eight-member assignment is required")
    for value in values:
        _index(value, 8, "assignment member")
    if set(values) != set(range(8)):
        raise ValueError("every source bit and circle must occur exactly once")


@dataclass(frozen=True)
class Circle:
    """Key-set circle binding; index 0 is the whole, indices 1..7 are parts.

    This stores the circle's exact space coordinate, not its complete native
    space relation. A scalar offset does not implement that relation.
    """
    index: int
    identity: str
    space: Fraction = field(repr=False)

    def __post_init__(self) -> None:
        _index(self.index, 8, "circle index")
        _identity(self.identity)
        object.__setattr__(self, "space", _phase(self.space))


@dataclass(frozen=True)
class PublicPair:
    """Only the whole and one part; no full-key or plaintext reference."""
    circles: tuple[Circle, Circle] = field(repr=False)

    def __post_init__(self) -> None:
        if (type(self.circles) is not tuple or len(self.circles) != 2
                or any(type(c) is not Circle for c in self.circles)):
            raise ValueError("exactly two Circle records are required")
        whole, part = self.circles
        if whole.index != 0 or part.index == 0 or whole.identity == part.identity:
            raise ValueError("public pair must be G0 followed by one distinct small circle")

    @property
    def indices(self) -> tuple[int, int]:
        return self.circles[0].index, self.circles[1].index


@dataclass(frozen=True)
class FullKeySet:
    """Eight circle bindings plus caller-supplied assignment, not KeyGen.

    bit_to_circle[i] locates the source byte's ith bit (MSB first). No default
    assignment, active-part sequence, or private-to-public transform is selected.
    """
    circles: tuple[Circle, ...] = field(repr=False)
    bit_to_circle: tuple[int, ...] = field(repr=False)

    def __post_init__(self) -> None:
        if (type(self.circles) is not tuple or len(self.circles) != 8
                or any(type(c) is not Circle for c in self.circles)):
            raise ValueError("the full record requires exactly eight Circle records")
        if tuple(c.index for c in self.circles) != tuple(range(8)):
            raise ValueError("store the whole first, followed by parts 1 through 7")
        if len({c.identity for c in self.circles}) != 8:
            raise ValueError("circle identities must be distinct")
        _assignment(self.bit_to_circle)

    def degenerate(self, part_index: int) -> PublicPair:
        """Select the established pair shape; this does not derive a trapdoor."""
        _index(part_index, 8, "part index")
        if part_index == 0:
            raise ValueError("select one small circle, not a second whole")
        return PublicPair((self.circles[0], self.circles[part_index]))


@dataclass(frozen=True)
class BitPlacement:
    """One source-bit occurrence assigned to one circle within a byte."""
    source_bit_index: int
    circle_index: int
    bit: int = field(repr=False)
    position: Fraction = field(repr=False)

    def __post_init__(self) -> None:
        _index(self.source_bit_index, 8, "source bit index")
        _index(self.circle_index, 8, "circle index")
        _index(self.bit, 2, "bit")
        object.__setattr__(self, "position", _phase(self.position))


@dataclass(frozen=True)
class ByteConstruction:
    """One byte's eight placements at its message-origin occurrence.

    Source recovery here reads the retained construction. It is NOT decryption.
    The whole carries one bit and remains addressable in every whole-part relation.
    Evolution of its state is not implemented by an invented public-feedback rule.
    """
    origin_id: str
    byte_index: int
    placements: tuple[BitPlacement, ...] = field(repr=False)

    def __post_init__(self) -> None:
        _identity(self.origin_id)
        if type(self.byte_index) is not int or self.byte_index < 0:
            raise ValueError("byte index must be a nonnegative integer")
        if (type(self.placements) is not tuple or len(self.placements) != 8
                or any(type(p) is not BitPlacement for p in self.placements)):
            raise ValueError("one byte requires exactly eight BitPlacement records")
        if tuple(p.circle_index for p in self.placements) != tuple(range(8)):
            raise ValueError("each circle must carry exactly one placement")
        _assignment(tuple(p.source_bit_index for p in self.placements))

    @property
    def source_value(self) -> int:
        return sum(p.bit << (7 - p.source_bit_index) for p in self.placements)


def construct_byte(value: int, full: FullKeySet, positions: tuple[Fraction, ...],
                   *, origin_id: str, byte_index: int) -> ByteConstruction:
    """Attach all eight bits together using supplied positions in circle order.

    Caller-supplied data is not an approved transform. This function emits a
    plaintext-bearing construction record, never ciphertext or a public packet.
    """
    _index(value, 256, "byte")
    if type(full) is not FullKeySet:
        raise TypeError("a full key-set record is required")
    if type(positions) is not tuple or len(positions) != 8:
        raise ValueError("supply all eight circle positions for the byte")
    phases = tuple(_phase(p) for p in positions)
    by_circle = sorted(
        (circle_index, source_index)
        for source_index, circle_index in enumerate(full.bit_to_circle)
    )
    placements = tuple(
        BitPlacement(source_index, circle_index, (value >> (7 - source_index)) & 1,
                     phases[circle_index])
        for circle_index, source_index in by_circle
    )
    return ByteConstruction(origin_id, byte_index, placements)
