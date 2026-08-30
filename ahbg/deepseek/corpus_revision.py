# ratios: loc_comments=110:11 imports_exports=7:4 calls_definitions=18:5
"""DeepCode AHBG shared corpus revision proposal generator (war_v3).

Emits the machine-readable revision proposal that re-grades the two War
collision scenarios after the canonical deterministic War resolver landed:

    corpus-revision-proposal/corpus-revision.json
    corpus-revision-proposal/CORPUS_REVISION.sha256
    corpus-revision-proposal/CORPUS_REVISION.md

The sealed corpus (calibration-family 1.0.0-proposal-1, digest
b05cba2c...e5e0) is not edited in place; this is a successor proposal whose
canonical digest changes only because the two collision scenarios lose their
``standing_override`` and their notes describe the resolved War outcomes.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any

from .scenarios import SCENARIOS, TILES, UNITS

REVISION_DIR = Path(__file__).resolve().parent / "corpus-revision-proposal"

CORPUS_SCHEMA = "interdependency.ahbg.calibration-corpus/1.0.0"
CORPUS_ID = "calibration-family"
REVISION_VERSION = "1.0.1-proposal-1"

PREDECESSOR = {
    "proposal_version": "1.0.0-proposal-1",
    "canonical_scenarios_sha256": "b05cba2cf2f15583548cc15158f09e2612545c978b6a42ddeb314f1e4ed0e5e0",
    "merged_to_main": "3a92c7b0f8568e6fc2600b45bca760030ea2ba3f",
    "pr": 5,
}

WAR_SCENARIO_IDS = {"occupied_target_collision", "dual_target_collision"}
WAR_NOTE = (
    "War collision resolver resolved deterministically (war_v3): occupied target -> "
    "defender holds; dual target -> smallest unit_id wins priority. Outcomes emit "
    "explicit war events and replay equal."
)


def canonical_json(obj: Any) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def _head_sha() -> str:
    return subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()


def revised_scenarios() -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for spec in SCENARIOS:
        entry = dict(spec)
        if entry.get("id") in WAR_SCENARIO_IDS:
            entry.pop("standing_override", None)
            entry["note"] = WAR_NOTE
        out.append(entry)
    return out


def build_revision() -> dict[str, Any]:
    scenarios = revised_scenarios()
    scenarios_digest = hashlib.sha256(canonical_json(scenarios).encode("utf-8")).hexdigest()
    return {
        "schema": CORPUS_SCHEMA,
        "corpus_id": CORPUS_ID,
        "proposal_version": REVISION_VERSION,
        "status": "proposal",
        "proposed_by": "DeepCode",
        "proposed_build_sha": _head_sha(),
        "predecessor": PREDECESSOR,
        "canonical_scenarios_sha256": scenarios_digest,
        "change_summary": [
            "war_v3 canonical deterministic War resolver (occupied -> defender_holds; dual -> smallest unit_id priority; explicit war events; replay equal)",
            "occupied_target_collision and dual_target_collision lose standing_override UNRESOLVED; their evidence standing is now determined by the run",
            "all other 33 scenarios and their fields are unchanged",
        ],
        "board": {
            "authority": "UCNS mobius_seed band centers (research/ucns/src/ucns/mobius_seed.py)",
            "projection": "axial (q, r) inverse projection of the seven unit-radius Seed-of-Life centerpoints",
            "tiles": TILES,
            "units": UNITS,
        },
        "scenarios": scenarios,
    }


def main() -> None:
    REVISION_DIR.mkdir(parents=True, exist_ok=True)
    corpus = build_revision()
    text = canonical_json(corpus) + "\n"
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()

    (REVISION_DIR / "corpus-revision.json").write_text(text, encoding="utf-8")
    (REVISION_DIR / "CORPUS_REVISION.sha256").write_text(f"{digest}  corpus-revision.json\n", encoding="utf-8")

    md = [
        "# DeepCode shared corpus revision proposal — war_v3",
        "",
        f"- Corpus id: `{CORPUS_ID}`",
        f"- Revision: `{REVISION_VERSION}` (successor to `1.0.0-proposal-1`)",
        "- Predecessor canonical scenarios digest: `b05cba2c…e5e0` (sealed, merged to main via PR #5)",
        f"- Proposed canonical scenarios digest: `{corpus['canonical_scenarios_sha256']}`",
        f"- Corpus file SHA-256: `{digest}`",
        "",
        "## Change",
        "",
        "- Adds the canonical deterministic War resolver (war_v3):",
        "  occupied target -> defender holds; dual target -> smallest `unit_id`",
        "  wins priority; outcomes emit explicit `war` events and replay equal.",
        "- Re-grades exactly two scenarios: `occupied_target_collision` and",
        "  `dual_target_collision` lose their `standing_override: UNRESOLVED`;",
        "  their standing is now determined by the run.",
        "- All other 33 scenarios are unchanged.",
        "",
        "## Adoption procedure",
        "",
        "- Frozen calibration SHAs are not touched.",
        "- The sealed `1.0.0-proposal-1` corpus is not edited in place.",
        "- This revision is sealed only when the other builders record the new",
        "  canonical digest or reject it explicitly.",
        "",
        "## hmmm",
        "",
        "- Whether the other two builders adopt war_v3 or keep fail-closed War.",
        "- Whether build_v2 and hidden threat terrain enter a later revision.",
    ]
    (REVISION_DIR / "CORPUS_REVISION.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print(json.dumps({
        "proposal_version": REVISION_VERSION,
        "predecessor": PREDECESSOR["canonical_scenarios_sha256"],
        "proposed_digest": corpus["canonical_scenarios_sha256"],
        "file_digest": digest,
        "scenario_count": len(corpus["scenarios"]),
        "changed_scenarios": sorted(WAR_SCENARIO_IDS),
    }, indent=2))


if __name__ == "__main__":
    main()
# ratios: loc_comments=110:11 imports_exports=7:4 calls_definitions=18:5
