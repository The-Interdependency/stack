"""Checks for the frozen critical-evaluation plan and receipt sealing."""

import json
from pathlib import Path

from ptcna.critical_evaluation import _canonical_digest, load_frozen_plan
from ptcna.evaluation import FALSIFIED, SURVIVED_NOT_PROVED

# === CHECKS ===
# id: check_ptcna_critical_plan_digest
#   proves: ptcna_critical_plan_digest_locked
#   call: self::test_critical_plan_is_balanced_and_digest_locked
#   requires: python3
#   timeout: 30
#   mutates: none
#   cleanup: none
#
# id: check_ptcna_critical_result_digest
#   proves: ptcna_critical_result_content_addressed
#   call: self::test_sealed_result_digest_and_independent_verdict_replay
#   requires: python3
#   timeout: 30
#   mutates: none
#   cleanup: none
# === END CHECKS ===


def test_critical_plan_is_balanced_and_digest_locked() -> None:
    plan, artifact = load_frozen_plan()
    counts = {ring: 0 for ring in ("phi", "psi", "omega")}
    for case in plan.workload:
        counts[case.expected_winner] += 1
    assert counts == {"phi": 6, "psi": 6, "omega": 6}
    assert plan.digest == artifact["plan_digest"]
    assert plan.minimum_target_accuracy == 0.75
    assert plan.minimum_target_advantage_vs_fallback == 0.05
    assert artifact["claim_rules"]["parity"] == "FALSIFIED for superiority only"
    assert len(_canonical_digest(artifact)) == 64


def test_sealed_result_digest_and_independent_verdict_replay() -> None:
    result_path = (
        Path(__file__).resolve().parents[1]
        / "data/ptcna-critical-result-v1.json"
    )
    result = json.loads(result_path.read_text(encoding="utf-8"))
    recorded_digest = result.pop("result_digest")
    assert _canonical_digest(result) == recorded_digest

    plan, _ = load_frozen_plan()
    receipt = result["receipt"]
    target = receipt["target_accuracy"]
    comparator = receipt["comparator_accuracy"]
    usefulness = (
        SURVIVED_NOT_PROVED
        if target >= plan.minimum_target_accuracy
        else FALSIFIED
    )
    superiority = (
        SURVIVED_NOT_PROVED
        if target - comparator >= plan.minimum_target_advantage_vs_fallback
        else FALSIFIED
    )
    assert usefulness == receipt["usefulness_status"] == FALSIFIED
    assert superiority == receipt["superiority_status"] == FALSIFIED
