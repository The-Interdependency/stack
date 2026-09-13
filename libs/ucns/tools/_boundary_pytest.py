# ratios: loc_comments=138:35 imports_exports=10:3 calls_definitions=62:10
# === MODULE_BUILD ===
# id: boundary_pytest_observer
#   module_name: _boundary_pytest
#   module_kind: instrument
#   summary: observes actual pytest exceptions, xfail outcomes, and imported source origins for UCNS receipts
#   owner: Erin Spencer
#   public_surface: run_suite; selected-check bootstrap launched by run_skill_lib_boundaries
#   internal_surface: Observer, main
#   auth_boundary: none
#   storage_boundary: write
#   storage_notes: writes caller-selected machine outcome report
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: tests/test_skill_lib_boundary_runner.py
#   rollout: boundary runner subprocess bootstrap
#   rollback: remove with boundary runner bootstrap integration
# === END MODULE_BUILD ===
# === CONTRACTS ===
# id: boundary_pytest_observes_actual_outcomes
#   given: a selected pytest boundary runs through this bootstrap
#   then: assertion subclasses fail, unexpected exceptions error, XPASS cannot pass, actual test function code must match the declared source, imported local package origins must match the bound tree
#   class: evidence
#
# id: geometry_suite_requires_nonempty_pass
#   given: the full geometry suite runs through run_suite
#   then: empty, unexecuted declared witnesses or collected parameter items, skipped, xfailed, XPASS, failed, or collection-error evidence cannot produce exit status zero
#   class: evidence
# === END CONTRACTS ===

"""Pytest evidence observer and selected-check bootstrap.

CI usage: ``run_suite(["tests", "-c", "pyproject.toml", "--noconftest"], Path.cwd())``.
Selected-check CLI usage remains owned by tools/run_skill_lib_boundaries.py.

Observations describe executed checks, not theorem standing or a hostile-code
sandbox. Ambient pytest plugins and PYTHONPATH are excluded by the parent.
"""
from __future__ import annotations

from collections import Counter
import json
from pathlib import Path
import sys
import tempfile
from types import CodeType, FunctionType, MethodType

from _pytest.assertion.rewrite import _rewrite_test

import pytest


class Observer:
    def __init__(self, root: Path):
        self.root = root
        self.calls: list[str] = []
        self.other: list[str] = []
        self.executed_witnesses: set[tuple[Path, str]] = set()
        self.collected_items: tuple[object, ...] = ()
        self.item_calls: Counter[int] = Counter()
        self.expected_code: dict[Path, CodeType] = {}

    def pytest_collection_finish(self, session):
        self.collected_items = tuple(session.items)

    def item_coverage_closed(self) -> bool:
        return Counter(id(item) for item in self.collected_items) == self.item_calls

    def _witness_matches_source(self, item) -> bool:
        path = Path(item.path).resolve()
        if not path.is_relative_to(self.root.resolve()):
            return False
        if path not in self.expected_code:
            if item.config.getoption("assertmode") == "plain":
                code = compile(path.read_bytes(), str(path), "exec", dont_inherit=True)
            else:
                _, code = _rewrite_test(path, item.config)
            self.expected_code[path] = code
        expected = self.expected_code[path]
        names = [item.originalname or item.name.split("[", 1)[0]]
        parent = item.parent
        while isinstance(parent, pytest.Class):
            names.insert(0, parent.name)
            parent = parent.parent
        for name in names:
            candidates = [value for value in expected.co_consts if isinstance(value, CodeType) and value.co_name == name]
            if len(candidates) != 1:
                return False
            expected = candidates[0]
        actual = item.obj
        if isinstance(actual, MethodType):
            actual = actual.__func__
        return isinstance(actual, FunctionType) and actual.__code__ == expected

    @pytest.hookimpl(hookwrapper=True, tryfirst=True)
    def pytest_pyfunc_call(self, pyfuncitem):
        if not self._witness_matches_source(pyfuncitem):
            pytest.fail("test witness code differs from its declared source", pytrace=False)
        yield
        if not self._witness_matches_source(pyfuncitem):
            pytest.fail("test witness code changed during execution", pytrace=False)

    def pytest_collectreport(self, report):
        if report.skipped:
            self.other.append("SKIP")
        elif report.failed:
            self.other.append("ERROR")

    @pytest.hookimpl(hookwrapper=True, tryfirst=True)
    def pytest_runtest_makereport(self, item, call):
        report = (yield).get_result()
        if report.skipped:
            status = "SKIP"
        elif hasattr(report, "wasxfail"):
            status = "FAIL"  # Includes explicit xfail(strict=False) XPASS.
        elif call.excinfo is not None:
            status = "FAIL" if call.when == "call" and (
                call.excinfo.errisinstance(AssertionError)
                or call.excinfo.errisinstance(pytest.fail.Exception)
            ) else "ERROR"
        elif report.failed:
            status = "FAIL" if call.when == "call" else "ERROR"
        else:
            status = "PASS"
        if call.when == "call":
            self.calls.append(status)
            self.item_calls[id(item)] += 1
            self.executed_witnesses.add((Path(item.path).resolve(), item.originalname or item.name.split("[", 1)[0]))
        elif status != "PASS":
            self.other.append(status)


