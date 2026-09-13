"""Construct Python 3.12 gonols from exact source occurrences, bottom up.

Usage guidance
--------------
Use :func:`affixiate_python_bytes` for files so the encoding declaration, BOM,
and exact original bytes remain receipt-bound.  Use
:func:`affixiate_python_source` for an already-decoded source string::

    receipt = affixiate_python_source("answer = f'{40 + 2}'\n", source_id="demo.py")
    assert receipt.standing == "implemented-candidate"
    assert replay_python_affixiation(receipt).receipt_digest == receipt.receipt_digest

The constructor always starts with one letter gonol per decoded Unicode scalar
occurrence.  Here ``letter`` names the admitted source floor, including spaces,
newlines, punctuation, and digits; it is not an alphabetic subclass.  Tokenizer
and AST values are recognition witnesses only.  No token, AST node, code object,
or compiler object is stored as a gonol or used in place of source participants.
"""

# === MODULE_BUILD ===
# id: python_gonol_affixiation
#   module_name: python_gonol.affixiation
#   module_kind: engine
#   summary: affixiates exact Python 3.12 source from letter occurrences through lexical, delimiter, and recursive grammar gonols without substituting parser objects for construction
#   owner: Python Gonol Construction (stack-local research)
#   public_surface: affixiate_python_source, affixiate_python_bytes, replay_python_affixiation, reconstruct_source, PythonGonolConstructionError
#   internal_surface: _SourceIndex, _Registry, _lexical_floor, _delimiter_gonols, _grammar_root
#   auth_boundary: Python Gonol Construction owns source admission and Python relation construction; METAPAT owns affixiation semantics; UCNS owns geometry
#   storage_boundary: none; caller-owned bytes and receipts remain in memory
#   network_boundary: none
#   user_data_boundary: reads caller-supplied source into an explicit caller-owned receipt and transmits nothing
#   admin_only: false
#   tests: tests.test_affixiation, tests.test_python312_surface
#   rollout: explicit Python 3.12 stack-local candidate
#   rollback: remove the python-gonol workspace before downstream binding
#   requires: Python 3.12 standard library; optional explicit UCNS Public Gonol authority
#   since: 2026-09-12
#   unresolved: exact UCNS affixiation geometry and later Python language profiles remain hmmm
# === END MODULE_BUILD ===

# === CAPABILITIES ===
# id: python_source_bottom_up_affixiation
#   summary: constructs a lossless addressable gonol registry from every decoded Python source occurrence upward
#   exposes: python_gonol.affixiation.affixiate_python_source, python_gonol.affixiation.affixiate_python_bytes
#   inputs: exact source text or bytes, source_id, optional explicit UCNS geometry authority
#   outputs: PythonAffixiationReceipt
#   boundaries: auth:none, storage:none, network:none, user_data:caller-owned receipt
#   owner: Python Gonol Construction (stack-local research)
# === END CAPABILITIES ===

# === DOCS ===
# id: python_gonol_affixiation_boundary_docs
#   summary: explains the bottom-up construction order, parser-witness boundary, replay contract, and unresolved geometry
#   audience: developer
#   source: docs/PYTHON_AFFIXIATION_BOUNDARY.md
#   covers: affixiate_python_source, affixiate_python_bytes, replay_python_affixiation
#   status: current
# === END DOCS ===

# === BOUNDARIES ===
# id: python_gonol_affixiation_runtime_boundary
#   summary: reads caller-owned Python source in memory, performs no execution or network access, and optionally observes an explicitly supplied matching UCNS carrier
#   auth_boundary: none
#   storage_boundary: none
#   network_boundary: none
#   user_data_boundary: read
#   admin_only: false
#   pii: possible
#   secrets: none
#   owner: Python Gonol Construction (stack-local research)
# === END BOUNDARIES ===

# === CONTRACTS ===
# id: every_python_source_occurrence_closes_first
#   given: any admitted decoded Python source string, including repeated whitespace or punctuation
#   then: exactly one individually addressable letter gonol closes for every Unicode scalar occurrence in exact source order
#   class: construction
#
# id: python_lexical_forms_affixiate_letters
#   given: the Python 3.12 lexical witness recognizes a nonempty form or an inter-token source gap
#   then: one lexical gonol closes over the exact ordered letter gonols covering that form without normalization or omission
#   class: construction
#
# id: python_constructions_affixiate_closed_gonols
#   given: delimiter and Python grammar relations are recognized after the lexical floor closes
#   then: every larger construction references already-closed gonols atomically and carries its constitutive relation, order, roles, multiplicity, source span, and provenance inside its identity
#   class: construction
#
# id: python_affixiation_is_lossless_and_replayable
#   given: a completed Python affixiation receipt
#   then: exact decoded source reconstructs from letter gonols and every gonol plus the receipt digest verifies deterministically
#   class: replay
#
# id: unresolved_python_source_remains_hmmm
#   given: source has an unmatched delimiter, tokenizer failure, or Python 3.12 grammar error
#   then: admitted lower gonols remain preserved beneath a source root whose standing and exact unresolved boundary are hmmm
#   class: safety

# id: parser_objects_never_become_gonols
#   given: tokenizer and AST recognition witnesses are used
#   then: receipt gonols contain only source-built relation records and closed-gonol references, never TokenInfo, AST, code, or compiler objects
#   class: boundary
#
# id: python_gonol_geometry_binding_fails_closed
#   given: an explicit UCNS Public Gonol authority is supplied
#   then: exact carrier positions are observed only when the carrier and declared digest match the pinned identity; function operations remain hmmm
#   class: boundary
# === END CONTRACTS ===

from __future__ import annotations

import ast
import base64
from dataclasses import dataclass, replace
from hashlib import sha256
import io
import json
import keyword
import platform
import sys
import token as token_module
import tokenize
from typing import Any, Iterable, Mapping, Sequence

