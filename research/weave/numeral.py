# === MODULE_BUILD ===
# id: weave_numeral_construction
#   module_name: numeral
#   module_kind: experiment
#   summary: exact length-bearing bit blocks, executable prime paths, and scoped Unicode references with self-contained recovery and full wire-size accounting
#   owner: Erin Spencer
#   public_surface: BitBlock, PrimePath, Entry, Packet, Limits, encode, decode, main
#   internal_surface: canonical wire reader and bounded exact prime evaluator
#   auth_boundary: none
#   storage_boundary: write
#   network_boundary: none
#   user_data_boundary: read
#   admin_only: false
#   tests: tests/test_numeral.py
#   rollout: explicit research API and CLI; not installed as Weave encryption
#   rollback: remove numeral.py, its tests, and its documentation link
#   unresolved: native gonol attachment and automatic prime-recipe discovery are not supplied by this representation layer
# === END MODULE_BUILD ===
# === CONTRACTS ===
# id: numeral_exact_recovery
#   given: admitted blocks including leading zero bits and partial bytes
#   then: decoding the self-contained packet restores each value, length, occurrence order, and supplied attachment
# id: numeral_recipe_replay
#   given: an admitted prime-index and embedded-span recipe
#   then: exact evaluation reproduces the bound block or refuses without substituting a literal
# id: numeral_scoped_symbols
#   given: a Unicode symbol in a message-origin and round scope
#   then: it resolves uniquely within that scope; no standard Unicode numeric meaning is claimed
# id: numeral_accounting
#   given: a serialized packet
#   then: header, definitions, and occurrence stream sizes sum to all transmitted bytes
# id: numeral_strict_input
#   given: malformed, noncanonical, ambiguous, or over-budget input
#   then: reject before unsafe allocation or prime work; budget refusal is not mathematical falsification
# === END CONTRACTS ===
"""Weave numeral construction, not encryption or a competing gonol constructor.

Usage: python numeral.py demo
       python numeral.py bind INPUT OUTPUT --origin message-1 --angle 1/7 --circle 3
       python numeral.py recover INPUT OUTPUT
       python numeral.py inspect INPUT

A Unicode symbol names a length-bearing integer or an executable prime path.
The packet includes definitions: there is no hidden dictionary or original-message
lookup. Angles/occurrence-circle assignments are caller-supplied attachment data,
not geometry generated here. No automatic splitting, corpus selection, interleave,
private/public key derivation, authentication, or native UCNS/UCHC claim is made.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass, field
from fractions import Fraction
from math import isqrt
from pathlib import Path
import json

MAGIC = b"WNC\x01"


class Refused(ValueError):
    """Malformed or inconsistent construction."""


class ResourceLimit(Refused):
    """This execution profile cannot admit the requested work."""


@dataclass(frozen=True)
class Limits:
    """Operational budgets, adjustable by the caller; not mathematical bounds."""
    output_bits: int = 64 * 1024 * 1024 * 8
    wire_bytes: int = 80 * 1024 * 1024
    entries: int = 137468
    occurrences: int = 1000000
    prime_index: int = 100000
    prime_value: int = 2**32 - 1
    sieve_bytes: int = 4000000
    recipe_steps: int = 256
    prime_work: int = 16000000

    def __post_init__(self):
        if any(type(v) is not int or v < 1 for v in vars(self).values()):
            raise Refused("budgets must be positive integers")


def _nat(value: int) -> int:
    if type(value) is not int or value < 0:
        raise Refused("nonnegative integer required; Booleans are not integers here")
    return value


@dataclass(frozen=True)
class BitBlock:
    """Exact ordered bits as (integer, length); the length is part of identity."""
    value: int = field(repr=False)
    length: int

    def __post_init__(self):
        _nat(self.value)
        _nat(self.length)
        if self.value.bit_length() > self.length:
            raise Refused("integer does not fit declared bit length")

    @classmethod
    def from_bytes(cls, data: bytes, length: int | None = None) -> BitBlock:
        """MSB-first input; any unused low bits in the last byte must be zero."""
        if type(data) is not bytes:
            raise Refused("exact bytes required")
        length = len(data) * 8 if length is None else _nat(length)
        if len(data) != (length + 7) // 8:
            raise Refused("byte count does not match bit length")
        padding = (-length) % 8
        value = int.from_bytes(data, "big")
        if padding and value & ((1 << padding) - 1):
            raise Refused("nonzero unused padding bits")
        return cls(value >> padding, length)

    def to_bytes(self) -> bytes:
        """Return MSB-first bytes, with zero low padding for a partial last byte."""
        return (self.value << ((-self.length) % 8)).to_bytes((self.length + 7) // 8, "big")


@dataclass(frozen=True)
class PrimePath:
    """Exact recipe: ('next',) or ('span', base, start, width).

    Spans are contiguous, zero-based from the left, in canonical base 2 or 10
    notation. Both the source and selected value must be prime. A leading-zero
    span keeps its original start/width in the recipe, not just its numeric value.
    These are supported candidate operations, not a universal Weave routing rule.
    """
    seed: int
    steps: tuple[tuple, ...]

    def replay(self, limits: Limits = Limits(), *, _engine=None) -> tuple[int, ...]:
        if type(self.steps) is not tuple:
            raise Refused("recipe steps must be an immutable tuple")
        if len(self.steps) > limits.recipe_steps:
            raise ResourceLimit("recipe step budget exceeded")
        primes = _engine if _engine is not None else _Primes(limits)
        primes.charge(len(self.steps) + 1)
        value = _nat(self.seed)
        primes.require(value)
        trace = [value]
        for step in self.steps:
            if type(step) is not tuple or not step:
                raise Refused("invalid recipe step")
            if step == ("next",):
                value = primes.nth(value)
            elif len(step) == 4 and step[0] == "span":
                _, base, start, width = step
                if type(base) is not int or base not in (2, 10):
                    raise Refused("span base must be 2 or 10")
                _nat(start)
                if _nat(width) == 0:
                    raise Refused("empty span")
                digits = format(value, "b") if base == 2 else str(value)
                if start + width > len(digits):
                    raise Refused("span outside source numeral")
                value = int(digits[start:start + width], base)
                primes.require(value)
            else:
                raise Refused("unknown recipe operation")
            trace.append(value)
        return tuple(trace)


class _Primes:
    def __init__(self, limits: Limits):
        self.limits = limits
        self.table: list[int] = []
        self.work = 0

    def charge(self, amount: int) -> None:
        self.work += amount
        if self.work > self.limits.prime_work:
            raise ResourceLimit("aggregate prime work exceeds execution budget")

    def require(self, value: int) -> None:
        if value > self.limits.prime_value:
            raise ResourceLimit("exact primality work exceeds prime-value budget")
        if value < 2 or (value != 2 and value % 2 == 0):
            raise Refused("selected value is not prime")
        self.charge(len(range(3, isqrt(value) + 1, 2)))
        for divisor in range(3, isqrt(value) + 1, 2):
            if value % divisor == 0:
                raise Refused("selected value is not prime")

    def nth(self, index: int) -> int:
        if index > self.limits.prime_index:
            raise ResourceLimit("nth-prime index exceeds execution budget")
        if index <= len(self.table):
            return self.table[index - 1]
        bound = max(16, index * 20)
        while True:
            bound = min(bound, self.limits.prime_value)
            if bound + 1 > self.limits.sieve_bytes:
                raise ResourceLimit("prime sieve exceeds allocation budget")
            self.charge(bound + 1)
            sieve = bytearray(b"\x01") * (bound + 1)
            sieve[0:2] = b"\x00\x00"
            for divisor in range(2, isqrt(bound) + 1):
                if sieve[divisor]:
                    start = divisor * divisor
                    sieve[start:bound + 1:divisor] = b"\x00" * ((bound - start) // divisor + 1)
            self.table = [i for i in range(2, bound + 1) if sieve[i]]
            if len(self.table) >= index:
                return self.table[index - 1]
            if bound == self.limits.prime_value:
                raise ResourceLimit("nth prime exceeds prime-value budget")
            bound *= 2


def _symbol(symbol: str) -> None:
    if type(symbol) is not str or len(symbol) != 1:
        raise Refused("one Unicode scalar required")
    cp = ord(symbol)
    if not (0xE000 <= cp <= 0xF8FF or 0xF0000 <= cp <= 0xFFFFD
            or 0x100000 <= cp <= 0x10FFFD):
        raise Refused("symbol must be a Unicode private-use scalar")


@dataclass(frozen=True)
class Entry:
    symbol: str
    block: BitBlock = field(repr=False)
    angle: Fraction
    circle: int
    recipe: PrimePath | None = field(default=None, repr=False)

    def validate(self, limits: Limits, *, _engine=None) -> None:
        _symbol(self.symbol)
        if type(self.block) is not BitBlock or self.block.length == 0:
            raise Refused("a definition must contain a nonempty BitBlock")
        if self.block.length > limits.output_bits:
            raise ResourceLimit("definition exceeds bit budget")
        if type(self.angle) is not Fraction or not 0 <= self.angle < 2:
            raise Refused("exact supplied angle must be in [0,2) turns")
        if type(self.circle) is not int or not 1 <= self.circle <= 7:
            raise Refused("occurrence circle must be one of the seven")
        if self.recipe is not None:
            if type(self.recipe) is not PrimePath or self.recipe.replay(limits, _engine=_engine)[-1] != self.block.value:
                raise Refused("recipe does not construct its bound integer")


@dataclass(frozen=True)
class Packet:
    """One scoped definition table and ordered occurrence stream.

    origin is a caller's scope identifier, not a fabricated UCNS origin object.
    The same glyph may legitimately denote another block in another scope.
    """
    origin: str
    round_id: int
    entries: tuple[Entry, ...]
    symbols: str

    def validate(self, limits: Limits = Limits(), *, _engine=None) -> int:
        if type(self.origin) is not str or not self.origin or len(self.origin.encode("utf-8")) > 1024:
            raise Refused("nonempty UTF-8 origin scope of at most 1024 bytes required")
        _nat(self.round_id)
        if type(self.entries) is not tuple:
            raise Refused("definitions must be an immutable tuple")
        if len(self.entries) > limits.entries:
            raise ResourceLimit("definition count exceeds execution budget")
        if type(self.symbols) is not str:
            raise Refused("occurrence stream must be a string")
        if len(self.symbols) > limits.occurrences:
            raise ResourceLimit("occurrence stream exceeds execution budget")
        mapping = {}
        angles = set()
        primes = _engine if _engine is not None else _Primes(limits)
        for entry in self.entries:
            if type(entry) is not Entry:
                raise Refused("Entry required")
            entry.validate(limits, _engine=primes)
            if entry.symbol in mapping or entry.angle in angles:
                raise Refused("duplicate symbol or angular attachment in this scope")
            mapping[entry.symbol] = entry
            angles.add(entry.angle)
        total = 0
        for symbol in self.symbols:
            if symbol not in mapping:
                raise Refused("undefined symbol")
            total += mapping[symbol].block.length
            if total > limits.output_bits:
                raise ResourceLimit("reconstructed stream exceeds bit budget")
        return total

    def occurrences(self, limits: Limits = Limits()) -> tuple[tuple[str, int, int, int], ...]:
        """(symbol, bit offset, ordinal on its occurrence circle, circle)."""
        self.validate(limits)
        mapping = {entry.symbol: entry for entry in self.entries}
        counts = [0] * 8
        offset = 0
        result = []
        for symbol in self.symbols:
            entry = mapping[symbol]
            result.append((symbol, offset, counts[entry.circle], entry.circle))
            counts[entry.circle] += 1
            offset += entry.block.length
        return tuple(result)

    def restore(self, limits: Limits = Limits()) -> BitBlock:
        """Reconstruct in linear output-byte work; no original input or hidden table."""
        total = self.validate(limits)
        mapping = {entry.symbol: entry.block for entry in self.entries}
        out = bytearray((total + 7) // 8)
        offset = 0
        for symbol in self.symbols:
            block = mapping[symbol]
            raw = block.to_bytes()
            byte, shift = divmod(offset, 8)
            if shift == 0:
                out[byte:byte + len(raw)] = raw
            else:
                for i, value in enumerate(raw):
                    out[byte + i] |= value >> shift
                    if byte + i + 1 < len(out):
                        out[byte + i + 1] |= (value << (8 - shift)) & 255
            offset += block.length
        return BitBlock.from_bytes(bytes(out), total)


def _uint(value: int) -> bytes:
    _nat(value)
    if value >= 2**64:
        raise Refused("wire integer field exceeds 64 bits; literal block values use bytes")
    out = bytearray()
    while value >= 128:
        out.append((value & 127) | 128)
        value >>= 7
    out.append(value)
    return bytes(out)


def _blob(data: bytes) -> bytes:
    return _uint(len(data)) + data


class _Reader:
    def __init__(self, data: bytes):
        self.data, self.pos = data, 0

    def take(self, count: int) -> bytes:
        if count > len(self.data) - self.pos:
            raise Refused("truncated packet")
        result = self.data[self.pos:self.pos + count]
        self.pos += count
        return result

    def uint(self) -> int:
        start = self.pos
        value = 0
        for shift in range(0, 70, 7):
            byte = self.take(1)[0]
            value |= (byte & 127) << shift
            if byte < 128:
                if value >= 2**64 or self.data[start:self.pos] != _uint(value):
                    raise Refused("noncanonical integer field")
                return value
        raise Refused("oversized integer field")

    def blob(self, maximum: int) -> bytes:
        count = self.uint()
        if count > maximum:
            raise ResourceLimit("field exceeds byte budget")
        return self.take(count)


def _parts(packet: Packet, limits: Limits) -> tuple[bytes, bytes, bytes]:
    total = packet.validate(limits)
    header = MAGIC + _blob(packet.origin.encode("utf-8")) + _uint(packet.round_id) + _uint(total)
    count = _uint(len(packet.entries))
    # Size the entire representation before allocating literal output buffers.
    # In particular, unused definitions cannot evade the output-length budget.
    stream_size = sum(3 if ord(c) <= 0xFFFF else 4 for c in packet.symbols)
    projected = len(header) + len(count) + len(_uint(stream_size)) + stream_size
    pieces = []
    for entry in packet.entries:
        prefix = (_blob(entry.symbol.encode("utf-8"))
                  + _uint(entry.angle.numerator) + _uint(entry.angle.denominator)
                  + _uint(entry.circle) + _uint(entry.block.length))
        if entry.recipe is None:
            prefix += b"\x00"
            payload_size = (entry.block.length + 7) // 8
            pieces.append((prefix, entry.block))
        else:
            recipe = entry.recipe
            prefix += b"\x01" + _uint(recipe.seed) + _uint(len(recipe.steps))
            for step in recipe.steps:
                if step == ("next",):
                    prefix += b"\x00"
                else:
                    prefix += b"\x01" + b"".join(_uint(v) for v in step[1:])
            payload_size = 0
            pieces.append((prefix, None))
        projected += len(prefix) + payload_size
        if projected > limits.wire_bytes:
            raise ResourceLimit("serialized packet exceeds byte budget")
    if projected > limits.wire_bytes:
        raise ResourceLimit("serialized packet exceeds byte budget")
    definitions = count + b"".join(prefix + (block.to_bytes() if block is not None else b"")
                                    for prefix, block in pieces)
    stream = _blob(packet.symbols.encode("utf-8"))
    return header, definitions, stream



def encode(packet: Packet, limits: Limits = Limits()) -> bytes:
    """Serialize all reconstruction information, including the definition table."""
    return b"".join(_parts(packet, limits))


def decode(data: bytes, limits: Limits = Limits()) -> Packet:
    """Strict self-contained decoder; malformed input never becomes a partial result."""
    if type(data) is not bytes:
        raise Refused("packet must be bytes")
    if len(data) > limits.wire_bytes:
        raise ResourceLimit("packet exceeds byte budget")
    reader = _Reader(data)
    if reader.take(len(MAGIC)) != MAGIC:
        raise Refused("unknown packet version")
    try:
        origin = reader.blob(1024).decode("utf-8")
        round_id, declared = reader.uint(), reader.uint()
        if declared > limits.output_bits:
            raise ResourceLimit("declared output exceeds bit budget")
        count = reader.uint()
        if count > limits.entries:
            raise ResourceLimit("definition count exceeds budget")
        entries = []
        primes = _Primes(limits)
        for _ in range(count):
            symbol = reader.blob(4).decode("utf-8")
            _symbol(symbol)
            numerator, denominator = reader.uint(), reader.uint()
            if denominator == 0:
                raise Refused("zero angle denominator")
            angle = Fraction(numerator, denominator)
            if (angle.numerator, angle.denominator) != (numerator, denominator):
                raise Refused("angle fraction is not canonical")
            circle, length = reader.uint(), reader.uint()
            if length > limits.output_bits:
                raise ResourceLimit("definition exceeds bit budget")
            tag = reader.take(1)[0]
            recipe = None
            if tag == 0:
                block = BitBlock.from_bytes(reader.take((length + 7) // 8), length)
            elif tag == 1:
                seed, step_count = reader.uint(), reader.uint()
                if step_count > limits.recipe_steps:
                    raise ResourceLimit("recipe step count exceeds budget")
                steps = []
                for _ in range(step_count):
                    kind = reader.take(1)[0]
                    if kind == 0:
                        steps.append(("next",))
                    elif kind == 1:
                        steps.append(("span", reader.uint(), reader.uint(), reader.uint()))
                    else:
                        raise Refused("unknown recipe opcode")
                recipe = PrimePath(seed, tuple(steps))
                block = BitBlock(recipe.replay(limits, _engine=primes)[-1], length)
            else:
                raise Refused("unknown definition tag")
            entries.append(Entry(symbol, block, angle, circle, recipe))
        symbols = reader.blob(limits.occurrences * 4).decode("utf-8")
    except UnicodeError as exc:
        raise Refused("invalid UTF-8") from exc
    if reader.pos != len(data):
        raise Refused("trailing packet data")
    packet = Packet(origin, round_id, tuple(entries), symbols)
    # Parsing and structural validation share one charged prime-work budget.
    if packet.validate(limits, _engine=primes) != declared:
        raise Refused("declared output length disagrees with occurrences")
    return packet


def accounting(packet: Packet, limits: Limits = Limits()) -> dict[str, int]:
    header, table, stream = _parts(packet, limits)
    bits = packet.validate(limits)
    return {"source_bits": bits, "source_packed_bytes": (bits + 7) // 8,
            "header_bytes": len(header), "definition_bytes": len(table),
            "occurrence_bytes": len(stream), "total_bytes": len(header) + len(table) + len(stream),
            "symbol_utf8_bytes": len(packet.symbols.encode("utf-8"))}


def demo() -> dict:
    """Measured nonsecret examples; no secret key or personal input."""
    block = BitBlock.from_bytes(bytes(range(256)) * 4096)
    entry = Entry(chr(0xE000), block, Fraction(1, 7), 3)
    single = Packet("demo-large", 0, (entry,), entry.symbol)
    repeated = Packet("demo-large", 0, (entry,), entry.symbol * 4)
    recipe = PrimePath(5381, (("span", 10, 0, 2), ("next",), ("next",)))
    r_entry = Entry(chr(0xE001), BitBlock(1523, 16), Fraction(2, 7), 4, recipe)
    replay = Packet("demo-prime", 0, (r_entry,), r_entry.symbol)
    result = {}
    for name, packet in (("single_large_block", single), ("four_repetitions", repeated), ("prime_path", replay)):
        wire = encode(packet)
        recovered = decode(wire).restore()
        result[name] = {**accounting(packet), "exact_recovery": recovered == packet.restore()}
    result["prime_path"]["trace"] = list(recipe.replay())
    result["standing"] = "representation-and-replay only; not encryption"
    return result


def _angle_argument(text: str) -> Fraction:
    """Translate malformed CLI fractions into argparse's status-2 refusal."""
    try:
        return Fraction(text)
    except (ValueError, ZeroDivisionError) as exc:
        raise argparse.ArgumentTypeError("angle must be an exact finite fraction") from exc


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("demo")
    bind = sub.add_parser("bind")
    bind.add_argument("input", type=Path)
    bind.add_argument("output", type=Path)
    bind.add_argument("--origin", required=True)
    bind.add_argument("--angle", required=True, type=_angle_argument)
    bind.add_argument("--circle", required=True, type=int)
    recover = sub.add_parser("recover")
    recover.add_argument("input", type=Path)
    recover.add_argument("output", type=Path)
    inspect = sub.add_parser("inspect")
    inspect.add_argument("input", type=Path)
    args = parser.parse_args()
    try:
        if args.command == "demo":
            result = demo()
        else:
            limit = Limits().output_bits // 8 if args.command == "bind" else Limits().wire_bytes
            if args.input.stat().st_size > limit:
                raise ResourceLimit("input file exceeds execution budget")
            with args.input.open("rb") as source:
                raw = source.read(limit + 1)
            if len(raw) > limit:
                raise ResourceLimit("input grew beyond execution budget")
            if args.command == "bind":
                entry = Entry(chr(0xE000), BitBlock.from_bytes(raw), args.angle, args.circle)
                packet = Packet(args.origin, 0, (entry,) if raw else (), entry.symbol if raw else "")
                wire = encode(packet)
                with args.output.open("xb") as target:
                    target.write(wire)
                result = accounting(packet)
            else:
                packet = decode(raw)
                result = accounting(packet)
                if args.command == "recover":
                    restored = packet.restore()
                    with args.output.open("xb") as target:
                        target.write(restored.to_bytes())
                    result["output_bit_length"] = restored.length
        print(json.dumps(result, indent=2))
        return 0
    except (OSError, Refused, UnicodeError) as exc:
        parser.exit(2, f"refused: {exc}\n")


if __name__ == "__main__":
    raise SystemExit(main())
