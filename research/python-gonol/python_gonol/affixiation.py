"""Construct Python 3.12 gonols from exact source characters upward.

Usage guidance
--------------
Use :func:`affixiate_python_bytes` for source files so encoding and exact bytes
remain receipt-bound. Use :func:`affixiate_python_source` for already-decoded
text. The public constructor closes one occurrence-specific character gonol per
Unicode scalar, closes that character's applicable definition gonols, and only
then permits the closed characters to participate atomically in lexical and
larger Python constructions.

CPython ``tokenize`` and ``ast`` remain recognition witnesses only. They never
become gonols and never replace source-built participants.
"""

# === MODULE_BUILD ===
# id: python_gonol_affixiation
#   module_name: python_gonol.affixiation
#   module_kind: engine
#   summary: affixiates exact Python 3.12 source from character occurrences and their definition-spaces through lexical, delimiter, and recursive grammar gonols
#   owner: Python Gonol Construction (stack-local research)
#   public_surface: affixiate_python_source, affixiate_python_bytes, replay_python_affixiation, reconstruct_source, grammar_witness_inventory, PythonGonolConstructionError
#   internal_surface: _upgrade_recognition_receipt, _character_definitions
#   auth_boundary: Python Gonol Construction owns source admission and Python relation construction; METAPAT owns affixiation semantics; UCNS owns geometry
#   storage_boundary: none; caller-owned bytes and receipts remain in memory
#   network_boundary: none
#   user_data_boundary: reads caller-supplied source into an explicit caller-owned receipt and transmits nothing
#   admin_only: false
#   tests: tests.test_affixiation, tests.test_python312_surface
#   rollout: explicit Python 3.12 stack-local candidate
#   rollback: remove the python-gonol workspace before downstream binding
#   requires: Python 3.12 standard library; python_gonol._recognition; optional explicit UCNS Public Gonol authority
#   since: 2026-09-12
#   unresolved: exact UCNS affixiation geometry and exhaustive CPython grammar-corpus parity remain hmmm
# === END MODULE_BUILD ===

# === CONTRACTS ===
# id: every_python_source_character_closes_first
#   given: any admitted decoded Python source string
#   then: exactly one independently addressable character gonol closes for every Unicode scalar occurrence in exact source order
#   class: construction
#
# id: python_character_definitions_share_character_origin
#   given: a source character occurrence has applicable Unicode or Python lexical-profile definitions
#   then: each definition closes as its own gonol over that already-closed character origin before lexical construction begins
#   class: construction
#
# id: python_lexical_forms_affixiate_characters
#   given: the Python 3.12 lexical witness recognizes a nonempty form or inter-token source gap
#   then: one lexical gonol closes over the exact ordered character gonols covering that form without normalization or omission
#   class: construction
#
# id: python_constructions_affixiate_closed_gonols
#   given: delimiter and Python grammar relations are recognized after the character and lexical floors close
#   then: every larger construction references already-closed gonols atomically and carries its constitutive relation, order, roles, multiplicity, source span, and provenance inside its identity
#   class: construction
#
# id: python_affixiation_is_lossless_and_replayable
#   given: a completed Python affixiation receipt
#   then: exact decoded source reconstructs from character gonols and every gonol plus the receipt digest verifies deterministically
#   class: replay
#
# id: parser_objects_never_become_gonols
#   given: tokenizer and AST recognition witnesses are used
#   then: receipt gonols contain only source-built relation records and closed-gonol references, never TokenInfo, AST, code, or compiler objects
#   class: boundary
# === END CONTRACTS ===

from __future__ import annotations

import ast
import base64
import binascii
from collections import Counter
from dataclasses import replace
from hashlib import sha256
import token as token_module
import tokenize
import unicodedata
from typing import Any, Iterable

from . import _recognition
from .model import (
    AffixiationRelation,
    ClosedGonol,
    PythonAffixiationReceipt,
    RelationMember,
    canonical_json_bytes,
)

SCHEMA = _recognition.SCHEMA
SCHEMA_VERSION = "1.1.0"
CONSTRUCTOR_ID = _recognition.CONSTRUCTOR_ID
CONSTRUCTOR_VERSION = "0.2.0"
LANGUAGE_PROFILE = _recognition.LANGUAGE_PROFILE
PINNED_PUBLIC_GONOL_SHA256 = _recognition.PINNED_PUBLIC_GONOL_SHA256
STANDING = _recognition.STANDING
SELECTION_EFFECT = _recognition.SELECTION_EFFECT
RELATION_AUTHORITY = _recognition.RELATION_AUTHORITY
NONCLAIMS = _recognition.NONCLAIMS
BASE_HMMM = _recognition.BASE_HMMM
PythonGonolConstructionError = _recognition.PythonGonolConstructionError


