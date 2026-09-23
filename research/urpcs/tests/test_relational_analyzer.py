"""Checks for the read-only URPCS relational carrier analyzer."""

# === CHECKS ===
# id: check_urpcs_relational_native_graph
#   proves: urpcs_relational_records_only_native_edges
#   call: self::check_source_backed_graph
#   requires: python3
#   timeout: 30
#   mutates: none
#   cleanup: none
#
# id: check_urpcs_relational_authentication_order
#   proves: urpcs_relational_authenticates_first
#   call: self::check_authentication_order
#   requires: python3
#   timeout: 20
#   mutates: none
#   cleanup: none
#
# id: check_urpcs_relational_evidence_replay
#   proves: urpcs_relational_evidence_is_deterministic
#   call: self::check_committed_evidence
#   requires: python3
#   timeout: 30
#   mutates: none
#   cleanup: none
# === END CHECKS ===

from __future__ import annotations

import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


URPCS_ROOT = Path(__file__).resolve().parents[1]
STACK_ROOT = URPCS_ROOT.parents[1]
sys.path.insert(0, str(URPCS_ROOT))

import urpcs_relational_analyzer as analyzer  # noqa: E402
import urpcs_v1_reference as ref  # noqa: E402


UCNS_ROOT = STACK_ROOT / "libs/ucns"
RECEIPT_PATH = URPCS_ROOT / "receipts/urpcs-relational-carrier-v0.json"
REPORT_PATH = URPCS_ROOT / "docs/URPCS-relational-carrier-v0.md"


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load_vectors() -> list[dict]:
    return json.loads((URPCS_ROOT / "vectors/urpcs-v1-vectors.json").read_text())["vectors"]


def odd_vector() -> dict:
    return next(row for row in load_vectors() if row["id"] == "odd_09_r0")


def check_source_backed_graph() -> None:
    row = odd_vector()
    ucns = analyzer.projection.load_ucns_direct_mobius(UCNS_ROOT)
    trace = analyzer.analyze_trace(
        case_id="test_odd_09_r0",
        ciphertext=bytes.fromhex(row["ciphertext_hex"]),
        state=analyzer._state_from_json(row["initial_state"]),
        associated_data=bytes.fromhex(row["ad_hex"]),
        ucns=ucns,
        expected_plaintext=b"\x09",
        source_kind="test-committed-vector",
    )
    graph = trace["graph"]
    node_ids = {node["id"] for node in graph["nodes"]}
    assert all(edge["source"] in node_ids and edge["target"] in node_ids for edge in graph["edges"])
    assert not any(":origin:" in edge["source"] and ":origin:" in edge["target"] for edge in graph["edges"])
    assert any(edge["kind"] == "attaches" for edge in graph["edges"])
    assert any(edge["kind"] == "member-of" for edge in graph["edges"])
    origins = [node for node in graph["nodes"] if node["kind"] == "origin"]
    assert origins and all(node["local_phase"] is None and node["local_sheet"] is None for node in origins)


def check_authentication_order() -> None:
    row = odd_vector()
    state = analyzer._state_from_json(row["initial_state"])
    ucns = analyzer.projection.load_ucns_direct_mobius(UCNS_ROOT)
    with mock.patch.object(ref, "decode_witness", side_effect=AssertionError("parser reached")) as parser:
        with unittest.TestCase().assertRaisesRegex(ref.CodecFail, "tag verification"):
            analyzer.analyze_trace(
                case_id="wrong-ad",
                ciphertext=bytes.fromhex(row["ciphertext_hex"]),
                state=state,
                associated_data=bytes.fromhex(row["ad_hex"]) + b"!",
                ucns=ucns,
                source_kind="test",
            )
        parser.assert_not_called()


