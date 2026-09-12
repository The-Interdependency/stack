"""Noncommutative invariant audit for ordered complete-return words.

This module consumes the target-free ordered path-groupoid lift.  It computes
Fox derivatives in the integral group ring and a degree-two noncommutative
Magnus expansion before any abelian projection.  These exact fingerprints
preserve traversal order, but they are not relators and do not by themselves
define a finite presentation or arithmetic cardinality.

The audit therefore stops before determinant or factor comparison when the
geometry supplies no cross-generator attaching words or global monodromy.
"""

# === MODULE_BUILD ===
# id: ucns_ordered_return_invariant_audit
#   module_name: ordered_return_invariant_audit
#   module_kind: experiment
#   summary: derives exact noncommutative Fox and Magnus fingerprints for ordered complete-return words, proves homology underdetermines monodromy, and gates arithmetic readout on missing geometry-derived relators
#   owner: The Interdependency
#   public_surface: OrderedReturnInvariantError, AuthorityGapEvidence, GroupRingElement, MagnusExpansion, OrderedWordInvariant, AutomorphismWitness, OrderedInvariantAudit, authority_gap_evidence, fox_derivative, fox_fundamental_identity_holds, magnus_expansion, ordered_word_invariant, substitute_word, monodromy_witnesses, audit, receipt_payload, receipt_bytes, receipt_digest
#   internal_surface: _stack_root, _canonical_bytes, _file_digest, _source_file_digests, _ring_from_mapping, _word_ring_element, _magnus_from_mapping, _identity_images, _automorphism_witness, _producer_code_reference, main
#   auth_boundary: none; consumes the frozen stack-local ordered return groupoid and read-only canonical UCNS word-before-abelianization precedent
#   storage_boundary: read-only at runtime
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: research/ucns/tests/test_ordered_return_invariant_audit.py
#   rollout: stack-local invariant and obstruction research only; no UCNS canon, stack libs, PCEA, arithmetic-factor, or successor-cardinality promotion
#   rollback: remove this module, its tests, report, and receipt
#   requires: ucns_ordered_complete_return_groupoid, ucns_prime_exact_milnor_alexander_p7_p5, ucns_prime_symbolic_alexander_p7_p5, gonol-build construction discipline
#   since: 2026-09-02
#   unresolved: geometry-selected traversal words; cross-generator Wirtinger or attaching relators; based global monodromy; representation or specialization of a Fox presentation; canonical finite integer invariant; arithmetic factor bridge; numerical next gonol
# === END MODULE_BUILD ===

# === CONTRACTS ===
# id: ordered_return_fox_derivative_is_exact
#   given: a freely reduced ordered return word is differentiated in the integral group ring
#   then: the noncommutative Fox product rule is exact and the fundamental identity sums to the word minus one
#   class: correctness
#   since: 2026-09-02
#
# id: ordered_return_magnus_preserves_order
#   given: differently ordered once-each return words are expanded through degree two
#   then: their noncommutative coefficients remain distinct while degree-one coefficients equal the explicit abelianization
#   class: correctness
#   since: 2026-09-02
#
# id: ordered_return_invariants_distinguish_triadic_words
#   given: all six positive permutations of three retained generators are evaluated
#   then: both exact Fox and degree-two Magnus fingerprints distinguish all six based words before cyclic or abelian quotient
#   class: evidence
#   since: 2026-09-02
#
# id: ordered_return_homology_underdetermines_monodromy
#   given: free groups of ranks two and three project to their first homology
#   then: executable nonidentity automorphisms replay with identity abelianization, including a triadic commutator shear invisible to H1
#   class: evidence
#   since: 2026-09-02
#
# id: ordered_return_authority_gap_is_provenance_bound
#   given: pinned UCNS and stack-local mechanics are inspected for ordered recursive geometry
#   then: exact source identities distinguish carrier order, caller-supplied coupling order, and unrelated seed event order from the still-missing geometry-selected traversal, attachment, and monodromy
#   class: evidence
#   since: 2026-09-02
#
# id: ordered_return_presentation_gate_fails_closed
#   given: current recursive return geometry has generators but no cross-generator attaching relators, crossings, or global monodromy
#   then: no Fox presentation determinant, finite integer invariant, arithmetic factorization, observation comparison, or numerical successor is emitted
#   class: safety
#   since: 2026-09-02
#
# id: ordered_return_invariant_audit_is_target_free
#   given: invariant derivation is inspected before the absent observation gate
#   then: no observed gonol cardinality or prime defines a word, derivative, expansion, automorphism witness, or presentation entry
#   class: doctrine
#   since: 2026-09-02
#
# id: ordered_return_invariant_receipt_replays
#   given: the frozen ordered groupoid and canonical source identities are unchanged
#   then: canonical audit receipt bytes and digest replay byte-identically
#   class: evidence
#   since: 2026-09-02
# === END CONTRACTS ===

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from hashlib import sha256
from itertools import permutations
import json
from pathlib import Path
from typing import Any, Iterable, Mapping

