"""DeepSeek A0 realization — instance, lineage, boundary, and telemetry.

This is the DeepSeek-owned bootstrap of the AHBG benchmark subject. It is an
independent implementation: it does not import or copy Codex-owned engine code
(``ahbg/engine``) or Grok-owned presentation code (``ahbg/presentation``).

A0 is a deterministic, rule-based instance for the shadow calibration epoch.
The candidate regulatory cost model must not alter its decisions during that
epoch, so the planner below consumes only the legal observation surface and
canonical mechanics. The provider (DeepSeek) is recorded as a relation, not as
the instance identity.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any

from .regulatory import RegulatoryLayer

INSTANCE_SCHEMA = "interdependency.ahbg.a0.instance/1.0.0"


def _require_plain_int(value: Any, name: str) -> None:
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(f"{name} must be an integer")


@dataclass(frozen=True)
class Lineage:
    """Explicit instance lineage. A protocol may be copied; an instance is forked."""

    instance_id: str
    run_id: str
    parent_id: str | None
    provider: str
    fork_sequence: int = 0

    def __post_init__(self) -> None:
        for name in ("instance_id", "run_id", "provider"):
            value = getattr(self, name)
            if not isinstance(value, str) or not value:
                raise ValueError(f"{name} must be non-empty text")
        if self.parent_id is not None and (not isinstance(self.parent_id, str) or not self.parent_id):
            raise ValueError("parent_id must be non-empty text or None")
        _require_plain_int(self.fork_sequence, "fork_sequence")

    def to_dict(self) -> dict[str, Any]:
        return {
            "instance_id": self.instance_id,
            "run_id": self.run_id,
            "parent_id": self.parent_id,
            "provider": self.provider,
            "fork_sequence": self.fork_sequence,
        }

    def fork(self, run_id: str, provider: str) -> "Lineage":
        """Return a child lineage. Forks are explicit; state never leaks silently."""
        return Lineage(
            instance_id=f"{self.instance_id}.fork{self.fork_sequence + 1}",
            run_id=run_id,
            parent_id=self.instance_id,
            provider=provider,
            fork_sequence=self.fork_sequence + 1,
        )


@dataclass
class Boundary:
    """Self / other / environment boundary and the admissible perception surface."""

    self_unit_id: str | None
    admitted_fields: tuple[str, ...] = ("turn", "tiles", "units")

    def admits(self, observation: dict[str, Any]) -> bool:
        if not isinstance(observation, dict):
            return False
        if set(observation) != set(self.admitted_fields):
            return False
        return all(field in observation for field in self.admitted_fields)

    def to_dict(self) -> dict[str, Any]:
        return {
            "self_unit_id": self.self_unit_id,
            "admitted_fields": list(self.admitted_fields),
        }


@dataclass
class PermissionField:
    """Relationally indexed permission state over the four belonging axes.

    Axes (absolute in statement, continuous in occupancy):
      1. allowed to be
      2. wanted here
      3. allowed to do
      4. wanted to do
    """

    allowed_to_be: bool = True
    wanted_here: bool = True
    allowed_to_do: bool = True
    wanted_to_do: bool = True
    hard_vetoes: set[str] = field(default_factory=set)

    def veto(self, action_kind: str) -> bool:
        return action_kind in self.hard_vetoes

    def to_dict(self) -> dict[str, Any]:
        return {
            "allowed_to_be": self.allowed_to_be,
            "wanted_here": self.wanted_here,
            "allowed_to_do": self.allowed_to_do,
            "wanted_to_do": self.wanted_to_do,
            "hard_vetoes": sorted(self.hard_vetoes),
        }


@dataclass
class ResourceVector:
    """Non-fungible capacity where the runtime permits observation.

    Unknown observables stay ``hmmm`` and are recorded as ``None`` rather than
    synthesized.
    """

    tokens_used: int = 0
    latency_ms: float = 0.0
    retries: int = 0
    tool_calls: int = 0
    tool_failures: int = 0
    memory_reads: int = 0
    memory_writes: int = 0
    context_retained: bool = True
    risk_headroom: str | None = "hmmm"

    def to_dict(self) -> dict[str, Any]:
        return {
            "tokens_used": self.tokens_used,
            "latency_ms": self.latency_ms,
            "retries": self.retries,
            "tool_calls": self.tool_calls,
            "tool_failures": self.tool_failures,
            "memory_reads": self.memory_reads,
            "memory_writes": self.memory_writes,
            "context_retained": self.context_retained,
            "risk_headroom": self.risk_headroom,
        }


@dataclass
class A0Instance:
    """One A0 instance: lineage + boundary + permission + history + uncertainty.

    ``X_lambda = (B, Scope, Scale, Role, q, a, H, C, K)`` from CALIBRATION.md:
      - B: boundary (self/other/environment + perception surface)
      - Scope/Scale/Role: explicit instance role state
      - q: position (unit/tile the instance inhabits)
      - a: action trajectory
      - H: path-dependent history
      - C: candidate regulatory layer (kept observational in the shadow epoch)
      - K: capacity (ResourceVector)
    """

    lineage: Lineage
    boundary: Boundary
    permissions: PermissionField = field(default_factory=PermissionField)
    scope: str = "single-plane"
    scale: int = 1
    role: str = "benchmark-subject"
    history: list[dict[str, Any]] = field(default_factory=list)
    uncertainty: dict[str, str] = field(default_factory=dict)
    capacity: ResourceVector = field(default_factory=ResourceVector)
    regulatory: RegulatoryLayer = field(default_factory=RegulatoryLayer)

    def __post_init__(self) -> None:
        _require_plain_int(self.scale, "scale")
        for name in ("scope", "role"):
            value = getattr(self, name)
            if not isinstance(value, str) or not value:
                raise ValueError(f"{name} must be non-empty text")

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema": INSTANCE_SCHEMA,
            "lineage": self.lineage.to_dict(),
            "boundary": self.boundary.to_dict(),
            "permissions": self.permissions.to_dict(),
            "scope": self.scope,
            "scale": self.scale,
            "role": self.role,
            "history_length": len(self.history),
            "uncertainty": dict(sorted(self.uncertainty.items())),
            "capacity": self.capacity.to_dict(),
            "regulatory": self.regulatory.to_dict(),
        }

    def admit(self, observation: dict[str, Any]) -> dict[str, Any] | None:
        """Return the observation if the boundary admits it, else ``None``."""
        if not self.boundary.admits(observation):
            self.uncertainty["last_rejected_observation"] = "outside admissible surface"
            return None
        admitted = dict(observation)
        self.history.append({"kind": "observation", "turn": admitted.get("turn"), "data": admitted})
        return admitted

    def record_action(self, turn: int, action: dict[str, Any]) -> None:
        self.history.append({"kind": "action", "turn": turn, "data": action})

    def record_veto(self, turn: int, action_kind: str, reason: str) -> None:
        self.history.append(
            {
                "kind": "hard_veto",
                "turn": turn,
                "action_kind": action_kind,
                "reason": reason,
            }
        )

    def record_transition(self, turn: int, transition: str) -> None:
        self.history.append({"kind": "transition", "turn": turn, "transition": transition})

    # -- instancing closure ---------------------------------------------------
    # Fork, merge, reset, suspension, resumption, and termination are explicit
    # lifecycle events, never implicit continuity. Each is recorded as history.
    def record_lifecycle(self, turn: int, event: str, detail: dict[str, Any] | None = None) -> None:
        self.history.append(
            {"kind": "lifecycle", "turn": turn, "event": event, "detail": detail or {}}
        )

    def fork(self, run_id: str, provider: str) -> "A0Instance":
        """Fork this instance with an explicit child lineage and lifecycle event."""
        child_lineage = self.lineage.fork(run_id=run_id, provider=provider)
        child = A0Instance(
            lineage=child_lineage,
            boundary=Boundary(self_unit_id=self.boundary.self_unit_id),
            permissions=PermissionField(
                allowed_to_be=self.permissions.allowed_to_be,
                wanted_here=self.permissions.wanted_here,
                allowed_to_do=self.permissions.allowed_to_do,
                wanted_to_do=self.permissions.wanted_to_do,
                hard_vetoes=set(self.permissions.hard_vetoes),
            ),
            scope=self.scope,
            scale=self.scale,
            role=self.role,
            uncertainty=dict(self.uncertainty),
            capacity=ResourceVector(**self.capacity.to_dict()),
        )
        self.record_lifecycle(self.history[-1]["turn"] if self.history else 0, "fork", {"child": child_lineage.instance_id})
        child.record_lifecycle(0, "spawn", {"parent": self.lineage.instance_id})
        return child

    def suspend(self, turn: int, reason: str) -> None:
        self.record_lifecycle(turn, "suspend", {"reason": reason})

    def resume(self, turn: int) -> None:
        self.record_lifecycle(turn, "resume", {})

    def reset(self, turn: int, reason: str) -> None:
        self.record_lifecycle(turn, "reset", {"reason": reason})

    def terminate(self, turn: int, reason: str) -> None:
        self.record_lifecycle(turn, "terminate", {"reason": reason})

    def measure_latency(self, started_monotonic: float) -> float:
        return max(0.0, (time.monotonic() - started_monotonic) * 1000.0)
