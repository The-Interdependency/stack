"""Declared dimensional arity.

Dimension tells where. Arity tells what intersects at once.

Ambient dimension count and coupling arity are independent. Geometry is
generated only from explicitly declared couplings. Overlapping lower-arity
couplings do not create a higher-arity coupling.

Domain claims (provisional, this candidate):

- surface_form: dimension
  term_id: epac.dimensional.dimension
  claiming_domain: epac candidate
  claimed_sense: an independent coordinate axis in a declared ambient space
  excluded: coupling arity; participant count; x/y/z as the general model

- surface_form: arity
  term_id: epac.dimensional.arity
  claiming_domain: epac candidate
  claimed_sense: number of dimensions participating in one declared coupling
  excluded: ambient dimension count; gonol participant-count policies
            (edcm.gonol arity_policy is a different sense)

- surface_form: coupling
  term_id: epac.dimensional.coupling
  claiming_domain: epac candidate
  claimed_sense: one explicit intersection of exactly k declared dimensions
  excluded: the power set of ambient dimensions; inferred closures

Collision: edcm.gonol ScaleOptionSet.arity_policy counts closed gonol
participants, not dimensional intersections. Resolution: different term ids.

hmmm: whether a coupling is intrinsically unordered ({x,z} = {z,x}) or may
carry orientation (zx ≠ xz) is undeclared. This module stores the declared
sequence as declaration identity only. It does not quotient by permutation
and does not treat order as geometric orientation.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Mapping, Sequence


class DimensionalArityError(ValueError):
    """Fail-closed dimensional arity error."""


@dataclass(frozen=True, slots=True)
class Dimension:
    """One independent coordinate axis."""

    id: str

    def __post_init__(self) -> None:
        if not isinstance(self.id, str) or not self.id or self.id.isspace():
            raise DimensionalArityError("dimension id must be exact non-empty text")


@dataclass(frozen=True, slots=True)
class Coupling:
    """One explicitly declared intersection of dimensions."""

    dimensions: tuple[Dimension, ...]

    def __post_init__(self) -> None:
        if not self.dimensions:
            raise DimensionalArityError("a coupling must declare at least one dimension")
        ids = [dimension.id for dimension in self.dimensions]
        if len(ids) != len(set(ids)):
            raise DimensionalArityError("a coupling cannot repeat a dimension")

    @property
    def arity(self) -> int:
        return len(self.dimensions)

    @property
    def declared_ids(self) -> tuple[str, ...]:
        return tuple(dimension.id for dimension in self.dimensions)

    @property
    def member_ids(self) -> frozenset[str]:
        """Membership view only. Not geometric identity."""

        return frozenset(self.declared_ids)


@dataclass(frozen=True, slots=True)
class DimensionalSpace:
    """Ambient axes plus only those couplings that were declared."""

    ambient_dimensions: tuple[Dimension, ...]
    couplings: tuple[Coupling, ...]

    def __post_init__(self) -> None:
        ambient_ids = [dimension.id for dimension in self.ambient_dimensions]
        if len(ambient_ids) != len(set(ambient_ids)):
            raise DimensionalArityError("ambient dimensions must be unique")
        ambient = set(ambient_ids)
        for coupling in self.couplings:
            missing = [item for item in coupling.declared_ids if item not in ambient]
            if missing:
                raise DimensionalArityError(
                    f"coupling {coupling.declared_ids} uses undeclared dimensions {tuple(missing)}"
                )


def dimension(id: str) -> Dimension:
    return Dimension(id)


def coupling(dimension_ids: Sequence[str]) -> Coupling:
    if not isinstance(dimension_ids, Sequence) or isinstance(dimension_ids, (str, bytes)):
        raise DimensionalArityError("coupling dimensions must be an ordered declaration sequence")
    return Coupling(tuple(Dimension(item) for item in dimension_ids))


def space(
    ambient_ids: Sequence[str],
    coupling_declarations: Sequence[Sequence[str]] = (),
) -> DimensionalSpace:
    if not isinstance(ambient_ids, Sequence) or isinstance(ambient_ids, (str, bytes)):
        raise DimensionalArityError("ambient dimensions must be a declared sequence")
    declared = tuple(coupling(item) for item in coupling_declarations)
    return DimensionalSpace(
        ambient_dimensions=tuple(Dimension(item) for item in ambient_ids),
        couplings=declared,
    )


def observed_shared_ids(left: Coupling, right: Coupling) -> frozenset[str]:
    """Shared members of two declarations. This is not a new coupling."""

    return left.member_ids & right.member_ids


def geometry_from_declared_couplings(declared: DimensionalSpace) -> Mapping[str, object]:
    """Geometry is the declared couplings, not the power set of ambient axes."""

    return {
        "ambient_ids": tuple(item.id for item in declared.ambient_dimensions),
        "ambient_count": len(declared.ambient_dimensions),
        "couplings": tuple(
            {
                "declared_ids": coupling.declared_ids,
                "arity": coupling.arity,
            }
            for coupling in declared.couplings
        ),
        "arity_counts": _arity_counts(declared.couplings),
        "observed_shares": tuple(_share_records(declared.couplings)),
        "inferred_from_ambient": False,
        "inferred_higher_arity_from_overlap": False,
        "order_identity": "hmmm",
    }


def _arity_counts(couplings: tuple[Coupling, ...]) -> tuple[tuple[int, int], ...]:
    counts: dict[int, int] = {}
    for item in couplings:
        counts[item.arity] = counts.get(item.arity, 0) + 1
    return tuple(sorted(counts.items()))


def _share_records(couplings: tuple[Coupling, ...]) -> Iterable[Mapping[str, object]]:
    for i, left in enumerate(couplings):
        for j, right in enumerate(couplings):
            if j <= i:
                continue
            shared = observed_shared_ids(left, right)
            if shared:
                yield {
                    "left": left.declared_ids,
                    "right": right.declared_ids,
                    "shared_ids": tuple(sorted(shared)),
                    "creates_higher_arity_coupling": False,
                }


def has_declared_coupling(declared: DimensionalSpace, dimension_ids: Sequence[str]) -> bool:
    """True only if this exact declaration sequence is present.

    Permuted declarations are not treated as the same or as different geometry.
    """

    target = tuple(dimension_ids)
    return any(item.declared_ids == target for item in declared.couplings)


__all__ = [
    "Coupling",
    "Dimension",
    "DimensionalArityError",
    "DimensionalSpace",
    "coupling",
    "dimension",
    "geometry_from_declared_couplings",
    "has_declared_coupling",
    "observed_shared_ids",
    "space",
]
