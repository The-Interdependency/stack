"""Molecular EPAC Public Gonols from atomic electron-shell gonols.

Attachment sites are unpaired valence electrons (atomic Hund filling).
If ligand count exceeds ground-state unpaired count, the atomic promoted
valence set (s→p in the same n) is used. Ligand and center (l, m_l) sets
are construction invariants. Construction uses ``epac.public_gonol``, not
``edcm.gonol``. No sealed molecular-shape file is opened here.

The three-dimensional structure is the combination of declared oriented
couplings and each arity's charge state (nuclear Z plus Möbius ε at t=0)
with degree. Every ligand instance has its own (center, instance) coupling.
It is not an inferred cartesian embedding.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from ucns.direct_mobius import native_mobius_state

from epac_atomic import AtomicRecord
from epac_dimensional_arity import (
    charged_structure_readout,
    geometry_from_declared_couplings,
    oriented_instance_couplings,
    space,
    topology_structure_readout,
)
from epac_periodic import atomic_of, carried, construct_element_gonol, symbol_of
from epac_public_gonol import ClosedPublicGonol, PublicGonolReceipt, construct_public_gonol, replay_public_gonol


MOLECULE_COMPOSITIONS: Mapping[str, tuple[tuple[str, int], ...]] = {
    "H2": (("H", 2),),
    "H2O": (("H", 2), ("O", 1)),
    "NH3": (("N", 1), ("H", 3)),
    "CH4": (("C", 1), ("H", 4)),
    "CO2": (("C", 1), ("O", 2)),
}

RELATION = "epac.affixiation.unpaired-valence"


@dataclass(frozen=True, slots=True)
class MolecularConstruction:
    formula: str
    receipt: PublicGonolReceipt
    invariants: Mapping[str, Any]


def _instantiate(composition: tuple[tuple[str, int], ...]) -> tuple[ClosedPublicGonol, ...]:
    instances: list[ClosedPublicGonol] = []
    occurrence = 0
    for symbol, count in composition:
        for _ in range(count):
            instances.append(construct_element_gonol(symbol, occurrence=occurrence).gonol)
            occurrence += 1
    return tuple(instances)


def _record_for(gonol: ClosedPublicGonol) -> AtomicRecord:
    return atomic_of(symbol_of(gonol))


def _choose_center(participants: tuple[ClosedPublicGonol, ...]) -> ClosedPublicGonol | None:
    """Center is the unique singleton symbol when ligands share another symbol.

    This is stoichiometric, not a shape rule. H2 has no singleton.
    """

    counts: dict[str, int] = {}
    for item in participants:
        counts[symbol_of(item)] = counts.get(symbol_of(item), 0) + 1
    singletons = [symbol for symbol, count in counts.items() if count == 1]
    if len(singletons) == 1 and len(counts) > 1:
        symbol = singletons[0]
        return next(item for item in participants if symbol_of(item) == symbol)
    return None


def _attachment_set(record: AtomicRecord, needed: int) -> tuple[tuple[int, int], ...]:
    ground = tuple((e.l, e.m_l) for e in record.unpaired_valence)
    if len(ground) >= needed:
        return ground[:needed]
    promoted = tuple((e.l, e.m_l) for e in record.promoted_unpaired_valence)
    if len(promoted) >= needed:
        return promoted[:needed]
    raise ValueError(
        f"{record.symbol} has {len(ground)} unpaired valence electrons; "
        f"{needed} attachment sites were requested"
    )


def _atom_dimension_id(gonol: ClosedPublicGonol) -> str:
    return f"{symbol_of(gonol)}#{gonol.occurrence}"


def _declared_dimensional_space(
    participants: tuple[ClosedPublicGonol, ...],
    center: ClosedPublicGonol | None,
    ligands: tuple[ClosedPublicGonol, ...],
):
    ambient = [_atom_dimension_id(item) for item in participants]
    charges = {_atom_dimension_id(item): int(carried(item, "Z")) for item in participants}
    if center is None:
        declarations = [[_atom_dimension_id(participants[0]), _atom_dimension_id(participants[1])]]
    else:
        center_id = _atom_dimension_id(center)
        declarations = [[center_id, _atom_dimension_id(ligand)] for ligand in ligands]
    return space(ambient, declarations, charges=charges)


def _mobius_coupling() -> Mapping[str, Any]:
    origin = native_mobius_state(0)
    one = origin.advance(1)
    two = origin.advance(2)
    return {
        "law": "ucns.native-mobius-root-loop",
        "parameter": "turn-index",
        "t": [0, 1, 2],
        "visible_phase": [
            str(origin.visible_key[1]),
            str(one.visible_key[1]),
            str(two.visible_key[1]),
        ],
        "frame": [origin.frame.value, one.frame.value, two.frame.value],
        "complete_restored": two.complete_key == origin.complete_key,
        "one_turn_flips_frame": one.frame != origin.frame and one.visible_key == origin.visible_key,
    }


def construct_molecule(formula: str) -> MolecularConstruction:
    if formula not in MOLECULE_COMPOSITIONS:
        raise ValueError(f"formula {formula!r} is outside the declared run")
    participants = _instantiate(MOLECULE_COMPOSITIONS[formula])
    center = _choose_center(participants)
    if center is None:
        ligands = ()
        center_sites: tuple[tuple[int, int], ...] = ()
        if len(participants) != 2:
            raise ValueError("symmetric affixiation is declared only for two equal atoms")
        left, right = (_record_for(participants[0]), _record_for(participants[1]))
        ligand_sites = (
            tuple((e.l, e.m_l) for e in left.unpaired_valence),
            tuple((e.l, e.m_l) for e in right.unpaired_valence),
        )
        used_promotion = False
    else:
        ligands = tuple(item for item in participants if item is not center)
        needed = len(ligands)
        center_record = _record_for(center)
        ground = tuple((e.l, e.m_l) for e in center_record.unpaired_valence)
        used_promotion = needed > len(ground)
        center_sites = _attachment_set(center_record, needed)
        ligand_sites = tuple(
            tuple((e.l, e.m_l) for e in _record_for(item).unpaired_valence) for item in ligands
        )
    mobius = _mobius_coupling()
    dimensional = _declared_dimensional_space(participants, center, ligands)
    instance_couplings: tuple[tuple[str, str], ...] = ()
    if center is not None:
        instance_couplings = oriented_instance_couplings(
            dimensional,
            hub_id=_atom_dimension_id(center),
            instance_ids=tuple(_atom_dimension_id(item) for item in ligands),
        )
    geometry = geometry_from_declared_couplings(dimensional)
    receipt = construct_public_gonol(
        source_id=f"epac.molecule:{formula}",
        relation=RELATION,
        participants=participants,
        couplings=geometry["couplings"],
        structure=geometry["structure"],
    )
    distinct_p_m = tuple(sorted({m for l, m in center_sites if l == 1}))
    ligand_has_p = any(any(l == 1 for l, _m in sites) for sites in ligand_sites)
    invariants = {
        "formula": formula,
        "atom_count": len(participants),
        "center_symbol": None if center is None else symbol_of(center),
        "center_Z": None if center is None else carried(center, "Z"),
        "center_configuration": None if center is None else carried(center, "electron-configuration"),
        "center_valence_electrons": None if center is None else carried(center, "valence-electrons"),
        "center_unpaired_lm": [f"{l}:{m}" for l, m in center_sites],
        "center_used_atomic_promotion": used_promotion,
        "center_distinct_p_m": [str(m) for m in distinct_p_m],
        "ligand_symbols": [symbol_of(item) for item in ligands],
        "ligand_unpaired_lm": [[f"{l}:{m}" for l, m in sites] for sites in ligand_sites],
        "ligand_has_p": ligand_has_p,
        "participant_symbols": [symbol_of(item) for item in participants],
        "atomic_coupling_signature": (
            None if center is None else carried(center, "electron-configuration"),
            tuple(center_sites),
            tuple(ligand_sites),
            used_promotion,
            ligand_has_p,
        ),
        "mobius": mobius,
        "ucns_coupling_signature": (
            mobius["law"],
            tuple(mobius["t"]),
            tuple(mobius["frame"]),
            mobius["complete_restored"],
        ),
        "dimensional_geometry": geometry,
        "declared_coupling_arities": [item["arity"] for item in geometry["couplings"]],
        "charged_structure_readout": charged_structure_readout(geometry["structure"]),
        "topology_structure_readout": topology_structure_readout(geometry["structure"]),
        "oriented_instance_couplings": instance_couplings,
    }
    return MolecularConstruction(formula=formula, receipt=receipt, invariants=invariants)


def replay_molecule(construction: MolecularConstruction) -> PublicGonolReceipt:
    return replay_public_gonol(construction.receipt)


def construct_declared_molecules() -> dict[str, MolecularConstruction]:
    return {formula: construct_molecule(formula) for formula in MOLECULE_COMPOSITIONS}


def matched_information_control(invariants: Mapping[str, Any]) -> tuple[Any, ...]:
    """Control: stoichiometric symbols only, no shells or wave identities."""

    return (
        invariants["atom_count"],
        invariants["center_symbol"],
        tuple(invariants["ligand_symbols"]),
    )
