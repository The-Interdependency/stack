# === MODULE_BUILD ===
# id: ucns_native_mobius_geometry
#   module_name: direct_mobius
#   module_kind: geometry
#   summary: exact framed Mobius root-loop quotient with 360-degree visible return and 720-degree complete return
#   owner: Erin Spencer
#   public_surface: StructuralNullIdentity, STRUCTURAL_NULL_ORIGIN, NativeMobiusFrame, NativeMobiusState, native_mobius_state
#   internal_surface: _coerce_turns
#   auth_boundary: none
#   storage_boundary: immutable exact rational state only
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: tests.test_direct_mobius
#   rollout: geometry-only UCNS root-loop primitive
#   rollback: restore the prior mixed experiment module from Git history
#   requires: none
#   since: 2026-08-20
#   unresolved: attachment to higher-dimensional circle, epicycle, disk, sphere, and full gonol constructions
# === END MODULE_BUILD ===

# === CONTRACTS ===
# id: native_mobius_one_turn_reverses_frame
#   given: any framed Mobius state advances one full visible turn
#   then: visible phase is unchanged and local frame is reversed
#   class: correctness
#   since: 2026-08-20
#
# id: native_mobius_two_turns_restore_complete_state
#   given: any framed Mobius state advances two full visible turns
#   then: phase and local frame both return exactly
#   class: correctness
#   since: 2026-08-20
#
# id: native_mobius_motion_is_exactly_invertible
#   given: an exact rational turn displacement is applied and then negated
#   then: the complete framed state is restored exactly
#   class: correctness
#   since: 2026-08-20
# === END CONTRACTS ===

"""Pure framed Möbius root-loop geometry.

The quotient is

    (t, ε) ~ (t + n, (-1)^n ε)

with exact rational turns ``t`` and integer windings ``n``.  One visible turn
returns to the same phase with reversed local frame; two visible turns restore
the complete state.  This module contains no corpus, lexical, EDCM, PTCNA,
evaluator, or source-admission semantics.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from enum import Enum
from fractions import Fraction

NATIVE_MOBIUS_LAW_ID = "ucns.native-mobius-root-loop"
NATIVE_MOBIUS_LAW_VERSION = "1.0.0"
STRUCTURAL_NULL_ORIGIN_ID = "ucns.structural-null-origin"


class DirectMobiusError(ValueError):
    """Raised when a requested state is outside the exact framed quotient."""


@dataclass(frozen=True, slots=True)
class StructuralNullIdentity:
    """Singular coordinate origin; not an ordinary scalar-zero state."""

    origin_id: str = STRUCTURAL_NULL_ORIGIN_ID
    carrier_position: int = 0

    def __post_init__(self) -> None:
        if self.origin_id != STRUCTURAL_NULL_ORIGIN_ID or self.carrier_position != 0:
            raise DirectMobiusError("Structural Null origin is fixed")


STRUCTURAL_NULL_ORIGIN = StructuralNullIdentity()


class NativeMobiusFrame(str, Enum):
    POSITIVE = "positive-local-frame"
    REVERSED = "reversed-local-frame"

    @property
    def sign(self) -> int:
        return 1 if self is NativeMobiusFrame.POSITIVE else -1

    def flipped(self) -> "NativeMobiusFrame":
        return NativeMobiusFrame.REVERSED if self is NativeMobiusFrame.POSITIVE else NativeMobiusFrame.POSITIVE


def _coerce_turns(value: Fraction | int) -> Fraction:
    if isinstance(value, bool):
        raise DirectMobiusError("turn motion cannot be boolean")
    if isinstance(value, int):
        return Fraction(value)
    if not isinstance(value, Fraction):
        raise DirectMobiusError("turn motion must be an int or exact Fraction")
    return value


@dataclass(frozen=True, slots=True)
class NativeMobiusState:
    """Canonical representative of the framed Möbius quotient."""

    phase_turns: Fraction = Fraction(0)
    frame: NativeMobiusFrame = NativeMobiusFrame.POSITIVE

    def __post_init__(self) -> None:
        if not isinstance(self.phase_turns, Fraction):
            raise DirectMobiusError("phase_turns must be an exact Fraction")
        if not Fraction(0) <= self.phase_turns < Fraction(1):
            raise DirectMobiusError("canonical phase_turns must lie in [0, 1)")
        if not isinstance(self.frame, NativeMobiusFrame):
            raise DirectMobiusError("frame must be a NativeMobiusFrame")

    def advance(self, turns: Fraction | int) -> "NativeMobiusState":
        displacement = _coerce_turns(turns)
        total = self.phase_turns + displacement
        whole_turns = total.numerator // total.denominator
        phase = total - whole_turns
        frame = self.frame.flipped() if whole_turns % 2 else self.frame
        return replace(self, phase_turns=phase, frame=frame)

    @property
    def visible_key(self) -> tuple[str, Fraction]:
        return (NATIVE_MOBIUS_LAW_ID, self.phase_turns)

    @property
    def complete_key(self) -> tuple[str, Fraction, NativeMobiusFrame]:
        return (NATIVE_MOBIUS_LAW_ID, self.phase_turns, self.frame)


def native_mobius_state(
    turns: Fraction | int = 0,
    frame: NativeMobiusFrame = NativeMobiusFrame.POSITIVE,
) -> NativeMobiusState:
    """Construct a canonical state by exact motion from phase zero."""

    return NativeMobiusState(Fraction(0), frame).advance(turns)


__all__ = [
    "DirectMobiusError",
    "NATIVE_MOBIUS_LAW_ID",
    "NATIVE_MOBIUS_LAW_VERSION",
    "NativeMobiusFrame",
    "NativeMobiusState",
    "STRUCTURAL_NULL_ORIGIN",
    "STRUCTURAL_NULL_ORIGIN_ID",
    "StructuralNullIdentity",
    "native_mobius_state",
]
