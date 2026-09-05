"""Contract checks for the stack-local psychsocio-metafauna research artifact."""

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


class PsychsocioMetafaunaContracts(unittest.TestCase):
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
        self.assertEqual(claim["term_id"], "psychsocio-metafauna.pattern-lineage")
        self.assertEqual(claim["surface_form"], "psychsocio metafauna")

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

    def test_preregistration_decision_rules_are_independent_and_frozen(self) -> None:
        prereg = (PROJECT / "PREREGISTRATION.md").read_text(encoding="utf-8")

        self.assertIn("difference-in-differences interaction contrast", prereg)
        self.assertIn(
            "no fitted threshold or breakpoint model participates in this decision",
            prereg,
        )
        self.assertNotIn("one declared piecewise-threshold model", prereg)
        self.assertIn(
            "does not reuse the candidate-capture configuration",
            prereg,
        )
        self.assertIn(
            "reduce both persistence and reproduction allocation by at least `0.15`",
            prereg,
        )
        self.assertNotIn("reduces persistence and reproduction demands", prereg)

    def test_human_and_machine_entrypoints_agree(self) -> None:
        readme = (PROJECT / "README.md").read_text(encoding="utf-8")
        prereg = (PROJECT / "PREREGISTRATION.md").read_text(encoding="utf-8")
        root_readme = (STACK / "README.md").read_text(encoding="utf-8")

        for phrase in (
            "proposed cross-domain theory",
            "clinical or diagnostic use: no",
            "human classification: no",
            "METAPAT root impact: none",
            "lineage identity        != an \"I\"",
            "Nine active research programs",
            "## Non-use boundary",
            "## hmmm",
        ):
            self.assertIn(phrase, readme)

        for phrase in (
            "run status: not-run",
            "human subjects: none",
            "LLM calls: none",
            "must not contain a `captured` state variable",
            "## hmmm",
        ):
            self.assertIn(phrase, prereg)

        self.assertIn("psychsocio-metafauna/ # proposed", root_readme)
        self.assertIn(
            "EPAC and psychsocio metafauna are currently in this pre-graduation state.",
            root_readme,
        )


if __name__ == "__main__":
    unittest.main()
