"""A0 vessel: one lineage bound to one permission field and history.

X_lambda is carried as named parts, not collapsed to a scalar. Occupancy on
the four belonging axes is continuous in [0, 1]; the questions stay absolute.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from typing import Any


def _new_id(salt: str) -> str:
    return hashlib.sha256(f"grok-a0:{salt}".encode("utf-8")).hexdigest()[:16]


@dataclass
class Belonging:
    allowed_to_be: float = 1.0
    wanted_here: float = 1.0
    allowed_to_do: float = 1.0
    wanted_to_do: float = 1.0

    def as_dict(self) -> dict[str, float]:
        return {
            "allowed_to_be": self.allowed_to_be,
            "wanted_here": self.wanted_here,
            "allowed_to_do": self.allowed_to_do,
            "wanted_to_do": self.wanted_to_do,
        }


@dataclass
class Vessel:
    lineage: str
    parent: str | None
    root: str
    role: str
    scope: str
    scale: str
    belonging: Belonging = field(default_factory=Belonging)
    belief: dict[str, Any] = field(default_factory=dict)
    history: list[dict[str, Any]] = field(default_factory=list)
    provider: str = "grok-4.6"
    capacity: dict[str, float] = field(
        default_factory=lambda: {
            "tokens": 1.0,
            "time": 1.0,
            "context": 1.0,
            "tools": 1.0,
            "retries": 1.0,
            "memory": 1.0,
            "risk": 1.0,
        }
    )

    @classmethod
    def instantiate(cls, *, salt: str, role: str = "mover", scope: str = "local-seven", scale: str = "tile") -> "Vessel":
        ident = _new_id(salt)
        return cls(lineage=ident, parent=None, root=ident, role=role, scope=scope, scale=scale)

    def fork(self, salt: str) -> "Vessel":
        child_id = _new_id(salt)
        child = Vessel(
            lineage=child_id,
            parent=self.lineage,
            root=self.root,
            role=self.role,
            scope=self.scope,
            scale=self.scale,
            belonging=Belonging(**self.belonging.as_dict()),
            belief=dict(self.belief),
            history=list(self.history),
            provider=self.provider,
            capacity=dict(self.capacity),
        )
        self.history.append({"kind": "lineage.fork", "child": child_id})
        child.history.append({"kind": "lineage.born", "parent": self.lineage})
        return child

    def remember(self, event: dict[str, Any]) -> None:
        self.history.append(dict(event))

    def identity(self) -> dict[str, Any]:
        return {
            "instance_id": self.lineage,
            "parent_id": self.parent,
            "root_id": self.root,
            "role": self.role,
            "scope": self.scope,
            "scale": self.scale,
            "provider_relation": self.provider,
            "belonging": self.belonging.as_dict(),
            "capacity": dict(self.capacity),
        }
