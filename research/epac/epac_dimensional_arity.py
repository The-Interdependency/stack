"""Declared dimensional arity, orientation, and degree.

Dimension tells where. Arity tells what intersects at once. Degree tells how
a dimension is incident on declared couplings.

``(z, x)`` is not ``(x, z)``. Shared members of ``(x, z)`` and ``(y, z)`` do
not yield ``(x, y, z)`` without an explicit proof. Overlap is not a proof.

Domain claims (provisional):

- dimension: independent coordinate axis
- arity: number of dimensions in one declared coupling
- degree: incidence of one dimension on declared couplings, including slot
- coupling: ordered declaration of participating dimensions

Collision: edcm.gonol arity_policy counts gonol participants, not dimensional
intersections.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Mapping, Sequence


FORBIDDEN_INFERENCE_RULES = frozenset(
    {
        "ambient-power-set",
        "overlap-closure",
        "permutation-identity",
        "shared-dimension-join",
    }
)


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
    """One explicitly declared ordered intersection of dimensions."""

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


@dataclass(frozen=True, slots=True)
class DegreeRelation:
    """How one dimension sits in declared couplings.

    degree is the number of incidences. slot_degrees counts incidences at each
    ordered position. (z,x) puts z in slot 0; (x,z) puts z in slot 1.
    """

    dimension: Dimension
    incidences: tuple[tuple[tuple[str, ...], int], ...]

    @property
    def degree(self) -> int:
        return len(self.incidences)

    @property
    def slot_degrees(self) -> tuple[tuple[int, int], ...]:
        counts: dict[int, int] = {}
        for _declared, slot in self.incidences:
            counts[slot] = counts.get(slot, 0) + 1
        return tuple(sorted(counts.items()))


@dataclass(frozen=True, slots=True)
class CouplingProof:
    """Certificate required before a higher-arity coupling may be installed."""

    conclusion: Coupling
    premises: tuple[Coupling, ...]
    rule_id: str

    def __post_init__(self) -> None:
        if not isinstance(self.rule_id, str) or not self.rule_id or self.rule_id.isspace():
            raise DimensionalArityError("a coupling proof must declare a non-empty rule_id")
        if self.rule_id in FORBIDDEN_INFERENCE_RULES:
            raise DimensionalArityError(
                f"rule {self.rule_id!r} is not a proof; overlap/permutation/ambient fill are forbidden"
            )
        if not self.premises:
            raise DimensionalArityError("a coupling proof must cite at least one premise coupling")


@dataclass(frozen=True, slots=True)
class DimensionalSpace:
    """Ambient axes, declared couplings, degree relations, and optional proofs."""

    ambient_dimensions: tuple[Dimension, ...]
    couplings: tuple[Coupling, ...]
    proofs: tuple[CouplingProof, ...] = ()

    def __post_init__(self) -> None:
        ambient_ids = [dimension.id for dimension in self.ambient_dimensions]
        if len(ambient_ids) != len(set(ambient_ids)):
            raise DimensionalArityError("ambient dimensions must be unique")
        ambient = set(ambient_ids)
        for item in self.couplings:
            missing = [name for name in item.declared_ids if name not in ambient]
            if missing:
                raise DimensionalArityError(
                    f"coupling {item.declared_ids} uses undeclared dimensions {tuple(missing)}"
                )
        declared = {item.declared_ids for item in self.couplings}
        for proof in self.proofs:
            for premise in proof.premises:
                if premise.declared_ids not in declared:
                    raise DimensionalArityError(
                        f"proof {proof.rule_id!r} cites missing premise {premise.declared_ids}"
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
    proofs: Sequence[CouplingProof] = (),
) -> DimensionalSpace:
    if not isinstance(ambient_ids, Sequence) or isinstance(ambient_ids, (str, bytes)):
        raise DimensionalArityError("ambient dimensions must be a declared sequence")
    declared = tuple(coupling(item) for item in coupling_declarations)
    return DimensionalSpace(
        ambient_dimensions=tuple(Dimension(item) for item in ambient_ids),
        couplings=declared,
        proofs=tuple(proofs),
    )


def degree_relations(declared: DimensionalSpace) -> tuple[DegreeRelation, ...]:
    incidences: dict[str, list[tuple[tuple[str, ...], int]]] = {
        item.id: [] for item in declared.ambient_dimensions
    }
    for item in declared.couplings:
        for slot, axis in enumerate(item.dimensions):
            incidences[axis.id].append((item.declared_ids, slot))
    return tuple(
        DegreeRelation(dimension=axis, incidences=tuple(incidences[axis.id]))
        for axis in declared.ambient_dimensions
    )


def observed_common_ids(left: Coupling, right: Coupling) -> frozenset[str]:
    """Common dimension ids. Not a coupling and not a proof."""

    return frozenset(left.declared_ids) & frozenset(right.declared_ids)


def has_declared_coupling(declared: DimensionalSpace, dimension_ids: Sequence[str]) -> bool:
    target = tuple(dimension_ids)
    return any(item.declared_ids == target for item in declared.couplings)


def install_proven_coupling(declared: DimensionalSpace, proof: CouplingProof) -> DimensionalSpace:
    """Add a coupling only with an explicit non-forbidden proof."""

    if proof.conclusion.declared_ids in {item.declared_ids for item in declared.couplings}:
        return DimensionalSpace(
            ambient_dimensions=declared.ambient_dimensions,
            couplings=declared.couplings,
            proofs=declared.proofs + (proof,),
        )
    missing = [
        name
        for name in proof.conclusion.declared_ids
        if name not in {axis.id for axis in declared.ambient_dimensions}
    ]
    if missing:
        raise DimensionalArityError(
            f"proven coupling {proof.conclusion.declared_ids} uses undeclared dimensions {tuple(missing)}"
        )
    declared_ids = {item.declared_ids for item in declared.couplings}
    for premise in proof.premises:
        if premise.declared_ids not in declared_ids:
            raise DimensionalArityError(
                f"proof {proof.rule_id!r} cites missing premise {premise.declared_ids}"
            )
    return DimensionalSpace(
        ambient_dimensions=declared.ambient_dimensions,
        couplings=declared.couplings + (proof.conclusion,),
        proofs=declared.proofs + (proof,),
    )


def geometry_from_declared_couplings(declared: DimensionalSpace) -> Mapping[str, object]:
    degrees = degree_relations(declared)
    return {
        "ambient_ids": tuple(item.id for item in declared.ambient_dimensions),
        "ambient_count": len(declared.ambient_dimensions),
        "couplings": tuple(
            {
                "declared_ids": item.declared_ids,
                "arity": item.arity,
            }
            for item in declared.couplings
        ),
        "arity_counts": _arity_counts(declared.couplings),
        "degree_relations": tuple(
            {
                "dimension": item.dimension.id,
                "degree": item.degree,
                "slot_degrees": item.slot_degrees,
                "incidences": item.incidences,
            }
            for item in degrees
        ),
        "observed_common_ids": tuple(_common_records(declared.couplings)),
        "proofs": tuple(
            {
                "rule_id": proof.rule_id,
                "premises": tuple(item.declared_ids for item in proof.premises),
                "conclusion": proof.conclusion.declared_ids,
            }
            for proof in declared.proofs
        ),
        "inferred_from_ambient": False,
        "inferred_higher_arity_from_overlap": False,
        "zx_equals_xz": False,
    }


def _arity_counts(couplings: tuple[Coupling, ...]) -> tuple[tuple[int, int], ...]:
    counts: dict[int, int] = {}
    for item in couplings:
        counts[item.arity] = counts.get(item.arity, 0) + 1
    return tuple(sorted(counts.items()))


def _common_records(couplings: tuple[Coupling, ...]) -> Iterable[Mapping[str, object]]:
    for i, left in enumerate(couplings):
        for j, right in enumerate(couplings):
            if j <= i:
                continue
            shared = observed_common_ids(left, right)
            if shared:
                yield {
                    "left": left.declared_ids,
                    "right": right.declared_ids,
                    "common_ids": tuple(sorted(shared)),
                    "proof_of_higher_arity": False,
                }


__all__ = [
    "Coupling",
    "CouplingProof",
    "DegreeRelation",
    "Dimension",
    "DimensionalArityError",
    "DimensionalSpace",
    "FORBIDDEN_INFERENCE_RULES",
    "coupling",
    "degree_relations",
    "dimension",
    "geometry_from_declared_couplings",
    "has_declared_coupling",
    "install_proven_coupling",
    "observed_common_ids",
    "space",
]
