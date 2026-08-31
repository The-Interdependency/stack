"""Aggregate AHBG burden and hierarchy evidence across local worktrees.

The runner is deliberately local, deterministic, and stdlib-only. It reads the
current Grok, Codex, and DeepCode successor-corpus artifacts plus DeepCode's
bounded live-provider extension runs. It reports evidence coverage and keeps
unfit models as hmmm/UNRESOLVED rather than inventing certainty.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


AHBG_ROOT = Path(__file__).resolve().parent
STACK_ROOT = AHBG_ROOT.parent
SRC_ROOT = STACK_ROOT.parent
DEFAULT_OUT_DIR = AHBG_ROOT / "burden-coupling"

CORPUS_RUN = "calibration-family-1.0.1-proposal-1"
CORPUS_PATH = AHBG_ROOT / "deepseek" / "corpus-proposal" / "corpus.json"

COMMON_INPUTS = {
    "Grok": SRC_ROOT
    / "stack"
    / "ahbg"
    / "grok"
    / "corpus-run"
    / CORPUS_RUN
    / "CALIBRATION_RESULT.json",
    "Codex": SRC_ROOT
    / "stack-codex"
    / "ahbg"
    / "codex"
    / "corpus-run"
    / CORPUS_RUN
    / "CALIBRATION_RESULT.json",
    "DeepCode": SRC_ROOT
    / "stack-deepcode"
    / "ahbg"
    / "deepseek"
    / "artifacts"
    / "CALIBRATION_RESULT.json",
}

DEEPCODE_EXTENSIONS = {
    "epoch3_live_provider": SRC_ROOT
    / "stack-deepcode"
    / "ahbg"
    / "deepseek"
    / "epoch3"
    / "RESULT.json",
    "whole_system_game": SRC_ROOT
    / "stack-deepcode"
    / "ahbg"
    / "deepseek"
    / "game"
    / "RESULT.json",
}

STANDINGS = ("SURVIVED", "UNRESOLVED", "FALSIFIED", "BLOCKED")
CORE_BURDEN_TERMS = ("tokens", "latency_ms", "retries", "tool_calls")
TERM_ALIASES = {
    "tokens": ("tokens", "token"),
    "latency_ms": ("latency",),
    "retries": ("retries", "retry"),
    "tool_calls": ("tool_calls",),
    "tool_failures": ("tool_failures",),
    "memory_reads": ("memory_reads", ".reads"),
    "memory_writes": ("memory_writes", ".writes"),
}
PERMISSION_AXES = ("allowed_to_be", "allowed_to_do", "wanted_here", "wanted_to_do")


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(SRC_ROOT))
    except ValueError:
        return str(path)


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def read_jsonl(path: Path) -> tuple[list[dict[str, Any]], list[str]]:
    records: list[dict[str, Any]] = []
    errors: list[str] = []
    if not path.exists():
        return records, [f"missing: {rel(path)}"]
    for index, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            value = json.loads(line)
        except json.JSONDecodeError as exc:
            errors.append(f"{rel(path)}:{index}: {exc.msg}")
            continue
        if isinstance(value, dict):
            records.append(value)
        else:
            errors.append(f"{rel(path)}:{index}: non-object JSONL record")
    return records, errors


def is_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def walk(value: Any, prefix: str = "") -> list[tuple[str, Any]]:
    if isinstance(value, dict):
        leaves: list[tuple[str, Any]] = []
        for key, child in value.items():
            child_prefix = f"{prefix}.{key}" if prefix else str(key)
            leaves.extend(walk(child, child_prefix))
        return leaves
    if isinstance(value, list):
        leaves = []
        for index, child in enumerate(value):
            leaves.extend(walk(child, f"{prefix}[{index}]"))
        return leaves
    return [(prefix, value)]


def contains_nonempty_key(value: Any, key: str) -> bool:
    if isinstance(value, dict):
        for child_key, child_value in value.items():
            if child_key == key and bool(child_value):
                return True
            if contains_nonempty_key(child_value, key):
                return True
    if isinstance(value, list):
        return any(contains_nonempty_key(item, key) for item in value)
    return False


def term_for_path(path: str) -> str | None:
    lower = f".{path.lower()}"
    for term, aliases in TERM_ALIASES.items():
        for alias in aliases:
            if alias.startswith("."):
                if lower.endswith(alias):
                    return term
            elif alias in lower:
                return term
    return None


def normalized_summary(summary: dict[str, Any] | None) -> dict[str, int]:
    counts = {standing: 0 for standing in STANDINGS}
    for key, value in (summary or {}).items():
        standing = str(key).upper()
        if standing in counts and is_number(value):
            counts[standing] = int(value)
    return counts


def telemetry_path(result_path: Path, scenario_id: str) -> Path:
    return result_path.parent / scenario_id / "telemetry.jsonl"


def collect_telemetry(path: Path) -> dict[str, Any]:
    records, errors = read_jsonl(path)
    numeric_counts: Counter[str] = Counter()
    hmmm_counts: Counter[str] = Counter()
    raw_sums: defaultdict[str, float] = defaultdict(float)
    permission_axes = set()
    resource_records = 0
    shadow_records = 0
    nonempty_coupling = 0
    nonempty_impedance = 0
    nonempty_scope_log = 0

    for record in records:
        kind = str(record.get("kind", ""))
        if kind == "resource.telemetry":
            resource_records += 1
        if kind == "regulatory.shadow" or "shadow" in record:
            shadow_records += 1
        if contains_nonempty_key(record, "coupling_weights"):
            nonempty_coupling += 1
        if contains_nonempty_key(record, "impedance"):
            nonempty_impedance += 1
        if contains_nonempty_key(record, "scope_log"):
            nonempty_scope_log += 1

        for leaf_path, value in walk(record):
            lower_path = leaf_path.lower()
            for axis in PERMISSION_AXES:
                if axis in lower_path and is_number(value):
                    permission_axes.add(axis)
            term = term_for_path(leaf_path)
            if term is None:
                continue
            if is_number(value):
                numeric_counts[term] += 1
                raw_sums[term] += float(value)
            elif value == "hmmm":
                hmmm_counts[term] += 1

    return {
        "path": rel(path),
        "records": len(records),
        "parse_errors": errors,
        "resource_records": resource_records,
        "shadow_records": shadow_records,
        "numeric_terms": sorted(numeric_counts),
        "hmmm_terms": sorted(hmmm_counts),
        "term_numeric_counts": dict(sorted(numeric_counts.items())),
        "term_hmmm_counts": dict(sorted(hmmm_counts.items())),
        "term_raw_sums": {key: round(value, 3) for key, value in sorted(raw_sums.items())},
        "permission_axes": sorted(permission_axes),
        "nonempty_coupling_records": nonempty_coupling,
        "nonempty_impedance_records": nonempty_impedance,
        "nonempty_scope_log_records": nonempty_scope_log,
    }


def collect_builder(name: str, result_path: Path) -> dict[str, Any]:
    data = read_json(result_path)
    results = data.get("results", [])
    if not isinstance(results, list):
        raise ValueError(f"{rel(result_path)} has non-list results")

    scenarios: dict[str, dict[str, Any]] = {}
    totals: Counter[str] = Counter()
    regulatory: Counter[str] = Counter()
    numeric_scenarios: defaultdict[str, set[str]] = defaultdict(set)
    hmmm_scenarios: defaultdict[str, set[str]] = defaultdict(set)
    raw_sums: defaultdict[str, float] = defaultdict(float)
    parse_errors: list[str] = []

    for row in results:
        scenario_id = str(row.get("scenario_id", "hmmm"))
        telemetry = collect_telemetry(telemetry_path(result_path, scenario_id))
        parse_errors.extend(telemetry["parse_errors"])

        for term in telemetry["numeric_terms"]:
            numeric_scenarios[term].add(scenario_id)
        for term in telemetry["hmmm_terms"]:
            hmmm_scenarios[term].add(scenario_id)
        for term, value in telemetry["term_raw_sums"].items():
            raw_sums[term] += float(value)

        totals["events"] += int(row.get("event_count") or 0)
        totals["telemetry_records_from_result"] += int(row.get("telemetry_records") or 0)
        totals["telemetry_records_from_files"] += int(telemetry["records"])
        totals["turns"] += int(row.get("turns") or 0)
        totals["selected_actions"] += int(row.get("selected_actions") or 0)
        totals["refusals"] += int(row.get("refusals") or 0)
        totals["invalid_actions"] += int(row.get("invalid_actions") or 0)
        totals["unresolved_hmmm"] += int(row.get("unresolved_hmmm") or 0)
        if row.get("replay_equal") is True:
            totals["replay_equal"] += 1
        if telemetry["resource_records"]:
            regulatory["scenarios_with_resource_records"] += 1
        if len(telemetry["permission_axes"]) == len(PERMISSION_AXES):
            regulatory["scenarios_with_permission_vector"] += 1
        if telemetry["shadow_records"]:
            regulatory["scenarios_with_shadow_records"] += 1
        if telemetry["nonempty_coupling_records"]:
            regulatory["scenarios_with_nonempty_coupling_weights"] += 1
        if telemetry["nonempty_impedance_records"]:
            regulatory["scenarios_with_nonempty_impedance"] += 1
        if telemetry["nonempty_scope_log_records"]:
            regulatory["scenarios_with_nonempty_scope_log"] += 1

        scenarios[scenario_id] = {
            "family": row.get("family"),
            "standing": row.get("evidence_standing") or row.get("observed_standing"),
            "turns": row.get("turns"),
            "event_count": row.get("event_count"),
            "telemetry_records": row.get("telemetry_records"),
            "refusals": row.get("refusals"),
            "invalid_actions": row.get("invalid_actions"),
            "selected_actions": row.get("selected_actions"),
            "replay_equal": row.get("replay_equal"),
            "world_digest": row.get("world_digest"),
            "numeric_terms": telemetry["numeric_terms"],
            "hmmm_terms": telemetry["hmmm_terms"],
            "resource_records": telemetry["resource_records"],
            "nonempty_coupling_records": telemetry["nonempty_coupling_records"],
            "nonempty_impedance_records": telemetry["nonempty_impedance_records"],
            "nonempty_scope_log_records": telemetry["nonempty_scope_log_records"],
        }

    scenario_count = len(scenarios)
    coverage = {}
    for term in TERM_ALIASES:
        numeric = len(numeric_scenarios[term])
        hmmm = len(hmmm_scenarios[term])
        coverage[term] = {
            "numeric_scenarios": numeric,
            "hmmm_scenarios": hmmm,
            "numeric_ratio": round(numeric / scenario_count, 3) if scenario_count else 0.0,
            "raw_numeric_sum": round(raw_sums[term], 3),
        }

    return {
        "name": name,
        "result_path": rel(result_path),
        "schema": data.get("schema"),
        "branch": data.get("branch"),
        "builder": data.get("builder"),
        "corpus_file_sha256": data.get("corpus_file_sha256"),
        "canonical_scenarios_sha256": data.get("canonical_scenarios_sha256"),
        "summary": normalized_summary(data.get("summary")),
        "scenario_count": scenario_count,
        "totals": dict(sorted(totals.items())),
        "coverage": coverage,
        "regulatory_coverage": dict(sorted(regulatory.items())),
        "parse_errors": parse_errors,
        "scenarios": dict(sorted(scenarios.items())),
    }


def collect_extension(name: str, path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"name": name, "path": rel(path), "exists": False}
    data = read_json(path)
    totals = data.get("totals") if isinstance(data.get("totals"), dict) else data
    fields = (
        "scenarios",
        "turns_played",
        "energy_calls",
        "energy_decisions",
        "fallback_decisions",
        "tokens_total",
        "latency_ms_total",
        "tool_calls",
        "tool_failures",
        "invalid_actions",
        "refusals",
        "wall_seconds",
        "replay_all_equal",
        "replay_equal",
        "win",
    )
    return {
        "name": name,
        "path": rel(path),
        "exists": True,
        "schema": data.get("schema"),
        "started_at": data.get("started_at"),
        "scalars": {field: totals.get(field) for field in fields if field in totals},
    }


def scope_transition(spec: dict[str, Any]) -> str:
    events = spec.get("scope_events") or []
    if not isinstance(events, list) or not events:
        return "none"
    last = events[-1]
    if isinstance(last, dict) and isinstance(last.get("transition"), str):
        return last["transition"]
    return "none"


def score_predictions(rows: list[dict[str, Any]], field: str) -> dict[str, Any]:
    correct = sum(1 for row in rows if row["actual_transition"] == row[field])
    total = len(rows)
    return {
        "correct": correct,
        "total": total,
        "accuracy": round(correct / total, 3) if total else 0.0,
    }


def collect_hierarchy_fixture(corpus: dict[str, Any]) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    for spec in corpus.get("scenarios", []):
        if not isinstance(spec, dict):
            continue
        impedance = spec.get("impedance") if isinstance(spec.get("impedance"), dict) else {}
        coupling_weights = spec.get("coupling_weights") if isinstance(spec.get("coupling_weights"), dict) else {}
        if spec.get("family") != "coupling" and not impedance and not coupling_weights:
            continue
        total_impedance = sum(float(value) for value in impedance.values() if is_number(value))
        actual = scope_transition(spec)
        impedance_sign = "contract" if total_impedance > 0.0 else "expand"
        rows.append(
            {
                "scenario_id": spec.get("id"),
                "family": spec.get("family"),
                "impedance": dict(sorted(impedance.items())),
                "coupling_weights": dict(sorted(coupling_weights.items())),
                "total_impedance": round(total_impedance, 6),
                "actual_transition": actual,
                "impedance_sign_prediction": impedance_sign,
                "constant_contract_prediction": "contract",
                "constant_expand_prediction": "expand",
                "constant_none_prediction": "none",
            }
        )

    models = {
        "impedance_sign": "impedance_sign_prediction",
        "constant_contract": "constant_contract_prediction",
        "constant_expand": "constant_expand_prediction",
        "constant_none": "constant_none_prediction",
    }
    scores = {name: score_predictions(rows, field) for name, field in models.items()}
    best_simple = max(
        (scores["constant_contract"]["accuracy"], scores["constant_expand"]["accuracy"], scores["constant_none"]["accuracy"]),
        default=0.0,
    )
    impedance_lift = round(scores["impedance_sign"]["accuracy"] - best_simple, 3) if rows else 0.0
    standing = "BLOCKED"
    if rows:
        standing = "UNRESOLVED"
    return {
        "standing": standing,
        "source": rel(CORPUS_PATH),
        "sample_count": len(rows),
        "minimum_claim_sample": 6,
        "scores": scores,
        "impedance_vs_best_simple_lift": impedance_lift,
        "rows": rows,
        "hmmm": [
            "The fixture is enough to exercise a comparator, not enough to validate a general hierarchy law.",
            "Grok and Codex still do not compute impedance into their action policy.",
            "No common scenario defines non-empty coupling_weights.",
        ],
    }


def compare_scenarios(builders: dict[str, dict[str, Any]]) -> dict[str, Any]:
    scenario_ids = sorted({sid for builder in builders.values() for sid in builder["scenarios"]})
    digest_mismatches = []
    standing_mismatches = []
    vectors: dict[str, Any] = {}
    for scenario_id in scenario_ids:
        standings = {}
        digests = {}
        compact = {}
        for name, builder in builders.items():
            row = builder["scenarios"].get(scenario_id)
            if row is None:
                compact[name] = {"missing": True}
                continue
            standing = str(row.get("standing")).upper()
            standings[name] = standing
            if row.get("world_digest"):
                digests[name] = row["world_digest"]
            compact[name] = {
                "standing": standing,
                "family": row.get("family"),
                "event_count": row.get("event_count"),
                "telemetry_records": row.get("telemetry_records"),
                "numeric_terms": row.get("numeric_terms", []),
                "hmmm_terms": row.get("hmmm_terms", []),
                "world_digest": row.get("world_digest"),
            }
        standing_agreement = len(set(standings.values())) <= 1
        digest_agreement = len(set(digests.values())) <= 1
        if not standing_agreement:
            standing_mismatches.append(scenario_id)
        if not digest_agreement:
            digest_mismatches.append(scenario_id)
        vectors[scenario_id] = {
            "standing_agreement": standing_agreement,
            "digest_agreement": digest_agreement,
            "builders": compact,
        }
    return {
        "scenario_count": len(scenario_ids),
        "standing_mismatch_count": len(standing_mismatches),
        "standing_mismatch_scenarios": standing_mismatches,
        "digest_mismatch_count": len(digest_mismatches),
        "digest_mismatch_scenarios": digest_mismatches,
        "vectors": vectors,
    }


def build_payload() -> dict[str, Any]:
    corpus = read_json(CORPUS_PATH)
    builders = {name: collect_builder(name, path) for name, path in COMMON_INPUTS.items()}
    extensions = {name: collect_extension(name, path) for name, path in DEEPCODE_EXTENSIONS.items()}
    scenario_comparison = compare_scenarios(builders)
    hierarchy_fixture = collect_hierarchy_fixture(corpus)

    corpus_hashes = {builder["corpus_file_sha256"] for builder in builders.values()}
    scenario_hashes = {builder["canonical_scenarios_sha256"] for builder in builders.values()}
    all_common_survived = all(
        builder["summary"].get("SURVIVED") == builder["scenario_count"]
        and builder["summary"].get("UNRESOLVED") == 0
        and builder["summary"].get("FALSIFIED") == 0
        and builder["summary"].get("BLOCKED") == 0
        for builder in builders.values()
    )

    comparable_terms = {
        term: all(
            builder["coverage"][term]["numeric_scenarios"] == builder["scenario_count"]
            for builder in builders.values()
        )
        for term in TERM_ALIASES
    }
    core_observables_present = all(comparable_terms[term] for term in CORE_BURDEN_TERMS)
    burden_mapping_fit_present = False
    core_hmmm_placeholders = {
        name: sorted(
            term
            for term in CORE_BURDEN_TERMS
            if builder["coverage"][term]["hmmm_scenarios"]
        )
        for name, builder in builders.items()
    }
    any_coupling_weights = any(
        builder["regulatory_coverage"].get("scenarios_with_nonempty_coupling_weights", 0)
        for builder in builders.values()
    )
    any_impedance = any(
        builder["regulatory_coverage"].get("scenarios_with_nonempty_impedance", 0)
        for builder in builders.values()
    )
    shared_hierarchy_runtime = all(
        builder["regulatory_coverage"].get("scenarios_with_nonempty_impedance", 0)
        for builder in builders.values()
    )
    deepcode_live_tokens = sum(
        int(extension.get("scalars", {}).get("tokens_total") or 0)
        for extension in extensions.values()
        if extension.get("exists")
    )

    oddities = []
    if any(core_hmmm_placeholders.values()):
        oddities.append("Some per-decision burden rows still preserve hmmm placeholders; scenario-level resource rows are the common surface.")
    if not any_coupling_weights:
        oddities.append("No common telemetry contains non-empty coupling_weights.")
    if any_impedance and not shared_hierarchy_runtime:
        oddities.append("DeepCode records non-empty impedance telemetry; Grok and Codex do not yet emit matching runtime vectors.")
    if hierarchy_fixture["sample_count"] < hierarchy_fixture["minimum_claim_sample"]:
        oddities.append("The admitted hierarchy fixture is too small for a general coupling claim.")
    if scenario_comparison["digest_mismatch_count"]:
        oddities.append(f"World digest vectors disagree on {scenario_comparison['digest_mismatch_count']} scenarios.")
    if deepcode_live_tokens:
        oddities.append("DeepCode has live-provider burden evidence, but it is not replicated by Grok and Codex.")

    return {
        "schema": "interdependency.ahbg.burden-coupling/1.2.0",
        "generated_at": utc_now(),
        "runner": rel(Path(__file__).resolve()),
        "common_corpus": CORPUS_RUN,
        "common_inputs": {name: rel(path) for name, path in COMMON_INPUTS.items()},
        "corpus_source": rel(CORPUS_PATH),
        "evidence_standing": {
            "common_corpus_survival": "SURVIVED" if all_common_survived else "UNRESOLVED",
            "org_burden_inventory": "SURVIVED",
            "common_runtime_burden_observables": "SURVIVED" if core_observables_present else "BLOCKED",
            "common_runtime_burden_mapping": "SURVIVED"
            if core_observables_present and burden_mapping_fit_present
            else ("UNRESOLVED" if core_observables_present else "BLOCKED"),
            "hierarchical_fixture_comparator": hierarchy_fixture["standing"],
            "hierarchical_runtime_vectors_shared": "SURVIVED" if shared_hierarchy_runtime else "BLOCKED",
            "hierarchical_coupling_vs_simpler_controls": hierarchy_fixture["standing"],
            "deepcode_live_burden_extension": "SURVIVED" if deepcode_live_tokens else "hmmm",
        },
        "shared_hashes": {
            "corpus_file_sha256_match": len(corpus_hashes) == 1,
            "corpus_file_sha256": sorted(corpus_hashes),
            "canonical_scenarios_sha256_match": len(scenario_hashes) == 1,
            "canonical_scenarios_sha256": sorted(scenario_hashes),
        },
        "builders": builders,
        "scenario_comparison": scenario_comparison,
        "deepcode_extensions": extensions,
        "hierarchical_fixture": hierarchy_fixture,
        "comparability": {
            "common_terms_numeric_in_every_builder": comparable_terms,
            "core_burden_observables_present": core_observables_present,
            "burden_mapping_fit_present": burden_mapping_fit_present,
            "core_burden_terms_with_hmmm_placeholders": core_hmmm_placeholders,
            "nonempty_coupling_weights_any": any_coupling_weights,
            "nonempty_impedance_any": any_impedance,
            "shared_hierarchy_runtime_vectors": shared_hierarchy_runtime,
            "deepcode_live_tokens_total": deepcode_live_tokens,
        },
        "oddities": oddities,
        "recommendations": [
            "Keep burden fitting on scenario-level resource rows until per-decision burden fields are normalized.",
            "Promote impedance telemetry into Grok and Codex before claiming shared runtime hierarchy evidence.",
            "Expand the two-row hierarchy fixture before treating impedance lift as a validated law.",
            "Add non-empty coupling_weights only with a declared update rule and a simpler-control comparator.",
            "Run live-provider burden extensions only as bounded, explicit spend decisions.",
        ],
        "hmmm": [
            "Cross-provider burden fitting remains unresolved.",
            "The hierarchy comparator exists, but the sample is too small and not implemented across all builders.",
            "Remote branch merge and release authority remain outside this local aggregate.",
        ],
    }


def render_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# AHBG burden and coupling aggregate",
        "",
        f"Generated: `{payload['generated_at']}`",
        "",
        "## Provenance",
        "",
        f"- schema: `{payload['schema']}`",
        f"- runner: `{payload['runner']}`",
        f"- corpus source: `{payload['corpus_source']}`",
        f"- common corpus: `{payload['common_corpus']}`",
    ]
    for name, path in payload["common_inputs"].items():
        lines.append(f"- {name}: `{path}`")

    lines += [
        "",
        "## Evidence standings",
        "",
        "| claim | standing |",
        "|---|---|",
    ]
    for claim, standing in payload["evidence_standing"].items():
        lines.append(f"| `{claim}` | `{standing}` |")

    lines += [
        "",
        "## Common corpus scalars",
        "",
        "| builder | scenarios | SURVIVED | events | telemetry rows | refusals | invalid | replay equal |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for name, builder in payload["builders"].items():
        totals = builder["totals"]
        summary = builder["summary"]
        lines.append(
            f"| {name} | {builder['scenario_count']} | {summary['SURVIVED']} | "
            f"{totals.get('events', 0)} | {totals.get('telemetry_records_from_files', 0)} | "
            f"{totals.get('refusals', 0)} | {totals.get('invalid_actions', 0)} | "
            f"{totals.get('replay_equal', 0)} |"
        )

    lines += [
        "",
        "## Runtime term coverage",
        "",
        "| builder | tokens | latency_ms | retries | tool_calls | memory |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for name, builder in payload["builders"].items():
        cells = []
        for term in ("tokens", "latency_ms", "retries", "tool_calls"):
            coverage = builder["coverage"][term]
            cells.append(f"{coverage['numeric_scenarios']}/{builder['scenario_count']} numeric; {coverage['hmmm_scenarios']} hmmm")
        memory_reads = builder["coverage"]["memory_reads"]["numeric_scenarios"]
        memory_writes = builder["coverage"]["memory_writes"]["numeric_scenarios"]
        cells.append(f"reads {memory_reads}; writes {memory_writes}")
        lines.append(f"| {name} | " + " | ".join(cells) + " |")

    fixture = payload["hierarchical_fixture"]
    lines += [
        "",
        "## Hierarchy Fixture Comparator",
        "",
        f"- standing: `{fixture['standing']}`",
        f"- sample count: {fixture['sample_count']}",
        f"- minimum claim sample: {fixture['minimum_claim_sample']}",
        f"- impedance lift vs best constant control: {fixture['impedance_vs_best_simple_lift']}",
        "",
        "| scenario | impedance | actual transition | impedance-sign | constant contract | constant expand | constant none |",
        "|---|---:|---|---|---|---|---|",
    ]
    for row in fixture["rows"]:
        lines.append(
            f"| `{row['scenario_id']}` | {row['total_impedance']} | `{row['actual_transition']}` | "
            f"`{row['impedance_sign_prediction']}` | `{row['constant_contract_prediction']}` | "
            f"`{row['constant_expand_prediction']}` | `{row['constant_none_prediction']}` |"
        )
    lines += [
        "",
        "| model | correct | total | accuracy |",
        "|---|---:|---:|---:|",
    ]
    for name, score in fixture["scores"].items():
        lines.append(f"| `{name}` | {score['correct']} | {score['total']} | {score['accuracy']} |")

    lines += [
        "",
        "## Regulatory Vector Coverage",
        "",
        "| builder | permission vectors | shadow records | non-empty coupling | non-empty impedance | non-empty scope log |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for name, builder in payload["builders"].items():
        reg = builder["regulatory_coverage"]
        lines.append(
            f"| {name} | {reg.get('scenarios_with_permission_vector', 0)} | "
            f"{reg.get('scenarios_with_shadow_records', 0)} | "
            f"{reg.get('scenarios_with_nonempty_coupling_weights', 0)} | "
            f"{reg.get('scenarios_with_nonempty_impedance', 0)} | "
            f"{reg.get('scenarios_with_nonempty_scope_log', 0)} |"
        )

    lines += [
        "",
        "## DeepCode Live Extensions",
        "",
        "| extension | tokens | latency_ms | calls | failures | scope |",
        "|---|---:|---:|---:|---:|---|",
    ]
    for name, extension in payload["deepcode_extensions"].items():
        scalars = extension.get("scalars", {})
        scope = scalars.get("scenarios", scalars.get("turns_played", "hmmm"))
        lines.append(
            f"| `{name}` | {scalars.get('tokens_total', 'hmmm')} | "
            f"{scalars.get('latency_ms_total', 'hmmm')} | "
            f"{scalars.get('energy_calls', 'hmmm')} | "
            f"{scalars.get('tool_failures', 'hmmm')} | {scope} |"
        )

    comparison = payload["scenario_comparison"]
    lines += [
        "",
        "## Scenario Vector Summary",
        "",
        f"- Standing mismatches: {comparison['standing_mismatch_count']}",
        f"- World-digest mismatches: {comparison['digest_mismatch_count']}",
        "- Full per-scenario vectors are in `BURDEN_COUPLING.json`.",
        "",
        "## Oddities",
        "",
    ]
    for oddity in payload["oddities"]:
        lines.append(f"- {oddity}")

    lines += ["", "## Recommendations", ""]
    for item in payload["recommendations"]:
        lines.append(f"- {item}")

    lines += ["", "## hmmm", ""]
    for item in payload["hmmm"]:
        lines.append(f"- {item}")
    lines.append("- Tiny samples make loud graphs; keep the volume down.")
    return "\n".join(lines) + "\n"


def write_outputs(payload: dict[str, Any], out_dir: Path) -> tuple[Path, Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    json_path = out_dir / "BURDEN_COUPLING.json"
    md_path = out_dir / "BURDEN_COUPLING.md"
    json_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    md_path.write_text(render_markdown(payload), encoding="utf-8")
    return json_path, md_path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    parser.add_argument("--no-write", action="store_true")
    args = parser.parse_args()

    payload = build_payload()
    if args.no_write:
        json_path = md_path = Path("hmmm")
    else:
        json_path, md_path = write_outputs(payload, args.out_dir)
    print(
        json.dumps(
            {
                "schema": payload["schema"],
                "generated_at": payload["generated_at"],
                "evidence_standing": payload["evidence_standing"],
                "oddities": len(payload["oddities"]),
                "json": "hmmm" if args.no_write else rel(json_path),
                "markdown": "hmmm" if args.no_write else rel(md_path),
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
