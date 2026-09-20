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
# id: check_digital_metric_typed_source_revision
#   proves: digital_metric_provenance_revision_is_typed
#   call: self::test_candidate_content_revision_must_match_artifact
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
# id: check_digital_metric_replay_attestation
#   proves: digital_metric_pass_requires_completed_replay
#   call: self::test_pass_is_created_only_by_post_replay_attestation
#   mutates: temporary directory only
#   cleanup: automatic temporary-directory cleanup
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
# id: check_digital_metric_metapat_import_origin
#   proves: digital_metric_generator_imports_verified_metapat
#   call: self::test_metapat_loader_ignores_and_restores_cached_module
#   mutates: temporary directory and process import cache
#   cleanup: automatic temporary-directory cleanup and explicit cache restoration
#
# id: check_digital_metric_bytecode_bypass
#   proves: digital_metric_generator_bypasses_cached_bytecode
#   call: self::test_producer_loaders_ignore_matching_stale_bytecode
#   mutates: temporary directory only
#   cleanup: automatic temporary-directory cleanup
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
from importlib.util import cache_from_source
from pathlib import Path
from tempfile import TemporaryDirectory
from types import ModuleType
import json
import os
import py_compile
import sys
import unittest
from unittest.mock import patch


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


import verify_receipt as receipt_replay  # noqa: E402
from generate_receipt import (  # noqa: E402
    ProducerIdentityError,
    _load_metapat_application,
    _load_ucns_native_module,
    verify_checkout,
)
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
        "source_revision": {"kind": "git-commit", "value": COMMIT_A},
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
    @staticmethod
    def _install_timestamp_valid_stale_bytecode(
        source_path: Path,
        *,
        poisoned_source: str,
        verified_source: str,
    ) -> Path:
        if len(poisoned_source.encode("utf-8")) != len(verified_source.encode("utf-8")):
            raise AssertionError("matched bytecode fixture sources must have equal byte length")
        fixed_timestamp = 1_700_000_000
        source_path.write_text(poisoned_source, encoding="utf-8")
        os.utime(source_path, (fixed_timestamp, fixed_timestamp))
        bytecode_path = Path(cache_from_source(str(source_path)))
        bytecode_path.parent.mkdir(parents=True, exist_ok=True)
        py_compile.compile(
            str(source_path),
            cfile=str(bytecode_path),
            doraise=True,
            invalidation_mode=py_compile.PycInvalidationMode.TIMESTAMP,
        )
        source_path.write_text(verified_source, encoding="utf-8")
        os.utime(source_path, (fixed_timestamp, fixed_timestamp))
        return bytecode_path

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

    def test_candidate_content_revision_must_match_artifact(self) -> None:
        defn = definition()
        candidate_provenance = provenance()
        candidate_provenance["source_revision"] = {
            "kind": "candidate-content",
            "value": SHA_C,
        }
        with self.assertRaisesRegex(
            MetricProtocolError,
            "candidate-content revision must equal source artifact digest",
        ):
            make_observation(
                definition=defn,
                subject_id="fixture",
                subject_sha256=SHA_C,
                sequence_index=0,
                status="observed",
                value=boolean_value(True),
                reason=None,
                uncertainty_kind="exact",
                provenance=candidate_provenance,
            )

        candidate_provenance["source_revision"]["value"] = SHA_B
        record = observed(defn, boolean_value(True))
        record["provenance"] = candidate_provenance
        record["observation_sha256"] = sha256_json(
            {key: value for key, value in record.items() if key != "observation_sha256"}
        )
        validate_observation(record, defn)

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

    def test_pass_is_created_only_by_post_replay_attestation(self) -> None:
        defn = definition()
        observation = observed(defn, boolean_value(True))
        candidate = seal_receipt(
            work_graph_sha256=WORK_GRAPH_SHA,
            definitions=[defn],
            observations=[observation],
            bindings=[
                {
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
            ],
            inputs=[{"identity": "fixture", "sha256": SHA_C}],
            verifier_id="stack.test.verifier",
            verifier_sha256=SHA_A,
            hmmm=[],
        )
        self.assertEqual(candidate["verification"]["result"], "pending")

        with TemporaryDirectory() as directory:
            root = Path(directory)
            pending_path = root / "pending.json"
            attested_path = root / "attested.json"
            pending_path.write_text(canonical_json(candidate) + "\n", encoding="utf-8")
            with patch.object(receipt_replay, "build_receipt", return_value=candidate):
                attested = receipt_replay.verify_and_replay(
                    pending_path,
                    metapat_root=root,
                    ucns_root=root,
                    work_graph_path=root / "WORK_GRAPH.json",
                    attest_output=attested_path,
                )
                self.assertEqual(attested["verification"]["result"], "pass")
                self.assertEqual(
                    attested_path.read_text(encoding="utf-8"),
                    canonical_json(attested) + "\n",
                )
                replayed = receipt_replay.verify_and_replay(
                    attested_path,
                    metapat_root=root,
                    ucns_root=root,
                    work_graph_path=root / "WORK_GRAPH.json",
                )
                self.assertEqual(replayed, attested)
                with self.assertRaisesRegex(MetricProtocolError, "attestation input must be pending"):
                    receipt_replay.verify_and_replay(
                        attested_path,
                        metapat_root=root,
                        ucns_root=root,
                        work_graph_path=root / "WORK_GRAPH.json",
                        attest_output=root / "second.json",
                    )

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

    def test_metapat_loader_ignores_and_restores_cached_module(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            package = root / "src/metapat"
            documents = root / "docs/applications"
            package.mkdir(parents=True)
            documents.mkdir(parents=True)
            (package / "__init__.py").write_text("", encoding="utf-8")
            (package / "affixiation_harmonics.py").write_text(
                "class _Application:\n"
                "    application_id = 'metapat.application.affixiation_harmonics'\n"
                "    application_version = 'affixiation-harmonics-application-v4'\n"
                "    measurement_validity_claim = False\n"
                "    ucns_theorem_status_transfer = False\n"
                "\n"
                "def affixiation_harmonics_application_module():\n"
                "    return _Application()\n",
                encoding="utf-8",
            )
            (documents / "affixiation-harmonics.md").write_text(
                "verified fixture\n",
                encoding="utf-8",
            )

            cached_package = ModuleType("metapat")
            cached_package.__path__ = []  # type: ignore[attr-defined]
            cached_module = ModuleType("metapat.affixiation_harmonics")
            cached_module.affixiation_harmonics_application_module = (  # type: ignore[attr-defined]
                lambda: object()
            )
            with patch.dict(
                sys.modules,
                {
                    "metapat": cached_package,
                    "metapat.affixiation_harmonics": cached_module,
                },
                clear=False,
            ):
                application, document_sha256 = _load_metapat_application(root)
                self.assertEqual(
                    application.application_id,
                    "metapat.application.affixiation_harmonics",
                )
                self.assertEqual(len(document_sha256), 64)
                self.assertIs(sys.modules["metapat"], cached_package)
                self.assertIs(
                    sys.modules["metapat.affixiation_harmonics"],
                    cached_module,
                )

    def test_producer_loaders_ignore_matching_stale_bytecode(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            metapat_package = root / "metapat/src/metapat"
            metapat_documents = root / "metapat/docs/applications"
            metapat_package.mkdir(parents=True)
            metapat_documents.mkdir(parents=True)
            (metapat_package / "__init__.py").write_text("", encoding="utf-8")
            metapat_module = metapat_package / "affixiation_harmonics.py"
            metapat_template = (
                "class _Application:\n"
                "    application_id = 'metapat.application.affixiation_harmonics'\n"
                "    application_version = 'affixiation-harmonics-application-v4'\n"
                "    measurement_validity_claim = False\n"
                "    ucns_theorem_status_transfer = False\n"
                "    marker = {marker!r}\n"
                "\n"
                "def affixiation_harmonics_application_module():\n"
                "    return _Application()\n"
            )
            metapat_bytecode = self._install_timestamp_valid_stale_bytecode(
                metapat_module,
                poisoned_source=metapat_template.format(marker="cached"),
                verified_source=metapat_template.format(marker="source"),
            )
            (metapat_documents / "affixiation-harmonics.md").write_text(
                "verified fixture\n",
                encoding="utf-8",
            )
            application, _digest = _load_metapat_application(root / "metapat")
            self.assertTrue(metapat_bytecode.is_file())
            self.assertEqual(application.marker, "source")

            ucns_package = root / "ucns/src/ucns"
            ucns_package.mkdir(parents=True)
            ucns_module = ucns_package / "direct_mobius.py"
            ucns_bytecode = self._install_timestamp_valid_stale_bytecode(
                ucns_module,
                poisoned_source="VALUE = 'cached'\n",
                verified_source="VALUE = 'source'\n",
            )
            module, _digest = _load_ucns_native_module(root / "ucns")
            self.assertTrue(ucns_bytecode.is_file())
            self.assertEqual(module.VALUE, "source")

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
