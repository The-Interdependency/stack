# ratios: loc_comments=448:52 imports_exports=8:3 calls_definitions=147:12
"""Audit digital-metrics CONTRACTS/CHECKS without importing inspected modules.

Usage guidance::

    python3 research/digital-metrics/audit_contracts_cli.py \
        --skill-lib-root /path/to/exact/skill-lib

The audit parses source declarations and Python AST only.  It exits nonzero for
unlinked contracts, unknown ``proves`` targets, unresolved ``self::`` calls,
or discoverable ``test_*`` methods without CHECKS declarations.
"""

from __future__ import annotations

# === MODULE_BUILD ===
# id: stack_digital_metric_contract_audit
#   module_name: digital metric contract audit
#   module_kind: instrument
#   summary: fail-closed no-import reconciliation of digital-metrics source obligations and executable witnesses
#   owner: The-Interdependency/stack
#   public_surface: audit,main
#   internal_surface: AST unittest discovery and CONTRACTS/CHECKS graph reconciliation
#   auth_boundary: none
#   storage_boundary: read-only
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: self-auditing against research/digital-metrics/tests/test_metric_protocol.py
#   rollout: explicit local and CI command
#   rollback: remove only if replaced by an equivalent or stricter contract graph audit
#   requires: manifest-pinned skill-lib msdmd parser
#   since: 2026-09-20
#   unresolved: mutation sensitivity is not established by linkage audit alone
# === END MODULE_BUILD ===

# === CONTRACTS ===
# id: digital_metric_contract_audit_requires_discoverable_tests
#   given: a CHECKS call names a top-level, nested, non-TestCase, skipped, expected-failure, or runner-overriding test-like function
#   then: the audit rejects statically ineligible targets; linkage never supplies behavioral proof credit
#   class: provenance
#
# id: digital_metric_contract_audit_binds_parser_identity
#   given: the contract audit parses evidence declarations with the vendored msdmd parser
#   then: it source-loads only bytes whose digest and skill-lib commit match the exact Stack/work-graph pins
#   class: provenance
#
# id: digital_metric_contract_audit_binds_executing_source
#   given: the outer auditor is entered without a source digest or its file changes after load
#   then: audit rejects unless the executing-byte digest equals the captured auditor snapshot
#   class: provenance
#
# id: digital_metric_work_graph_matches_stack_manifest
#   given: the digital-metrics work graph and Stack machine/human manifests project the same workspace
#   then: participant commits, authority, relations, boundaries, and parser identity agree exactly
#   class: provenance
# === END CONTRACTS ===

import ast
import hashlib
import json
from pathlib import Path
import subprocess
import sys
from types import ModuleType


ROOT = Path(__file__).resolve().parent
STACK_ROOT = ROOT.parents[1]
WORK_GRAPH_PATH = ROOT / "WORK_GRAPH.json"
STACK_MANIFEST_PATH = STACK_ROOT / "stack-manifest.json"
STACK_HUMAN_MANIFEST_PATH = STACK_ROOT / "STACK_MANIFEST.md"
BASE_PATH = ROOT / "BASE.json"
PARSER_PATH = ROOT / "vendor/universal.py"
AUDITOR_PATH = ROOT / "audit_contracts.py"
FROZEN_RECEIPT_PATH = ROOT / "receipts/native-mobius-v0.json"
SOURCE_FILES = (
    AUDITOR_PATH,
    ROOT / "audit_contracts_cli.py",
    ROOT / "metric_protocol.py",
    ROOT / "generate_receipt.py",
    ROOT / "generate_receipt_cli.py",
    ROOT / "verify_receipt.py",
    ROOT / "verify_receipt_cli.py",
    ROOT / "run_tests.py",
)
TEST_FILES = (ROOT / "tests/test_metric_protocol.py",)
WITNESS_DEPENDENCY_FILES = (STACK_ROOT / "tools/check_stack_consistency.py",)
WITNESS_DATA_FILES = (
    WORK_GRAPH_PATH,
    STACK_MANIFEST_PATH,
    STACK_HUMAN_MANIFEST_PATH,
    BASE_PATH,
    FROZEN_RECEIPT_PATH,
    PARSER_PATH,
)
AUDITED_IMPORT_ORDER = (
    ("metric_protocol", ROOT / "metric_protocol.py"),
    ("audit_contracts", ROOT / "audit_contracts.py"),
    ("audit_contracts_cli", ROOT / "audit_contracts_cli.py"),
    ("generate_receipt", ROOT / "generate_receipt.py"),
    ("generate_receipt_cli", ROOT / "generate_receipt_cli.py"),
    ("verify_receipt", ROOT / "verify_receipt.py"),
    ("verify_receipt_cli", ROOT / "verify_receipt_cli.py"),
)
UNSAFE_RUNNER_HOOKS = frozenset(
    {
        "run",
        "__call__",
        "debug",
        "_callSetUp",
        "_callTestMethod",
        "_callTearDown",
        "_callMaybeAsync",
        "setUpClass",
        "tearDownClass",
        "__getattribute__",
        "__getattr__",
    }
)
_LOADED_AUDITOR_SHA256 = globals().get("__source_sha256__")