def _identity(gonol: ClosedGonol) -> str:
    return sha256(canonical_json_bytes(gonol.identity_payload())).hexdigest()


def _rewrite_provenance(provenance: Iterable[tuple[str, str]]) -> tuple[tuple[str, str], ...]:
    rewritten: list[tuple[str, str]] = []
    saw_constructor = False
    for key, value in provenance:
        if key == "constructor":
            rewritten.append((key, f"{CONSTRUCTOR_ID}/{CONSTRUCTOR_VERSION}"))
            saw_constructor = True
        else:
            rewritten.append((key, value))
    if not saw_constructor:
        rewritten.insert(0, ("constructor", f"{CONSTRUCTOR_ID}/{CONSTRUCTOR_VERSION}"))
    return tuple(rewritten)


def _character_definitions(character: str) -> tuple[tuple[str, str], ...]:
    """Return deterministic definitions applicable to one source character.

    These are definition-space facts, not the contextual lexical role of this
    occurrence. A character may therefore have several definitions at once.
    """

    values: set[tuple[str, str]] = {
        ("unicode-category", unicodedata.category(character)),
    }
    unicode_name = unicodedata.name(character, "")
    if unicode_name:
        values.add(("unicode-name", unicode_name))

    if character.isidentifier():
        values.add(("python-identifier", "start"))
    if ("A" + character).isidentifier():
        values.add(("python-identifier", "continue"))
    if character.isdecimal():
        values.add(("python-numeric", "decimal-digit"))
    if character in " \t\f":
        values.add(("python-layout", "horizontal-whitespace"))
    if character in "\r\n":
        values.add(("python-layout", "line-break"))
    if character in {"'", '"'}:
        values.add(("python-delimiter", "string-quote-candidate"))
    if character == "#":
        values.add(("python-delimiter", "comment-introducer"))
    if character == "\\":
        values.add(("python-layout", "explicit-line-join-candidate"))

    for spelling, token_type in tokenize.EXACT_TOKEN_TYPES.items():
        if len(spelling) == 1 and spelling == character:
            values.add(("python-exact-token", token_module.tok_name[token_type]))

    return tuple(sorted(values))


def _character_from_recognition(old: ClosedGonol) -> ClosedGonol:
    relation = replace(old.relation, kind="python.source.character-occurrence", members=())
    prefix, marker, suffix = old.address.rpartition("#letter:")
    if not marker:
        raise PythonGonolConstructionError(f"recognition letter address is malformed: {old.address}")
    provisional = replace(
        old,
        address=prefix + "#character:" + suffix,
        scale="character",
        relation=relation,
        provenance=_rewrite_provenance(old.provenance),
        gonol_id="",
    )
    return replace(provisional, gonol_id=_identity(provisional))


def _definition_gonol(
    *,
    source_id: str,
    character: ClosedGonol,
    character_index: int,
    definition_index: int,
    kind: str,
    value: str,
) -> ClosedGonol:
    relation = AffixiationRelation(
        kind="python.character.definition",
        members=(
            RelationMember(
                ordinal=0,
                role="origin",
                gonol_id=character.gonol_id,
                address=character.address,
            ),
        ),
        properties=(
            ("definition_kind", kind),
            ("definition_value", value),
        ),
        authority=RELATION_AUTHORITY,
    )
    provisional = ClosedGonol(
        address=f"{source_id}#character-definition:{character_index}:{definition_index}",
        scale="character-definition",
        span=character.span,
        relation=relation,
        provenance=(
            ("constructor", f"{CONSTRUCTOR_ID}/{CONSTRUCTOR_VERSION}"),
            ("language_profile", LANGUAGE_PROFILE),
            ("source_id", source_id),
            ("definition_authority", f"Python 3.12 lexical profile + Unicode {unicodedata.unidata_version}"),
        ),
        hmmm=(),
        gonol_id="",
    )
    return replace(provisional, gonol_id=_identity(provisional))


