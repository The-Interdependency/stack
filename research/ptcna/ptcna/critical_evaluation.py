# ratios: loc_comments=49:51 imports_exports=7:3 calls_definitions=21:5
"""Load and execute the preregistered PTCNA critical evaluation.

The plan artifact is frozen before execution. This module refuses a changed
plan digest and writes a content-addressed result receipt only when invoked
explicitly. Loading or testing the plan never constructs either backend.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

from .evaluation import EvaluationCase, EvaluationPlan, evaluate

# === MODULE_BUILD ===
# id: ptcna_critical_evaluation
#   module_name: critical_evaluation
#   module_kind: experiment
#   summary: loads the immutable representative role-acquisition plan and seals its separate usefulness and superiority verdicts
#   owner: Erin Spencer
#   public_surface: load_frozen_plan, execute_frozen_plan, main
#   internal_surface: _artifact_path, _canonical_digest
#   auth_boundary: none
#   storage_boundary: write
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: ptcna/tests/test_critical_evaluation.py
#   rollout: execute only after the preregistration commit is merged
#   rollback: preserve plan and result receipts; remove executable wrapper without changing runtime
#   requires: ptcna_frozen_evaluation
#   since: unreleased
#   unresolved: outcome until the merged frozen plan is executed
# === END MODULE_BUILD ===

# === CONTRACTS ===
# id: ptcna_critical_plan_digest_locked
#   given: the checked-in critical evaluation plan is loaded
#   then: its canonical EvaluationPlan digest must equal the independently stored frozen digest
#   class: evidence
#
# id: ptcna_critical_result_content_addressed
#   given: the frozen plan completes or reaches a frozen failure rule
#   then: the serialized result names the plan digest, separate claim verdicts, and its own canonical result digest
#   class: evidence
# === END CONTRACTS ===

# === BOUNDARIES ===
# id: ptcna_critical_evaluation_local_receipt
#   summary: reads the repository-owned frozen plan and writes one caller-selected local JSON result without network, authentication, secrets, or user data
#   auth_boundary: none
#   storage_boundary: write
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   pii: none
#   secrets: none
#   owner: Erin Spencer
#   since: unreleased
# === END BOUNDARIES ===


def _artifact_path() -> Path:
    return Path(__file__).resolve().parent / "data/ptcna-critical-plan-v1.json"


def _canonical_digest(value: Any) -> str:
    encoded = json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def load_frozen_plan(path: Path | None = None) -> tuple[EvaluationPlan, dict[str, Any]]:
    """Load the preregistration and reject any plan-byte semantic drift."""

    artifact = json.loads((path or _artifact_path()).read_text(encoding="utf-8"))
    values = dict(artifact["plan"])
    values["workload"] = tuple(EvaluationCase(**case) for case in values["workload"])
    plan = EvaluationPlan(**values)
    if plan.digest != artifact["plan_digest"]:
        raise ValueError("frozen critical evaluation plan digest mismatch")
    return plan, artifact


def execute_frozen_plan(output: Path) -> dict[str, Any]:
    """Execute exactly the frozen plan and seal its result receipt."""

    plan, artifact = load_frozen_plan()
    receipt = evaluate(plan)
    result = {
        "schema": "ptcna.critical-evaluation-result",
        "schema_version": "1.0.0",
        "source_commit": artifact["source_commit"],
        "plan_digest": plan.digest,
        "claim_rules": artifact["claim_rules"],
        "receipt": receipt.to_dict(),
    }
    result["result_digest"] = _canonical_digest(result)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    result = execute_frozen_plan(args.output)
    print(json.dumps(result, sort_keys=True, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
# ratios: loc_comments=49:51 imports_exports=7:3 calls_definitions=21:5
