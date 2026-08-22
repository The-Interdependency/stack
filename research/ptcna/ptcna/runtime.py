# ratios: loc_comments=243:78 imports_exports=8:5 calls_definitions=58:23
"""Explicit runtime boundary for the experimental PTCNA path and fallback.

Usage:

    from ptcna.runtime import PTCNARuntime

    runtime = PTCNARuntime()
    target = runtime.infer("bounded question")
    fallback = runtime.infer("bounded question", backend="fallback")

The target path constructs the repository's full four-layer architecture. The
fallback is a deterministic hashed linear learner behind the same
``infer``/``reward`` task surface. A target failure raises by default. Callers
must set ``fallback_on_error=True`` to continue through the fallback, and the
returned receipt always names the backend actually used.
"""
from __future__ import annotations

import hashlib
import math
from typing import Any, Literal, Mapping, Protocol

import numpy as np

from .core.prime_core import Core, CoreSpec, build_core
from .neural import PCNAEngine, WINNER_RINGS

# === MODULE_BUILD ===
# id: ptcna_runtime_boundary
#   module_name: runtime
#   module_kind: engine
#   summary: exposes the intended four-layer PTCNA path and a distinct dependable fallback behind one attributed task interface
#   owner: Erin Spencer
#   public_surface: PTCNAEngine, HashedLinearFallback, PTCNARuntime, InferenceBackend, PTCNA_BACKEND, FALLBACK_BACKEND
#   internal_surface: _validate_text, _validate_reward, _attach_route
#   auth_boundary: none
#   storage_boundary: none
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: ptcna/tests/test_runtime.py
#   rollout: explicit public API; target selected by default and fallback selected or enabled by the caller
#   rollback: remove runtime exports while preserving the existing layer modules and PCNAEngine
#   requires: pcna_pcna, ptcna_prime_core_composition
#   since: unreleased
#   unresolved: representative task workload and whether either backend is useful under it
# === END MODULE_BUILD ===

# === CONTRACTS ===
# id: ptcna_target_reports_four_live_layers
#   given: non-empty text is inferred through PTCNAEngine
#   then: the receipt identifies the experimental PTCNA backend and reports neural, circle, seed, and core layer state without transferring gradients to structural layers
#   class: correctness
#
# id: ptcna_fallback_is_distinct_and_deterministic
#   given: identical text and fresh HashedLinearFallback instances
#   then: both produce the same bounded prediction under a fallback identity that is never labeled PTCNA
#   class: correctness
#
# id: ptcna_fallback_reward_changes_selected_score
#   given: the fallback infers text and receives a positive bounded reward for the selected winner
#   then: a second inference of the same text gives that winner a strictly greater linear score
#   class: correctness
#
# id: ptcna_failover_is_explicit_and_attributed
#   given: the target raises during inference
#   then: PTCNARuntime raises by default and uses the fallback only when explicitly enabled while recording the target failure and actual backend
#   class: safety
#
# id: ptcna_reward_follows_backend_receipt
#   given: a reward is applied to an inference receipt
#   then: only the backend named by backend_used receives the reward
#   class: safety
# === END CONTRACTS ===

# === BOUNDARIES ===
# id: ptcna_runtime_local_boundary
#   summary: performs deterministic in-process inference and learning with no authentication, persistence, network, user-data, or administrative effect
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

PTCNA_BACKEND = "ptcna.experimental.v1"
FALLBACK_BACKEND = "fallback.hashed-linear.v1"
BackendChoice = Literal["ptcna", "fallback"]


class InferenceBackend(Protocol):
    """Shared task surface implemented independently by target and fallback."""

    identity: str

    def infer(self, text: str) -> dict[str, Any]: ...

    def reward(self, winner: str, outcome: float) -> dict[str, Any]: ...

    def state(self) -> dict[str, Any]: ...


def _validate_text(text: str) -> None:
    if not isinstance(text, str) or not text.strip():
        raise ValueError("text must be a non-empty string")


