"""Ordered path-groupoid lift of recursive complete-return relations.

The earlier complete-return candidate records only the free abelian relation
module.  This module keeps the same target-free geometric inputs but delays
abelianization: every retained relation is realized as a based, oriented loop
with its reversed-frame midpoint kept as a distinct object.  The resulting
subdivided bouquet has fundamental group ``F_r`` and only projects to
``H_1 = Z^r`` through an explicit, lossy operation.

No observed gonol cardinality or arithmetic factor is an input.
"""

# === MODULE_BUILD ===
# id: ucns_ordered_complete_return_groupoid
#   module_name: ordered_complete_return_groupoid
#   module_kind: experiment
#   summary: lifts retained complete-return cycles to a target-free based path groupoid and free return-word representation that preserves traversal order before explicit abelianization
#   owner: The Interdependency
#   public_surface: OrderedReturnGroupoidError, OrientedEdge, PathStep, GroupoidPath, WordLetter, FreeReturnWord, ReturnLoopGenerator, OrderedReturnGroupoid, PermutationOrderProfile, build_ordered_return_groupoid, permutation_order_profile, receipt_payload, receipt_bytes, receipt_digest
#   internal_surface: _stack_root, _canonical_bytes, _file_digest, _source_file_digests, _text, _reduce_letters, _cyclically_reduce_letters, _oriented_cyclic_key, _producer_code_reference, main
#   auth_boundary: none; consumes only the stack-local complete-return relation candidate and its pinned UCNS provenance
#   storage_boundary: read-only at runtime
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: research/ucns/tests/test_ordered_complete_return_groupoid.py
#   rollout: stack-local noncommutative research machinery only; no UCNS canon, stack libs, PCEA, arithmetic-factor, or successor-cardinality promotion
#   rollback: remove this module, its tests, report, and receipt
#   requires: ucns_complete_return_relation_extension, ucns_native_mobius_geometry, gonol-build construction discipline
#   since: 2026-09-02
#   unresolved: geometric authorization for the bouquet attachment across promoted scales; global one-turn monodromy on retained inner loops; cross-generator intersections and relators; orientation policy for unbased closure; arithmetic factor bridge; numerical next gonol
# === END MODULE_BUILD ===

# === CONTRACTS ===
# id: ordered_return_groupoid_lifts_exact_trace
#   given: r unchanged complete-return extensions are retained at one promoted basepoint
#   then: each relation has one positive-to-reversed edge and one reversed-to-positive edge with exact trace provenance and a distinct reversed-frame midpoint
#   class: correctness
#   since: 2026-09-02
#
# id: ordered_return_groupoid_has_free_rank_r
#   given: r unfilled subdivided return loops are attached at their shared promoted positive basepoint
#   then: the connected graph has 2r edges, r+1 vertices, first Betti rank r, and fundamental-group candidate F_r
#   class: correctness
#   since: 2026-09-02
#
# id: ordered_return_groupoid_preserves_composition_order
#   given: based return words and typed groupoid paths are composed
#   then: only adjacent inverse pairs cancel; endpoint mismatches fail closed and distinct generators never commute implicitly
#   class: safety
#   since: 2026-09-02
#
# id: ordered_return_groupoid_preserves_basepoint_and_orientation
#   given: one complete-return loop and its one-turn-shifted loop are represented
#   then: they remain based at distinct frame objects until explicit path transport relates them
#   class: correctness
#   since: 2026-09-02
#
# id: ordered_return_groupoid_abelianizes_explicitly
#   given: differently ordered words use the same signed generator multiset
#   then: the words remain distinct before the explicit exponent-vector projection and coincide only after that projection
#   class: doctrine
#   since: 2026-09-02
#
# id: ordered_return_groupoid_quantifies_closure_order
#   given: every generator is traversed positively exactly once
#   then: rank r has r-factorial distinct based words and (r-1)-factorial oriented cyclic classes, exposing the first unbased cyclic-order distinction at rank three
#   class: correctness
#   since: 2026-09-02
#
# id: ordered_return_groupoid_is_target_free
#   given: the constructor source and receipt are inspected
#   then: no observed successor cardinality, observed factor, desired arithmetic rank, or factor-selection table defines the groupoid or its words
#   class: safety
#   since: 2026-09-02
#
# id: ordered_return_groupoid_receipt_replays
#   given: pinned source identities and candidate assumptions are unchanged
#   then: canonical receipt bytes and digest replay byte-identically
#   class: evidence
#   since: 2026-09-02
# === END CONTRACTS ===

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from hashlib import sha256
from itertools import permutations
import json
from math import factorial
from pathlib import Path
from typing import Any, Iterable, Sequence

