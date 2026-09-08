"""Contracts for the stack-local From Photons to the Macroverse research package."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import re
import unittest
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[1]
STACK = PROJECT.parents[1]
HEX40 = re.compile(r"^[0-9a-f]{40}$")
HEX64 = re.compile(r"^[0-9a-f]{64}$")
SOURCE_MD_SHA = "f25960d3f691788d3c79bf11a1c6fa47ae1a76700e7d7c042e911f6b56579696"
SOURCE_DOCX_SHA = "18d08a24c2837e4455fb25c06294b4302d8187d1b0a449a826754b9a4d26aaa2"
SOURCE_PDF_SHA = "e1715a26b46b210a821e8bef72df934646e330e03489bf1e9b97a1b8e786e6f4"


def load_json(name: str) -> dict:
    return json.loads((PROJECT / name).read_text(encoding="utf-8"))


def load_assembler():
    path = PROJECT / "tools" / "assemble_paper.py"
    spec = importlib.util.spec_from_file_location("from_photons_assembler", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load assembler at {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class Contracts(unittest.TestCase):
    def test_original_markdown_is_immutable_and_receipted(self) -> None:
        receipt = load_json("SOURCE_RECEIPT.json")
        by_role = {item["role"]: item for item in receipt["sources"]}
        self.assertEqual(
            by_role["external original authoring source used for exact text comparison"]["sha256"],
            SOURCE_MD_SHA,
        )
        self.assertFalse(
            by_role["external original authoring source used for exact text comparison"]["repository_copy"]
        )
        self.assertEqual(
            by_role["editable authoring counterpart used for identity and render verification"]["sha256"],
            SOURCE_DOCX_SHA,
        )
        self.assertEqual(by_role["user-supplied rendered submission"]["sha256"], SOURCE_PDF_SHA)
        self.assertEqual(
            by_role["user-supplied rendered submission"]["visual_audit"]["standing"], "HEALTHY"
        )
        source_note = (PROJECT / receipt["source_note_path"]).read_text(encoding="utf-8")
        for digest in (SOURCE_MD_SHA, SOURCE_DOCX_SHA, SOURCE_PDF_SHA):
            self.assertIn(digest, source_note)
        for source in receipt["sources"]:
            retrieval = source["retrieval"]
            self.assertEqual(retrieval["status"], "BLOCKED_EXTERNAL_HASH_ONLY")
            self.assertEqual(retrieval["durable_locator"], "hmmm")
            self.assertFalse(retrieval["fresh_checkout_reproducible"])

    def test_audited_fragments_are_repository_owned_and_retrievable(self) -> None:
        receipt = load_json("SOURCE_RECEIPT.json")
        self.assertTrue(receipt["revision"]["repository_copy"])
        self.assertEqual(
            receipt["revision"]["verified_render"]["status"],
            "HMMM_STALE_AFTER_PAPER_TEXT_REPAIRS",
        )
        retrieval = receipt["revision"]["retrieval"]
        self.assertEqual(retrieval["status"], "REPOSITORY_OWNED_FRAGMENTS")
        self.assertTrue(retrieval["fresh_checkout_reproducible"])
        self.assertEqual(
            retrieval["fragment_manifest_carries"],
            ["path", "bytes", "sha256", "git_blob_sha1"],
        )
        manifest = load_json("paper/manifest.json")
        ledger = load_json("CLAIM_LEDGER.json")
        assembler = load_assembler()
        paper = assembler.assemble()
        for item in manifest["fragments"]:
            data = (PROJECT / item["path"]).read_bytes()
            self.assertEqual(hashlib.sha256(data).hexdigest(), item["sha256"])
            self.assertEqual(assembler.git_blob_sha1(data), item["git_blob_sha1"])
        self.assertEqual(hashlib.sha256(paper).hexdigest(), receipt["revision"]["assembled_sha256"])
        self.assertEqual(manifest["assembled_sha256"], receipt["revision"]["assembled_sha256"])
        self.assertEqual(ledger["paper_sha256"], receipt["revision"]["assembled_sha256"])

    def test_parser_artifact_is_not_misreported_as_defect(self) -> None:
        source_note = (PROJECT / "source" / "README.md").read_text(encoding="utf-8")
        audit = (PROJECT / "AUDIT.md").read_text(encoding="utf-8")
        ledger = load_json("CLAIM_LEDGER.json")
        self.assertIn("D(Z) in [0,1]", source_note)
        self.assertIn("parsed-text endpoint was not a paper defect", audit)
        claim = next(x for x in ledger["claims"] if x["id"] == "DIFFERENTIATION_RANGE")
        self.assertEqual(claim["status"], "HEALTHY_PARSER_ARTIFACT_CLOSED")

    def test_active_paper_contains_actual_repairs(self) -> None:
        manifest = load_json("paper/manifest.json")
        text = b"".join((PROJECT / item["path"]).read_bytes() for item in manifest["fragments"]).decode("utf-8")
        flat = " ".join(text.split())
        self.assertIn("hmmm_undefined", text)
        self.assertIn(r"\mathcal B_{\mathrm{bdry}}", text)
        self.assertNotIn(r"+\epsilon", text)
        self.assertIn("measurement certificate", text)
        self.assertIn("single argmax selects one high-scoring candidate", text)
        self.assertIn("candidate necessary architecture", text)
        self.assertNotIn("Consciousness precedes biological life as a pattern class", text)
        self.assertIn("pre-biological embodiments remain logically open within the postulate but empirically unestablished", flat)
        self.assertIn("not ratified as selected UCNS geometry", text)
        self.assertIn("The indicator is non-operational in this package", text)
        self.assertNotIn("The indicator classifies organized episodes", text)
        self.assertNotIn("learned from preregistered contrasts among waking reportable experience", text)
        self.assertIn(r"\operatorname{Part}_{\mathrm{proper}}([n])", text)
        self.assertNotIn(r"\Phi_n=\min_{\pi}D_{\mathrm{KL}}", text)
        self.assertIn(r"\mathcal M_T(Y)", text)
        self.assertIn(r"\mathcal A_M(Y)", text)
        self.assertIn(r"n_r(t)=(\cos 2\pi t,\sin 2\pi t,0)", text)
        self.assertIn(r"\mathcal P_t\in\operatorname*{arg\,max}_{\mathcal A\subseteq\mathcal Y_t}", text)
        self.assertNotIn(r"\mathcal S_t\in\arg\max_Y\Lambda(Y)", text)
        self.assertIn(r"\(|S_G|\ge k_G\)", text)
        self.assertIn(r"\(G_{\mathrm c}>0\) by itself is not enough", text)
        self.assertIn(r"K_{\tau}(z,z'\mid x^{-Z})", text)
        self.assertIn("current-context distribution or point context", text)
        self.assertIn(r"R_\delta^{\mathrm{disj}}", text)
        self.assertNotIn(r"R_\delta=\frac1{f_\delta}", text)
        self.assertNotIn("Disorders of consciousness should be better classified", text)
        self.assertIn("must not diagnose, classify, or determine the conscious status of any person", text)
        self.assertIn("10.53765/20512201.31.3.056", text)
        self.assertIn("10.1142/S0217751X26300115", text)

    def test_domain_claim_is_bounded(self) -> None:
        claim = load_json("DOMAIN_CLAIM.json")
        status = claim["claim_status"].lower()
        for phrase in ("stack-local research", "not canon", "not empirically validated", "not clinical", "not a human classifier"):
            self.assertIn(phrase, status)
        exclusions = " ".join(claim["excluded_uses"]).lower()
        for phrase in ("derive primitive consciousness", "automatic evidence for consciousness", "clinical diagnosis", "extra spacetime dimension"):
            self.assertIn(phrase, exclusions)
        self.assertEqual(claim["no_transfer"]["metapat_root_impact"], "none")
        self.assertIsNone(claim["no_transfer"]["canon_selection"])

    def test_claim_ledger_standing(self) -> None:
        by_id = {x["id"]: x for x in load_json("CLAIM_LEDGER.json")["claims"]}
        self.assertEqual(by_id["BOUNDARY_INTEGRITY_SUPPORT"]["status"], "REPAIRED")
        self.assertEqual(by_id["TRIADIC_MINIMUM"]["status"], "REPAIRED_NECESSARY_NOT_SUFFICIENT")
        self.assertEqual(by_id["SUBJECT_FAMILY_SELECTION"]["status"], "REPAIRED_BUT_UNRESOLVED")
        self.assertEqual(by_id["HUMAN_HEPTAD"]["status"], "UNVALIDATED_HIGH_RISK")
        self.assertEqual(by_id["SOURCE_REFERENCES_21_22"]["standing"], "HMMM")

    def test_symbol_registry_prevents_plain_text_collisions(self) -> None:
        text = (PROJECT / "SYMBOL_REGISTRY.md").read_text(encoding="utf-8")
        for token in ("`C0_presence`", "`C_org_t`", "`M_macro`", "`M_eff_T`", "`B_bdry`", "`A_torus`", "`I_event_t`", "`Cl_n`", "`CG_k`", "`T_arity_t`"):
            self.assertIn(token, text)
        self.assertIn("Bare `consciousness` is forbidden", text)
        self.assertIn("Typography is not a type system", text)

    def test_work_graph_digest_and_nontransfer(self) -> None:
        graph = load_json("WORK_GRAPH.json")
        participants = graph["participants"]
        boundaries = graph["boundaries"]
        self.assertEqual(len({x["id"] for x in participants}), len(participants))
        for item in participants:
            if item["kind"] == "repository":
                self.assertRegex(item["commit"], HEX40)
            elif item["kind"] == "artifact":
                self.assertRegex(item["sha256"], HEX64)
            elif item["kind"] == "publication":
                self.assertRegex(item["doi"], r"^10\.")
            elif item["kind"] == "unpublished-manuscript":
                self.assertEqual(item["identity"], "hmmm")
        payload = {"participants": participants, "boundaries": boundaries}
        observed = hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
        self.assertEqual(observed, graph["work_graph_sha256"])
        for key in ("authority_transfer", "proof_status_transfer", "measurement_status_transfer", "empirical_status_transfer", "clinical_status_transfer", "metaphysical_postulate_to_physics", "physics_to_primitive_intrinsic_presence", "physics_to_organized_subjecthood", "physics_to_candidate_content", "ucns_geometry_to_primitive_intrinsic_presence", "ucns_geometry_to_organized_subjecthood", "ucns_geometry_to_candidate_content", "ucns_candidate_ratification_transfer", "edcm_validation_claim", "pcea_security_to_ontology", "epac_internal_result_to_external_physics", "human_classification"):
            self.assertIs(boundaries[key], False, key)
        self.assertNotIn("physics_to_consciousness", boundaries)
        self.assertNotIn("ucns_geometry_to_consciousness", boundaries)
        self.assertEqual(boundaries["metapat_root_impact"], "none")
        self.assertIsNone(boundaries["canon_selection"])
        ucns = next(x for x in participants if x["id"] == "ucns")
        self.assertEqual(ucns["commit"], "ef98748309913588fb13f389f809d5ef6cb5fec3")
        self.assertIn("no ratification", ucns["role"])

    def test_preregistration_is_frozen_and_nonclassifying(self) -> None:
        text = (PROJECT / "PREREGISTRATION.md").read_text(encoding="utf-8")
        flat = " ".join(text.split())
        for phrase in ("run status: not-run", "human subjects: none", "animal subjects: none", "LLM calls: none", "seeds `32..63`: sealed decision set", "`SURVIVED` requires all of the following", "`FALSIFIED` applies", "`UNRESOLVED` applies", "No outcome classifies a human, animal, model, organization, or physical system as conscious"):
            self.assertIn(phrase, flat)
        for phrase in ("configuration `arity-recursion-synthetic-v2` exactly", "carrier state dimension: `2` real coordinates per carrier", "trainable parameter ceiling: `4096`", "episode length: `128` transitions after a `32`-transition burn-in", "optimizer: Adam with learning rate `0.001`", "Primary decision outcomes", "Guardrail and diagnostic outcomes", "both primary decision outcomes"):
            self.assertIn(phrase, flat)
        for phrase in ("Synthetic generator", "SHA-256 input is the UTF-8 encoding", "process_noise", "intervention_plan", "model_initializers", "Discrete choices use `floor(u*K)`", "Matched candidate/control comparisons use the same", "Held-out interventional negative log likelihood is the mean one-step predictive Gaussian NLL", "ordered child-arity vector", "left-rotated child-arity vector", "Embedded primary-outcome certificate", "observed scalar-coordinate identity", "input encoding is the dual map", "Adjacent-arity comparisons are `BLOCKED`"):
            self.assertIn(phrase, flat)
        self.assertIn("No other random-number source, output lane, block rule, or key encoding is admissible", flat)
        self.assertIn("`SYSTEMS.json` must carry the realized coefficient tensors", flat)
        self.assertIn("q_{m,n}(i) = floor(i*m/n)", text)
        self.assertIn("r_{m,n}(a) = floor(a*n/m)", text)
        self.assertNotIn("both primary outcomes: interventional log score and recovery", flat)
        for control in ("six-carrier", "arbitrary-seven", "unnested-seven", "label-shuffled"):
            self.assertIn(control, text)
        self.assertIn("hmmm_undefined", text)

    def test_preregistration_closes_exact_head_replay_blockers(self) -> None:
        text = (PROJECT / "PREREGISTRATION.md").read_text(encoding="utf-8")
        flat = " ".join(text.split())

        for phrase in (
            "protocol version: 0.3.0",
            '["arity-recursion-synthetic-v2",s,n,sigma_milli,domain,role,[k0,...,kp],block]',
            "concatenated placeholders or language-native float strings are forbidden",
            "stability/00` through `stability/15",
            "If no attempt is accepted, that system is `BLOCKED`",
        ):
            self.assertIn(phrase, flat)

        for phrase in (
            "exactly `r=0` generic intervention channels",
            "`u_t=()` at every transition",
            "there is no `A_i u_t` term to sample or fit",
            "additional to the `64/16/16` observational episodes",
            "Class `5` and `6` are never used for fitting or restart selection",
        ):
            self.assertIn(phrase, flat)

        for phrase in (
            "The nested transition has one leaf noise source",
            "g_{t,i}",
            "y_{t+1,i,l} = tanh(ell_{t,i,l} + g_{t,i}/a_i)",
            "no other coefficient or noise role contributes",
        ):
            self.assertIn(phrase, flat)

        for phrase in (
            "Fitted-family equations and registry",
            "capacity-only family over flattened observed dimension `D`",
            "v_c = 1e-6 + softplus(rho_c)",
            "`B_H=min(4096,min_f P_f)`",
            "### Required comparisons",
            "`H_A(n)` requires",
            "`H_R(n)` requires",
            "`H_7` uses the union",
        ):
            self.assertIn(phrase, flat)

        for phrase in (
            "Embedded primary-outcome certificate `primary-outcome-v1`",
            "it may not choose or replace a primary estimator",
            "Recovery uses exactly the `16` held-out class-`5` episodes",
            "active for transitions `t0,...,t0+15`",
            "Recursively feed back that family's decoded predictive mean",
            "`ECE_candidate - ECE_control <= 0.02`",
            "exactly `B=65536` nonparametric paired bootstrap draws",
            "exactly `P=65536` sampled paired sign permutations",
            "finite-sample `+1` correction",
        ):
            self.assertIn(phrase, flat)

        for phrase in (
            "One scalar key consumes exactly one lane from `block=0`",
            "implementations never take a second lane or advance to `block>0`",
            '["arity-recursion-synthetic-v2","parameter-mask",family_id,tensor_name,[i0,...,iq]]',
            "The label-shuffle families are the sole exception to independent ranking",
            "let `S_f(a)` be the set of original observed scalar coordinates",
            "The class-`5` recovery cut uses this same map",
            "exactly `0.5*NLL_full + 0.5*NLL_cut`",
            "The simultaneous standardized-effect interval is `I_g=[g-q95_g,g+q95_g]`",
        ):
            self.assertIn(phrase, flat)

        self.assertNotIn("arity-recursion-synthetic-v1", text)

    def test_human_and_machine_entrypoints_agree(self) -> None:
        readme = (PROJECT / "README.md").read_text(encoding="utf-8")
        paper_index = (PROJECT / "PAPER.md").read_text(encoding="utf-8")
        root = (STACK / "README.md").read_text(encoding="utf-8")
        for phrase in ("SURVIVED as a candidate research program", "canon:                  no", "clinical use:           no", "human classification:  no", "Why the root canonical pins are unchanged", "## hmmm"):
            self.assertIn(phrase, readme)
        self.assertIn("ordered, hash-bound Markdown fragments", paper_index)
        self.assertIn("current visual render is `hmmm` until rerendered", readme)
        self.assertIn("from-photons-to-macroverse/", root)
        self.assertIn("consciousness-first candidate research", root)

    def test_root_manifest_records_noncanonical_research_participants(self) -> None:
        root_manifest_text = (STACK / "STACK_MANIFEST.md").read_text(encoding="utf-8")
        root_manifest = json.loads((STACK / "stack-manifest.json").read_text(encoding="utf-8"))
        self.assertIn("Research-Only Composition Participants", root_manifest_text)
        self.assertEqual(root_manifest["version"], "1.1.0")
        self.assertIn("version `1.1.0`", root_manifest_text)
        records = [
            item
            for item in root_manifest["research_participants"]
            if item["workspace"] == "research/from-photons-to-macroverse/"
        ]
        self.assertEqual(len(records), 7)
        by_repo = {item["repository"]: item for item in records}
        self.assertEqual(
            by_repo["The-Interdependency/skill-lib"]["commit"],
            "61eb3b14db440e6ee9b7bf8de3b646dbfd00fb32",
        )
        self.assertEqual(
            by_repo["The-Interdependency/ucns"]["commit"],
            "ef98748309913588fb13f389f809d5ef6cb5fec3",
        )
        self.assertTrue(all(item["canonical_release"] is False for item in records))
        payload = {
            "repositories": root_manifest["repositories"],
            "research_participants": root_manifest["research_participants"],
            "boundaries": root_manifest["boundaries"],
        }
        observed = hashlib.sha256(
            json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
        ).hexdigest()
        self.assertEqual(observed, root_manifest["work_graph_sha256"])
        self.assertIn(root_manifest["work_graph_sha256"], root_manifest_text)

    def test_workflow_is_path_scoped(self) -> None:
        workflow = (STACK / ".github/workflows/from-photons-to-macroverse.yml").read_text(encoding="utf-8")
        self.assertGreaterEqual(workflow.count('"research/from-photons-to-macroverse/**"'), 2)
        self.assertGreaterEqual(workflow.count('"STACK_MANIFEST.md"'), 2)
        self.assertGreaterEqual(workflow.count('"stack-manifest.json"'), 2)
        self.assertIn("actions/checkout@v6", workflow)
        self.assertIn("actions/setup-python@v6", workflow)
        self.assertIn("python -m unittest discover -s research/from-photons-to-macroverse/tests -q", workflow)


if __name__ == "__main__":
    unittest.main()
