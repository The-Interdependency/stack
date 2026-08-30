"""Fresh-making derivation specs, keys, receipts, and affected closure."""
from __future__ import annotations

# === MODULE_BUILD ===
# id: stack_freshness_engine
#   module_name: freshness_engine
#   module_kind: engine
#   summary: stores derivation specs, computes freshness keys, evaluates accepted receipts, and derives minimal affected closure
#   owner: stack
#   public_surface: SpecStore, FreshnessReport, freshness_key, write_receipt
#   storage_boundary: write
#   network_boundary: none
#   tests: backend.tests.test_orchestrator
#   rollout: first consumed by backend.msdmd
#   rollback: stop callers; spec and receipt files are untracked operational evidence
# === END MODULE_BUILD ===

# === CONTRACTS ===
# id: stack_freshness_identity_not_time
#   given: a derivation specification and runtime execution metadata
#   then: freshness identity binds exact inputs, generator, verifier, outputs, dependencies, and schema but excludes timestamps and executor choice
#   class: provenance
#
# id: stack_freshness_affected_closure_minimal
#   given: one or more changed derivation targets
#   then: affected_closure returns only those targets and their transitive dependents in dependency order
#   class: efficiency
#
# id: stack_freshness_hmmm_fail_closed
#   given: a required input, generator, or verifier identity is unresolved
#   then: the target reports hmmm rather than fresh
#   class: correctness
# === END CONTRACTS ===

from dataclasses import dataclass, asdict
import hashlib
import json
import os
from pathlib import Path
from typing import Any, Iterable

from .jobs import JobLedger


SPEC_SCHEMA = "the-interdependency.fresh-making-spec"
SPEC_VERSION = "1.0.0"
RECEIPT_SCHEMA = "the-interdependency.fresh-making-receipt"
RECEIPT_VERSION = "1.0.0"


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: str | Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def tree_sha256(root: str | Path, *, suffixes: tuple[str, ...] = (".py",)) -> str:
    """Digest a code tree including relative paths and bytes."""
    base = Path(root).resolve()
    if not base.is_dir():
        raise FileNotFoundError(base)
    digest = hashlib.sha256()
    files = sorted(
        path for path in base.rglob("*")
        if path.is_file() and (not suffixes or path.suffix in suffixes)
    )
    if not files:
        raise ValueError(f"no generator files found under {base}")
    for path in files:
        relative = path.relative_to(base).as_posix().encode("utf-8")
        digest.update(relative)
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def _required_spec_fields(spec: dict[str, Any]) -> None:
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
    _required_spec_fields(spec)
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
    unresolved: list[str] = []
    for item in spec.get("inputs", []):
        identity = str(item.get("identity", ""))
        if not identity or identity == "hmmm" or "hmmm" in identity:
            unresolved.append(str(item.get("name", "input")))
    for section in ("generator", "verifier"):
        identity = str(spec.get(section, {}).get("identity", ""))
        if not identity or identity == "hmmm" or "hmmm" in identity:
            unresolved.append(section)
    return unresolved


def _safe_name(target: str) -> str:
    return hashlib.sha256(target.encode("utf-8")).hexdigest()[:24]


