"""Source-loading CLI launcher for the digital-metric receipt generator.

This launcher reads ``generate_receipt.py`` exactly once, computes the digest of
that byte buffer, compiles the same bytes, and invokes the loaded generator.  It
is the supported command-line entry point.
"""

from __future__ import annotations

# === MODULE_BUILD ===
# id: stack_digital_metric_receipt_generator_cli
#   module_name: digital metric generator source-loading CLI
#   module_kind: instrument
#   summary: read-once launcher binding generator execution to its recorded source digest
#   owner: The-Interdependency/stack
#   public_surface: main
#   internal_surface: read-once source loader
#   auth_boundary: none
#   storage_boundary: delegated to the loaded generator
#   network_boundary: none
#   user_data_boundary: public research fixtures only
#   admin_only: false
#   tests: research/digital-metrics/tests/test_metric_protocol.py
#   rollout: supported command-line entry for digital-metric receipt generation
#   rollback: remove with the digital-metrics research workspace
#   requires: stack_digital_metric_receipt_generator
#   since: 2026-09-20
#   unresolved: generated candidates remain pending until independent replay
# === END MODULE_BUILD ===

# === CONTRACTS ===
# id: digital_metric_generator_cli_binds_loaded_bytes
#   given: the generator source path changes after the CLI loader reads it
#   then: execution and the recorded generator digest remain bound to the original read buffer
#   class: provenance
# === END CONTRACTS ===

import hashlib
from pathlib import Path
import sys
from types import ModuleType


def _load_generator(source_path: Path) -> ModuleType:
    source_path = source_path.resolve()
    source = source_path.read_bytes()
    module = ModuleType("_stack_digital_metric_generator_cli")
    module.__file__ = str(source_path)
    module.__cached__ = None
    module.__package__ = ""
    module.__source_sha256__ = hashlib.sha256(source).hexdigest()
    previous = sys.modules.get(module.__name__)
    sys.modules[module.__name__] = module
    try:
        exec(
            compile(source, str(source_path), "exec", dont_inherit=True),
            module.__dict__,
        )
    finally:
        if previous is None:
            sys.modules.pop(module.__name__, None)
        else:
            sys.modules[module.__name__] = previous
    return module


def main() -> int:
    generator = _load_generator(Path(__file__).resolve().with_name("generate_receipt.py"))
    return generator.main()


if __name__ == "__main__":
    raise SystemExit(main())
