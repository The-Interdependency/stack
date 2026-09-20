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
# id: check_digital_metric_replay_bytecode_bypass
#   proves: digital_metric_verifier_bypasses_cached_bytecode
#   call: self::test_replay_modules_ignore_matching_stale_bytecode
#   mutates: temporary directory only
#   cleanup: automatic temporary-directory cleanup
#
# id: check_digital_metric_nontransfer
#   proves: digital_metric_status_does_not_transfer
#   call: self::test_binding_status_transfer_must_remain_false
#   mutates: none
#   cleanup: none
#
# id: check_digital_metric_source_bound_generator_entry
#   proves: digital_metric_generator_requires_source_bound_entry
#   call: self::test_normal_imported_generator_cannot_generate
#   mutates: none
#   cleanup: none
#
# id: check_digital_metric_exact_producer_gate
#   proves: digital_metric_generator_requires_exact_clean_producers
#   call: self::test_generator_rejects_wrong_checkout_commit
#   mutates: none
#   cleanup: none
#
# id: check_digital_metric_exact_producer_root
#   proves: digital_metric_generator_requires_exact_clean_producers
#   call: self::test_generator_rejects_nested_producer_root
#   mutates: temporary directory only
#   cleanup: automatic temporary-directory cleanup
#
# id: check_digital_metric_fixed_participant_set
#   proves: digital_metric_work_graph_requires_fixed_participants
#   call: self::test_work_graph_requires_complete_fixed_participant_set
#   mutates: temporary directory only
#   cleanup: automatic temporary-directory cleanup
#
# id: check_digital_metric_metapat_import_origin
#   proves: digital_metric_generator_imports_verified_metapat
#   call: self::test_metapat_loader_ignores_and_restores_cached_module
#   mutates: temporary directory and process import cache
#   cleanup: automatic temporary-directory cleanup and explicit cache restoration
#
# id: check_digital_metric_committed_source_only
#   proves: digital_metric_generator_loads_committed_sources_only
#   call: self::test_metapat_loader_ignores_untracked_package_shadow
#   mutates: temporary Git repository only
#   cleanup: automatic temporary-directory cleanup
#
# id: check_digital_metric_bytecode_bypass
#   proves: digital_metric_generator_bypasses_cached_bytecode
#   call: self::test_producer_loaders_ignore_matching_stale_bytecode
#   mutates: temporary directory only
#   cleanup: automatic temporary-directory cleanup
#
# id: check_digital_metric_git_replacement_bypass
#   proves: digital_metric_generator_ignores_git_replacements
#   call: self::test_producer_reads_ignore_git_replacement_objects
#   mutates: temporary Git repository only
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
#
# id: check_digital_metric_committed_blob_only
#   proves: digital_metric_generator_loads_committed_sources_only
#   call: self::test_metapat_loader_uses_committed_dependency_blob
#   mutates: temporary Git repository only
#   cleanup: automatic temporary-directory cleanup
#
# id: check_digital_metric_loaded_digest_binding
#   proves: digital_metric_replay_binds_executing_source_bytes,digital_metric_cli_binds_loaded_verifier_bytes,digital_metric_generator_cli_binds_loaded_bytes
#   call: self::test_replay_digests_bind_loaded_source_bytes
#   mutates: temporary directory only
#   cleanup: automatic temporary-directory cleanup
#
# id: check_digital_metric_discoverable_test_gate
#   proves: digital_metric_contract_audit_requires_discoverable_tests
#   call: self::test_contract_audit_rejects_undiscoverable_check_targets
#   mutates: temporary directory only
#   cleanup: automatic temporary-directory cleanup
#
# id: check_digital_metric_source_bound_verifier_entry
#   proves: digital_metric_verifier_requires_source_bound_entry
#   call: self::test_normal_imported_verifier_cannot_attest
#   mutates: none
#   cleanup: none
#
# === END CHECKS ===

from copy import deepcopy
from fractions import Fraction
from importlib.util import cache_from_source
from pathlib import Path
import subprocess
from tempfile import TemporaryDirectory
from types import ModuleType
import hashlib
import json
import os
import py_compile
import sys
import unittest
from unittest.mock import patch


WORKSPACE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(WORKSPACE))
sys.path.insert(0, str(WORKSPACE.parents[1] / "skill-lib"))