from .model import (
    AffixiationRelation,
    ClosedGonol,
    PythonAffixiationReceipt,
    RelationMember,
    SourceSpan,
    canonical_json_bytes,
)


SCHEMA = "the-interdependency.python-gonol-affixiation"
SCHEMA_VERSION = "1.0.0"
CONSTRUCTOR_ID = "python-gonol.affixiation"
CONSTRUCTOR_VERSION = "0.1.0"
LANGUAGE_PROFILE = "python-3.12-file-input"
CPYTHON_VERSION = (3, 12, 14)
PINNED_PUBLIC_GONOL_SHA256 = (
    "55d10c84529a4d7bc7714786357e977b68d9df2ac3f73d20e229580b552c2ef5"
)
STANDING = "implemented-candidate"
SELECTION_EFFECT = "none"
RELATION_AUTHORITY = (
    "METAPAT affixiation semantics; Python 3.12 source relation witnessed by CPython; "
    "UCNS geometry not implied"
)

NONCLAIMS = (
    "not an AST, token stream, code object, or compiler-object representation",
    "not execution or behavioral equivalence of the source",
    "not selected UCNS geometry or a UCNS affixiation/coupling law",
    "not EDCM measurement validity",
    "not canon or independent release authority",
)

BASE_HMMM = (
    "exact UCNS geometric operation of Public Gonol function positions",
    "exact UCNS Mobius-carrier affixiation/coupling law",
    "Python language profiles after Python 3.12 file input",
)


class PythonGonolConstructionError(RuntimeError):
    """Raised when a receipt or explicit authority fails closed."""


@dataclass(frozen=True, slots=True)
class _LexicalWitness:
    start: int
    end: int
    token_name: str
    exact_name: str
    spelling: str
    gonol: ClosedGonol


@dataclass(frozen=True, slots=True)
class _MemberCandidate:
    role: str
    gonol: ClosedGonol
    priority: int


class _SourceIndex:
    def __init__(self, source: str) -> None:
        self.source = source
        self.recognition_source = source.replace("\r\n", "\n").replace("\r", "\n")
        self._recognition_to_source: list[int] = []
        index = 0
        while index < len(source):
            self._recognition_to_source.append(index)
            if source[index] == "\r" and index + 1 < len(source) and source[index + 1] == "\n":
                index += 2
            else:
                index += 1
        self._recognition_to_source.append(len(source))
        starts = [0]
        for index, character in enumerate(source):
            if character == "\r":
                if index + 1 < len(source) and source[index + 1] == "\n":
                    continue
                starts.append(index + 1)
            elif character == "\n":
                starts.append(index + 1)
        self.line_starts = tuple(starts)
        recognition_starts = [0]
        for index, character in enumerate(self.recognition_source):
            if character == "\n":
                recognition_starts.append(index + 1)
        self.recognition_line_starts = tuple(recognition_starts)

    def recognition_offset(self, offset: int) -> int:
        if not 0 <= offset <= len(self.recognition_source):
            raise PythonGonolConstructionError(f"recognition offset outside source: {offset}")
        return self._recognition_to_source[offset]

    def token_offset(self, position: tuple[int, int]) -> int:
        row, column = position
        if row < 1:
            raise PythonGonolConstructionError(f"invalid tokenizer row: {row}")
        if row > len(self.line_starts):
            if row == len(self.line_starts) + 1 and column == 0:
                return len(self.source)
            raise PythonGonolConstructionError(f"tokenizer position outside source: {position!r}")
        offset = self.recognition_line_starts[row - 1] + column
        if not 0 <= offset <= len(self.recognition_source):
            raise PythonGonolConstructionError(f"tokenizer position outside source: {position!r}")
        return self.recognition_offset(offset)

    def ast_offset(self, row: int, utf8_column: int) -> int:
        if row < 1 or row > len(self.line_starts):
            raise PythonGonolConstructionError(
                f"AST position outside decoded source: {(row, utf8_column)!r}"
            )
        start = self.recognition_line_starts[row - 1]
        end = self.recognition_line_starts[row] if row < len(self.recognition_line_starts) else len(self.recognition_source)
        line = self.recognition_source[start:end]
        byte_count = 0
        for char_column, character in enumerate(line):
            if byte_count == utf8_column:
                return self.recognition_offset(start + char_column)
            byte_count += len(character.encode("utf-8"))
            if byte_count > utf8_column:
                break
        if byte_count == utf8_column:
            return self.recognition_offset(end)
        raise PythonGonolConstructionError(
            f"AST UTF-8 column does not align to a source scalar: {(row, utf8_column)!r}"
        )

    def line_column(self, offset: int) -> tuple[int, int]:
        if not 0 <= offset <= len(self.source):
            raise PythonGonolConstructionError(f"source offset outside source: {offset}")
        low = 0
        high = len(self.line_starts)
        while low + 1 < high:
            middle = (low + high) // 2
            if self.line_starts[middle] <= offset:
                low = middle
            else:
                high = middle
        return (low + 1, offset - self.line_starts[low])

    def span(self, start: int, end: int) -> SourceSpan:
        if not 0 <= start <= end <= len(self.source):
            raise PythonGonolConstructionError(f"invalid source span: {(start, end)!r}")
        start_line, start_column = self.line_column(start)
        end_line, end_column = self.line_column(end)
        return SourceSpan(start, end, start_line, start_column, end_line, end_column)


