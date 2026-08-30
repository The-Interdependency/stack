# ratios: loc_comments=110:53 imports_exports=7:2 calls_definitions=56:5
"""Audit PTCNA's source-owned contracts against test-owned checks without imports.

Usage:

    python scripts/check_contracts.py

The audit parses declarations and Python syntax only. It never imports a test
module, so collection cannot execute module top-level code. A closed graph
means every declared obligation has a resolvable accountable witness; normal
``pytest`` execution remains the separate behavior gate.
"""
from __future__ import annotations

import argparse
import ast
import sys
from collections import defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / ".agents" / "skills"))

from msdmd.parsers.universal import walk_tree  # noqa: E402

# === MODULE_BUILD ===
# id: ptcna_contract_audit
#   module_name: contract audit
#   module_kind: verification
#   summary: reconciles source CONTRACTS with test CHECKS using syntax-only call resolution
#   owner: Erin Spencer
#   public_surface: audit, main
#   internal_surface: _definitions, _split
#   auth_boundary: none
#   storage_boundary: read repository source
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: ptcna/tests/test_contract_audit.py
#   rollout: release gate
#   rollback: remove the gate without changing runtime code
#   requires: vendored msdmd parser
#   since: 0.1.1
#   unresolved: mutation sensitivity remains outside this syntax-only audit
# === END MODULE_BUILD ===

# === CONTRACTS ===
# id: contract_audit_closes_complete_graph
#   given: unique contracts and checks whose proves targets and self calls all resolve
#   then: audit returns no gaps
#   class: evidence
#
# id: contract_audit_exposes_broken_edges
#   given: an orphan contract, unknown proves target, unresolved self call, or undeclared executable test
#   then: audit returns a visible GAP for every broken edge
#   class: evidence
# === END CONTRACTS ===

# === BOUNDARIES ===
# id: contract_audit_repository_boundary
#   summary: reads repository source text and Python syntax without importing modules or mutating files
#   auth_boundary: none
#   storage_boundary: read repository source
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   pii: none
#   secrets: none
#   owner: Erin Spencer
#   since: 0.1.1
# === END BOUNDARIES ===

REQUIRED_CHECK_FIELDS = ("proves", "call", "mutates", "cleanup")


def _split(value: str) -> list[str]:
    return [part.strip() for part in value.split(",") if part.strip()]


def _definitions(path: Path) -> dict[str, ast.FunctionDef | ast.AsyncFunctionDef]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    return {
        node.name: node
        for node in ast.walk(tree)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    }


def _required_parameters(node: ast.FunctionDef | ast.AsyncFunctionDef) -> int:
    positional = [*node.args.posonlyargs, *node.args.args]
    required_positional = max(0, len(positional) - len(node.args.defaults))
    required_kwonly = sum(default is None for default in node.args.kw_defaults)
    return required_positional + required_kwonly


def audit(root: Path) -> list[str]:
    """Return deterministic human-readable gaps for a repository tree."""

    root = root.resolve()
    contract_rows = [
        (entry, path)
        for path, entries in walk_tree(root, "CONTRACTS")[0]
        for entry in entries
    ]
    check_rows = [
        (entry, path)
        for path, entries in walk_tree(root, "CHECKS")[0]
        for entry in entries
    ]
    gaps: list[str] = []

    contracts: dict[str, list[Path]] = defaultdict(list)
    checks: dict[str, list[Path]] = defaultdict(list)
    for entry, path in contract_rows:
        contracts[entry["id"]].append(path)
    for entry, path in check_rows:
        checks[entry["id"]].append(path)

    for contract_id, paths in sorted(contracts.items()):
        if len(paths) > 1:
            gaps.append(f"GAP duplicate contract {contract_id}: {len(paths)} declarations")
    for check_id, paths in sorted(checks.items()):
        if len(paths) > 1:
            gaps.append(f"GAP duplicate check {check_id}: {len(paths)} declarations")

    known_contracts = set(contracts)
    proved: set[str] = set()
    definitions: dict[Path, dict[str, ast.FunctionDef | ast.AsyncFunctionDef]] = {}
    declared_calls: dict[Path, set[str]] = defaultdict(set)

    for check, path in check_rows:
        check_id = check["id"]
        for field in REQUIRED_CHECK_FIELDS:
            if not check.get(field):
                gaps.append(f"GAP {check_id} missing required field: {field}")
        for target in _split(check.get("proves", "")):
            if target not in known_contracts:
                gaps.append(f"GAP {check_id} claims unknown contract: {target}")
            else:
                proved.add(target)

        call = check.get("call", "")
        if not call.startswith("self::"):
            gaps.append(f"GAP {check_id} call does not resolve: only self::fn is auditable")
            continue
        function_name = call.removeprefix("self::")
        declared_calls[path].add(function_name)
        try:
            file_definitions = definitions.setdefault(path, _definitions(path))
        except (OSError, SyntaxError) as exc:
            gaps.append(f"GAP {check_id} call does not resolve: {exc}")
            continue
        node = file_definitions.get(function_name)
        if node is None:
            gaps.append(f"GAP {check_id} call does not resolve: self::{function_name}")
        elif _required_parameters(node):
            gaps.append(
                f"GAP {check_id} call requires arguments: self::{function_name}"
            )

    for contract_id in sorted(known_contracts - proved):
        gaps.append(f"GAP {contract_id} has no CHECKS entry claiming to prove it")

    for path in sorted({path for _, path in check_rows}):
        try:
            file_definitions = definitions.setdefault(path, _definitions(path))
        except (OSError, SyntaxError):
            continue
        executable = {
            name for name in file_definitions if name.startswith("test_")
        }
        for function_name in sorted(executable - declared_calls[path]):
            relative = path.relative_to(root)
            gaps.append(
                f"GAP executable check {relative}::{function_name} "
                "has no resolving CHECKS declaration"
            )

    return sorted(set(gaps))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=REPO_ROOT)
    args = parser.parse_args(argv)
    gaps = audit(args.root)
    if gaps:
        print("\n".join(gaps))
        return 1
    print("contract audit . CLOSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
# ratios: loc_comments=110:53 imports_exports=7:2 calls_definitions=56:5