import ordered_complete_return_groupoid as groupoid_module


SCHEMA_ID = "the-interdependency.stack-research.ucns.ordered-return-invariant-audit"
SCHEMA_VERSION = "0.1.0"
STANDING = "stack-local-target-free-noncommutative-invariant-audit"
SELECTION_EFFECT = "none"
STATUS = "ORDERED_LAYER_EXECUTABLE__MONODROMY_PRESENTATION_AND_FACTOR_BRIDGE_UNRESOLVED"

NONCLAIMS: tuple[str, ...] = (
    "not UCNS canon",
    "not evidence that an arbitrary traversal word is selected by recursive gonol geometry",
    "not a Wirtinger presentation for the recursive gonol",
    "not permission to take a determinant before geometry supplies relators and a specialization",
    "not an arithmetic factor or successor-cardinality operation",
    "not a numerical next-gonol prediction",
    "not PCEA key, entropy, hardness, replay-resistance, recovery, or public-authenticity evidence",
)

HMMM: tuple[str, ...] = (
    "the ordered groupoid can represent every based word, but current UCNS recursive geometry does not select which cross-generator traversal words actually occur",
    "Fox derivatives of a traversal word are order-sensitive fingerprints, not a presentation matrix unless geometry declares the word to be a relator",
    "degree-two Magnus coefficients preserve pairwise ordering but provide no canonical finite cardinality",
    "identity action on H1 does not determine free-group monodromy; at rank three a commutator shear is already invisible to abelianization",
    "current recursive return geometry has no cross-generator crossing, linking, intersection, or attaching-word ledger",
    "without frozen relators and a geometry-derived representation or specialization, there is no determinant or factorization gate to compare with observations",
    "numerical next gonol remains unresolved",
)

FALSIFICATION_CONDITIONS: tuple[str, ...] = (
    "Fox differentiation violates the exact group-ring fundamental identity",
    "Magnus degree-one coefficients differ from the word exponent sums",
    "two distinct triadic based permutations receive the same degree-two ordered fingerprint",
    "homology is treated as if it uniquely determined a free-group monodromy",
    "a traversal word is silently imposed as a relator without geometric closure evidence",
    "a determinant, factorization, or observed-prime comparison is emitted while the presentation or specialization is absent",
    "an observed gonol value or factor enters noncommutative invariant derivation",
)

PROMOTION_EVIDENCE: tuple[str, ...] = (
    "derive exact cross-generator traversal and closure words from recursive UCNS geometry",
    "derive a based monodromy automorphism on every retained free-group generator",
    "derive projection crossings, intersection numbers, or attaching maps with replayable provenance",
    "freeze the resulting noncommutative presentation before choosing any representation or abelian specialization",
    "freeze a canonical integer readout before opening the observation comparison gate",
)


class OrderedReturnInvariantError(ValueError):
    """Raised when a noncommutative invariant crosses an undeclared boundary."""


WordKey = tuple[groupoid_module.WordLetter, ...]
Monomial = tuple[str, ...]


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
            "libs/ucns/src/ucns/prime_exact_milnor_alexander.py",
            "libs/ucns/src/ucns/prime_symbolic_alexander.py",
            "libs/ucns/src/ucns/public_gonol.py",
            "libs/ucns/src/ucns/direct_mobius.py",
            "libs/ucns/src/ucns/mobius_seed.py",
            "research/ucns/public_gonol_functional_operations.py",
            "research/ucns/affinization_coupling_geometry.py",
            "research/ucns/recursive_scale_transition.py",
            "research/ucns/ordered_complete_return_groupoid.py",
            "research/ucns/receipts/ordered-complete-return-groupoid-v0.json",
        )
    )


@dataclass(frozen=True, slots=True)
class AuthorityGapEvidence:
    """One provenance-bound distinction between existing and required order."""

    surface: str
    source_path: str
    source_sha256: str
    existing_ordered_data: str
    missing_recursive_geometry: str
    required_source_marker: str

    def to_payload(self) -> dict[str, str]:
        return {
            "surface": self.surface,
            "source_path": self.source_path,
            "source_sha256": self.source_sha256,
            "existing_ordered_data": self.existing_ordered_data,
            "missing_recursive_geometry": self.missing_recursive_geometry,
            "required_source_marker": self.required_source_marker,
        }


