"""Generate canon-bound METAPAT envelope and semantic catalog fixtures.

Run without flags to rewrite both current fixtures. Use ``--check`` in CI or
before commit to fail when either packaged record differs from its live
constructor. ``--out`` remains a catalog-only compatibility option.
"""

# === MODULE_BUILD ===
# id: metapat_catalog_generator
#   module_name: tools.generate_catalog
#   module_kind: instrument
#   summary: generates or verifies byte-current root-spine-envelope-v2 and semantic-module-catalog-v2 fixtures from their live constructors
#   owner: The Interdependency
#   public_surface: render_root_spine_envelope, render_catalog, write_semantic_fixtures, write_catalog, main
#   internal_surface: FIXTURES
#   auth_boundary: none
#   storage_boundary: read, optional generated-file write
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: tests.test_catalog
#   rollout: CI compliance gate and explicit regeneration command
#   rollback: restore prior generated fixture only with constructor and digest evidence attached
#   requires: metapat_semantic_catalog
#   since: 2026-07-21
#   unresolved: none
# === END MODULE_BUILD ===

# === CONTRACTS ===
# id: metapat_catalog_fixture_generated
#   given: the canonical semantic catalog constructor runs
#   then: the rendered fixture is deterministic JSON with one trailing newline
#   class: evidence
#
# id: metapat_catalog_fixture_current
#   given: the generator runs in check mode against the packaged fixture
#   then: stale or missing fixture bytes fail visibly and current bytes pass
#   class: safety
#
# id: metapat_root_envelope_fixture_generated
#   given: the canonical root-spine envelope constructor runs
#   then: the rendered fixture is deterministic JSON with one trailing newline
#   class: evidence
#
# id: metapat_root_envelope_fixture_current
#   given: the generator runs in check mode against the packaged root-spine envelope fixture
#   then: stale or missing fixture bytes fail visibly and current bytes pass
#   class: safety
# === END CONTRACTS ===

from __future__ import annotations

import argparse
from pathlib import Path

from metapat.catalog import canonical_semantic_catalog
from metapat.envelope import root_spine_module_envelope

ROOT_SPINE_OUTPUT = Path("src/metapat/fixtures/root-spine-envelope-v2.json")
OUTPUT = Path("src/metapat/fixtures/semantic-module-catalog-v2.json")


def render_root_spine_envelope() -> str:
    return root_spine_module_envelope().to_json() + "\n"


def render_catalog() -> str:
    return canonical_semantic_catalog().to_json() + "\n"


FIXTURES = {
    ROOT_SPINE_OUTPUT: render_root_spine_envelope,
    OUTPUT: render_catalog,
}


def write_catalog(root: Path, output: Path | None = None) -> Path:
    target = root.resolve() / (output or OUTPUT)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(render_catalog(), encoding="utf-8")
    return target


def write_semantic_fixtures(root: Path) -> tuple[Path, ...]:
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
    parser.add_argument("--out", type=Path)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args(argv)
    root = args.root.resolve()
    selected = (
        {args.out: render_catalog}
        if args.out is not None
        else FIXTURES
    )
    failures = 0
    for relative, renderer in selected.items():
        target = root / relative
        rendered = renderer()
        if not args.check:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(rendered, encoding="utf-8")
            print(target)
            continue
        try:
            existing = target.read_text(encoding="utf-8")
        except OSError:
            print(f"GAP  semantic fixture missing: {target}")
            failures += 1
            continue
        if existing != rendered:
            print(f"GAP  semantic fixture is stale: {target}")
            failures += 1
            continue
        shown = target.relative_to(root) if target.is_relative_to(root) else target
        print(f"CURRENT  {shown}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