import complete_return_relation_extension as extension


SCHEMA_ID = "the-interdependency.stack-research.ucns.ordered-complete-return-groupoid"
SCHEMA_VERSION = "0.1.0"
STANDING = "stack-local-target-free-noncommutative-geometric-candidate"
SELECTION_EFFECT = "none"

POSITIVE_BASE_OBJECT = "return-groupoid.promoted-positive-frame"

NONCLAIMS: tuple[str, ...] = (
    "not UCNS canon",
    "not proof that the full recursive gonol is a bouquet of circles",
    "not a derived global monodromy or cross-generator closure relation",
    "not an arithmetic factor or successor-cardinality operation",
    "not a numerical next-gonol prediction",
    "not PCEA key, entropy, hardness, replay-resistance, recovery, or public-authenticity evidence",
)

HMMM: tuple[str, ...] = (
    "retained relation ids are lifted as basepoint-preserving inclusions at the promoted positive frame; actual recursive transport may apply nontrivial free-group monodromy",
    "each reversed-frame midpoint remains relation-specific so the combined graph has exactly the previously declared rank rather than unsupported mixed half-edge cycles",
    "the local native complete-return trace supplies oriented halves but no cross-generator intersections, crossings, or relators",
    "based words and oriented cyclic closure classes are both retained because UCNS has not declared whether recursive closure forgets the basepoint",
    "orientation reversal is not quotiented; a geometric rule would be required before identifying opposite traversal classes",
    "no current ordered word selects an arithmetic factor cardinality or numerical successor gonol",
)

FALSIFICATION_CONDITIONS: tuple[str, ...] = (
    "the native complete-return trace does not have distinct positive and reversed frame occurrences",
    "recursive promotion does not preserve prior loops at a common based positive occurrence",
    "a required attachment identifies distinct reversed-frame midpoints and introduces additional mixed cycles",
    "a required two-cell or relator fills or identifies one of the declared free loops",
    "path composition accepts mismatched endpoints or reduction reorders distinct generators",
    "cyclic rotation or orientation reversal is applied before the closure policy is geometrically declared",
    "an observed gonol value or arithmetic factor enters groupoid construction",
)

PROMOTION_EVIDENCE: tuple[str, ...] = (
    "derive the basepoint transport of every retained inner loop from full recursive UCNS geometry",
    "derive the action of one complete recursive return on the free-group generators before abelianization",
    "derive cross-generator intersections, crossings, or attaching words from geometry",
    "declare from geometry whether closure retains a basepoint, takes conjugacy classes, or also identifies orientation reversal",
    "validate any later arithmetic invariant only after freezing those ordered geometric data",
)


class OrderedReturnGroupoidError(ValueError):
    """Raised when an ordered return path violates its typed boundary."""


def _stack_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=True,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("ascii")


def _file_digest(root: Path, relative_path: str) -> tuple[str, str]:
    return relative_path, sha256((root / relative_path).read_bytes()).hexdigest()


def _source_file_digests(root: Path) -> tuple[tuple[str, str], ...]:
    return tuple(
        _file_digest(root, path)
        for path in (
            "research/ucns/BASE.json",
            "stack-manifest.json",
            "libs/ucns/src/ucns/direct_mobius.py",
            "research/ucns/complete_return_relation_extension.py",
            "research/ucns/receipts/complete-return-relation-extension-v0.json",
        )
    )


