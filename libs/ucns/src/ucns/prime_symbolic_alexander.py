# === MODULE_BUILD ===
# id: ucns_prime_symbolic_alexander_p7_p5
#   module_name: prime_symbolic_alexander
#   module_kind: experiment
#   summary: derives the exact multivariable Fox-Alexander presentations and certifies their first nonzero elementary-ideal boundaries for the frozen P7 and P5 diagrams
#   owner: Erin Spencer
#   public_surface: SymbolicAlexanderCertificate, symbolic_alexander_certificate, symbolic_alexander_family_certificate, write_symbolic_alexander_family_certificate
#   internal_surface: exact Laurent Fox derivatives, rational-function rank, pivot minor, Fox fundamental identity
#   auth_boundary: none
#   storage_boundary: caller-supplied local paths only through writer functions
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: tests/test_prime_symbolic_alexander.py
#   rollout: P7 first and P5 same-construction comparison second; selection effect none
#   rollback: remove this module, its tests, documentation, and generated certificate
#   requires: ucns_prime_exact_milnor_alexander_p7_p5, sympy>=1.12,<2
#   since: 2026-08-15
#   unresolved: complete generating sets and Groebner bases for the first nonzero ideals, higher elementary ideals, phase-co-winner separation, higher Milnor invariants
# === END MODULE_BUILD ===

# === CONTRACTS ===
# id: prime_symbolic_fox_presentation_is_exact
#   given: the frozen P7 or P5 Wirtinger diagram is abelianized over one Laurent variable per component
#   then: every sparse Fox entry has exact integer Laurent coefficients and every row satisfies the Fox fundamental identity
#   class: correctness
#   since: 2026-08-15
#
# id: prime_symbolic_elementary_boundary_is_exact
#   given: the exact symbolic presentation is evaluated over its Laurent-polynomial fraction field
#   then: exact rank and a nonzero pivot minor certify every earlier elementary ideal as zero and the declared first nonzero ideal as nonzero
#   class: evidence
#   since: 2026-08-15
#
# id: prime_symbolic_certificate_replays_finite_characters
#   given: the symbolic matrix is specialized at every previously frozen prime-order character
#   then: every modular rank equals the independently retained Fox-character fingerprint
#   class: regression
#   since: 2026-08-15
#
# id: prime_symbolic_alexander_receipt_is_nonselecting
#   given: the family certificate is serialized
#   then: it distinguishes presentation and ideal-boundary evidence from a complete ideal basis, link classification, phase selection, or spectral claim
#   class: doctrine
#   since: 2026-08-15
# === END CONTRACTS ===