class AuditIdentityError(ValueError):
    """Raised when an operational audit input is not exactly pinned."""


def _unique_json_pairs(pairs):
    value = {}
    for key, item in pairs:
        if key in value:
            raise AuditIdentityError(f"duplicate JSON member: {key}")
        value[key] = item
    return value


def _canonical_sha256(value: object, *, ensure_ascii: bool = True) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=ensure_ascii).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _git_output(root: Path, *args: str) -> bytes:
    result = subprocess.run(
        ["git", "--no-replace-objects", "-C", str(root), *args],
        check=False,
        capture_output=True,
    )
    if result.returncode:
        detail = result.stderr.decode("utf-8", errors="replace").strip()
        raise AuditIdentityError(
            f"git {' '.join(args)} failed for skill-lib checkout {root}: {detail}"
        )
    return result.stdout


def _load_pinned_parser(
    skill_lib_root: Path,
    *,
    graph_source: bytes,
    manifest_source: bytes,
    parser_source: bytes,
) -> ModuleType:
    """Source-load the exact parser bound by the work graph and Stack manifest."""
    graph = json.loads(graph_source.decode("utf-8"), object_pairs_hook=_unique_json_pairs)
    payload = {
        "participants": graph["participants"],
        "boundaries": graph["boundaries"],
    }
    # Digital graphs use protocol UTF-8; the root manifest retains ASCII escapes.
    if graph.get("work_graph_sha256") != _canonical_sha256(payload, ensure_ascii=False):
        raise AuditIdentityError("digital-metrics work-graph digest mismatch")
    graph_skills = [
        item for item in graph["participants"]
        if item.get("repository") == "The-Interdependency/skill-lib"
    ]
    if len(graph_skills) != 1:
        raise AuditIdentityError("work graph must pin exactly one skill-lib participant")

    manifest = json.loads(manifest_source.decode("utf-8"), object_pairs_hook=_unique_json_pairs)
    manifest_payload = {
        key: manifest[key]
        for key in ("repositories", "research_participants", "boundaries")
    }
    if manifest.get("work_graph_sha256") != _canonical_sha256(manifest_payload):
        raise AuditIdentityError("Stack manifest digest mismatch")
    manifest_skills = [
        item for item in manifest["research_participants"]
        if item.get("repository") == "The-Interdependency/skill-lib"
        and item.get("workspace") == "research/digital-metrics/"
    ]
    if len(manifest_skills) != 1:
        raise AuditIdentityError("Stack manifest must pin exactly one skill-lib repository")
    skill = manifest_skills[0]
    if skill.get("commit") != graph_skills[0].get("commit"):
        raise AuditIdentityError(
            "skill-lib commit differs between work graph and Stack manifest"
        )
    commit = skill.get("commit")
    skill_lib_root = skill_lib_root.resolve()
    git_root = Path(
        _git_output(skill_lib_root, "rev-parse", "--show-toplevel")
        .decode("utf-8")
        .strip()
    ).resolve()
    if git_root != skill_lib_root:
        raise AuditIdentityError(
            f"skill-lib root is not the Git top level: {skill_lib_root}"
        )
    head = _git_output(skill_lib_root, "rev-parse", "HEAD").decode("ascii").strip()
    if head != commit:
        raise AuditIdentityError(
            f"skill-lib checkout is not at graph-selected commit {commit}: {head}"
        )
    artifacts = skill.get("operational_artifacts")
    expected = {
        "source_path": "msdmd/parsers/universal.py",
        "workspace_path": "research/digital-metrics/vendor/universal.py",
    }
    matches = [
        item for item in artifacts if all(item.get(key) == value for key, value in expected.items())
    ] if isinstance(artifacts, list) else []
    if len(matches) != 1:
        raise AuditIdentityError("Stack manifest must pin the msdmd parser artifact exactly once")
    source = parser_source
    committed_source = _git_output(
        skill_lib_root,
        "show",
        f"{commit}:msdmd/parsers/universal.py",
    )
    if committed_source != source:
        raise AuditIdentityError(
            "vendored msdmd parser differs from graph-selected skill-lib commit"
        )
    actual_sha256 = hashlib.sha256(source).hexdigest()
    actual_blob_sha1 = hashlib.sha1(
        f"blob {len(source)}\0".encode("ascii") + source
    ).hexdigest()
    if matches[0].get("sha256") != actual_sha256:
        raise AuditIdentityError(
            f"msdmd parser digest mismatch: expected {matches[0].get('sha256')!r}, "
            f"got {actual_sha256}"
        )
    if matches[0].get("git_blob_sha1") != actual_blob_sha1:
        raise AuditIdentityError(
            f"msdmd parser Git blob mismatch: expected {matches[0].get('git_blob_sha1')!r}, "
            f"got {actual_blob_sha1}"
        )

    module = ModuleType("_stack_digital_metrics_pinned_msdmd_parser")
    module.__file__ = str(PARSER_PATH)
    module.__cached__ = None
    module.__package__ = ""
    exec(compile(source, str(PARSER_PATH), "exec", dont_inherit=True), module.__dict__)
    if not callable(getattr(module, "parse_text", None)) or not callable(
        getattr(module, "marker_for", None)
    ):
        raise AuditIdentityError("pinned msdmd parser does not expose parse_text/marker_for")
    return module


