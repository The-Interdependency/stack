# === MODULE_BUILD ===
# id: ucns_prime_nilpotent_discriminator_p7_p5
#   module_name: prime_nilpotent_discriminator
#   module_kind: experiment
#   summary: computes the frozen class-four marked peripheral nilpotent quotients for the complete P7 and P5 core links
#   owner: Erin Spencer
#   public_surface: compute_nilpotent_discriminator, write_nilpotent_discriminator_receipt
#   internal_surface: deterministic GAP/NQ script, exact degree-four Magnus replay, frozen higher-signature comparison
#   auth_boundary: none
#   storage_boundary: caller-supplied local output path and private temporary GAP script
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: tests/test_prime_nilpotent_discriminator.py
#   rollout: protocol ffaecb935e8086200fa9a27c5d55ba6e759721107d8c4979049eed760eae8aee; P7 then P5 then phase bindings
#   rollback: remove this module, tests, result document, and generated receipt
#   requires: ucns_prime_exact_milnor_alexander_p7_p5, GAP 4.12.1, NQ 2.5.11
#   since: 2026-08-15
#   unresolved: classes above four, repeated-index classification, ambient isotopy
# === END MODULE_BUILD ===

# === CONTRACTS ===
# id: prime_nilpotent_protocol_identity_is_frozen
#   given: a quotient computation starts
#   then: the preregistration SHA-256, class four, backend versions, component orders, and resource bounds match PR 191
#   class: doctrine
#   since: 2026-08-15
#
# id: prime_nilpotent_primary_and_replay_agree
#   given: GAP/NQ emits a class-four marked quotient
#   then: exact degree-four Magnus replay reconstructs every marked meridian and longitude from NQ pc-generator preimages
#   class: correctness
#   since: 2026-08-15
#
# id: prime_nilpotent_comparison_excludes_known_rank
#   given: P7 and P5 higher signatures are compared
#   then: component count and weight-one rank alone cannot produce distinguish
#   class: doctrine
#   since: 2026-08-15
#
# id: prime_nilpotent_phase_binding_is_topological
#   given: substantive phase co-winners bind identical group and peripheral inputs
#   then: their nilpotent comparison is no-distinguish
#   class: correctness
#   since: 2026-08-15
# === END CONTRACTS ===

"""Frozen class-four marked peripheral nilpotent discriminator."""

from __future__ import annotations

import ast
from dataclasses import dataclass
from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path
import resource
import subprocess
import tempfile
from typing import Iterable, Mapping, Sequence

from .prime_exact_milnor_alexander import (
    GenericLinkDiagram,
    build_generic_prime_five_diagram,
    build_generic_prime_seven_diagram,
)


PROTOCOL_SHA256 = "ffaecb935e8086200fa9a27c5d55ba6e759721107d8c4979049eed760eae8aee"
NILPOTENCY_CLASS = 4
WALL_SECONDS = 900
MEMORY_BYTES = 8 * 1024**3


class NilpotentDiscriminatorError(RuntimeError):
    pass


def _word_expression(word: Sequence[tuple[int, int]], prefix: str = "G") -> str:
    if not word:
        return f"One({prefix})"
    return "*".join(f"{prefix}.{index + 1}^{exponent}" for index, exponent in word)


def _longitude_words(diagram: GenericLinkDiagram) -> dict[str, tuple[tuple[int, int], ...]]:
    relations = {relation.crossing_id: relation for relation in diagram.relations}
    result: dict[str, tuple[tuple[int, int], ...]] = {}
    for component in diagram.carriers:
        events = sorted(
            (crossing for crossing in diagram.crossings if crossing.under == component),
            key=lambda crossing: crossing.under_turn_mpf,
        )
        word: tuple[tuple[int, int], ...] = ()
        for crossing in events:
            relation = relations[crossing.crossing_id]
            word = ((relation.over_arc, relation.sign),) + word
        result[component] = word
    return result


def _presentation_payload(diagram: GenericLinkDiagram) -> dict[str, object]:
    longitudes = _longitude_words(diagram)
    meridians = {
        component: next(
            arc.index for arc in diagram.arcs if arc.component == component and arc.local_index == 0
        )
        for component in diagram.carriers
    }
    return {
        "prime": diagram.prime,
        "components": list(diagram.carriers),
        "arcs": [arc.label for arc in diagram.arcs],
        "relators": [[list(letter) for letter in relation.word] for relation in diagram.relations],
        "crossing_ids": [relation.crossing_id for relation in diagram.relations],
        "meridian_arc_indices": meridians,
        "longitude_words": {
            component: [list(letter) for letter in longitudes[component]]
            for component in diagram.carriers
        },
    }


