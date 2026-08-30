"""Generate packaged METAPAT application-module fixtures."""

# === MODULE_BUILD ===
# id: metapat_application_fixture_generator
#   module_name: tools.generate_application_fixtures
#   module_kind: instrument
#   summary: generates or verifies deterministic packaged application and engineering-design fixtures from canonical constructors
#   owner: The Interdependency
#   public_surface: render_quantum_magnetism_fixture, render_electromagnetic_pipe_fixture, write_fixtures, main
#   internal_surface: FIXTURES
#   auth_boundary: none
#   storage_boundary: read, optional generated-file write
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: tests.test_quantum_magnetism, tests.test_electromagnetic_pipe
#   rollout: CI compliance gate and explicit regeneration command
#   rollback: restore prior generated fixtures only with constructor and digest evidence attached
#   requires: metapat_quantum_magnetism_application, metapat_electromagnetic_pipe_application
#   since: 2026-07-21
#   unresolved: future application fixtures require separate constructors and evidence classification
# === END MODULE_BUILD ===

# === CONTRACTS ===
# id: metapat_quantum_fixture_generated
#   given: the quantum-magnetism application constructor runs
#   then: the rendered fixture is deterministic JSON with one trailing newline
#   class: evidence
#
# id: metapat_quantum_fixture_current
#   given: the generator runs in check mode against the packaged quantum-magnetism fixture
#   then: stale or missing fixture bytes fail visibly and current bytes pass
#   class: safety
#
# id: metapat_pipe_fixture_generated
#   given: the electromagnetic-pipe design constructor runs
#   then: the rendered fixture is deterministic JSON with one trailing newline
#   class: evidence
#
# id: metapat_pipe_fixture_current
#   given: the generator runs in check mode against the packaged electromagnetic-pipe fixture
#   then: stale or missing fixture bytes fail visibly and current bytes pass
#   class: safety
# === END CONTRACTS ===

from __future__ import annotations

import argparse
from pathlib import Path

from metapat.electromagnetic_pipe import electromagnetic_pipe_design
from metapat.quantum_magnetism import quantum_magnetism_application_module

QUANTUM_MAGNETISM_OUTPUT = Path(
    "src/metapat/fixtures/quantum-magnetism-application-v2.json"
)
ELECTROMAGNETIC_PIPE_OUTPUT = Path(
    "src/metapat/fixtures/three-phase-electromagnetic-pipe-v2.json"
)


def render_quantum_magnetism_fixture() -> str:
    return quantum_magnetism_application_module().to_json() + "\n"


def render_electromagnetic_pipe_fixture() -> str:
    return electromagnetic_pipe_design().to_json() + "\n"


FIXTURES = {
    QUANTUM_MAGNETISM_OUTPUT: render_quantum_magnetism_fixture,
    ELECTROMAGNETIC_PIPE_OUTPUT: render_electromagnetic_pipe_fixture,
}


def write_fixtures(root: Path) -> tuple[Path, ...]:
    written: list[Path] = []
    for relative, renderer in FIXTURES.items():
        target = root.resolve() / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(renderer(), encoding="utf-8")
        written.append(target)
    return tuple(written)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args(argv)
    root = args.root.resolve()
    failures = 0
    for relative, renderer in FIXTURES.items():
        target = root / relative
        rendered = renderer()
        if args.check:
            try:
                existing = target.read_text(encoding="utf-8")
            except OSError:
                print(f"GAP  application fixture missing: {target}")
                failures += 1
                continue
            if existing != rendered:
                print(f"GAP  application fixture is stale: {target}")
                failures += 1
                continue
            print(f"CURRENT  {relative}")
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(rendered, encoding="utf-8")
            print(target)
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