def check_committed_evidence() -> None:
    receipt_bytes = RECEIPT_PATH.read_bytes()
    receipt = json.loads(receipt_bytes)
    analyzer.verify_receipt(receipt)
    assert receipt_bytes == analyzer._json_bytes(receipt)
    assert receipt["measurement"]["relation_audit"]["first_task_classification"] == "MULTI_ORIGIN_RELATION_PRESENT"
    assert receipt["measurement"]["relation_audit"]["direct_origin_to_origin_edges"] == 0
    assert receipt["measurement"]["relation_audit"]["edge_counts"]["state-successor"] == 2
    assert len(receipt["measurement"]["canonical_graph"]["cross_trace_edges"]) == 2
    assert receipt["measurement"]["cycle_check"]["directed_cycle_present"] is False
    assert receipt["measurement"]["cycle_check"]["visited_by_topological_check"] == receipt["measurement"]["cycle_check"]["node_count"]
    assert len(receipt["measurement"]["serialization_boundaries"]["boundary_records"]) == 2
    assert all(
        row["source_wire_sha256"] == row["target_input_sha256"] and row["information_lost"] == "none"
        for row in receipt["measurement"]["serialization_boundaries"]["boundary_records"]
    )
    assert len(receipt["corpus"]["committed_vector_ids"]) == 8
    assert receipt["corpus"]["narrow_514_case_baseline"]["messages_processed"] == 514
    for path, identity in receipt["sources"].items():
        data = (STACK_ROOT / path).read_bytes()
        assert len(data) == identity["bytes"]
        assert sha256(data) == identity["sha256"]
    receipt_sha = sha256(receipt_bytes)
    assert analyzer.render_report(receipt, receipt_sha) == REPORT_PATH.read_text()
    for trace in receipt["measurement"]["traces"]:
        graph = trace["graph"]
        payload = {"schema": graph["schema"], "nodes": graph["nodes"], "edges": graph["edges"]}
        assert analyzer._sha256(analyzer._compact(payload)) == graph["graph_sha256"]
    recursive = next(trace for trace in receipt["measurement"]["traces"] if trace["case_id"] == "generated_odd_09_r1")
    assert any(
        "case:generated_odd_09_r1:serialization:0->1" in row["history"]
        for row in recursive["observations"]
    )
    chain_two = next(trace for trace in receipt["measurement"]["traces"] if trace["case_id"] == "generated_state_chain_2")
    assert all("case:generated_state_chain_0:transform" in row["history"] for row in chain_two["observations"])
    assert all("case:generated_state_chain_1:transform" in row["history"] for row in chain_two["observations"])
    canonical_graph = dict(receipt["measurement"]["canonical_graph"])
    claimed_graph_hash = canonical_graph.pop("graph_sha256")
    assert analyzer._sha256(analyzer._compact(canonical_graph)) == claimed_graph_hash


