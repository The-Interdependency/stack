"""Molecular gonols from atomic electron-shell gonols plus UCNS Möbius coupling.

Attachment sites are unpaired valence electrons (atomic Hund filling).
If ligand count exceeds ground-state unpaired count, the atomic promoted
valence set (s→p in the same n) is used. Ligand and center (l, m_l) sets
are construction invariants. No sealed molecular-shape file is opened here.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from edcm.gonol import ClosedGonol, GonolReceipt, construct_gonol, replay_gonol
from ucns.direct_mobius import native_mobius_state

from epac_atomic import AtomicRecord, atomic_record
from epac_periodic import atomic_of, carried, construct_element_gonol, symbol_of


MOLECULE_COMPOSITIONS: Mapping[str, tuple[tuple[str, int], ...]] = {
    "H2": (("H", 2),),
    "H2O": (("H", 2), ("O", 1)),
    "NH3": (("N", 1), ("H", 3)),
    "CH4": (("C", 1), ("H", 4)),
    "CO2": (("C", 1), ("O", 2)),
}

RELATION = "epac.affixiation.unpaired-valence"
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


def _record_for(gonol: ClosedGonol) -> AtomicRecord:
    return atomic_of(symbol_of(gonol))


def _choose_center(participants: tuple[ClosedGonol, ...]) -> ClosedGonol | None:
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
    receipt = construct_gonol(
        scale=SCALE,
        source_id=f"epac.molecule:{formula}",
        participants=participants,
        relation=RELATION,
        geometry_authority=__import__("ucns.public_gonol", fromlist=["public_gonol"]),
    )
    mobius = _mobius_coupling()
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
    }
    return MolecularConstruction(formula=formula, receipt=receipt, invariants=invariants)


def replay_molecule(construction: MolecularConstruction) -> GonolReceipt:
    return replay_gonol(receipt=construction.receipt)


def construct_declared_molecules() -> dict[str, MolecularConstruction]:
    return {formula: construct_molecule(formula) for formula in MOLECULE_COMPOSITIONS}


def matched_information_control(invariants: Mapping[str, Any]) -> tuple[Any, ...]:
    """Control: stoichiometric symbols only, no shells or wave identities."""

    return (
        invariants["atom_count"],
        invariants["center_symbol"],
        tuple(invariants["ligand_symbols"]),
    )
