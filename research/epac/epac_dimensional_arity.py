"""Declared dimensional arity, orientation, and degree.

Dimension tells where. Arity tells what intersects at once. Degree tells how
a dimension is incident on declared couplings.

``(z, x)`` is not ``(x, z)``. Shared members of ``(x, z)`` and ``(y, z)`` do
not yield ``(x, y, z)`` without an explicit proof. Overlap is not a proof.

Every instance of ``x`` has its own declared ``(z, x_i)``. Every instance of
``y`` has its own declared ``(z, y_j)``. A second occurrence is a second
instance, not a reuse of the first coupling. ``(x_i, z)`` does not satisfy
``(z, x_i)``.

The three-dimensional structure is the combination of declared oriented
couplings, their arity charge states, and degree. That span can involve three
axes through two charged binaries. It is not a ternary coupling.

Domain claims (provisional):

- dimension: independent coordinate axis
- arity: number of dimensions in one declared coupling
- degree: incidence of one dimension on declared couplings, including slot
- coupling: ordered declaration of participating dimensions
- charge state: per-slot charges on a coupling, with Möbius ε at t=0
- instance: occurrence-addressed dimension; each x_i / y_j is distinct

Collision: edcm.gonol arity_policy counts gonol participants, not dimensional
intersections.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Mapping, Sequence


# Established UCNS Möbius frame sign at t=0: ε in (t, ε) ~ (t+n, (-1)^n ε).
MOBIUS_EPSILON_T0 = 1

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
    """One independent coordinate axis, with optional established charge."""

    id: str
    charge: int | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.id, str) or not self.id or self.id.isspace():
            raise DimensionalArityError("dimension id must be exact non-empty text")
        if self.charge is not None and (isinstance(self.charge, bool) or not isinstance(self.charge, int)):
            raise DimensionalArityError("dimension charge must be an int or None")


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

    @property
    def slot_charges(self) -> tuple[int | None, ...]:
        return tuple(dimension.charge for dimension in self.dimensions)

    @property
    def charge_state(self) -> tuple[tuple[int | None, ...], int]:
        """Per-slot charges plus Möbius ε at t=0. Ordered: (z,x) ≠ (x,z)."""

        return (self.slot_charges, MOBIUS_EPSILON_T0)


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


def dimension(id: str, charge: int | None = None) -> Dimension:
    return Dimension(id, charge)


def coupling(dimension_ids: Sequence[str], charges: Mapping[str, int] | None = None) -> Coupling:
    if not isinstance(dimension_ids, Sequence) or isinstance(dimension_ids, (str, bytes)):
        raise DimensionalArityError("coupling dimensions must be an ordered declaration sequence")
    charge_map = dict(charges or {})
    return Coupling(tuple(Dimension(item, charge_map.get(item)) for item in dimension_ids))


def space(
    ambient_ids: Sequence[str],
    coupling_declarations: Sequence[Sequence[str]] = (),
    proofs: Sequence[CouplingProof] = (),
    charges: Mapping[str, int] | None = None,
) -> DimensionalSpace:
    if not isinstance(ambient_ids, Sequence) or isinstance(ambient_ids, (str, bytes)):
        raise DimensionalArityError("ambient dimensions must be a declared sequence")
    charge_map = dict(charges or {})
    ambient = tuple(Dimension(item, charge_map.get(item)) for item in ambient_ids)
    by_id = {item.id: item for item in ambient}
    declared = []
    for item in coupling_declarations:
        if not isinstance(item, Sequence) or isinstance(item, (str, bytes)):
            raise DimensionalArityError("each coupling declaration must be an ordered sequence")
        declared.append(Coupling(tuple(by_id[name] if name in by_id else Dimension(name) for name in item)))
    return DimensionalSpace(
        ambient_dimensions=ambient,
        couplings=tuple(declared),
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


def instances_missing_oriented_hub_coupling(
    declared: DimensionalSpace,
    *,
    hub_id: str,
    instance_ids: Sequence[str],
) -> tuple[str, ...]:
    """Instances that do not have a declared (hub, instance) coupling.

    (instance, hub) does not count. One (z, x) does not cover a second x.
    """

    ambient = {axis.id for axis in declared.ambient_dimensions}
    if hub_id not in ambient:
        raise DimensionalArityError(f"hub {hub_id!r} is not an ambient dimension")
    missing: list[str] = []
    seen: set[str] = set()
    for instance_id in instance_ids:
        if not isinstance(instance_id, str) or not instance_id or instance_id.isspace():
            raise DimensionalArityError("instance id must be exact non-empty text")
        if instance_id == hub_id:
            raise DimensionalArityError("the hub is not an instance of x or y")
        if instance_id not in ambient:
            raise DimensionalArityError(f"instance {instance_id!r} is not an ambient dimension")
        if instance_id in seen:
            raise DimensionalArityError(f"instance {instance_id!r} is repeated; occurrences must be unique")
        seen.add(instance_id)
        if not has_declared_coupling(declared, [hub_id, instance_id]):
            missing.append(instance_id)
    return tuple(missing)


def require_every_instance_has_oriented_hub_coupling(
    declared: DimensionalSpace,
    *,
    hub_id: str,
    instance_ids: Sequence[str],
) -> None:
    """Fail closed unless every instance has its own (z, instance)."""

    missing = instances_missing_oriented_hub_coupling(
        declared, hub_id=hub_id, instance_ids=instance_ids
    )
    if missing:
        raise DimensionalArityError(
            f"every instance must have declared ({hub_id}, instance); missing {tuple(missing)}"
        )


def oriented_instance_couplings(
    declared: DimensionalSpace,
    *,
    hub_id: str,
    instance_ids: Sequence[str],
) -> tuple[tuple[str, str], ...]:
    """The (z, x_i) / (z, y_j) coupling for each instance, in instance order."""

    require_every_instance_has_oriented_hub_coupling(
        declared, hub_id=hub_id, instance_ids=instance_ids
    )
    return tuple((hub_id, instance_id) for instance_id in instance_ids)


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


def structure_from_charged_couplings(declared: DimensionalSpace) -> Mapping[str, object]:
    """The three-dimensional structure already present in the couplings.

    Each part is one declared oriented coupling together with its arity charge
    state. Degree records how those parts sit on shared axes. This is not an
    inferred cartesian embedding and not a ternary coupling.
    """

    degrees = degree_relations(declared)
    parts = tuple(
        {
            "coupling": item.declared_ids,
            "arity": item.arity,
            "charge_state": item.charge_state,
        }
        for item in declared.couplings
    )
    return {
        "kind": "combination-of-oriented-couplings-and-arity-charge-states",
        "parts": parts,
        "degree": tuple(
            {
                "dimension": item.dimension.id,
                "charge": item.dimension.charge,
                "degree": item.degree,
                "slot_degrees": item.slot_degrees,
            }
            for item in degrees
            if item.degree
        ),
        "participating_dimension_count": len(
            {name for item in declared.couplings for name in item.declared_ids}
        ),
        "ternary_coupling_declared": any(item.arity == 3 for item in declared.couplings),
        "inferred_cartesian_embedding": False,
    }


def _tuple_tree(value: object) -> object:
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes)):
        return tuple(_tuple_tree(item) for item in value)
    return value


def charged_structure_readout(structure: Mapping[str, object]) -> tuple[object, ...]:
    """Order-invariant 3-structure: couplings + charge states + degree.

    Each instance stays in the coupling ids. Slot order inside each coupling is
    kept, so ``(8, 1)`` is not ``(1, 8)`` and ``(z, x0)`` is not ``(z, x1)``.
    """

    parts = tuple(
        sorted(
            (
                int(part["arity"]),
                _tuple_tree(part["charge_state"]),
                _tuple_tree(part["coupling"]),
            )
            for part in structure["parts"]
        )
    )
    degree = tuple(
        sorted(
            (
                int(item["degree"]),
                _tuple_tree(item["slot_degrees"]),
                item["charge"],
            )
            for item in structure["degree"]
        )
    )
    return (
        parts,
        degree,
        int(structure["participating_dimension_count"]),
        bool(structure["ternary_coupling_declared"]),
    )


def topology_structure_readout(structure: Mapping[str, object]) -> tuple[object, ...]:
    """Arity and degree only. Charge state is omitted."""

    parts, degree, participating, ternary = charged_structure_readout(structure)
    return (
        tuple(item[0] for item in parts),
        tuple((deg, slots) for deg, slots, _charge in degree),
        participating,
        ternary,
    )


def geometry_from_declared_couplings(declared: DimensionalSpace) -> Mapping[str, object]:
    degrees = degree_relations(declared)
    couplings = tuple(
        {
            "declared_ids": item.declared_ids,
            "arity": item.arity,
            "slot_charges": item.slot_charges,
            "charge_state": item.charge_state,
            "mobius_epsilon_t0": MOBIUS_EPSILON_T0,
        }
        for item in declared.couplings
    )
    return {
        "ambient_ids": tuple(item.id for item in declared.ambient_dimensions),
        "ambient_count": len(declared.ambient_dimensions),
        "couplings": couplings,
        "participating_ids": tuple(
            dict.fromkeys(name for item in declared.couplings for name in item.declared_ids)
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
        "structure": structure_from_charged_couplings(declared),
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
    "MOBIUS_EPSILON_T0",
    "charged_structure_readout",
    "coupling",
    "degree_relations",
    "dimension",
    "geometry_from_declared_couplings",
    "has_declared_coupling",
    "install_proven_coupling",
    "instances_missing_oriented_hub_coupling",
    "observed_common_ids",
    "oriented_instance_couplings",
    "require_every_instance_has_oriented_hub_coupling",
    "space",
    "structure_from_charged_couplings",
    "topology_structure_readout",
]
