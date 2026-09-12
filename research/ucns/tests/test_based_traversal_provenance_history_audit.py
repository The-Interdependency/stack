"""Executable witnesses for the based-traversal provenance history audit."""

# === CHECKS ===
# id: check_traversal_provenance_audit_binds_search_universe
#   proves: traversal_provenance_audit_binds_search_universe
#   call: self::test_repository_history_snapshots_are_exact
#   mutates: none
#   cleanup: none
#
# id: check_traversal_provenance_audit_binds_candidate_artifacts
#   proves: traversal_provenance_audit_binds_candidate_artifacts
#   call: self::test_candidate_artifacts_replay_and_remain_nonqualifying
#   mutates: none
#   cleanup: none
#
# id: check_traversal_provenance_audit_requires_geometric_selection
#   proves: traversal_provenance_audit_requires_geometric_selection
#   call: self::test_promising_substitutes_retain_their_disqualifiers
#   mutates: none
#   cleanup: none
#
# id: check_traversal_provenance_audit_freezes_five_unresolved_fields
#   proves: traversal_provenance_audit_freezes_five_unresolved_fields
#   call: self::test_all_five_certificate_fields_are_unresolved
#   mutates: none
#   cleanup: none
#
# id: check_traversal_provenance_audit_stops_constructor
#   proves: traversal_provenance_audit_stops_constructor
#   call: self::test_constructor_stops_with_all_outputs_null
#   mutates: none
#   cleanup: none
#
# id: check_traversal_provenance_audit_classifies_pcea_control
#   proves: traversal_provenance_audit_classifies_pcea_control
#   call: self::test_pcea_interpolation_control_is_unresolved
#   mutates: none
#   cleanup: none
#
# id: check_traversal_provenance_audit_receipt_replays
#   proves: traversal_provenance_audit_receipt_replays
#   call: self::test_receipt_replays_byte_identically
#   mutates: none
#   cleanup: none
# === END CHECKS ===

from __future__ import annotations

from dataclasses import replace
from hashlib import sha256
import json
from pathlib import Path
import sys
import unittest


UCNS_RESEARCH_ROOT = Path(__file__).resolve().parents[1]
COMMITTED_RECEIPT = (
    UCNS_RESEARCH_ROOT
    / "receipts"
    / "based-traversal-provenance-history-audit-v0.json"
)
sys.path.insert(0, str(UCNS_RESEARCH_ROOT))

import based_traversal_provenance_history_audit as m


