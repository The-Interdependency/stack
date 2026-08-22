# === MODULE_BUILD ===
# id: skill_lib_contract_audit
#   module_name: verify_skill_lib_contracts
#   module_kind: instrument
#   summary: performs a no-exec reconciliation of skill-lib MODULE_BUILD, CONTRACTS, and CHECKS declarations
#   owner: Erin Spencer
#   public_surface: command-line audit
#   internal_surface: parse_blocks, audit_repository
#   auth_boundary: none
#   storage_boundary: read
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: tests/test_skill_lib_contracts.py
#   rollout: required CI gate
#   rollback: remove workflow invocation and script
#   since: 2026-07-21
#   unresolved: mutation-level verification beyond planted graph gaps
# === END MODULE_BUILD ===

# === CONTRACTS ===
# id: contract_audit_is_no_exec
#   given: the repository contract graph is audited
#   then: Python source is parsed without importing product or test modules
#   class: safety
#   since: 2026-07-21
#
# id: contract_audit_reports_graph_gaps
#   given: a contract, check target, or self call is missing or unknown
#   then: the audit reports the gap and exits nonzero
#   class: evidence
#   since: 2026-07-21
#
# id: contract_audit_accepts_closed_graph
#   given: every declared contract has a resolving check and every check names known contracts
#   then: the audit exits successfully
#   class: evidence
#   since: 2026-07-21
# === END CONTRACTS ===

"""Minimal no-exec skill-lib contract graph audit.

The parser is intentionally bounded to the line-oriented msdmd fields used by
this repository. It does not replace skill-lib's canonical universal parser.
"""

from __future__ import annotations

import ast
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Set, Tuple

BLOCK_RE = re.compile(r"^\s*#\s*===\s*(MODULE_BUILD|CONTRACTS|CHECKS)\s*===\s*$")
END_RE = re.compile(r"^\s*#\s*===\s*END\s+(MODULE_BUILD|CONTRACTS|CHECKS)\s*===\s*$")
FIELD_RE = re.compile(r"^\s*#\s*(?P<key>[A-Za-z_][\w-]*):\s*(?P<value>.*)$")
REQUIRED_MODULE_FIELDS = {
    "module_name",
    "module_kind",
    "summary",
    "owner",
    "public_surface",
    "internal_surface",
    "auth_boundary",
    "storage_boundary",
    "network_boundary",
    "user_data_boundary",
    "admin_only",
    "tests",
    "rollout",
    "rollback",
}
REQUIRED_CONTRACT_FIELDS = {"given", "then"}
REQUIRED_CHECK_FIELDS = {"proves", "call", "timeout", "mutates", "cleanup"}


@dataclass(frozen=True)
class Entry:
    block: str
    source: Path
    fields: Dict[str, str]

    @property
    def id(self) -> str:
        return self.fields["id"]


def _source_files(root: Path) -> Iterable[Path]:
    for base in (root / "src", root / "tools", root / "tests"):
        if base.exists():
            yield from sorted(base.rglob("*.py"))


def parse_blocks(path: Path) -> List[Entry]:
    entries: List[Entry] = []
    active: str | None = None
    current: Dict[str, str] | None = None

    for raw in path.read_text(encoding="utf-8").splitlines():
        start = BLOCK_RE.match(raw)
        if start:
            active = start.group(1)
            current = None
            continue
        end = END_RE.match(raw)
        if end:
            if active != end.group(1):
                raise ValueError(f"{path}: mismatched END {end.group(1)}")
            if current:
                entries.append(Entry(active, path, current))
            active = None
            current = None
            continue
        if active is None:
            continue
        field = FIELD_RE.match(raw)
        if not field:
            continue
        key, value = field.group("key"), field.group("value").strip()
        if key == "id":
            if current:
                entries.append(Entry(active, path, current))
            current = {"id": value}
        elif current is not None:
            current[key] = value

    if active is not None:
        raise ValueError(f"{path}: unterminated {active} block")
    return entries