def _remap_gonol(old: ClosedGonol, mapped: dict[str, ClosedGonol]) -> ClosedGonol:
    members: list[RelationMember] = []
    for member in old.relation.members:
        child = mapped.get(member.gonol_id)
        if child is None:
            raise PythonGonolConstructionError(
                f"recognition witness referenced an unclosed child: {old.address}"
            )
        role = member.role
        if role.startswith("letter["):
            role = "character[" + role[len("letter[") :]
        members.append(
            RelationMember(
                ordinal=member.ordinal,
                role=role,
                gonol_id=child.gonol_id,
                address=child.address,
            )
        )
    provisional = replace(
        old,
        relation=replace(old.relation, members=tuple(members)),
        provenance=_rewrite_provenance(old.provenance),
        gonol_id="",
    )
    return replace(provisional, gonol_id=_identity(provisional))


def _receipt_digest(receipt: PythonAffixiationReceipt) -> str:
    return sha256(canonical_json_bytes(receipt.payload())).hexdigest()


def _upgrade_recognition_receipt(
    recognized: PythonAffixiationReceipt,
) -> PythonAffixiationReceipt:
    """Close the public character/definition construction from a private witness plan."""

    mapped: dict[str, ClosedGonol] = {}
    values: list[ClosedGonol] = []
    character_index = 0

    for old in recognized.gonols:
        if old.scale == "letter":
            character = _character_from_recognition(old)
            mapped[old.gonol_id] = character
            values.append(character)
            scalar = dict(character.relation.properties).get("unicode_scalar")
            if scalar is None or len(scalar) != 1:
                raise PythonGonolConstructionError(
                    f"recognition character has no exact Unicode scalar: {old.address}"
                )
            for definition_index, (kind, value) in enumerate(_character_definitions(scalar)):
                values.append(
                    _definition_gonol(
                        source_id=recognized.source_id,
                        character=character,
                        character_index=character_index,
                        definition_index=definition_index,
                        kind=kind,
                        value=value,
                    )
                )
            character_index += 1
            continue

        value = _remap_gonol(old, mapped)
        mapped[old.gonol_id] = value
        values.append(value)

    root = mapped.get(recognized.root_gonol_id)
    if root is None:
        raise PythonGonolConstructionError("recognition root was not remapped")

    provisional = replace(
        recognized,
        version=SCHEMA_VERSION,
        constructor_version=CONSTRUCTOR_VERSION,
        root_gonol_id=root.gonol_id,
        gonols=tuple(values),
        receipt_digest="",
    )
    return replace(provisional, receipt_digest=_receipt_digest(provisional))


def affixiate_python_source(
    source: str,
    *,
    source_id: str,
    geometry_authority: Any | None = None,
) -> PythonAffixiationReceipt:
    """Affixiate exact decoded Python 3.12 file-input source from characters upward."""

    recognized = _recognition.affixiate_python_source(
        source,
        source_id=source_id,
        geometry_authority=geometry_authority,
    )
    return _upgrade_recognition_receipt(recognized)


def affixiate_python_bytes(
    source_bytes: bytes,
    *,
    source_id: str,
    geometry_authority: Any | None = None,
) -> PythonAffixiationReceipt:
    """Detect Python's declared encoding, preserve exact bytes, and affixiate source."""

    recognized = _recognition.affixiate_python_bytes(
        source_bytes,
        source_id=source_id,
        geometry_authority=geometry_authority,
    )
    return _upgrade_recognition_receipt(recognized)


def _property(gonol: ClosedGonol, name: str) -> str:
    values = [value for key, value in gonol.relation.properties if key == name]
    if len(values) != 1:
        raise PythonGonolConstructionError(
            f"gonol {gonol.address} must carry exactly one {name!r} property"
        )
    return values[0]


def reconstruct_source(receipt: PythonAffixiationReceipt) -> str:
    """Reconstruct decoded source solely from ordered character gonols."""

    characters = sorted(
        (gonol for gonol in receipt.gonols if gonol.scale == "character"),
        key=lambda gonol: gonol.span.start,
    )
    return "".join(_property(gonol, "unicode_scalar") for gonol in characters)


def grammar_witness_inventory() -> tuple[str, ...]:
    """Return the public CPython AST witness vocabulary for the pinned runtime profile.

    The constructor itself does not dispatch on this list; ``_recognition`` walks
    arbitrary AST fields recursively. This inventory exists so runtime/profile
    drift is visible instead of silently narrowing the claimed witness surface.
    """

    return tuple(
        sorted(
            name
            for name, value in vars(ast).items()
            if isinstance(value, type)
            and issubclass(value, ast.AST)
            and value is not ast.AST
            and not name.startswith("_")
        )
    )


