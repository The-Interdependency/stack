"""Fresh-making derivation identity, receipts, and affected-closure logic."""
from __future__ import annotations

# === MODULE_BUILD ===
# id: stack_freshness_engine
#   module_name: freshness_engine
#   module_kind: engine
#   summary: computes deterministic freshness identities, fail-closed unresolved states, receipts, and minimal affected closure
#   owner: stack
#   public_surface: freshness_key, affected_closure, FreshnessReport, base_report, receipt_payload
#   auth_boundary: none
#   storage_boundary: none
#   network_boundary: none
#   tests: backend.tests.test_orchestrator
#   rollout: consumed by derivation adapters and the operator CLI
#   rollback: remove callers; no persistent state is owned here
# === END MODULE_BUILD ===

# === CONTRACTS ===
# id: stack_freshness_identity_not_time
#   given: a derivation specification and incidental runtime metadata
#   then: freshness binds exact inputs, generator, verifier, outputs, dependencies, and schema but excludes timestamps and executor choice
#   class: provenance
#
# id: stack_freshness_hmmm_fail_closed
#   given: a required input, generator, or verifier identity is unresolved
#   then: the target reports hmmm rather than fresh
#   class: correctness
#
# id: stack_freshness_affected_closure_minimal
#   given: one or more changed derivation targets
#   then: affected closure contains only those targets and their transitive dependents in dependency order
#   class: efficiency
# === END CONTRACTS ===

from dataclasses import dataclass, asdict
import hashlib
import json
from typing import Any, Iterable, Protocol

SPEC_SCHEMA = "the-interdependency.fresh-making-spec"
SPEC_VERSION = "1.0.0"
RECEIPT_SCHEMA = "the-interdependency.fresh-making-receipt"
RECEIPT_VERSION = "1.0.0"


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _validate_spec(spec: dict[str, Any]) -> None:
    if spec.get("schema") != SPEC_SCHEMA or spec.get("version") != SPEC_VERSION:
        raise ValueError("unsupported fresh-making spec schema/version")
    for field in ("target", "kind", "inputs", "generator", "outputs", "verifier", "depends_on"):
        if field not in spec:
            raise ValueError(f"fresh-making spec missing {field}")
    if not isinstance(spec["target"], str) or not spec["target"]:
        raise ValueError("fresh-making target must be a non-empty string")
    if not isinstance(spec["inputs"], list) or not isinstance(spec["outputs"], list):
        raise ValueError("fresh-making inputs/outputs must be lists")
    if not isinstance(spec["depends_on"], list):
        raise ValueError("fresh-making depends_on must be a list")


def identity_material(spec: dict[str, Any]) -> dict[str, Any]:
    """Return only fields whose change semantically invalidates the derivation."""
    _validate_spec(spec)
    return {
        "schema": spec["schema"],
        "version": spec["version"],
        "target": spec["target"],
        "kind": spec["kind"],
        "inputs": spec["inputs"],
        "generator": spec["generator"],
        "outputs": spec["outputs"],
        "verifier": spec["verifier"],
        "depends_on": spec["depends_on"],
    }


def freshness_key(spec: dict[str, Any]) -> str:
    return sha256_bytes(canonical_json(identity_material(spec)).encode("utf-8"))


def unresolved_identities(spec: dict[str, Any]) -> list[str]:
    _validate_spec(spec)
    unresolved: list[str] = []
    for item in spec["inputs"]:
        identity = str(item.get("identity", ""))
        if not identity or identity == "hmmm" or "hmmm" in identity:
            unresolved.append(str(item.get("name", "input")))
    for section in ("generator", "verifier"):
        identity = str(spec.get(section, {}).get("identity", ""))
        if not identity or identity == "hmmm" or "hmmm" in identity:
            unresolved.append(section)
    return unresolved


