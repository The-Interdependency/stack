"""Audit digital-metrics CONTRACTS/CHECKS without importing inspected modules.

Usage guidance::

    PYTHONPATH=skill-lib python3 \
      research/digital-metrics/audit_contracts.py

The audit parses source declarations and Python AST only.  It exits nonzero for
unwitnessed contracts, unknown ``proves`` targets, unresolved ``self::`` calls,
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
#   given: a CHECKS call names a top-level, nested, or non-TestCase test-like function
#   then: the audit rejects it unless unittest discovery can execute the named method
#   class: provenance
# === END CONTRACTS ===

import ast
import json
from pathlib import Path
import sys

from msdmd.parsers.universal import parse_file


ROOT = Path(__file__).resolve().parent
SOURCE_FILES = (
    ROOT / "audit_contracts.py",
    ROOT / "metric_protocol.py",
    ROOT / "generate_receipt.py",
    ROOT / "verify_receipt.py",
)
TEST_FILES = (ROOT / "tests/test_metric_protocol.py",)


def _dotted_name(node: ast.expr) -> str | None:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        parent = _dotted_name(node.value)
        return f"{parent}.{node.attr}" if parent is not None else None
    return None


def _discoverable_test_methods(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    unittest_aliases = {"unittest"}
    testcase_aliases: set[str] = set()
    classes = {node.name: node for node in tree.body if isinstance(node, ast.ClassDef)}
    for node in tree.body:
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name == "unittest":
                    unittest_aliases.add(alias.asname or alias.name)
        elif isinstance(node, ast.ImportFrom) and node.module in {"unittest", "unittest.case"}:
            for alias in node.names:
                if alias.name == "TestCase":
                    testcase_aliases.add(alias.asname or alias.name)

    direct_testcase_bases = testcase_aliases | {
        base
        for alias in unittest_aliases
        for base in (f"{alias}.TestCase", f"{alias}.case.TestCase")
    }
    discoverable_classes: set[str] = set()
    changed = True
    while changed:
        changed = False
        for name, node in classes.items():
            if name in discoverable_classes:
                continue
            bases = {_dotted_name(base) for base in node.bases}
            direct = bool(bases & direct_testcase_bases)
            inherited = any(base in discoverable_classes for base in bases)
            if direct or inherited:
                discoverable_classes.add(name)
                changed = True

    return {
        method.name
        for name, node in classes.items()
        if name in discoverable_classes
        for method in node.body
        if isinstance(method, (ast.FunctionDef, ast.AsyncFunctionDef))
        and method.name.startswith("test_")
    }


def audit() -> dict[str, object]:
    contracts: dict[str, str] = {}
    checks: dict[str, tuple[str, str]] = {}
    findings: list[str] = []

    for path in SOURCE_FILES:
        for entry in parse_file(path, "CONTRACTS"):
            contract_id = entry.get("id", "")
            if not contract_id:
                findings.append(f"GAP {path.name} CONTRACTS entry has no id")
            elif contract_id in contracts:
                findings.append(f"GAP duplicate contract: {contract_id}")
            else:
                contracts[contract_id] = path.name

    declared_calls: set[tuple[Path, str]] = set()
    proved: set[str] = set()
    for path in TEST_FILES:
        discoverable = _discoverable_test_methods(path)
        for entry in parse_file(path, "CHECKS"):
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
            proved.update(known_claims)

        for function_name in sorted(discoverable):
            if (path, function_name) not in declared_calls:
                findings.append(f"GAP executable check {function_name} has no CHECKS declaration")

    for contract_id in sorted(set(contracts) - proved):
        findings.append(f"GAP {contract_id} has no CHECKS entry claiming to prove it")

    return {
        "schema": "the-interdependency.digital-metric-contract-audit",
        "version": "0.1.0",
        "contracts": len(contracts),
        "checks": len(checks),
        "findings": findings,
        "passed": not findings,
    }


def main() -> int:
    report = audit()
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
