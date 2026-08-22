"""Symbol-abbreviation coupling for subatomic element gonols.

Adds each element's one- or two-letter abbreviation as a closed symbol gonol
and couples it to the closed subatomic element gonol through the EPAC Public
Gonol constructor.

- one-letter symbols (H, B, C, ...) close from a single identity glyph;
- two-letter symbols (He, Li, Be, Fe, ...) close from two ordered character
  gonols; each letter instance has its own oriented hub coupling ``(z, x_i)``
  / ``(z, y_j)``. That is the three-dimensional structure for a two-letter
  abbreviation.
- the element/symbol coupling declares exactly two participants: element gonol
  and symbol gonol. Geometry follows declared couplings only.

Status: CROSS-DOMAIN-HYPOTHESIS / implemented candidate. Not selected canon.

Usage guidance:

    from symbol_coupling import couple_symbol

    receipt = couple_symbol("Fe")
    print(receipt.receipt_digest)
"""

# === MODULE_BUILD ===
# id: epac_subatomic_symbol_coupling
#   module_name: symbol_coupling
#   module_kind: experiment
#   summary: couples each subatomic element gonol with its closed one/two-letter symbol-abbreviation gonol through the EPAC Public Gonol constructor
#   owner: The Interdependency
#   public_surface: SUPPORTED_SYMBOLS, construct_symbol_gonol, couple_symbol, replay_symbol_coupling
#   internal_surface: none
#   auth_boundary: none
#   storage_boundary: none
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: subatomic.test_symbol_coupling
#   rollout: local candidate module under stack/research/epac/subatomic/
#   rollback: remove module, tests, and generated receipts
#   requires: epac_public_gonol, epac_subatomic_gonol
#   since: 2026-08-22
#   unresolved: two-letter symbols have no single Public Gonol glyph; coupling is declared, not geometry-inferred
# === END MODULE_BUILD ===

# === CONTRACTS ===
# id: symbol_gonol_preserves_exact_abbreviation
#   given: a symbol gonol for element symbol S
#   then: participants are the exact ordered characters of S with one identity glyph each, and carried abbreviation-length equals len(S)
#   class: correctness
#
# id: symbol_every_letter_instance_has_oriented_hub_coupling
#   given: a symbol gonol with one or two letter instances
#   then: every letter instance has its own declared (z, instance) coupling; two-letter symbols occupy three participating dimensions without declaring a ternary coupling
#   class: construction
#
# id: symbol_coupling_arity_two
#   given: a symbol-coupled gonol
#   then: exactly two participants (element gonol, symbol gonol) are declared and the coupling declares arity 2
#   class: correctness
#
# id: symbol_coupling_replays_byte_identical
#   given: a symbol-coupled receipt
#   then: replay_public_gonol reproduces the same receipt_digest
#   class: correctness
#
# id: symbol_coupling_stays_cross_domain_hypothesis
#   given: any symbol-coupled receipt
#   then: standing is implemented-candidate, selection_effect is none, and no canon is selected
#   class: doctrine
# === END CONTRACTS ===

from __future__ import annotations

import os
import sys

_PARENT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _PARENT not in sys.path:
    sys.path.insert(0, _PARENT)

from epac_dimensional_arity import (  # noqa: E402
    geometry_from_declared_couplings,
    oriented_instance_couplings,
    space,
)
from epac_public_gonol import (  # noqa: E402
    ClosedPublicGonol,
    PublicGonolReceipt,
    construct_public_gonol,
    replay_public_gonol,
)
from extended_atomic import SYMBOL_TO_Z  # noqa: E402

import subatomic_gonol  # noqa: E402

SUPPORTED_SYMBOLS: tuple[str, ...] = subatomic_gonol.SUPPORTED_SYMBOLS

RELATION_SYMBOL = "epac.symbol.abbreviation"
RELATION_COUPLING = "epac.symbol-coupling"


def construct_symbol_gonol(symbol: str, *, occurrence: int = 0) -> PublicGonolReceipt:
    """Close one symbol-abbreviation gonol from its exact ordered characters.

    Every letter instance has declared ``(z, instance)``. Two letters are two
    instances, so the structure is ``(z, x)`` and ``(z, y)``.
    """
    if symbol not in SUPPORTED_SYMBOLS:
        raise ValueError(f"symbol {symbol!r} is outside the supported element table")
    characters = tuple(symbol)
    glyphs: list[ClosedPublicGonol] = []
    for index, character in enumerate(characters):
        glyphs.append(
            construct_public_gonol(
                source_id=f"epac.symbol.character:{symbol}#{occurrence}:{index}:{character}",
                relation="epac.symbol.character",
                identity_glyph=character,
                occurrence=index,
            ).gonol
        )
    hub_id = f"epac.symbol:{symbol}#{occurrence}"
    instance_ids = tuple(item.source_id for item in glyphs)
    declared = space(
        (hub_id, *instance_ids),
        [[hub_id, instance_id] for instance_id in instance_ids],
        charges={hub_id: int(SYMBOL_TO_Z[symbol])},
    )
    instance_couplings = oriented_instance_couplings(
        declared, hub_id=hub_id, instance_ids=instance_ids
    )
    geometry = geometry_from_declared_couplings(declared)
    return construct_public_gonol(
        source_id=hub_id,
        relation=RELATION_SYMBOL,
        participants=tuple(glyphs),
        occurrence=occurrence,
        couplings=geometry["couplings"],
        structure=geometry["structure"],
        carried_options=(
            ("symbol", symbol),
            ("abbreviation-length", str(len(symbol))),
            (
                "oriented-instance-couplings",
                ";".join(f"({hub},{inst})" for hub, inst in instance_couplings),
            ),
        ),
    )


def couple_symbol(symbol: str, *, occurrence: int = 0) -> PublicGonolReceipt:
    """Couple a closed element gonol with its closed symbol-abbreviation gonol."""
    element = subatomic_gonol.construct_subatomic_gonol(symbol, occurrence=occurrence).gonol
    symbol_gonol = construct_symbol_gonol(symbol, occurrence=occurrence).gonol
    return construct_public_gonol(
        source_id=f"epac.symbol-coupled:{symbol}#{occurrence}",
        relation=RELATION_COUPLING,
        participants=(element, symbol_gonol),
        couplings=(
            {
                "relation": RELATION_COUPLING,
                "arity": 2,
                "dimensions": [element.source_id, symbol_gonol.source_id],
            },
        ),
        occurrence=occurrence,
        carried_options=(("symbol", symbol),),
    )


def replay_symbol_coupling(receipt: PublicGonolReceipt) -> str:
    return replay_public_gonol(receipt).receipt_digest


__all__ = [
    "RELATION_COUPLING",
    "RELATION_SYMBOL",
    "SUPPORTED_SYMBOLS",
    "construct_symbol_gonol",
    "couple_symbol",
    "replay_symbol_coupling",
]
