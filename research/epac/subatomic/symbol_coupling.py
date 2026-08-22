"""Symbol-abbreviation coupling for subatomic element gonols.

Adds each element's one- or two-letter abbreviation as a closed symbol gonol
and couples it to the closed subatomic element gonol through the EPAC Public
Gonol constructor.

- one-letter symbols (H, B, C, ...) close from a single identity glyph;
- two-letter symbols (He, Li, Be, Fe, ...) close from two ordered character
  gonols affixiated at arity 2;
- the coupled gonol declares exactly two participants: element gonol and
  symbol gonol. Geometry follows the declared coupling only.

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

from epac_public_gonol import (
    ClosedPublicGonol,
    PublicGonolReceipt,
    construct_public_gonol,
    replay_public_gonol,
)

import subatomic_gonol

SUPPORTED_SYMBOLS: tuple[str, ...] = subatomic_gonol.SUPPORTED_SYMBOLS

RELATION_SYMBOL = "epac.symbol.abbreviation"
RELATION_COUPLING = "epac.symbol-coupling"


def construct_symbol_gonol(symbol: str, *, occurrence: int = 0) -> PublicGonolReceipt:
    """Close one symbol-abbreviation gonol from its exact ordered characters."""
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
    return construct_public_gonol(
        source_id=f"epac.symbol:{symbol}#{occurrence}",
        relation=RELATION_SYMBOL,
        participants=tuple(glyphs),
        occurrence=occurrence,
        carried_options=(
            ("symbol", symbol),
            ("abbreviation-length", str(len(symbol))),
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
