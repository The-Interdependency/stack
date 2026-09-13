# ratios: loc_comments=204:82 imports_exports=4:5 calls_definitions=92:10
# === MODULE_BUILD ===
# id: ucns_modular_orbit_geometry
#   module_name: modular_orbit
#   module_kind: instrument
#   summary: exact finite modular-action orbit decomposition and normalized circle embedding candidate
#   owner: Erin Spencer
#   public_surface: ModularOrbitError, CircularResiduePosition, ModularOrbitGeometry, build_modular_orbit_geometry
#   internal_surface: residue validation, permutation closure audit, deterministic cycle traversal
#   auth_boundary: none
#   storage_boundary: none
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: tests/test_modular_orbit.py
#   rollout: executable candidate geometry; downstream domains may test the representation, but UCNS selection/ratification remains unresolved
#   rollback: remove this module, facade exports, tests, and documentation
#   since: 2026-09-05
#   unresolved: candidate ratification; exact composition with the native Mobius carrier and higher-dimensional UCNS construction remains hmmm
# === END MODULE_BUILD ===

# === CONTRACTS ===
# id: modular_orbit_action_decomposes_exact_permutation
#   given: modulus m > 1, multiplier a, and a nonempty declared residue carrier on which x -> a*x mod m is a permutation
#   then: the action is recorded exactly and decomposed into deterministic disjoint cycles covering every declared position once, with periods equal to cycle lengths
#   class: correctness
#   since: 2026-09-05
#
# id: modular_orbit_circle_embedding_is_exact
#   given: a valid modular orbit geometry
#   then: every residue r is embedded on the normalized circle at exactly r/m turns using Fraction, with no floating-point or trigonometric approximation in the core representation
#   class: correctness
#   since: 2026-09-05
#
# id: modular_orbit_fails_closed_outside_permutation_boundary
#   given: malformed residues, an empty carrier, a carrier not closed under the action, a non-bijective action, or an inconsistent direct record construction
#   then: construction raises ModularOrbitError rather than inventing an orbit decomposition or accepting contradictory geometry
#   class: safety
#   since: 2026-09-05
#
# id: modular_orbit_carries_geometry_not_domain_semantics
#   given: a modular orbit geometry is serialized or consumed
#   then: it exposes only modulus, multiplier, declared positions, action edges, cycles, periods, and exact circle turns; prime, Fibonacci, PCEA, EPAC, and physical interpretations are absent
#   class: doctrine
#   since: 2026-09-05
#
# id: modular_orbit_remains_candidate_until_ratified
#   given: the executable modular orbit representation exists without a declared falsifier/replay/ratification receipt selecting it as UCNS geometry
#   then: repository standing remains candidate rather than active selected UCNS canon
#   class: doctrine
#   since: 2026-09-06
# === END CONTRACTS ===

