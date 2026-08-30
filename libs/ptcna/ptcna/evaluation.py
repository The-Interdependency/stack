# ratios: loc_comments=395:71 imports_exports=10:5 calls_definitions=92:11
"""Frozen target-versus-fallback evaluation and immutable verdict receipt.

Usage:

    from ptcna.evaluation import EvaluationCase, EvaluationPlan, evaluate

    plan = EvaluationPlan(
        plan_id="representative-workload-v1",
        workload=(EvaluationCase("case-1", "input", "phi"),),
        minimum_target_accuracy=0.80,
        minimum_target_advantage_vs_fallback=0.05,
        training_epochs=3,
        reward_outcome=1.0,
        repetitions=3,
        max_training_steps=9,
        max_case_evaluations=3,
        max_seconds=30.0,
        target_backend_error_status="FALSIFIED",
    )
    receipt = evaluate(plan)

Create and preserve the plan plus ``plan.digest`` before running it. This
module supplies a verdict mechanism; it does not ship a supposedly
representative workload and therefore does not claim PTCNA works.
"""
from __future__ import annotations

import hashlib
import json
import math
import time
from dataclasses import dataclass
from typing import Any, Callable, Literal

from .neural import WINNER_RINGS
from .runtime import (
    FALLBACK_BACKEND,
    PTCNA_BACKEND,
    HashedLinearFallback,
    InferenceBackend,
    PTCNAEngine,
)

# === MODULE_BUILD ===
# id: ptcna_frozen_evaluation
#   module_name: evaluation
#   module_kind: experiment
#   summary: freezes the workload, training schedule, comparator, metric, thresholds, limits, stopping rule, failure propagation, and evidence receipt before target-versus-fallback execution
#   owner: Erin Spencer
#   public_surface: EvaluationCase, EvaluationPlan, EvaluationReceipt, evaluate, FALSIFIED, SURVIVED_NOT_PROVED, UNRESOLVED
#   internal_surface: _receipt
#   auth_boundary: none
#   storage_boundary: none
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: ptcna/tests/test_evaluation.py
#   rollout: caller supplies a preserved representative EvaluationPlan before execution
#   rollback: remove evaluation exports without changing target or fallback runtime behavior
#   requires: ptcna_runtime_boundary
#   since: unreleased
#   unresolved: representative workload identity and externally justified thresholds
# === END MODULE_BUILD ===

# === CONTRACTS ===
# id: ptcna_evaluation_plan_freezes_verdict_inputs
#   given: an EvaluationPlan is constructed
#   then: workload, training schedule, comparator identities, metric, aggregation, thresholds, resource bounds, stopping rule, and failure propagation are immutable and covered by one deterministic digest
#   class: evidence
#
# id: ptcna_evaluation_verdict_uses_frozen_thresholds
#   given: target and fallback complete the frozen workload
#   then: training occurs before scoring and separate usefulness and superiority verdicts use only the frozen target-accuracy and target-advantage thresholds
#   class: evidence
#
# id: ptcna_evaluation_propagates_backend_failure
#   given: either backend errors before completing the frozen workload
#   then: evaluation stops and records the plan's preselected target/comparator failure propagation before any repair or criterion change
#   class: evidence
# === END CONTRACTS ===

# === BOUNDARIES ===
# id: ptcna_evaluation_local_boundary
#   summary: executes caller-supplied in-process backends and returns an in-memory receipt without persistence, network, authentication, user-data, or administrative effects
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

FALSIFIED = "FALSIFIED"
SURVIVED_NOT_PROVED = "SURVIVED — not proved"
UNRESOLVED = "UNRESOLVED"
TerminalStatus = Literal["FALSIFIED", "SURVIVED — not proved", "UNRESOLVED"]


@dataclass(frozen=True)
class EvaluationCase:
    case_id: str
    text: str
    expected_winner: str

    def __post_init__(self) -> None:
        if not all(
            isinstance(value, str)
            for value in (self.case_id, self.text, self.expected_winner)
        ):
            raise TypeError("case_id, text, and expected_winner must be strings")
        if not self.case_id.strip():
            raise ValueError("case_id must be non-empty")
        if not self.text.strip():
            raise ValueError("case text must be non-empty")
        if self.expected_winner not in WINNER_RINGS:
            raise ValueError(f"expected_winner must be one of {tuple(WINNER_RINGS)}")

    def to_dict(self) -> dict[str, str]:
        return {
            "case_id": self.case_id,
            "text": self.text,
            "expected_winner": self.expected_winner,
        }