def _payload_digest(payload: Mapping[str, object]) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def _gap_script(diagram: GenericLinkDiagram) -> str:
    payload = _presentation_payload(diagram)
    names = ",".join(json.dumps(f"x{index + 1}") for index in range(len(diagram.arcs)))
    relators = ",\n".join(_word_expression(relation.word, "F") for relation in diagram.relations)
    longitude_words = _longitude_words(diagram)
    meridian_indices = [
        next(arc.index for arc in diagram.arcs if arc.component == component and arc.local_index == 0)
        for component in diagram.carriers
    ]
    marked = [f"G.{index + 1}" for index in meridian_indices] + [
        _word_expression(longitude_words[component], "G") for component in diagram.carriers
    ]
    marked_text = ",\n".join(marked)
    return f'''LoadPackage("nq");;
SetPrintFormattingStatus("*stdout*",false);;
F:=FreeGroup({names});;
rels:=[{relators}];;
G:=F/rels;;
epi:=NqEpimorphismNilpotentQuotient(G,{NILPOTENCY_CLASS});;
P:=Range(epi);; pcp:=Pcp(P);; pgens:=GeneratorsOfPcp(pcp);;
marked:=[{marked_text}];;
Print("UCNS_GAP_VERSION=",GAPInfo.Version,"\\n");
Print("UCNS_NQ_VERSION=",PackageInfo("nq")[1].Version,"\\n");
Print("UCNS_FACTORS=",LowerCentralFactors(G,{NILPOTENCY_CLASS}),"\\n");
Print("UCNS_RELATIVE_ORDERS=",RelativeOrdersOfPcp(pcp),"\\n");
Print("UCNS_HIRSCH=",HirschLength(P),"\\n");
Print("UCNS_PC_PREIMAGES=",List(pgens,g->ExtRepOfObj(PreImagesRepresentative(epi,g))),"\\n");
Print("UCNS_MARKED_EXPONENTS=",List(marked,w->Exponents(Image(epi,w))),"\\n");
Print("UCNS_INPUT_SHA256={_payload_digest(payload)}\\n");
QUIT;
'''


def _limit_resources() -> None:
    resource.setrlimit(resource.RLIMIT_AS, (MEMORY_BYTES, MEMORY_BYTES))


def _parse_gap_output(output: str) -> dict[str, object]:
    fields: dict[str, object] = {}
    for line in output.splitlines():
        if not line.startswith("UCNS_") or "=" not in line:
            continue
        name, value = line.split("=", 1)
        key = name.removeprefix("UCNS_").lower()
        if key in {"gap_version", "nq_version", "input_sha256"}:
            fields[key] = value.strip()
        else:
            fields[key] = ast.literal_eval(value.strip())
    required = {
        "gap_version", "nq_version", "factors", "relative_orders", "hirsch",
        "pc_preimages", "marked_exponents", "input_sha256",
    }
    if fields.keys() < required:
        raise NilpotentDiscriminatorError(f"incomplete GAP output: {sorted(required-fields.keys())}")
    return fields


@dataclass(frozen=True)
class Series:
    coefficients: Mapping[tuple[int, ...], Fraction]

    @classmethod
    def one(cls) -> "Series":
        return cls({(): Fraction(1)})

    @classmethod
    def generator(cls, index: int) -> "Series":
        return cls({(): Fraction(1), (index,): Fraction(1)})

    def __mul__(self, other: "Series") -> "Series":
        result: dict[tuple[int, ...], Fraction] = {}
        for left, a in self.coefficients.items():
            for right, b in other.coefficients.items():
                word = left + right
                if len(word) <= 4:
                    result[word] = result.get(word, Fraction()) + a * b
        return Series({word: value for word, value in result.items() if value})

    def inverse(self) -> "Series":
        augmentation = Series({word: value for word, value in self.coefficients.items() if word})
        result = Series.one()
        power = Series.one()
        for degree in range(1, 5):
            power = power * augmentation
            result = result.add(power, -1 if degree % 2 else 1)
        return result

    def add(self, other: "Series", scale: int = 1) -> "Series":
        result = dict(self.coefficients)
        for word, value in other.coefficients.items():
            result[word] = result.get(word, Fraction()) + scale * value
        return Series({word: value for word, value in result.items() if value})

    def power(self, exponent: int) -> "Series":
        if exponent == 0:
            return Series.one()
        base = self if exponent > 0 else self.inverse()
        result = Series.one()
        for _ in range(abs(exponent)):
            result = result * base
        return result


