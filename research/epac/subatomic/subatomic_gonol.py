"""Subatomic gonol constructor.

Closes one subatomic element gonol per supported symbol from three source
layers, all kept separately addressable:

1. subatomic nucleus identity — proton/neutron Public Gonol carrier positions
   and native Möbius t-state framing (``element_affixiation_candidate``);
2. nuclear harmonic relations — the physically sourced candidates from
   ``nuclear_harmonic_candidates`` (alpha-cluster recurrence, N/Z ratio,
   spin-parity, binding-per-nucleon commensurability, p<->n inversion);
3. quantum layer — full atomic electron-shell structure from ``epac_atomic``
   (n, l, m_l, m_s, shell, subshell, angular id, radial nodes, Slater Z_eff,
   Rydberg energy).

Construction uses the EDCM gonol candidate constructor
(``edcm.gonol.construct_gonol``) with ``ucns.public_gonol`` supplied as the
explicit geometry authority. No Public Gonol position operation and no Möbius
coupling law is invented.

Status: CROSS-DOMAIN-HYPOTHESIS / implemented candidate. Not selected canon.

Usage guidance:

    PYTHONPATH="<epac>:<edcm>:<ucns>/src" python3 - <<'PY'
    from subatomic_gonol import construct_subatomic_gonol, replay_subatomic_gonol

    receipt = construct_subatomic_gonol("He")
    print(receipt.receipt_digest)
    assert replay_subatomic_gonol(receipt) == receipt.receipt_digest
    PY
"""

import os
import sys

_PARENT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _PARENT not in sys.path:
    sys.path.insert(0, _PARENT)

from edcm.gonol import (  # noqa: E402
    ClosedGonol,
    GonolReceipt,
    construct_gonol,
    replay_gonol,
)
from epac_atomic import AtomicRecord, atomic_record  # noqa: E402

import element_affixiation_candidate as identity  # noqa: E402
import nuclear_harmonic_candidates as harmonics  # noqa: E402

# === MODULE_BUILD ===
# id: epac_subatomic_gonol
#   module_name: subatomic_gonol
#   module_kind: experiment
#   summary: closes one subatomic element gonol per symbol from subatomic nucleus identity, nuclear harmonic relations, and quantum-layer electron shells via the EDCM gonol candidate constructor
#   owner: The Interdependency
#   public_surface: SUPPORTED_SYMBOLS, construct_subatomic_gonol, replay_subatomic_gonol, subatomic_receipt_record
#   internal_surface: _geometry_authority, _nucleus_participant, _shell_participants, _electron_options, _harmonic_rows
#   auth_boundary: none
#   storage_boundary: none
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: subatomic.test_subatomic_gonol
#   rollout: local candidate module under stack/research/epac/subatomic/
#   rollback: remove module, tests, and generated receipts
#   requires: edcm_gonol, epac_atomic, epac_subatomic_element_affixiation_candidate, epac_subatomic_nuclear_harmonic_candidates
#   since: 2026-08-22
#   unresolved: UCNS position operations; UCNS harmonic notation; EDCM gonol candidate is not selected canon
# === END MODULE_BUILD ===

# === CONTRACTS ===
# id: subatomic_gonol_combines_three_sources
#   given: a subatomic gonol is constructed for a supported symbol
#   then: participants are one subatomic nucleus gonol plus quantum-layer electron-shell gonols, and carried options include subatomic identity, harmonic relation results, and electron configuration
#   class: construction
#
# id: subatomic_gonol_replays_byte_identical
#   given: a subatomic gonol receipt
#   then: replay_gonol reproduces the same receipt_digest
#   class: correctness
#
# id: subatomic_gonol_keeps_layers_distinct
#   given: constructed gonol participants
#   then: nucleus (subatomic layer) and electron shells (quantum layer) remain separately addressable with their own source_ids; scales are not interchanged
#   class: doctrine
#
# id: subatomic_gonol_invents_no_geometry
#   given: construction
#   then: UCNS geometry is consumed only as the explicit public_gonol authority; no position operation or Möbius coupling law is defined or inferred
#   class: safety
#
# id: subatomic_gonol_stays_cross_domain_hypothesis
#   given: any receipt
#   then: standing is implemented-candidate, selection_effect is none, and no physics validation or canon promotion is claimed
#   class: doctrine
# === END CONTRACTS ===

SUPPORTED_SYMBOLS: tuple[str, ...] = ("H", "He", "Li", "C")


def _geometry_authority():
    from ucns import public_gonol

    return public_gonol


def _harmonic_rows(symbol: str) -> tuple[harmonics.HarmonicCandidate, ...]:
    return tuple(
        candidate
        for candidate in harmonics.CANDIDATES
        if any(participant.startswith(f"{symbol}-") for participant in candidate.participants)
    )


def _electron_options(record: AtomicRecord, electron) -> tuple[tuple[str, str], ...]:
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