def affected_closure(specs: Iterable[dict[str, Any]], changed_targets: Iterable[str]) -> list[str]:
    """Return changed targets plus transitive dependents in dependency order."""
    indexed: dict[str, dict[str, Any]] = {}
    for spec in specs:
        _validate_spec(spec)
        target = spec["target"]
        if target in indexed:
            raise ValueError(f"duplicate derivation target: {target}")
        indexed[target] = spec

    reverse: dict[str, set[str]] = {target: set() for target in indexed}
    for target, spec in indexed.items():
        for dependency in spec["depends_on"]:
            reverse.setdefault(str(dependency), set()).add(target)

    selected = {str(target) for target in changed_targets}
    queue = list(sorted(selected))
    while queue:
        current = queue.pop(0)
        for dependent in sorted(reverse.get(current, set())):
            if dependent not in selected:
                selected.add(dependent)
                queue.append(dependent)

    indegree = {target: 0 for target in selected}
    for target in selected:
        spec = indexed.get(target)
        if spec is None:
            continue
        for dependency in spec["depends_on"]:
            if dependency in selected:
                indegree[target] += 1

    ready = sorted(target for target, degree in indegree.items() if degree == 0)
    ordered: list[str] = []
    while ready:
        current = ready.pop(0)
        ordered.append(current)
        for dependent in sorted(reverse.get(current, set())):
            if dependent not in indegree:
                continue
            indegree[dependent] -= 1
            if indegree[dependent] == 0:
                ready.append(dependent)
                ready.sort()
    if len(ordered) != len(indegree):
        raise ValueError("fresh-making derivation cycle is blocked")
    return ordered


@dataclass(frozen=True)
class FreshnessReport:
    target: str
    state: str
    diagnosis: str
    desired_freshness_key: str | None
    accepted_freshness_key: str | None
    receipt_id: str | None
    active_job_id: str | None
    reason: str
    hmmm: list[str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class FreshnessLedger(Protocol):
    def get_acceptance(self, target: str): ...
    def active_job_for_target(self, target: str): ...


def base_report(ledger: FreshnessLedger, spec: dict[str, Any]) -> FreshnessReport:
    unresolved = unresolved_identities(spec)
    acceptance = ledger.get_acceptance(spec["target"])
    active = ledger.active_job_for_target(spec["target"])
    if unresolved:
        return FreshnessReport(
            target=spec["target"], state="hmmm", diagnosis="unresolved",
            desired_freshness_key=None,
            accepted_freshness_key=acceptance.freshness_key if acceptance else None,
            receipt_id=acceptance.receipt_id if acceptance else None,
            active_job_id=active.id if active else None,
            reason="required identities are unresolved",
            hmmm=[f"unresolved identity: {name}" for name in unresolved],
        )

    desired = freshness_key(spec)
    if active and active.freshness_key == desired:
        return FreshnessReport(
            target=spec["target"], state="making-fresh", diagnosis="in-progress",
            desired_freshness_key=desired,
            accepted_freshness_key=acceptance.freshness_key if acceptance else None,
            receipt_id=acceptance.receipt_id if acceptance else None,
            active_job_id=active.id,
            reason=f"fresh-making job is {active.state}", hmmm=[],
        )
    if acceptance is None:
        return FreshnessReport(
            target=spec["target"], state="making-fresh", diagnosis="no-accepted-receipt",
            desired_freshness_key=desired, accepted_freshness_key=None,
            receipt_id=None, active_job_id=None,
            reason="no accepted receipt exists for the desired derivation", hmmm=[],
        )
    if acceptance.freshness_key != desired:
        return FreshnessReport(
            target=spec["target"], state="making-fresh", diagnosis="identity-changed",
            desired_freshness_key=desired, accepted_freshness_key=acceptance.freshness_key,
            receipt_id=acceptance.receipt_id, active_job_id=None,
            reason="accepted receipt binds a different freshness key", hmmm=[],
        )
    return FreshnessReport(
        target=spec["target"], state="fresh", diagnosis="receipt-key-match",
        desired_freshness_key=desired, accepted_freshness_key=acceptance.freshness_key,
        receipt_id=acceptance.receipt_id, active_job_id=None,
        reason="receipt key matches current derivation identities; kind verifier still required",
        hmmm=[],
    )


def receipt_payload(*, spec: dict[str, Any], key: str, outputs: list[dict[str, str]],
                    verifier_identity: str, executor: str, attempt_id: str,
                    made_fresh_at: str) -> dict[str, Any]:
    _validate_spec(spec)
    return {
        "schema": RECEIPT_SCHEMA,
        "version": RECEIPT_VERSION,
        "target": spec["target"],
        "freshness_key_sha256": key,
        "inputs": spec["inputs"],
        "generator": spec["generator"],
        "outputs": outputs,
        "verification": {"verifier_identity": verifier_identity, "result": "pass"},
        "executor": {"kind": executor, "attempt_id": attempt_id},
        "made_fresh_at": made_fresh_at,
        "hmmm": [],
    }
