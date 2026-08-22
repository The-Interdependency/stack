"""Molecular gonols by affixiation of element gonols plus UCNS Möbius coupling.

Usage guidance
--------------
Construction consumes element gonols, typical valence, and a stoichiometric
formula. It applies only the implemented UCNS Möbius root loop. It does not
open the sealed comparison file.

    from epac_molecular import construct_molecule

    water = construct_molecule("H2O")
    print(water.invariants)
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from edcm.gonol import ClosedGonol, GonolReceipt, construct_gonol, replay_gonol
from ucns.direct_mobius import native_mobius_state

from epac_periodic import construct_element_gonol, symbol_of, typical_valence_of


MOLECULE_COMPOSITIONS: Mapping[str, tuple[tuple[str, int], ...]] = {
    "H2": (("H", 2),),
    "H2O": (("H", 2), ("O", 1)),
    "NH3": (("N", 1), ("H", 3)),
    "CH4": (("C", 1), ("H", 4)),
    "CO2": (("C", 1), ("O", 2)),
}

RELATION = "epac.affixiation.valence-coupling"
SCALE = "recursive"


@dataclass(frozen=True, slots=True)
class MolecularConstruction:
    formula: str
    receipt: GonolReceipt
    invariants: Mapping[str, Any]


def _instantiate(composition: tuple[tuple[str, int], ...]) -> tuple[ClosedGonol, ...]:
    instances: list[ClosedGonol] = []
    occurrence = 0
    for symbol, count in composition:
        for _ in range(count):
            instances.append(construct_element_gonol(symbol, occurrence=occurrence).gonol)
            occurrence += 1
    return tuple(instances)


def _choose_center(participants: tuple[ClosedGonol, ...]) -> ClosedGonol | None:
    ranked = sorted(
        participants,
        key=lambda item: (typical_valence_of(item), symbol_of(item)),
        reverse=True,
    )
    top = ranked[0]
    if typical_valence_of(top) <= 0:
        return None
    if len(ranked) >= 2 and typical_valence_of(ranked[0]) == typical_valence_of(ranked[1]):
        return None
    return top


def _slot_occupancy(center: ClosedGonol, ligands: tuple[ClosedGonol, ...]) -> tuple[int, ...]:
    valence = typical_valence_of(center)
    if not ligands:
        raise ValueError("affixiation requires ligands when a center exists")
    if valence % len(ligands) != 0:
        raise ValueError("valence arity does not divide ligand count")
    occupancy = valence // len(ligands)
    return tuple(occupancy for _ in ligands)


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
    """Affixiate element gonols for one declared formula."""

    if formula not in MOLECULE_COMPOSITIONS:
        raise ValueError(f"formula {formula!r} is outside the declared run")
    participants = _instantiate(MOLECULE_COMPOSITIONS[formula])
    center = _choose_center(participants)
    if center is None:
        occupancy: tuple[int, ...] = ()
        ligands: tuple[ClosedGonol, ...] = ()
        if len(participants) != 2:
            raise ValueError("symmetric affixiation is declared only for two equal participants")
    else:
        ligands = tuple(item for item in participants if item is not center)
        occupancy = _slot_occupancy(center, ligands)
    receipt = construct_gonol(
        scale=SCALE,
        source_id=f"epac.molecule:{formula}",
        participants=participants,
        relation=RELATION,
        geometry_authority=__import__("ucns.public_gonol", fromlist=["public_gonol"]),
    )
    mobius = _mobius_coupling()
    invariants = {
        "formula": formula,
        "atom_count": len(participants),
        "center_symbol": None if center is None else symbol_of(center),
        "center_typical_valence": None if center is None else typical_valence_of(center),
        "ligand_symbols": [symbol_of(item) for item in ligands] if center is not None else [],
        "slot_occupancy": list(occupancy),
        "participant_symbols": [symbol_of(item) for item in participants],
        "mobius": mobius,
        "ucns_coupling_signature": (
            mobius["law"],
            tuple(mobius["t"]),
            tuple(mobius["frame"]),
            mobius["complete_restored"],
        ),
    }
    return MolecularConstruction(formula=formula, receipt=receipt, invariants=invariants)


def replay_molecule(construction: MolecularConstruction) -> GonolReceipt:
    return replay_gonol(receipt=construction.receipt)


def construct_declared_molecules() -> dict[str, MolecularConstruction]:
    return {formula: construct_molecule(formula) for formula in MOLECULE_COMPOSITIONS}


def matched_information_control(invariants: Mapping[str, Any]) -> tuple[Any, ...]:
    """Control that uses only formula composition and valence occupancy."""

    return (
        invariants["atom_count"],
        invariants["center_symbol"],
        invariants["center_typical_valence"],
        tuple(invariants["ligand_symbols"]),
        tuple(invariants["slot_occupancy"]),
    )
