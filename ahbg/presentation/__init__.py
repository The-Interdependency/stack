# === MODULE_BUILD ===
# id: ahbg_presentation_public_boundary
#   module_name: presentation
#   module_kind: adapter
#   summary: exposes the validated presentation snapshot and projection boundary without exporting mechanics
#   owner: AHBG presentation
#   public_surface: PresentationSnapshotError, load_snapshot, snapshot_from_observation, validate_snapshot
#   internal_surface: none
#   auth_boundary: none
#   storage_boundary: none
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: ahbg/presentation/tests/test_presentation.py
#   rollout: import explicitly from ahbg.presentation
#   rollback: remove package exports with presentation package
#   requires: ahbg_presentation_snapshot_contract, ahbg_presentation_observation_projector
#   since: 2026-08-31
#   unresolved: none
# === END MODULE_BUILD ===

"""Presentation-only AHBG graphics boundary.

Usage guidance: import only validated presentation helpers from this package;
game mechanics remain outside this namespace.
"""

from .project import snapshot_from_observation
from .snapshot import PresentationSnapshotError, load_snapshot, validate_snapshot

__all__ = [
    "PresentationSnapshotError",
    "load_snapshot",
    "snapshot_from_observation",
    "validate_snapshot",
]
