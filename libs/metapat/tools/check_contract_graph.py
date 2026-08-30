"""No-execution audit for the METAPAT msdmd CONTRACTS/CHECKS graph."""

# === MODULE_BUILD ===
# id: metapat_contract_graph_audit
#   module_name: tools.check_contract_graph
#   module_kind: instrument
#   summary: reconciles source-owned CONTRACTS against test-owned CHECKS without importing product or test modules
#   owner: The Interdependency
#   public_surface: audit_repository, main
#   internal_surface: _load_parser, _top_level_test_functions, _split_csv, _audit
#   auth_boundary: none
#   storage_boundary: read
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: tests.test_contract_audit
#   rollout: CI compliance gate
#   rollback: remove the gate only with an explicit replacement audit
#   requires: repo-local skill-lib msdmd parser
#   since: 2026-07-12
#   unresolved: block type for harness-only checks remains hmmm in skill-lib doctrine
# === END MODULE_BUILD ===

# === CONTRACTS ===
# id: metapat_contract_graph_closes
#   given: current METAPAT source promises and test evidence are audited without imports
#   then: every contract has a proving check, every check targets known contracts, every self call resolves, and every top-level test has a declaration
#   class: evidence
#
# id: metapat_contract_audit_detects_gaps
#   given: orphan contracts, phantom proves targets, unresolvable calls, or undeclared executable tests are planted
#   then: the audit reports each gap and exits nonzero
#   class: safety
# === END CONTRACTS ===

from __future__ import annotations

import argparse
import ast
import importlib.util
from dataclasses import dataclass
from pathlib import Path
from types import ModuleType
from typing import Iterable


@dataclass(frozen=True, slots=True)
class AuditResult:
    contracts: int
    checks: int
    executable_tests: int
    gaps: tuple[str, ...]

    @property
    def closed(self) -> bool:
        return not self.gaps


def _load_parser(root: Path) -> ModuleType:
    path = root / ".agents" / "skills" / "msdmd" / "parsers" / "universal.py"
    spec = importlib.util.spec_from_file_location("metapat_skill_lib_msdmd_parser", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load pinned msdmd parser: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _split_csv(value: str) -> tuple[str, ...]:
    return tuple(part.strip() for part in value.split(",") if part.strip())


def _top_level_test_functions(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    return {
        node.name
        for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name.startswith("test_")
    }


def _python_files(root: Path, relative: str) -> list[Path]:
    base = root / relative
    return sorted(path for path in base.rglob("*.py") if "__pycache__" not in path.parts) if base.exists() else []


def _audit(root: Path, source_files: Iterable[Path], test_files: Iterable[Path]) -> AuditResult:
    parser = _load_parser(root)
    gaps: list[str] = []
    contracts: dict[str, tuple[Path, dict[str, str]]] = {}
    checks: dict[str, tuple[Path, dict[str, str]]] = {}
    test_functions: dict[Path, set[str]] = {}

    for path in source_files:
        for entry in parser.parse_file(path, "CONTRACTS"):
            contract_id = entry.get("id", "")
            if not contract_id:
                gaps.append(f"GAP  {path.relative_to(root)} CONTRACTS entry has no id")
                continue
            if contract_id in contracts:
                gaps.append(f"GAP  duplicate contract id: {contract_id}")
                continue
            if "call" in entry:
                gaps.append(f"GAP  {contract_id} places call in CONTRACTS; executable topology belongs in CHECKS")
            for field in ("given", "then"):
                if not entry.get(field):
                    gaps.append(f"GAP  {contract_id} missing required CONTRACTS field: {field}")
            contracts[contract_id] = (path, entry)

    for path in test_files:
        test_functions[path] = _top_level_test_functions(path)
        for entry in parser.parse_file(path, "CHECKS"):
            check_id = entry.get("id", "")
            if not check_id:
                gaps.append(f"GAP  {path.relative_to(root)} CHECKS entry has no id")
                continue
            if check_id in checks:
                gaps.append(f"GAP  duplicate check id: {check_id}")
                continue
            for field in ("proves", "call", "mutates", "cleanup"):
                if not entry.get(field):
                    gaps.append(f"GAP  {check_id} missing required CHECKS field: {field}")
            checks[check_id] = (path, entry)

    proving_checks: dict[str, list[str]] = {contract_id: [] for contract_id in contracts}
    declared_functions: dict[Path, set[str]] = {path: set() for path in test_functions}

    for check_id, (path, entry) in checks.items():
        for contract_id in _split_csv(entry.get("proves", "")):
            if contract_id not in contracts:
                gaps.append(f"GAP  {check_id} claims unknown contract: {contract_id}")
            else:
                proving_checks[contract_id].append(check_id)

        call = entry.get("call", "")
        if not call.startswith("self::"):
            gaps.append(f"GAP  {check_id} call does not resolve: only self::fn is permitted")
            continue
        function_name = call.removeprefix("self::")
        if function_name not in test_functions.get(path, set()):
            gaps.append(f"GAP  {check_id} call does not resolve: {function_name} is not a top-level test in {path.relative_to(root)}")
        else:
            declared_functions[path].add(function_name)

    for contract_id, witnesses in proving_checks.items():
        if not witnesses:
            gaps.append(f"GAP  {contract_id} has no CHECKS entry claiming to prove it")

    for path, functions in test_functions.items():
        for function_name in sorted(functions - declared_functions[path]):
            gaps.append(f"GAP  executable check {function_name} has no resolving CHECKS declaration in {path.relative_to(root)}")

    return AuditResult(
        contracts=len(contracts),
        checks=len(checks),
        executable_tests=sum(len(functions) for functions in test_functions.values()),
        gaps=tuple(sorted(set(gaps))),
    )


def audit_repository(root: Path) -> AuditResult:
    root = root.resolve()
    source_files = [*_python_files(root, "src/metapat"), *_python_files(root, "tools")]
    test_files = _python_files(root, "tests")
    return _audit(root, source_files, test_files)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("."))
    args = parser.parse_args(argv)
    result = audit_repository(args.root)
    if result.gaps:
        for gap in result.gaps:
            print(gap)
        return 1
    print(
        f"CLOSED  {result.contracts} contracts / {result.checks} checks / "
        f"{result.executable_tests} executable tests"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
