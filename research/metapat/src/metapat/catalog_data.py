"""Combined static declarations for the canonical METAPAT semantic catalog."""

# === MODULE_BUILD ===
# id: metapat_semantic_catalog_declarations
#   module_name: metapat.catalog_data
#   module_kind: schema
#   summary: combines stable doctrine and theory declarations for canonical catalog construction
#   owner: The Interdependency
#   public_surface: none
#   internal_surface: CATALOG_SPECS, CATALOG_DERIVATIONS, CATALOG_DERIVED_TEXT
#   auth_boundary: none
#   storage_boundary: none
#   network_boundary: none
#   user_data_boundary: exact canon statements and references only
#   admin_only: false
#   tests: tests.test_catalog
#   rollout: internal catalog constructor dependency
#   rollback: remove only with semantic catalog
#   requires: metapat_semantic_doctrine_declarations, metapat_semantic_theory_declarations
#   since: 2026-07-21
#   unresolved: future canon rotation requires explicit catalog version and migration
# === END MODULE_BUILD ===

from .catalog_doctrine_data import DOCTRINE_SPECS
from .catalog_theory_data import CATALOG_DERIVATIONS, CATALOG_DERIVED_TEXT, THEORY_SPECS

CATALOG_SPECS = DOCTRINE_SPECS + THEORY_SPECS