"""Exact finite modular-action orbit geometry candidate.

UCNS owns the candidate representation only: declared residue positions, the
exact multiplication action ``x -> a*x (mod m)``, its cycle decomposition,
periods, and exact normalized circle positions. The executable mathematics is
exact within its declared inputs; selection of this representation as active
UCNS geometry still requires its own falsifier/replay/ratification evidence.

Usage::

    geometry = build_modular_orbit_geometry(
        modulus=9,
        multiplier=2,
        positions=range(1, 9),
    )
    assert geometry.orbits == ((1, 2, 4, 8, 7, 5), (3, 6))

Canonical residues are always ``0 <= r < modulus``. Display aliases such as
showing residue 0 as the digit ``9`` in a mod-9 diagram belong to a renderer,
not to this geometry primitive. Domain meanings also stay outside this module.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Iterable


class ModularOrbitError(ValueError):
    """Raised when a declared modular carrier cannot support cycle geometry."""


@dataclass(frozen=True, slots=True)
class CircularResiduePosition:
    """Exact normalized-circle placement of one canonical residue."""

    residue: int
    turn: Fraction

    def __post_init__(self) -> None:
        if isinstance(self.residue, bool) or not isinstance(self.residue, int):
            raise ModularOrbitError("embedding residue must be an integer")
        if not isinstance(self.turn, Fraction) or not 0 <= self.turn < 1:
            raise ModularOrbitError("embedding turn must be an exact Fraction in [0, 1)")


@dataclass(frozen=True, slots=True)
class ModularOrbitGeometry:
    """Immutable exact geometry of one finite modular multiplication action.

    Restore records with nested tuples and nonboolean integers; numeric equality
    to an integer is not sufficient admission. Use the builder for iterables.
    """

    modulus: int
    multiplier: int
    positions: tuple[int, ...]
    action: tuple[tuple[int, int], ...]
    orbits: tuple[tuple[int, ...], ...]
    periods: tuple[int, ...]
    embedding: tuple[CircularResiduePosition, ...]

    def __post_init__(self) -> None:
        for name in ("positions", "action", "orbits", "periods", "embedding"):
            if not isinstance(getattr(self, name), tuple):
                raise ModularOrbitError(f"{name} must be an immutable tuple")
        for name in ("action", "orbits"):
            for row in getattr(self, name):
                if not isinstance(row, tuple) or not row:
                    raise ModularOrbitError(f"{name} must contain nonempty immutable tuples")
                if name == "action" and len(row) != 2:
                    raise ModularOrbitError("action entries must be source/target pairs")
                if any(isinstance(value, bool) or not isinstance(value, int) for value in row):
                    raise ModularOrbitError(f"{name} must contain nonboolean integer residues")
        if any(isinstance(value, bool) or not isinstance(value, int) for value in self.periods):
            raise ModularOrbitError("periods must be nonboolean integers")
        if isinstance(self.modulus, bool) or not isinstance(self.modulus, int) or self.modulus <= 1:
            raise ModularOrbitError("modulus must be an integer greater than 1")
        if isinstance(self.multiplier, bool) or not isinstance(self.multiplier, int):
            raise ModularOrbitError("multiplier must be an integer")
        if self.multiplier != self.multiplier % self.modulus:
            raise ModularOrbitError("multiplier must be its canonical residue modulo modulus")
        if not self.positions:
            raise ModularOrbitError("positions must be nonempty")
        if any(
            isinstance(value, bool)
            or not isinstance(value, int)
            or value < 0
            or value >= self.modulus
            for value in self.positions
        ):
            raise ModularOrbitError("positions contain a noncanonical residue")
        if tuple(sorted(self.positions)) != self.positions or len(set(self.positions)) != len(self.positions):
            raise ModularOrbitError("positions must be sorted unique canonical residues")

        expected_action = tuple(
            (source, (self.multiplier * source) % self.modulus)
            for source in self.positions
        )
        if self.action != expected_action:
            raise ModularOrbitError("action does not match x -> multiplier*x mod modulus")

        targets = tuple(target for _, target in self.action)
        if set(targets) != set(self.positions) or len(set(targets)) != len(self.positions):
            raise ModularOrbitError("action is not a permutation of the declared positions")

        flattened = tuple(value for orbit in self.orbits for value in orbit)
        if set(flattened) != set(self.positions) or len(flattened) != len(self.positions):
            raise ModularOrbitError("orbits must cover every declared position exactly once")
        if any(not orbit for orbit in self.orbits):
            raise ModularOrbitError("orbits must be nonempty")
        if tuple(orbit[0] for orbit in self.orbits) != tuple(
            sorted(orbit[0] for orbit in self.orbits)
        ):
            raise ModularOrbitError("orbits must be ordered by their canonical start")
        action_map = dict(self.action)
        for orbit in self.orbits:
            if orbit[0] != min(orbit):
                raise ModularOrbitError("each orbit must start at its least residue")
            successors = orbit[1:] + orbit[:1]
            if any(action_map[source] != target for source, target in zip(orbit, successors)):
                raise ModularOrbitError("orbit order does not follow the declared action")

        if self.periods != tuple(len(orbit) for orbit in self.orbits):
            raise ModularOrbitError("periods must equal orbit lengths")

        expected_embedding = tuple(
            CircularResiduePosition(residue=residue, turn=Fraction(residue, self.modulus))
            for residue in self.positions
        )
        if self.embedding != expected_embedding:
            raise ModularOrbitError("embedding must place residue r at exactly r/modulus turns")

    def target(self, residue: int) -> int:
        """Return the exact action target for a declared position."""

        if isinstance(residue, bool) or not isinstance(residue, int):
            raise ModularOrbitError("residue must be a nonboolean integer")
        for source, target in self.action:
            if source == residue:
                return target
        raise ModularOrbitError(f"residue {residue!r} is not in this carrier")

    def turn_of(self, residue: int) -> Fraction:
        """Return the exact normalized-circle turn for a declared position."""

        if isinstance(residue, bool) or not isinstance(residue, int):
            raise ModularOrbitError("residue must be a nonboolean integer")
        for position in self.embedding:
            if position.residue == residue:
                return position.turn
        raise ModularOrbitError(f"residue {residue!r} is not in this carrier")

    def as_dict(self) -> dict[str, object]:
        """Serialize without adding renderer or downstream-domain semantics."""

        return {
            "modulus": self.modulus,
            "multiplier": self.multiplier,
            "positions": list(self.positions),
            "action": [[source, target] for source, target in self.action],
            "orbits": [list(orbit) for orbit in self.orbits],
            "periods": list(self.periods),
            "embedding": [
                {
                    "residue": position.residue,
                    "turn": {
                        "numerator": position.turn.numerator,
                        "denominator": position.turn.denominator,
                    },
                }
                for position in self.embedding
            ],
        }


def _canonical_positions(modulus: int, positions: Iterable[int] | None) -> tuple[int, ...]:
    if positions is None:
        return tuple(range(modulus))

    raw = tuple(positions)
    if not raw:
        raise ModularOrbitError("positions must be nonempty")
    if any(isinstance(value, bool) or not isinstance(value, int) for value in raw):
        raise ModularOrbitError("positions must contain integers only")
    if any(value < 0 or value >= modulus for value in raw):
        raise ModularOrbitError(
            f"positions must be canonical residues in [0, {modulus - 1}]"
        )
    if len(set(raw)) != len(raw):
        raise ModularOrbitError("positions must not contain duplicate residues")
    return tuple(sorted(raw))


def build_modular_orbit_geometry(
    modulus: int,
    multiplier: int,
    positions: Iterable[int] | None = None,
) -> ModularOrbitGeometry:
    """Build exact cycle and circle geometry for ``x -> multiplier*x mod modulus``.

    The declared position carrier must be invariant under the action and the
    action must be bijective on that finite carrier. This fail-closed boundary
    is what makes ``orbits`` a disjoint cycle decomposition rather than a
    functional graph with transient trees.
    """

    if isinstance(modulus, bool) or not isinstance(modulus, int) or modulus <= 1:
        raise ModularOrbitError("modulus must be an integer greater than 1")
    if isinstance(multiplier, bool) or not isinstance(multiplier, int):
        raise ModularOrbitError("multiplier must be an integer")

    resolved_positions = _canonical_positions(modulus, positions)
    resolved_multiplier = multiplier % modulus
    position_set = set(resolved_positions)

    action_map = {
        source: (resolved_multiplier * source) % modulus
        for source in resolved_positions
    }

    outside = tuple(
        (source, target)
        for source, target in action_map.items()
        if target not in position_set
    )
    if outside:
        source, target = outside[0]
        raise ModularOrbitError(
            "positions are not closed under the modular action: "
            f"{source} maps to {target}"
        )

    if len(set(action_map.values())) != len(resolved_positions):
        raise ModularOrbitError(
            "modular action must be bijective on the declared positions"
        )

    unseen = set(resolved_positions)
    orbits: list[tuple[int, ...]] = []
    for start in resolved_positions:
        if start not in unseen:
            continue
        orbit: list[int] = []
        current = start
        while current in unseen:
            unseen.remove(current)
            orbit.append(current)
            current = action_map[current]
        if current != start:
            raise ModularOrbitError(
                "declared action did not close as a cycle on the carrier"
            )
        orbits.append(tuple(orbit))

    action = tuple((source, action_map[source]) for source in resolved_positions)
    orbit_tuple = tuple(orbits)
    embedding = tuple(
        CircularResiduePosition(residue=residue, turn=Fraction(residue, modulus))
        for residue in resolved_positions
    )

    return ModularOrbitGeometry(
        modulus=modulus,
        multiplier=resolved_multiplier,
        positions=resolved_positions,
        action=action,
        orbits=orbit_tuple,
        periods=tuple(len(orbit) for orbit in orbit_tuple),
        embedding=embedding,
    )


__all__ = [
    "CircularResiduePosition",
    "ModularOrbitError",
    "ModularOrbitGeometry",
    "build_modular_orbit_geometry",
]
# ratios: loc_comments=204:82 imports_exports=4:5 calls_definitions=92:10