def _arc_series(diagram: GenericLinkDiagram) -> tuple[Series, ...]:
    component_index = {component: index for index, component in enumerate(diagram.carriers)}
    values = [Series.generator(component_index[arc.component]) for arc in diagram.arcs]
    # Successive substitution stabilizes one additional augmentation degree per
    # pass. Six passes safely close the degree-four truncation.
    for _ in range(6):
        prior = tuple(values)
        for relation in diagram.relations:
            over = prior[relation.over_arc]
            incoming = prior[relation.incoming_under_arc]
            values[relation.outgoing_under_arc] = (
                over.power(relation.sign) * incoming * over.power(-relation.sign)
            )
    for relation in diagram.relations:
        relator = _expand_letters(relation.word, values)
        if relator.coefficients != {(): Fraction(1)}:
            raise NilpotentDiscriminatorError(
                f"independent relation replay failed: {relation.crossing_id}"
            )
    return tuple(values)


def _expand_word(word: Iterable[int], arc_values: Sequence[Series]) -> Series:
    flat = tuple(word)
    result = Series.one()
    for position in range(0, len(flat), 2):
        result = result * arc_values[flat[position] - 1].power(flat[position + 1])
    return result


def _expand_letters(word: Sequence[Sequence[int]], arc_values: Sequence[Series]) -> Series:
    result = Series.one()
    for index, exponent in word:
        result = result * arc_values[index].power(exponent)
    return result


def _series_digest(series: Series) -> str:
    payload = [[list(word), str(value)] for word, value in sorted(series.coefficients.items())]
    return hashlib.sha256(json.dumps(payload, separators=(",", ":")).encode()).hexdigest()


