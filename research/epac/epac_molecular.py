"""Molecular EPAC Public Gonols from closed valence-electron arity couplings.

Molecules are made where unpaired valence electrons couple. Each bond is a
declared arity-2 coupling of two already-closed valence electron gonols:
``(center_electron, ligand_electron)``. Closed atoms remain molecular
participants; nucleons and core electrons stay inside them. The table is
not re-queried.

Construction uses ``epac.public_gonol``, not ``edcm.gonol``. No sealed
molecular-shape file is opened here.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from ucns.direct_mobius import native_mobius_state

from epac_dimensional_arity import (
    charged_structure_readout,
    geometry_from_declared_couplings,
    oriented_instance_couplings,
    quaternion_structure_readout,
    space,
    topology_structure_readout,
)
from epac_periodic import (
    ELECTRON_CHARGE,
    construct_element_gonol,
    electron_lm,
    nuclear_charge,
    symbol_of,
    unpaired_valence_electrons,
)
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


def _atom_dimension_id(gonol: ClosedPublicGonol) -> str:
    return f"{symbol_of(gonol)}#{gonol.occurrence}"


def _declared_valence_space(
    bonds: tuple[tuple[ClosedPublicGonol, ClosedPublicGonol], ...],
):
    """Arity-2 couplings of closed valence electrons. Atoms are not these axes."""

    ambient: list[str] = []
    charges: dict[str, int] = {}
    declarations: list[list[str]] = []
    by_hub: dict[str, list[str]] = {}
    for hub_electron, instance_electron in bonds:
        hub_id = hub_electron.source_id
        instance_id = instance_electron.source_id
        if hub_id not in charges:
            ambient.append(hub_id)
            charges[hub_id] = ELECTRON_CHARGE
        if instance_id not in charges:
            ambient.append(instance_id)
            charges[instance_id] = ELECTRON_CHARGE
        declarations.append([hub_id, instance_id])
        by_hub.setdefault(hub_id, []).append(instance_id)
    declared = space(ambient, declarations, charges=charges)
    for hub_id, instance_ids in by_hub.items():
        oriented_instance_couplings(declared, hub_id=hub_id, instance_ids=tuple(instance_ids))
    return declared


def _site_label(site: tuple[int, int]) -> str:
    return f"{site[0]}:{site[1]}"


def _mobius_coupling(
    *,
    bonds: tuple[tuple[ClosedPublicGonol, ClosedPublicGonol], ...],
) -> Mapping[str, Any]:
    origin = native_mobius_state(0)
    one = origin.advance(1)
    two = origin.advance(2)
    attachment_slots = tuple(
        {
            "slot": slot,
            "center_electron": hub.source_id,
            "center_site": _site_label(electron_lm(hub)),
            "ligand_electron": instance.source_id,
            "ligand_site": _site_label(electron_lm(instance)),
        }
        for slot, (hub, instance) in enumerate(bonds)
    )
    return {
        "law": "ucns.native-mobius-root-loop",
        "binding": "declared-valence-electron-arity-couplings",
        "parameter": "turn-index-over-declared-attachment-evidence",
        "participant_axes": tuple(electron.source_id for bond in bonds for electron in bond),
        "attachment_slots": attachment_slots,
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


def _option(gonol: ClosedPublicGonol, key: str) -> str:
    for item_key, value in gonol.carried_options:
        if item_key == key:
            return value
    raise KeyError(key)


def _sites_from_closed(gonol: ClosedPublicGonol) -> tuple[tuple[int, int], ...]:
    return tuple(electron_lm(electron) for electron in unpaired_valence_electrons(gonol))


def _attachment_electron_ids(gonol: ClosedPublicGonol, *, limit: int | None = None) -> tuple[str, ...]:
    electrons = unpaired_valence_electrons(gonol)
    if limit is not None:
        electrons = electrons[:limit]
    return tuple(electron.source_id for electron in electrons)


def _consume_center(
    center: ClosedPublicGonol, needed: int
) -> tuple[ClosedPublicGonol, bool]:
    ground = unpaired_valence_electrons(center)
    if len(ground) >= needed:
        return center, False
    promoted = construct_element_gonol(
        symbol_of(center), occurrence=center.occurrence, promoted=True
    ).gonol
    if len(unpaired_valence_electrons(promoted)) < needed:
        raise ValueError(
            f"{symbol_of(center)} closed gonol has {len(ground)} unpaired valence electrons; "
            f"{needed} attachment sites were requested"
        )
    return promoted, True


def construct_molecule(formula: str) -> MolecularConstruction:
    if formula not in MOLECULE_COMPOSITIONS:
        raise ValueError(f"formula {formula!r} is outside the declared run")
    participants = _instantiate(MOLECULE_COMPOSITIONS[formula])
    center = _choose_center(participants)
    if center is None:
        ligands = ()
        if len(participants) != 2:
            raise ValueError("symmetric affixiation is declared only for two equal atoms")
        left_electrons = unpaired_valence_electrons(participants[0])
        right_electrons = unpaired_valence_electrons(participants[1])
        if len(left_electrons) != 1 or len(right_electrons) != 1:
            raise ValueError("symmetric affixiation requires one unpaired valence electron on each atom")
        bonds = ((left_electrons[0], right_electrons[0]),)
        ligand_sites = tuple(_sites_from_closed(item) for item in participants)
        center_sites = ()
        used_promotion = False
        center_attachment_ids = ()
        ligand_attachment_ids = tuple(_attachment_electron_ids(item) for item in participants)
    else:
        ligands = tuple(item for item in participants if item is not center)
        ligand_electrons = tuple(
            electron for ligand in ligands for electron in unpaired_valence_electrons(ligand)
        )
        needed = len(ligand_electrons)
        center, used_promotion = _consume_center(center, needed)
        participants = tuple(
            center
            if symbol_of(item) == symbol_of(center) and item.occurrence == center.occurrence
            else item
            for item in participants
        )
        ligands = tuple(item for item in participants if item is not center)
        ligand_electrons = tuple(
            electron for ligand in ligands for electron in unpaired_valence_electrons(ligand)
        )
        needed = len(ligand_electrons)
        center_unpaired = unpaired_valence_electrons(center)
        if len(center_unpaired) < needed:
            raise ValueError(
                f"{symbol_of(center)} has {len(center_unpaired)} unpaired valence electrons; "
                f"{needed} attachment sites were requested"
            )
        center_electrons = center_unpaired[:needed]
        bonds = tuple(zip(center_electrons, ligand_electrons))
        center_sites = tuple(electron_lm(electron) for electron in center_electrons)
        ligand_sites = tuple(_sites_from_closed(item) for item in ligands)
        center_attachment_ids = tuple(electron.source_id for electron in center_electrons)
        ligand_attachment_ids = tuple(_attachment_electron_ids(item) for item in ligands)
    mobius = _mobius_coupling(bonds=bonds)
    dimensional = _declared_valence_space(bonds)
    instance_couplings = tuple((hub.source_id, instance.source_id) for hub, instance in bonds)
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
        "center_Z": None if center is None else nuclear_charge(center),
        "center_configuration": None if center is None else _option(center, "electron-configuration"),
        "center_valence_electrons": None if center is None else _option(center, "valence-electrons"),
        "center_unpaired_lm": [f"{l}:{m}" for l, m in center_sites],
        "center_attachment_site_count": len(center_sites),
        "ligand_attachment_site_count": sum(len(sites) for sites in ligand_sites),
        "center_used_atomic_promotion": used_promotion,
        "center_attachment_electron_ids": list(center_attachment_ids),
        "ligand_attachment_electron_ids": [list(ids) for ids in ligand_attachment_ids],
        "consumed_atomic_quaternions": {
            _atom_dimension_id(item): quaternion_structure_readout(item.structure or {"quaternions": ()})
            for item in participants
        },
        "center_distinct_p_m": [str(m) for m in distinct_p_m],
        "ligand_symbols": [symbol_of(item) for item in ligands],
        "ligand_unpaired_lm": [[f"{l}:{m}" for l, m in sites] for sites in ligand_sites],
        "ligand_has_p": ligand_has_p,
        "participant_symbols": [symbol_of(item) for item in participants],
        "atomic_coupling_signature": (
            None if center is None else _option(center, "electron-configuration"),
            tuple(center_sites),
            tuple(ligand_sites),
            used_promotion,
            ligand_has_p,
        ),
        "mobius": mobius,
        "ucns_coupling_signature": (
            mobius["law"],
            tuple(mobius["participant_axes"]),
            tuple(
                tuple(sorted(slot.items()))
                for slot in mobius["attachment_slots"]
            ),
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