@lru_cache(maxsize=1)
def authority_gap_evidence() -> tuple[AuthorityGapEvidence, ...]:
    """Fail closed unless every claimed authority boundary remains explicit."""

    root = _stack_root()
    declarations = (
        (
            "canonical Public Gonol carrier",
            "libs/ucns/src/ucns/public_gonol.py",
            "exact position and glyph order",
            "position-specific geometric operations and traversal words",
            "unresolved: the exact geometric operation expressed by each function position beyond its carrier identity",
        ),
        (
            "canonical native Mobius return",
            "libs/ucns/src/ucns/direct_mobius.py",
            "exact positive/reversed frame sequence under local turns",
            "attachment to higher geometry and action on retained inner loops",
            "unresolved: attachment to higher-dimensional circle, epicycle, disk, sphere, and full gonol constructions",
        ),
        (
            "stack-local Public Gonol operations",
            "research/ucns/public_gonol_functional_operations.py",
            "identity and candidate cyclic carrier permutations",
            "canonical position operation and recursive traversal selection",
            "the exact operation expressed by each Public Gonol function position remains unresolved",
        ),
        (
            "stack-local affinization coupling",
            "research/ucns/affinization_coupling_geometry.py",
            "slot-sensitive order supplied explicitly by the caller",
            "coordinate or topological coupling that derives participant order",
            "exact coordinate embedding of coupling on the UCNS carrier remains unresolved",
        ),
        (
            "stack-local recursive promotion",
            "research/ucns/recursive_scale_transition.py",
            "recoverable constituent order inside a digest-bound promoted atom",
            "next-scale placement and free-group transport or monodromy",
            "exact next-scale carrier placement remains unresolved",
        ),
        (
            "canonical Mobius seed candidate",
            "libs/ucns/src/ucns/mobius_seed.py",
            "exact band event turns, projection incidences, and over-under changes",
            "authorized map from seed events to Public Gonol recursive relation words",
            "the canonical UCNS seven-gonol composition and option-registry standing remain separate decisions",
        ),
    )
    evidence: list[AuthorityGapEvidence] = []
    for surface, relative_path, existing, missing, marker in declarations:
        path = root / relative_path
        source = path.read_text(encoding="utf-8")
        if marker not in source:
            raise OrderedReturnInvariantError(
                f"authority boundary marker changed for {surface}: {relative_path}"
            )
        evidence.append(AuthorityGapEvidence(
            surface=surface,
            source_path=relative_path,
            source_sha256=sha256(path.read_bytes()).hexdigest(),
            existing_ordered_data=existing,
            missing_recursive_geometry=missing,
            required_source_marker=marker,
        ))
    return tuple(evidence)


@dataclass(frozen=True, slots=True)
class GroupRingElement:
    """Sparse exact element of the integral group ring of a free group."""

    basis_digest: str
    terms: tuple[tuple[WordKey, int], ...]

    def __post_init__(self) -> None:
        if not isinstance(self.basis_digest, str) or not self.basis_digest:
            raise OrderedReturnInvariantError("group-ring basis digest is required")
        keys: list[WordKey] = []
        for key, coefficient in self.terms:
            if key != groupoid_module._reduce_letters(key):
                raise OrderedReturnInvariantError("group-ring word keys must be freely reduced")
            if isinstance(coefficient, bool) or not isinstance(coefficient, int) or coefficient == 0:
                raise OrderedReturnInvariantError("group-ring coefficients must be nonzero integers")
            keys.append(key)
        if len(set(keys)) != len(keys):
            raise OrderedReturnInvariantError("group-ring terms must have unique word keys")
        if tuple(sorted(self.terms, key=lambda item: item[0])) != self.terms:
            raise OrderedReturnInvariantError("group-ring terms must be canonically ordered")

    @property
    def is_zero(self) -> bool:
        return not self.terms

    def _mapping(self) -> dict[WordKey, int]:
        return dict(self.terms)

    def add(self, other: "GroupRingElement") -> "GroupRingElement":
        if self.basis_digest != other.basis_digest:
            raise OrderedReturnInvariantError("group-ring bases differ")
        values = self._mapping()
        for key, coefficient in other.terms:
            values[key] = values.get(key, 0) + coefficient
        return _ring_from_mapping(self.basis_digest, values)

    def negate(self) -> "GroupRingElement":
        return _ring_from_mapping(
            self.basis_digest,
            {key: -coefficient for key, coefficient in self.terms},
        )

    def subtract(self, other: "GroupRingElement") -> "GroupRingElement":
        return self.add(other.negate())

    def multiply(self, other: "GroupRingElement") -> "GroupRingElement":
        if self.basis_digest != other.basis_digest:
            raise OrderedReturnInvariantError("group-ring bases differ")
        values: dict[WordKey, int] = {}
        for left_key, left_coefficient in self.terms:
            for right_key, right_coefficient in other.terms:
                key = groupoid_module._reduce_letters(left_key + right_key)
                values[key] = values.get(key, 0) + left_coefficient * right_coefficient
        return _ring_from_mapping(self.basis_digest, values)

    def to_payload(
        self,
        groupoid: groupoid_module.OrderedReturnGroupoid,
    ) -> list[dict[str, Any]]:
        if self.basis_digest != groupoid.basis_digest:
            raise OrderedReturnInvariantError("group-ring element belongs to another groupoid")
        return [
            {
                "coefficient": coefficient,
                "word": [
                    groupoid.symbol_for(letter.relation_id)
                    + ("^-1" if letter.exponent == -1 else "")
                    for letter in key
                ],
            }
            for key, coefficient in self.terms
        ]