class SpecStore:
    """JSON derivation-spec store colocated with the SQLite operational state."""

    def __init__(self, state_dir: str | Path):
        self.state_dir = Path(state_dir)
        self.root = self.state_dir / "specs"
        self.root.mkdir(parents=True, exist_ok=True)

    def path_for(self, target: str) -> Path:
        return self.root / f"{_safe_name(target)}.json"

    def put(self, spec: dict[str, Any]) -> Path:
        _required_spec_fields(spec)
        path = self.path_for(spec["target"])
        tmp = path.with_suffix(".json.tmp")
        tmp.write_text(json.dumps(spec, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        os.replace(tmp, path)
        return path

    def get(self, target: str) -> dict[str, Any]:
        path = self.path_for(target)
        if not path.is_file():
            raise KeyError(target)
        spec = json.loads(path.read_text(encoding="utf-8"))
        _required_spec_fields(spec)
        if spec["target"] != target:
            raise ValueError(f"spec path/target mismatch: {target} != {spec['target']}")
        return spec

    def list(self) -> list[dict[str, Any]]:
        specs: list[dict[str, Any]] = []
        for path in sorted(self.root.glob("*.json")):
            spec = json.loads(path.read_text(encoding="utf-8"))
            _required_spec_fields(spec)
            specs.append(spec)
        return specs

    def affected_closure(self, changed_targets: Iterable[str]) -> list[str]:
        specs = {spec["target"]: spec for spec in self.list()}
        reverse: dict[str, set[str]] = {target: set() for target in specs}
        for target, spec in specs.items():
            for dependency in spec.get("depends_on", []):
                reverse.setdefault(str(dependency), set()).add(target)

        selected = set(str(target) for target in changed_targets)
        queue = list(selected)
        while queue:
            current = queue.pop(0)
            for dependent in sorted(reverse.get(current, set())):
                if dependent not in selected:
                    selected.add(dependent)
                    queue.append(dependent)

        indegree = {target: 0 for target in selected}
        for target in selected:
            spec = specs.get(target)
            if spec is None:
                continue
            for dependency in spec.get("depends_on", []):
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
    receipt_path: str | None
    active_job_id: str | None
    reason: str
    hmmm: list[str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def receipt_payload(*, spec: dict[str, Any], key: str,
                    outputs: list[dict[str, str]], verifier_identity: str,
                    executor: str, attempt_id: str, made_fresh_at: str) -> dict[str, Any]:
    return {
        "schema": RECEIPT_SCHEMA,
        "version": RECEIPT_VERSION,
        "target": spec["target"],
        "freshness_key_sha256": key,
        "inputs": spec["inputs"],
        "generator": spec["generator"],
        "outputs": outputs,
        "verification": {
            "verifier_identity": verifier_identity,
            "result": "pass",
        },
        "executor": {
            "kind": executor,
            "attempt_id": attempt_id,
        },
        "made_fresh_at": made_fresh_at,
        "hmmm": [],
    }


def write_receipt(state_dir: str | Path, payload: dict[str, Any]) -> Path:
    target = str(payload["target"])
    key = str(payload["freshness_key_sha256"])
    directory = Path(state_dir) / "receipts" / _safe_name(target)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / f"{key}.json"
    tmp = path.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    os.replace(tmp, path)
    return path


def read_receipt(path: str | Path) -> dict[str, Any]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if data.get("schema") != RECEIPT_SCHEMA or data.get("version") != RECEIPT_VERSION:
        raise ValueError("unsupported fresh-making receipt schema/version")
    return data


def base_report(ledger: JobLedger, spec: dict[str, Any]) -> FreshnessReport:
    """Evaluate identity/receipt relationship before kind-specific verification."""
    unresolved = unresolved_identities(spec)
    desired = None if unresolved else freshness_key(spec)
    acceptance = ledger.get_acceptance(spec["target"])
    active = ledger.active_job_for_target(spec["target"])
    if unresolved:
        return FreshnessReport(
            target=spec["target"], state="hmmm", diagnosis="unresolved",
            desired_freshness_key=None,
            accepted_freshness_key=acceptance.freshness_key if acceptance else None,
            receipt_path=acceptance.receipt_path if acceptance else None,
            active_job_id=active.id if active else None,
            reason="required identities are unresolved",
            hmmm=[f"unresolved identity: {name}" for name in unresolved],
        )
    if active and active.freshness_key == desired:
        return FreshnessReport(
            target=spec["target"], state="making-fresh", diagnosis="in-progress",
            desired_freshness_key=desired,
            accepted_freshness_key=acceptance.freshness_key if acceptance else None,
            receipt_path=acceptance.receipt_path if acceptance else None,
            active_job_id=active.id,
            reason=f"fresh-making job is {active.state}", hmmm=[],
        )
    if acceptance is None:
        return FreshnessReport(
            target=spec["target"], state="making-fresh", diagnosis="no-accepted-receipt",
            desired_freshness_key=desired, accepted_freshness_key=None,
            receipt_path=None, active_job_id=None,
            reason="no accepted receipt exists for the desired derivation", hmmm=[],
        )
    if acceptance.freshness_key != desired:
        return FreshnessReport(
            target=spec["target"], state="making-fresh", diagnosis="identity-changed",
            desired_freshness_key=desired, accepted_freshness_key=acceptance.freshness_key,
            receipt_path=acceptance.receipt_path, active_job_id=None,
            reason="accepted receipt binds a different freshness key", hmmm=[],
        )
    if not Path(acceptance.receipt_path).is_file():
        return FreshnessReport(
            target=spec["target"], state="hmmm", diagnosis="receipt-missing",
            desired_freshness_key=desired, accepted_freshness_key=acceptance.freshness_key,
            receipt_path=acceptance.receipt_path, active_job_id=None,
            reason="accepted receipt path is missing", hmmm=["accepted receipt cannot be read"],
        )
    return FreshnessReport(
        target=spec["target"], state="fresh", diagnosis="receipt-key-match",
        desired_freshness_key=desired, accepted_freshness_key=acceptance.freshness_key,
        receipt_path=acceptance.receipt_path, active_job_id=None,
        reason="receipt key matches current derivation identities; kind verifier still required",
        hmmm=[],
    )
