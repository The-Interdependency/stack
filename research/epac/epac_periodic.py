"""Element gonols closed from full atomic electron-shell structure.

Usage guidance
--------------
Each electron is a closed gonol with (n, l, m_l, m_s), shell, subshell,
hydrogenic angular id, radial nodes, Slater Z_eff, and Rydberg energy.
Electrons of one n affixiate as a shell. Shells plus a nucleus gonol
affixiate as the element. Nothing molecular is encoded.

    from epac_periodic import construct_element_gonol, construct_periodic_table

    oxygen = construct_element_gonol("O")
"""

from __future__ import annotations

from typing import Any, Iterable

from edcm.gonol import ClosedGonol, GonolReceipt, construct_gonol, replay_gonol

from epac_atomic import AtomicRecord, ElectronState, atomic_record, iter_table


def _geometry_authority() -> Any:
    from ucns import public_gonol

    return public_gonol


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


def _construct_electron(electron: ElectronState, *, symbol: str, atom_occurrence: int) -> ClosedGonol:
    receipt = construct_gonol(
        scale="word",
        source="e",
        source_id=f"epac.electron:{symbol}#{atom_occurrence}:{electron.index}",
        carried_options=_electron_options(electron),
        geometry_authority=_geometry_authority(),
        occurrence=electron.index,
    )
    return receipt.gonol


def _construct_shell(
    n: int,
    electrons: Iterable[ElectronState],
    *,
    symbol: str,
    atom_occurrence: int,
) -> ClosedGonol:
    members = tuple(_construct_electron(e, symbol=symbol, atom_occurrence=atom_occurrence) for e in electrons)
    return construct_gonol(
        scale="word",
        source=f"n{n}",
        source_id=f"epac.shell:{symbol}#{atom_occurrence}:n{n}",
        participants=members,
        relation="epac.atomic.shell",
        geometry_authority=_geometry_authority(),
        occurrence=n,
    ).gonol


def _construct_nucleus(record: AtomicRecord, *, atom_occurrence: int) -> ClosedGonol:
    return construct_gonol(
        scale="word",
        source="nuc",
        source_id=f"epac.nucleus:{record.symbol}#{atom_occurrence}",
        carried_options=(
            ("Z", str(record.Z)),
            ("A", str(record.A)),
            ("protons", str(record.proton_count)),
            ("neutrons", str(record.neutron_count)),
        ),
        geometry_authority=_geometry_authority(),
        occurrence=0,
    ).gonol


def construct_element_gonol(symbol: str, *, occurrence: int = 0) -> GonolReceipt:
    """Close one element gonol whose participants are nucleus + electron shells."""

    record = None
    for item in iter_table():
        if item.symbol == symbol:
            record = item
            break
    if record is None:
        raise ValueError(f"no atomic record for symbol {symbol!r}")
    shells: list[ClosedGonol] = []
    by_n: dict[int, list[ElectronState]] = {}
    for electron in record.electrons:
        by_n.setdefault(electron.n, []).append(electron)
    for n in sorted(by_n):
        shells.append(
            _construct_shell(n, by_n[n], symbol=symbol, atom_occurrence=occurrence)
        )
    nucleus = _construct_nucleus(record, atom_occurrence=occurrence)
    unpaired = record.unpaired_valence
    promoted = record.promoted_unpaired_valence
    carried = (
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
    return construct_gonol(
        scale="word",
        source=symbol,
        source_id=f"epac.periodic:{symbol}#{occurrence}",
        participants=(nucleus, *shells),
        relation="epac.atomic.element",
        carried_options=carried,
        geometry_authority=_geometry_authority(),
        occurrence=occurrence,
    )


def construct_periodic_table() -> dict[str, GonolReceipt]:
    return {record.symbol: construct_element_gonol(record.symbol) for record in iter_table()}


def replay_element_gonol(receipt: GonolReceipt) -> GonolReceipt:
    return replay_gonol(receipt=receipt)


def atomic_of(symbol: str) -> AtomicRecord:
    for record in iter_table():
        if record.symbol == symbol:
            return record
    raise ValueError(symbol)


def symbol_of(gonol: ClosedGonol) -> str:
    return "".join(gonol.source_units)


def carried(gonol: ClosedGonol, key: str) -> str:
    for item_key, value in gonol.carried_options:
        if item_key == key:
            return value
    raise KeyError(key)
