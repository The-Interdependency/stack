"""Element gonols closed as EPAC Public Gonols from atomic electron-shell structure.

Every electron instance has its own ``(nucleus, electron_i)`` coupling.
Nuclear ``Z`` and electron charge ``-1`` are the slot charges. That atomic
3-structure closes with the element gonol. Molecular construction must not
reopen it. Letters and abbreviations are not these axes.

Usage guidance
--------------
Each electron, shell, nucleus, and element is an EPAC Public Gonol on the
UCNS carrier. This module does not use ``edcm.gonol``. Nothing molecular is
encoded here.

    from epac_periodic import construct_element_gonol, construct_periodic_table

    oxygen = construct_element_gonol("O")
    assert oxygen.constructor_id == "epac.public_gonol"
    assert len(oxygen.structure["parts"]) == 8
"""

from __future__ import annotations

from typing import Iterable

from epac_atomic import AtomicRecord, ElectronState, iter_table
from epac_dimensional_arity import (
    geometry_from_declared_couplings,
    oriented_instance_couplings,
    space,
)
from epac_public_gonol import (
    ClosedPublicGonol,
    PublicGonolReceipt,
    construct_public_gonol,
    replay_public_gonol,
)

# Elementary charge in units of e. Nuclear Z is proton count in the same units.
ELECTRON_CHARGE = -1


def _carrier_glyph(text: str) -> str | None:
    if len(text) == 1:
        return text
    return None


def _electron_options(electron: ElectronState) -> tuple[tuple[str, str], ...]:
    return (
        ("n", str(electron.n)),
        ("l", str(electron.l)),
        ("m_l", str(electron.m_l)),
        ("m_s", str(electron.m_s)),
        ("shell", electron.shell),
        ("subshell", electron.subshell),
        ("angular-id", electron.angular_id),
        ("radial-nodes", str(electron.radial_nodes)),
        ("z-eff", electron.z_eff),
        ("e-rydberg", electron.e_rydberg),
        ("valence", "true" if electron.valence else "false"),
        ("paired", "true" if electron.paired else "false"),
    )


def _construct_electron(
    electron: ElectronState, *, symbol: str, atom_occurrence: int
) -> ClosedPublicGonol:
    return construct_public_gonol(
        source_id=f"epac.electron:{symbol}#{atom_occurrence}:{electron.index}",
        relation="epac.atomic.electron",
        identity_glyph="e",
        carried_options=_electron_options(electron),
        occurrence=electron.index,
    ).gonol


def _construct_shell(
    n: int,
    electrons: Iterable[ElectronState],
    *,
    symbol: str,
    atom_occurrence: int,
) -> ClosedPublicGonol:
    members = tuple(
        _construct_electron(e, symbol=symbol, atom_occurrence=atom_occurrence) for e in electrons
    )
    return construct_public_gonol(
        source_id=f"epac.shell:{symbol}#{atom_occurrence}:n{n}",
        relation="epac.atomic.shell",
        identity_glyph=_carrier_glyph(str(n)),
        participants=members,
        occurrence=n,
        carried_options=(("n", str(n)),),
    ).gonol


def _construct_nucleus(record: AtomicRecord, *, atom_occurrence: int) -> ClosedPublicGonol:
    return construct_public_gonol(
        source_id=f"epac.nucleus:{record.symbol}#{atom_occurrence}",
        relation="epac.atomic.nucleus",
        carried_options=(
            ("Z", str(record.Z)),
            ("A", str(record.A)),
            ("protons", str(record.proton_count)),
            ("neutrons", str(record.neutron_count)),
            ("symbol", record.symbol),
        ),
        occurrence=0,
    ).gonol


def _nucleus_dimension_id(symbol: str, atom_occurrence: int) -> str:
    return f"epac.nucleus:{symbol}#{atom_occurrence}"


def _electron_dimension_id(symbol: str, atom_occurrence: int, index: int) -> str:
    return f"epac.electron:{symbol}#{atom_occurrence}:{index}"