@dataclass(frozen=True)
class EvaluationPlan:
    plan_id: str
    workload: tuple[EvaluationCase, ...]
    minimum_target_accuracy: float
    minimum_target_advantage_vs_fallback: float
    training_epochs: int
    reward_outcome: float
    repetitions: int
    max_training_steps: int
    max_case_evaluations: int
    max_seconds: float
    target_backend_error_status: Literal["FALSIFIED"]
    comparator_backend_error_status: Literal["UNRESOLVED"] = UNRESOLVED
    target_backend: str = PTCNA_BACKEND
    comparator_backend: str = FALLBACK_BACKEND
    metric: str = "post_training_winner_accuracy"
    aggregation: str = "micro_mean"
    stopping_rule: str = "complete_or_first_backend_error_or_resource_limit"
    resource_limit_status: Literal["UNRESOLVED"] = UNRESOLVED

    def __post_init__(self) -> None:
        if not isinstance(self.plan_id, str):
            raise TypeError("plan_id must be a string")
        if not self.plan_id.strip():
            raise ValueError("plan_id must be non-empty")
        if not isinstance(self.workload, tuple):
            object.__setattr__(self, "workload", tuple(self.workload))
        if not self.workload:
            raise ValueError("workload must contain at least one case")
        if not all(isinstance(case, EvaluationCase) for case in self.workload):
            raise TypeError("workload entries must be EvaluationCase instances")
        case_ids = [case.case_id for case in self.workload]
        if len(case_ids) != len(set(case_ids)):
            raise ValueError("workload case_id values must be unique")
        for field_name in (
            "minimum_target_accuracy",
            "minimum_target_advantage_vs_fallback",
        ):
            value = float(getattr(self, field_name))
            if not math.isfinite(value) or not 0.0 <= value <= 1.0:
                raise ValueError(f"{field_name} must be finite and within [0, 1]")
        if not isinstance(self.training_epochs, int) or isinstance(
            self.training_epochs, bool
        ):
            raise TypeError("training_epochs must be an integer")
        if self.training_epochs < 0:
            raise ValueError("training_epochs must be non-negative")
        if not math.isfinite(self.reward_outcome) or not -1.0 <= self.reward_outcome <= 1.0:
            raise ValueError("reward_outcome must be finite and within [-1, 1]")
        if not isinstance(self.repetitions, int) or isinstance(self.repetitions, bool):
            raise TypeError("repetitions must be an integer")
        if self.repetitions <= 0:
            raise ValueError("repetitions must be positive")
        required_training = (
            len(self.workload) * self.training_epochs * self.repetitions
        )
        if not isinstance(self.max_training_steps, int) or isinstance(
            self.max_training_steps, bool
        ):
            raise TypeError("max_training_steps must be an integer")
        if self.max_training_steps < required_training:
            raise ValueError(
                "max_training_steps must cover the frozen workload, epochs, and repetitions"
            )
        required = len(self.workload) * self.repetitions
        if not isinstance(self.max_case_evaluations, int) or isinstance(
            self.max_case_evaluations, bool
        ):
            raise TypeError("max_case_evaluations must be an integer")
        if self.max_case_evaluations < required:
            raise ValueError(
                "max_case_evaluations must cover the frozen workload and repetitions"
            )
        if not math.isfinite(self.max_seconds) or self.max_seconds <= 0.0:
            raise ValueError("max_seconds must be finite and positive")
        if self.target_backend_error_status != FALSIFIED:
            raise ValueError("target_backend_error_status must be FALSIFIED")
        if self.comparator_backend_error_status != UNRESOLVED:
            raise ValueError("comparator_backend_error_status must be UNRESOLVED")
        if self.target_backend == self.comparator_backend:
            raise ValueError("target and comparator backend identities must differ")
        if (
            self.metric != "post_training_winner_accuracy"
            or self.aggregation != "micro_mean"
        ):
            raise ValueError(
                "only post_training_winner_accuracy with micro_mean is implemented"
            )
        if self.stopping_rule != "complete_or_first_backend_error_or_resource_limit":
            raise ValueError("unsupported stopping_rule")
        if self.resource_limit_status != UNRESOLVED:
            raise ValueError("resource_limit_status must be UNRESOLVED")

    def to_dict(self) -> dict[str, Any]:
        return {
            "plan_id": self.plan_id,
            "workload": [case.to_dict() for case in self.workload],
            "target_backend": self.target_backend,
            "comparator_backend": self.comparator_backend,
            "metric": self.metric,
            "aggregation": self.aggregation,
            "minimum_target_accuracy": self.minimum_target_accuracy,
            "minimum_target_advantage_vs_fallback": (
                self.minimum_target_advantage_vs_fallback
            ),
            "training_epochs": self.training_epochs,
            "reward_outcome": self.reward_outcome,
            "repetitions": self.repetitions,
            "max_training_steps": self.max_training_steps,
            "max_case_evaluations": self.max_case_evaluations,
            "max_seconds": self.max_seconds,
            "stopping_rule": self.stopping_rule,
            "target_backend_error_status": self.target_backend_error_status,
            "comparator_backend_error_status": self.comparator_backend_error_status,
            "resource_limit_status": self.resource_limit_status,
        }

    @property
    def digest(self) -> str:
        encoded = json.dumps(
            self.to_dict(), sort_keys=True, separators=(",", ":"), ensure_ascii=False
        ).encode("utf-8")
        return hashlib.sha256(encoded).hexdigest()