class _Registry:
    def __init__(self, source_id: str, source_index: _SourceIndex) -> None:
        self.source_id = source_id
        self.source_index = source_index
        self.values: list[ClosedGonol] = []
        self.by_id: dict[str, ClosedGonol] = {}
        self.by_address: dict[str, ClosedGonol] = {}

    def close(
        self,
        *,
        address: str,
        scale: str,
        start: int,
        end: int,
        relation_kind: str,
        candidates: Sequence[_MemberCandidate] = (),
        properties: Sequence[tuple[str, str]] = (),
        provenance: Sequence[tuple[str, str]] = (),
        hmmm: Sequence[str] = (),
    ) -> ClosedGonol:
        if address in self.by_address:
            raise PythonGonolConstructionError(f"duplicate gonol address: {address}")
        members: list[RelationMember] = []
        for ordinal, candidate in enumerate(candidates):
            child = self.by_id.get(candidate.gonol.gonol_id)
            if child is None or child.address != candidate.gonol.address:
                raise PythonGonolConstructionError(
                    "larger construction may reference only an already-closed gonol"
                )
            members.append(
                RelationMember(
                    ordinal=ordinal,
                    role=candidate.role,
                    gonol_id=child.gonol_id,
                    address=child.address,
                )
            )
        relation = AffixiationRelation(
            kind=relation_kind,
            members=tuple(members),
            properties=tuple((str(key), str(value)) for key, value in properties),
            authority=RELATION_AUTHORITY,
        )
        provisional = ClosedGonol(
            address=address,
            scale=scale,
            span=self.source_index.span(start, end),
            relation=relation,
            provenance=(
                ("constructor", f"{CONSTRUCTOR_ID}/{CONSTRUCTOR_VERSION}"),
                ("language_profile", LANGUAGE_PROFILE),
                ("source_id", self.source_id),
            )
            + tuple((str(key), str(value)) for key, value in provenance),
            hmmm=tuple(str(item) for item in hmmm),
            gonol_id="",
        )
        gonol_id = sha256(canonical_json_bytes(provisional.identity_payload())).hexdigest()
        value = replace(provisional, gonol_id=gonol_id)
        if gonol_id in self.by_id:
            raise PythonGonolConstructionError(
                "closed gonol identity collision; occurrence address failed to distinguish values"
            )
        self.values.append(value)
        self.by_id[gonol_id] = value
        self.by_address[address] = value
        return value


def _require_source(source: str, source_id: str) -> None:
    if not isinstance(source, str):
        raise TypeError("source must be an exact decoded Unicode string")
    if not isinstance(source_id, str) or not source_id:
        raise TypeError("source_id must be exact non-empty text")
    for field, value in (("source", source), ("source_id", source_id)):
        for character in value:
            if 0xD800 <= ord(character) <= 0xDFFF:
                raise PythonGonolConstructionError(f"{field} contains a surrogate code point")