class URPCSRelationalAnalyzerTests(unittest.TestCase):
    def test_source_backed_graph(self) -> None:
        check_source_backed_graph()

    def test_authentication_precedes_graph_construction(self) -> None:
        check_authentication_order()

    def test_ablation_is_monotone_and_attributes_marginals(self) -> None:
        records = [
            {
                "id": "a",
                "kind": "gonol-state",
                "origin": "o1",
                "gonol": "g1",
                "occurrence": None,
                "phase": "(0,8)",
                "frame": "positive-local-frame",
                "arity": 0,
                "shape": [0],
                "provenance": ["c1"],
                "history": ["t1"],
            },
            {
                "id": "b",
                "kind": "gonol-state",
                "origin": "o2",
                "gonol": "g2",
                "occurrence": None,
                "phase": "(0,8)",
                "frame": "reversed-local-frame",
                "arity": 1,
                "shape": [1],
                "provenance": ["c2"],
                "history": ["t2"],
            },
            {
                "id": "c",
                "kind": "member-state",
                "origin": "o2",
                "gonol": "g2",
                "occurrence": "x",
                "phase": "(0,8)",
                "frame": "reversed-local-frame",
                "arity": 1,
                "shape": [1],
                "provenance": ["c2"],
                "history": ["t2", "m"],
            },
        ]
        result = analyzer.ablate(records)
        classes = [step["equivalence_classes"] for step in result["steps"]]
        self.assertEqual(classes, sorted(classes))
        self.assertEqual(result["marginal_contributions"]["frame"]["pairs_separated"], 2)
        self.assertGreater(result["marginal_contributions"]["transformation_history"]["pairs_separated"], 0)

    def test_common_native_motion_exposes_noninvariant_sheet_product(self) -> None:
        records = [
            {"phase": "(0,8)", "frame": "positive-local-frame"},
            {"phase": "(5,8)", "frame": "positive-local-frame"},
        ]
        result = analyzer.torsor_rotation_check(
            records,
            analyzer.projection.load_ucns_direct_mobius(UCNS_ROOT),
        )
        self.assertEqual(result["classification"], "PHASE_INVARIANT_SHEET_PRODUCT_NOT_INVARIANT")
        self.assertFalse(result["coordinate_zero_selected"])
        self.assertEqual(result["relative_phase_changes"], 0)
        self.assertGreater(result["sheet_product_changes"], 0)
        witness = result["minimal_sheet_change_witness"]
        self.assertEqual(witness["common_native_displacement"], "(3,8)")
        self.assertEqual(witness["relation_before"]["sheet_product"], 1)
        self.assertEqual(witness["relation_after"]["sheet_product"], -1)

    def test_graph_rejects_duplicate_and_missing_references(self) -> None:
        with self.assertRaisesRegex(analyzer.RelationalAnalysisError, "duplicate graph node"):
            analyzer._canonical_graph([{"id": "x"}, {"id": "x"}], [])
        with self.assertRaisesRegex(analyzer.RelationalAnalysisError, "inconsistent graph reference"):
            analyzer._canonical_graph([{"id": "x"}], [{"id": "e", "source": "x", "target": "y"}])

    def test_committed_deterministic_evidence(self) -> None:
        check_committed_evidence()

    def test_authority_context_rejects_dirty_consumed_ucns_source(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            ucns_root = Path(tmp)
            consumed = ucns_root / "src/ucns/direct_mobius.py"
            consumed.parent.mkdir(parents=True)
            consumed.write_bytes(b"dirty-working-tree-bytes")
            with mock.patch.object(
                analyzer,
                "_git_text",
                side_effect=[
                    analyzer.STACK_INPUT_TREE,
                    analyzer.UCNS_COMMIT,
                    analyzer.UCNS_TREE,
                ],
            ), mock.patch.object(analyzer, "_git_bytes", return_value=b"pinned-committed-bytes"):
                with self.assertRaisesRegex(analyzer.RelationalAnalysisError, "UCNS consumed source drift"):
                    analyzer._authority_context(
                        STACK_ROOT,
                        ucns_root,
                        Path("/unused-skill-lib"),
                        Path("/unused-metapat"),
                    )

    def test_wire_has_no_frame_field_and_frozen_sources_match_governing_head(self) -> None:
        for row in load_vectors():
            if "ciphertext_hex" not in row:
                continue
            c0, _tag = ref.unframe(bytes.fromhex(row["ciphertext_hex"]))
            self.assertNotIn(b"positive-local-frame", c0)
            self.assertNotIn(b"reversed-local-frame", c0)
        receipt = json.loads(RECEIPT_PATH.read_text())
        governing_files = {
            row["path"]: row
            for row in receipt["corpus"]["source_corpus"]["files"]
        }
        for path in analyzer.FROZEN_PATHS:
            data = (STACK_ROOT / path).read_bytes()
            self.assertEqual(len(data), governing_files[path]["bytes"])
            self.assertEqual(sha256(data), governing_files[path]["sha256"])


if __name__ == "__main__":
    unittest.main()