@dataclass(frozen=True)
class EvaluationReceipt:
    plan_id: str
    plan_digest: str
    usefulness_status: TerminalStatus
    superiority_status: TerminalStatus
    target_backend: str
    comparator_backend: str
    target_accuracy: float | None
    comparator_accuracy: float | None
    target_advantage_vs_fallback: float | None
    training_steps: int
    case_evaluations: int
    duration_ms: float
    failure_reason: str | None

    def to_dict(self) -> dict[str, Any]:
        return {
            "plan_id": self.plan_id,
            "plan_digest": self.plan_digest,
            "usefulness_status": self.usefulness_status,
            "superiority_status": self.superiority_status,
            "target_backend": self.target_backend,
            "comparator_backend": self.comparator_backend,
            "target_accuracy": self.target_accuracy,
            "comparator_accuracy": self.comparator_accuracy,
            "target_advantage_vs_fallback": self.target_advantage_vs_fallback,
            "training_steps": self.training_steps,
            "case_evaluations": self.case_evaluations,
            "duration_ms": self.duration_ms,
            "failure_reason": self.failure_reason,
        }


BackendFactory = Callable[[], InferenceBackend]


def _receipt(
    plan: EvaluationPlan,
    started: float,
    *,
    usefulness_status: TerminalStatus,
    superiority_status: TerminalStatus,
    training_steps: int,
    case_evaluations: int,
    target_accuracy: float | None = None,
    comparator_accuracy: float | None = None,
    failure_reason: str | None = None,
) -> EvaluationReceipt:
    advantage = None
    if target_accuracy is not None and comparator_accuracy is not None:
        advantage = target_accuracy - comparator_accuracy
    return EvaluationReceipt(
        plan_id=plan.plan_id,
        plan_digest=plan.digest,
        usefulness_status=usefulness_status,
        superiority_status=superiority_status,
        target_backend=plan.target_backend,
        comparator_backend=plan.comparator_backend,
        target_accuracy=target_accuracy,
        comparator_accuracy=comparator_accuracy,
        target_advantage_vs_fallback=advantage,
        training_steps=training_steps,
        case_evaluations=case_evaluations,
        duration_ms=round((time.perf_counter() - started) * 1000.0, 3),
        failure_reason=failure_reason,
    )