def _defined_functions(path: Path) -> Set[str]:
    """Return top-level functions without importing or executing the module."""

    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    return {
        node.name
        for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    }


def _missing(fields: Dict[str, str], required: Set[str]) -> Set[str]:
    return {name for name in required if not fields.get(name)}


def audit_repository(root: Path) -> Tuple[bool, List[str]]:
    entries: List[Entry] = []
    problems: List[str] = []
    for path in _source_files(root):
        try:
            path_entries = parse_blocks(path)
        except (SyntaxError, ValueError) as exc:
            problems.append(f"GAP parse {exc}")
            continue

        entries.extend(path_entries)
        if path.is_relative_to(root / "src") or path.is_relative_to(root / "tools"):
            declared = {entry.block for entry in path_entries}
            for required_block in ("MODULE_BUILD", "CONTRACTS"):
                if required_block not in declared:
                    problems.append(f"GAP {path} missing {required_block} declaration block")

    ids: Dict[str, Entry] = {}
    for entry in entries:
        if not entry.id:
            problems.append(f"GAP {entry.source}: entry without id")
            continue
        if entry.id in ids:
            problems.append(f"GAP duplicate id {entry.id}: {ids[entry.id].source} and {entry.source}")
        ids[entry.id] = entry
        required = {
            "MODULE_BUILD": REQUIRED_MODULE_FIELDS,
            "CONTRACTS": REQUIRED_CONTRACT_FIELDS,
            "CHECKS": REQUIRED_CHECK_FIELDS,
        }[entry.block]
        missing = _missing(entry.fields, required)
        if missing:
            problems.append(f"GAP {entry.id} missing fields: {', '.join(sorted(missing))}")

    contracts = {entry.id: entry for entry in entries if entry.block == "CONTRACTS"}
    checks = [entry for entry in entries if entry.block == "CHECKS"]
    proved: Set[str] = set()

    for check in checks:
        targets = [target.strip() for target in check.fields.get("proves", "").split(",") if target.strip()]
        for target in targets:
            if target not in contracts:
                problems.append(f"GAP {check.id} claims unknown contract: {target}")
            else:
                proved.add(target)

        call = check.fields.get("call", "")
        if not call.startswith("self::"):
            problems.append(f"GAP {check.id} call is not no-exec self::fn: {call}")
        else:
            name = call[len("self::") :]
            try:
                defined = _defined_functions(check.source)
            except SyntaxError as exc:
                problems.append(f"GAP {check.id} cannot parse call source: {exc}")
            else:
                is_test_module = (
                    check.source.is_relative_to(root / "tests")
                    and check.source.name.startswith("test_")
                )
                if not is_test_module or not name.startswith("test_"):
                    problems.append(
                        f"GAP {check.id} call does not target an executable pytest test: {call}"
                    )
                elif name not in defined:
                    problems.append(f"GAP {check.id} call does not resolve: {call}")

    for contract_id in sorted(set(contracts) - proved):
        problems.append(f"GAP {contract_id} has no CHECKS entry claiming to prove it")

    for test_path in sorted((root / "tests").rglob("test_*.py")) if (root / "tests").exists() else ():
        declared_calls = {
            entry.fields.get("call", "")[len("self::") :]
            for entry in checks
            if entry.source == test_path and entry.fields.get("call", "").startswith("self::")
        }
        for function in _defined_functions(test_path):
            if function.startswith("test_") and function not in declared_calls:
                problems.append(f"GAP executable check {test_path}::{function} has no resolving CHECKS declaration")

    return not problems, problems


def main(argv: Sequence[str] | None = None) -> int:
    args = list(argv or sys.argv[1:])
    root = Path(args[0] if args else ".").resolve()
    ok, problems = audit_repository(root)
    if ok:
        print("skill-lib contract graph: closed")
        return 0
    for problem in problems:
        print(problem)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