def _validate_reward(winner: str, outcome: float) -> float:
    if winner not in WINNER_RINGS:
        raise ValueError(f"winner must be one of {tuple(WINNER_RINGS)}")
    outcome = float(outcome)
    if not math.isfinite(outcome) or not -1.0 <= outcome <= 1.0:
        raise ValueError("outcome must be finite and within [-1, 1]")
    return outcome


class PTCNAEngine:
    """Target backend joining the live neural engine to the full local core."""

    identity = PTCNA_BACKEND

    def __init__(self, phases: int = 7, core_spec: CoreSpec | None = None) -> None:
        self.neural = PCNAEngine(phases=phases)
        self.core: Core = build_core(
            core_spec if core_spec is not None else CoreSpec(), init=0.0
        )
        self._core_state = {
            "requires_grad": self.core.requires_grad,
            "seed_count": self.core.spec.seed_count,
            "circles_per_seed": self.core.spec.circles_per_seed,
            "tensors_per_circle": self.core.spec.tensors_per_circle,
            "tensor_dim": self.core.spec.tensor_dim,
            "tensor_leaves": self.core.spec.tensor_leaves,
            "param_positions": self.core.spec.param_count,
            "ucns_state": self.core.ucns_status.state.value,
            "ucns_adapter_active": self.core.ucns_status.adapter_active,
            "ucns_producer_profile": self.core.ucns_status.producer_profile,
            "ucns_state_sha256": self.core.ucns_status.state_sha256,
            "provenance": (
                "ucns-candidate-state"
                if self.core.ucns_status.adapter_active
                else "ptcna-local"
            ),
        }

    def infer(self, text: str) -> dict[str, Any]:
        """Run the experimental architecture and return an attributed receipt."""

        _validate_text(text)
        neural_receipt = self.neural.infer(text)
        result = dict(neural_receipt)
        result.update(
            {
                "architecture": "ptcna",
                "backend": self.identity,
                "layers": {
                    "neural": {
                        "requires_grad": True,
                        "engine": "PCNAEngine",
                        "infer_index": neural_receipt["infer_index"],
                    },
                    "circle": {
                        "requires_grad": False,
                        **neural_receipt["step5_circle"],
                    },
                    "seed": {
                        "requires_grad": False,
                        **neural_receipt["step4_seed"],
                    },
                    "core": dict(self._core_state),
                },
            }
        )
        return result

    def reward(self, winner: str, outcome: float) -> dict[str, Any]:
        """Reward the neural owner; structural layers remain non-differentiating."""

        outcome = _validate_reward(winner, outcome)
        result = dict(self.neural.reward(winner, outcome))
        result["backend"] = self.identity
        result["structural_layers_nudged"] = False
        return result

    def state(self) -> dict[str, Any]:
        return {
            "backend": self.identity,
            "architecture": "ptcna",
            "neural": self.neural.state(),
            "core": dict(self._core_state),
        }


class HashedLinearFallback:
    """Deterministic in-memory online learner used only as the fallback path."""

    identity = FALLBACK_BACKEND
    feature_count = 53

    def __init__(self, learning_rate: float = 0.1) -> None:
        learning_rate = float(learning_rate)
        if not math.isfinite(learning_rate) or learning_rate <= 0.0:
            raise ValueError("learning_rate must be finite and positive")
        self.learning_rate = learning_rate
        self._weights = np.zeros(
            (len(WINNER_RINGS), self.feature_count), dtype=np.float64
        )
        self._last_features: np.ndarray | None = None
        self.infer_count = 0
        self.reward_count = 0

    @classmethod
    def _features(cls, text: str) -> np.ndarray:
        digest = hashlib.sha512(text.encode("utf-8")).digest()
        values = np.frombuffer(digest, dtype=np.uint8)[: cls.feature_count]
        features = (values.astype(np.float64) - 127.5) / 127.5
        norm = float(np.linalg.norm(features))
        return features / norm if norm else features

    def infer(self, text: str) -> dict[str, Any]:
        _validate_text(text)
        features = self._features(text)
        scores = self._weights @ features
        shifted = scores - float(scores.max())
        probabilities = np.exp(shifted)
        probabilities /= float(probabilities.sum())
        winner_index = int(np.argmax(probabilities))
        self._last_features = features
        self.infer_count += 1
        return {
            "step": "fallback_infer",
            "architecture": "hashed_linear_fallback",
            "backend": self.identity,
            "infer_index": self.infer_count,
            "winner": WINNER_RINGS[winner_index],
            "confidence": round(float(probabilities[winner_index]), 6),
            "scores": {
                label: round(float(scores[index]), 6)
                for index, label in enumerate(WINNER_RINGS)
            },
        }

    def reward(self, winner: str, outcome: float) -> dict[str, Any]:
        outcome = _validate_reward(winner, outcome)
        if self._last_features is None:
            raise RuntimeError("fallback reward requires a preceding inference")
        winner_index = WINNER_RINGS.index(winner)
        self._weights[winner_index] += (
            self.learning_rate * outcome * self._last_features
        )
        self.reward_count += 1
        return {
            "step": "fallback_reward",
            "backend": self.identity,
            "reward_index": self.reward_count,
            "winner": winner,
            "outcome": outcome,
        }

    def state(self) -> dict[str, Any]:
        return {
            "backend": self.identity,
            "feature_count": self.feature_count,
            "learning_rate": self.learning_rate,
            "infer_count": self.infer_count,
            "reward_count": self.reward_count,
            "weights_digest": hashlib.sha256(self._weights.tobytes()).hexdigest(),
        }


