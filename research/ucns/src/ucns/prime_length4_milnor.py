# === MODULE_BUILD ===
# id: ucns_prime_length4_milnor_p7
#   module_name: prime_length4_milnor
#   module_kind: experiment
#   summary: evaluates the frozen minimal P7 length-four Milnor experiment with exact degree-three Magnus arithmetic
#   owner: Erin Spencer
#   public_surface: LengthFourMilnorCertificate, length_four_commutator_gate, evaluate_p7_length_four_milnor, write_p7_length_four_milnor_certificate
#   internal_surface: degree-three noncommutative series, fixed-diagram Wirtinger longitude replay
#   auth_boundary: none
#   storage_boundary: caller-supplied local paths only through writer function
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: tests/test_prime_length4_milnor.py
#   rollout: frozen ordered target R0,R1,R4,R5 only; accept nonzero, zero, or unresolved without retargeting
#   rollback: remove this module, its tests, result document, and generated certificate
#   requires: ucns_prime_exact_milnor_alexander_p7_p5
#   since: 2026-08-15
#   unresolved: repeated-index Milnor invariants, higher nilpotent quotients, whole-link length-four program
# === END MODULE_BUILD ===

# === CONTRACTS ===
# id: prime_length4_magnus_gate_matches_frozen_commutator
#   given: the degree-three Magnus engine evaluates [[x1,x2],x3]
#   then: the four frozen degree-three coefficients and every lower degree coefficient match the preregistration
#   class: correctness
#   since: 2026-08-15
#
# id: prime_p7_length4_target_is_frozen_and_lower_gated
#   given: the minimal P7 length-four experiment is evaluated
#   then: only R0,R1,R4,R5 is targeted and all six linking, four triple-Milnor, and required longitude lower-degree gates are exact zero
#   class: doctrine
#   since: 2026-08-15
#
# id: prime_p7_length4_result_records_cyclic_conventions
#   given: the frozen target passes its lower-order gates
#   then: the canonical, reverse-word, and four cyclic-rotation coefficients are retained without changing the primary target
#   class: evidence
#   since: 2026-08-15
#
# id: prime_p7_length4_receipt_is_bounded
#   given: the result is serialized
#   then: it preserves computer-assisted diagram standing and makes no isotopy-classification, phase, spectral, zeta, or theorem-status claim
#   class: doctrine
#   since: 2026-08-15
# === END CONTRACTS ===

