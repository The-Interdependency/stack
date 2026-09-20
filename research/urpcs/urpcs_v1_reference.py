#!/usr/bin/env python3
"""URPCS v1 reference encoder/decoder and vector generator.

Status
------
Research/reference code for accepted URPCS Laws 1-13 and the bounded vector
profile.  It proves deterministic construction and round-trip behavior for the
published fixtures.  It does not claim confidentiality or production fitness.

Usage
-----
    python3 urpcs_v1_reference.py --self-test
    python3 urpcs_v1_reference.py --write-vectors urpcs-v1-vectors.json

The implementation uses only Python's standard library.  It deliberately owns
the small deterministic-CBOR subset and KMAC256 implementation needed by the
wire law so package version changes cannot silently change fixture bytes.

Limitations
-----------
The harness accepts at most one input byte and depth one.  The state-slot CAS
test models the host obligation in memory; it is not a durable-storage proof.
"""

# === MODULE_BUILD ===
# id: urpcs_v1_reference
#   module_name: urpcs_v1_reference
#   module_kind: experiment
#   summary: executable reference and deterministic fixture generator for URPCS v1 Laws 1-13
#   owner: The-Interdependency/stack research/urpcs
#   public_surface: encrypt, decrypt, generate_vectors, command-line self-test and vector writer
#   internal_surface: deterministic CBOR subset, Keccak/cSHAKE/KMAC256, witness and layer codecs
#   auth_boundary: none
#   storage_boundary: write
#   network_boundary: none
#   user_data_boundary: read
#   admin_only: false
#   tests: research/urpcs/tests/test_reference.py
#   rollout: stack-local research only; no production import or encryption claim
#   rollback: remove research/urpcs and its stack research-participant projections as one transaction
#   unresolved: independent decoder interoperability, confidentiality model, production key lifecycle
# === END MODULE_BUILD ===

# === CONTRACTS ===
# id: urpcs_bounded_roundtrip
#   given: a permitted harness plaintext, valid KState, and associated data
#   then: decrypting the emitted frame under the same pre-message state and associated data recovers the plaintext, receipt, and next state
#   class: correctness
#
# id: urpcs_authenticated_fail_closed
#   given: a framed message with wrong associated data or mutated authenticated bytes
#   then: decryption raises CodecFail before witness recovery or plaintext release
#   class: security
#
# id: urpcs_vectors_are_canonical
#   given: the frozen v1 harness profile and vector state
#   then: vector generation reproduces the committed deterministic JSON bytes
#   class: evidence
# === END CONTRACTS ===

# === BOUNDARIES ===
# id: urpcs_reference_runtime_boundary
#   summary: processes caller-provided plaintext and secret state in memory and may write an explicitly requested vector file
#   auth_boundary: none
#   storage_boundary: write
#   network_boundary: none
#   user_data_boundary: read
#   admin_only: false
#   pii: possible
#   secrets: read
#   owner: The-Interdependency/stack research/urpcs
# === END BOUNDARIES ===

from __future__ import annotations

import argparse
import hashlib
import hmac
import json
import struct
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Sequence


class CodecFail(Exception):
    """Closed codec or harness failure."""


X = 1
M = 8
MAX_INPUT = 1
MAX_DEPTH = 1
MAX_INTERMEDIATE = 1 << 20
MAX_LAYER_WIRE = 1 << 20
MAX_BETA = 4 << 20
MAX_C0 = 8 << 20
MAX_TRACE = 16 << 20

BOOT_MAGIC = b"URPCS001"
FRAME_MAGIC = b"URPCF001"
LAYER_MAGIC = b"URGON001"
BOOT_HEADER_LEN = 24
FRAME_HEADER_LEN = 24
TAG_LEN = 32
U64_MAX = (1 << 64) - 1
U256_MAX = (1 << 256) - 1


def require(condition: bool, message: str) -> None:
    if not condition:
        raise CodecFail(message)


