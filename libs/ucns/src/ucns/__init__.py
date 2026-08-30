# === MODULE_BUILD ===
# id: ucns_geometry_public_surface
#   module_name: __init__
#   module_kind: facade
#   summary: geometry-only UCNS public surface
#   owner: Erin Spencer
#   public_surface: carrier geometry, framed Mobius root loop, exact Public Gonol carrier, Mobius vesica and seed geometry
#   internal_surface: none
#   auth_boundary: none
#   storage_boundary: none
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: tests.test_public_gonol, tests.test_geometry_public_surface, tests.test_carrier
#   rollout: active geometry-only package facade
#   rollback: restore prior facade from Git history
#   requires: directed_carrier_floor, ucns_native_mobius_geometry, ucns_public_gonol_geometry, ucns_mobius_vesica_candidate, ucns_mobius_seed_of_life_candidate
#   since: 2026-08-20
#   unresolved: canonical completion of the full UCNS geometric construction
# === END MODULE_BUILD ===

# === CONTRACTS ===
# id: geometry_public_surface_excludes_nongeometric_domains
#   given: the active ucns package facade is imported
#   then: its declared public surface contains geometry only and removed lexical, semantic, EDCM, PTCNA, evaluator, and bridge modules are absent from the package tree
#   class: safety
#   since: 2026-08-20
# === END CONTRACTS ===

"""UCNS geometry.

The active package surface is deliberately geometric: carriers, exact motion,
Möbius constructions, geometric certificates, and topological/prime geometry.
Lexical semantics, corpora, morphology, definition recursion, evaluator
frameworks, PTCNA state, and cross-stack adapters are not UCNS package content.
"""

from .carrier import (
    LIFTED_PERIOD,
    STRUCTURAL_NULL,
    VISIBLE_PERIOD,
    LiftedCarrierPoint,
    VisibleCarrierPoint,
    carrier_from_breadth,
    deck_translate,
    lifted_preimages,
    project,
    radius_from_breadth,
    same_lifted_position,
    same_visible_position,
)
from .direct_mobius import (
    DirectMobiusError,
    NativeMobiusFrame,
    NativeMobiusState,
    STRUCTURAL_NULL_ORIGIN,
    StructuralNullIdentity,
    native_mobius_state,
)
from .public_gonol import (
    PUBLIC_GONOL_157,
    PUBLIC_GONOL_SHA256,
    PublicGonolPosition,
    public_gonol_function,
    public_gonol_position,
    public_gonol_sha256,
)
from .mobius_vesica import __all__ as _mobius_vesica_all
from .mobius_vesica import *  # noqa: F401,F403 - geometric public module
from .mobius_seed import __all__ as _mobius_seed_all
from .mobius_seed import *  # noqa: F401,F403 - geometric public module

__all__ = list(dict.fromkeys([
    "DirectMobiusError",
    "LIFTED_PERIOD",
    "LiftedCarrierPoint",
    "NativeMobiusFrame",
    "NativeMobiusState",
    "PUBLIC_GONOL_157",
    "PUBLIC_GONOL_SHA256",
    "PublicGonolPosition",
    "STRUCTURAL_NULL",
    "STRUCTURAL_NULL_ORIGIN",
    "StructuralNullIdentity",
    "VISIBLE_PERIOD",
    "VisibleCarrierPoint",
    "carrier_from_breadth",
    "deck_translate",
    "lifted_preimages",
    "native_mobius_state",
    "project",
    "public_gonol_function",
    "public_gonol_position",
    "public_gonol_sha256",
    "radius_from_breadth",
    "same_lifted_position",
    "same_visible_position",
] + list(_mobius_vesica_all) + list(_mobius_seed_all)))
