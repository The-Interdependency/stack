# ratios: loc_comments=266:78 imports_exports=15:1 calls_definitions=85:15
# 295:27
"""
PCNA Inference Engine — six-ring pipeline, all rings real.

Six rings:

Φ (phi) N=53, seed=53 — cognitive substrate
Ψ (psi) N=53, seed=43 — self-model
Ω (omega) N=53, seed=47 — autonomy
Guardian N=29 — microkernel gate
Memory-L N=19, seed=19 — long-term
Memory-S N=17, seed=17 — short-term

Six inference steps:

1. Project — encode input text → normalized signal vector
2. Inject — push signal into Φ, self-referential into Ψ, autonomy into Ω
3. Propagate — run heptagram propagation on Φ/Ψ/Ω + guardian
4. Seed-audit — per-prime-node audit on all three cores (ptcna.seed)
5. Circle-audit — guardian circle audit (ptcna.circle)
6. Coherence — weighted ring coherence → winner + confidence

Backprop:

reward(winner, outcome) → nudge all three PTCA cores + guardian + memory flush
"""

# === MODULE_BUILD ===
# id: pcna_pcna
#   module_name: pcna
#   module_kind: engine
#   summary: Six-ring PCNA inference engine (phi/psi/omega/theta/memory_l/memory_s) running project->inject->propagate->seed-audit->circle-audit->coherence, with RING_WEIGHTS scoring and numpy checkpointing.
#   owner: Erin Spencer
#   public_surface: PCNAEngine, RING_WEIGHTS, WINNER_RINGS
#   internal_surface: _tensor_to_b64, _b64_to_tensor, _CHECKPOINT_DIR, PCNAEngine._project, PCNAEngine._inject, PCNAEngine._propagate, PCNAEngine._seed_audit, PCNAEngine._circle_audit, PCNAEngine._coherence_score
#   auth_boundary: none
#   storage_boundary: write
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: ptcna/neural/tests/test_pcna.py
#   rollout: default_enabled
#   rollback: remove import and call sites; checkpoints under .checkpoints/ can be deleted
#   requires: pcna_ring_core, pcna_memory_core, pcna_theta
#   since: 2026-06-02
#   unresolved: none
# === END MODULE_BUILD ===

# === CONTRACTS ===
# id: pcna_infer_reports_complete_six_step_pipeline
#   given: non-empty input text is passed to PCNAEngine.infer
#   then: the result reports project, inject, propagate, seed audit, circle audit, and coherence steps with a bounded confidence
#   class: correctness
#
# id: pcna_checkpoint_round_trips_ring_state
#   given: an engine saves a checkpoint and a compatible engine loads it
#   then: all five persisted ring tensors are restored with the saved shapes and values
#   class: correctness
#
# id: pcna_reward_updates_neural_and_timing_state
#   given: a bounded outcome is passed to PCNAEngine.reward
#   then: the neural rings and theta timing state are updated and one unambiguous memory flush result is reported
#   class: correctness
# === END CONTRACTS ===

# === BOUNDARIES ===
# id: pcna_checkpoint_runtime_boundary
#   summary: performs local numpy checkpoint reads and writes under the configured checkpoint directory
#   auth_boundary: none
#   storage_boundary: write
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   pii: none
#   secrets: none
#   owner: Erin Spencer
#   since: 0.1.1
# === END BOUNDARIES ===

import base64
import hashlib
import io
import os
import time
import numpy as np

from .ring_core import RingCore
from .memory_core import MemoryCore
from .theta import ThetaTensor

# Audit aggregation is owned by the seed and circle layers (auditing/timing
# tensors); the neural engine orchestrates and delegates to them.
from ..seed.audit import seed_audit
from ..circle.audit import circle_audit


def _tensor_to_b64(arr: np.ndarray) -> str:
    buf = io.BytesIO()
    np.save(buf, arr)
    return base64.b64encode(buf.getvalue()).decode()