"""Frozen minimal P7 length-four Milnor experiment."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
import bisect
import json
from pathlib import Path
from typing import Mapping, Sequence

import mpmath as mp

from .prime_exact_milnor_alexander import (
    ExactMilnorAlexanderError,
    GenericLinkDiagram,
    _milnor_certificate,
    _triple_crossing_records,
    build_generic_prime_seven_diagram,
)


TARGET = ("R0", "R1", "R4", "R5")
COMMUTATOR_CONVENTION = "[a,b]=a b a^-1 b^-1"
PREREGISTRATION_SHA256 = "c013b36ff1d1c982c0531b061e8ce024b6db2aa3dbb7a2072bc25a75e74b1bb1"


class DegreeThreeSeries:
    """Exact noncommutative Magnus series modulo words of degree four."""

    __slots__ = ("coefficients",)

    def __init__(self, coefficients: Mapping[tuple[int, ...], Fraction] | None = None):
        self.coefficients = {
            tuple(word): Fraction(value)
            for word, value in (coefficients or {}).items()
            if value and len(word) <= 3
        }

    @classmethod
    def one(cls) -> "DegreeThreeSeries":
        return cls({(): Fraction(1)})

    @classmethod
    def generator(cls, index: int) -> "DegreeThreeSeries":
        return cls({(): Fraction(1), (index,): Fraction(1)})

    def __mul__(self, other: "DegreeThreeSeries") -> "DegreeThreeSeries":
        result: dict[tuple[int, ...], Fraction] = {}
        for left_word, left_value in self.coefficients.items():
            for right_word, right_value in other.coefficients.items():
                word = left_word + right_word
                if len(word) <= 3:
                    result[word] = result.get(word, Fraction()) + left_value * right_value
        return DegreeThreeSeries(result)

    def inverse(self) -> "DegreeThreeSeries":
        if self.coefficients.get((), Fraction()) != 1:
            raise ExactMilnorAlexanderError("Magnus inverse requires constant coefficient one")
        augmentation = DegreeThreeSeries(
            {word: value for word, value in self.coefficients.items() if word}
        )
        square = augmentation * augmentation
        cube = square * augmentation
        result: dict[tuple[int, ...], Fraction] = {(): Fraction(1)}
        for sign, series in ((-1, augmentation), (1, square), (-1, cube)):
            for word, value in series.coefficients.items():
                result[word] = result.get(word, Fraction()) + sign * value
        return DegreeThreeSeries(result)

    def power(self, exponent: int) -> "DegreeThreeSeries":
        if exponent == 1:
            return self
        if exponent == -1:
            return self.inverse()
        raise ExactMilnorAlexanderError("only exponents plus or minus one are supported")

    def coefficient(self, word: Sequence[int]) -> Fraction:
        return self.coefficients.get(tuple(word), Fraction())


def _commutator(left: DegreeThreeSeries, right: DegreeThreeSeries) -> DegreeThreeSeries:
    return left * right * left.inverse() * right.inverse()


def length_four_commutator_gate() -> dict[str, object]:
    generators = tuple(DegreeThreeSeries.generator(index) for index in range(3))
    value = _commutator(_commutator(generators[0], generators[1]), generators[2])
    expected = {
        (0, 1, 2): 1,
        (1, 0, 2): -1,
        (2, 0, 1): -1,
        (2, 1, 0): 1,
    }
    observed = {word: int(value.coefficient(word)) for word in expected}
    lower = {
        word: coefficient
        for word, coefficient in value.coefficients.items()
        if word and len(word) < 3 and coefficient
    }
    return {
        "word": "[[x1,x2],x3]",
        "commutator_convention": COMMUTATOR_CONVENTION,
        "degree_three_coefficients": {
            "_".join(f"X{index + 1}" for index in word): coefficient
            for word, coefficient in observed.items()
        },
        "lower_degree_nonzero_coefficients": {
            ",".join(map(str, word)): str(coefficient) for word, coefficient in lower.items()
        },
        "passed": observed == expected and not lower,
    }


def _longitudes(
    components: Sequence[str], crossing_rows: Sequence[Mapping[str, object]]
) -> dict[str, DegreeThreeSeries]:
    component_index = {component: index for index, component in enumerate(components)}
    meridians = {
        component: DegreeThreeSeries.generator(component_index[component])
        for component in components
    }
    under_events = {
        component: tuple(
            sorted(
                (row for row in crossing_rows if row["under"] == component),
                key=lambda row: row["under_turn"],
            )
        )
        for component in components
    }
    after_states: dict[str, tuple[DegreeThreeSeries, ...]] = {}
    for component in components:
        current = meridians[component]
        states: list[DegreeThreeSeries] = []
        for row in under_events[component]:
            over = meridians[str(row["over"])]
            sign = int(row["sign"])
            current = over.power(sign) * current * over.power(-sign)
            states.append(current)
        after_states[component] = tuple(states)

    def arc_at(component: str, turn: mp.mpf) -> DegreeThreeSeries:
        events = under_events[component]
        if not events:
            return meridians[component]
        first_turn = mp.mpf(events[0]["under_turn"])
        relative = [mp.fmod(mp.mpf(row["under_turn"]) - first_turn, 1) for row in events]
        relative = [value if value >= 0 else value + 1 for value in relative]
        target = mp.fmod(turn - first_turn, 1)
        if target < 0:
            target += 1
        position = bisect.bisect_left(relative, target) - 1
        return meridians[component] if position < 0 else after_states[component][position]

    result: dict[str, DegreeThreeSeries] = {}
    for component in components:
        longitude = DegreeThreeSeries.one()
        for row in under_events[component]:
            over_arc = arc_at(str(row["over"]), mp.mpf(row["over_turn"]))
            longitude = over_arc.power(int(row["sign"])) * longitude
        result[component] = longitude
    return result


def _coefficient_for_order(
    diagram: GenericLinkDiagram, order: tuple[str, str, str, str]
) -> int:
    rows = _triple_crossing_records(diagram, order)
    longitude = _longitudes(order, rows)[order[3]]
    coefficient = longitude.coefficient((0, 1, 2))
    if coefficient.denominator != 1:
        raise ExactMilnorAlexanderError("length-four Magnus coefficient is nonintegral")
    return coefficient.numerator


@dataclass(frozen=True, slots=True)
class LengthFourMilnorCertificate:
    primary_coefficient: int | None
    reverse_word_coefficient: int | None
    cyclic_coefficients: tuple[int, ...]
    lower_degree_nonzero: tuple[tuple[str, int], ...]
    pairwise_linking: tuple[int, ...]
    triple_milnor: tuple[int, ...]
    crossing_ids: tuple[str, ...]
    status: str
    obstruction: str | None

    def as_dict(self) -> dict[str, object]:
        return {
            "schema_id": "ucns.p7-length4-milnor.result",
            "schema_version": "1.0.0",
            "preregistration": {
                "document": "docs/PREREGISTRATION_P7_LENGTH4_MILNOR.md",
                "sha256": PREREGISTRATION_SHA256,
                "frozen_before_evaluation": True,
            },
            "preregistered_target": list(TARGET),
            "primary_invariant": "mu_bar_R0_R1_R4_R5",
            "primary_coefficient": self.primary_coefficient,
            "reverse_word_coefficient": self.reverse_word_coefficient,
            "cyclic_rotations": [
                {"order": list(TARGET[offset:] + TARGET[:offset]), "coefficient": value}
                for offset, value in enumerate(self.cyclic_coefficients)
            ],
            "lower_order_gates": {
                "pairwise_linking_numbers": list(self.pairwise_linking),
                "triple_milnor_invariants": list(self.triple_milnor),
                "preferred_longitude_nonzero_degree_one_or_two": [
                    {"word": word, "coefficient": value}
                    for word, value in self.lower_degree_nonzero
                ],
            },
            "crossing_ids": list(self.crossing_ids),
            "algebraic_gate": length_four_commutator_gate(),
            "status": self.status,
            "obstruction": self.obstruction,
            "diagram_standing": "computer-assisted fixed generic P7 diagram with recorded nonzero margins",
            "selection_effect": "none",
            "nonclaims": [
                "not a complete ambient-isotopy classification",
                "not a phase law or prime-forcing result",
                "not a spectral or zeta claim",
                "not theorem-status escalation",
            ],
        }


def evaluate_p7_length_four_milnor() -> LengthFourMilnorCertificate:
    gate = length_four_commutator_gate()
    if not gate["passed"]:
        raise ExactMilnorAlexanderError("frozen degree-three commutator gate failed")
    diagram = build_generic_prime_seven_diagram()
    carrier_index = {
        component: index for index, component in enumerate(diagram.carriers)
    }
    indices = tuple(carrier_index[component] for component in TARGET)
    pairwise = tuple(
        diagram.pairwise_linking_matrix[left][right]
        for position, left in enumerate(indices)
        for right in indices[position + 1 :]
    )
    triple_orders = (
        ("R0", "R1", "R4"),
        ("R0", "R1", "R5"),
        ("R0", "R4", "R5"),
        ("R1", "R4", "R5"),
    )
    triple_values = tuple(
        _milnor_certificate(diagram, order).coefficient_ij_in_longitude_k
        for order in triple_orders
    )
    rows = _triple_crossing_records(diagram, TARGET)
    longitude = _longitudes(TARGET, rows)[TARGET[3]]
    lower = tuple(
        ("_".join(TARGET[index] for index in word), coefficient.numerator)
        for word, coefficient in sorted(longitude.coefficients.items())
        if word and len(word) < 3 and coefficient
    )
    obstruction = None
    if any(pairwise):
        obstruction = "pairwise linking gate failed"
    elif any(triple_values):
        obstruction = "length-three Milnor gate failed"
    elif lower:
        obstruction = "preferred-longitude lower-degree gate failed"
    if obstruction:
        return LengthFourMilnorCertificate(
            primary_coefficient=None,
            reverse_word_coefficient=None,
            cyclic_coefficients=(),
            lower_degree_nonzero=lower,
            pairwise_linking=pairwise,
            triple_milnor=triple_values,
            crossing_ids=tuple(str(row["crossing_id"]) for row in rows),
            status="unresolved",
            obstruction=obstruction,
        )
    primary = longitude.coefficient((0, 1, 2))
    reverse = longitude.coefficient((2, 1, 0))
    if primary.denominator != 1 or reverse.denominator != 1:
        raise ExactMilnorAlexanderError("length-four Magnus coefficient is nonintegral")
    cyclic = tuple(
        _coefficient_for_order(diagram, TARGET[offset:] + TARGET[:offset])
        for offset in range(4)
    )
    if len(set(cyclic)) != 1:
        obstruction = "cyclic convention check disagreed"
        status = "unresolved"
    else:
        status = "nonzero" if primary else "zero"
    return LengthFourMilnorCertificate(
        primary_coefficient=primary.numerator,
        reverse_word_coefficient=reverse.numerator,
        cyclic_coefficients=cyclic,
        lower_degree_nonzero=lower,
        pairwise_linking=pairwise,
        triple_milnor=triple_values,
        crossing_ids=tuple(str(row["crossing_id"]) for row in rows),
        status=status,
        obstruction=obstruction,
    )


def write_p7_length_four_milnor_certificate(path: str | Path) -> Path:
    output = Path(path)
    output.write_text(
        json.dumps(evaluate_p7_length_four_milnor().as_dict(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return output
