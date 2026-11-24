"""Contract checks for the stack-local PSFR research artifact."""

from __future__ import annotations

import hashlib
import json
import re
import unittest
from pathlib import Path


PROJECT = Path(__file__).resolve().parents[1]
STACK = PROJECT.parents[1]
HEX40 = re.compile(r"^[0-9a-f]{40}$")


def load_json(name: str) -> dict:
    return json.loads((PROJECT / name).read_text(encoding="utf-8"))


class PSFRContracts(unittest.TestCase):
    def test_domain_claim_is_explicitly_provisional_and_bounded(self) -> None:
        claim = load_json("DOMAIN_CLAIM.json")

        required = {
            "term_id",
            "surface_form",
            "claiming_domain",
            "claimed_sense",
            "scope",
            "claim_type",
            "claim_status",
            "authority_source",
            "included_uses",
            "excluded_uses",
            "nearby_terms",
            "known_namespace_collisions",
            "effective_version",
            "hmmm",
        }
        self.assertFalse(required - claim.keys())
        self.assertEqual(claim["term_id"], "psfr.psychosocial-fauna")
        self.assertEqual(claim["surface_form"], "psychosocial fauna")

        status = claim["claim_status"].lower()
        self.assertIn("stack-local research", status)
        self.assertIn("not canon", status)
        self.assertIn("not diagnosis", status)
        self.assertIn("not a human classifier", status)

        exclusions = " ".join(claim["excluded_uses"]).lower()
        for boundary in (
            "diagnosing",
            "inferring trauma",
            "targeting people",
            "coercive influence",
            "claiming that a lineage possesses an accountable i",
        ):
            self.assertIn(boundary, exclusions)

        self.assertTrue(claim["hmmm"])

    def test_work_graph_identity_and_digest(self) -> None:
        graph = load_json("WORK_GRAPH.json")
        participants = graph["participants"]
        boundaries = graph["boundaries"]

        ids = [item["id"] for item in participants]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertGreaterEqual(len(ids), 20)

        for item in participants:
            commit = item["commit"]
            if item["kind"] == "external-authority":
                self.assertEqual(commit, "hmmm")
            else:
                self.assertRegex(commit, HEX40)

        stack_participant = next(item for item in participants if item["id"] == "stack")
        self.assertEqual(
            stack_participant["commit"],
            "6c3f94b1e6d77e8f1abd36edc53da5fda596b416",
        )
        self.assertEqual(stack_participant["path"], "research/psfr/")
        self.assertIn("introduction snapshot", stack_participant["relation"])
        self.assertIn("avoiding recursive self-reference", stack_participant["relation"])

        metapat = next(item for item in participants if item["id"] == "metapat")
        metapat_base = json.loads(
            (STACK / "research" / "metapat" / "BASE.json").read_text(encoding="utf-8")
        )
        self.assertEqual(metapat["commit"], metapat_base["source_commit"])
        self.assertIn("libs/metapat", metapat["relation"])

        payload = {"participants": participants, "boundaries": boundaries}
        canonical = json.dumps(
            payload, sort_keys=True, separators=(",", ":")
        ).encode("utf-8")
        observed = hashlib.sha256(canonical).hexdigest()
        self.assertEqual(observed, graph["work_graph_sha256"])

    def test_workflow_rechecks_when_metapat_base_changes(self) -> None:
        workflow = (STACK / ".github" / "workflows" / "psfr.yml").read_text(
            encoding="utf-8"
        )
        self.assertGreaterEqual(
            workflow.count('"research/metapat/BASE.json"'),
            2,
            "pull_request and push path filters must both watch the exact METAPAT pin",
        )

    def test_non_transfer_boundaries_fail_closed(self) -> None:
        boundaries = load_json("WORK_GRAPH.json")["boundaries"]

        false_boundaries = (
            "authority_transfer",
            "proof_status_transfer",
            "measurement_status_transfer",
            "empirical_status_transfer",
            "certification_status_transfer",
            "clinical_status_transfer",
            "diagnostic_use",
            "human_classification",
            "coercive_intervention_authority",
            "ucns_geometry_required_for_theory_statement",
        )
        for key in false_boundaries:
            self.assertIs(boundaries[key], False, key)

        self.assertEqual(boundaries["metapat_root_impact"], "none")
        self.assertEqual(boundaries["edcm_activation"], "not-run")
        self.assertIsNone(boundaries["canon_selection"])
        self.assertTrue(boundaries["hmmm"])

if __name__ == "__main__":
    unittest.main()
