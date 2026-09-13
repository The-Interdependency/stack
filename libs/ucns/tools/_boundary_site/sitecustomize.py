# ratios: loc_comments=36:28 imports_exports=5:2 calls_definitions=19:5
# === MODULE_BUILD ===
# id: boundary_descendant_import_binding
#   module_name: sitecustomize
#   module_kind: instrument
#   summary: keeps bound package imports ahead of child working directories during declared checks
#   owner: Erin Spencer
#   public_surface: none; installed on the boundary runner's sanitized PYTHONPATH
#   internal_surface: BoundSourceFinder, BoundSourceLoader
#   auth_boundary: none
#   storage_boundary: read
#   storage_notes: reads source package locations
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: tests/test_skill_lib_boundary_runner.py
#   rollout: inherited by ordinary Python check descendants
#   rollback: remove together with the runner's startup-hook contract
# === END MODULE_BUILD ===
# === CONTRACTS ===
# id: boundary_descendants_import_bound_source
#   given: an ordinary Python check subprocess inherits the boundary environment
#   then: bound source packages compile inventoried source bytes before same-named packages in the working directory
#   class: evidence
# === END CONTRACTS ===
"""Internal startup hook; the runner sets UCNS_BOUND_SOURCE_ROOT and PYTHONPATH.

Explicit isolated/no-site interpreters and replaced environments do not inherit
this protocol. This is trusted-check evidence instrumentation, not a sandbox.
"""
from __future__ import annotations

from importlib.machinery import PathFinder, SourceFileLoader, SourcelessFileLoader
import os
from pathlib import Path
import sys


BOUND_ROOT = os.environ.get("UCNS_BOUND_SOURCE_ROOT", "")
FINDER = None


class BoundSourceLoader(SourceFileLoader):
    def get_code(self, fullname):
        filename = self.get_filename(fullname)
        return self.source_to_code(self.get_data(filename), filename)


class BoundSourceFinder:
    def __init__(self, root: Path):
        self.source = root / "src"
        self.names = {p.stem if p.is_file() else p.name for p in self.source.iterdir()
                      if p.is_dir() or p.suffix == ".py"} if self.source.is_dir() else set()

    def find_spec(self, fullname, path=None, target=None):
        if fullname.split(".", 1)[0] not in self.names:
            return None
        search = [str(self.source)] if "." not in fullname else path
        spec = PathFinder.find_spec(fullname, search, target)
        if spec is None:
            raise ModuleNotFoundError(f"module absent from bound source: {fullname}")
        locations = list(spec.submodule_search_locations or ())
        if spec.origin is not None:
            locations.append(spec.origin)
        if not locations or any(not Path(location).resolve().is_relative_to(self.source) for location in locations):
            raise ImportError(f"module outside bound source: {fullname}")
        if isinstance(spec.loader, SourceFileLoader):
            spec.loader = BoundSourceLoader(fullname, spec.origin)
        elif isinstance(spec.loader, SourcelessFileLoader):
            raise ImportError(f"sourceless bytecode outside the source contract: {fullname}")
        return spec


if BOUND_ROOT:
    FINDER = BoundSourceFinder(Path(BOUND_ROOT).resolve())
    sys.meta_path.insert(0, FINDER)
# ratios: loc_comments=36:28 imports_exports=5:2 calls_definitions=19:5
