# === MODULE_BUILD ===
# id: weave_message_byte_origin
#   module_name: message_origin
#   module_kind: schema
#   summary: one message origin containing ordered byte occurrences with eight-circle attachments
#   owner: Erin Spencer
#   public_surface: ByteOccurrence, MessageOrigin, construct_origin, construct_at
#   internal_surface: strict occurrence and scope validation
#   auth_boundary: none
#   storage_boundary: none
#   network_boundary: none
#   user_data_boundary: read
#   admin_only: false
#   tests: tests/test_message_origin.py
#   rollout: replaces PR 74 bit-axis feedback substitution
#   rollback: revert this repair as one transaction without restoring the rejected cipher
#   unresolved: native UCHC binding and full-byte keyed positional evolution
# === END MODULE_BUILD ===
# === CONTRACTS ===
# id: weave_message_origin_contains_bytes
#   given: an admitted raw-byte message
#   then: its origin contains one ordered occurrence per byte, not eight independent message axes per byte
#   class: correctness
# id: weave_byte_occurrences_preserve_scope
#   given: repeated byte values at one origin or equal messages at distinct named origins
#   then: occurrence order and supplied origin identity remain distinct and recoverable
#   class: correctness
# === END CONTRACTS ===
"""Message -> byte occurrences -> eight-circle placements.

Usage: origin = construct_origin(b"AA", identity="message-1")
       byte_state = construct_at(origin, 0, full_key_record, eight_positions)

These are Weave construction records, not a copied UCHC constructor or a new
UCNS geometry. An origin identifier scopes occurrences; it is not a hash of the
message, a nonce, or a source of cryptographic secrecy. Native origin/axis
integration and dynamic positional encryption remain unimplemented.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from fractions import Fraction
from .eight_circle import ByteConstruction, FullKeySet, construct_byte, _identity, _index


@dataclass(frozen=True)
class ByteOccurrence:
    origin_id: str
    index: int
    value: int = field(repr=False)

    def __post_init__(self) -> None:
        _identity(self.origin_id)
        if type(self.index) is not int or self.index < 0:
            raise ValueError("byte occurrence index must be nonnegative")
        _index(self.value, 256, "byte")


@dataclass(frozen=True)
class MessageOrigin:
    identity: str
    bytesets: tuple[ByteOccurrence, ...] = field(repr=False)

    def __post_init__(self) -> None:
        _identity(self.identity)
        if (type(self.bytesets) is not tuple
                or any(type(b) is not ByteOccurrence for b in self.bytesets)):
            raise TypeError("message participants must be a tuple of byte occurrences")
        for index, occurrence in enumerate(self.bytesets):
            if occurrence.index != index or occurrence.origin_id != self.identity:
                raise ValueError("byte occurrence order and origin must match this message")

    @property
    def byte_length(self) -> int:
        return len(self.bytesets)

    def recover_bytes(self) -> bytes:
        """Read the exact retained source construction, not decrypt a ciphertext."""
        return bytes(b.value for b in self.bytesets)


def construct_origin(data: bytes, *, identity: str) -> MessageOrigin:
    """Admit each raw byte once at its caller-named message origin."""
    if type(data) is not bytes:
        raise TypeError("raw bytes required; no text normalization")
    _identity(identity)
    return MessageOrigin(identity, tuple(
        ByteOccurrence(identity, index, value) for index, value in enumerate(data)
    ))


def construct_at(origin: MessageOrigin, byte_index: int, full: FullKeySet,
                 positions: tuple[Fraction, ...]) -> ByteConstruction:
    """Attach one whole byte, carrying its source occurrence into all placements."""
    if type(origin) is not MessageOrigin:
        raise TypeError("a MessageOrigin is required")
    _index(byte_index, origin.byte_length, "byte index")
    occurrence = origin.bytesets[byte_index]
    return construct_byte(occurrence.value, full, positions,
                          origin_id=origin.identity, byte_index=occurrence.index)