def _nucleus_participant(symbol: str, occurrence: int) -> ClosedGonol:
    element = identity.affixiate_element(symbol)
    carried = [
        ("Z", str(element.Z)),
        ("A", str(element.A)),
        ("proton-positions", ",".join(str(i) for i in element.proton_positions)),
        ("proton-glyphs", "".join(element.proton_glyphs)),
        (
            "neutron-positions",
            ",".join(str(i) for i in element.neutron_positions) or "none",
        ),
        ("neutron-glyphs", "".join(element.neutron_glyphs) or "none"),
        ("mobius-t0-frame", element.t_states[0]["frame"]),
        ("mobius-t1-frame", element.t_states[1]["frame"]),
        ("mobius-t2-frame", element.t_states[2]["frame"]),
    ]
    for candidate in _harmonic_rows(symbol):
        import json as _json

        carried.append(
            (
                f"harmonic:{candidate.candidate_id}",
                _json.dumps(
                    harmonics.recurrence_test(candidate), sort_keys=True, separators=(",", ":")
                ),
            )
        )
    receipt = construct_gonol(
        scale="word",
        source="nuc",
        source_id=f"epac.subatomic.nucleus:{symbol}#{occurrence}",
        relation="epac.subatomic.nucleus",
        carried_options=carried,
        geometry_authority=_geometry_authority(),
        occurrence=occurrence,
    )
    return receipt.gonol


def _shell_participants(record: AtomicRecord, occurrence: int) -> tuple[ClosedGonol, ...]:
    by_n: dict[int, list] = {}
    for electron in record.electrons:
        by_n.setdefault(electron.n, []).append(electron)
    shells: list[ClosedGonol] = []
    for n in sorted(by_n):
        members: list[ClosedGonol] = []
        for electron in by_n[n]:
            electron_receipt = construct_gonol(
                scale="word",
                source="e",
                source_id=f"epac.subatomic.electron:{record.symbol}#{occurrence}:{electron.index}",
                relation="epac.atomic.electron",
                carried_options=_electron_options(record, electron),
                geometry_authority=_geometry_authority(),
                occurrence=electron.index,
            )
            members.append(electron_receipt.gonol)
        shell_receipt = construct_gonol(
            scale="word",
            source=f"n{n}",
            source_id=f"epac.subatomic.shell:{record.symbol}#{occurrence}:n{n}",
            relation="epac.atomic.shell",
            participants=members,
            geometry_authority=_geometry_authority(),
            occurrence=n,
        )
        shells.append(shell_receipt.gonol)
    return tuple(shells)


def construct_subatomic_gonol(symbol: str, *, occurrence: int = 0) -> GonolReceipt:
    """Close one subatomic element gonol: nucleus + electron shells."""
    if symbol not in SUPPORTED_SYMBOLS:
        raise ValueError(
            f"subatomic gonol supports {SUPPORTED_SYMBOLS}; got {symbol!r}"
        )
    record = atomic_record(identity.ISOTOPE_DEFAULTS[symbol][0])
    nucleus = _nucleus_participant(symbol, occurrence)
    shells = _shell_participants(record, occurrence)
    harmonic_surviving = ",".join(
        candidate.candidate_id
        for candidate in _harmonic_rows(symbol)
        if any(harmonics.recurrence_test(candidate).values())
    )
    carried = [
        ("Z", str(record.Z)),
        ("period", str(record.period)),
        ("group", str(record.group)),
        ("A", str(record.A)),
        ("electron-configuration", record.configuration),
        ("valence-electrons", str(record.valence_electrons)),
        ("harmonic-surviving", harmonic_surviving or "none"),
        ("status", "CROSS-DOMAIN-HYPOTHESIS"),
    ]
    return construct_gonol(
        scale="word",
        source=symbol,
        source_id=f"epac.subatomic.element:{symbol}#{occurrence}",
        relation="epac.subatomic.element",
        participants=(nucleus, *shells),
        carried_options=carried,
        geometry_authority=_geometry_authority(),
        occurrence=occurrence,
    )


def replay_subatomic_gonol(receipt: GonolReceipt) -> str:
    """Replay a completed subatomic gonol receipt; returns its digest."""
    return replay_gonol(receipt=receipt).receipt_digest


def subatomic_receipt_record(receipt: GonolReceipt) -> dict:
    """JSON-safe summary of one subatomic gonol receipt."""
    gonol = receipt.gonol
    return {
        "constructor_id": receipt.constructor_id,
        "constructor_version": receipt.constructor_version,
        "standing": receipt.standing,
        "selection_effect": receipt.selection_effect,
        "source_id": receipt.source_id,
        "receipt_digest": receipt.receipt_digest,
        "atomic_id": gonol.atomic_id,
        "scale": gonol.scale,
        "relation": gonol.relation,
        "participant_kinds": [
            ("nucleus" if "nucleus" in p.source_id else "shell") for p in gonol.participants
        ],
        "carried_options": list(gonol.carried_options),
        "nonclaims": list(receipt.nonclaims),
        "hmmm": list(receipt.hmmm),
    }


__all__ = [
    "SUPPORTED_SYMBOLS",
    "construct_subatomic_gonol",
    "replay_subatomic_gonol",
    "subatomic_receipt_record",
]