def _source_load_module(module_name: str, source_path: Path) -> ModuleType:
    source = source_path.read_bytes()
    module = ModuleType(module_name)
    module.__file__ = str(source_path)
    module.__cached__ = None
    module.__package__ = ""
    module.__source_sha256__ = hashlib.sha256(source).hexdigest()
    previous = sys.modules.get(module_name)
    sys.modules[module_name] = module
    try:
        exec(
            compile(source, str(source_path), "exec", dont_inherit=True),
            module.__dict__,
        )
    finally:
        if previous is None:
            sys.modules.pop(module_name, None)
        else:
            sys.modules[module_name] = previous
    return module


from metric_protocol import (  # noqa: E402
    MetricProtocolError,
    boolean_value,
    canonical_json,
    make_metric_definition,
    make_observation,
    measure_retention,
    rational_value,
    integer_value,
    seal_receipt,
    seal_structure,
    sha256_json,
    validate_observation,
    verify_receipt,
)
import audit_contracts as contract_audit  # noqa: E402


generator_cli = _source_load_module(  # noqa: E402
    "_test_stack_metric_generator_cli",
    WORKSPACE / "generate_receipt_cli.py",
)
receipt_replay = _source_load_module(  # noqa: E402
    "_test_stack_metric_receipt_replay",
    WORKSPACE / "verify_receipt.py",
)
receipt_cli = _source_load_module(  # noqa: E402
    "_test_stack_metric_receipt_cli",
    WORKSPACE / "verify_receipt_cli.py",
)
from generate_receipt import (  # noqa: E402
    ProducerIdentityError,
    _execution_source_digests,
    load_work_graph,
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

    @staticmethod
    def _commit_fixture_repo(root: Path) -> None:
        subprocess.run(
            ["git", "init", "-q", str(root)],
            check=True,
        )
        subprocess.run(
            ["git", "-C", str(root), "add", "."],
            check=True,
        )
        subprocess.run(
            [
                "git",
                "-C",
                str(root),
                "-c",
                "user.name=fixture",
                "-c",
                "user.email=fixture@example.invalid",
                "commit",
                "-q",
                "-m",
                "fixture",
            ],
            check=True,
        )

    @staticmethod
    def _head(root: Path) -> str:
        return subprocess.run(
            ["git", "-C", str(root), "rev-parse", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()

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

        whitespace_reason = deepcopy(unresolved)
        whitespace_reason["reason"] = "   "
        whitespace_reason["observation_sha256"] = sha256_json(
            {
                key: value
                for key, value in whitespace_reason.items()
                if key != "observation_sha256"
            }
        )
        with self.assertRaisesRegex(MetricProtocolError, "non-empty string"):
            validate_observation(whitespace_reason, defn)

    def test_boolean_and_integer_encodings_do_not_alias(self) -> None:
        with self.assertRaisesRegex(MetricProtocolError, "must be a boolean"):
            boolean_value(1)  # type: ignore[arg-type]
        with self.assertRaisesRegex(MetricProtocolError, "must be an integer"):
            integer_value(True)  # type: ignore[arg-type]
        with self.assertRaisesRegex(MetricProtocolError, "exact Fraction or integer"):
            rational_value(True)

        integer_definition = definition(kind="integer")
        self.assertEqual(integer_definition["value_contract"]["minimum"], integer_value(0))
        integer_record = observed(integer_definition, integer_value(1))
        self.assertEqual(integer_record["value"], {"kind": "integer", "value": 1})

        wrong_integer = deepcopy(integer_record)
        wrong_integer["value"] = {"kind": "rational", "value": 1}
        wrong_integer["observation_sha256"] = sha256_json(
            {key: value for key, value in wrong_integer.items() if key != "observation_sha256"}
        )
        with self.assertRaisesRegex(MetricProtocolError, "kind must be 'integer'"):
            validate_observation(wrong_integer, integer_definition)

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
                with self.assertRaisesRegex(
                    receipt_replay.MetricProtocolError,
                    "attestation input must be pending",
                ):
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

    def test_generator_rejects_nested_producer_root(self) -> None:
        repository_root = WORKSPACE.parents[1]
        with TemporaryDirectory(dir=repository_root) as directory:
            participant = {
                "repository": "The-Interdependency/stack",
                "commit": "0" * 40,
            }
            with self.assertRaisesRegex(ProducerIdentityError, "not the Git top level"):
                verify_checkout(Path(directory), participant, ())

    def test_work_graph_requires_complete_fixed_participant_set(self) -> None:
        graph = json.loads((WORKSPACE / "WORK_GRAPH.json").read_text(encoding="utf-8"))
        graph["participants"] = graph["participants"][:-1]
        graph["work_graph_sha256"] = sha256_json(
            {
                "participants": graph["participants"],
                "boundaries": graph["boundaries"],
            }
        )
        with TemporaryDirectory() as directory:
            graph_path = Path(directory) / "WORK_GRAPH.json"
            graph_path.write_text(canonical_json(graph) + "\n", encoding="utf-8")
            with self.assertRaisesRegex(ProducerIdentityError, "exact ordered v0 participant set"):
                load_work_graph(graph_path)

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
            self._commit_fixture_repo(root)
            commit = self._head(root)

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
                application, document_sha256 = _load_metapat_application(root, commit)
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

    def test_metapat_loader_ignores_untracked_package_shadow(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            package = root / "src/metapat"
            documents = root / "docs/applications"
            package.mkdir(parents=True)
            documents.mkdir(parents=True)
            (package / "__init__.py").write_text("", encoding="utf-8")
            (package / "application.py").write_text("MARKER = 'source'\n", encoding="utf-8")
            (package / "affixiation_harmonics.py").write_text(
                "from .application import MARKER\n"
                "class _Application:\n"
                "    application_id = 'metapat.application.affixiation_harmonics'\n"
                "    application_version = 'affixiation-harmonics-application-v4'\n"
                "    measurement_validity_claim = False\n"
                "    ucns_theorem_status_transfer = False\n"
                "    marker = MARKER\n"
                "\n"
                "def affixiation_harmonics_application_module():\n"
                "    return _Application()\n",
                encoding="utf-8",
            )
            (documents / "affixiation-harmonics.md").write_text(
                "verified fixture\n",
                encoding="utf-8",
            )
            self._commit_fixture_repo(root)
            commit = self._head(root)
            shadow = package / "application"
            shadow.mkdir()
            (shadow / "__init__.py").write_text("MARKER = 'cached'\n", encoding="utf-8")
            application, _digest = _load_metapat_application(root, commit)
            self.assertTrue((shadow / "__init__.py").is_file())
            self.assertEqual(application.marker, "source")

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
            metapat_module.write_text(
                metapat_template.format(marker="source"),
                encoding="utf-8",
            )
            (metapat_documents / "affixiation-harmonics.md").write_text(
                "verified fixture\n",
                encoding="utf-8",
            )
            self._commit_fixture_repo(root / "metapat")
            metapat_commit = self._head(root / "metapat")
            metapat_bytecode = self._install_timestamp_valid_stale_bytecode(
                metapat_module,
                poisoned_source=metapat_template.format(marker="cached"),
                verified_source=metapat_template.format(marker="source"),
            )
            application, _digest = _load_metapat_application(
                root / "metapat", metapat_commit
            )
            self.assertTrue(metapat_bytecode.is_file())
            self.assertEqual(application.marker, "source")

            ucns_package = root / "ucns/src/ucns"
            ucns_package.mkdir(parents=True)
            ucns_module = ucns_package / "direct_mobius.py"
            ucns_module.write_text("VALUE = 'source'\n", encoding="utf-8")
            self._commit_fixture_repo(root / "ucns")
            ucns_commit = self._head(root / "ucns")
            ucns_bytecode = self._install_timestamp_valid_stale_bytecode(
                ucns_module,
                poisoned_source="VALUE = 'cached'\n",
                verified_source="VALUE = 'source'\n",
            )
            module, _digest = _load_ucns_native_module(root / "ucns", ucns_commit)
            self.assertTrue(ucns_bytecode.is_file())
            self.assertEqual(module.VALUE, "source")

    def test_replay_modules_ignore_matching_stale_bytecode(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            verifier_path = root / "verify_receipt.py"
            generator_path = root / "generate_receipt.py"
            protocol_path = root / "metric_protocol.py"
            verified_verifier = (WORKSPACE / "verify_receipt.py").read_text(
                encoding="utf-8"
            )
            verifier_path.write_text(verified_verifier, encoding="utf-8")
            verified_protocol = (
                "class MetricProtocolError(ValueError):\n"
                "    pass\n"
                "\n"
                "def _marker(*args, **kwargs):\n"
                "    return 'source'\n"
                "\n"
                "boolean_value = _marker\n"
                "canonical_json = _marker\n"
                "make_metric_definition = _marker\n"
                "make_observation = _marker\n"
                "measure_retention = _marker\n"
                "seal_receipt = _marker\n"
                "seal_structure = _marker\n"
                "sha256_json = _marker\n"
                "verify_receipt = _marker\n"
            )
            protocol_bytecode = self._install_timestamp_valid_stale_bytecode(
                protocol_path,
                poisoned_source=verified_protocol.replace("'source'", "'cached'"),
                verified_source=verified_protocol,
            )
            verified_generator = (WORKSPACE / "generate_receipt.py").read_text(
                encoding="utf-8"
            )
            poison_prefix = "def build_receipt(*args, **kwargs):\n    return 'cached'\n"
            padding_size = len(verified_generator.encode("utf-8")) - len(poison_prefix) - 1
            self.assertGreater(padding_size, 0)
            poison_generator = poison_prefix + ("#" * padding_size) + "\n"
            generator_bytecode = self._install_timestamp_valid_stale_bytecode(
                generator_path,
                poisoned_source=poison_generator,
                verified_source=verified_generator,
            )
            verifier_poison_prefix = (
                "def verify_and_replay(*args, **kwargs):\n"
                "    return 'cached'\n"
            )
            verifier_padding_size = (
                len(verified_verifier.encode("utf-8"))
                - len(verifier_poison_prefix.encode("utf-8"))
                - 1
            )
            self.assertGreater(verifier_padding_size, 0)
            verifier_bytecode = self._install_timestamp_valid_stale_bytecode(
                verifier_path,
                poisoned_source=(
                    verifier_poison_prefix + ("#" * verifier_padding_size) + "\n"
                ),
                verified_source=verified_verifier,
            )
            loaded_generator = generator_cli._load_generator(generator_path)
            self.assertEqual(loaded_generator.boolean_value(), "source")
            loaded_verifier = receipt_cli._load_verifier(verifier_path)
            self.assertTrue(protocol_bytecode.is_file())
            self.assertTrue(generator_bytecode.is_file())
            self.assertTrue(verifier_bytecode.is_file())
            self.assertEqual(loaded_verifier.canonical_json(None), "source")
            with self.assertRaises(TypeError):
                loaded_verifier.build_receipt()

    def test_metapat_loader_uses_committed_dependency_blob(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            package = root / "src/metapat"
            documents = root / "docs/applications"
            package.mkdir(parents=True)
            documents.mkdir(parents=True)
            (package / "__init__.py").write_text("", encoding="utf-8")
            dependency = package / "catalog_data.py"
            dependency.write_text("MARKER = 'committed'\n", encoding="utf-8")
            (package / "affixiation_harmonics.py").write_text(
                "from .catalog_data import MARKER\n"
                "class _Application:\n"
                "    application_id = 'metapat.application.affixiation_harmonics'\n"
                "    application_version = 'affixiation-harmonics-application-v4'\n"
                "    measurement_validity_claim = False\n"
                "    ucns_theorem_status_transfer = False\n"
                "    marker = MARKER\n"
                "\n"
                "def affixiation_harmonics_application_module():\n"
                "    return _Application()\n",
                encoding="utf-8",
            )
            (documents / "affixiation-harmonics.md").write_text(
                "verified fixture\n",
                encoding="utf-8",
            )
            self._commit_fixture_repo(root)
            pinned_commit = self._head(root)
            subprocess.run(
                [
                    "git", "-C", str(root), "update-index", "--assume-unchanged",
                    "src/metapat/catalog_data.py",
                ],
                check=True,
            )
            dependency.write_text("MARKER = 'altered'\n", encoding="utf-8")
            status = subprocess.run(
                ["git", "-C", str(root), "status", "--porcelain", "--untracked-files=no"],
                check=True,
                capture_output=True,
                text=True,
            )
            self.assertEqual(status.stdout, "")
            application, _digest = _load_metapat_application(root, pinned_commit)
            self.assertEqual(application.marker, "committed")

            subprocess.run(
                [
                    "git", "-C", str(root), "update-index", "--no-assume-unchanged",
                    "src/metapat/catalog_data.py",
                ],
                check=True,
            )
            self._commit_fixture_repo(root)
            self.assertNotEqual(self._head(root), pinned_commit)
            application, _digest = _load_metapat_application(root, pinned_commit)
            self.assertEqual(application.marker, "committed")

    def test_producer_reads_ignore_git_replacement_objects(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            package = root / "src/metapat"
            documents = root / "docs/applications"
            package.mkdir(parents=True)
            documents.mkdir(parents=True)
            (package / "__init__.py").write_text("", encoding="utf-8")
            dependency = package / "catalog_data.py"
            dependency.write_text("MARKER = 'original'\n", encoding="utf-8")
            (package / "affixiation_harmonics.py").write_text(
                "from .catalog_data import MARKER\n"
                "class _Application:\n"
                "    application_id = 'metapat.application.affixiation_harmonics'\n"
                "    application_version = 'affixiation-harmonics-application-v4'\n"
                "    measurement_validity_claim = False\n"
                "    ucns_theorem_status_transfer = False\n"
                "    marker = MARKER\n"
                "    application_digest = 'a' * 64\n"
                "    def to_dict(self): return {'marker': self.marker}\n"
                "\n"
                "def affixiation_harmonics_application_module():\n"
                "    return _Application()\n",
                encoding="utf-8",
            )
            (documents / "affixiation-harmonics.md").write_text(
                "original fixture\n",
                encoding="utf-8",
            )
            self._commit_fixture_repo(root)
            pinned_commit = self._head(root)
            dependency.write_text("MARKER = 'replaced'\n", encoding="utf-8")
            self._commit_fixture_repo(root)
            replacement_commit = self._head(root)
            subprocess.run(
                ["git", "-C", str(root), "replace", pinned_commit, replacement_commit],
                check=True,
            )
            replaced_blob = subprocess.run(
                [
                    "git", "-C", str(root), "show",
                    f"{pinned_commit}:src/metapat/catalog_data.py",
                ],
                check=True,
                capture_output=True,
                text=True,
            ).stdout
            self.assertIn("replaced", replaced_blob)
            application, _digest = _load_metapat_application(root, pinned_commit)
            self.assertEqual(application.marker, "original")

    def test_replay_digests_bind_loaded_source_bytes(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            paths = {
                name: root / name
                for name in ("metric_protocol.py", "generate_receipt.py", "verify_receipt.py")
            }
            for name, path in paths.items():
                path.write_bytes((WORKSPACE / name).read_bytes())
            expected = {
                name: hashlib.sha256(path.read_bytes()).hexdigest()
                for name, path in paths.items()
            }
            loaded_generator = generator_cli._load_generator(
                paths["generate_receipt.py"]
            )
            loaded = receipt_cli._load_verifier(paths["verify_receipt.py"])
            self.assertEqual(
                loaded_generator._LOADED_GENERATOR_SHA256,
                expected["generate_receipt.py"],
            )
            self.assertEqual(
                loaded._METRIC_PROTOCOL.__source_sha256__,
                loaded._GENERATOR._LOADED_PROTOCOL_SHA256,
            )
            for path in paths.values():
                path.write_text("# changed after load\n", encoding="utf-8")
            actual = loaded._GENERATOR._execution_source_digests(
                verifier_path=paths["verify_receipt.py"],
                verifier_sha256=loaded._LOADED_VERIFIER_SHA256,
            )
            expected_digests = {
                "generator": expected["generate_receipt.py"],
                "protocol": expected["metric_protocol.py"],
                "verifier": expected["verify_receipt.py"],
            }
            self.assertEqual(actual, expected_digests)
            self.assertEqual(
                loaded_generator._execution_source_digests(
                    verifier_path=paths["verify_receipt.py"],
                    verifier_sha256=expected["verify_receipt.py"],
                ),
                expected_digests,
            )
            self.assertNotEqual(
                hashlib.sha256(paths["generate_receipt.py"].read_bytes()).hexdigest(),
                actual["generator"],
            )

    def test_normal_imported_generator_cannot_generate(self) -> None:
        with self.assertRaisesRegex(
            ProducerIdentityError,
            "generator API must be source-loaded",
        ):
            _execution_source_digests(
                verifier_path=WORKSPACE / "verify_receipt.py"
            )

    def test_normal_imported_verifier_cannot_attest(self) -> None:
        source_path = WORKSPACE / "verify_receipt.py"
        source = source_path.read_bytes()
        module = ModuleType("_test_normal_imported_verifier")
        module.__file__ = str(source_path)
        module.__cached__ = None
        module.__package__ = ""
        exec(
            compile(source, str(source_path), "exec", dont_inherit=True),
            module.__dict__,
        )
        with self.assertRaisesRegex(
            module.MetricProtocolError,
            "verifier API must be source-loaded",
        ):
            module.verify_and_replay(
                Path("missing"),
                metapat_root=Path("."),
                ucns_root=Path("."),
                work_graph_path=WORKSPACE / "WORK_GRAPH.json",
            )

    def test_contract_audit_rejects_undiscoverable_check_targets(self) -> None:
        source_text = (
            "# === CONTRACTS ===\n"
            "# id: fixture_contract\n"
            "#   given: a fixture\n"
            "#   then: it is witnessed\n"
            "#   class: provenance\n"
            "# === END CONTRACTS ===\n"
        )
        check_header = (
            "# === CHECKS ===\n"
            "# id: fixture_check\n"
            "#   proves: fixture_contract\n"
            "#   call: self::test_hidden\n"
            "#   mutates: none\n"
            "#   cleanup: none\n"
            "# === END CHECKS ===\n"
        )
        hidden_forms = (
            "def test_hidden():\n    pass\n",
            "class Helper:\n    def test_hidden(self):\n        pass\n",
            (
                "import unittest\n"
                "def outer():\n"
                "    class Hidden(unittest.TestCase):\n"
                "        def test_hidden(self):\n"
                "            pass\n"
                "    return Hidden\n"
            ),
            (
                "import unittest\n"
                "class AsyncWrong(unittest.TestCase):\n"
                "    async def test_hidden(self):\n"
                "        pass\n"
            ),
            (
                "import unittest\n"
                "@unittest.skip('disabled')\n"
                "class Skipped(unittest.TestCase):\n"
                "    def test_hidden(self):\n"
                "        pass\n"
            ),
            (
                "import unittest\n"
                "class SkippedMethod(unittest.TestCase):\n"
                "    @unittest.skipIf(True, 'disabled')\n"
                "    def test_hidden(self):\n"
                "        pass\n"
            ),
            (
                "from unittest import TestCase, expectedFailure as xfail\n"
                "class Expected(TestCase):\n"
                "    @xfail\n"
                "    def test_hidden(self):\n"
                "        raise AssertionError\n"
            ),
        )
        with TemporaryDirectory() as directory:
            root = Path(directory)
            source_path = root / "source.py"
            test_path = root / "test_fixture.py"
            source_path.write_text(source_text, encoding="utf-8")
            for hidden in hidden_forms:
                with self.subTest(hidden=hidden.splitlines()[0]):
                    test_path.write_text(check_header + hidden, encoding="utf-8")
                    with patch.object(contract_audit, "SOURCE_FILES", (source_path,)), patch.object(
                        contract_audit, "TEST_FILES", (test_path,)
                    ):
                        report = contract_audit.audit()
                    self.assertFalse(report["passed"])
                    self.assertTrue(
                        any("not a discoverable unittest" in item for item in report["findings"])
                    )

            test_path.write_text(
                check_header
                + "import unittest\n"
                + "class AsyncRight(unittest.IsolatedAsyncioTestCase):\n"
                + "    async def test_hidden(self):\n"
                + "        pass\n",
                encoding="utf-8",
            )
            with patch.object(
                contract_audit, "SOURCE_FILES", (source_path,)
            ), patch.object(contract_audit, "TEST_FILES", (test_path,)):
                report = contract_audit.audit()
            self.assertTrue(report["passed"], report["findings"])

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
