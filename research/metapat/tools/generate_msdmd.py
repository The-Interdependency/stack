"""Generate the repository msdmd collection from bounded product surfaces."""

# === MODULE_BUILD ===
# id: metapat_msdmd_generator
#   module_name: tools.generate_msdmd
#   module_kind: instrument
#   summary: invokes the pinned skill-lib collector over METAPAT source, tests, and repository tools while excluding vendored skill declarations
#   owner: The Interdependency
#   public_surface: render_collection, write_collection, main
#   internal_surface: _load_collector, _stage_inputs
#   auth_boundary: none
#   storage_boundary: read, optional generated-file write
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: tests.test_msdmd_generation
#   rollout: CI compliance gate and explicit regeneration command
#   rollback: restore prior generated file only with the generator output attached
#   requires: repo-local skill-lib msdmd collector
#   since: 2026-07-12
#   unresolved: none
# === END MODULE_BUILD ===

# === CONTRACTS ===
# id: metapat_msdmd_generated
#   given: the pinned collector runs over the bounded METAPAT product surfaces
#   then: its rendered output is byte-for-byte identical to committed metapat_msdmd.ts
#   class: evidence
#
# id: metapat_msdmd_scope_bounded
#   given: the collection is generated
#   then: product metadata from src, tests, and tools is included while vendored .agents skill metadata is excluded
#   class: safety
# === END CONTRACTS ===

from __future__ import annotations

import argparse
import hashlib
import importlib
import json
import shutil
import sys
import tempfile
from pathlib import Path
from types import ModuleType

REPOSITORY = "The-Interdependency/metapat"
SKILL_LIB_PIN = "The-Interdependency/skill-lib@6f36340"
OUTPUT_NAME = "metapat_msdmd.ts"
SELECTED_PATHS = ("src", "tests", "tools")


def _load_collector(root: Path) -> ModuleType:
    skill_root = root / ".agents" / "skills"
    sys.path.insert(0, str(skill_root))
    try:
        return importlib.import_module("msdmd.collect")
    finally:
        try:
            sys.path.remove(str(skill_root))
        except ValueError:
            pass


def _stage_inputs(root: Path, stage: Path) -> None:
    for relative in SELECTED_PATHS:
        source = root / relative
        if source.exists():
            shutil.copytree(
                source,
                stage / relative,
                ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".pytest_cache"),
            )


def render_collection(root: Path) -> str:
    root = root.resolve()
    collector = _load_collector(root)
    with tempfile.TemporaryDirectory(prefix="metapat-msdmd-") as directory:
        stage = Path(directory)
        _stage_inputs(root, stage)
        collection = collector.collect(
            stage,
            REPOSITORY,
            source_commit=SKILL_LIB_PIN,
        )
        grouped: dict[tuple[str, str], list[dict]] = {}
        for declaration in collection["declarations"]:
            grouped.setdefault((declaration["file"], declaration["block"]), []).append(declaration)

        declarations = []
        for (file, block), entries in sorted(grouped.items()):
            ids = sorted(entry["id"] for entry in entries)
            digest_payload = [
                {"id": entry["id"], "fields": entry["fields"]}
                for entry in sorted(entries, key=lambda item: item["id"])
            ]
            slug = file.replace("/", "_").replace(".", "_").replace("-", "_")
            declarations.append(
                {
                    "file": file,
                    "block": block,
                    "id": f"generated_{slug}_{block.lower()}",
                    "fields": {
                        "count": str(len(entries)),
                        "ids": ",".join(ids),
                        "metadata_digest": hashlib.sha256(
                            json.dumps(digest_payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
                        ).hexdigest(),
                    },
                }
            )

        compact = {
            "repo": collection["repo"],
            "source_commit": collection["source_commit"],
            "declarations": declarations,
            "gaps": collection["gaps"],
            "edges": [edge for edge in collection["edges"] if edge["kind"] == "claims_proves"],
        }
        payload = json.dumps(compact, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        return (
            'import { defineMsdmdCollection } from "./.agents/skills/msdmd/collection";\n\n'
            f"export default defineMsdmdCollection({payload});\n"
        )


def write_collection(root: Path, output: Path | None = None) -> Path:
    root = root.resolve()
    target = output or root / OUTPUT_NAME
    target.write_text(render_collection(root), encoding="utf-8")
    return target


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--out", type=Path)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args(argv)
    root = args.root.resolve()
    target = args.out or root / OUTPUT_NAME
    rendered = render_collection(root)
    if args.check:
        try:
            existing = target.read_text(encoding="utf-8")
        except OSError:
            print(f"GAP  generated collection missing: {target}")
            return 1
        if existing != rendered:
            print(f"GAP  generated collection is stale: {target}")
            return 1
        print(f"CURRENT  {target.relative_to(root) if target.is_relative_to(root) else target}")
        return 0
    target.write_text(rendered, encoding="utf-8")
    print(target)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
