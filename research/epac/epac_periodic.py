"""Element gonols closed as EPAC Public Gonols from nucleon then electron structure.

Precursors: each proton and each neutron is a closed gonol. The nucleus is
their affixiation. Electrons then couple to that closed nucleus. Occupancy-2
``(n, l, m_l)`` electrons pair inside the atom. Leftover unpaired valence
``(nucleus, electron_i)`` incidences are the bonding surfaces. Molecular
construction matches those surfaces and must not reopen nucleons or paired
electrons. Letters are not axes.

Usage guidance
--------------
Each nucleon, nucleus, electron, shell, and element is an EPAC Public Gonol
on the UCNS carrier. This module does not use ``edcm.gonol``.

    from epac_periodic import (
        PRIMARY_RESEARCH_ATOM,
        bonding_surfaces,
        construct_element_gonol,
        construct_periodic_table,
        pairing_couplings,
    )

    carbon = construct_element_gonol(PRIMARY_RESEARCH_ATOM)
    assert dict(carbon.gonol.carried_options)["symbol"] == "C"
    helium = construct_element_gonol("He")
    nucleus = helium.gonol.participants[0]
    assert [p.relation for p in nucleus.participants] == [
        "epac.atomic.proton", "epac.atomic.proton",
        "epac.atomic.neutron", "epac.atomic.neutron",
    ]
    assert pairing_couplings(helium.gonol) == (
        ("epac.electron:He#0:0", "epac.electron:He#0:1"),
    )
    assert bonding_surfaces(helium.gonol) == ()
    hydrogen = construct_element_gonol("H")
    assert [e.source_id for e in bonding_surfaces(hydrogen.gonol)] == [
        "epac.electron:H#0:0"
    ]
"""

from __future__ import annotations

from typing import Iterable

from epac_atomic import AtomicRecord, ElectronState, iter_table, promoted_atomic_record
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

# Elementary charge in units of e. Nuclear Z is the proton-count sum.
PROTON_CHARGE = 1
NEUTRON_CHARGE = 0
ELECTRON_CHARGE = -1
PRIMARY_RESEARCH_ATOM = "C"
NUCLEUS_RELATION = "epac.atomic.nucleus"
PROTON_RELATION = "epac.atomic.proton"
NEUTRON_RELATION = "epac.atomic.neutron"
SHELL_RELATION = "epac.atomic.shell"
ELECTRON_RELATION = "epac.atomic.electron"


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


def _proton_dimension_id(symbol: str, atom_occurrence: int, index: int) -> str:
    return f"epac.proton:{symbol}#{atom_occurrence}:{index}"


def _neutron_dimension_id(symbol: str, atom_occurrence: int, index: int) -> str:
    return f"epac.neutron:{symbol}#{atom_occurrence}:{index}"


def _construct_proton(
    *, symbol: str, atom_occurrence: int, index: int
) -> ClosedPublicGonol:
    return construct_public_gonol(
        source_id=_proton_dimension_id(symbol, atom_occurrence, index),
        relation=PROTON_RELATION,
        occurrence=index,
        carried_options=(
            ("charge", str(PROTON_CHARGE)),
            ("symbol", symbol),
            ("kind", "proton"),
        ),
    ).gonol


def _construct_neutron(
    *, symbol: str, atom_occurrence: int, index: int
) -> ClosedPublicGonol:
    return construct_public_gonol(
        source_id=_neutron_dimension_id(symbol, atom_occurrence, index),
        relation=NEUTRON_RELATION,
        occurrence=index,
        carried_options=(
            ("charge", str(NEUTRON_CHARGE)),
            ("symbol", symbol),
            ("kind", "neutron"),
        ),
    ).gonol