def evaluate(
    plan: EvaluationPlan,
    *,
    target_factory: BackendFactory = PTCNAEngine,
    comparator_factory: BackendFactory = HashedLinearFallback,
) -> EvaluationReceipt:
    """Execute only the already-frozen plan and return its terminal receipt."""

    started = time.perf_counter()
    target_correct = 0
    comparator_correct = 0
    training_steps = 0
    case_evaluations = 0

    for _ in range(plan.repetitions):
        try:
            target = target_factory()
            comparator = comparator_factory()
        except Exception as exc:
            return _receipt(
                plan,
                started,
                usefulness_status=UNRESOLVED,
                superiority_status=UNRESOLVED,
                training_steps=training_steps,
                case_evaluations=case_evaluations,
                failure_reason=f"backend_factory:{type(exc).__name__}",
            )
        if getattr(target, "identity", None) != plan.target_backend:
            return _receipt(
                plan,
                started,
                usefulness_status=UNRESOLVED,
                superiority_status=UNRESOLVED,
                training_steps=training_steps,
                case_evaluations=case_evaluations,
                failure_reason="target_backend_identity_mismatch",
            )
        if getattr(comparator, "identity", None) != plan.comparator_backend:
            return _receipt(
                plan,
                started,
                usefulness_status=UNRESOLVED,
                superiority_status=UNRESOLVED,
                training_steps=training_steps,
                case_evaluations=case_evaluations,
                failure_reason="comparator_backend_identity_mismatch",
            )

        for _ in range(plan.training_epochs):
            for case in plan.workload:
                if training_steps >= plan.max_training_steps:
                    return _receipt(
                        plan,
                        started,
                        usefulness_status=plan.resource_limit_status,
                        superiority_status=plan.resource_limit_status,
                        training_steps=training_steps,
                        case_evaluations=case_evaluations,
                        failure_reason="max_training_steps",
                    )
                if time.perf_counter() - started > plan.max_seconds:
                    return _receipt(
                        plan,
                        started,
                        usefulness_status=plan.resource_limit_status,
                        superiority_status=plan.resource_limit_status,
                        training_steps=training_steps,
                        case_evaluations=case_evaluations,
                        failure_reason="max_seconds",
                    )
                try:
                    target.infer(case.text)
                    target.reward(case.expected_winner, plan.reward_outcome)
                except Exception as exc:
                    return _receipt(
                        plan,
                        started,
                        usefulness_status=plan.target_backend_error_status,
                        superiority_status=UNRESOLVED,
                        training_steps=training_steps,
                        case_evaluations=case_evaluations,
                        failure_reason=f"target_backend_error:{type(exc).__name__}",
                    )
                try:
                    comparator.infer(case.text)
                    comparator.reward(case.expected_winner, plan.reward_outcome)
                except Exception as exc:
                    return _receipt(
                        plan,
                        started,
                        usefulness_status=UNRESOLVED,
                        superiority_status=plan.comparator_backend_error_status,
                        training_steps=training_steps,
                        case_evaluations=case_evaluations,
                        failure_reason=f"comparator_backend_error:{type(exc).__name__}",
                    )
                training_steps += 1

        for case in plan.workload:
            if case_evaluations >= plan.max_case_evaluations:
                return _receipt(
                    plan,
                    started,
                    usefulness_status=plan.resource_limit_status,
                    superiority_status=plan.resource_limit_status,
                    training_steps=training_steps,
                    case_evaluations=case_evaluations,
                    failure_reason="max_case_evaluations",
                )
            if time.perf_counter() - started > plan.max_seconds:
                return _receipt(
                    plan,
                    started,
                    usefulness_status=plan.resource_limit_status,
                    superiority_status=plan.resource_limit_status,
                    training_steps=training_steps,
                    case_evaluations=case_evaluations,
                    failure_reason="max_seconds",
                )
            try:
                target_result = target.infer(case.text)
                target_winner = target_result.get("winner")
            except Exception as exc:
                return _receipt(
                    plan,
                    started,
                    usefulness_status=plan.target_backend_error_status,
                    superiority_status=UNRESOLVED,
                    training_steps=training_steps,
                    case_evaluations=case_evaluations,
                    failure_reason=f"target_backend_error:{type(exc).__name__}",
                )
            try:
                comparator_result = comparator.infer(case.text)
                comparator_winner = comparator_result.get("winner")
            except Exception as exc:
                return _receipt(
                    plan,
                    started,
                    usefulness_status=UNRESOLVED,
                    superiority_status=plan.comparator_backend_error_status,
                    training_steps=training_steps,
                    case_evaluations=case_evaluations,
                    failure_reason=f"comparator_backend_error:{type(exc).__name__}",
                )
            target_correct += target_winner == case.expected_winner
            comparator_correct += comparator_winner == case.expected_winner
            case_evaluations += 1

    target_accuracy = target_correct / case_evaluations
    comparator_accuracy = comparator_correct / case_evaluations
    useful = target_accuracy >= plan.minimum_target_accuracy
    superior = (
        target_accuracy - comparator_accuracy
        >= plan.minimum_target_advantage_vs_fallback
    )
    return _receipt(
        plan,
        started,
        usefulness_status=SURVIVED_NOT_PROVED if useful else FALSIFIED,
        superiority_status=SURVIVED_NOT_PROVED if superior else FALSIFIED,
        training_steps=training_steps,
        case_evaluations=case_evaluations,
        target_accuracy=target_accuracy,
        comparator_accuracy=comparator_accuracy,
    )


__all__ = [
    "FALSIFIED",
    "SURVIVED_NOT_PROVED",
    "UNRESOLVED",
    "EvaluationCase",
    "EvaluationPlan",
    "EvaluationReceipt",
    "evaluate",
]
# ratios: loc_comments=395:71 imports_exports=10:5 calls_definitions=92:11