def _ring_from_mapping(
    basis_digest: str,
    values: Mapping[WordKey, int],
) -> GroupRingElement:
    combined: dict[WordKey, int] = {}
    for key, coefficient in values.items():
        if isinstance(coefficient, bool) or not isinstance(coefficient, int):
            raise OrderedReturnInvariantError("group-ring coefficients must be integers")
        reduced_key = groupoid_module._reduce_letters(key)
        combined[reduced_key] = combined.get(reduced_key, 0) + coefficient
    return GroupRingElement(
        basis_digest,
        tuple(sorted(
            ((key, coefficient) for key, coefficient in combined.items() if coefficient),
            key=lambda item: item[0],
        )),
    )


def _word_ring_element(word: groupoid_module.FreeReturnWord) -> GroupRingElement:
    return _ring_from_mapping(word.basis_digest, {word.letters: 1})


def _ring_one(basis_digest: str) -> GroupRingElement:
    return _ring_from_mapping(basis_digest, {(): 1})


def _ring_zero(basis_digest: str) -> GroupRingElement:
    return _ring_from_mapping(basis_digest, {})


def fox_derivative(
    groupoid: groupoid_module.OrderedReturnGroupoid,
    word: groupoid_module.FreeReturnWord,
    relation_id: str,
) -> GroupRingElement:
    """Return the exact left Fox derivative in ``Z[F_r]``."""

    if word.basis_digest != groupoid.basis_digest:
        raise OrderedReturnInvariantError("word belongs to another groupoid")
    if relation_id not in {item.relation_id for item in groupoid.generators}:
        raise OrderedReturnInvariantError("Fox derivative generator is outside the basis")
    derivative = _ring_zero(groupoid.basis_digest)
    prefix: WordKey = ()
    for letter in word.letters:
        if letter.exponent == 1:
            if letter.relation_id == relation_id:
                derivative = derivative.add(_ring_from_mapping(groupoid.basis_digest, {prefix: 1}))
            prefix = groupoid_module._reduce_letters(prefix + (letter,))
        else:
            prefix_with_inverse = groupoid_module._reduce_letters(prefix + (letter,))
            if letter.relation_id == relation_id:
                derivative = derivative.add(
                    _ring_from_mapping(groupoid.basis_digest, {prefix_with_inverse: -1})
                )
            prefix = prefix_with_inverse
    return derivative


def fox_fundamental_identity_holds(
    groupoid: groupoid_module.OrderedReturnGroupoid,
    word: groupoid_module.FreeReturnWord,
) -> bool:
    """Check ``sum d_i(w)(g_i-1) = w-1`` exactly in ``Z[F_r]``."""

    one = _ring_one(groupoid.basis_digest)
    left = _ring_zero(groupoid.basis_digest)
    for generator in groupoid.generators:
        generator_word = groupoid.word((groupoid_module.WordLetter(generator.relation_id),))
        generator_minus_one = _word_ring_element(generator_word).subtract(one)
        left = left.add(
            fox_derivative(groupoid, word, generator.relation_id).multiply(generator_minus_one)
        )
    right = _word_ring_element(word).subtract(one)
    return left == right