class BasedTraversalProvenanceHistoryAuditTest(unittest.TestCase):
    def test_repository_history_snapshots_are_exact(self) -> None:
        snapshots = {item.key: item for item in m.repository_snapshots()}
        self.assertEqual(set(snapshots), {"ucns", "a0-betatest"})

        ucns = snapshots["ucns"]
        self.assertEqual(ucns.anchor_commit, m.UCNS_PINNED_COMMIT)
        self.assertEqual(ucns.anchor_tree, m.UCNS_PINNED_TREE)
        self.assertEqual(ucns.head_commit, "52ce6839c3f884d01a3cf561ae96fd2ef4c35ab8")
        self.assertEqual(ucns.origin_main_commit, "828c0b8bbcfc267efb5701da714191c1f73a81ff")
        self.assertEqual(ucns.ref_count, 225)
        self.assertEqual(ucns.unique_tip_count, 188)
        self.assertEqual(ucns.reachable_commit_count, 1128)
        self.assertEqual(
            ucns.ref_set_sha256,
            "7db1f42da92c14b0cc26f95bb9f0a18453a00754c004be02442dd041f53ec115",
        )
        self.assertEqual(
            ucns.unique_tip_set_sha256,
            "9bd507bceb6dd3ee5c4f9ce741c64a112d1884996dae07cdec36226b74af62a1",
        )
        self.assertEqual(ucns.exact_term_match_count, 0)
        self.assertEqual(ucns.semantic_candidate_count, 283)
        self.assertEqual(
            ucns.semantic_candidate_set_sha256,
            "549b3953f290b9ff8c6482625fb1823e485db14e0714bca6e3948cc7fd272cc0",
        )

        a0 = snapshots["a0-betatest"]
        self.assertEqual(a0.anchor_commit, m.A0_SOURCE_COMMIT)
        self.assertEqual(a0.anchor_tree, m.A0_SOURCE_TREE)
        self.assertEqual(a0.head_commit, "11cda399f510b2bb3b0ba0a717b379a777200b88")
        self.assertEqual(a0.origin_main_commit, a0.head_commit)
        self.assertEqual(a0.ref_count, 18)
        self.assertEqual(a0.unique_tip_count, 15)
        self.assertEqual(a0.reachable_commit_count, 2032)
        self.assertEqual(
            a0.ref_set_sha256,
            "4eb447e000c3ff129c3599210f8e305a947292e19da95108c6cca11d2b31413c",
        )
        self.assertEqual(
            a0.unique_tip_set_sha256,
            "dab518bfa3271bc4905a4dd07cb45778a8b82adce53fe71f4a17e0e5ff9d0d0c",
        )
        self.assertEqual(a0.exact_term_match_count, 0)
        self.assertEqual(a0.semantic_candidate_count, 133)
        self.assertEqual(
            a0.semantic_candidate_set_sha256,
            "4455d6101ea2c709be05785bb89f19b63d2cb6e55f23c980cf04cb3f77a8c406",
        )

    def test_candidate_artifacts_replay_and_remain_nonqualifying(self) -> None:
        artifacts = m.evidence_artifacts()
        self.assertEqual(len(artifacts), 21)
        self.assertEqual(len({item.artifact_id for item in artifacts}), len(artifacts))
        self.assertFalse(any(item.qualifying_certificate_fields for item in artifacts))
        for item in artifacts:
            self.assertEqual(len(item.blob_oid), 40)
            self.assertEqual(len(item.content_sha256), 64)
            self.assertEqual(len(item.commit_tree), 40)
            self.assertTrue(set(item.candidate_fields) <= set(m.CERTIFICATE_FIELDS))

        bad = replace(m.ARTIFACT_SPECS[0], content_sha256="0" * 64)
        with self.assertRaisesRegex(m.ProvenanceAuditError, "content digest changed"):
            m._verify_artifact(bad)

    def test_promising_substitutes_retain_their_disqualifiers(self) -> None:
        by_id = {item.artifact_id: item for item in m.evidence_artifacts()}
        expected_fragments = {
            "pinned_public_gonol": "no operation attaching",
            "pinned_direct_mobius": "does not select displacement sign",
            "merged_public_gonol_contract": "must not be invented",
            "merged_public_gonol_faces": "caller argument",
            "merged_public_gonol_lifted_text_path": "text codec",
            "merged_generic_recursive_traversal": "caller child enumeration",
            "merged_v015_partial_attachment": "nonselecting",
            "merged_v017_source_bound_initiation": "no geometric position",
            "post_pinned_seed_construction": "selection effect is none",
            "p5_p7_marked_link_preregistration": "no artifact maps them",
            "a0_lifted_path_scope_correction": "text codec",
            "a0_reset_boundary": "remains unresolved",
        }
        for artifact_id, fragment in expected_fragments.items():
            self.assertIn(fragment, by_id[artifact_id].disqualifier)

        self.assertEqual(
            by_id["pinned_geometry_boundary"].candidate_fields,
            (),
        )
        self.assertEqual(
            by_id["post_pinned_seed_construction"].authority_standing,
            "post-pinned-not-audit-authority",
        )
        clusters = m.excluded_candidate_clusters()
        self.assertEqual(len(clusters), 1)
        self.assertEqual(
            clusters[0]["authority_standing"],
            "reachable-branch-only-not-in-pinned-ancestry",
        )
        self.assertEqual(
            tuple(item["commit"] for item in clusters[0]["commits"]),
            m.LEXICAL_BRANCH_CANDIDATE_COMMITS,
        )
        self.assertEqual(clusters[0]["qualifying_certificate_fields"], [])

    def test_all_five_certificate_fields_are_unresolved(self) -> None:
        findings = m.certificate_field_findings()
        self.assertEqual(tuple(item.field for item in findings), m.CERTIFICATE_FIELDS)
        for item in findings:
            self.assertEqual(item.status, m.FIELD_STATUS)
            self.assertTrue(item.candidate_artifact_ids)
            self.assertEqual(item.qualifying_artifact_ids, ())
            self.assertTrue(item.promotion_requirement)

    def test_constructor_stops_with_all_outputs_null(self) -> None:
        result = m.audit()
        self.assertEqual(result.history_status, m.HISTORY_STATUS)
        self.assertEqual(result.constructor_status, m.CONSTRUCTOR_STATUS)
        self.assertEqual(
            result.constructor_certificate,
            {field: None for field in m.CERTIFICATE_FIELDS},
        )
        self.assertIsNone(result.geometry_selected_traversal_word)
        self.assertIsNone(result.monodromy)
        self.assertIsNone(result.arithmetic_readout)
        self.assertIsNone(result.successor)
        self.assertIsNone(result.fourth_gonol)

    def test_pcea_interpolation_control_is_unresolved(self) -> None:
        control = m.audit().to_payload()["pcea_interpolation_control"]
        self.assertEqual(control["prediction"], 164513086777)
        self.assertEqual(control["status"], "UNRESOLVED")
        self.assertFalse(control["comparison_performed"])
        self.assertIsNone(control["survived"])
        self.assertIsNone(control["falsified"])

        source = Path(m.__file__).read_text(encoding="utf-8")
        self.assertNotIn("54837698421", source)
        self.assertNotIn("2881", source)

    def test_receipt_replays_byte_identically(self) -> None:
        raw = COMMITTED_RECEIPT.read_bytes()
        committed = json.loads(raw)
        committed_digest = committed.pop("receipt_sha256")
        self.assertEqual(committed, m.receipt_payload())
        self.assertEqual(committed_digest, m.receipt_digest())
        self.assertEqual(committed_digest, sha256(m.receipt_bytes()).hexdigest())
        self.assertEqual(raw, m.formatted_receipt_bytes())

        for item in committed["source"]["source_file_digests"]:
            path = m._stack_root() / item["path"]
            self.assertEqual(sha256(path.read_bytes()).hexdigest(), item["sha256"])
        self.assertEqual(
            committed["source"]["predecessor_audit_receipt"]["payload_sha256"],
            "4c4f06aae237fd4ce771dc7849738617b0cbc9ab3cc5bd6685ffec84b2921a09",
        )


if __name__ == "__main__":
    unittest.main()
