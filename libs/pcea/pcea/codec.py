# ratios: loc_comments=64:55 imports_exports=1:5 calls_definitions=34:10
# GPT/Claude generated; context, prompt Erin Spencer
"""
Möbius disk codec for PCEA.

Values are mapped to positions on a Möbius disk before encryption:
- mobius_encode: signed integer → unsigned position in {0..2^W - 1}
- mobius_decode: unsigned position → signed integer

The two sides of the disk are the two two's-complement halves. Positive
values sit in the lower half, negative values wrap to the upper half via
Python's natural modular arithmetic. An observer sees only the encrypted
position — the side (sign) is invisible without the key.

Fixed-width base-p encoding ensures the encrypted output always has exactly
k = digit_count(p, word_bits) digits, so the magnitude of the original
value does not leak through output length.

    mobius_encode(v, word_bits)   -> u in {0..2^W - 1}
    mobius_decode(u, word_bits)   -> v (signed)
    digit_count(p, word_bits)     -> k (fixed digit count for prime p)
    to_fixed(u, p, k)             -> k digits in {0..p-1}, little-endian
    from_fixed(digits, p)         -> unsigned integer
"""

# === MODULE_BUILD ===
# id: pcea_codec
#   module_name: codec
#   module_kind: adapter
#   summary: Mobius disk codec: signed<->unsigned position mapping and fixed-width base-p digit encoding with explicit word-range guards
#   owner: Erin Spencer
#   public_surface: mobius_encode, mobius_decode, digit_count, to_fixed, from_fixed
#   internal_surface: none
#   auth_boundary: none
#   storage_boundary: none
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: tests.test_codec
#   rollout: default_enabled
#   rollback: remove module and its references
#   requires: none
#   since: 2026-06-02
#   unresolved: none
# === END MODULE_BUILD ===

# === CONTRACTS ===
# id: codec_rejects_out_of_range_signed_words
#   given: mobius_encode receives a value outside the signed word_bits range
#   then:  raises ValueError instead of wrapping to a different plaintext
#   class: correctness
#
# id: fixed_width_codec_rejects_overflow
#   given: to_fixed receives an unsigned value that cannot fit in k base-p digits
#   then:  raises ValueError instead of truncating high-order digits
#   class: correctness
# === END CONTRACTS ===

from __future__ import annotations


def _validate_word_bits(word_bits: int) -> None:
    if not isinstance(word_bits, int) or word_bits < 1:
        raise ValueError("word_bits must be a positive integer")


def _validate_prime_base(p: int) -> None:
    if not isinstance(p, int) or p < 2:
        raise ValueError("p must be an integer base >= 2")


def _signed_bounds(word_bits: int) -> tuple[int, int]:
    _validate_word_bits(word_bits)
    half = 1 << (word_bits - 1)
    return -half, half - 1


def _validate_signed_word(v: int, word_bits: int) -> None:
    if not isinstance(v, int):
        raise ValueError("value must be an integer")
    lo, hi = _signed_bounds(word_bits)
    if v < lo or v > hi:
        raise ValueError(f"value must fit signed word_bits range [{lo}, {hi}]")


def _validate_unsigned_position(u: int, word_bits: int) -> None:
    if not isinstance(u, int):
        raise ValueError("unsigned position must be an integer")
    _validate_word_bits(word_bits)
    if u < 0 or u >= (1 << word_bits):
        raise ValueError(f"unsigned position must be in [0, {1 << word_bits})")


def mobius_encode(v: int, word_bits: int) -> int:
    """Map signed integer v to unsigned position on the Möbius disk."""
    _validate_signed_word(v, word_bits)
    mask = (1 << word_bits) - 1
    return v & mask


def mobius_decode(u: int, word_bits: int) -> int:
    """Map unsigned Möbius disk position back to signed integer."""
    _validate_unsigned_position(u, word_bits)
    half = 1 << (word_bits - 1)
    return u if u < half else u - (1 << word_bits)


def digit_count(p: int, word_bits: int) -> int:
    """Fixed number of base-p digits needed to cover the full Möbius disk (2^word_bits positions)."""
    _validate_prime_base(p)
    _validate_word_bits(word_bits)
    k = 0
    capacity = 1
    while capacity < (1 << word_bits):
        capacity *= p
        k += 1
    return k


def to_fixed(u: int, p: int, k: int) -> list[int]:
    """Encode unsigned integer u as exactly k standard base-p digits, little-endian."""
    _validate_prime_base(p)
    if not isinstance(k, int) or k < 0:
        raise ValueError("k must be a non-negative integer")
    if not isinstance(u, int):
        raise ValueError("unsigned value must be an integer")
    capacity = p ** k
    if u < 0 or u >= capacity:
        raise ValueError(f"unsigned value must fit in {k} base-{p} digits")
    digits: list[int] = []
    for _ in range(k):
        digits.append(u % p)
        u //= p
    return digits


def from_fixed(digits: list[int], p: int) -> int:
    """Reconstruct unsigned integer from standard base-p digits, little-endian."""
    _validate_prime_base(p)
    result = 0
    power = 1
    for d in digits:
        if not isinstance(d, int) or d < 0 or d >= p:
            raise ValueError(f"digit must be an integer in [0, {p})")
        result += d * power
        power *= p
    return result
# ratios: loc_comments=64:55 imports_exports=1:5 calls_definitions=34:10