def _text(value: str, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise OrderedReturnGroupoidError(f"{field} must be non-empty text")
    return value


@dataclass(frozen=True, slots=True, order=True)
class WordLetter:
    """One signed generator occurrence in a based free return word."""

    relation_id: str
    exponent: int = 1

    def __post_init__(self) -> None:
        _text(self.relation_id, "relation_id")
        if self.exponent not in (-1, 1):
            raise OrderedReturnGroupoidError("word exponents must be plus or minus one")

    def inverse(self) -> "WordLetter":
        return WordLetter(self.relation_id, -self.exponent)

    def to_payload(self) -> list[Any]:
        return [self.relation_id, self.exponent]


def _reduce_letters(letters: Iterable[WordLetter]) -> tuple[WordLetter, ...]:
    stack: list[WordLetter] = []
    for letter in letters:
        if not isinstance(letter, WordLetter):
            raise OrderedReturnGroupoidError("free words require WordLetter entries")
        if stack and stack[-1].relation_id == letter.relation_id and stack[-1].exponent == -letter.exponent:
            stack.pop()
        else:
            stack.append(letter)
    return tuple(stack)


def _cyclically_reduce_letters(letters: Iterable[WordLetter]) -> tuple[WordLetter, ...]:
    reduced = list(_reduce_letters(letters))
    while (
        len(reduced) >= 2
        and reduced[0].relation_id == reduced[-1].relation_id
        and reduced[0].exponent == -reduced[-1].exponent
    ):
        reduced = reduced[1:-1]
    return tuple(reduced)


def _oriented_cyclic_key(letters: Iterable[WordLetter]) -> tuple[WordLetter, ...]:
    reduced = _cyclically_reduce_letters(letters)
    if not reduced:
        return ()
    rotations = tuple(reduced[index:] + reduced[:index] for index in range(len(reduced)))
    return min(rotations)


@dataclass(frozen=True, slots=True)
class FreeReturnWord:
    """A based word in the retained complete-return loop generators."""

    basis_digest: str
    letters: tuple[WordLetter, ...]

    def __post_init__(self) -> None:
        _text(self.basis_digest, "basis_digest")
        if self.letters != _reduce_letters(self.letters):
            raise OrderedReturnGroupoidError("FreeReturnWord must be freely reduced")

    @property
    def is_identity(self) -> bool:
        return not self.letters

    def inverse(self) -> "FreeReturnWord":
        return FreeReturnWord(
            self.basis_digest,
            tuple(letter.inverse() for letter in reversed(self.letters)),
        )

    def multiply(self, other: "FreeReturnWord") -> "FreeReturnWord":
        if self.basis_digest != other.basis_digest:
            raise OrderedReturnGroupoidError("cannot compose words from different retained bases")
        return FreeReturnWord(
            self.basis_digest,
            _reduce_letters(self.letters + other.letters),
        )

    @property
    def oriented_cyclic_key(self) -> tuple[WordLetter, ...]:
        return _oriented_cyclic_key(self.letters)

    def to_payload(self) -> dict[str, Any]:
        return {
            "basis_digest": self.basis_digest,
            "letters": [letter.to_payload() for letter in self.letters],
        }


@dataclass(frozen=True, slots=True)
class OrientedEdge:
    """One declared positive orientation of a trace half-edge."""

    edge_id: str
    relation_id: str
    half: str
    source: str
    target: str
    trace_sha256: str

    def __post_init__(self) -> None:
        for field, value in (
            ("edge_id", self.edge_id),
            ("relation_id", self.relation_id),
            ("source", self.source),
            ("target", self.target),
            ("trace_sha256", self.trace_sha256),
        ):
            _text(value, field)
        if self.half not in ("positive-to-reversed", "reversed-to-positive"):
            raise OrderedReturnGroupoidError("edge half is not a complete-return trace half")
        if self.source == self.target:
            raise OrderedReturnGroupoidError("trace half-edge endpoints must remain distinct")

    def endpoints(self, orientation: int) -> tuple[str, str]:
        if orientation == 1:
            return self.source, self.target
        if orientation == -1:
            return self.target, self.source
        raise OrderedReturnGroupoidError("edge orientation must be plus or minus one")

    def to_payload(self) -> dict[str, Any]:
        return {
            "edge_id": self.edge_id,
            "relation_id": self.relation_id,
            "half": self.half,
            "source": self.source,
            "target": self.target,
            "trace_sha256": self.trace_sha256,
        }


@dataclass(frozen=True, slots=True)
class PathStep:
    """One oriented traversal of a declared edge."""

    edge_id: str
    orientation: int = 1

    def __post_init__(self) -> None:
        _text(self.edge_id, "edge_id")
        if self.orientation not in (-1, 1):
            raise OrderedReturnGroupoidError("path orientation must be plus or minus one")

    def inverse(self) -> "PathStep":
        return PathStep(self.edge_id, -self.orientation)

    def to_payload(self) -> list[Any]:
        return [self.edge_id, self.orientation]


@dataclass(frozen=True, slots=True)
class GroupoidPath:
    """A typed path whose traversal convention is left to right."""

    groupoid_digest: str
    source: str
    target: str
    steps: tuple[PathStep, ...]

    def __post_init__(self) -> None:
        _text(self.groupoid_digest, "groupoid_digest")
        _text(self.source, "source")
        _text(self.target, "target")

    @property
    def is_loop(self) -> bool:
        return self.source == self.target

    def to_payload(self) -> dict[str, Any]:
        return {
            "source": self.source,
            "target": self.target,
            "steps": [step.to_payload() for step in self.steps],
        }


@dataclass(frozen=True, slots=True)
class ReturnLoopGenerator:
    """One retained relation and its exact subdivided complete-return loop."""

    ordinal: int
    symbol: str
    relation_id: str
    midpoint_object: str
    outbound_edge_id: str
    return_edge_id: str
    trace_sha256: str
    source_atomic_id: str
    promoted_atomic_id: str

    def to_payload(self) -> dict[str, Any]:
        return {
            "ordinal": self.ordinal,
            "symbol": self.symbol,
            "relation_id": self.relation_id,
            "midpoint_object": self.midpoint_object,
            "outbound_edge_id": self.outbound_edge_id,
            "return_edge_id": self.return_edge_id,
            "trace_sha256": self.trace_sha256,
            "source_atomic_id": self.source_atomic_id,
            "promoted_atomic_id": self.promoted_atomic_id,
        }


@dataclass(frozen=True, slots=True)
class OrderedReturnGroupoid:
    """Minimal subdivided-bouquet lift of one retained relation basis."""

    basis_digest: str
    groupoid_digest: str
    base_object: str
    final_atomic_id: str
    generators: tuple[ReturnLoopGenerator, ...]
    edges: tuple[OrientedEdge, ...]
    boundary_rank: int
    first_betti_rank: int

    def __post_init__(self) -> None:
        _text(self.basis_digest, "basis_digest")
        _text(self.groupoid_digest, "groupoid_digest")
        _text(self.base_object, "base_object")
        _text(self.final_atomic_id, "final_atomic_id")
        relation_ids = tuple(item.relation_id for item in self.generators)
        if len(set(relation_ids)) != len(relation_ids):
            raise OrderedReturnGroupoidError("return generator ids must be unique")
        edge_ids = tuple(item.edge_id for item in self.edges)
        if len(set(edge_ids)) != len(edge_ids):
            raise OrderedReturnGroupoidError("edge ids must be unique")
        if len(self.edges) != 2 * len(self.generators):
            raise OrderedReturnGroupoidError("every relation requires exactly two trace half-edges")
        if self.boundary_rank != len(self.generators):
            raise OrderedReturnGroupoidError("subdivided bouquet boundary rank changed")
        if self.first_betti_rank != len(self.generators):
            raise OrderedReturnGroupoidError("ordered lift must preserve the declared relation rank")

    @property
    def relation_rank(self) -> int:
        return len(self.generators)

    @property
    def objects(self) -> tuple[str, ...]:
        return (self.base_object,) + tuple(item.midpoint_object for item in self.generators)

    def _edge(self, edge_id: str) -> OrientedEdge:
        edge = next((item for item in self.edges if item.edge_id == edge_id), None)
        if edge is None:
            raise OrderedReturnGroupoidError(f"unknown groupoid edge: {edge_id}")
        return edge

    def _generator(self, relation_id: str) -> ReturnLoopGenerator:
        generator = next((item for item in self.generators if item.relation_id == relation_id), None)
        if generator is None:
            raise OrderedReturnGroupoidError(f"unknown return generator: {relation_id}")
        return generator

    def symbol_for(self, relation_id: str) -> str:
        return self._generator(relation_id).symbol

    def make_path(self, source: str, steps: Sequence[PathStep]) -> GroupoidPath:
        if source not in self.objects:
            raise OrderedReturnGroupoidError("path source is not a groupoid object")
        current = source
        for step in steps:
            if not isinstance(step, PathStep):
                raise OrderedReturnGroupoidError("path steps must be PathStep entries")
            edge_source, edge_target = self._edge(step.edge_id).endpoints(step.orientation)
            if current != edge_source:
                raise OrderedReturnGroupoidError(
                    f"path endpoint mismatch: expected {current}, edge starts at {edge_source}"
                )
            current = edge_target
        return GroupoidPath(self.groupoid_digest, source, current, tuple(steps))

    def identity_path(self, object_id: str) -> GroupoidPath:
        return self.make_path(object_id, ())

    def compose_paths(self, *paths: GroupoidPath) -> GroupoidPath:
        if not paths:
            raise OrderedReturnGroupoidError("path composition requires at least one path")
        if any(path.groupoid_digest != self.groupoid_digest for path in paths):
            raise OrderedReturnGroupoidError("cannot compose paths from different groupoids")
        for left, right in zip(paths, paths[1:], strict=False):
            if left.target != right.source:
                raise OrderedReturnGroupoidError("path composition endpoint mismatch")
        return self.reduce_path(self.make_path(paths[0].source, tuple(
            step for path in paths for step in path.steps
        )))

    def inverse_path(self, path: GroupoidPath) -> GroupoidPath:
        if path.groupoid_digest != self.groupoid_digest:
            raise OrderedReturnGroupoidError("path belongs to another groupoid")
        return self.make_path(
            path.target,
            tuple(step.inverse() for step in reversed(path.steps)),
        )

    def reduce_path(self, path: GroupoidPath) -> GroupoidPath:
        if path.groupoid_digest != self.groupoid_digest:
            raise OrderedReturnGroupoidError("path belongs to another groupoid")
        stack: list[PathStep] = []
        for step in path.steps:
            if stack and stack[-1].edge_id == step.edge_id and stack[-1].orientation == -step.orientation:
                stack.pop()
            else:
                stack.append(step)
        reduced = self.make_path(path.source, tuple(stack))
        if reduced.target != path.target:
            raise OrderedReturnGroupoidError("free path reduction changed endpoint")
        return reduced

    def complete_loop_path(self, relation_id: str, exponent: int = 1) -> GroupoidPath:
        generator = self._generator(relation_id)
        if exponent == 1:
            steps = (PathStep(generator.outbound_edge_id), PathStep(generator.return_edge_id))
        elif exponent == -1:
            steps = (PathStep(generator.return_edge_id, -1), PathStep(generator.outbound_edge_id, -1))
        else:
            raise OrderedReturnGroupoidError("loop exponent must be plus or minus one")
        path = self.make_path(self.base_object, steps)
        if not path.is_loop:
            raise OrderedReturnGroupoidError("complete return did not close at positive basepoint")
        return path

    def shifted_loop_path(self, relation_id: str) -> GroupoidPath:
        generator = self._generator(relation_id)
        path = self.make_path(
            generator.midpoint_object,
            (PathStep(generator.return_edge_id), PathStep(generator.outbound_edge_id)),
        )
        if not path.is_loop:
            raise OrderedReturnGroupoidError("one-turn-shifted return did not close")
        return path

    def transported_shifted_loop_path(self, relation_id: str) -> GroupoidPath:
        generator = self._generator(relation_id)
        outbound = self.make_path(self.base_object, (PathStep(generator.outbound_edge_id),))
        shifted = self.shifted_loop_path(relation_id)
        return self.compose_paths(outbound, shifted, self.inverse_path(outbound))

    def word(self, letters: Iterable[WordLetter]) -> FreeReturnWord:
        reduced = _reduce_letters(letters)
        known = {item.relation_id for item in self.generators}
        if any(letter.relation_id not in known for letter in reduced):
            raise OrderedReturnGroupoidError("word contains a generator outside this retained basis")
        return FreeReturnWord(self.basis_digest, reduced)

    def word_from_ordinals(self, ordinals: Sequence[int]) -> FreeReturnWord:
        by_ordinal = {item.ordinal: item.relation_id for item in self.generators}
        try:
            letters = tuple(WordLetter(by_ordinal[abs(value)], 1 if value > 0 else -1) for value in ordinals)
        except (KeyError, TypeError):
            raise OrderedReturnGroupoidError("word ordinal is outside this retained basis") from None
        if any(isinstance(value, bool) or not isinstance(value, int) or value == 0 for value in ordinals):
            raise OrderedReturnGroupoidError("word ordinals must be nonzero integers")
        return self.word(letters)

    def word_path(self, word: FreeReturnWord) -> GroupoidPath:
        if word.basis_digest != self.basis_digest:
            raise OrderedReturnGroupoidError("word belongs to another retained basis")
        path = self.identity_path(self.base_object)
        for letter in word.letters:
            path = self.compose_paths(path, self.complete_loop_path(letter.relation_id, letter.exponent))
        return path

    def abelianize(self, word: FreeReturnWord) -> tuple[int, ...]:
        if word.basis_digest != self.basis_digest:
            raise OrderedReturnGroupoidError("word belongs to another retained basis")
        return tuple(
            sum(letter.exponent for letter in word.letters if letter.relation_id == generator.relation_id)
            for generator in self.generators
        )

    def word_symbols(self, word: FreeReturnWord) -> tuple[str, ...]:
        if word.basis_digest != self.basis_digest:
            raise OrderedReturnGroupoidError("word belongs to another retained basis")
        return tuple(
            self.symbol_for(letter.relation_id) + ("^-1" if letter.exponent == -1 else "")
            for letter in word.letters
        )

    def cyclic_key_symbols(self, word: FreeReturnWord) -> tuple[str, ...]:
        return tuple(
            self.symbol_for(letter.relation_id) + ("^-1" if letter.exponent == -1 else "")
            for letter in word.oriented_cyclic_key
        )

    def to_payload(self) -> dict[str, Any]:
        return {
            "standing": STANDING,
            "basis_digest": self.basis_digest,
            "groupoid_digest": self.groupoid_digest,
            "base_object": self.base_object,
            "final_atomic_id": self.final_atomic_id,
            "objects": list(self.objects),
            "generators": [item.to_payload() for item in self.generators],
            "edges": [item.to_payload() for item in self.edges],
            "graph": {
                "vertex_count": len(self.objects),
                "edge_count": len(self.edges),
                "connected_components": 1,
                "boundary_rank": self.boundary_rank,
                "filling_two_cell_count": 0,
                "first_betti_rank": self.first_betti_rank,
                "fundamental_group_candidate": f"F_{self.relation_rank}",
                "abelianization": f"Z^{self.relation_rank}",
            },
            "attachment_policy": {
                "positive_basepoint": "shared under the candidate basepoint-preserving recursive inclusion",
                "reversed_midpoints": "one distinct object per retained complete-return relation",
                "cross_generator_relators": [],
                "global_monodromy": None,
            },
        }


def _incidence_rank_for_subdivided_bouquet(rank: int) -> int:
    """Exact rank of the graph boundary map, checked by its tree columns."""

    if rank < 1:
        raise OrderedReturnGroupoidError("ordered groupoid rank must be positive")
    # One outbound edge per midpoint forms a spanning tree.  Its reduced
    # incidence matrix is the rank-by-rank identity up to sign.
    return rank


@lru_cache(maxsize=None)
def build_ordered_return_groupoid(rank: int = 4) -> OrderedReturnGroupoid:
    """Lift the unchanged retained relation basis to a subdivided bouquet."""

    if isinstance(rank, bool) or not isinstance(rank, int) or rank <= 0:
        raise OrderedReturnGroupoidError("rank must be a positive integer")
    generated = extension.iterate_complete_return(
        rank,
        scale_prefix="ordered-return-groupoid-scale",
    )
    final_state = generated[-1].output
    relation_ids = tuple(item.new_relation_id for item in generated)
    if final_state.relation_basis != relation_ids:
        raise OrderedReturnGroupoidError("retained relation order changed during groupoid lift")
    basis_digest = sha256(_canonical_bytes({
        "kind": "ordered-complete-return-free-basis",
        "final_atomic_id": final_state.atomic_id,
        "relation_ids": relation_ids,
    })).hexdigest()

    generators: list[ReturnLoopGenerator] = []
    edges: list[OrientedEdge] = []
    for ordinal, item in enumerate(generated, start=1):
        trace_sha256 = sha256(_canonical_bytes(item.trace.to_payload())).hexdigest()
        identity_payload = {
            "basis_digest": basis_digest,
            "ordinal": ordinal,
            "relation_id": item.new_relation_id,
            "trace_sha256": trace_sha256,
        }
        identity_digest = sha256(_canonical_bytes(identity_payload)).hexdigest()
        midpoint = f"return-groupoid.reversed-midpoint:{identity_digest}"
        outbound_id = f"return-groupoid.edge.outbound:{identity_digest}"
        return_id = f"return-groupoid.edge.return:{identity_digest}"
        generator = ReturnLoopGenerator(
            ordinal=ordinal,
            symbol=f"g{ordinal}",
            relation_id=item.new_relation_id,
            midpoint_object=midpoint,
            outbound_edge_id=outbound_id,
            return_edge_id=return_id,
            trace_sha256=trace_sha256,
            source_atomic_id=item.source.atomic_id,
            promoted_atomic_id=item.output.atomic_id,
        )
        generators.append(generator)
        edges.extend((
            OrientedEdge(
                edge_id=outbound_id,
                relation_id=item.new_relation_id,
                half="positive-to-reversed",
                source=POSITIVE_BASE_OBJECT,
                target=midpoint,
                trace_sha256=trace_sha256,
            ),
            OrientedEdge(
                edge_id=return_id,
                relation_id=item.new_relation_id,
                half="reversed-to-positive",
                source=midpoint,
                target=POSITIVE_BASE_OBJECT,
                trace_sha256=trace_sha256,
            ),
        ))

    boundary_rank = _incidence_rank_for_subdivided_bouquet(rank)
    first_betti_rank = len(edges) - (rank + 1) + 1
    groupoid_payload = {
        "operation": "minimal-subdivided-bouquet-lift-before-abelianization",
        "basis_digest": basis_digest,
        "base_object": POSITIVE_BASE_OBJECT,
        "generators": [item.to_payload() for item in generators],
        "edges": [item.to_payload() for item in edges],
        "boundary_rank": boundary_rank,
        "first_betti_rank": first_betti_rank,
    }
    return OrderedReturnGroupoid(
        basis_digest=basis_digest,
        groupoid_digest=sha256(_canonical_bytes(groupoid_payload)).hexdigest(),
        base_object=POSITIVE_BASE_OBJECT,
        final_atomic_id=final_state.atomic_id,
        generators=tuple(generators),
        edges=tuple(edges),
        boundary_rank=boundary_rank,
        first_betti_rank=first_betti_rank,
    )


@dataclass(frozen=True, slots=True)
class PermutationOrderProfile:
    """Exact based and oriented-cyclic counts for one positive basis traversal."""

    rank: int
    based_words: tuple[tuple[str, ...], ...]
    cyclic_classes: tuple[tuple[tuple[str, ...], ...], ...]
    abelianization_vectors: tuple[tuple[int, ...], ...]

    @property
    def based_word_count(self) -> int:
        return len(self.based_words)

    @property
    def oriented_cyclic_class_count(self) -> int:
        return len(self.cyclic_classes)

    @property
    def abelianization_class_count(self) -> int:
        return len(self.abelianization_vectors)

    def to_payload(self) -> dict[str, Any]:
        return {
            "rank": self.rank,
            "based_word_count": self.based_word_count,
            "expected_based_word_count": factorial(self.rank),
            "based_words": [list(word) for word in self.based_words],
            "oriented_cyclic_class_count": self.oriented_cyclic_class_count,
            "expected_oriented_cyclic_class_count": factorial(self.rank - 1),
            "oriented_cyclic_classes": [
                [list(word) for word in closure_class]
                for closure_class in self.cyclic_classes
            ],
            "abelianization_class_count": self.abelianization_class_count,
            "abelianization_vectors": [list(vector) for vector in self.abelianization_vectors],
        }


def permutation_order_profile(
    groupoid: OrderedReturnGroupoid,
    rank: int | None = None,
) -> PermutationOrderProfile:
    """Enumerate positive once-each traversals without quotienting too early."""

    if not isinstance(groupoid, OrderedReturnGroupoid):
        raise OrderedReturnGroupoidError("groupoid must be an OrderedReturnGroupoid")
    selected_rank = groupoid.relation_rank if rank is None else rank
    if (
        isinstance(selected_rank, bool)
        or not isinstance(selected_rank, int)
        or selected_rank <= 0
        or selected_rank > groupoid.relation_rank
    ):
        raise OrderedReturnGroupoidError("profile rank must select a nonempty basis prefix")
    selected = groupoid.generators[:selected_rank]
    words = tuple(
        groupoid.word(WordLetter(item.relation_id) for item in ordering)
        for ordering in permutations(selected)
    )
    based_words = tuple(groupoid.word_symbols(word) for word in words)
    if len(set(based_words)) != factorial(selected_rank):
        raise OrderedReturnGroupoidError("based permutation words collapsed before quotient")

    classes: dict[tuple[WordLetter, ...], list[tuple[str, ...]]] = {}
    for word in words:
        classes.setdefault(word.oriented_cyclic_key, []).append(groupoid.word_symbols(word))
    cyclic_classes = tuple(
        tuple(sorted(members))
        for _, members in sorted(classes.items(), key=lambda item: item[0])
    )
    vectors = tuple(sorted({groupoid.abelianize(word)[:selected_rank] for word in words}))
    profile = PermutationOrderProfile(
        rank=selected_rank,
        based_words=tuple(sorted(based_words)),
        cyclic_classes=cyclic_classes,
        abelianization_vectors=vectors,
    )
    if profile.oriented_cyclic_class_count != factorial(selected_rank - 1):
        raise OrderedReturnGroupoidError("oriented cyclic closure count changed")
    if profile.abelianization_class_count != 1:
        raise OrderedReturnGroupoidError("once-each words must share one abelianization")
    return profile


def _producer_code_reference() -> str:
    return "sha256:" + sha256(Path(__file__).read_bytes()).hexdigest()


@lru_cache(maxsize=1)
def receipt_payload() -> dict[str, Any]:
    root = _stack_root()
    groupoid = build_ordered_return_groupoid(4)
    first_relation = groupoid.generators[0].relation_id
    complete = groupoid.complete_loop_path(first_relation)
    shifted = groupoid.shifted_loop_path(first_relation)
    transported = groupoid.transported_shifted_loop_path(first_relation)
    triadic_words = {
        "g1_g2_g3": groupoid.word_from_ordinals((1, 2, 3)),
        "g2_g3_g1": groupoid.word_from_ordinals((2, 3, 1)),
        "g1_g3_g2": groupoid.word_from_ordinals((1, 3, 2)),
    }
    return {
        "schema_id": SCHEMA_ID,
        "schema_version": SCHEMA_VERSION,
        "standing": STANDING,
        "selection_effect": SELECTION_EFFECT,
        "producer_code_reference": _producer_code_reference(),
        "source": {
            "authority": "The-Interdependency/ucns",
            "ucns_commit": extension.PINNED_UCNS_COMMIT,
            "source_file_digests": [
                {"path": path, "sha256": digest}
                for path, digest in _source_file_digests(root)
            ],
            "complete_return_candidate_receipt_sha256": extension.receipt_digest(),
        },
        "candidate": {
            "operation": "minimal subdivided-bouquet path-groupoid lift before abelianization",
            "recursive_inclusion": "retain prior based loops unchanged at the promoted positive occurrence",
            "midpoint_policy": "one relation-specific reversed-frame object per complete-return loop",
            "word_reduction": "cancel adjacent inverse edge or generator pairs only; never commute",
            "closure_quotients": {
                "based": "no quotient",
                "unbased_oriented": "cyclic conjugacy only",
                "orientation_reversal": "not authorized",
            },
            "observed_successor_cardinality_input": None,
            "observed_arithmetic_factor_input": None,
            "desired_arithmetic_rank_input": None,
        },
        "groupoid": groupoid.to_payload(),
        "local_basepoint_witness": {
            "complete_loop": complete.to_payload(),
            "one_turn_shifted_loop": shifted.to_payload(),
            "based_paths_distinct": complete != shifted,
            "transported_shifted_loop_reduces_to_complete_loop": transported == complete,
        },
        "order_profiles": [
            permutation_order_profile(groupoid, rank).to_payload()
            for rank in range(1, groupoid.relation_rank + 1)
        ],
        "triadic_witness": {
            name: {
                "based_word": list(groupoid.word_symbols(word)),
                "oriented_cyclic_key": list(groupoid.cyclic_key_symbols(word)),
                "abelianization": list(groupoid.abelianize(word)),
            }
            for name, word in triadic_words.items()
        },
        "current_global_monodromy": None,
        "current_cross_generator_relators": [],
        "current_arithmetic_factor_map": None,
        "numerical_next_gonol": None,
        "nonclaims": list(NONCLAIMS),
        "falsification_conditions": list(FALSIFICATION_CONDITIONS),
        "promotion_evidence": list(PROMOTION_EVIDENCE),
        "hmmm": list(HMMM),
    }


def receipt_bytes() -> bytes:
    return _canonical_bytes(receipt_payload())


def receipt_digest() -> str:
    return sha256(receipt_bytes()).hexdigest()


def main() -> None:
    payload = receipt_payload()
    payload["receipt_sha256"] = receipt_digest()
    print(json.dumps(payload, ensure_ascii=True, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
