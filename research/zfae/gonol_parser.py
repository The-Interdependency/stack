# ratios: loc_comments=183:53 imports_exports=10:6 calls_definitions=86:19
"""Lossless glyph-gonol admission for Stack ZFAE construction research.

Usage (Python 3.12, stdlib): ``parser = load_parser(ucns_source_file)``;
then ``parser.parse_text(text, source_id="turn:1")`` or
``parser.parse_gonols(gonols, source_id="turn:1")``. See GONOL_PARSER.json.
The parser consumes the English producer's GlyphGonol objects. It does not
construct a prompt/word gonol, select geometry, or perform inference.
"""

# === MODULE_BUILD ===
# id: zfae_gonol_parser
#   module_name: gonol_parser
#   module_kind: adapter
#   summary: consume source-verified glyph constructors and retain ordered source occurrences with lossless recovery
#   owner: The-Interdependency/stack
#   public_surface: load_parser, GonolParser, ParsedGonols, GlyphOccurrence, GonolAdmissionError
#   internal_surface: verified module loading and declared inventory construction
#   auth_boundary: content identity only; no producer authentication claim
#   storage_boundary: read explicit UCNS source and local profile/producer; temporary in-memory SQLite
#   network_boundary: none
#   user_data_boundary: caller input stays in memory; to_dict exposes the complete source construction
#   tests: research/zfae/tests/test_gonol_parser.py
#   rollout: explicit Stack research input adapter
#   rollback: revert parser/profile/tests; retain historical heuristic-parser evidence
#   unresolved: geometric function operations, higher closure, neural audit, inference integration
# === END MODULE_BUILD ===

# === CONTRACTS ===
# id: zfae_gonol_parser_consumes_producers
#   given: the exact UCNS source and Stack glyph producer match the declared profile
#   then: use the producer GlyphGonol objects and retain separate carrier and axis positions; changed sources fail before execution
#   class: construction
# id: zfae_gonol_parser_preserves_occurrences
#   given: admitted Unicode scalars including repeated glyphs and control characters
#   then: retain their exact order, multiplicity, scalar and UTF-8 byte spans, source identity and recoverable construction
#   class: correctness
# id: zfae_gonol_parser_reports_missing_admission
#   given: an unsupported scalar or a non-scalar input
#   then: preserve unsupported scalar occurrences but refuse complete gonol consumption; reject invalid UTF-8, surrogates and coercion
#   class: correctness
# id: zfae_gonol_parser_replays_construction
#   given: a serialized parse or a sequence of declared producer gonols
#   then: recover canonical shared objects with exact source and reject foreign or mutated construction evidence
#   class: correctness
# === END CONTRACTS ===

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
import sqlite3
import sys
from types import MappingProxyType, ModuleType
from typing import Any, Iterable
import unicodedata

HERE = Path(__file__).resolve().parent


class GonolAdmissionError(ValueError):
    """Source or construction is outside the declared admission profile."""


def _canonical(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":"), allow_nan=False).encode("utf-8")


def _verified_module(path: Path, expected_blob: str, *, module_name: str | None = None) -> ModuleType:
    raw = path.read_bytes()
    observed = hashlib.sha1(f"blob {len(raw)}\0".encode() + raw).hexdigest()
    if observed != expected_blob:
        raise GonolAdmissionError(f"producer Git blob mismatch: {path.name}")
    name = module_name or "_zfae_gonol_source_" + expected_blob
    # Execute the verified bytes on every admission; a cached namespace can be patched.
    package_name, _, child = name.rpartition(".")
    if package_name and package_name not in sys.modules:
        package = ModuleType(package_name)
        package.__path__ = [str(path.parent)]
        sys.modules[package_name] = package
    module = ModuleType(name)
    module.__file__ = str(path)
    previous = sys.modules.get(name)
    sys.modules[name] = module
    try:
        exec(compile(raw, str(path), "exec"), module.__dict__)
    except BaseException:
        if previous is None:
            sys.modules.pop(name, None)
        else:
            sys.modules[name] = previous
        raise
    if package_name:
        setattr(sys.modules[package_name], child, module)
    return module