def _declared_nuclear_space(record: AtomicRecord, *, atom_occurrence: int):
    """Neutrons couple to protons. Proton-proton and neutron-neutron are not inferred.

    Hydrogen-1 has one proton and no neutrons, so no nuclear 3.
    """

    if record.proton_count != record.Z:
        raise ValueError(f"{record.symbol}: proton count must equal Z")
    if record.neutron_count != record.A - record.Z:
        raise ValueError(f"{record.symbol}: neutron count must equal A-Z")
    proton_ids = [
        _proton_dimension_id(record.symbol, atom_occurrence, index)
        for index in range(record.proton_count)
    ]
    neutron_ids = [
        _neutron_dimension_id(record.symbol, atom_occurrence, index)
        for index in range(record.neutron_count)
    ]
    charges = {
        **{proton_id: PROTON_CHARGE for proton_id in proton_ids},
        **{neutron_id: NEUTRON_CHARGE for neutron_id in neutron_ids},
    }
    declarations = [
        [proton_id, neutron_id] for proton_id in proton_ids for neutron_id in neutron_ids
    ]
    declared = space([*proton_ids, *neutron_ids], declarations, charges=charges)
    for proton_id in proton_ids:
        if neutron_ids:
            oriented_instance_couplings(
                declared, hub_id=proton_id, instance_ids=neutron_ids
            )
    return declared


def _construct_nucleus(record: AtomicRecord, *, atom_occurrence: int) -> ClosedPublicGonol:
    protons = tuple(
        _construct_proton(symbol=record.symbol, atom_occurrence=atom_occurrence, index=index)
        for index in range(record.proton_count)
    )
    neutrons = tuple(
        _construct_neutron(symbol=record.symbol, atom_occurrence=atom_occurrence, index=index)
        for index in range(record.neutron_count)
    )
    if len(protons) != record.Z or len(neutrons) != record.neutron_count:
        raise ValueError(f"{record.symbol}: nucleon gonols must match Z and A-Z")
    geometry = geometry_from_declared_couplings(
        _declared_nuclear_space(record, atom_occurrence=atom_occurrence)
    )
    couplings = geometry["couplings"]
    structure = geometry["structure"] if couplings else None
    return construct_public_gonol(
        source_id=f"epac.nucleus:{record.symbol}#{atom_occurrence}",
        relation=NUCLEUS_RELATION,
        participants=(*protons, *neutrons),
        carried_options=(
            ("Z", str(record.Z)),
            ("A", str(record.A)),
            ("protons", str(record.proton_count)),
            ("neutrons", str(record.neutron_count)),
            ("symbol", record.symbol),
        ),
        occurrence=0,
        couplings=couplings,
        structure=structure,
    ).gonol


def _nucleus_dimension_id(symbol: str, atom_occurrence: int) -> str:
    return f"epac.nucleus:{symbol}#{atom_occurrence}"


def _electron_dimension_id(symbol: str, atom_occurrence: int, index: int) -> str:
    return f"epac.electron:{symbol}#{atom_occurrence}:{index}"


def _orbital_key(electron: ElectronState) -> tuple[int, int, int]:
    return (electron.n, electron.l, electron.m_l)


def _pairing_electron_ids(
    record: AtomicRecord, *, atom_occurrence: int
) -> tuple[tuple[str, str], ...]:
    """Occupancy-2 ``(n, l, m_l)``: couple ``m_s=+1`` then ``m_s=-1``.

    One declared pair per orbital. Occupancy 1 is leftover and is not paired.
    Occupancy above 2 is Pauli-forbidden.
    """

    by_orbital: dict[tuple[int, int, int], list[ElectronState]] = {}
    for electron in record.electrons:
        by_orbital.setdefault(_orbital_key(electron), []).append(electron)
    pairs: list[tuple[str, str]] = []
    for key in sorted(by_orbital):
        occupants = by_orbital[key]
        if len(occupants) > 2:
            raise ValueError(
                f"{record.symbol}: orbital {key} has occupancy {len(occupants)}; Pauli limit is 2"
            )
        if len(occupants) != 2:
            continue
        first = next(item for item in occupants if item.m_s == 1)
        second = next(item for item in occupants if item.m_s == -1)
        pairs.append(
            (
                _electron_dimension_id(record.symbol, atom_occurrence, first.index),
                _electron_dimension_id(record.symbol, atom_occurrence, second.index),
            )
        )
    return tuple(pairs)