def _attach_route(
    result: Mapping[str, Any],
    *,
    requested_backend: BackendChoice,
    backend_used: str,
    routing_reason: Literal["requested", "target_failure"],
    target_error: str | None = None,
) -> dict[str, Any]:
    receipt = dict(result)
    receipt.update(
        {
            "requested_backend": requested_backend,
            "backend_used": backend_used,
            "fallback_used": backend_used == FALLBACK_BACKEND,
            "routing_reason": routing_reason,
            "target_error": target_error,
        }
    )
    return receipt


class PTCNARuntime:
    """Select target or fallback without hiding which implementation ran."""

    def __init__(
        self,
        target: InferenceBackend | None = None,
        fallback: InferenceBackend | None = None,
    ) -> None:
        self.target = target if target is not None else PTCNAEngine()
        self.fallback = fallback if fallback is not None else HashedLinearFallback()

    def infer(
        self,
        text: str,
        *,
        backend: BackendChoice = "ptcna",
        fallback_on_error: bool = False,
    ) -> dict[str, Any]:
        _validate_text(text)
        if backend == "fallback":
            return _attach_route(
                self.fallback.infer(text),
                requested_backend=backend,
                backend_used=self.fallback.identity,
                routing_reason="requested",
            )
        if backend != "ptcna":
            raise ValueError("backend must be 'ptcna' or 'fallback'")
        try:
            result = self.target.infer(text)
        except Exception as exc:
            if not fallback_on_error:
                raise
            return _attach_route(
                self.fallback.infer(text),
                requested_backend=backend,
                backend_used=self.fallback.identity,
                routing_reason="target_failure",
                target_error=type(exc).__name__,
            )
        return _attach_route(
            result,
            requested_backend=backend,
            backend_used=self.target.identity,
            routing_reason="requested",
        )

    def reward(self, receipt: Mapping[str, Any], outcome: float) -> dict[str, Any]:
        """Route reward to the backend recorded by a prior inference receipt."""

        backend_used = receipt.get("backend_used")
        winner = receipt.get("winner")
        if not isinstance(winner, str):
            raise ValueError("receipt must contain a string winner")
        if backend_used == self.target.identity:
            return self.target.reward(winner, outcome)
        if backend_used == self.fallback.identity:
            return self.fallback.reward(winner, outcome)
        raise ValueError("receipt backend_used does not match this runtime")

    def state(self) -> dict[str, Any]:
        return {
            "target": self.target.state(),
            "fallback": self.fallback.state(),
        }


__all__ = [
    "PTCNA_BACKEND",
    "FALLBACK_BACKEND",
    "InferenceBackend",
    "PTCNAEngine",
    "HashedLinearFallback",
    "PTCNARuntime",
]
# ratios: loc_comments=243:78 imports_exports=8:5 calls_definitions=58:23