def _same_construction(left, right):
    """Native equality must preserve types as well as values recursively."""
    if type(left) is not type(right):
        return False
    if isinstance(left, tuple):
        return len(left) == len(right) and all(_same_construction(a, b) for a, b in zip(left, right))
    return left == right


def _scalar_text(text: str) -> str:
    if not isinstance(text, str):
        raise TypeError("source must be str; use parse_utf8 for bytes")
    for offset, scalar in enumerate(text):
        if 0xD800 <= ord(scalar) <= 0xDFFF:
            raise GonolAdmissionError(f"surrogate at scalar offset {offset}")
    return text


@dataclass(frozen=True)
class GlyphOccurrence:
    """An occurrence reference, not a new gonol schema or geometry."""

    ordinal: int
    scalar: str
    utf8_start: int
    utf8_end: int
    gonol: Any | None


@dataclass(frozen=True)
class ParsedGonols:
    source_id: str
    profile_sha256: str
    inventory_sha256: str
    occurrences: tuple[GlyphOccurrence, ...]

    def recover_text(self) -> str:
        return "".join(occurrence.scalar for occurrence in self.occurrences)

    @property
    def unadmitted(self) -> tuple[GlyphOccurrence, ...]:
        return tuple(o for o in self.occurrences if o.gonol is None)

    @property
    def admitted(self) -> bool:
        return not self.unadmitted

    def require_gonols(self) -> tuple[Any, ...]:
        """Require complete admission before passing glyphs to a consumer."""
        if self.unadmitted:
            positions = ", ".join(str(o.ordinal) for o in self.unadmitted)
            raise GonolAdmissionError("unadmitted scalar offsets: " + positions)
        return tuple(o.gonol for o in self.occurrences)

    def to_dict(self) -> dict:
        """Keep native construction records inside the serialized parse."""
        used = {o.gonol.identity: o.gonol for o in self.occurrences if o.gonol is not None}
        return {
            "schema": "stack.zfae.gonol-input", "version": "1.0.0",
            "source_id": self.source_id,
            "source_sha256": hashlib.sha256(self.recover_text().encode("utf-8")).hexdigest(),
            "profile_sha256": self.profile_sha256,
            "inventory_sha256": self.inventory_sha256,
            "admitted": self.admitted,
            "gonols": [g.as_dict() for g in sorted(used.values(), key=lambda g: g.axis_index)],
            "occurrences": [{
                "ordinal": o.ordinal, "scalar": o.scalar,
                "scalar_span": [o.ordinal, o.ordinal + 1],
                "utf8_span": [o.utf8_start, o.utf8_end],
                "glyph_identity": o.gonol.identity if o.gonol is not None else None,
            } for o in self.occurrences],
        }