def _dotted_name(node: ast.expr) -> str | None:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        parent = _dotted_name(node.value)
        return f"{parent}.{node.attr}" if parent is not None else None
    return None


def _decorator_name(node: ast.expr) -> str | None:
    if isinstance(node, ast.Call):
        node = node.func
    return _dotted_name(node)


def _function_contains_yield(
    method: ast.FunctionDef | ast.AsyncFunctionDef,
) -> bool:
    pending = list(method.body)
    while pending:
        node = pending.pop()
        if isinstance(node, (ast.Yield, ast.YieldFrom)):
            return True
        if isinstance(
            node,
            (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda, ast.ClassDef),
        ):
            continue
        pending.extend(ast.iter_child_nodes(node))
    return False


def _discoverable_test_methods(path: Path, source: bytes) -> dict[str, str]:
    tree = ast.parse(source.decode("utf-8"), filename=str(path))
    unittest_aliases = {"unittest"}
    testcase_aliases: set[str] = set()
    async_testcase_aliases: set[str] = set()
    nonproof_decorator_aliases: set[str] = set()
    classes = {node.name: node for node in tree.body if isinstance(node, ast.ClassDef)}
    for node in tree.body:
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name == "unittest":
                    unittest_aliases.add(alias.asname or alias.name)
        elif isinstance(node, ast.ImportFrom) and node.module in {
            "unittest", "unittest.case", "unittest.async_case",
        }:
            for alias in node.names:
                if alias.name == "TestCase":
                    testcase_aliases.add(alias.asname or alias.name)
                elif alias.name == "IsolatedAsyncioTestCase":
                    async_testcase_aliases.add(alias.asname or alias.name)
                elif alias.name in {"skip", "skipIf", "skipUnless", "expectedFailure"}:
                    nonproof_decorator_aliases.add(alias.asname or alias.name)

    nonproof_decorators = nonproof_decorator_aliases | {
        f"{alias}.{name}"
        for alias in unittest_aliases
        for name in ("skip", "skipIf", "skipUnless", "expectedFailure")
    }
    direct_testcase_bases = testcase_aliases | {
        base
        for alias in unittest_aliases
        for base in (f"{alias}.TestCase", f"{alias}.case.TestCase")
    }
    direct_async_bases = async_testcase_aliases | {
        base
        for alias in unittest_aliases
        for base in (
            f"{alias}.IsolatedAsyncioTestCase",
            f"{alias}.async_case.IsolatedAsyncioTestCase",
        )
    }
    discoverable_classes: set[str] = set()
    async_classes: set[str] = set()
    nonproof_classes: set[str] = set()
    changed = True
    while changed:
        changed = False
        for name, node in classes.items():
            bases = {_dotted_name(base) for base in node.bases}
            is_async = bool(bases & direct_async_bases) or any(
                base in async_classes for base in bases
            )
            is_discoverable = (
                bool(bases & direct_testcase_bases)
                or is_async
                or any(base in discoverable_classes for base in bases)
            )
            is_nonproof = bool(node.decorator_list) or any(
                base in nonproof_classes for base in bases
            ) or any(
                isinstance(member, (ast.FunctionDef, ast.AsyncFunctionDef))
                and member.name in UNSAFE_RUNNER_HOOKS
                for member in node.body
            )
            if is_discoverable and name not in discoverable_classes:
                discoverable_classes.add(name)
                changed = True
            if is_async and name not in async_classes:
                async_classes.add(name)
                changed = True
            if is_nonproof and name not in nonproof_classes:
                nonproof_classes.add(name)
                changed = True

    methods: dict[str, str] = {}
    for name, node in classes.items():
        if name not in discoverable_classes or name in nonproof_classes:
            continue
        for method in node.body:
            if not isinstance(method, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            if not method.name.startswith("test_"):
                continue
            if method.decorator_list:
                continue
            if isinstance(method, ast.FunctionDef) and not _function_contains_yield(
                method
            ):
                admitted = True
            elif (
                isinstance(method, ast.AsyncFunctionDef)
                and name in async_classes
                and not _function_contains_yield(method)
            ):
                admitted = True
            else:
                admitted = False
            if admitted:
                if method.name in methods:
                    raise AuditIdentityError(
                        f"ambiguous unittest method {method.name!r} in "
                        f"{methods[method.name]!r} and {name!r}"
                    )
                methods[method.name] = name
    return methods


def audit(*, skill_lib_root: Path | None = None) -> dict[str, object]:
    contracts: dict[str, str] = {}
    checks: dict[str, tuple[str, str]] = {}
    findings: list[str] = []

    try:
        if not isinstance(_LOADED_AUDITOR_SHA256, str) or len(
            _LOADED_AUDITOR_SHA256
        ) != 64 or any(
            character not in "0123456789abcdef"
            for character in _LOADED_AUDITOR_SHA256
        ):
            raise AuditIdentityError(
                "auditor API must be source-loaded; use audit_contracts_cli.py"
            )
        auditor_source = AUDITOR_PATH.read_bytes()
        auditor_sha256 = hashlib.sha256(auditor_source).hexdigest()
        if auditor_sha256 != _LOADED_AUDITOR_SHA256:
            raise AuditIdentityError(
                "executing auditor digest differs from captured source snapshot"
            )
        snapshot_paths = dict.fromkeys(
            (
                *SOURCE_FILES,
                *WITNESS_DEPENDENCY_FILES,
                *WITNESS_DATA_FILES,
                WORK_GRAPH_PATH,
                STACK_MANIFEST_PATH,
                PARSER_PATH,
                *(path for _name, path in AUDITED_IMPORT_ORDER),
            )
        )
        snapshot_paths.pop(AUDITOR_PATH, None)
        source_snapshots = {AUDITOR_PATH: auditor_source}
        source_snapshots.update(
            {path: path.read_bytes() for path in snapshot_paths}
        )
        test_snapshots = {path: path.read_bytes() for path in TEST_FILES}
        if skill_lib_root is None:
            raise AuditIdentityError("exact skill-lib root is required")
        parser = _load_pinned_parser(
            skill_lib_root,
            graph_source=source_snapshots[WORK_GRAPH_PATH],
            manifest_source=source_snapshots[STACK_MANIFEST_PATH],
            parser_source=source_snapshots[PARSER_PATH],
        )
    except (
        AuditIdentityError,
        OSError,
        KeyError,
        TypeError,
        UnicodeDecodeError,
        json.JSONDecodeError,
        SyntaxError,
    ) as exc:
        findings.append(f"GAP audit identity unavailable: {exc}")
        return {
            "schema": "the-interdependency.digital-metric-contract-audit",
            "version": "0.2.0",
            "scope": "static-linkage-only",
            "witness_execution": "NOT_RUN",
            "verified_contracts": 0,
            "contracts": 0,
            "checks": 0,
            "findings": findings,
            "linkage_passed": False,
        }

    def parse_snapshot(path: Path, block_name: str, source: bytes):
        marker = parser.marker_for(path)
        if marker is None:
            return []
        return parser.parse_text(source.decode("utf-8"), block_name, marker)

    for path in SOURCE_FILES:
        for entry in parse_snapshot(path, "CONTRACTS", source_snapshots[path]):
            contract_id = entry.get("id", "")
            if not contract_id:
                findings.append(f"GAP {path.name} CONTRACTS entry has no id")
            elif contract_id in contracts:
                findings.append(f"GAP duplicate contract: {contract_id}")
            else:
                contracts[contract_id] = path.name

    declared_calls: set[tuple[Path, str]] = set()
    linked: set[str] = set()
    for path in TEST_FILES:
        try:
            discoverable = _discoverable_test_methods(path, test_snapshots[path])
        except (AuditIdentityError, SyntaxError, UnicodeDecodeError) as exc:
            findings.append(f"GAP {path.name} static unittest discovery failed: {exc}")
            discoverable = {}
        for entry in parse_snapshot(path, "CHECKS", test_snapshots[path]):
            check_id = entry.get("id", "")
            proves = entry.get("proves", "")
            call = entry.get("call", "")
            if not check_id:
                findings.append(f"GAP {path.name} CHECKS entry has no id")
                continue
            if check_id in checks:
                findings.append(f"GAP duplicate check: {check_id}")
            checks[check_id] = (proves, call)
            known_claims: list[str] = []
            for contract_id in (item.strip() for item in proves.split(",") if item.strip()):
                if contract_id not in contracts:
                    findings.append(f"GAP {check_id} claims unknown contract: {contract_id}")
                else:
                    known_claims.append(contract_id)
            if not call.startswith("self::"):
                findings.append(f"GAP {check_id} call is not no-import self:: target: {call}")
                continue
            function_name = call.removeprefix("self::")
            if function_name not in discoverable:
                findings.append(f"GAP {check_id} call is not a discoverable unittest: {call}")
                continue
            declared_calls.add((path, function_name))
            linked.update(known_claims)

        for function_name in sorted(discoverable):
            if (path, function_name) not in declared_calls:
                findings.append(f"GAP executable check {function_name} has no CHECKS declaration")

    for contract_id in sorted(set(contracts) - linked):
        findings.append(f"GAP {contract_id} has no CHECKS entry claiming to prove it")

    return {
        "schema": "the-interdependency.digital-metric-contract-audit",
        "version": "0.2.0",
            "scope": "static-linkage-only",
            "witness_execution": "NOT_RUN",
            "verified_contracts": 0,
        "contracts": len(contracts),
        "checks": len(checks),
        "findings": findings,
        "linkage_passed": not findings,
    }


def main(*, skill_lib_root: Path) -> int:
    report = audit(skill_lib_root=skill_lib_root)
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["linkage_passed"] else 1


if __name__ == "__main__":
    raise SystemExit("run audit_contracts_cli.py so auditor execution is source-bound")
# ratios: loc_comments=448:52 imports_exports=8:3 calls_definitions=147:12
