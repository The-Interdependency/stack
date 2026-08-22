# === MODULE_BUILD ===
# id: ucns_public_gonol_geometry
#   module_name: public_gonol
#   module_kind: geometry
#   summary: exact 157-position Public Gonol carrier; every glyph position is a Public Gonol function position without linguistic subclassing
#   owner: Erin Spencer
#   public_surface: PUBLIC_GONOL_157, PUBLIC_GONOL_SHA256, PublicGonolPosition, public_gonol_position, public_gonol_function, public_gonol_sha256
#   internal_surface: _POSITION
#   auth_boundary: exact inherited Public Gonol arrangement and digest
#   storage_boundary: immutable constants only
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: tests.test_public_gonol
#   rollout: geometry-only UCNS carrier floor
#   rollback: restore the prior file from Git history
#   requires: none
#   since: 2026-08-20
#   unresolved: the exact geometric operation expressed by each function position beyond its carrier identity
# === END MODULE_BUILD ===

# === CONTRACTS ===
# id: public_gonol_has_exactly_157_unique_positions
#   given: the Public Gonol carrier is imported
#   then: exactly 157 unique one-scalar glyphs retain their exact order and pinned digest
#   class: correctness
#   since: 2026-08-20
#
# id: every_public_gonol_glyph_is_a_function_position
#   given: any admitted Public Gonol glyph or index
#   then: one PublicGonolPosition is returned without letter, digit, punctuation, lexical, or semantic subclassing
#   class: doctrine
#   since: 2026-08-20
# === END CONTRACTS ===

"""Geometry-only Public Gonol carrier.

Every admitted glyph is a Public Gonol function position.  UCNS does not divide
these positions into letters versus punctuation, symbols versus digits, or any
other linguistic class.  This module records only carrier geometry: exact order,
position, glyph identity, and the inherited arrangement digest.

What a position *does* in a particular construction is not guessed here.  A
function may be identity-like (for example, "carry on") or may participate in a
larger geometric relation, but that operation requires its own geometric
construction and evidence.
"""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json

PUBLIC_GONOL_SHA256 = "55d10c84529a4d7bc7714786357e977b68d9df2ac3f73d20e229580b552c2ef5"

PUBLIC_GONOL_157: tuple[str, ...] = (
    " ", "A", "!", '"', "B", "#", "$", "C", "%", "(", "D", "&", "'", "E", "1", "*",
    "F", "+", "[", "G", ",", "-", "H", ".", "/", "I", "3", "{", "J", ":", ";", "K",
    "=", "?", "L", "<", "@", "M", "5", "\\", "N", "^", "_", "O", "‘", "`", "P", "|",
    "~", "Q", "7", "…", "R", "“", "—", "S", "–", "·", "T", "°", "«", "U", "9", "±",
    "V", "×", "÷", "W", "√", "∂", "X", "∫", "∑", "Y", "∏", "∇", "Z", "∞", "≈", "≠",
    "a", "≤", "≥", "b", "→", "←", "c", ")", "↑", "d", "↓", "2", "e", "↔", "⊕", "f",
    "]", "⊗", "g", "⊙", "⊘", "h", "∈", "4", "i", "}", "∉", "j", "⊂", "⊃", "k", "⊆",
    ">", "l", "⊇", "6", "m", "∩", "∪", "n", "∧", "’", "o", "∨", "¬", "p", "∀", "8",
    "q", "∃", "”", "r", "⊢", "⊨", "s", "∴", "∵", "t", "»", "0", "u", "≡", "ψ", "v",
    "φ", "ω", "w", "α", "β", "x", "γ", "δ", "y", "λ", "π", "z", "σ",
)

_POSITION = {glyph: index for index, glyph in enumerate(PUBLIC_GONOL_157)}


def public_gonol_sha256(arrangement: tuple[str, ...] = PUBLIC_GONOL_157) -> str:
    payload = json.dumps(tuple(arrangement), ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    return sha256(payload).hexdigest()


@dataclass(frozen=True, slots=True)
class PublicGonolPosition:
    """One exact glyph/function position on the Public Gonol carrier."""

    index: int
    glyph: str

    def __post_init__(self) -> None:
        if isinstance(self.index, bool) or not isinstance(self.index, int):
            raise TypeError("Public Gonol index must be an integer")
        if not 0 <= self.index < len(PUBLIC_GONOL_157):
            raise ValueError("Public Gonol index outside carrier")
        if PUBLIC_GONOL_157[self.index] != self.glyph:
            raise ValueError("glyph does not occupy the declared Public Gonol position")


def public_gonol_position(glyph: str) -> int | None:
    """Return the exact carrier position of one glyph, or None if not admitted."""

    if not isinstance(glyph, str) or len(glyph) != 1:
        raise TypeError("glyph must be exactly one Unicode scalar")
    if 0xD800 <= ord(glyph) <= 0xDFFF:
        raise ValueError("surrogate code points are not Unicode scalars")
    return _POSITION.get(glyph)


def public_gonol_function(value: int | str) -> PublicGonolPosition:
    """Return one carrier function position by exact index or glyph."""

    if isinstance(value, bool):
        raise TypeError("Public Gonol function requires an integer index or glyph")
    if isinstance(value, int):
        if not 0 <= value < len(PUBLIC_GONOL_157):
            raise ValueError("Public Gonol index outside carrier")
        return PublicGonolPosition(value, PUBLIC_GONOL_157[value])
    position = public_gonol_position(value)
    if position is None:
        raise ValueError("glyph is not on the Public Gonol carrier")
    return PublicGonolPosition(position, value)


if len(PUBLIC_GONOL_157) != 157:
    raise RuntimeError("Public Gonol arity mismatch")
if len(set(PUBLIC_GONOL_157)) != 157:
    raise RuntimeError("Public Gonol positions must be unique")
if not all(len(glyph) == 1 and not 0xD800 <= ord(glyph) <= 0xDFFF for glyph in PUBLIC_GONOL_157):
    raise RuntimeError("every Public Gonol glyph must be one Unicode scalar")
if PUBLIC_GONOL_157[0] != " ":
    raise RuntimeError("SPACE must remain at Public Gonol origin")
if public_gonol_sha256() != PUBLIC_GONOL_SHA256:
    raise RuntimeError("Public Gonol arrangement digest mismatch")


__all__ = [
    "PUBLIC_GONOL_157",
    "PUBLIC_GONOL_SHA256",
    "PublicGonolPosition",
    "public_gonol_function",
    "public_gonol_position",
    "public_gonol_sha256",
]