def _declared_atomic_space(record: AtomicRecord, *, atom_occurrence: int):
    """One ``(nucleus, electron_i)`` coupling for every electron instance.

    Closed shells still participate as instances. Letters do not.
    """

    hub = _nucleus_dimension_id(record.symbol, atom_occurrence)
    electron_ids = [
        _electron_dimension_id(record.symbol, atom_occurrence, electron.index)
        for electron in record.electrons
    ]
    charges = {hub: record.Z, **{electron_id: ELECTRON_CHARGE for electron_id in electron_ids}}
    declared = space(
        [hub, *electron_ids],
        [[hub, electron_id] for electron_id in electron_ids],
        charges=charges,
    )
    oriented_instance_couplings(declared, hub_id=hub, instance_ids=electron_ids)
    return declared


def construct_element_gonol(symbol: str, *, occurrence: int = 0) -> PublicGonolReceipt:
    """Close one element Public Gonol whose participants are nucleus + electron shells."""

    record = None
    for item in iter_table():
        if item.symbol == symbol:
            record = item
            break
    if record is None:
        raise ValueError(f"no atomic record for symbol {symbol!r}")
    shells: list[ClosedPublicGonol] = []
    by_n: dict[int, list[ElectronState]] = {}
    for electron in record.electrons:
        by_n.setdefault(electron.n, []).append(electron)
    for n in sorted(by_n):
        shells.append(_construct_shell(n, by_n[n], symbol=symbol, atom_occurrence=occurrence))
    nucleus = _construct_nucleus(record, atom_occurrence=occurrence)
    unpaired = record.unpaired_valence
    promoted = record.promoted_unpaired_valence
    carried = (
        ("symbol", record.symbol),
        ("Z", str(record.Z)),
        ("period", str(record.period)),
        ("group", str(record.group)),
        ("A", str(record.A)),
        ("electron-configuration", record.configuration),
        ("valence-n", str(record.valence_n)),
        ("valence-electrons", str(record.valence_electrons)),
        ("unpaired-valence-count", str(len(unpaired))),
        ("unpaired-valence-lm", ",".join(f"{e.l}:{e.m_l}" for e in unpaired) or "none"),
        ("promoted-unpaired-count", str(len(promoted))),
        ("promoted-unpaired-lm", ",".join(f"{e.l}:{e.m_l}" for e in promoted) or "none"),
        ("valence-angular-ids", ",".join(e.angular_id for e in record.electrons if e.valence)),
    )
    geometry = geometry_from_declared_couplings(
        _declared_atomic_space(record, atom_occurrence=occurrence)
    )
    return construct_public_gonol(
        source_id=f"epac.periodic:{symbol}#{occurrence}",
        relation="epac.atomic.element",
        identity_glyph=_carrier_glyph(symbol),
        participants=(nucleus, *shells),
        carried_options=carried,
        occurrence=occurrence,
        couplings=geometry["couplings"],
        structure=geometry["structure"],
    )


def construct_periodic_table() -> dict[str, PublicGonolReceipt]:
    return {record.symbol: construct_element_gonol(record.symbol) for record in iter_table()}


def replay_element_gonol(receipt: PublicGonolReceipt) -> PublicGonolReceipt:
    return replay_public_gonol(receipt)


def atomic_of(symbol: str) -> AtomicRecord:
    for record in iter_table():
        if record.symbol == symbol:
            return record
    raise ValueError(symbol)


def symbol_of(gonol: ClosedPublicGonol) -> str:
    for key, value in gonol.carried_options:
        if key == "symbol":
            return value
    if gonol.identity_glyph:
        return gonol.identity_glyph
    raise KeyError("symbol")


def carried(gonol: ClosedPublicGonol, key: str) -> str:
    for item_key, value in gonol.carried_options:
        if item_key == key:
            return value
    raise KeyError(key)