def _b64_to_tensor(s: str) -> np.ndarray:
    return np.load(io.BytesIO(base64.b64decode(s)))


RING_WEIGHTS = {
    "phi": 0.30,
    "psi": 0.15,
    "omega": 0.15,
    "theta": 0.20,
    "memory_l": 0.12,
    "memory_s": 0.08,
}

WINNER_RINGS = ["phi", "psi", "omega"]

_CHECKPOINT_DIR = os.path.join(os.path.dirname(__file__), "..", ".checkpoints")


class PCNAEngine:
    """PCNA six-ring inference engine — no stubs, all rings real."""

    def __init__(self, phases: int = 7):
        self.phases = phases
        self.phi = RingCore(name="phi", symbol="Φ", role="cognitive", n=53, seed=53, phases=phases)
        self.psi = RingCore(name="psi", symbol="Ψ", role="self_model", n=53, seed=43, phases=phases)
        self.omega = RingCore(name="omega", symbol="Ω", role="autonomy", n=53, seed=47, phases=phases)
        self.memory_l = MemoryCore(n=19, seed=19, role="long_term", phases=phases)
        self.memory_s = MemoryCore(n=17, seed=17, role="short_term", phases=phases)
        self.theta = ThetaTensor(phases=phases)
        self.infer_count = 0
        self.reward_count = 0
        self.last_coherence = 0.0
        self.last_winner = "phi"
        self.blueprint_hash = self.theta.blueprint_hash
        self.created_at = time.time()
        self.checkpoint_at: float | None = None
        self.checkpoint_ring_means: dict[str, float] = {}
        self._checkpoint_key = "pcna_checkpoint" if phases == 7 else f"pcna_checkpoint_p{phases}"

    def load_checkpoint(self):
        """Restore ring tensors from numpy checkpoint file."""
        try:
            path = os.path.join(_CHECKPOINT_DIR, f"{self._checkpoint_key}.npz")
            if not os.path.exists(path):
                return
            with np.load(path, allow_pickle=False) as data:
                ring_map = {
                    "phi": self.phi,
                    "psi": self.psi,
                    "omega": self.omega,
                    "memory_l": self.memory_l,
                    "memory_s": self.memory_s,
                }
                for name, ring in ring_map.items():
                    t_key = f"{name}_tensor"
                    if t_key not in data:
                        print(f"[pcna] checkpoint missing key: {t_key}")
                        return
                    tensor = data[t_key]
                    if tensor.shape != ring.tensor.shape:
                        print(f"[pcna] checkpoint shape mismatch on {name}: {tensor.shape} vs {ring.tensor.shape}")
                        return
                    ring.tensor = tensor
                    v_key = f"{name}_velocities"
                    if hasattr(ring, "velocities") and v_key in data:
                        vel = data[v_key]
                        if vel.shape == ring.velocities.shape:
                            ring.velocities = vel
                    if hasattr(ring, "_recompute_coherence"):
                        ring._recompute_coherence()
                    elif hasattr(ring, "_recompute_hub_avg"):
                        ring._recompute_hub_avg()
                ts = float(data["saved_at"]) if "saved_at" in data else 0.0
                self.checkpoint_at = ts if ts else None
                self.checkpoint_ring_means = {
                    name: round(float(ring_map[name].tensor.mean()), 4) for name in ring_map
                }
                print(f"[pcna] checkpoint restored: {len(ring_map)} rings, saved_at={ts}")
        except Exception as e:
            print(f"[pcna] checkpoint load failed (fresh start): {e}")

    def save_checkpoint(self):
        """Serialize all ring tensors to numpy checkpoint file."""
        try:
            os.makedirs(_CHECKPOINT_DIR, exist_ok=True)
            rings = {
                "phi": self.phi,
                "psi": self.psi,
                "omega": self.omega,
                "memory_l": self.memory_l,
                "memory_s": self.memory_s,
            }
            arrays = {"saved_at": np.array(time.time())}
            for name, ring in rings.items():
                arrays[f"{name}_tensor"] = ring.tensor
                if hasattr(ring, "velocities"):
                    arrays[f"{name}_velocities"] = ring.velocities
            path = os.path.join(_CHECKPOINT_DIR, f"{self._checkpoint_key}.npz")
            np.savez(path, **arrays)
            self.checkpoint_at = float(arrays["saved_at"])
            self.checkpoint_ring_means = {
                name: round(float(ring.tensor.mean()), 4) for name, ring in rings.items()
            }
            print(f"[pcna] checkpoint saved: {len(rings)} rings")
        except Exception as e:
            print(f"[pcna] checkpoint save failed: {e}")

    def _project(self, text: str) -> np.ndarray:
        h = hashlib.sha512(text.encode("utf-8")).digest()
        arr = np.frombuffer(h, dtype=np.uint8).astype(np.float64)
        arr = arr / 255.0
        padded = np.tile(arr, 4)[:53]
        return padded

    def _inject(self, signal: np.ndarray):
        self.phi.inject(signal)
        self.phi._recompute_coherence()
        self.memory_s.write(signal)

        theta_nc = self.theta.node_coherence
        theta_signal = np.full(53, float(theta_nc.mean()), dtype=np.float64)
        theta_signal[:len(theta_nc)] = theta_nc
        self.phi.inject(theta_signal)
        self.phi._recompute_coherence()

        psi_signal = np.full(53, self.phi.ring_coherence, dtype=np.float64)
        phi_node_c = self.phi.node_coherence
        psi_signal[:len(phi_node_c)] = phi_node_c
        self.psi.inject(psi_signal)

        try:
            from .sigma import get_sigma
            _sig = get_sigma()
            if _sig.tensor is not None and _sig.n > 0:
                sigma_signal = np.full(53, _sig.ring_coherence, dtype=np.float64)
                nc = _sig.node_coherence
                top = min(len(nc), 53)
                sigma_signal[:top] = nc[:top]
                self.psi.inject(sigma_signal)
        except Exception:
            pass

        ml_hub = self.memory_l.hub_avg
        omega_base = np.full(53, float(ml_hub.mean()), dtype=np.float64)
        omega_base[:len(ml_hub)] *= ml_hub
        omega_base = np.clip(omega_base, 0.0, 1.0)
        self.omega.inject(omega_base)

    def _propagate(self):
        self.phi.propagate(steps=10)
        self.psi.propagate(steps=8)
        self.omega.propagate(steps=6)
        self.theta.propagate(steps=5)

    def _seed_audit(self) -> dict:
        # Seed-layer auditing is owned by ptcna.seed; the neural engine only
        # supplies the cores and short-term memory to audit.
        cores = {"phi": self.phi, "psi": self.psi, "omega": self.omega}
        return seed_audit(cores, self.memory_s)

    def _circle_audit(self) -> dict:
        # Circle-layer auditing is owned by ptcna.circle.
        return circle_audit(self.theta, self.memory_l)

    def _coherence_score(self, seed_audit: dict, circle_audit: dict) -> dict:
        ring_scores = {
            "phi": seed_audit["phi_coherence"],
            "psi": seed_audit["psi_coherence"],
            "omega": seed_audit["omega_coherence"],
            "theta": circle_audit["theta_coherence"],
            "memory_l": self.memory_l.state()["avg_hub"],
            "memory_s": self.memory_s.state()["avg_hub"],
        }
        weighted = sum(RING_WEIGHTS[r] * ring_scores[r] for r in ring_scores)
        winner = max(WINNER_RINGS, key=lambda r: ring_scores[r])
        confidence = float(np.clip(weighted, 0.0, 1.0))
        return {
            "ring_scores": {k: round(v, 4) for k, v in ring_scores.items()},
            "weighted_coherence": round(weighted, 4),
            "winner": winner,
            "confidence": round(confidence, 4),
        }

    def infer(self, text: str) -> dict:
        t0 = time.time()
        signal = self._project(text)
        self._inject(signal)
        self._propagate()

        seed_audit = self._seed_audit()
        circle_audit = self._circle_audit()
        coherence = self._coherence_score(seed_audit, circle_audit)

        self.infer_count += 1
        self.last_coherence = coherence["weighted_coherence"]
        self.last_winner = coherence["winner"]

        elapsed_ms = round((time.time() - t0) * 1000, 1)

        return {
            "step": "pcna_infer",
            "infer_index": self.infer_count,
            "blueprint_hash": self.blueprint_hash[:16] + "...",
            "elapsed_ms": elapsed_ms,
            "signal_mean": round(float(signal.mean()), 4),
            "step1_project": {"signal_len": len(signal), "signal_mean": round(float(signal.mean()), 4)},
            "step2_inject": {"phi_n": 53, "psi_n": 53, "omega_n": 53, "memory_s_n": 17},
            "step3_propagate": {"phi_steps": 10, "psi_steps": 8, "omega_steps": 6, "theta_steps": 5},
            "step4_seed": seed_audit,
            "step5_circle": circle_audit,
            "step6_coherence": coherence,
            "coherence_score": coherence["weighted_coherence"],
            "winner": coherence["winner"],
            "confidence": coherence["confidence"],
            "theta_circles": int(self.theta.circle_count.mean()),
            "memory_l_state": self.memory_l.state(),
            "memory_s_state": self.memory_s.state(),
        }

    def reward(self, winner: str, outcome: float) -> dict:
        self.phi.nudge(outcome, lr=0.025)
        self.psi.nudge(outcome, lr=0.020)
        self.omega.nudge(outcome, lr=0.015)
        self.theta.apply_reward(outcome)
        flushed = self.memory_s.flush_to(self.memory_l, outcome)

        try:
            from .sigma import get_sigma
            get_sigma().nudge(outcome, lr=0.015)
        except Exception:
            pass

        self.reward_count += 1

        return {
            "step": "pcna_reward",
            "reward_index": self.reward_count,
            "winner": winner,
            "outcome": round(outcome, 4),
            "nudged": True,
            "nudged_cores": ["phi", "psi", "omega", "theta", "sigma"],
            "memory_flush": flushed,
            "phi_coherence_after": round(self.phi.ring_coherence, 4),
            "psi_coherence_after": round(self.psi.ring_coherence, 4),
            "omega_coherence_after": round(self.omega.ring_coherence, 4),
            "theta_coherence_after": round(float(self.theta.node_coherence.mean()), 4),
            "theta_circles_after": [int(v) for v in self.theta.circle_count],
            "memory_l_flush_count": self.memory_l.flush_count,
            "memory_s_flush_count": self.memory_s.flush_count,
        }

    def state(self) -> dict:
        try:
            from .zeta import _zeta_engine
            echo_history = list(_zeta_engine.echo_buffer) if _zeta_engine else []
        except Exception:
            echo_history = []

        try:
            from .sigma import get_sigma
            sigma_state = get_sigma().state()
        except Exception:
            sigma_state = {}

        theta_state = self.theta.state()

        return {
            "engine": "pcna",
            "version": "2.2.0",
            "phases": self.phases,
            "infer_count": self.infer_count,
            "reward_count": self.reward_count,
            "last_coherence": round(self.last_coherence, 4),
            "last_winner": self.last_winner,
            "rings": {
                "phi": self.phi.state(),
                "psi": self.psi.state(),
                "omega": self.omega.state(),
                "theta": theta_state,
                "sigma": sigma_state,
                "memory_l": self.memory_l.state(),
                "memory_s": self.memory_s.state(),
            },
            "ring_weights": RING_WEIGHTS,
            "uptime_s": round(time.time() - self.created_at, 1),
            "checkpoint_at": self.checkpoint_at,
            "checkpoint_ring_means": self.checkpoint_ring_means,
            "echo_history": echo_history[-20:],
        }
# 295:27
# ratios: loc_comments=266:78 imports_exports=15:1 calls_definitions=85:15