@dataclass(frozen=True, slots=True)
class MagnusExpansion:
    """Sparse noncommutative Magnus series truncated at a declared degree."""

    basis_digest: str
    max_degree: int
    terms: tuple[tuple[Monomial, int], ...]

    def __post_init__(self) -> None:
        if not isinstance(self.basis_digest, str) or not self.basis_digest:
            raise OrderedReturnInvariantError("Magnus basis digest is required")
        if isinstance(self.max_degree, bool) or not isinstance(self.max_degree, int) or self.max_degree < 1:
            raise OrderedReturnInvariantError("Magnus degree must be a positive integer")
        monomials: list[Monomial] = []
        for monomial, coefficient in self.terms:
            if len(monomial) > self.max_degree:
                raise OrderedReturnInvariantError("Magnus term exceeds truncation degree")
            if isinstance(coefficient, bool) or not isinstance(coefficient, int) or coefficient == 0:
                raise OrderedReturnInvariantError("Magnus coefficients must be nonzero integers")
            monomials.append(monomial)
        if len(set(monomials)) != len(monomials):
            raise OrderedReturnInvariantError("Magnus terms must be unique")
        if tuple(sorted(self.terms, key=lambda item: item[0])) != self.terms:
            raise OrderedReturnInvariantError("Magnus terms must be canonically ordered")

    def multiply(self, other: "MagnusExpansion") -> "MagnusExpansion":
        if self.basis_digest != other.basis_digest or self.max_degree != other.max_degree:
            raise OrderedReturnInvariantError("Magnus expansion boundaries differ")
        values: dict[Monomial, int] = {}
        for left_word, left_coefficient in self.terms:
            for right_word, right_coefficient in other.terms:
                monomial = left_word + right_word
                if len(monomial) <= self.max_degree:
                    values[monomial] = values.get(monomial, 0) + left_coefficient * right_coefficient
        return _magnus_from_mapping(self.basis_digest, self.max_degree, values)

    def coefficient(self, monomial: Iterable[str]) -> int:
        return dict(self.terms).get(tuple(monomial), 0)

    def to_payload(
        self,
        groupoid: groupoid_module.OrderedReturnGroupoid,
    ) -> list[dict[str, Any]]:
        if self.basis_digest != groupoid.basis_digest:
            raise OrderedReturnInvariantError("Magnus expansion belongs to another groupoid")
        return [
            {
                "coefficient": coefficient,
                "monomial": [groupoid.symbol_for(relation_id) for relation_id in monomial],
            }
            for monomial, coefficient in self.terms
        ]


def _magnus_from_mapping(
    basis_digest: str,
    max_degree: int,
    values: Mapping[Monomial, int],
) -> MagnusExpansion:
    combined: dict[Monomial, int] = {}
    for monomial, coefficient in values.items():
        if len(monomial) > max_degree:
            continue
        if isinstance(coefficient, bool) or not isinstance(coefficient, int):
            raise OrderedReturnInvariantError("Magnus coefficients must be integers")
        combined[tuple(monomial)] = combined.get(tuple(monomial), 0) + coefficient
    return MagnusExpansion(
        basis_digest,
        max_degree,
        tuple(sorted(
            ((monomial, coefficient) for monomial, coefficient in combined.items() if coefficient),
            key=lambda item: item[0],
        )),
    )


def magnus_expansion(
    groupoid: groupoid_module.OrderedReturnGroupoid,
    word: groupoid_module.FreeReturnWord,
    *,
    max_degree: int = 2,
) -> MagnusExpansion:
    """Expand a free word under ``g_i -> 1 + X_i`` without commuting."""

    if word.basis_digest != groupoid.basis_digest:
        raise OrderedReturnInvariantError("word belongs to another groupoid")
    if isinstance(max_degree, bool) or not isinstance(max_degree, int) or max_degree < 1:
        raise OrderedReturnInvariantError("Magnus degree must be a positive integer")
    known = {item.relation_id for item in groupoid.generators}
    result = _magnus_from_mapping(groupoid.basis_digest, max_degree, {(): 1})
    for letter in word.letters:
        if letter.relation_id not in known:
            raise OrderedReturnInvariantError("Magnus generator is outside the basis")
        if letter.exponent == 1:
            factor = _magnus_from_mapping(
                groupoid.basis_digest,
                max_degree,
                {(): 1, (letter.relation_id,): 1},
            )
        else:
            factor = _magnus_from_mapping(
                groupoid.basis_digest,
                max_degree,
                {
                    (letter.relation_id,) * degree: (-1) ** degree
                    for degree in range(max_degree + 1)
                },
            )
        result = result.multiply(factor)
    return result