def _declared_atomic_space(record: AtomicRecord, *, atom_occurrence: int):
    """Two declared atomic relations.

    1. 3-structure: hub nucleus; every electron instance has ``(nucleus, electron_i)``.
    2. pairing: occupancy-2 electrons couple as ``(e_ms+1, e_ms-1)`` of the same
       ``(n, l, m_l)``.

    Leftover unpaired valence ``(nucleus, electron_i)`` are bonding surfaces.
    Pairing is not a proof of ``(nucleus, e_i, e_j)``. Letters do not participate.
    """

    hub = _nucleus_dimension_id(record.symbol, atom_occurrence)
    electron_ids = [
        _electron_dimension_id(record.symbol, atom_occurrence, electron.index)
        for electron in record.electrons
    ]
    pairing_ids = _pairing_electron_ids(record, atom_occurrence=atom_occurrence)
    charges = {hub: record.Z, **{electron_id: ELECTRON_CHARGE for electron_id in electron_ids}}
    declarations = [[hub, electron_id] for electron_id in electron_ids]
    declarations.extend([list(pair) for pair in pairing_ids])
    declared = space([hub, *electron_ids], declarations, charges=charges)
    oriented_instance_couplings(declared, hub_id=hub, instance_ids=electron_ids)
    for hub_electron, instance_electron in pairing_ids:
        oriented_instance_couplings(
            declared, hub_id=hub_electron, instance_ids=(instance_electron,)
        )
    return declared