def _public_gonol_positions(authority: Any | None) -> tuple[dict[str, int] | None, str]:
    if authority is None:
        return None, "not-supplied"
    if isinstance(authority, Mapping):
        carrier_value = authority.get("PUBLIC_GONOL_157")
        declared_digest = authority.get("PUBLIC_GONOL_SHA256")
    else:
        carrier_value = getattr(authority, "PUBLIC_GONOL_157", None)
        declared_digest = getattr(authority, "PUBLIC_GONOL_SHA256", None)
    if not isinstance(carrier_value, Sequence) or isinstance(carrier_value, (str, bytes)):
        raise PythonGonolConstructionError(
            "explicit UCNS authority must expose PUBLIC_GONOL_157"
        )
    carrier = tuple(carrier_value)
    if len(carrier) != 157 or len(set(carrier)) != 157:
        raise PythonGonolConstructionError(
            "explicit UCNS Public Gonol carrier must contain 157 unique positions"
        )
    if any(not isinstance(item, str) or len(item) != 1 for item in carrier):
        raise PythonGonolConstructionError(
            "explicit UCNS Public Gonol positions must be one Unicode scalar each"
        )
    computed = sha256(
        json.dumps(carrier, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    if declared_digest != computed or computed != PINNED_PUBLIC_GONOL_SHA256:
        raise PythonGonolConstructionError(
            "explicit UCNS Public Gonol authority digest does not match the pinned carrier"
        )
    name = (
        str(authority.get("authority_name", "mapping"))
        if isinstance(authority, Mapping)
        else str(getattr(authority, "__name__", authority.__class__.__name__))
    )
    return {glyph: index for index, glyph in enumerate(carrier)}, name


def _letter_floor(
    source: str,
    source_id: str,
    source_index: _SourceIndex,
    registry: _Registry,
    positions: dict[str, int] | None,
    geometry_name: str,
) -> tuple[ClosedGonol, ...]:
    letters: list[ClosedGonol] = []
    for index, character in enumerate(source):
        address = f"{source_id}#letter:{index}"
        if positions is None:
            position = "hmmm:not-supplied"
        else:
            found = positions.get(character)
            position = "hmmm:not-on-pinned-carrier" if found is None else str(found)
        letters.append(
            registry.close(
                address=address,
                scale="letter",
                start=index,
                end=index + 1,
                relation_kind="python.source.letter-occurrence",
                properties=(
                    ("unicode_scalar", character),
                    ("code_point", f"U+{ord(character):04X}"),
                    ("occurrence", str(index)),
                    ("public_gonol_position", position),
                    ("public_gonol_function", "hmmm"),
                ),
                provenance=(("geometry_authority", geometry_name),),
            )
        )
    return tuple(letters)


def _token_relation(token_type: int, spelling: str) -> tuple[str, str]:
    token_name = token_module.tok_name[token_type]
    if token_type == token_module.NAME and keyword.iskeyword(spelling):
        return "KEYWORD", token_name
    if token_type == token_module.OP:
        return token_module.tok_name.get(tokenize.EXACT_TOKEN_TYPES.get(spelling, token_type), "OP"), token_name
    return token_name, token_name


def _lexical_floor(
    source: str,
    source_id: str,
    source_index: _SourceIndex,
    registry: _Registry,
    letters: Sequence[ClosedGonol],
) -> tuple[tuple[_LexicalWitness, ...], tuple[str, ...], tuple[str, ...]]:
    raw_tokens: list[tuple[int, int, str, str, str]] = []
    zero_width: list[str] = []
    unresolved: list[str] = []
    stream = tokenize.generate_tokens(io.StringIO(source_index.recognition_source).readline)
    while True:
        try:
            item = next(stream)
        except StopIteration:
            break
        except (tokenize.TokenError, IndentationError, SyntaxError) as exc:
            detail = exc.args[0] if exc.args else exc.__class__.__name__
            location = exc.args[1] if len(exc.args) > 1 else None
            unresolved.append(f"tokenizer: {detail}; location={location!r}")
            break
        exact_name, token_name = _token_relation(item.type, item.string)
        if item.string == "":
            if token_name not in {"ENDMARKER", "ENCODING"}:
                zero_width.append(
                    f"{token_name}@{source_index.token_offset(item.start)}"
                )
            continue
        start = source_index.token_offset(item.start)
        end = source_index.token_offset(item.end)
        if start == end:
            if token_name not in {"ENDMARKER", "ENCODING"}:
                zero_width.append(f"{token_name}@{start}")
            continue
        recognition_start = source_index.recognition_line_starts[item.start[0] - 1] + item.start[1]
        recognition_end = source_index.recognition_line_starts[item.end[0] - 1] + item.end[1]
        spelling = source_index.recognition_source[recognition_start:recognition_end]
        if spelling != item.string:
            unresolved.append(
                f"tokenizer spelling mismatch at {start}:{end}; witness={item.string!r} source={spelling!r}"
            )
        raw_tokens.append((start, end, token_name, exact_name, spelling))

    raw_tokens.sort(key=lambda value: (value[0], value[1]))
    previous = 0
    complete: list[tuple[int, int, str, str, str]] = []
    for start, end, token_name, exact_name, spelling in raw_tokens:
        if start < previous:
            unresolved.append(f"overlapping lexical witnesses at decoded offset {start}")
            continue
        if start > previous:
            complete.append((previous, start, "INTERTOKEN", "INTERTOKEN", source[previous:start]))
        complete.append((start, end, token_name, exact_name, spelling))
        previous = end
    if previous < len(source):
        complete.append((previous, len(source), "INTERTOKEN", "INTERTOKEN", source[previous:]))

    witnesses: list[_LexicalWitness] = []
    for lexical_index, (start, end, token_name, exact_name, spelling) in enumerate(complete):
        candidates = tuple(
            _MemberCandidate(role=f"letter[{offset - start}]", gonol=letters[offset], priority=3)
            for offset in range(start, end)
        )
        address = f"{source_id}#lexical:{lexical_index}:{start}-{end}"
        gonol = registry.close(
            address=address,
            scale="lexical-form",
            start=start,
            end=end,
            relation_kind=f"python.lexical.{exact_name}",
            candidates=candidates,
            properties=(
                ("tokenizer_class", token_name),
                ("exact_form", exact_name),
                ("source_length", str(end - start)),
            ),
            provenance=(("recognition_witness", "stdlib.tokenize/python-3.12"),),
        )
        witnesses.append(_LexicalWitness(start, end, token_name, exact_name, spelling, gonol))
    return tuple(witnesses), tuple(zero_width), tuple(unresolved)


def _member_sort_key(candidate: _MemberCandidate) -> tuple[int, int, int, str, str]:
    span = candidate.gonol.span
    return (span.start, candidate.priority, -span.end, candidate.role, candidate.gonol.address)


def _maximal_enclosures(
    enclosures: Sequence[ClosedGonol],
    start: int,
    end: int,
    *,
    excluded: Sequence[tuple[int, int]] = (),
) -> tuple[ClosedGonol, ...]:
    eligible = [
        item
        for item in enclosures
        if start <= item.span.start
        and item.span.end <= end
        and not any(left <= item.span.start and item.span.end <= right for left, right in excluded)
    ]
    selected: list[ClosedGonol] = []
    for item in sorted(eligible, key=lambda value: (value.span.start, -value.span.end)):
        if any(
            parent.span.start <= item.span.start and item.span.end <= parent.span.end
            for parent in selected
        ):
            continue
        selected.append(item)
    return tuple(selected)


def _delimiter_gonols(
    source_id: str,
    registry: _Registry,
    letters: Sequence[ClosedGonol],
    lexicals: Sequence[_LexicalWitness],
) -> tuple[tuple[ClosedGonol, ...], tuple[str, ...]]:
    openers = {"(": ")", "[": "]", "{": "}"}
    names = {"(": "parentheses", "[": "brackets", "{": "braces"}
    stack: list[_LexicalWitness] = []
    pairs: list[tuple[_LexicalWitness, _LexicalWitness]] = []
    unresolved: list[str] = []
    for item in lexicals:
        if item.spelling in openers and item.exact_name in {"LPAR", "LSQB", "LBRACE"}:
            stack.append(item)
        elif item.spelling in {")", "]", "}"} and item.exact_name in {"RPAR", "RSQB", "RBRACE"}:
            if not stack:
                unresolved.append(f"unmatched closing delimiter {item.spelling!r} at {item.start}")
                continue
            opener = stack.pop()
            if openers[opener.spelling] != item.spelling:
                unresolved.append(
                    f"delimiter mismatch {opener.spelling!r}@{opener.start} with {item.spelling!r}@{item.start}"
                )
                continue
            pairs.append((opener, item))
    for opener in stack:
        unresolved.append(f"unmatched opening delimiter {opener.spelling!r} at {opener.start}")

    built: list[ClosedGonol] = []
    for pair_index, (opener, closer) in enumerate(
        sorted(pairs, key=lambda pair: (pair[1].end - pair[0].start, pair[0].start))
    ):
        start, end = opener.start, closer.end
        nested = _maximal_enclosures(built, start, end)
        nested_ranges = tuple((item.span.start, item.span.end) for item in nested)
        candidates: list[_MemberCandidate] = []
        for item in lexicals:
            if not (start <= item.start and item.end <= end):
                continue
            if any(left <= item.start and item.end <= right for left, right in nested_ranges):
                continue
            role = "opener" if item is opener else "closer" if item is closer else "content"
            candidates.append(_MemberCandidate(role, item.gonol, 2))
        candidates.extend(_MemberCandidate("nested", item, 1) for item in nested)
        candidates.sort(key=_member_sort_key)
        counter = 0
        normalized: list[_MemberCandidate] = []
        for candidate in candidates:
            if candidate.role in {"content", "nested"}:
                normalized.append(replace(candidate, role=f"content[{counter}]"))
                counter += 1
            else:
                normalized.append(candidate)
        built.append(
            registry.close(
                address=f"{source_id}#delimiter:{pair_index}:{start}-{end}",
                scale="delimiter-construction",
                start=start,
                end=end,
                relation_kind=f"python.delimiter.{names[opener.spelling]}",
                candidates=normalized,
                properties=(
                    ("opener", opener.spelling),
                    ("closer", closer.spelling),
                    ("closure", "matched"),
                ),
                provenance=(("recognition_witness", "python-3.12 delimiter stack"),),
                hmmm=("exact UCNS delimiter relation geometry",),
            )
        )
    return tuple(built), tuple(unresolved)


def _primitive_properties(node: ast.AST) -> tuple[tuple[str, str], ...]:
    properties: list[tuple[str, str]] = []
    skipped_values = {
        ("Constant", "value"),
        ("MatchSingleton", "value"),
    }
    for field, value in ast.iter_fields(node):
        if field == "ctx" or (node.__class__.__name__, field) in skipped_values:
            continue
        if isinstance(value, ast.AST):
            if isinstance(value, (ast.operator, ast.unaryop, ast.boolop, ast.cmpop)):
                properties.append((f"grammar_field.{field}", value.__class__.__name__))
            continue
        if isinstance(value, list):
            if value and all(isinstance(item, str) for item in value):
                properties.append((f"grammar_field.{field}", json.dumps(value, ensure_ascii=False)))
            continue
        if value is None:
            continue
        if isinstance(value, (str, int, bool)):
            properties.append((f"grammar_field.{field}", json.dumps(value, ensure_ascii=False)))
    return tuple(properties)


def _spanless_relation_property(field: str, node: ast.AST) -> tuple[str, str]:
    """Keep a witnessed child relation inside its source-built parent.

    A few CPython grammar records, notably an empty ``arguments`` value and
    ``TypeIgnore``, have no independent source span.  They cannot honestly
    close as gonols of their own.  Their relation is therefore recorded on the
    parent that already owns the exact surface gonols; the parser record itself
    is discarded.
    """

    descriptor: dict[str, Any] = {"grammar_construct": node.__class__.__name__}
    for name, value in ast.iter_fields(node):
        if isinstance(value, (str, int, bool)) or value is None:
            descriptor[name] = value
        elif isinstance(value, list) and not any(isinstance(item, ast.AST) for item in value):
            descriptor[name] = value
    return (
        f"grammar_field.{field}.spanless_relation",
        json.dumps(descriptor, ensure_ascii=False, sort_keys=True, separators=(",", ":")),
    )


def _grammar_root(
    source: str,
    source_id: str,
    source_index: _SourceIndex,
    registry: _Registry,
    letters: Sequence[ClosedGonol],
    lexicals: Sequence[_LexicalWitness],
    enclosures: Sequence[ClosedGonol],
    zero_width: Sequence[str],
) -> tuple[ClosedGonol | None, tuple[str, ...]]:
    try:
        tree = ast.parse(
            source_index.recognition_source,
            filename=source_id,
            mode="exec",
            type_comments=True,
            feature_version=(3, 12),
        )
    except (SyntaxError, ValueError, TypeError, MemoryError) as exc:
        if isinstance(exc, SyntaxError):
            detail = f"grammar: {exc.msg}; line={exc.lineno!r}; offset={exc.offset!r}"
        else:
            detail = f"grammar: {exc.__class__.__name__}: {exc}"
        return None, (detail,)

    nodes = list(ast.walk(tree))
    node_order = {id(node): index for index, node in enumerate(nodes)}
    span_memo: dict[int, tuple[int, int] | None] = {}

    for node in reversed(nodes):
        key = id(node)
        spans: list[tuple[int, int]] = []
        if all(hasattr(node, name) for name in ("lineno", "col_offset", "end_lineno", "end_col_offset")):
            end_line = getattr(node, "end_lineno", None)
            end_column = getattr(node, "end_col_offset", None)
            if end_line is not None and end_column is not None:
                spans.append(
                    (
                        source_index.ast_offset(int(node.lineno), int(node.col_offset)),
                        source_index.ast_offset(int(end_line), int(end_column)),
                    )
                )
        for child in ast.iter_child_nodes(node):
            child_span = span_memo.get(id(child))
            if child_span is not None:
                spans.append(child_span)
        if isinstance(node, ast.Module):
            result: tuple[int, int] | None = (0, len(source))
        elif spans:
            result = (min(item[0] for item in spans), max(item[1] for item in spans))
        else:
            result = None
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)) and node.decorator_list:
            first_decorator = min(node.decorator_list, key=lambda item: (item.lineno, item.col_offset))
            decorator_start = source_index.ast_offset(
                int(first_decorator.lineno), int(first_decorator.col_offset)
            )
            marker = max(
                (
                    item
                    for item in lexicals
                    if item.spelling == "@"
                    and item.exact_name == "AT"
                    and item.end <= decorator_start
                    and source_index.line_column(item.start)[0] == int(first_decorator.lineno)
                ),
                key=lambda item: item.start,
                default=None,
            )
            if marker is not None and result is not None:
                result = (min(marker.start, result[0]), result[1])
        span_memo[key] = result
    built: dict[int, ClosedGonol] = {}

    def construct(node: ast.AST) -> ClosedGonol | None:
        key = id(node)
        if key in built:
            return built[key]
        span = span_memo.get(key)
        if span is None:
            return None
        start, end = span
        child_candidates: list[_MemberCandidate] = []
        child_ranges: list[tuple[int, int]] = []
        spanless_properties: list[tuple[str, str]] = []
        for field, value in ast.iter_fields(node):
            if isinstance(value, ast.AST):
                child = built.get(id(value))
                if child is not None:
                    child_candidates.append(_MemberCandidate(field, child, 0))
                    child_ranges.append((child.span.start, child.span.end))
                elif not isinstance(
                    value,
                    (ast.operator, ast.unaryop, ast.boolop, ast.cmpop, ast.expr_context),
                ):
                    spanless_properties.append(_spanless_relation_property(field, value))
            elif isinstance(value, list):
                for position, item in enumerate(value):
                    if not isinstance(item, ast.AST):
                        continue
                    child = built.get(id(item))
                    if child is not None:
                        child_candidates.append(_MemberCandidate(f"{field}[{position}]", child, 0))
                        child_ranges.append((child.span.start, child.span.end))
                    elif not isinstance(
                        item,
                        (ast.operator, ast.unaryop, ast.boolop, ast.cmpop, ast.expr_context),
                    ):
                        spanless_properties.append(
                            _spanless_relation_property(f"{field}[{position}]", item)
                        )

        selected_enclosures = _maximal_enclosures(
            enclosures,
            start,
            end,
            excluded=child_ranges,
        )
        enclosure_ranges = tuple((item.span.start, item.span.end) for item in selected_enclosures)
        surface_candidates: list[_MemberCandidate] = [
            _MemberCandidate("surface", item, 1) for item in selected_enclosures
        ]
        for lexical in lexicals:
            if not (start <= lexical.start and lexical.end <= end):
                continue
            if any(left <= lexical.start and lexical.end <= right for left, right in child_ranges):
                continue
            if any(left <= lexical.start and lexical.end <= right for left, right in enclosure_ranges):
                continue
            surface_candidates.append(_MemberCandidate("surface", lexical.gonol, 2))

        candidates = child_candidates + surface_candidates
        candidates.sort(key=_member_sort_key)
        surface_index = 0
        normalized: list[_MemberCandidate] = []
        for candidate in candidates:
            if candidate.role == "surface":
                normalized.append(replace(candidate, role=f"surface[{surface_index}]"))
                surface_index += 1
            else:
                normalized.append(candidate)
        properties = [
            ("grammar_profile", LANGUAGE_PROFILE),
            ("grammar_construct", node.__class__.__name__),
        ]
        properties.extend(_primitive_properties(node))
        properties.extend(spanless_properties)
        if isinstance(node, ast.Module):
            properties.extend(
                (f"zero_width_witness[{index}]", item)
                for index, item in enumerate(zero_width)
            )
        value = registry.close(
            address=(
                f"{source_id}#grammar:{node_order[key]}:{node.__class__.__name__}:{start}-{end}"
            ),
            scale="module" if isinstance(node, ast.Module) else "python-construction",
            start=start,
            end=end,
            relation_kind=f"python.grammar.{node.__class__.__name__}",
            candidates=normalized,
            properties=properties,
            provenance=(("recognition_witness", "stdlib.ast/python-3.12"),),
            hmmm=("exact UCNS geometry for this Python relation",),
        )
        built[key] = value
        return value

    for node in reversed(nodes):
        construct(node)
    return built.get(id(tree)), ()


