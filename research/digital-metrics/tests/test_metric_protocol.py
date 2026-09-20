"""Adversarial witnesses for the Stack-local digital metric protocol."""

from __future__ import annotations

# === CHECKS ===
# id: check_digital_metric_missing_field_rejection
#   proves: digital_metric_missing_never_becomes_zero
#   call: self::test_missing_value_field_is_rejected_before_any_default
#   mutates: none
#   cleanup: none
#
# id: check_digital_metric_explicit_nonobserved
#   proves: digital_metric_missing_never_becomes_zero
#   call: self::test_non_observed_value_requires_explicit_null_and_reason
#   mutates: none
#   cleanup: none
#
# id: check_digital_metric_boolean_integer_separation
#   proves: digital_metric_types_are_exact
#   call: self::test_boolean_and_integer_encodings_do_not_alias
#   mutates: none
#   cleanup: none
#
# id: check_digital_metric_float_rejection
#   proves: digital_metric_types_are_exact
#   call: self::test_float_is_rejected_everywhere
#   mutates: none
#   cleanup: none
#
# id: check_digital_metric_relation_fidelity
#   proves: digital_metric_structure_preserves_order_multiplicity_provenance
#   call: self::test_relation_order_and_multiplicity_are_measured
#   mutates: none
#   cleanup: none
#
# id: check_digital_metric_provenance_fidelity
#   proves: digital_metric_structure_preserves_order_multiplicity_provenance
#   call: self::test_provenance_change_is_not_retained
#   mutates: none
#   cleanup: none
#
# id: check_digital_metric_receipt_replay
#   proves: digital_metric_receipt_replays_byte_identically
#   call: self::test_receipt_is_byte_deterministic_and_tamper_evident
#   mutates: none
#   cleanup: none
#
# id: check_digital_metric_nontransfer
#   proves: digital_metric_status_does_not_transfer
#   call: self::test_binding_status_transfer_must_remain_false
#   mutates: none
#   cleanup: none
#
# id: check_digital_metric_exact_producer_gate
#   proves: digital_metric_generator_requires_exact_clean_producers
#   call: self::test_generator_rejects_wrong_checkout_commit
#   mutates: none
#   cleanup: none
#
# id: check_digital_metric_metapat_binding
#   proves: digital_metric_metapat_binding_is_constraint_only
#   call: self::test_frozen_receipt_preserves_metapat_nontransfer
#   mutates: none
#   cleanup: none
#
# id: check_digital_metric_ucns_transition
#   proves: digital_metric_ucns_transition_uses_native_law
#   call: self::test_frozen_receipt_records_native_ucns_transition
#   mutates: none
#   cleanup: none
# === END CHECKS ===

from copy import deepcopy
from fractions import Fraction
from pathlib import Path
import json
import sys
import unittest


WORKSPACE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(WORKSPACE))

from metric_protocol import (  # noqa: E402
    MetricProtocolError,
    boolean_value,
    canonical_json,
    make_metric_definition,
    make_observation,
    measure_retention,
    rational_value,
    seal_receipt,
    seal_structure,
    sha256_json,
    validate_observation,
    verify_receipt,
)


from generate_receipt import ProducerIdentityError, verify_checkout  # noqa: E402
SHA_A = "a" * 64
SHA_B = "b" * 64
SHA_C = "c" * 64
COMMIT_A = "1" * 40
WORK_GRAPH_SHA = "d" * 64


def definition(*, kind: str = "boolean") -> dict:
    numeric = kind in {"integer", "rational"}
    return make_metric_definition(
        metric_id=f"stack.test.{kind}",
        metric_version="0.1.0",
        owner_repository="The-Interdependency/stack",
        construct="test-only strict wire behavior",
        subject_kind="test-fixture",
        value_kind=kind,
        unit="ratio" if numeric else "truth-value",
        minimum=0 if numeric else None,
        maximum=1 if numeric else None,
        computation_id="stack.test.metric",
        computation_sha256=SHA_A,
        interpretation="test fixture only",
        nonclaims=("No semantic, geometric, measurement, or empirical status transfer.",),
    )