def construct_element_gonol(
    symbol: str, *, occurrence: int = 0, promoted: bool = False
) -> PublicGonolReceipt:
    """Close one element Public Gonol whose participants are nucleus + electron shells."""

    record = None
    for item in iter_table():
        if item.symbol == symbol:
            record = item
            break
    if record is None:
        raise ValueError(f"no atomic record for symbol {symbol!r}")
    if promoted:
        record = promoted_atomic_record(record)
    shells: list[ClosedPublicGonol] = []
    by_n: dict[int, list[ElectronState]] = {}
    for electron in record.electrons:
        by_n.setdefault(electron.n, []).append(electron)
    for n in sorted(by_n):
        shells.append(_construct_shell(n, by_n[n], symbol=symbol, atom_occurrence=occurrence))
    nucleus = _construct_nucleus(record, atom_occurrence=occurrence)
    unpaired = record.unpaired_valence
    promoted_unpaired = record.promoted_unpaired_valence
    pairing_ids = _pairing_electron_ids(record, atom_occurrence=occurrence)
    paired_ids = {electron_id for pair in pairing_ids for electron_id in pair}
    surface_ids = tuple(
        _electron_dimension_id(record.symbol, occurrence, electron.index)
        for electron in record.electrons
        if electron.valence
        and _electron_dimension_id(record.symbol, occurrence, electron.index) not in paired_ids
    )
    carried = (
        ("symbol", record.symbol),
        ("Z", str(record.Z)),
        ("period", str(record.period)),
        ("group", str(record.group)),
        ("A", str(record.A)),
        ("electron-configuration", record.configuration),
        ("valence-n", str(record.valence_n)),
        ("valence-electrons", str(record.valence_electrons)),
        ("pairing-count", str(len(pairing_ids))),
        ("unpaired-valence-count", str(len(unpaired))),
        ("unpaired-valence-lm", ",".join(f"{e.l}:{e.m_l}" for e in unpaired) or "none"),
        ("bonding-surface-count", str(len(surface_ids))),
        ("bonding-surface-ids", ",".join(surface_ids) or "none"),
        ("promoted-unpaired-count", str(len(promoted_unpaired))),
        ("promoted-unpaired-lm", ",".join(f"{e.l}:{e.m_l}" for e in promoted_unpaired) or "none"),
        ("valence-angular-ids", ",".join(e.angular_id for e in record.electrons if e.valence)),
        ("promoted", "true" if promoted else "false"),
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


def construct_primary_research_atom(
    *, occurrence: int = 0, promoted: bool = False
) -> PublicGonolReceipt:
    """Close the primary research atom. Carbon is that atom for this candidate."""

    return construct_element_gonol(
        PRIMARY_RESEARCH_ATOM, occurrence=occurrence, promoted=promoted
    )


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


def nucleus_of(gonol: ClosedPublicGonol) -> ClosedPublicGonol:
    for item in gonol.participants:
        if item.relation == NUCLEUS_RELATION:
            return item
    raise KeyError("nucleus")


def electrons_of(gonol: ClosedPublicGonol) -> tuple[ClosedPublicGonol, ...]:
    return tuple(
        electron
        for shell in gonol.participants
        if shell.relation == SHELL_RELATION
        for electron in shell.participants
        if electron.relation == ELECTRON_RELATION
    )


def _is_electron_axis(axis_id: str) -> bool:
    return axis_id.startswith("epac.electron:")


def pairing_couplings(gonol: ClosedPublicGonol) -> tuple[tuple[str, str], ...]:
    """Declared occupancy-2 electron-electron pairings already closed inside the atom."""

    pairs: list[tuple[str, str]] = []
    for part in (gonol.structure or {}).get("parts", ()):
        declared = tuple(part["coupling"])
        if len(declared) == 2 and _is_electron_axis(declared[0]) and _is_electron_axis(declared[1]):
            pairs.append((declared[0], declared[1]))
    return tuple(pairs)


def paired_electron_ids(gonol: ClosedPublicGonol) -> frozenset[str]:
    return frozenset(electron_id for pair in pairing_couplings(gonol) for electron_id in pair)


def bonding_surfaces(gonol: ClosedPublicGonol) -> tuple[ClosedPublicGonol, ...]:
    """Leftover unpaired valence electrons whose ``(nucleus, e_i)`` remain exposed.

    Pairing is already closed inside the atom. These leftover incidences are
    the bonding surfaces a later molecule may match. Core and paired electrons
    stay inside.
    """

    paired = paired_electron_ids(gonol)
    nucleus_id = nucleus_of(gonol).source_id
    nucleus_electron_ids = {
        tuple(part["coupling"])[1]
        for part in (gonol.structure or {}).get("parts", ())
        if len(part["coupling"]) == 2 and part["coupling"][0] == nucleus_id
    }
    surfaces: list[ClosedPublicGonol] = []
    for electron in electrons_of(gonol):
        options = dict(electron.carried_options)
        if options.get("valence") != "true":
            continue
        if electron.source_id in paired:
            continue
        if electron.source_id not in nucleus_electron_ids:
            raise ValueError(
                f"{electron.source_id} is valence and unpaired but has no leftover "
                f"({nucleus_id}, electron) incidence"
            )
        surfaces.append(electron)
    return tuple(surfaces)


def bonding_surface_couplings(gonol: ClosedPublicGonol) -> tuple[tuple[str, str], ...]:
    """Published leftover ``(nucleus, electron_i)`` bonding surfaces."""

    nucleus_id = nucleus_of(gonol).source_id
    return tuple((nucleus_id, electron.source_id) for electron in bonding_surfaces(gonol))


def unpaired_valence_electrons(gonol: ClosedPublicGonol) -> tuple[ClosedPublicGonol, ...]:
    """Unpaired valence electron gonols published as bonding surfaces."""

    return bonding_surfaces(gonol)


def nuclear_charge(gonol: ClosedPublicGonol) -> int:
    return int(dict(nucleus_of(gonol).carried_options)["Z"])


def electron_lm(electron: ClosedPublicGonol) -> tuple[int, int]:
    options = dict(electron.carried_options)
    return (int(options["l"]), int(options["m_l"]))