def _compiler_validation(source_index: _SourceIndex, source_id: str) -> tuple[str, ...]:
    """Run CPython's non-executing file-input compiler checks after parsing."""

    try:
        compile(source_index.recognition_source, source_id, "exec", dont_inherit=True)
    except (SyntaxError, ValueError, TypeError, MemoryError) as exc:
        if isinstance(exc, SyntaxError):
            return (f"compiler: {exc.msg}; line={exc.lineno!r}; offset={exc.offset!r}",)
        return (f"compiler: {exc.__class__.__name__}: {exc}",)
    return ()


def _source_root_hmmm(
    source_id: str,
    registry: _Registry,
    letters: Sequence[ClosedGonol],
    lexicals: Sequence[_LexicalWitness],
    enclosures: Sequence[ClosedGonol],
    unresolved: Sequence[str],
    zero_width: Sequence[str],
) -> ClosedGonol:
    selected = _maximal_enclosures(enclosures, 0, len(letters))
    selected_ranges = tuple((item.span.start, item.span.end) for item in selected)
    candidates: list[_MemberCandidate] = [
        _MemberCandidate("closed-delimiter", item, 1) for item in selected
    ]
    for item in lexicals:
        if any(left <= item.start and item.end <= right for left, right in selected_ranges):
            continue
        candidates.append(_MemberCandidate("lexical-form", item.gonol, 2))
    candidates.sort(key=_member_sort_key)
    properties = [("standing", "hmmm")]
    properties.extend((f"unresolved[{index}]", item) for index, item in enumerate(unresolved))
    properties.extend(
        (f"zero_width_witness[{index}]", item) for index, item in enumerate(zero_width)
    )
    return registry.close(
        address=f"{source_id}#source:hmmm",
        scale="source",
        start=0,
        end=len(letters),
        relation_kind="python.source.hmmm",
        candidates=candidates,
        properties=properties,
        provenance=(("recognition_witness", "partial Python 3.12 recognition"),),
        hmmm=unresolved,
    )