@dataclass(frozen=True, slots=True)
class OrderedWordInvariant:
    """Exact order-sensitive witnesses for one based return word."""

    word: groupoid_module.FreeReturnWord
    abelianization: tuple[int, ...]
    fox_derivatives: tuple[GroupRingElement, ...]
    fox_fundamental_identity: bool
    magnus: MagnusExpansion
    fox_fingerprint_sha256: str
    magnus_fingerprint_sha256: str

    def to_payload(
        self,
        groupoid: groupoid_module.OrderedReturnGroupoid,
    ) -> dict[str, Any]:
        return {
            "based_word": list(groupoid.word_symbols(self.word)),
            "oriented_cyclic_key": list(groupoid.cyclic_key_symbols(self.word)),
            "abelianization": list(self.abelianization),
            "fox_derivatives": {
                generator.symbol: derivative.to_payload(groupoid)
                for generator, derivative in zip(groupoid.generators, self.fox_derivatives, strict=True)
            },
            "fox_fundamental_identity": self.fox_fundamental_identity,
            "fox_fingerprint_sha256": self.fox_fingerprint_sha256,
            "magnus_degree": self.magnus.max_degree,
            "magnus_terms": self.magnus.to_payload(groupoid),
            "magnus_fingerprint_sha256": self.magnus_fingerprint_sha256,
        }


def ordered_word_invariant(
    groupoid: groupoid_module.OrderedReturnGroupoid,
    word: groupoid_module.FreeReturnWord,
) -> OrderedWordInvariant:
    """Compute exact Fox and degree-two Magnus fingerprints before H1."""

    derivatives = tuple(
        fox_derivative(groupoid, word, generator.relation_id)
        for generator in groupoid.generators
    )
    fox_payload = [derivative.to_payload(groupoid) for derivative in derivatives]
    magnus = magnus_expansion(groupoid, word, max_degree=2)
    magnus_payload = magnus.to_payload(groupoid)
    identity_holds = fox_fundamental_identity_holds(groupoid, word)
    if not identity_holds:
        raise OrderedReturnInvariantError("Fox fundamental identity failed")
    abelianization = groupoid.abelianize(word)
    degree_one = tuple(
        magnus.coefficient((generator.relation_id,))
        for generator in groupoid.generators
    )
    if degree_one != abelianization:
        raise OrderedReturnInvariantError("Magnus degree one no longer equals abelianization")
    return OrderedWordInvariant(
        word=word,
        abelianization=abelianization,
        fox_derivatives=derivatives,
        fox_fundamental_identity=identity_holds,
        magnus=magnus,
        fox_fingerprint_sha256=sha256(_canonical_bytes(fox_payload)).hexdigest(),
        magnus_fingerprint_sha256=sha256(_canonical_bytes(magnus_payload)).hexdigest(),
    )


def substitute_word(
    groupoid: groupoid_module.OrderedReturnGroupoid,
    word: groupoid_module.FreeReturnWord,
    images: Mapping[str, groupoid_module.FreeReturnWord],
) -> groupoid_module.FreeReturnWord:
    """Apply one exact free-group substitution to a based word."""

    relation_ids = {item.relation_id for item in groupoid.generators}
    if set(images) != relation_ids:
        raise OrderedReturnInvariantError("substitution must define every basis generator")
    result = groupoid.word(())
    for letter in word.letters:
        image = images[letter.relation_id]
        if image.basis_digest != groupoid.basis_digest:
            raise OrderedReturnInvariantError("substitution image belongs to another basis")
        result = result.multiply(image if letter.exponent == 1 else image.inverse())
    return result


def _identity_images(
    groupoid: groupoid_module.OrderedReturnGroupoid,
) -> dict[str, groupoid_module.FreeReturnWord]:
    return {
        item.relation_id: groupoid.word((groupoid_module.WordLetter(item.relation_id),))
        for item in groupoid.generators
    }


@dataclass(frozen=True, slots=True)
class AutomorphismWitness:
    """One nonidentity free-group action hidden by first homology."""

    witness_id: str
    rank: int
    interpretation: str
    images: tuple[groupoid_module.FreeReturnWord, ...]
    inverse_images: tuple[groupoid_module.FreeReturnWord, ...]
    abelianization_matrix: tuple[tuple[int, ...], ...]
    inverse_replay: bool
    nonidentity_before_abelianization: bool

    def to_payload(
        self,
        groupoid: groupoid_module.OrderedReturnGroupoid,
    ) -> dict[str, Any]:
        return {
            "witness_id": self.witness_id,
            "rank": self.rank,
            "interpretation": self.interpretation,
            "images": {
                generator.symbol: list(groupoid.word_symbols(image))
                for generator, image in zip(groupoid.generators, self.images, strict=True)
            },
            "inverse_images": {
                generator.symbol: list(groupoid.word_symbols(image))
                for generator, image in zip(groupoid.generators, self.inverse_images, strict=True)
            },
            "abelianization_matrix": [list(row) for row in self.abelianization_matrix],
            "same_as_identity_on_h1": self.abelianization_matrix == tuple(
                tuple(1 if row == column else 0 for column in range(self.rank))
                for row in range(self.rank)
            ),
            "inverse_replay": self.inverse_replay,
            "nonidentity_before_abelianization": self.nonidentity_before_abelianization,
        }


