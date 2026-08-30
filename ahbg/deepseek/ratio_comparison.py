# ratios: loc_comments=157:11 imports_exports=5:4 calls_definitions=33:4


"""DeepCode AHBG calibration — ratio comparisons across all six reviews.

All six directional reviews share the same 13 check ids from the frozen
protocol, so per-check agreement and pass ratios are directly computable.
Outputs:

    reviews/RATIO_COMPARISON.json
    reviews/RATIO_COMPARISON.md

Usage:

    python3 -m ahbg.deepseek.ratio_comparison
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any

REVIEWS_DIR = Path(__file__).resolve().parent / "reviews"

SHARED_IDS = [
    "deterministic_scenario_validation",
    "event_ordering_and_lineage_integrity",
    "replay_equivalence",
    "no_silent_cross_instance_state_leakage",
    "known_neutral_vs_unknown",
    "hard_veto_removes_action",
    "task_value_separate_from_regulatory_burden",
    "voluntary_disengagement_capacity_preserving",
    "scope_contraction_changes_admitted_surface",
    "apparent_decoupling_delayed_cost",
    "hierarchical_models_vs_simpler_controls",
    "provider_identity_is_relation",
    "unit_tests",
]

SIBLING_REVIEWS = {
    "grok->codex": ("origin/agent/ahbg-grok", "ahbg/grok/reviews/codex-review.json"),
    "grok->deepcode": ("origin/agent/ahbg-grok", "ahbg/grok/reviews/deepcode-review.json"),
    "codex->grok": ("origin/agent/ahbg-codex", "ahbg/codex/reviews/grok-review.json"),
    "codex->deepcode": ("origin/agent/ahbg-codex", "ahbg/codex/reviews/deepcode-review.json"),
}

LOCAL_REVIEWS = {
    "deepcode->grok": "grok-review.json",
    "deepcode->codex": "codex-review.json",
}


def load_sibling(ref: str, path: str) -> dict[str, Any]:
    out = subprocess.check_output(["git", "show", f"{ref}:{path}"], text=True)
    return json.loads(out)


def load_local(name: str) -> dict[str, Any]:
    return json.loads((REVIEWS_DIR / name).read_text(encoding="utf-8"))


def checks_by_id(review: dict[str, Any]) -> dict[str, str]:
    return {c.get("id"): c.get("result") for c in review.get("checks", []) if c.get("id") in SHARED_IDS}


def main() -> None:
    reviews: dict[str, dict[str, Any]] = {}
    for direction, (ref, path) in SIBLING_REVIEWS.items():
        reviews[direction] = load_sibling(ref, path)
    for direction, name in LOCAL_REVIEWS.items():
        reviews[direction] = load_local(name)

    directions = {}
    for direction, review in reviews.items():
        by_id = checks_by_id(review)
        passed = sum(1 for r in by_id.values() if r == "PASS")
        unresolved = sum(1 for r in by_id.values() if r == "UNRESOLVED")
        failed = sum(1 for r in by_id.values() if r not in ("PASS", "UNRESOLVED"))
        directions[direction] = {
            "checker": direction.split("->")[0],
            "subject": direction.split("->")[1],
            "standing": review.get("evidence_standing"),
            "checks": len(by_id),
            "pass": passed,
            "unresolved": unresolved,
            "failed": failed,
            "pass_ratio": round(passed / len(by_id), 3) if by_id else None,
        }

    # Per-subject checker agreement on the 13 shared ids.
    subjects = {"grok": ["codex->grok", "deepcode->grok"], "codex": ["grok->codex", "deepcode->codex"], "deepcode": ["grok->deepcode", "codex->deepcode"]}
    subject_agreement = {}
    for subject, pair in subjects.items():
        a = checks_by_id(reviews[pair[0]])
        b = checks_by_id(reviews[pair[1]])
        agree = 0
        disagreements = []
        for check_id in SHARED_IDS:
            if a.get(check_id) == b.get(check_id):
                agree += 1
            else:
                disagreements.append({"id": check_id, pair[0]: a.get(check_id), pair[1]: b.get(check_id)})
        subject_agreement[subject] = {
            "checkers": pair,
            "agreement_ratio": round(agree / len(SHARED_IDS), 3),
            "disagreements": disagreements,
            "standing_agreement": reviews[pair[0]].get("evidence_standing") == reviews[pair[1]].get("evidence_standing"),
        }

    # Per-check consensus across all six reviews.
    consensus = {}
    for check_id in SHARED_IDS:
        results = [checks_by_id(r).get(check_id) for r in reviews.values()]
        consensus[check_id] = {
            "pass": results.count("PASS"),
            "unresolved": results.count("UNRESOLVED"),
            "other": len(results) - results.count("PASS") - results.count("UNRESOLVED"),
            "total": len(results),
        }

    total_pass = sum(c["pass"] for c in consensus.values())
    total_unresolved = sum(c["unresolved"] for c in consensus.values())
    total_checks = sum(c["total"] for c in consensus.values())
    overall = {
        "six_review_standing_agreement": all(r["standing"] == "SURVIVED" for r in directions.values()),
        "survived_directions": sum(1 for r in directions.values() if r["standing"] == "SURVIVED"),
        "total_directions": len(directions),
        "shared_checks_total": total_checks,
        "shared_pass_total": total_pass,
        "shared_unresolved_total": total_unresolved,
        "shared_pass_ratio": round(total_pass / total_checks, 3),
    }

    payload = {
        "schema": "interdependency.ahbg.review-ratios/1.0.0",
        "directions": directions,
        "subject_agreement": subject_agreement,
        "consensus": consensus,
        "overall": overall,
    }
    (REVIEWS_DIR / "RATIO_COMPARISON.json").write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    md = [
        "# DeepCode AHBG calibration — ratio comparisons across all six reviews",
        "",
        "## Per-direction ratios (shared 13-check framework)",
        "",
        "| direction | standing | checks | PASS | UNRESOLVED | FAILED | pass ratio |",
        "|---|---|---|---|---|---|---|",
    ]
    for direction, r in directions.items():
        md.append(f"| {direction} | {r['standing']} | {r['checks']} | {r['pass']} | {r['unresolved']} | {r['failed']} | {r['pass_ratio']} |")
    md += [
        "",
        "## Per-subject checker agreement",
        "",
        "| subject | checkers | agreement ratio | standing agreement | disagreements |",
        "|---|---|---|---|---|",
    ]
    for subject, a in subject_agreement.items():
        md.append(f"| {subject} | {', '.join(a['checkers'])} | {a['agreement_ratio']} | {a['standing_agreement']} | {len(a['disagreements'])} |")
    md += [
        "",
        "## Per-check consensus (PASS / UNRESOLVED across six reviews)",
        "",
        "| check id | PASS | UNRESOLVED | consensus |",
        "|---|---|---|---|",
    ]
    for check_id, c in consensus.items():
        if c["pass"] == c["total"]:
            consensus_label = "PASS"
        elif c["unresolved"] == c["total"]:
            consensus_label = "UNRESOLVED"
        else:
            consensus_label = "MIXED"
        md.append(f"| {check_id} | {c['pass']} | {c['unresolved']} | {consensus_label} |")
    md += [
        "",
        "## Overall",
        "",
        f"- Six-review standing agreement (all SURVIVED): {overall['six_review_standing_agreement']}",
        f"- Survived directions: {overall['survived_directions']}/{overall['total_directions']}",
        f"- Shared checks: {overall['shared_checks_total']} (PASS {overall['shared_pass_total']}, UNRESOLVED {overall['shared_unresolved_total']})",
        f"- Overall shared pass ratio: {overall['shared_pass_ratio']}",
        "",
        "Agreement is replication evidence, not truth by vote. Disagreements remain",
        "`hmmm` and are preserved in each checker's divergence register.",
    ]
    (REVIEWS_DIR / "RATIO_COMPARISON.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print(json.dumps(overall, indent=2))


if __name__ == "__main__":
    main()
# ratios: loc_comments=157:11 imports_exports=5:4 calls_definitions=33:4