def _receipt_digest(receipt: PythonAffixiationReceipt) -> str:
    return sha256(canonical_json_bytes(receipt.payload())).hexdigest()


def _construct(
    source: str,
    *,
    source_id: str,
    source_bytes: bytes,
    encoding: str,
    geometry_authority: Any | None,
) -> PythonAffixiationReceipt:
    _require_source(source, source_id)
    if platform.python_implementation() != "CPython" or tuple(sys.version_info[:3]) != CPYTHON_VERSION:
        raise PythonGonolConstructionError(
            f"{LANGUAGE_PROFILE} requires CPython 3.12.14; got "
            f"{platform.python_implementation()} {platform.python_version()}"
        )
    source_index = _SourceIndex(source)
    registry = _Registry(source_id, source_index)
    positions, geometry_name = _public_gonol_positions(geometry_authority)
    letters = _letter_floor(
        source,
        source_id,
        source_index,
        registry,
        positions,
        geometry_name,
    )
    lexicals, zero_width, lexical_hmmm = _lexical_floor(
        source,
        source_id,
        source_index,
        registry,
        letters,
    )
    enclosures, delimiter_hmmm = _delimiter_gonols(
        source_id,
        registry,
        letters,
        lexicals,
    )
    grammar_root, grammar_hmmm = _grammar_root(
        source,
        source_id,
        source_index,
        registry,
        letters,
        lexicals,
        enclosures,
        zero_width,
    )
    compiler_hmmm = _compiler_validation(source_index, source_id)
    syntax_hmmm = lexical_hmmm + delimiter_hmmm + grammar_hmmm + compiler_hmmm
    if grammar_root is None or syntax_hmmm:
        root = _source_root_hmmm(
            source_id,
            registry,
            letters,
            lexicals,
            enclosures,
            syntax_hmmm or ("grammar root was not constructed",),
            zero_width,
        )
        standing = "hmmm"
    else:
        root = grammar_root
        standing = STANDING

    hmmm = list(BASE_HMMM)
    if geometry_authority is None:
        hmmm.append("UCNS Public Gonol geometry authority was not supplied")
    if positions is not None and any(character not in positions for character in source):
        hmmm.append("one or more admitted source scalars have no position on the pinned Public Gonol carrier")
    hmmm.extend(syntax_hmmm)
    runtime = f"{platform.python_implementation()}-{platform.python_version()}"
    provisional = PythonAffixiationReceipt(
        schema=SCHEMA,
        version=SCHEMA_VERSION,
        constructor_id=CONSTRUCTOR_ID,
        constructor_version=CONSTRUCTOR_VERSION,
        language_profile=LANGUAGE_PROFILE,
        source_id=source_id,
        encoding=encoding,
        source_bytes_base64=base64.b64encode(source_bytes).decode("ascii"),
        source_bytes_sha256=sha256(source_bytes).hexdigest(),
        decoded_source_sha256=sha256(source.encode("utf-8")).hexdigest(),
        recognition_witness=runtime,
        standing=standing,
        selection_effect=SELECTION_EFFECT,
        root_gonol_id=root.gonol_id,
        gonols=tuple(registry.values),
        nonclaims=NONCLAIMS,
        hmmm=tuple(hmmm),
        receipt_digest="",
    )
    return replace(provisional, receipt_digest=_receipt_digest(provisional))