def _automorphism_witness(
    groupoid: groupoid_module.OrderedReturnGroupoid,
    *,
    witness_id: str,
    interpretation: str,
    images: Mapping[str, groupoid_module.FreeReturnWord],
    inverse_images: Mapping[str, groupoid_module.FreeReturnWord],
) -> AutomorphismWitness:
    identity = _identity_images(groupoid)
    relation_ids = tuple(item.relation_id for item in groupoid.generators)
    if set(images) != set(relation_ids) or set(inverse_images) != set(relation_ids):
        raise OrderedReturnInvariantError("automorphism witness must cover the entire basis")
    inverse_replay = all(
        substitute_word(groupoid, images[relation_id], inverse_images) == identity[relation_id]
        and substitute_word(groupoid, inverse_images[relation_id], images) == identity[relation_id]
        for relation_id in relation_ids
    )
    matrix = tuple(groupoid.abelianize(images[relation_id]) for relation_id in relation_ids)
    nonidentity = any(images[relation_id] != identity[relation_id] for relation_id in relation_ids)
    if not inverse_replay or not nonidentity:
        raise OrderedReturnInvariantError("automorphism witness failed exact replay")
    return AutomorphismWitness(
        witness_id=witness_id,
        rank=groupoid.relation_rank,
        interpretation=interpretation,
        images=tuple(images[relation_id] for relation_id in relation_ids),
        inverse_images=tuple(inverse_images[relation_id] for relation_id in relation_ids),
        abelianization_matrix=matrix,
        inverse_replay=inverse_replay,
        nonidentity_before_abelianization=nonidentity,
    )


@lru_cache(maxsize=1)
def monodromy_witnesses() -> tuple[AutomorphismWitness, ...]:
    """Exhibit distinct based actions that first homology cannot select."""

    rank_two = groupoid_module.build_ordered_return_groupoid(2)
    x2, y2 = (item.relation_id for item in rank_two.generators)
    identity_two = _identity_images(rank_two)
    inner_images = dict(identity_two)
    inner_images[x2] = rank_two.word_from_ordinals((2, 1, -2))
    inner_inverse = dict(identity_two)
    inner_inverse[x2] = rank_two.word_from_ordinals((-2, 1, 2))
    rank_two_witness = _automorphism_witness(
        rank_two,
        witness_id="rank-two-inner-basepoint-transport",
        interpretation="a based inner conjugation; it may become a basepoint change in an outer-monodromy quotient",
        images=inner_images,
        inverse_images=inner_inverse,
    )

    rank_three = groupoid_module.build_ordered_return_groupoid(3)
    x3, y3, z3 = (item.relation_id for item in rank_three.generators)
    identity_three = _identity_images(rank_three)
    shear_images = dict(identity_three)
    shear_images[x3] = rank_three.word_from_ordinals((1, 2, 3, -2, -3))
    shear_inverse = dict(identity_three)
    shear_inverse[x3] = rank_three.word_from_ordinals((1, 3, 2, -3, -2))
    rank_three_witness = _automorphism_witness(
        rank_three,
        witness_id="rank-three-commutator-ia-shear",
        interpretation="x maps to x[y,z] while y and z remain fixed; the commutator is erased by H1",
        images=shear_images,
        inverse_images=shear_inverse,
    )
    return rank_two_witness, rank_three_witness


