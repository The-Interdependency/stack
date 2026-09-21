"""Read-once launcher for the digital-metrics contract auditor."""

from __future__ import annotations

# === MODULE_BUILD ===
# id: stack_digital_metric_contract_audit_cli
#   module_name: digital metric contract audit source-loading CLI
#   module_kind: instrument
#   summary: binds contract-audit execution and its recorded identity to one source byte buffer
#   owner: The-Interdependency/stack
#   public_surface: main
#   internal_surface: read-once auditor source loader
#   auth_boundary: none
#   storage_boundary: read-only
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: research/digital-metrics/tests/test_metric_protocol.py
#   rollout: supported command-line entry for the digital-metrics contract audit
#   rollback: remove with the digital-metrics research workspace
#   requires: stack_digital_metric_contract_audit
#   since: 2026-09-21
#   unresolved: none
# === END MODULE_BUILD ===

# === CONTRACTS ===
# id: digital_metric_audit_cli_binds_loaded_bytes
#   given: the auditor source path changes after the launcher reads it
#   then: execution and the captured auditor snapshot remain bound to the original read buffer
#   class: provenance
# === END CONTRACTS ===

import argparse
import hashlib
from pathlib import Path
import sys
from types import ModuleType


def _load_auditor(source_path: Path) -> ModuleType:
    source_path = source_path.resolve()
    source = source_path.read_bytes()
    module = ModuleType("_stack_digital_metric_contract_auditor_cli")
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


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--skill-lib-root", type=Path, required=True)
    args = parser.parse_args(argv)
    auditor = _load_auditor(Path(__file__).resolve().with_name("audit_contracts.py"))
    return auditor.main(skill_lib_root=args.skill_lib_root)


if __name__ == "__main__":
    raise SystemExit(main())