def affixiate_python_source(
    source: str,
    *,
    source_id: str,
    geometry_authority: Any | None = None,
) -> PythonAffixiationReceipt:
    """Affixiate exact decoded Python 3.12 file-input source from letters upward."""

    if not isinstance(source, str):
        raise TypeError("source must be an exact decoded Unicode string")
    return _construct(
        source,
        source_id=source_id,
        source_bytes=source.encode("utf-8"),
        encoding="utf-8",
        geometry_authority=geometry_authority,
    )


def affixiate_python_bytes(
    source_bytes: bytes,
    *,
    source_id: str,
    geometry_authority: Any | None = None,
) -> PythonAffixiationReceipt:
    """Detect Python's declared encoding, preserve exact bytes, and affixiate source."""

    if not isinstance(source_bytes, bytes):
        raise TypeError("source_bytes must be exact bytes")
    try:
        encoding, _lines = tokenize.detect_encoding(io.BytesIO(source_bytes).readline)
        source = source_bytes.decode(encoding)
    except (SyntaxError, UnicodeDecodeError, LookupError) as exc:
        raise PythonGonolConstructionError(f"Python source decoding failed: {exc}") from exc
    return _construct(
        source,
        source_id=source_id,
        source_bytes=source_bytes,
        encoding=encoding,
        geometry_authority=geometry_authority,
    )


def _property(gonol: ClosedGonol, name: str) -> str:
    values = [value for key, value in gonol.relation.properties if key == name]
    if len(values) != 1:
        raise PythonGonolConstructionError(
            f"gonol {gonol.address} must carry exactly one {name!r} property"
        )
    return values[0]


def reconstruct_source(receipt: PythonAffixiationReceipt) -> str:
    """Reconstruct decoded source solely from ordered letter gonols."""

    letters = sorted(
        (gonol for gonol in receipt.gonols if gonol.scale == "letter"),
        key=lambda gonol: gonol.span.start,
    )
    return "".join(_property(gonol, "unicode_scalar") for gonol in letters)