@dataclass(frozen=True, init=False)
class GonolParser:
    """An immutable declared inventory shared by individually addressed parses."""

    inventory: Any
    profile_sha256: str
    inventory_sha256: str
    _gonol_type: type

    def __init__(self, inventory: dict, *, profile_sha256: str, gonol_type: type):
        object.__setattr__(self, "inventory", MappingProxyType(dict(inventory)))
        object.__setattr__(self, "profile_sha256", profile_sha256)
        digest = hashlib.sha256(_canonical(
            [g.as_dict() for g in sorted(inventory.values(), key=lambda g: g.axis_index)]
        )).hexdigest()
        object.__setattr__(self, "inventory_sha256", digest)
        object.__setattr__(self, "_gonol_type", gonol_type)

    def parse_text(self, text: str, *, source_id: str) -> ParsedGonols:
        text = _scalar_text(text)
        if not isinstance(source_id, str) or not source_id:
            raise GonolAdmissionError("source_id must be nonempty text")
        _scalar_text(source_id)
        occurrences = []
        byte_offset = 0
        for ordinal, scalar in enumerate(text):
            end = byte_offset + len(scalar.encode("utf-8"))
            occurrences.append(GlyphOccurrence(
                ordinal, scalar, byte_offset, end, self.inventory.get(scalar)
            ))
            byte_offset = end
        return ParsedGonols(source_id, self.profile_sha256,
                            self.inventory_sha256, tuple(occurrences))

    def parse_utf8(self, data: bytes, *, source_id: str) -> ParsedGonols:
        if not isinstance(data, bytes):
            raise TypeError("UTF-8 source must be bytes")
        return self.parse_text(data.decode("utf-8", errors="strict"), source_id=source_id)

    def parse_gonols(self, gonols: Iterable[Any], *, source_id: str) -> ParsedGonols:
        """Consume declared native glyph objects without coercing them to text."""
        glyphs = []
        for ordinal, gonol in enumerate(gonols):
            if not isinstance(gonol, self._gonol_type):
                raise GonolAdmissionError(f"foreign gonol type at occurrence {ordinal}")
            expected = self.inventory.get(gonol.identity)
            if expected is None or not all(
                _same_construction(getattr(expected, field), getattr(gonol, field))
                for field in self._gonol_type.__dataclass_fields__
            ):
                raise GonolAdmissionError(f"undeclared glyph construction at occurrence {ordinal}")
            glyphs.append(gonol.identity)
        return self.parse_text("".join(glyphs), source_id=source_id)

    def replay(self, payload: dict) -> ParsedGonols:
        """Rehydrate a JSON parse only if all evidence exactly replays."""
        try:
            text = "".join(row["scalar"] for row in payload["occurrences"])
            result = self.parse_text(text, source_id=payload["source_id"])
            matches = _canonical(result.to_dict()) == _canonical(payload)
        except (KeyError, TypeError, ValueError) as exc:
            raise GonolAdmissionError("invalid serialized gonol input") from exc
        if not matches:
            raise GonolAdmissionError("serialized gonol input does not replay")
        return result


def load_parser(ucns_source_file: str | Path) -> GonolParser:
    """Build the declared finite inventory using both verified owning sources."""
    profile_bytes = (HERE / "GONOL_PARSER.json").read_bytes()
    profile = json.loads(profile_bytes)
    if unicodedata.unidata_version != profile["unicode_version"]:
        raise GonolAdmissionError("Unicode database differs from the declared profile")
    carrier = _verified_module(Path(ucns_source_file), profile["ucns"]["blob_sha"])
    producer = _verified_module(HERE.parents[1] / profile["producer"]["path"],
                                profile["producer"]["blob_sha"],
                                module_name="english_gonol.hyperspace_construct")
    extras = tuple(profile["additional_scalars"])
    for scalar in extras:
        if len(_scalar_text(scalar)) != 1 or scalar in carrier.PUBLIC_GONOL_157:
            raise GonolAdmissionError("additional admission must be one non-carrier scalar")
    if len(set(extras)) != len(extras):
        raise GonolAdmissionError("duplicate additional scalar admission")
    scalars = carrier.PUBLIC_GONOL_157 + extras
    connection = sqlite3.connect(":memory:")
    try:
        connection.execute("CREATE TABLE characters (id INTEGER, scalar TEXT, public_position INTEGER)")
        connection.executemany("INSERT INTO characters VALUES (?, ?, ?)", (
            (i + 1, scalar, carrier.public_gonol_position(scalar))
            for i, scalar in enumerate(scalars)
        ))
        inventory = producer.glyph_inventory(connection)
    finally:
        connection.close()
    # The declared primitive is one scalar; CRLF remains two occurrences.
    inventory = {scalar: inventory[scalar] for scalar in scalars}
    return GonolParser(inventory, profile_sha256=hashlib.sha256(profile_bytes).hexdigest(),
                       gonol_type=producer.GlyphGonol)


__all__ = ["load_parser", "GonolParser", "ParsedGonols", "GlyphOccurrence", "GonolAdmissionError"]
# ratios: loc_comments=183:53 imports_exports=10:6 calls_definitions=86:19
