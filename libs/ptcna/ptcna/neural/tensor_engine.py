# ratios: loc_comments=56:42 imports_exports=3:2 calls_definitions=23:7
"""
Tensor engine primitives: TensorState, simple spectral descriptor, and
a MarkovRecursion updater that enforces (approximate) mass conservation.
"""

# === MODULE_BUILD ===
# id: pcna_tensor_engine
#   module_name: tensor_engine
#   module_kind: engine
#   summary: Tensor engine primitives — TensorState (E[a,t,m,c]) with spectral descriptor Z = Sum E.e^(i*theta), and a MarkovRecursion updater that enforces approximate mass conservation.
#   owner: Erin Spencer
#   public_surface: TensorState, MarkovRecursion
#   internal_surface: none
#   auth_boundary: none
#   storage_boundary: none
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: tests/test_tensor_engine.py
#   rollout: default_enabled
#   rollback: remove import and call sites
#   requires: none
#   since: 2026-06-02
#   unresolved: none
# === END MODULE_BUILD ===

from dataclasses import dataclass
from typing import Tuple
import numpy as np


@dataclass
class TensorState:
    """E[a, t, m, c] tensor representation (components are numpy arrays)"""
    actor: np.ndarray
    time: np.ndarray
    metric: np.ndarray
    context: np.ndarray

    @property
    def shape(self) -> Tuple[int, ...]:
        return (
            len(self.actor),
            len(self.time),
            len(self.metric),
            len(self.context),
        )

    @property
    def mass(self) -> float:
        """Total constraint energy"""
        return float(np.sum(self.metric))

    def spectral_descriptor(self) -> Tuple[float, float]:
        """Compute Z = Σ E · e^(iθ). Return magnitude and phase.

        If metric is flat or empty, return (0.0, 0.0).
        """
        flattened = self.metric.flatten()
        n = flattened.size
        if n == 0:
            return 0.0, 0.0
        phases = np.linspace(0, 2 * np.pi, n, endpoint=False)
        z = np.sum(flattened * np.exp(1j * phases))
        return float(abs(z)), float(np.angle(z))


class MarkovRecursion:
    def __init__(self, learning_rate: float = 0.1, tol: float = 1e-9):
        self.lr = float(learning_rate)
        self.tol = float(tol)

    def update(self, state: TensorState, injected: np.ndarray, resolved: np.ndarray) -> TensorState:
        """
        E(t+1) = E(t) + lr * Delta, where Delta = injected - resolved but adjusted
        to enforce global mass conservation.

        If injected and resolved have a small net imbalance, we subtract the
        imbalance uniformly across the delta so the sum(delta) == 0 and mass
        of the metric remains constant after the update.
        """
        if state.metric.size == 0:
            return state

        # Ensure shapes match metric
        injected = np.asarray(injected, dtype=float)
        resolved = np.asarray(resolved, dtype=float)

        # Broadcast to metric shape if necessary
        try:
            delta = injected - resolved
        except Exception:
            # Attempt flatten fallback
            injected_flat = injected.flatten()
            resolved_flat = resolved.flatten()
            # Pad/truncate to metric size
            N = state.metric.size
            injected_flat = np.resize(injected_flat, N)
            resolved_flat = np.resize(resolved_flat, N)
            delta = injected_flat - resolved_flat
            delta = delta.reshape(state.metric.shape)

        mass_balance = float(np.sum(delta))  # this equals sum(injected)-sum(resolved)
        N = state.metric.size

        if abs(mass_balance) > self.tol:
            # Remove the mass imbalance uniformly so sum(delta_corrected) == 0.
            correction_per_entry = mass_balance / N
            delta_corrected = delta - correction_per_entry
        else:
            delta_corrected = delta

        new_metric = state.metric + self.lr * delta_corrected

        # Return new TensorState reusing actor/time/context arrays
        return TensorState(actor=state.actor, time=state.time, metric=new_metric, context=state.context)
# ratios: loc_comments=56:42 imports_exports=3:2 calls_definitions=23:7