@dataclass(frozen=True, slots=True)
class OrderedInvariantAudit:
    """Bounded result of the noncommutative layer and presentation gate."""

    status: str
    groupoid: groupoid_module.OrderedReturnGroupoid
    triadic_invariants: tuple[OrderedWordInvariant, ...]
    fox_fingerprint_count: int
    magnus_fingerprint_count: int
    monodromy_witnesses: tuple[AutomorphismWitness, ...]
    authority_gaps: tuple[AuthorityGapEvidence, ...]
    current_relators: tuple[groupoid_module.FreeReturnWord, ...]
    current_global_monodromy: None
    current_integer_presentation: None
    current_canonical_integer_invariant: None
    current_factorization: None
    observation_comparison: None
    numerical_next_gonol: None

    def to_payload(self) -> dict[str, Any]:
        return {
            "status": self.status,
            "ordered_groupoid": {
                "basis_digest": self.groupoid.basis_digest,
                "groupoid_digest": self.groupoid.groupoid_digest,
                "rank": self.groupoid.relation_rank,
                "fundamental_group_candidate": f"F_{self.groupoid.relation_rank}",
                "abelianization": f"Z^{self.groupoid.relation_rank}",
            },
            "triadic_order_audit": {
                "based_permutation_count": len(self.triadic_invariants),
                "fox_fingerprint_count": self.fox_fingerprint_count,
                "magnus_degree_two_fingerprint_count": self.magnus_fingerprint_count,
                "abelianization_vector_count": len({
                    item.abelianization for item in self.triadic_invariants
                }),
                "words": [item.to_payload(self.groupoid) for item in self.triadic_invariants],
            },
            "homology_monodromy_obstruction": [
                witness.to_payload(groupoid_module.build_ordered_return_groupoid(witness.rank))
                for witness in self.monodromy_witnesses
            ],
            "authority_surface_audit": [
                item.to_payload() for item in self.authority_gaps
            ],
            "presentation_gate": {
                "generators": [item.symbol for item in self.groupoid.generators],
                "geometry_derived_relators": [
                    list(self.groupoid.word_symbols(word)) for word in self.current_relators
                ],
                "relator_count": len(self.current_relators),
                "current_group": f"free-group candidate F_{self.groupoid.relation_rank}",
                "current_global_monodromy": self.current_global_monodromy,
                "cross_generator_crossings": None,
                "cross_generator_linking_or_intersection_data": None,
                "fox_presentation_matrix": self.current_integer_presentation,
                "canonical_integer_invariant": self.current_canonical_integer_invariant,
                "factorization": self.current_factorization,
                "observation_comparison": self.observation_comparison,
                "gate_result": "NOT_REACHED_MISSING_GEOMETRY_DERIVED_RELATORS_AND_MONODROMY",
            },
            "numerical_next_gonol": self.numerical_next_gonol,
        }


@lru_cache(maxsize=1)
def audit() -> OrderedInvariantAudit:
    """Run the ordered layer and stop at the missing presentation boundary."""

    groupoid = groupoid_module.build_ordered_return_groupoid(4)
    selected = groupoid.generators[:3]
    words = tuple(
        groupoid.word(groupoid_module.WordLetter(item.relation_id) for item in ordering)
        for ordering in permutations(selected)
    )
    invariants = tuple(ordered_word_invariant(groupoid, word) for word in words)
    fox_count = len({item.fox_fingerprint_sha256 for item in invariants})
    magnus_count = len({item.magnus_fingerprint_sha256 for item in invariants})
    if fox_count != len(words) or magnus_count != len(words):
        raise OrderedReturnInvariantError("noncommutative triadic fingerprints collapsed")
    if len({item.abelianization for item in invariants}) != 1:
        raise OrderedReturnInvariantError("triadic abelianization control changed")
    return OrderedInvariantAudit(
        status=STATUS,
        groupoid=groupoid,
        triadic_invariants=invariants,
        fox_fingerprint_count=fox_count,
        magnus_fingerprint_count=magnus_count,
        monodromy_witnesses=monodromy_witnesses(),
        authority_gaps=authority_gap_evidence(),
        current_relators=(),
        current_global_monodromy=None,
        current_integer_presentation=None,
        current_canonical_integer_invariant=None,
        current_factorization=None,
        observation_comparison=None,
        numerical_next_gonol=None,
    )


def _producer_code_reference() -> str:
    return "sha256:" + sha256(Path(__file__).read_bytes()).hexdigest()


@lru_cache(maxsize=1)
def receipt_payload() -> dict[str, Any]:
    root = _stack_root()
    result = audit()
    return {
        "schema_id": SCHEMA_ID,
        "schema_version": SCHEMA_VERSION,
        "standing": STANDING,
        "selection_effect": SELECTION_EFFECT,
        "producer_code_reference": _producer_code_reference(),
        "source": {
            "authority": "The-Interdependency/ucns",
            "ucns_commit": groupoid_module.extension.PINNED_UCNS_COMMIT,
            "source_file_digests": [
                {"path": path, "sha256": digest}
                for path, digest in _source_file_digests(root)
            ],
            "ordered_groupoid_receipt_sha256": groupoid_module.receipt_digest(),
            "canonical_architecture_precedent": {
                "pipeline": "geometry-derived Wirtinger words -> noncommutative Fox/Magnus data -> explicit later abelian specialization",
                "transfer_boundary": "architecture only; canonical prime-selected P7/P5 data do not define recursive return words or factors",
            },
        },
        "candidate": {
            "operation": "exact noncommutative word invariants before homology",
            "coefficient_ring": "integral group ring Z[F_r] for Fox derivatives",
            "magnus_truncation_degree": 2,
            "word_selection_policy": "enumeration witness only; current geometry selects no cross-generator traversal",
            "observed_successor_cardinality_input": None,
            "observed_arithmetic_factor_input": None,
        },
        "result": result.to_payload(),
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