def replay_python_affixiation(receipt: PythonAffixiationReceipt) -> PythonAffixiationReceipt:
    """Fail closed unless every visible gonol and receipt identity remains valid."""

    if not isinstance(receipt, PythonAffixiationReceipt):
        raise TypeError("receipt must be a PythonAffixiationReceipt")
    expected = (SCHEMA, SCHEMA_VERSION, CONSTRUCTOR_ID, CONSTRUCTOR_VERSION, LANGUAGE_PROFILE)
    actual = (
        receipt.schema,
        receipt.version,
        receipt.constructor_id,
        receipt.constructor_version,
        receipt.language_profile,
    )
    if actual != expected:
        raise PythonGonolConstructionError("receipt schema, constructor, or language profile mismatch")
    try:
        raw = base64.b64decode(receipt.source_bytes_base64, validate=True)
    except ValueError as exc:
        raise PythonGonolConstructionError("receipt source bytes are not valid base64") from exc
    if sha256(raw).hexdigest() != receipt.source_bytes_sha256:
        raise PythonGonolConstructionError("receipt source byte digest mismatch")
    source = reconstruct_source(receipt)
    if sha256(source.encode("utf-8")).hexdigest() != receipt.decoded_source_sha256:
        raise PythonGonolConstructionError("decoded source digest mismatch")
    try:
        decoded = raw.decode(receipt.encoding)
    except (UnicodeDecodeError, LookupError) as exc:
        raise PythonGonolConstructionError("receipt source bytes no longer decode as declared") from exc
    if decoded != source:
        raise PythonGonolConstructionError("receipt bytes and letter gonols reconstruct different source")

    source_index = _SourceIndex(source)
    known: dict[str, ClosedGonol] = {}
    known_addresses: set[str] = set()
    expected_letter_start = 0
    for gonol in receipt.gonols:
        if gonol.gonol_id in known:
            raise PythonGonolConstructionError("duplicate gonol identity in receipt")
        if gonol.address in known_addresses:
            raise PythonGonolConstructionError("duplicate gonol address in receipt")
        expected_id = sha256(canonical_json_bytes(gonol.identity_payload())).hexdigest()
        if gonol.gonol_id != expected_id:
            raise PythonGonolConstructionError(f"gonol identity mismatch: {gonol.address}")
        if gonol.span != source_index.span(gonol.span.start, gonol.span.end):
            raise PythonGonolConstructionError(f"source coordinates drifted: {gonol.address}")
        if tuple(member.ordinal for member in gonol.relation.members) != tuple(
            range(len(gonol.relation.members))
        ):
            raise PythonGonolConstructionError(f"member order drifted: {gonol.address}")
        member_spans: list[tuple[int, int]] = []
        for member in gonol.relation.members:
            child = known.get(member.gonol_id)
            if child is None or child.address != member.address:
                raise PythonGonolConstructionError(
                    f"gonol references a child that was not already closed: {gonol.address}"
                )
            member_spans.append((child.span.start, child.span.end))
        if gonol.scale == "letter":
            if gonol.span.start != expected_letter_start or gonol.span.end != expected_letter_start + 1:
                raise PythonGonolConstructionError("letter floor is not contiguous and ordered")
            scalar = _property(gonol, "unicode_scalar")
            if len(scalar) != 1 or scalar != source[gonol.span.start : gonol.span.end]:
                raise PythonGonolConstructionError("letter gonol does not match its source occurrence")
            expected_letter_start += 1
        else:
            merged: list[list[int]] = []
            for start, end in sorted(member_spans):
                if not merged or start > merged[-1][1]:
                    merged.append([start, end])
                elif end > merged[-1][1]:
                    merged[-1][1] = end
            expected = [] if gonol.span.start == gonol.span.end else [[gonol.span.start, gonol.span.end]]
            if merged != expected:
                raise PythonGonolConstructionError(
                    f"gonol span differs from its atomic closed participants: {gonol.address}"
                )
        known[gonol.gonol_id] = gonol
        known_addresses.add(gonol.address)
    if expected_letter_start != len(source):
        raise PythonGonolConstructionError("letter floor does not cover complete decoded source")
    root = known.get(receipt.root_gonol_id)
    if (
        root is None
        or not receipt.gonols
        or root is not receipt.gonols[-1]
        or root.span.start != 0
        or root.span.end != len(source)
        or root.scale not in {"module", "source"}
    ):
        raise PythonGonolConstructionError("receipt root does not cover every source occurrence")
    root_kind = root.relation.kind
    if receipt.standing == STANDING:
        if root.scale != "module" or root_kind != "python.grammar.Module":
            raise PythonGonolConstructionError(
                "implemented-candidate receipt must be rooted at a compiler-valid module"
            )
    elif receipt.standing == "hmmm":
        if root.scale != "source" or root_kind != "python.source.hmmm":
            raise PythonGonolConstructionError(
                "hmmm receipt must be rooted at the source-hmmm construction"
            )
    else:
        raise PythonGonolConstructionError(f"unsupported receipt standing: {receipt.standing!r}")
    if receipt.nonclaims != NONCLAIMS or not all(item in receipt.hmmm for item in BASE_HMMM):
        raise PythonGonolConstructionError("receipt nonclaim or hmmm boundary mismatch")
    if receipt.receipt_digest != _receipt_digest(replace(receipt, receipt_digest="")):
        raise PythonGonolConstructionError("receipt digest mismatch")
    return receipt


__all__ = [
    "CONSTRUCTOR_ID",
    "CONSTRUCTOR_VERSION",
    "LANGUAGE_PROFILE",
    "PINNED_PUBLIC_GONOL_SHA256",
    "PythonGonolConstructionError",
    "affixiate_python_bytes",
    "affixiate_python_source",
    "reconstruct_source",
    "replay_python_affixiation",
]