def n_bytes(value: int) -> bytes:
    require(isinstance(value, int) and not isinstance(value, bool) and value >= 0,
            "N requires a nonnegative integer")
    if value == 0:
        return b""
    return value.to_bytes((value.bit_length() + 7) // 8, "big")


def n_value(encoded: Any) -> int:
    require(isinstance(encoded, bytes), "N slot is not a byte string")
    require(not encoded or encoded[0] != 0, "nonminimal N")
    return int.from_bytes(encoded, "big")


def _cbor_head(major: int, length: int) -> bytes:
    require(0 <= length <= U64_MAX, "CBOR length out of range")
    base = major << 5
    if length < 24:
        return bytes([base | length])
    if length <= 0xFF:
        return bytes([base | 24, length])
    if length <= 0xFFFF:
        return bytes([base | 25]) + length.to_bytes(2, "big")
    if length <= 0xFFFFFFFF:
        return bytes([base | 26]) + length.to_bytes(4, "big")
    return bytes([base | 27]) + length.to_bytes(8, "big")


def dcbor(value: Any) -> bytes:
    if isinstance(value, bytes):
        return _cbor_head(2, len(value)) + value
    if isinstance(value, bool):
        return b"\xf5" if value else b"\xf4"
    if isinstance(value, list):
        return _cbor_head(4, len(value)) + b"".join(dcbor(v) for v in value)
    raise CodecFail(f"forbidden CBOR type: {type(value).__name__}")


class _CBORDecoder:
    def __init__(self, data: bytes):
        self.data = data
        self.pos = 0

    def _take(self, count: int) -> bytes:
        require(count >= 0 and self.pos + count <= len(self.data), "truncated CBOR")
        out = self.data[self.pos:self.pos + count]
        self.pos += count
        return out

    def _length(self, ai: int) -> int:
        if ai < 24:
            return ai
        widths = {24: 1, 25: 2, 26: 4, 27: 8}
        require(ai in widths, "indefinite or reserved CBOR length")
        width = widths[ai]
        raw = self._take(width)
        value = int.from_bytes(raw, "big")
        minimum = {1: 24, 2: 256, 4: 65536, 8: 1 << 32}[width]
        require(value >= minimum, "nonpreferred CBOR length")
        return value

    def item(self) -> Any:
        initial = self._take(1)[0]
        major, ai = initial >> 5, initial & 31
        if major == 2:
            return self._take(self._length(ai))
        if major == 4:
            return [self.item() for _ in range(self._length(ai))]
        if major == 7 and ai in (20, 21):
            return ai == 21
        raise CodecFail("forbidden CBOR item")


def decode_dcbor(data: bytes) -> Any:
    decoder = _CBORDecoder(data)
    value = decoder.item()
    require(decoder.pos == len(data), "trailing CBOR bytes")
    require(dcbor(value) == data, "CBOR re-encode mismatch")
    return value


# Keccak-f[1600], cSHAKE256, and KMAC256 per NIST SP 800-185.
_ROT = (
    (0, 36, 3, 41, 18),
    (1, 44, 10, 45, 2),
    (62, 6, 43, 15, 61),
    (28, 55, 25, 21, 56),
    (27, 20, 39, 8, 14),
)
_RC = (
    0x0000000000000001, 0x0000000000008082,
    0x800000000000808A, 0x8000000080008000,
    0x000000000000808B, 0x0000000080000001,
    0x8000000080008081, 0x8000000000008009,
    0x000000000000008A, 0x0000000000000088,
    0x0000000080008009, 0x000000008000000A,
    0x000000008000808B, 0x800000000000008B,
    0x8000000000008089, 0x8000000000008003,
    0x8000000000008002, 0x8000000000000080,
    0x000000000000800A, 0x800000008000000A,
    0x8000000080008081, 0x8000000000008080,
    0x0000000080000001, 0x8000000080008008,
)
_MASK64 = (1 << 64) - 1


def _rol64(value: int, shift: int) -> int:
    if shift == 0:
        return value & _MASK64
    return ((value << shift) | (value >> (64 - shift))) & _MASK64


def _keccak_f(state: list[int]) -> None:
    for rc in _RC:
        c = [state[x] ^ state[x + 5] ^ state[x + 10] ^ state[x + 15] ^ state[x + 20]
             for x in range(5)]
        d = [c[(x - 1) % 5] ^ _rol64(c[(x + 1) % 5], 1) for x in range(5)]
        for y in range(5):
            for x in range(5):
                state[x + 5 * y] ^= d[x]
        b = [0] * 25
        for y in range(5):
            for x in range(5):
                b[y % 5 + 5 * ((2 * x + 3 * y) % 5)] = _rol64(
                    state[x + 5 * y], _ROT[x][y]
                )
        for y in range(5):
            row = b[5 * y:5 * y + 5]
            for x in range(5):
                state[x + 5 * y] = row[x] ^ ((~row[(x + 1) % 5]) & row[(x + 2) % 5])
        state[0] ^= rc


def _keccak_sponge(data: bytes, output_len: int, suffix: int, rate: int = 136) -> bytes:
    state = [0] * 25
    padded = bytearray(data)
    padded.append(suffix)
    padded.extend(b"\x00" * ((rate - (len(padded) % rate)) % rate))
    if not padded or len(padded) % rate:
        raise AssertionError("Keccak padding length")
    padded[-1] ^= 0x80
    for offset in range(0, len(padded), rate):
        block = padded[offset:offset + rate]
        for i in range(rate // 8):
            state[i] ^= int.from_bytes(block[8 * i:8 * i + 8], "little")
        _keccak_f(state)
    output = bytearray()
    while len(output) < output_len:
        block = b"".join(state[i].to_bytes(8, "little") for i in range(rate // 8))
        output.extend(block[:min(rate, output_len - len(output))])
        if len(output) < output_len:
            _keccak_f(state)
    return bytes(output)


def _left_encode(value: int) -> bytes:
    require(value >= 0, "left_encode negative")
    width = max(1, (value.bit_length() + 7) // 8)
    return bytes([width]) + value.to_bytes(width, "big")


def _right_encode(value: int) -> bytes:
    require(value >= 0, "right_encode negative")
    width = max(1, (value.bit_length() + 7) // 8)
    return value.to_bytes(width, "big") + bytes([width])


def _encode_string(value: bytes) -> bytes:
    return _left_encode(8 * len(value)) + value


def _bytepad(value: bytes, width: int) -> bytes:
    out = _left_encode(width) + value
    return out + b"\x00" * ((-len(out)) % width)


def _cshake256(data: bytes, output_len: int, name: bytes, custom: bytes) -> bytes:
    if not name and not custom:
        return hashlib.shake_256(data).digest(output_len)
    prefix = _bytepad(_encode_string(name) + _encode_string(custom), 136)
    return _keccak_sponge(prefix + data, output_len, 0x04)


def kmac256(key: bytes, data: bytes, output_len: int, custom: bytes) -> bytes:
    require(len(key) >= 32, "KMAC256 key shorter than 256 bits")
    new_data = _bytepad(_encode_string(key), 136) + data + _right_encode(8 * output_len)
    return _cshake256(new_data, output_len, b"KMAC", custom)


@dataclass(frozen=True)
class KState:
    pair: bytes
    integrity: bytes
    advance: bytes
    origin: bytes
    depth: int

    def validate(self) -> None:
        require(all(len(k) == 32 for k in (self.pair, self.integrity, self.advance)),
                "state key length")
        require(len({self.pair, self.integrity, self.advance}) == 3,
                "state keys are not pairwise distinct")
        require(len(self.origin) == 32, "origin namespace length")
        require(0 <= self.depth <= MAX_DEPTH, "depth outside harness")
        require(int.from_bytes(self.origin, "big") < U256_MAX, "origin namespace exhausted")


@dataclass
class BuildResult:
    witness: list[Any]
    layers: list[Any]


@dataclass
class EncryptResult:
    ciphertext: bytes
    next_state: KState
    receipt: bytes
    beta: bytes
    c0: bytes
    layers: list[bytes]


@dataclass
class DecryptResult:
    plaintext: bytes
    next_state: KState
    receipt: bytes
    beta: bytes
    layers: list[bytes]


def _bits(data: bytes) -> bytes:
    return b"".join(f"{byte:08b}".encode("ascii") for byte in data)


def _pack_bits(bits: bytes) -> bytes:
    require(bits and all(ch in (48, 49) for ch in bits), "invalid bit payload")
    padded = bits + b"0" * ((-len(bits)) % 8)
    return bytes(int(padded[i:i + 8], 2) for i in range(0, len(padded), 8))


def _unpack_bits(packed: bytes, length: int) -> bytes:
    require(length >= 1 and len(packed) == (length + 7) // 8, "axis packed length")
    raw = _bits(packed)
    require(all(ch == 48 for ch in raw[length:]), "axis nonzero pad bits")
    return raw[:length]


def axis_id(payload: bytes) -> bytes:
    return dcbor([n_bytes(len(payload)), _pack_bits(payload)])


def parse_axis(axis: bytes) -> tuple[int, bytes]:
    value = decode_dcbor(axis)
    require(isinstance(value, list) and len(value) == 2, "axis shape")
    length = n_value(value[0])
    require(length >= 1 and isinstance(value[1], bytes), "axis fields")
    return length, _unpack_bits(value[1], length)


def origin_id(state: KState, layer: int, region: int) -> bytes:
    return b"ORG\x01" + dcbor([state.origin, n_bytes(layer), n_bytes(region)])


def occurrence_id(origin: bytes, start: int, axis: bytes) -> bytes:
    return b"OCC\x01" + dcbor([origin, n_bytes(start), axis])


def detect(region: bytes, origin: bytes) -> list[dict[str, Any]]:
    bits = _bits(region)
    n = len(bits)
    out: list[dict[str, Any]] = []
    start = 0
    while start < n:
        best = 1
        for length in range(min(n - start, n // 2), 1, -1):
            payload = bits[start:start + length]
            left = bits.find(payload, 0, start) >= 0
            right = bits.find(payload, start + length) >= 0
            if left or right:
                best = length
                break
        payload = bits[start:start + best]
        axis = axis_id(payload)
        occ = occurrence_id(origin, start, axis)
        out.append({"axis": axis, "origin": origin, "start": start,
                    "id": occ, "payload": payload})
        start += best
    return out


def pair_occurrences(occurrences: Sequence[dict[str, Any]], state: KState,
                     origin: bytes) -> tuple[list[tuple[bytes, bytes]], bytes | None]:
    require(all(item["origin"] == origin for item in occurrences), "mixed-origin pair input")
    require(len({item["id"] for item in occurrences}) == len(occurrences), "duplicate occurrence")
    ranked = sorted(
        occurrences,
        key=lambda item: (
            kmac256(state.pair, dcbor([origin, item["id"]]), 32, b"URPCS/PAIR/v1"),
            item["id"],
        ),
    )
    pairs = []
    for i in range(0, len(ranked) - 1, 2):
        first, second = sorted((ranked[i]["id"], ranked[i + 1]["id"]))
        pairs.append((first, second))
    carry = ranked[-1]["id"] if len(ranked) % 2 else None
    return pairs, carry


def pair_gonol(origin: bytes, first: bytes, second: bytes) -> bytes:
    require(first < second, "pair id order")
    return b"\x01" + dcbor([origin, first, second])


def carry_gonol(origin: bytes, occurrence: bytes) -> bytes:
    return b"\x00" + dcbor([origin, occurrence])


def _row_sort(rows: Iterable[list[Any]]) -> list[list[Any]]:
    encoded = sorted((dcbor(row), row) for row in rows)
    require(len({item[0] for item in encoded}) == len(encoded), "duplicate row")
    return [row for _, row in encoded]


def _partition(data: bytes) -> list[bytes]:
    if not data:
        return [b""]
    return [data[i:i + X] for i in range(0, len(data), X)]


def _build_layer(data: bytes, state: KState, layer: int,
                 accum: dict[str, list[list[Any]]]) -> list[Any]:
    require(len(data) <= MAX_INTERMEDIATE, "intermediate input cap")
    regions_wire: list[Any] = []
    for region_ix, region in enumerate(_partition(data)):
        origin = origin_id(state, layer, region_ix)
        accum["origin"].append([n_bytes(layer), n_bytes(region_ix), origin])
        occurrences = detect(region, origin)
        for occurrence in occurrences:
            accum["occur"].append([
                occurrence["axis"], origin, n_bytes(occurrence["start"]), occurrence["id"]
            ])
        pairs, carry = pair_occurrences(occurrences, state, origin)
        gonols: list[dict[str, Any]] = []
        occurrence_by_id = {item["id"]: item for item in occurrences}
        for first, second in pairs:
            accum["pair"].append([n_bytes(layer), first, second])
            gonols.append({"id": pair_gonol(origin, first, second),
                           "kind": 0, "members": [first, second]})
        if carry is not None:
            gonols.append({"id": carry_gonol(origin, carry),
                           "kind": 1, "members": [carry]})
        gonols.sort(key=lambda item: (item["kind"], item["id"]))
        children: dict[bytes, list[bytes]] = {item["id"]: [] for item in gonols}
        phases: dict[bytes, int] = {}
        if gonols:
            phases[gonols[0]["id"]] = 0
        for i in range(1, len(gonols)):
            parent_ix = (i - 1) // 2
            parent = gonols[parent_ix]["id"]
            child = gonols[i]["id"]
            delta = 1 + ((i - 1) % (M - 1))
            children[parent].append(child)
            accum["attach"].append([parent, child, n_bytes(layer)])
            accum["delta"].append([parent, child, n_bytes(delta)])
            phases[child] = (phases[parent] + delta) % M
        gonol_wire: list[Any] = []
        for gonol in gonols:
            gid = gonol["id"]
            members = sorted(gonol["members"])
            for occurrence in members:
                accum["member"].append([occurrence, gid])
            accum["a"].append([
                n_bytes(layer), n_bytes(region_ix), gid,
                [n_bytes(len(children[gid])), n_bytes(1 if gonol["kind"] else 0)],
            ])
            member_wire = []
            for member_ix, occurrence in enumerate(members):
                local = 0 if len(members) == 1 or member_ix == 0 else M // 2
                theta = (phases[gid] + local) % M
                require(occurrence in occurrence_by_id, "member occurrence missing")
                member_wire.append([occurrence, n_bytes(theta)])
            gonol_wire.append([gid, n_bytes(phases[gid]), member_wire])
        regions_wire.append([n_bytes(region_ix), n_bytes(len(region)), origin, gonol_wire])
    return [n_bytes(layer), n_bytes(len(data)), regions_wire]


def layer_wire(layer: list[Any]) -> bytes:
    encoded = LAYER_MAGIC + dcbor(layer)
    require(len(encoded) <= MAX_LAYER_WIRE, "layer wire cap")
    return encoded


def build(plaintext: bytes, state: KState) -> BuildResult:
    state.validate()
    require(len(plaintext) <= MAX_INPUT, "plaintext outside harness")
    accum = {name: [] for name in ("a", "origin", "pair", "member", "occur", "attach", "delta")}
    layers: list[Any] = []
    data = plaintext
    for layer in range(state.depth + 1):
        current = _build_layer(data, state, layer, accum)
        layers.append(current)
        if layer < state.depth:
            data = layer_wire(current)
            require(len(data) <= MAX_INTERMEDIATE, "serialized intermediate cap")
    witness = [
        _row_sort(accum["a"]),
        [
            _row_sort(accum["origin"]),
            _row_sort(accum["pair"]),
            _row_sort(accum["member"]),
            _row_sort(accum["occur"]),
            _row_sort(accum["attach"]),
        ],
        _row_sort(accum["delta"]),
        [[], True],
        [n_bytes(32), state.depth.to_bytes(4, "big")],
    ]
    return BuildResult(witness=witness, layers=layers)


def encode_witness(witness: list[Any]) -> bytes:
    encoded = dcbor(witness)
    require(len(encoded) <= MAX_BETA, "witness cap")
    return encoded


def boot_header(length: int) -> bytes:
    require(0 <= length <= U64_MAX, "bootstrap length range")
    return struct.pack(">8sHHQI", BOOT_MAGIC, 1, BOOT_HEADER_LEN, length, 0)


def frame_header(length: int) -> bytes:
    require(0 <= length <= U64_MAX, "frame length range")
    return struct.pack(">8sHHQHH", FRAME_MAGIC, 1, FRAME_HEADER_LEN, length, TAG_LEN, 0)


def tag(state: KState, c0: bytes, ad: bytes) -> bytes:
    header = frame_header(len(c0))
    tagged = dcbor([header, c0, ad])
    return kmac256(state.integrity, tagged, TAG_LEN, b"URPCS/TAG/v1")


def frame(c0: bytes, authentication_tag: bytes) -> bytes:
    require(len(authentication_tag) == TAG_LEN, "tag length")
    return frame_header(len(c0)) + c0 + authentication_tag


def unframe(ciphertext: bytes) -> tuple[bytes, bytes]:
    require(len(ciphertext) >= FRAME_HEADER_LEN + TAG_LEN, "short frame")
    magic, version, header_len, length, tag_len, flags = struct.unpack(
        ">8sHHQHH", ciphertext[:FRAME_HEADER_LEN]
    )
    require(magic == FRAME_MAGIC and version == 1 and header_len == FRAME_HEADER_LEN,
            "frame identity")
    require(tag_len == TAG_LEN and flags == 0, "frame fields")
    require(length <= len(ciphertext) - FRAME_HEADER_LEN - TAG_LEN, "frame length overflow")
    require(len(ciphertext) == FRAME_HEADER_LEN + length + TAG_LEN, "frame exact length")
    return (ciphertext[FRAME_HEADER_LEN:FRAME_HEADER_LEN + length],
            ciphertext[FRAME_HEADER_LEN + length:])


def receipt(witness: list[Any], layers: Sequence[list[Any]]) -> bytes:
    trace = dcbor([encode_witness(witness), [layer_wire(item) for item in layers]])
    require(len(trace) <= MAX_TRACE, "trace cap")
    return hashlib.sha3_256(dcbor([b"URPCS/RECEIPT/v1", trace])).digest()


def _avoid(candidate: bytes, forbidden: set[bytes]) -> bytes:
    base = int.from_bytes(candidate, "big")
    for increment in range(len(forbidden) + 1):
        value = ((base + increment) & U256_MAX).to_bytes(32, "big")
        if value not in forbidden:
            return value
    raise AssertionError("Avoid pigeonhole failure")


def advance(state: KState, ciphertext: bytes, trace_receipt: bytes) -> KState:
    state.validate()
    require(len(trace_receipt) == 32, "receipt length")
    context = dcbor([state.origin, n_bytes(state.depth), ciphertext, trace_receipt])
    pair = kmac256(state.advance, context, 32, b"URPCS/ADV/PAIR/v1")
    integrity = _avoid(
        kmac256(state.advance, context, 32, b"URPCS/ADV/INTEGRITY/v1"), {pair}
    )
    next_advance = _avoid(
        kmac256(state.advance, context, 32, b"URPCS/ADV/ROOT/v1"),
        {pair, integrity},
    )
    origin = (int.from_bytes(state.origin, "big") + 1).to_bytes(32, "big")
    result = KState(pair, integrity, next_advance, origin, state.depth)
    result.validate()
    return result


def encrypt(plaintext: bytes, state: KState, ad: bytes) -> EncryptResult:
    result = build(plaintext, state)
    beta = encode_witness(result.witness)
    body = layer_wire(result.layers[-1])
    c0 = boot_header(len(beta)) + beta + body
    require(len(c0) <= MAX_C0, "C0 cap")
    authentication_tag = tag(state, c0, ad)
    ciphertext = frame(c0, authentication_tag)
    q = receipt(result.witness, result.layers)
    next_state = advance(state, ciphertext, q)
    return EncryptResult(ciphertext, next_state, q, beta, c0,
                         [layer_wire(item) for item in result.layers])


def _expect_array(value: Any, length: int, name: str) -> list[Any]:
    require(isinstance(value, list) and len(value) == length, f"{name} shape")
    return value


def _validate_sorted_rows(rows: Any, arity: int, name: str) -> list[list[Any]]:
    require(isinstance(rows, list), f"{name} is not an array")
    parsed = []
    encodings = []
    for row in rows:
        _expect_array(row, arity, name)
        parsed.append(row)
        encodings.append(dcbor(row))
    require(encodings == sorted(encodings) and len(set(encodings)) == len(encodings),
            f"{name} sort/duplicate")
    return parsed


def decode_witness(beta: bytes, state: KState) -> tuple[list[Any], dict[str, Any]]:
    require(len(beta) <= MAX_BETA, "witness cap")
    witness = _expect_array(decode_dcbor(beta), 5, "witness")
    a_rows = _validate_sorted_rows(witness[0], 4, "A")
    relations = _expect_array(witness[1], 5, "relations")
    origin_rows = _validate_sorted_rows(relations[0], 3, "origin")
    pair_rows = _validate_sorted_rows(relations[1], 3, "pair")
    member_rows = _validate_sorted_rows(relations[2], 2, "member")
    occur_rows = _validate_sorted_rows(relations[3], 4, "occur")
    attach_rows = _validate_sorted_rows(relations[4], 3, "attach")
    delta_rows = _validate_sorted_rows(witness[2], 3, "delta")
    require(witness[3] == [[], True], "Law 13 cursor")
    halt = _expect_array(witness[4], 2, "halt")
    require(n_value(halt[0]) == 32 and isinstance(halt[1], bytes) and len(halt[1]) == 4,
            "halt seed")
    require(int.from_bytes(halt[1], "big") == state.depth, "halt/state depth")

    origins: dict[bytes, tuple[int, int]] = {}
    region_keys: set[tuple[int, int]] = set()
    layers: set[int] = set()
    for row in origin_rows:
        layer, region, origin = n_value(row[0]), n_value(row[1]), row[2]
        require(isinstance(origin, bytes), "origin id type")
        require((layer, region) not in region_keys and origin not in origins, "origin uniqueness")
        require(origin == origin_id(state, layer, region), "origin reconstruction")
        region_keys.add((layer, region))
        origins[origin] = (layer, region)
        layers.add(layer)
    require(layers == set(range(state.depth + 1)), "origin layer coverage")

    occurrences: dict[bytes, dict[str, Any]] = {}
    by_origin: dict[bytes, list[dict[str, Any]]] = {origin: [] for origin in origins}
    for row in occur_rows:
        axis, origin, start_raw, occ = row
        require(isinstance(axis, bytes) and isinstance(origin, bytes) and isinstance(occ, bytes),
                "occurrence field type")
        require(origin in origins and occ not in occurrences, "occurrence reference/uniqueness")
        start = n_value(start_raw)
        length, payload = parse_axis(axis)
        require(occ == occurrence_id(origin, start, axis), "occurrence id reconstruction")
        item = {"axis": axis, "origin": origin, "start": start, "id": occ,
                "length": length, "payload": payload}
        occurrences[occ] = item
        by_origin[origin].append(item)

    actual_pairs: dict[bytes, set[tuple[bytes, bytes]]] = {origin: set() for origin in origins}
    for row in pair_rows:
        layer, first, second = n_value(row[0]), row[1], row[2]
        require(isinstance(first, bytes) and isinstance(second, bytes) and first < second,
                "pair order/type")
        require(first in occurrences and second in occurrences, "pair occurrence reference")
        origin = occurrences[first]["origin"]
        require(occurrences[second]["origin"] == origin and origins[origin][0] == layer,
                "pair origin/layer")
        actual_pairs[origin].add((first, second))

    expected_gonols: dict[bytes, dict[str, Any]] = {}
    gonols_by_origin: dict[bytes, list[dict[str, Any]]] = {}
    expected_pair_rows = []
    for origin, items in by_origin.items():
        pairs, carry = pair_occurrences(items, state, origin)
        expected_pair_rows.extend([[n_bytes(origins[origin][0]), first, second]
                                   for first, second in pairs])
        require(actual_pairs[origin] == set(pairs), "pair recomputation")
        gonols = []
        for first, second in pairs:
            gid = pair_gonol(origin, first, second)
            item = {"id": gid, "kind": 0, "members": [first, second], "origin": origin}
            expected_gonols[gid] = item
            gonols.append(item)
        if carry is not None:
            gid = carry_gonol(origin, carry)
            item = {"id": gid, "kind": 1, "members": [carry], "origin": origin}
            expected_gonols[gid] = item
            gonols.append(item)
        gonols.sort(key=lambda item: (item["kind"], item["id"]))
        gonols_by_origin[origin] = gonols
    require(_row_sort(expected_pair_rows) == pair_rows, "pair row completeness")

    expected_members = _row_sort(
        [[occ, gid] for gid, gonol in expected_gonols.items() for occ in gonol["members"]]
    )
    require(member_rows == expected_members, "membership exactness")

    expected_attach = []
    expected_delta = []
    expected_a = []
    phases: dict[bytes, int] = {}
    for origin, gonols in gonols_by_origin.items():
        layer, region = origins[origin]
        children = {item["id"]: [] for item in gonols}
        if gonols:
            phases[gonols[0]["id"]] = 0
        for i in range(1, len(gonols)):
            parent = gonols[(i - 1) // 2]["id"]
            child = gonols[i]["id"]
            delta = 1 + ((i - 1) % (M - 1))
            children[parent].append(child)
            expected_attach.append([parent, child, n_bytes(layer)])
            expected_delta.append([parent, child, n_bytes(delta)])
            phases[child] = (phases[parent] + delta) % M
        for gonol in gonols:
            expected_a.append([
                n_bytes(layer), n_bytes(region), gonol["id"],
                [n_bytes(len(children[gonol["id"]])), n_bytes(1 if gonol["kind"] else 0)],
            ])
    require(attach_rows == _row_sort(expected_attach), "attachment reconstruction")
    require(delta_rows == _row_sort(expected_delta), "delta reconstruction")
    require(a_rows == _row_sort(expected_a), "shape reconstruction")
    return witness, {
        "origins": origins,
        "occurrences": occurrences,
        "by_origin": by_origin,
        "gonols": expected_gonols,
        "gonols_by_origin": gonols_by_origin,
        "phases": phases,
    }


def deserialize_layer(data: bytes, expected_layer: int | None = None) -> list[Any]:
    require(len(data) <= MAX_LAYER_WIRE and data.startswith(LAYER_MAGIC), "layer magic/cap")
    layer = _expect_array(decode_dcbor(data[len(LAYER_MAGIC):]), 3, "layer")
    layer_ix = n_value(layer[0])
    if expected_layer is not None:
        require(layer_ix == expected_layer, "layer index")
    n_value(layer[1])
    require(isinstance(layer[2], list), "layer regions")
    require(layer_wire(layer) == data, "Law 9 layer re-encode")
    return layer


def _expand_layer(layer: list[Any], state: KState, index: dict[str, Any]) -> bytes:
    layer_ix = n_value(layer[0])
    total_length = n_value(layer[1])
    regions = layer[2]
    require(isinstance(regions, list), "region list")
    rebuilt_regions = []
    for expected_j, raw_region in enumerate(regions):
        region = _expect_array(raw_region, 4, "region")
        j = n_value(region[0])
        region_length = n_value(region[1])
        origin = region[2]
        gonol_wire = region[3]
        require(j == expected_j and isinstance(origin, bytes) and isinstance(gonol_wire, list),
                "region order/type")
        require(index["origins"].get(origin) == (layer_ix, j), "region origin")
        expected_gonols = index["gonols_by_origin"][origin]
        require(len(gonol_wire) == len(expected_gonols), "gonol count")
        for raw, expected in zip(gonol_wire, expected_gonols):
            gonol = _expect_array(raw, 3, "gonol")
            gid, phase_raw, members = gonol
            require(gid == expected["id"] and n_value(phase_raw) == index["phases"][gid],
                    "gonol id/phase")
            require(isinstance(members, list), "gonol members")
            member_ids = sorted(expected["members"])
            require(len(members) == len(member_ids), "gonol member count")
            for member_ix, (member_raw, member_id) in enumerate(zip(members, member_ids)):
                member = _expect_array(member_raw, 2, "member")
                local = 0 if len(member_ids) == 1 or member_ix == 0 else M // 2
                expected_theta = (index["phases"][gid] + local) % M
                require(member[0] == member_id and n_value(member[1]) == expected_theta,
                        "member id/theta")
        occs = sorted(index["by_origin"][origin], key=lambda item: item["start"])
        cursor = 0
        bits = bytearray()
        for occ in occs:
            require(occ["start"] == cursor, "occurrence coverage gap/overlap")
            bits.extend(occ["payload"])
            cursor += occ["length"]
        require(cursor == 8 * region_length, "region covered length")
        require(cursor % 8 == 0, "region bit alignment")
        region_bytes = bytes(int(bits[i:i + 8], 2) for i in range(0, len(bits), 8))
        rerun = detect(region_bytes, origin)
        require([(x["axis"], x["origin"], x["start"], x["id"]) for x in rerun] ==
                [(x["axis"], x["origin"], x["start"], x["id"]) for x in occs],
                "Detect replay")
        rebuilt_regions.append(region_bytes)
    data = b"".join(rebuilt_regions)
    require(len(data) == total_length, "layer total length")
    expected_regions = _partition(data)
    require(len(expected_regions) == len(rebuilt_regions) and expected_regions == rebuilt_regions,
            "region partition")
    return data


def decrypt(ciphertext: bytes, state: KState, ad: bytes) -> DecryptResult:
    state.validate()
    c0, received_tag = unframe(ciphertext)
    expected_tag = tag(state, c0, ad)
    require(hmac.compare_digest(received_tag, expected_tag), "tag verification")
    require(len(c0) >= BOOT_HEADER_LEN, "short bootstrap")
    magic, version, header_len, beta_len, flags = struct.unpack(
        ">8sHHQI", c0[:BOOT_HEADER_LEN]
    )
    require(magic == BOOT_MAGIC and version == 1 and header_len == BOOT_HEADER_LEN and flags == 0,
            "bootstrap identity")
    require(beta_len <= len(c0) - BOOT_HEADER_LEN, "bootstrap length overflow")
    beta = c0[BOOT_HEADER_LEN:BOOT_HEADER_LEN + beta_len]
    body = c0[BOOT_HEADER_LEN + beta_len:]
    witness, index = decode_witness(beta, state)
    terminal = deserialize_layer(body, state.depth)
    layers_reversed = [terminal]
    current = terminal
    plaintext = b""
    for layer_ix in range(state.depth, -1, -1):
        plaintext = _expand_layer(current, state, index)
        if layer_ix > 0:
            current = deserialize_layer(plaintext, layer_ix - 1)
            layers_reversed.append(current)
    layers = list(reversed(layers_reversed))
    q = receipt(witness, layers)
    next_state = advance(state, ciphertext, q)
    return DecryptResult(plaintext, next_state, q, beta,
                         [layer_wire(item) for item in layers])


class StateSlot:
    """Minimal in-memory compare-and-swap model for the host single-use law."""

    def __init__(self, state: KState):
        self.state = state

    def commit(self, expected: KState, replacement: KState) -> bool:
        if self.state != expected:
            return False
        self.state = replacement
        return True


def _state_hex(state: KState) -> dict[str, Any]:
    return {
        "k_pair": state.pair.hex(),
        "k_integrity": state.integrity.hex(),
        "k_advance": state.advance.hex(),
        "nu_origin": state.origin.hex(),
        "R_cap": state.depth,
    }


def vector_state(depth: int) -> KState:
    return KState(bytes(range(0x00, 0x20)), bytes(range(0x20, 0x40)),
                  bytes(range(0x40, 0x60)), b"\x00" * 32, depth)


VECTOR_AD = b"URPCS vector v1"


def _expect_fail(operation, contains: str | None = None) -> str:
    try:
        operation()
    except CodecFail as exc:
        message = str(exc)
        if contains is not None:
            require(contains in message, f"wrong failure: {message}")
        return message
    raise AssertionError("expected CodecFail")


def generate_vectors() -> dict[str, Any]:
    vectors: list[dict[str, Any]] = []
    positives: dict[str, tuple[bytes, KState, EncryptResult, DecryptResult]] = {}
    for name, plaintext, depth in (
        ("empty_r0", b"", 0),
        ("empty_r1", b"", 1),
        ("odd_09_r0", b"\x09", 0),
    ):
        state = vector_state(depth)
        encrypted = encrypt(plaintext, state, VECTOR_AD)
        decrypted = decrypt(encrypted.ciphertext, state, VECTOR_AD)
        require(decrypted.plaintext == plaintext, "positive plaintext mismatch")
        require(decrypted.receipt == encrypted.receipt, "positive receipt mismatch")
        require(decrypted.next_state == encrypted.next_state, "positive state mismatch")
        positives[name] = (plaintext, state, encrypted, decrypted)
        vectors.append({
            "id": name,
            "classification": "COMPUTATION",
            "expected": "success",
            "plaintext_hex": plaintext.hex(),
            "ad_hex": VECTOR_AD.hex(),
            "initial_state": _state_hex(state),
            "beta_hex": encrypted.beta.hex(),
            "layer_wire_hex": [item.hex() for item in encrypted.layers],
            "c0_hex": encrypted.c0.hex(),
            "ciphertext_hex": encrypted.ciphertext.hex(),
            "receipt_hex": encrypted.receipt.hex(),
            "next_state": _state_hex(encrypted.next_state),
            "verified": {
                "plaintext_equal": True,
                "receipt_equal": True,
                "next_state_equal": True,
            },
        })

    plaintext, state, encrypted, _ = positives["odd_09_r0"]
    wrong_ad = VECTOR_AD + b"!"
    message = _expect_fail(lambda: decrypt(encrypted.ciphertext, state, wrong_ad), "tag")
    vectors.append({
        "id": "wrong_ad",
        "classification": "COMPUTATION",
        "base_vector": "odd_09_r0",
        "wrong_ad_hex": wrong_ad.hex(),
        "expected": "fail_before_bootstrap",
        "observed_failure": message,
    })

    header = encrypted.ciphertext[:FRAME_HEADER_LEN]
    _, _, _, c0_len, _, _ = struct.unpack(">8sHHQHH", header)
    c0 = bytearray(encrypted.ciphertext[FRAME_HEADER_LEN:FRAME_HEADER_LEN + c0_len])
    mutation_in_c0 = BOOT_HEADER_LEN + int.from_bytes(c0[12:20], "big")
    require(mutation_in_c0 < len(c0), "mutation offset")
    c0[mutation_in_c0] ^= 0x01
    mutated = header + bytes(c0) + encrypted.ciphertext[FRAME_HEADER_LEN + c0_len:]
    message = _expect_fail(lambda: decrypt(mutated, state, VECTOR_AD), "tag")
    vectors.append({
        "id": "authenticated_body_mutation",
        "classification": "COMPUTATION",
        "base_vector": "odd_09_r0",
        "ciphertext_offset": FRAME_HEADER_LEN + mutation_in_c0,
        "mutated_ciphertext_hex": mutated.hex(),
        "expected": "fail_before_bootstrap",
        "observed_failure": message,
    })

    first = decrypt(encrypted.ciphertext, state, VECTOR_AD)
    message = _expect_fail(
        lambda: decrypt(encrypted.ciphertext, first.next_state, VECTOR_AD), "tag"
    )
    vectors.append({
        "id": "replay_after_advance",
        "classification": "COMPUTATION",
        "base_vector": "odd_09_r0",
        "first_decrypt": "success",
        "replay_expected": "fail_under_K_t_plus_1",
        "observed_failure": message,
    })

    concurrent_state = vector_state(0)
    contender_a = encrypt(b"", concurrent_state, VECTOR_AD)
    contender_b = encrypt(b"\x09", concurrent_state, VECTOR_AD)
    slot = StateSlot(concurrent_state)
    first_won = slot.commit(concurrent_state, contender_a.next_state)
    second_won = slot.commit(concurrent_state, contender_b.next_state)
    require(first_won and not second_won, "CAS result")
    vectors.append({
        "id": "concurrent_state_rejection",
        "classification": "HOST_COMPUTATION",
        "candidate_a_ciphertext_sha3_256": hashlib.sha3_256(contender_a.ciphertext).hexdigest(),
        "candidate_b_ciphertext_sha3_256": hashlib.sha3_256(contender_b.ciphertext).hexdigest(),
        "candidate_a_commit": first_won,
        "candidate_b_commit": second_won,
        "expected": "exactly_one_commit",
    })

    vectors.append({
        "id": "receipt_and_state_equality",
        "classification": "COMPUTATION",
        "positive_vectors": [
            {
                "id": name,
                "receipt_equal": encrypted.receipt == decrypted.receipt,
                "next_state_equal": encrypted.next_state == decrypted.next_state,
            }
            for name, (_, _, encrypted, decrypted) in positives.items()
        ],
        "expected": "all_true",
    })

    return {
        "artifact": "URPCS v1 byte-exact vectors",
        "standing": "COMPUTATION",
        "claims": [
            "Laws 1-13 are implemented for the bounded harness profile.",
            "Positive fixtures round-trip with equal receipts and next states.",
            "Negative fixtures fail at the stated boundary.",
            "Confidentiality is not claimed.",
        ],
        "profile": {
            "x_bytes": X,
            "M": M,
            "max_input_bytes": MAX_INPUT,
            "max_depth": MAX_DEPTH,
            "max_intermediate_bytes": MAX_INTERMEDIATE,
            "max_layer_wire_bytes": MAX_LAYER_WIRE,
            "max_beta_bytes": MAX_BETA,
            "max_c0_bytes": MAX_C0,
            "max_trace_wire_bytes": MAX_TRACE,
        },
        "vectors": vectors,
        "hmmm": (
            "The vectors establish deterministic codec behavior only. "
            "A separate security model must test any future confidentiality construction."
        ),
    }


def self_test() -> None:
    # KMAC256 known answer for the SP 800-185 construction, independently
    # cross-checked against OpenSSL 3 KMAC-256.
    sample_key = bytes(range(0x40, 0x60))
    expected = bytes.fromhex(
        "2ebd1622de2de44174e3477206060d7f64489a639b7545649132317609fa214f"
        "4c8ac90630fb4c757fba074b15186fe452ae71b6a1e443bf54059e090c11ae20"
    )
    require(kmac256(sample_key, bytes.fromhex("00010203"), 64, b"") == expected,
            "KMAC256 NIST sample")
    require(dcbor(decode_dcbor(dcbor([b"x", [b"", True, False]]))) ==
            dcbor([b"x", [b"", True, False]]), "CBOR self-test")
    vectors = generate_vectors()
    require(len(vectors["vectors"]) == 8, "vector count")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true", help="run all positive and negative tests")
    parser.add_argument("--write-vectors", type=Path, help="write deterministic JSON vectors")
    args = parser.parse_args()
    require(args.self_test or args.write_vectors is not None, "choose --self-test or --write-vectors")
    self_test()
    if args.write_vectors is not None:
        payload = generate_vectors()
        args.write_vectors.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n",
                                      encoding="utf-8")
        print(args.write_vectors)
    else:
        print("8/8 vector cases passed")


if __name__ == "__main__":
    main()