def provenance() -> dict:
    return {
        "work_graph_sha256": WORK_GRAPH_SHA,
        "source_repository": "The-Interdependency/stack",
        "source_commit": COMMIT_A,
        "source_artifact_sha256": SHA_B,
        "generator_id": "stack.test.metric",
        "generator_sha256": SHA_A,
    }


def observed(defn: dict, value: dict) -> dict:
    return make_observation(
        definition=defn,
        subject_id="fixture",
        subject_sha256=SHA_C,
        sequence_index=0,
        status="observed",
        value=value,
        reason=None,
        uncertainty_kind="exact",
        provenance=provenance(),
    )


def structure(
    *,
    structure_id: str,
    order: tuple[str, str] = ("left", "right"),
    multiplicity: int = 2,
    left_provenance: str = SHA_A,
) -> dict:
    return seal_structure(
        structure_id=structure_id,
        scale="test-scale",
        participants=(
            {"identity": "left", "provenance_sha256": left_provenance},
            {"identity": "right", "provenance_sha256": SHA_B},
        ),
        relations=(
            {
                "identity": "pair",
                "kind": "ordered-pair",
                "ordered_participants": list(order),
                "multiplicity": multiplicity,
            },
        ),
    )


class MetricProtocolTests(unittest.TestCase):
    def test_missing_value_field_is_rejected_before_any_default(self) -> None:
        defn = definition()
        record = observed(defn, boolean_value(False))
        del record["value"]

        with self.assertRaisesRegex(MetricProtocolError, "missing required fields: value"):
            validate_observation(record, defn)

    def test_non_observed_value_requires_explicit_null_and_reason(self) -> None:
        defn = definition()
        unresolved = make_observation(
            definition=defn,
            subject_id="fixture",
            subject_sha256=SHA_C,
            sequence_index=0,
            status="unresolved",
            value=None,
            reason="hmmm: source observation unavailable",
            uncertainty_kind="not_quantified",
            provenance=provenance(),
        )
        self.assertIsNone(unresolved["value"])

        wrong = deepcopy(unresolved)
        wrong["value"] = boolean_value(False)
        wrong["observation_sha256"] = sha256_json(
            {key: value for key, value in wrong.items() if key != "observation_sha256"}
        )
        with self.assertRaisesRegex(MetricProtocolError, "must be explicit null"):
            validate_observation(wrong, defn)

    def test_boolean_and_integer_encodings_do_not_alias(self) -> None:
        with self.assertRaisesRegex(MetricProtocolError, "must be a boolean"):
            boolean_value(1)  # type: ignore[arg-type]
        with self.assertRaisesRegex(MetricProtocolError, "exact Fraction or integer"):
            rational_value(True)

        defn = definition()
        wrong = observed(defn, boolean_value(True))
        wrong["value"]["value"] = 1
        wrong["observation_sha256"] = sha256_json(
            {key: value for key, value in wrong.items() if key != "observation_sha256"}
        )
        with self.assertRaisesRegex(MetricProtocolError, "must be a boolean"):
            validate_observation(wrong, defn)

    def test_float_is_rejected_everywhere(self) -> None:
        defn = definition(kind="rational")
        record = observed(defn, rational_value(Fraction(1, 2)))
        record["value"] = {"kind": "rational", "numerator": 0.5, "denominator": 1}
        with self.assertRaisesRegex(MetricProtocolError, "must be an integer"):
            validate_observation(record, defn)
        with self.assertRaisesRegex(MetricProtocolError, "floating-point"):
            canonical_json({"value": 0.0})

    def test_relation_order_and_multiplicity_are_measured(self) -> None:
        before = structure(structure_id="before")
        after = structure(
            structure_id="after",
            order=("right", "left"),
            multiplicity=1,
        )
        _definitions, observations = measure_retention(
            before,
            after,
            provenance=provenance(),
            computation_sha256=SHA_A,
        )
        relation_value = observations[1]["value"]
        self.assertEqual(relation_value, rational_value(0))

        same_order = structure(structure_id="after-same-order", multiplicity=1)
        _definitions, observations = measure_retention(
            before,
            same_order,
            provenance=provenance(),
            computation_sha256=SHA_A,
        )
        self.assertEqual(observations[1]["value"], rational_value(Fraction(1, 2)))

    def test_provenance_change_is_not_retained(self) -> None:
        before = structure(structure_id="before")
        after = structure(structure_id="after", left_provenance=SHA_C)
        _definitions, observations = measure_retention(
            before,
            after,
            provenance=provenance(),
            computation_sha256=SHA_A,
        )
        self.assertEqual(observations[0]["value"], rational_value(1))
        self.assertEqual(observations[2]["value"], boolean_value(False))

    def test_receipt_is_byte_deterministic_and_tamper_evident(self) -> None:
        defn = definition()
        observation = observed(defn, boolean_value(True))
        binding = {
            "kind": "test-binding",
            "identity": "test",
            "version": "0.1.0",
            "repository": "The-Interdependency/stack",
            "commit": COMMIT_A,
            "artifact_sha256": SHA_A,
            "record_digest": SHA_B,
            "authority_transfer": False,
            "measurement_status_transfer": False,
        }
        kwargs = {
            "work_graph_sha256": WORK_GRAPH_SHA,
            "definitions": [defn],
            "observations": [observation],
            "bindings": [binding],
            "inputs": [{"identity": "fixture", "sha256": SHA_C}],
            "verifier_id": "stack.test.verifier",
            "verifier_sha256": SHA_A,
            "hmmm": [],
        }
        first = seal_receipt(**kwargs)
        second = seal_receipt(**kwargs)
        self.assertEqual(canonical_json(first), canonical_json(second))

        tampered = deepcopy(first)
        tampered["observations"][0]["value"] = boolean_value(False)
        with self.assertRaisesRegex(MetricProtocolError, "observation digest mismatch"):
            verify_receipt(tampered)

    def test_binding_status_transfer_must_remain_false(self) -> None:
        defn = definition()
        observation = observed(defn, boolean_value(True))
        binding = {
            "kind": "test-binding",
            "identity": "test",
            "version": "0.1.0",
            "repository": "The-Interdependency/stack",
            "commit": COMMIT_A,
            "artifact_sha256": SHA_A,
            "record_digest": SHA_B,
            "authority_transfer": True,
            "measurement_status_transfer": False,
        }
        with self.assertRaisesRegex(MetricProtocolError, "authority_transfer must be false"):
            seal_receipt(
                work_graph_sha256=WORK_GRAPH_SHA,
                definitions=[defn],
                observations=[observation],
                bindings=[binding],
                inputs=[{"identity": "fixture", "sha256": SHA_C}],
                verifier_id="stack.test.verifier",
                verifier_sha256=SHA_A,
                hmmm=[],
            )


    def test_generator_rejects_wrong_checkout_commit(self) -> None:
        participant = {
            "repository": "The-Interdependency/stack",
            "commit": "0" * 40,
        }
        with self.assertRaisesRegex(ProducerIdentityError, "checkout is not at"):
            verify_checkout(WORKSPACE.parents[1], participant, ("README.md",))

    def test_frozen_receipt_preserves_metapat_nontransfer(self) -> None:
        receipt_path = WORKSPACE / "receipts/native-mobius-v0.json"
        receipt = verify_receipt(json.loads(receipt_path.read_text(encoding="utf-8")))
        binding = next(
            item for item in receipt["bindings"]
            if item["identity"] == "metapat.application.affixiation_harmonics"
        )
        self.assertEqual(binding["version"], "affixiation-harmonics-application-v4")
        self.assertIs(binding["authority_transfer"], False)
        self.assertIs(binding["measurement_status_transfer"], False)

    def test_frozen_receipt_records_native_ucns_transition(self) -> None:
        receipt_path = WORKSPACE / "receipts/native-mobius-v0.json"
        receipt = verify_receipt(json.loads(receipt_path.read_text(encoding="utf-8")))
        values = {
            item["metric_id"]: item["value"]["value"]
            for item in receipt["observations"]
            if item["metric_id"].startswith("stack.observation.ucns.")
        }
        self.assertEqual(
            values,
            {
                "stack.observation.ucns.visible_return_after_one_turn": True,
                "stack.observation.ucns.complete_return_after_one_turn": False,
                "stack.observation.ucns.complete_return_after_two_turns": True,
                "stack.observation.ucns.exact_inverse_round_trip": True,
            },
        )

if __name__ == "__main__":
    unittest.main()