def run_suite(arguments: list[str], root: Path) -> int:
    from tools.verify_skill_lib_contracts import _defined_functions
    expected = {(path.resolve(), name) for path in (root / "tests").rglob("*.py")
                if path.name.startswith("test_") or path.name.endswith("_test.py")
                for name in _defined_functions(path) if name.startswith("test")}
    observer = Observer(root)
    previous_prefix = sys.pycache_prefix
    try:
        with tempfile.TemporaryDirectory(prefix="ucns-suite-bytecode-") as cache:
            sys.pycache_prefix = cache
            result = int(pytest.main(arguments, plugins=[observer]))
    finally:
        sys.pycache_prefix = previous_prefix
    if result:
        return result
    missing = expected - observer.executed_witnesses
    if missing:
        print("Declared witnesses did not execute:", sorted(str(path) + "::" + name for path, name in missing))
    if not observer.item_coverage_closed():
        print("Collected test item execution differs:", [(item.nodeid, observer.item_calls[id(item)]) for item in observer.collected_items])
    return 0 if observer.calls and set(observer.calls) == {"PASS"} and not observer.other and not missing and observer.item_coverage_closed() else 1


def main() -> int:
    root = Path(sys.argv[1]).resolve()
    report_path = Path(sys.argv[2])
    sys.path[:0] = [str(root / "src"), str(root)]
    observer = Observer(root)
    hook = sys.modules.get("sitecustomize")
    if getattr(hook, "BOUND_ROOT", None) != str(root) or getattr(hook, "FINDER", None) not in sys.meta_path:
        raise RuntimeError("bound descendant import hook is unavailable")
    exit_code = int(pytest.main(sys.argv[3:], plugins=[observer]))
    source_root = root / "src"
    local_names = {p.stem if p.is_file() else p.name for p in source_root.iterdir()} if source_root.exists() else set()
    origins = {}
    wrong_origins = []
    for name, module in tuple(sys.modules.items()):
        if name.split(".", 1)[0] not in local_names:
            continue
        paths = [getattr(module, "__file__", None), *getattr(module, "__path__", ())]
        paths = [str(Path(p).resolve()) for p in paths if p is not None]
        origins[name] = paths
        if not paths or any(not Path(p).is_relative_to(source_root) for p in paths):
            wrong_origins.append(name)
    statuses = observer.calls + observer.other
    if wrong_origins or "ERROR" in statuses:
        status = "ERROR"
    elif "FAIL" in statuses:
        status = "FAIL"
    elif "SKIP" in statuses:
        status = "SKIP"
    elif observer.calls and exit_code == 0 and observer.item_coverage_closed():
        status = "PASS"
    else:
        status = "ERROR"
    report_path.write_text(json.dumps({"status": status, "calls": observer.calls, "other": observer.other, "origins": origins, "wrong_origins": wrong_origins, "descendants_reaped": 0, "item_coverage_closed": observer.item_coverage_closed()}), encoding="utf-8")
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
# ratios: loc_comments=138:35 imports_exports=10:3 calls_definitions=62:10
