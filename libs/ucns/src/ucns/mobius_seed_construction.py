# === MODULE_BUILD ===
# id: ucns_mobius_seed_construction
#   module_name: mobius_seed_construction
#   module_kind: experiment
#   summary: smallest construction-state authority for the Mobius Seed of Life: a built-slot set plus buildable-next rule derived only from the seed's own structural-vesica relations
#   owner: Erin Spencer
#   public_surface: CONSTRUCTION_SCHEMA_ID, CONSTRUCTION_SCHEMA_VERSION, ConstructionState, initial_construction_state, buildable_slots, construct, from_built
#   internal_surface: slot validation and relation lookups against MobiusSeedOfLife
#   auth_boundary: none
#   storage_boundary: none
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: tests/test_mobius_seed_construction.py
#   rollout: explicit UCNS-only candidate; selection effect none; AHBG and other consumers bind to this state rather than inventing build geometry
#   rollback: remove this module and its tests without altering mobius_seed geometry
#   requires: ucns_mobius_seed_of_life_candidate
#   since: 2026-09-02
#   unresolved: later Flower-of-Life rings and any canonical seven-gonol composition remain separate UCNS decisions
# === END MODULE_BUILD ===

# === CONTRACTS ===
# id: mobius_seed_construction_starts_at_the_center
#   given: the default construction state is requested
#   then: exactly the CENTER band is built and every ring slot is buildable next because each CENTER-ring pair is a structural vesica
#   class: correctness
#   since: 2026-09-02
#
# id: mobius_seed_construction_state_boundary_is_immutable_and_centered
#   given: a ConstructionState is created from a built-slot collection
#   then: built is normalized to an immutable frozenset of BandSlot values, CENTER is required, and invalid or out-of-seed entries fail closed
#   class: correctness
#   since: 2026-09-02
#
# id: mobius_seed_construction_is_adjacency_from_seed_relations
#   given: any construction state
#   then: a slot is buildable only when it is unbuilt and shares a structural-vesica relation with a built slot; no other adjacency rule is used
#   class: correctness
#   since: 2026-09-02
#
# id: mobius_seed_construction_never_invents_game_semantics
#   given: a build is recorded
#   then: the artifact only records UCNS slots and the seed schema identity; it carries no AHBG tile, unit, turn, or permission semantics
#   class: doctrine
#   since: 2026-09-02
#
# id: mobius_seed_construction_completes_and_replays
#   given: repeated buildable-next construction or a persisted built-slot list
#   then: repeated builds complete all seven slots and from_built reproduces the exact built set
#   class: correctness
#   since: 2026-09-02
# === END CONTRACTS ===

