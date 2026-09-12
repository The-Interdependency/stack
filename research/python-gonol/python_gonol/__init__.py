"""Public surface for stack-local Python Gonol Construction.

Usage guidance: call ``affixiate_python_bytes`` for a file or
``affixiate_python_source`` for already-decoded text, persist the returned
receipt, and call ``replay_python_affixiation`` before consuming a receipt
across a boundary.
"""

# === MODULE_BUILD ===
# id: python_gonol_public_surface
#   module_name: python_gonol
#   module_kind: adapter
#   summary: exposes the bounded Python 3.12 character-first affixiation constructor and immutable receipt types
#   owner: Python Gonol Construction (stack-local research)
#   public_surface: affixiate_python_source, affixiate_python_bytes, replay_python_affixiation, reconstruct_source, grammar_witness_inventory, PythonAffixiationReceipt
#   internal_surface: none
#   auth_boundary: none
#   storage_boundary: none
#   network_boundary: none
#   user_data_boundary: caller-owned source only
#   admin_only: false
#   tests: tests.test_affixiation, tests.test_python312_surface
#   rollout: explicit import only
#   rollback: remove package exports with the workspace
#   requires: python_gonol_affixiation, python_gonol_model
#   since: 2026-09-12
#   unresolved: independent package and release authority remain hmmm
# === END MODULE_BUILD ===

from .affixiation import (
    CONSTRUCTOR_ID,
    CONSTRUCTOR_VERSION,
    LANGUAGE_PROFILE,
    PINNED_PUBLIC_GONOL_SHA256,
    PythonGonolConstructionError,
    affixiate_python_bytes,
    affixiate_python_source,
    grammar_witness_inventory,
    reconstruct_source,
    replay_python_affixiation,
)
from .model import (
    AffixiationRelation,
    ClosedGonol,
    PythonAffixiationReceipt,
    RelationMember,
    SourceSpan,
)

__all__ = [
    "AffixiationRelation",
    "CONSTRUCTOR_ID",
    "CONSTRUCTOR_VERSION",
    "ClosedGonol",
    "LANGUAGE_PROFILE",
    "PINNED_PUBLIC_GONOL_SHA256",
    "PythonAffixiationReceipt",
    "PythonGonolConstructionError",
    "RelationMember",
    "SourceSpan",
    "affixiate_python_bytes",
    "affixiate_python_source",
    "grammar_witness_inventory",
    "reconstruct_source",
    "replay_python_affixiation",
]
