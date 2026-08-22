# ratios: loc_comments=41:51 imports_exports=4:1 calls_definitions=1:0
"""PTCNA — Prime Tensor Circled Neural Architecture.

One architecture, four layers. Each layer's tensors divide into the next; every
circle, seed, and core is itself a tensor.

    neural  → base neural tensors        (the ONLY back-propagating layer)
    circle  → neural tensors → circles   (auditing / timing tensors)
    seed    → circles → seeds            (auditing / timing tensors)
    core    → seeds → cores              (auditing / timing; fiqs gate internal
                                          propagation per Fick's law J = -D grad(phi))

Consolidates the former The-Interdependency repos pcna (neural), pcta (seed),
and pcsa (core). PCEA (encryption guardian) stays a separate, orthogonal repo.
PTCNA is the single upstream that feeds interdependent-lib.
"""

__version__ = "0.1.1"
__license__ = "MPL-2.0"

from . import neural, circle, seed, core  # noqa: F401
from .ucns_integration import (
    UCNS_PRODUCER_COMMIT,
    UCNS_RECEIPT_SHA256,
    UCNSIntegrationState,
    UCNSIntegrationStatus,
    UCNSIntegrationSuspended,
    UCNSReceiptError,
    consume_ucns_receipt,
    load_bundled_ucns_receipt,
    require_ucns_integration,
    ucns_integration_status,
)
from .runtime import HashedLinearFallback, PTCNAEngine, PTCNARuntime
from .evaluation import EvaluationCase, EvaluationPlan, EvaluationReceipt, evaluate

# === MODULE_BUILD ===
# id: ptcna_package_surface
#   module_name: package surface
#   module_kind: adapter
#   summary: exposes the four layers, explicit runtime boundary, dependable fallback, and frozen evaluation types from the package root
#   owner: Erin Spencer
#   public_surface: neural, circle, seed, core, PTCNAEngine, HashedLinearFallback, PTCNARuntime, EvaluationCase, EvaluationPlan, EvaluationReceipt, evaluate, UCNS integration status types
#   internal_surface: none
#   auth_boundary: none
#   storage_boundary: none
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: ptcna/tests/test_runtime.py
#   rollout: imported through ptcna
#   rollback: remove root re-exports while retaining module-qualified imports
#   requires: ptcna_runtime_boundary, ptcna_frozen_evaluation, ptcna_ucns_integration
#   since: unreleased
#   unresolved: none
# === END MODULE_BUILD ===

# === CONTRACTS ===
# id: ptcna_root_exports_runtime_boundary
#   given: a caller imports ptcna
#   then: the experimental engine, distinct fallback, attributed runtime, frozen evaluation types, and evaluator are available without importing deprecated service surfaces
#   class: compatibility
# === END CONTRACTS ===

# === BOUNDARIES ===
# id: ptcna_package_import_boundary
#   summary: imports local package definitions without constructing engines or performing persistence, network, authentication, user-data, or administrative effects
#   auth_boundary: none
#   storage_boundary: none
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   pii: none
#   secrets: none
#   owner: Erin Spencer
#   since: unreleased
# === END BOUNDARIES ===

__all__ = [
    "neural",
    "circle",
    "seed",
    "core",
    "UCNS_PRODUCER_COMMIT",
    "UCNS_RECEIPT_SHA256",
    "UCNSIntegrationState",
    "UCNSIntegrationStatus",
    "UCNSIntegrationSuspended",
    "UCNSReceiptError",
    "consume_ucns_receipt",
    "load_bundled_ucns_receipt",
    "ucns_integration_status",
    "require_ucns_integration",
    "PTCNAEngine",
    "HashedLinearFallback",
    "PTCNARuntime",
    "EvaluationCase",
    "EvaluationPlan",
    "EvaluationReceipt",
    "evaluate",
    "__version__",
]
# ratios: loc_comments=41:51 imports_exports=4:1 calls_definitions=1:0