"""Construction state for the seven-band Mobius Seed of Life.

This is the smallest UCNS construction authority: a set of built band slots
plus a buildable-next rule derived only from the seed's own structural-vesica
relations. A consumer (for example AHBG) binds its build mechanic to this state
instead of inventing construction geometry.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .mobius_seed import (
    MOBIUS_SEED_PROJECTION_ID,
    MOBIUS_SEED_SCHEMA_ID,
    MOBIUS_SEED_SCHEMA_VERSION,
    MOBIUS_SEED_SELECTION_EFFECT,
    BandSlot,
    MobiusSeedError,
    MobiusSeedOfLife,
    PairStanding,
    build_mobius_seed_of_life,
)

CONSTRUCTION_SCHEMA_ID = "ucns.mobius-seed-construction"
CONSTRUCTION_SCHEMA_VERSION = "0.1.0"
CONSTRUCTION_SELECTION_EFFECT = "none"


@dataclass(frozen=True, slots=True)
class ConstructionState:
    """Built band slots of one Mobius Seed of Life construction."""

    seed: MobiusSeedOfLife
    built: frozenset[BandSlot]
    schema_id: str = CONSTRUCTION_SCHEMA_ID
    schema_version: str = CONSTRUCTION_SCHEMA_VERSION
    selection_effect: str = CONSTRUCTION_SELECTION_EFFECT

    def __post_init__(self) -> None:
        normalized = frozenset(self.built)
        invalid = [item for item in normalized if not isinstance(item, BandSlot)]
        if invalid:
            raise MobiusSeedError("construction built entries must be BandSlot values")
        object.__setattr__(self, "built", normalized)

        slots = {band.slot for band in self.seed.bands}
        if not normalized:
            raise MobiusSeedError("construction state must build at least one slot")
        unknown = normalized - slots
        if unknown:
            raise MobiusSeedError(
                f"built slots outside the seed: {', '.join(sorted(slot.value for slot in unknown))}"
            )
        if BandSlot.CENTER not in normalized:
            raise MobiusSeedError("construction state must include CENTER")
        if self.schema_id != CONSTRUCTION_SCHEMA_ID or self.schema_version != CONSTRUCTION_SCHEMA_VERSION:
            raise MobiusSeedError("construction schema identity mismatch")
        if self.selection_effect != CONSTRUCTION_SELECTION_EFFECT:
            raise MobiusSeedError("construction candidate cannot select UCNS canon")

    def is_built(self, slot: BandSlot) -> bool:
        return slot in self.built

    def as_dict(self) -> dict[str, object]:
        return {
            "schema_id": self.schema_id,
            "schema_version": self.schema_version,
            "selection_effect": self.selection_effect,
            "seed": {
                "schema_id": self.seed.schema_id,
                "schema_version": self.seed.schema_version,
                "projection_id": MOBIUS_SEED_PROJECTION_ID,
            },
            "built": [slot.value for slot in sorted(self.built, key=lambda item: (item.ring_index is None, item.ring_index or 0, item.value))],
            "buildable": [slot.value for slot in buildable_slots(self)],
        }


def initial_construction_state(seed: MobiusSeedOfLife | None = None) -> ConstructionState:
    """Construction starts at the center band only."""

    resolved = seed if seed is not None else build_mobius_seed_of_life()
    return ConstructionState(seed=resolved, built=frozenset((BandSlot.CENTER,)))


def buildable_slots(state: ConstructionState) -> tuple[BandSlot, ...]:
    """Unbuilt slots adjacent to a built slot via a structural vesica.

    Adjacency is read from the seed's own relation ledger: a structural-vesica
    relation between a built and an unbuilt slot is the only buildable-next
    authority. No distance arithmetic is re-derived here.
    """

    buildable: list[BandSlot] = []
    built = state.built
    for relation in state.seed.relations:
        if relation.standing is not PairStanding.STRUCTURAL_VESICA:
            continue
        for left, right in ((relation.left, relation.right), (relation.right, relation.left)):
            if left in built and right not in built:
                buildable.append(right)
    unique = list(dict.fromkeys(buildable))
    return tuple(
        sorted(unique, key=lambda slot: (slot is BandSlot.CENTER, slot.ring_index or 0, slot.value))
    )


def construct(state: ConstructionState, slot: BandSlot) -> ConstructionState:
    """Record one built slot, fail-closed unless it is currently buildable."""

    if slot in state.built:
        raise MobiusSeedError(f"{slot.value} is already built")
    if slot not in buildable_slots(state):
        raise MobiusSeedError(
            f"{slot.value} is not buildable; buildable now: "
            + ", ".join(item.value for item in buildable_slots(state))
        )
    return ConstructionState(seed=state.seed, built=state.built | {slot})


def from_built(
    slots: Iterable[BandSlot | str],
    seed: MobiusSeedOfLife | None = None,
) -> ConstructionState:
    """Rebuild a construction state from persisted BandSlot or string values."""

    normalized: list[BandSlot] = []
    for raw in slots:
        try:
            slot = raw if isinstance(raw, BandSlot) else BandSlot(str(raw))
        except (TypeError, ValueError) as exc:
            raise MobiusSeedError(f"unknown persisted construction slot {raw!r}") from exc
        normalized.append(slot)
    if BandSlot.CENTER not in normalized:
        raise MobiusSeedError("persisted construction must include CENTER")

    resolved = seed if seed is not None else build_mobius_seed_of_life()
    state = initial_construction_state(resolved)
    for slot in normalized:
        if slot is not BandSlot.CENTER:
            state = construct(state, slot)
    return state
