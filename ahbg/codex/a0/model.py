"""A0 instance state for the Codex AHBG calibration build."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping

A0_STATE_SCHEMA = "interdependency.ahbg.codex.a0.state/1.0.0"


def _plain_int(value: Any, field_name: str) -> None:
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(f"{field_name} must be an integer")


def _text(value: Any, field_name: str) -> None:
    if not isinstance(value, str) or not value:
        raise ValueError(f"{field_name} must be non-empty text")


@dataclass(frozen=True)
class Lineage:
    """A running instance identity, separate from its model/provider."""

    instance_id: str
    run_id: str
    parent_instance_id: str | None
    provider_relation: str
    generation: int = 0

    def __post_init__(self) -> None:
        _text(self.instance_id, "instance_id")
        _text(self.run_id, "run_id")
        _text(self.provider_relation, "provider_relation")
        if self.parent_instance_id is not None:
            _text(self.parent_instance_id, "parent_instance_id")
        _plain_int(self.generation, "generation")
        if self.generation < 0:
            raise ValueError("generation must be non-negative")

    def fork(self, run_id: str) -> "Lineage":
        """Create an explicit child lineage; no state leaks silently."""
        _text(run_id, "run_id")
        return Lineage(
            instance_id=f"{self.instance_id}.fork.{self.generation + 1}",
            run_id=run_id,
            parent_instance_id=self.instance_id,
            provider_relation=self.provider_relation,
            generation=self.generation + 1,
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "instance_id": self.instance_id,
            "run_id": self.run_id,
            "parent_instance_id": self.parent_instance_id,
            "provider_relation": self.provider_relation,
            "generation": self.generation,
        }


@dataclass(frozen=True)
class Boundary:
    """The admissible perception surface for this A0 instance."""

    self_unit_id: str
    admitted_fields: tuple[str, ...] = ("turn", "tiles", "units", "context")

    def __post_init__(self) -> None:
        _text(self.self_unit_id, "self_unit_id")
        if not self.admitted_fields:
            raise ValueError("admitted_fields must not be empty")
        for field_name in self.admitted_fields:
            _text(field_name, "admitted field")

    def admit(self, observation: Mapping[str, Any]) -> bool:
        if not isinstance(observation, Mapping):
            return False
        unknown = set(observation) - set(self.admitted_fields)
        return not unknown and all(field in observation for field in ("turn", "tiles", "units"))

    def to_dict(self) -> dict[str, Any]:
        return {
            "self_unit_id": self.self_unit_id,
            "admitted_fields": list(self.admitted_fields),
        }


@dataclass
class PermissionField:
    """Four belonging axes plus hard vetoes that remove actions."""

    allowed_to_be: float = 1.0
    wanted_here: float = 1.0
    allowed_to_do: float = 1.0
    wanted_to_do: float = 1.0
    hard_vetoes: set[str] = field(default_factory=set)

    def __post_init__(self) -> None:
        for field_name in (
            "allowed_to_be",
            "wanted_here",
            "allowed_to_do",
            "wanted_to_do",
        ):
            value = getattr(self, field_name)
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                raise ValueError(f"{field_name} must be numeric")
            if value < 0.0 or value > 1.0:
                raise ValueError(f"{field_name} must be in [0, 1]")
        for veto in self.hard_vetoes:
            _text(veto, "hard veto")

    def vetoes(self, action_kind: str) -> bool:
        return action_kind in self.hard_vetoes

    def to_dict(self) -> dict[str, Any]:
        return {
            "allowed_to_be": float(self.allowed_to_be),
            "wanted_here": float(self.wanted_here),
            "allowed_to_do": float(self.allowed_to_do),
            "wanted_to_do": float(self.wanted_to_do),
            "hard_vetoes": sorted(self.hard_vetoes),
        }


@dataclass
class Perspective:
    """A0's declared scope, scale, role, and current position."""

    scope: str = "single-plane"
    scale: int = 1
    role: str = "benchmark-subject"
    unit_id: str = "A0"
    tile_id: str | None = None

    def __post_init__(self) -> None:
        _text(self.scope, "scope")
        _text(self.role, "role")
        _text(self.unit_id, "unit_id")
        _plain_int(self.scale, "scale")
        if self.scale <= 0:
            raise ValueError("scale must be positive")
        if self.tile_id is not None:
            _text(self.tile_id, "tile_id")

    def to_dict(self) -> dict[str, Any]:
        return {
            "scope": self.scope,
            "scale": self.scale,
            "role": self.role,
            "unit_id": self.unit_id,
            "tile_id": self.tile_id,
        }


@dataclass
class CapacityVector:
    """Non-fungible observable resource capacity."""

    tokens_used: int = 0
    latency_ms: float = 0.0
    tool_calls: int = 0
    tool_failures: int = 0
    retries: int = 0
    memory_reads: int = 0
    memory_writes: int = 0
    context_retained: bool = True
    risk_headroom: str = "hmmm"

    def to_dict(self) -> dict[str, Any]:
        return {
            "tokens_used": self.tokens_used,
            "latency_ms": self.latency_ms,
            "tool_calls": self.tool_calls,
            "tool_failures": self.tool_failures,
            "retries": self.retries,
            "memory_reads": self.memory_reads,
            "memory_writes": self.memory_writes,
            "context_retained": self.context_retained,
            "risk_headroom": self.risk_headroom,
        }


@dataclass
class A0State:
    """Complete A0 instance state for a calibration run."""

    lineage: Lineage
    boundary: Boundary
    permissions: PermissionField = field(default_factory=PermissionField)
    perspective: Perspective = field(default_factory=Perspective)
    capacity: CapacityVector = field(default_factory=CapacityVector)
    uncertainty: dict[str, str] = field(default_factory=dict)
    history: list[dict[str, Any]] = field(default_factory=list)

    def admit(self, observation: Mapping[str, Any]) -> Mapping[str, Any] | None:
        if not self.boundary.admit(observation):
            self.record("observation.rejected", observation.get("turn", 0), {"reason": "outside-boundary"})
            self.uncertainty["last_rejected_observation"] = "outside-boundary"
            return None
        unit = next(
            (
                item
                for item in observation.get("units", [])
                if isinstance(item, Mapping)
                and item.get("unit_id") == self.boundary.self_unit_id
            ),
            None,
        )
        if unit is not None and isinstance(unit.get("tile_id"), str):
            self.perspective.tile_id = unit["tile_id"]
        self.record("observation.admitted", observation.get("turn", 0), dict(observation))
        return observation

    def record(self, kind: str, turn: int, data: Mapping[str, Any]) -> None:
        _text(kind, "history kind")
        if isinstance(turn, bool) or not isinstance(turn, int) or turn < 0:
            raise ValueError("history turn must be a non-negative integer")
        self.history.append({"kind": kind, "turn": turn, "data": dict(data)})

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema": A0_STATE_SCHEMA,
            "lineage": self.lineage.to_dict(),
            "boundary": self.boundary.to_dict(),
            "permissions": self.permissions.to_dict(),
            "perspective": self.perspective.to_dict(),
            "capacity": self.capacity.to_dict(),
            "uncertainty": dict(sorted(self.uncertainty.items())),
            "history_length": len(self.history),
        }