def replay_python_affixiation(receipt: PythonAffixiationReceipt) -> PythonAffixiationReceipt:
    """Fail closed unless every public character-first construction remains valid."""

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
    except (ValueError, binascii.Error) as exc:
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
        raise PythonGonolConstructionError("receipt bytes and character gonols reconstruct different source")

    source_index = _recognition._SourceIndex(source)
    known: dict[str, ClosedGonol] = {}
    known_addresses: set[str] = set()
    character_definitions: Counter[str] = Counter()
    lexical_characters: Counter[str] = Counter()
    expected_character_start = 0

    for gonol in receipt.gonols:
        if gonol.gonol_id in known:
            raise PythonGonolConstructionError("duplicate gonol identity in receipt")
        if gonol.address in known_addresses:
            raise PythonGonolConstructionError("duplicate gonol address in receipt")
        if gonol.scale == "letter" or "#letter:" in gonol.address:
            raise PythonGonolConstructionError("deprecated letter-floor gonol present")
        expected_id = _identity(replace(gonol, gonol_id=""))
        if gonol.gonol_id != expected_id:
            raise PythonGonolConstructionError(f"gonol identity mismatch: {gonol.address}")
        if gonol.span != source_index.span(gonol.span.start, gonol.span.end):
            raise PythonGonolConstructionError(f"source coordinates drifted: {gonol.address}")
        if tuple(member.ordinal for member in gonol.relation.members) != tuple(
            range(len(gonol.relation.members))
        ):
            raise PythonGonolConstructionError(f"member order drifted: {gonol.address}")

        member_children: list[ClosedGonol] = []
        for member in gonol.relation.members:
            child = known.get(member.gonol_id)
            if child is None or child.address != member.address:
                raise PythonGonolConstructionError(
                    f"gonol references a child that was not already closed: {gonol.address}"
                )
            member_children.append(child)

        if gonol.scale == "character":
            if gonol.relation.members:
                raise PythonGonolConstructionError("character gonol cannot contain prior participants")
            if gonol.span.start != expected_character_start or gonol.span.end != expected_character_start + 1:
                raise PythonGonolConstructionError("character floor is not contiguous and ordered")
            scalar = _property(gonol, "unicode_scalar")
            if len(scalar) != 1 or scalar != source[gonol.span.start : gonol.span.end]:
                raise PythonGonolConstructionError("character gonol does not match its source occurrence")
            expected_character_start += 1
        elif gonol.scale == "character-definition":
            if len(member_children) != 1 or member_children[0].scale != "character":
                raise PythonGonolConstructionError("character definition must have one closed character origin")
            if member_children[0].span != gonol.span:
                raise PythonGonolConstructionError("character definition span differs from its origin")
            _property(gonol, "definition_kind")
            _property(gonol, "definition_value")
            character_definitions[member_children[0].address] += 1
        else:
            merged: list[list[int]] = []
            for child in sorted(member_children, key=lambda item: (item.span.start, item.span.end)):
                if not merged or child.span.start > merged[-1][1]:
                    merged.append([child.span.start, child.span.end])
                elif child.span.end > merged[-1][1]:
                    merged[-1][1] = child.span.end
            expected_span = [] if gonol.span.start == gonol.span.end else [[gonol.span.start, gonol.span.end]]
            if merged != expected_span:
                raise PythonGonolConstructionError(
                    f"gonol span differs from its atomic closed participants: {gonol.address}"
                )
            if gonol.scale == "lexical-form":
                for member, child in zip(gonol.relation.members, member_children, strict=True):
                    if child.scale != "character" or not member.role.startswith("character["):
                        raise PythonGonolConstructionError(
                            "lexical form must affixiate exact closed character occurrences"
                        )
                    lexical_characters[child.address] += 1

        known[gonol.gonol_id] = gonol
        known_addresses.add(gonol.address)

    if expected_character_start != len(source):
        raise PythonGonolConstructionError("character floor does not cover complete decoded source")
    character_addresses = {
        gonol.address for gonol in receipt.gonols if gonol.scale == "character"
    }
    if set(character_definitions) != character_addresses:
        raise PythonGonolConstructionError("every source character must have a definition-space")
    if lexical_characters != Counter({address: 1 for address in character_addresses}):
        raise PythonGonolConstructionError("lexical floor is not an exact partition of source characters")

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
    "grammar_witness_inventory",
    "reconstruct_source",
    "replay_python_affixiation",
]