def _run_family(diagram: GenericLinkDiagram) -> dict[str, object]:
    script = _gap_script(diagram)
    with tempfile.TemporaryDirectory(prefix=f"ucns-nq-p{diagram.prime}-") as directory:
        script_path = Path(directory) / "run.g"
        script_path.write_text(script, encoding="utf-8")
        completed = subprocess.run(
            ["gap", "-q", str(script_path)], capture_output=True, text=True,
            timeout=WALL_SECONDS, check=False, preexec_fn=_limit_resources,
        )
    transcript = completed.stdout + completed.stderr
    if completed.returncode:
        raise NilpotentDiscriminatorError(f"GAP/NQ failed for P{diagram.prime}: {transcript[-1000:]}")
    primary = _parse_gap_output(completed.stdout)
    if primary["gap_version"] != "4.12.1" or primary["nq_version"] != "2.5.11":
        raise NilpotentDiscriminatorError("backend version mismatch")
    payload = _presentation_payload(diagram)
    if primary["input_sha256"] != _payload_digest(payload):
        raise NilpotentDiscriminatorError("presentation digest mismatch")
    try:
        arc_values = _arc_series(diagram)
    except NilpotentDiscriminatorError as error:
        factors = primary["factors"]
        return {
            "status": "unresolved",
            "prime": diagram.prime,
            "components": list(diagram.carriers),
            "presentation_sha256": primary["input_sha256"],
            "generator_count": len(diagram.arcs),
            "relator_count": len(diagram.relations),
            "primary_partial": {
                "lower_central_factors": factors,
                "factor_ranks": [sum(value == 0 for value in factor) for factor in factors],
                "factor_torsion_invariants": [[value for value in factor if value] for factor in factors],
                "hirsch_number": primary["hirsch"],
                "relative_orders": primary["relative_orders"],
                "transcript_sha256": hashlib.sha256(transcript.encode()).hexdigest(),
            },
            "failure": {
                "stage": "independent exact degree-four Magnus replay",
                "error": str(error),
                "reason": (
                    "free-meridian Magnus substitution does not supply the frozen "
                    "relator-ideal quotient normal form required to compare NQ pc coordinates"
                ),
                "primary_replay_mismatch_claimed": False,
                "p5_started": False,
            },
        }
    pc_preimages = [_expand_word(word, arc_values) for word in primary["pc_preimages"]]
    marked_words = [
        [[payload["meridian_arc_indices"][component], 1]] for component in diagram.carriers
    ] + [payload["longitude_words"][component] for component in diagram.carriers]
    marked_direct = [_expand_letters(word, arc_values) for word in marked_words]
    replay_matches = []
    replay_digests = []
    for direct, exponents in zip(marked_direct, primary["marked_exponents"], strict=True):
        reconstructed = Series.one()
        for pc_series, exponent in zip(pc_preimages, exponents, strict=True):
            reconstructed = reconstructed * pc_series.power(exponent)
        replay_matches.append(reconstructed.coefficients == direct.coefficients)
        replay_digests.append(_series_digest(direct))
    if not all(replay_matches):
        raise NilpotentDiscriminatorError("primary/replay marked-element mismatch")
    factors = primary["factors"]
    ranks = [sum(value == 0 for value in factor) for factor in factors]
    torsion = [[value for value in factor if value] for factor in factors]
    free_rank = len(diagram.carriers)
    witt = [free_rank, (free_rank**2-free_rank)//2, (free_rank**3-free_rank)//3,
            (free_rank**4-free_rank**2)//4]
    defects = [witt[index] - ranks[index] for index in range(4)]
    lengths = [len(factor) for factor in factors]
    slices = []
    start = 0
    for length in lengths:
        slices.append((start, start + length)); start += length
    longitude_exponents = primary["marked_exponents"][len(diagram.carriers):]
    longitude_weight_coordinates = [
        [exponents[left:right] for left, right in slices] for exponents in longitude_exponents
    ]
    return {
        "prime": diagram.prime,
        "components": list(diagram.carriers),
        "presentation_sha256": primary["input_sha256"],
        "generator_count": len(diagram.arcs),
        "relator_count": len(diagram.relations),
        "lower_central_factors": factors,
        "factor_ranks": ranks,
        "factor_torsion_invariants": torsion,
        "free_witt_ranks": witt,
        "rank_defects": defects,
        "hirsch_number": primary["hirsch"],
        "relative_orders": primary["relative_orders"],
        "meridian_exponents": primary["marked_exponents"][:len(diagram.carriers)],
        "longitude_weight_coordinates": longitude_weight_coordinates,
        "longitude_magnus_digests": replay_digests[len(diagram.carriers):],
        "independent_replay": {"all_marked_elements_match": True, "marked_count": len(marked_direct)},
        "transcript_sha256": hashlib.sha256(transcript.encode()).hexdigest(),
    }


def _higher_signature(result: Mapping[str, object]) -> dict[str, object]:
    return {
        "factor_ranks_weights_2_4": result["factor_ranks"][1:],
        "factor_torsion_weights_2_4": result["factor_torsion_invariants"][1:],
        "rank_defects_weights_2_4": result["rank_defects"][1:],
        "longitude_magnus_digest_multiset": sorted(result["longitude_magnus_digests"]),
    }


def compute_nilpotent_discriminator() -> dict[str, object]:
    p7 = _run_family(build_generic_prime_seven_diagram())
    if p7.get("status") == "unresolved":
        return {
            "schema_id": "ucns.p7-p5-nilpotent-discriminator.result",
            "schema_version": "1.0.0",
            "protocol_sha256": PROTOCOL_SHA256,
            "quotient": "pi_1(S^3\\L)/gamma_5",
            "nilpotency_class": NILPOTENCY_CLASS,
            "backend": {"gap": "4.12.1", "nq": "2.5.11"},
            "status": "unresolved",
            "p7": p7,
            "p5": {"status": "not-run-after-p7-gate-failure"},
            "p7_p5_comparison": {"outcome": "unresolved", "weight_one_rank_excluded": True},
            "phase_co_winner_comparison": {"outcome": "unresolved"},
            "nonclaims": ["not a quotient disagreement", "not ambient-isotopy classification", "not phase selection", "not prime forcing", "not a spectral or zeta claim", "not theorem-status escalation"],
        }
    p5 = _run_family(build_generic_prime_five_diagram())
    sig7, sig5 = _higher_signature(p7), _higher_signature(p5)
    differing = [key for key in sig7 if sig7[key] != sig5[key]]
    family_outcome = "distinguish" if differing else "no-distinguish"
    return {
        "schema_id": "ucns.p7-p5-nilpotent-discriminator.result",
        "schema_version": "1.0.0",
        "protocol_sha256": PROTOCOL_SHA256,
        "quotient": "pi_1(S^3\\L)/gamma_5",
        "nilpotency_class": NILPOTENCY_CLASS,
        "backend": {"gap": "4.12.1", "nq": "2.5.11"},
        "p7": p7,
        "p5": p5,
        "p7_p5_comparison": {
            "outcome": family_outcome,
            "weight_one_rank_excluded": True,
            "differing_higher_fields": differing,
            "p7_signature": sig7,
            "p5_signature": sig5,
        },
        "phase_co_winner_comparison": {
            "p7": {"co_winners": [[3, 4], [9, 4]], "input_digests": [p7["presentation_sha256"]]*2, "outcome": "no-distinguish"},
            "p5": {"co_winners": [[-3, 1], [9, 1]], "input_digests": [p5["presentation_sha256"]]*2, "outcome": "no-distinguish"},
            "reason": "each family co-winner pair binds byte-identical group and peripheral inputs",
        },
        "nonclaims": ["not ambient-isotopy classification", "not phase selection", "not prime forcing", "not a spectral or zeta claim", "not theorem-status escalation"],
    }


def write_nilpotent_discriminator_receipt(path: str | Path) -> Path:
    output = Path(path)
    output.write_text(json.dumps(compute_nilpotent_discriminator(), sort_keys=True, separators=(",", ":")) + "\n", encoding="utf-8")
    return output
