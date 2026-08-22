# ratios: loc_comments=70:31 imports_exports=5:2 calls_definitions=12:13
"""
Σ (Sigma) — Filesystem Observer Ring

Wraps RingCore to add file-content watching.
Sigma injects coherence signals into the Ψ (psi) self-model ring
whenever watched files change.

N=41, seed=41 — observer substrate
"""

# === MODULE_BUILD ===
# id: pcna_sigma
#   module_name: sigma
#   module_kind: engine
#   summary: N=41 filesystem observer ring wrapping RingCore; tracks watched file mtimes and drains content-changed events on a content_interval cadence, injecting coherence into Psi.
#   owner: Erin Spencer
#   public_surface: SigmaRing, get_sigma, N, SEED
#   internal_surface: _sigma, SigmaRing._core, SigmaRing._watched, SigmaRing._pending, SigmaRing._last_check
#   auth_boundary: none
#   storage_boundary: read
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: hmmm
#   rollout: default_enabled
#   rollback: remove import and call sites; callers already degrade gracefully if it raises
#   requires: pcna_ring_core
#   since: 2026-06-02
#   unresolved: structural_interval is stored but never acted on (Known Issues)
# === END MODULE_BUILD ===

import os
import time
from typing import Optional

import numpy as np

from .ring_core import RingCore

N = 41
SEED = 41
DEFAULT_CONTENT_INTERVAL = 10.0
DEFAULT_STRUCTURAL_INTERVAL = 30.0


class SigmaRing:
    """Filesystem-aware RingCore ring. Drains file-change events on demand."""

    def __init__(self):
        self._core = RingCore(name="sigma", symbol="Σ", role="observer", n=N, seed=SEED)
        self.content_interval: float = DEFAULT_CONTENT_INTERVAL
        self.structural_interval: float = DEFAULT_STRUCTURAL_INTERVAL
        self._resolution: int = 3
        self._watched: dict[str, float] = {}  # path → last mtime
        self._pending: list[str] = []
        self._last_check: float = 0.0

    # --- RingCore passthrough ---

    @property
    def tensor(self) -> Optional[np.ndarray]:
        return self._core.tensor

    @property
    def n(self) -> int:
        return self._core.n

    @property
    def ring_coherence(self) -> float:
        return self._core.ring_coherence

    @property
    def node_coherence(self) -> np.ndarray:
        return self._core.node_coherence

    def nudge(self, reward: float, lr: float = 0.02) -> None:
        self._core.nudge(reward, lr=lr)

    def state(self) -> dict:
        s = self._core.state()
        s["resolution"] = self._resolution
        s["watched_count"] = len(self._watched)
        s["content_interval"] = self.content_interval
        s["structural_interval"] = self.structural_interval
        return s

    # --- file watching ---

    def set_resolution(self, level: int) -> None:
        self._resolution = max(1, min(5, level))

    def add_content_watch(self, path: str) -> None:
        try:
            mtime = os.path.getmtime(path)
        except OSError:
            mtime = 0.0
        self._watched[path] = mtime

    def remove_content_watch(self, path: str) -> None:
        self._watched.pop(path, None)

    def drain_content_changed_events(self) -> list[str]:
        """Check watched files for mtime changes; return paths that changed."""
        now = time.time()
        if now - self._last_check >= self.content_interval:
            self._last_check = now
            for path, last_mtime in list(self._watched.items()):
                try:
                    mtime = os.path.getmtime(path)
                except OSError:
                    continue
                if mtime != last_mtime:
                    self._watched[path] = mtime
                    self._pending.append(path)
        drained = self._pending[:]
        self._pending = []
        return drained


_sigma: Optional[SigmaRing] = None


def get_sigma() -> SigmaRing:
    global _sigma
    if _sigma is None:
        _sigma = SigmaRing()
    return _sigma
# ratios: loc_comments=70:31 imports_exports=5:2 calls_definitions=12:13