"""Exact symbolic Alexander-module evidence for the frozen P7/P5 diagrams.

The coefficient ring is the Laurent ring over the integers with one variable
per oriented link component.  Exact fraction-field elimination determines the
rank.  A pivot minor then witnesses the first nonzero elementary ideal, while
rank bounds prove all earlier determinantal ideals zero.  The certificate does
not claim a complete generating set for the first nonzero ideal.
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
import hashlib
import json
from pathlib import Path
from typing import Mapping

from sympy.polys.domains import QQ
from sympy.polys.matrices import DomainMatrix
import sympy as sp

from .prime_exact_milnor_alexander import (
    FIELD_MODULUS,
    _component_character,
    _matrix_rank_mod,
    build_generic_prime_five_diagram,
    build_generic_prime_seven_diagram,
    fox_rank_fingerprint,
)

SCHEMA_ID = "ucns.prime-symbolic-alexander"
SCHEMA_VERSION = "0.1.0"


class SymbolicAlexanderError(ValueError):
    """Raised when exact symbolic evidence fails closed."""


def _canonical_sha256(value: object) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()


def _diagram(prime: int):
    if prime == 7:
        return build_generic_prime_seven_diagram()
    if prime == 5:
        return build_generic_prime_five_diagram()
    raise SymbolicAlexanderError("only the frozen P7 and P5 diagrams are supported")


def _matrix_data(prime: int):
    diagram = _diagram(prime)
    components = tuple(sorted({arc.component for arc in diagram.arcs}))
    variable_names = tuple(f"t_{component}" for component in components)
    field = QQ.frac_field(*variable_names)
    variables = dict(zip(components, field.gens))
    generator_values = {arc.index: variables[arc.component] for arc in diagram.arcs}
    rows: dict[int, dict[int, object]] = {}
    serialized_rows: list[list[dict[str, object]]] = []

    for row_index, relation in enumerate(diagram.relations):
        derivatives: dict[int, object] = {}
        prefix = field.one
        for generator, exponent in relation.word:
            value = generator_values[generator]
            if exponent == 1:
                derivatives[generator] = derivatives.get(generator, field.zero) + prefix
                prefix *= value
            elif exponent == -1:
                derivatives[generator] = derivatives.get(generator, field.zero) - prefix / value
                prefix /= value
            else:
                raise SymbolicAlexanderError("Fox word contains an unsupported exponent")
        if prefix != field.one:
            raise SymbolicAlexanderError("Wirtinger relator did not abelianize to one")
        rows[row_index] = {column: value for column, value in derivatives.items() if value}
        serialized_rows.append(
            [
                {"column": column, "laurent_polynomial": str(value)}
                for column, value in sorted(rows[row_index].items())
            ]
        )

    matrix = DomainMatrix(rows, (diagram.generator_count, diagram.generator_count), field)
    fox_vector = [generator_values[index] - field.one for index in range(diagram.generator_count)]
    for row in rows.values():
        identity = sum((value * fox_vector[column] for column, value in row.items()), field.zero)
        if identity != field.zero:
            raise SymbolicAlexanderError("Fox fundamental identity failed")
    return diagram, components, variable_names, field, matrix, serialized_rows


def _specialized_matrix(prime: int, rows, component_values: Mapping[str, int]):
    diagram = _diagram(prime)
    modulus = FIELD_MODULUS[prime]
    values = {sp.Symbol(f"t_{component}"): value % modulus for component, value in component_values.items()}
    result: list[list[int]] = []
    for row in rows:
        output = [0] * diagram.generator_count
        for entry in row:
            # Fraction-field elements are Laurent polynomials here, so every
            # denominator is a monomial and is invertible at character values.
            expression = sp.cancel(sp.sympify(entry["laurent_polynomial"]).subs(values))
            numerator_expr, denominator_expr = sp.fraction(expression)
            numerator = int(numerator_expr) % modulus
            denominator = int(denominator_expr) % modulus
            output[entry["column"]] = numerator * pow(denominator, -1, modulus) % modulus
        result.append(output)
    return result


@dataclass(frozen=True, slots=True)
class SymbolicAlexanderCertificate:
    prime: int
    variables: tuple[str, ...]
    generator_labels: tuple[str, ...]
    sparse_rows: tuple[tuple[tuple[int, str], ...], ...]
    fraction_field_rank: int
    first_nonzero_elementary_ideal: int
    pivot_rows: tuple[int, ...]
    pivot_columns: tuple[int, ...]
    pivot_minor: str
    specialized_rank_vector_sha256: str

    def as_dict(self) -> dict[str, object]:
        presentation = {
            "coefficient_ring": "Z[" + ",".join(f"{name}^+-1" for name in self.variables) + "]",
            "variables": list(self.variables),
            "generators": list(self.generator_labels),
            "rows": [
                [{"column": column, "laurent_polynomial": value} for column, value in row]
                for row in self.sparse_rows
            ],
        }
        return {
            "prime": self.prime,
            "presentation": presentation,
            "presentation_sha256": _canonical_sha256(presentation),
            "fraction_field_rank": self.fraction_field_rank,
            "nullity": len(self.generator_labels) - self.fraction_field_rank,
            "elementary_ideal_boundary": {
                "convention": "E_k is generated by all (n-k)-minors of the n-by-n Fox matrix",
                "zero_ideals": [f"E_{index}" for index in range(self.first_nonzero_elementary_ideal)],
                "first_nonzero_ideal": f"E_{self.first_nonzero_elementary_ideal}",
                "witness_minor_size": self.fraction_field_rank,
                "pivot_rows": list(self.pivot_rows),
                "pivot_columns": list(self.pivot_columns),
                "nonzero_pivot_minor": self.pivot_minor,
                "standing": "exact nonzero membership witness, not a complete generating set or Groebner basis",
            },
            "finite_character_replay": {
                "ordered_rank_vector_sha256": self.specialized_rank_vector_sha256,
                "matches_frozen_fingerprint": True,
            },
        }


@lru_cache(maxsize=2)
def symbolic_alexander_certificate(prime: int) -> SymbolicAlexanderCertificate:
    diagram, _, variable_names, _, matrix, serialized = _matrix_data(prime)
    dense = matrix.to_dense()
    rank = matrix.rank()
    pivot_columns = tuple(dense.rref()[1])
    pivot_rows = tuple(dense.transpose().rref()[1])
    if len(pivot_columns) != rank or len(pivot_rows) != rank:
        raise SymbolicAlexanderError("exact pivot profile disagrees with rank")
    pivot_minor = dense.extract(list(pivot_rows), list(pivot_columns)).det()
    if not pivot_minor:
        raise SymbolicAlexanderError("declared elementary-ideal witness is zero")

    rows = tuple(
        tuple((entry["column"], entry["laurent_polynomial"]) for entry in row)
        for row in serialized
    )
    ranks: list[int] = []
    fingerprint = fox_rank_fingerprint(prime)
    for character in fingerprint.rows:
        values = _component_character(prime, character.winding_residue, character.outer_numerator)
        specialized = _specialized_matrix(prime, serialized, values)
        computed_rank = _matrix_rank_mod(specialized, FIELD_MODULUS[prime])
        if computed_rank != character.rank:
            raise SymbolicAlexanderError("symbolic specialization disagrees with frozen fingerprint")
        ranks.append(computed_rank)
    rank_digest = _canonical_sha256(ranks)
    frozen_rank_digest = _canonical_sha256([row.rank for row in fingerprint.rows])
    if rank_digest != frozen_rank_digest:
        raise SymbolicAlexanderError("finite-character rank digest mismatch")

    return SymbolicAlexanderCertificate(
        prime=prime,
        variables=variable_names,
        generator_labels=tuple(arc.label for arc in diagram.arcs),
        sparse_rows=rows,
        fraction_field_rank=rank,
        first_nonzero_elementary_ideal=diagram.generator_count - rank,
        pivot_rows=pivot_rows,
        pivot_columns=pivot_columns,
        pivot_minor=str(pivot_minor),
        specialized_rank_vector_sha256=rank_digest,
    )


def symbolic_alexander_family_certificate() -> dict[str, object]:
    p7 = symbolic_alexander_certificate(7)
    p5 = symbolic_alexander_certificate(5)
    return {
        "schema_id": f"{SCHEMA_ID}.family",
        "schema_version": SCHEMA_VERSION,
        "selection_effect": "none",
        "research_order": [7, 5],
        "p7": p7.as_dict(),
        "p5": p5.as_dict(),
        "comparison": {
            "P7_fraction_field_rank": p7.fraction_field_rank,
            "P5_fraction_field_rank": p5.fraction_field_rank,
            "P7_first_nonzero_elementary_ideal": f"E_{p7.first_nonzero_elementary_ideal}",
            "P5_first_nonzero_elementary_ideal": f"E_{p5.first_nonzero_elementary_ideal}",
            "result": "the fixed diagrams have distinct exact Alexander-module rank and elementary-ideal onset",
        },
        "nonclaims": [
            "not a complete generating set or Groebner basis for either first nonzero ideal",
            "not a complete link invariant or ambient-isotopy classification",
            "not a phase-law selection or unique prime-forcing theorem",
            "not a spectral, zeta, or Riemann-hypothesis claim",
        ],
        "next": [
            "compute reduced generating sets for the first nonzero elementary ideals with an independently pinned computer-algebra backend",
            "calculate length-four Milnor invariants or finite nilpotent quotients",
            "preregister a whole-link invariant for the substantive phase co-winners",
        ],
    }


def write_symbolic_alexander_family_certificate(path: str | Path) -> Path:
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(symbolic_alexander_family_certificate(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return output


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    arguments = parser.parse_args()
    write_symbolic_alexander_family_certificate(arguments.output)
