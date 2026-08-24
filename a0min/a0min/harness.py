# ratios: loc_comments=297:24 imports_exports=10:4 calls_definitions=53:21
"""Minimal agent harness over the imported a0 platonic superpotential.

The harness holds one open PlatonicAgent (the superpotential) and creates
potential sub-agents by projecting its declared semantic regions, enforcing the
same depth / fanout / concurrent-live recursion caps a0's sub_agent_spawn uses.

Provenance:
- PlatonicAgent, AgentSemanticRegion, AgentProjection imported verbatim from
  The-Interdependency/a0 @ f9470a74138da89a2d075ecf6c3241aac63923f1
  (python/agents/platonic.py, platonic_regions.py, zfae.py).
- Cap semantics mirror The-Interdependency/a0
  python/services/spawn_caps.py (tier fallbacks plus env overrides).

The harness is intentionally in-memory and stdlib-only: it creates and tracks
sub-agent records; it does not execute inference, persistence, or networking.
"""

from __future__ import annotations

import json
import os
import uuid
from dataclasses import dataclass, replace
from pathlib import Path
from types import MappingProxyType
from typing import Any, Mapping

from .platonic import PlatonicAgent, candidate_platonic_agent
from .platonic.zfae import sub_agent_name

SUPPORTED_ORCHESTRATION_MODES = (
    "single",
    "fan_out",
    "council",
    "daisy_chain",
    "room_synthesized",
    "room_all",
)
SUPPORTED_CUT_MODES = ("off", "soft", "hard")

_TIER_DEPTH = {"free": 2, "seeker": 3, "operator": 4, "patron": 5, "admin": 5}
_TIER_CONCURRENT_LIVE = {
    "free": 2,
    "seeker": 4,
    "operator": 8,
    "patron": 12,
    "admin": 20,
}
_DEFAULT_DEPTH = int(os.environ.get("A0MIN_MAX_SPAWN_DEPTH", "3"))
_DEFAULT_FANOUT = int(os.environ.get("A0MIN_MAX_SPAWN_FANOUT", "5"))
_DEFAULT_CONCURRENT_LIVE = int(
    os.environ.get("A0MIN_MAX_SPAWN_CONCURRENT_LIVE", "10")
)


class SpawnCapExceeded(RuntimeError):
    """Raised when creating a sub-agent would exceed a recursion cap."""

    def __init__(self, cap: str, current: int, limit: int) -> None:
        self.cap = cap
        self.current = current
        self.limit = limit
        super().__init__(f"spawn cap exceeded: {cap}={current} > limit={limit}")


@dataclass(frozen=True, slots=True)
class PotentialSubAgent:
    """One potential sub-agent option exposed by the superpotential."""

    region: str
    description: str
    dimensions: tuple[str, ...]
    surfaces: tuple[str, ...]
    status: str
    orchestration_modes: tuple[str, ...] = SUPPORTED_ORCHESTRATION_MODES
    cut_modes: tuple[str, ...] = SUPPORTED_CUT_MODES

    def as_dict(self) -> dict[str, Any]:
        return {
            "region": self.region,
            "description": self.description,
            "dimensions": list(self.dimensions),
            "surfaces": list(self.surfaces),
            "status": self.status,
            "orchestration_modes": list(self.orchestration_modes),
            "cut_modes": list(self.cut_modes),
        }


@dataclass(frozen=True, slots=True)
class SubAgent:
    """A created sub-agent: one bounded projection of a superpotential region."""

    sub_agent_id: str
    name: str
    run_id: str
    parent_run_id: str | None
    root_run_id: str
    depth: int
    region: str
    selected: tuple[str, ...]
    omitted: tuple[str, ...]
    unresolved: tuple[str, ...]
    bindings: Mapping[str, Any]
    orchestration_mode: str
    cut_mode: str
    providers: tuple[str, ...]
    task: str
    status: str = "spawned"

    def __post_init__(self) -> None:
        object.__setattr__(self, "bindings", MappingProxyType(dict(self.bindings)))

    def as_dict(self) -> dict[str, Any]:
        return {
            "sub_agent_id": self.sub_agent_id,
            "name": self.name,
            "run_id": self.run_id,
            "parent_run_id": self.parent_run_id,
            "root_run_id": self.root_run_id,
            "depth": self.depth,
            "region": self.region,
            "selected": list(self.selected),
            "omitted": list(self.omitted),
            "unresolved": list(self.unresolved),
            "bindings": dict(self.bindings),
            "orchestration_mode": self.orchestration_mode,
            "cut_mode": self.cut_mode,
            "providers": list(self.providers),
            "task": self.task,
            "status": self.status,
        }


class Harness:
    """Minimal creator of potential sub-agents from a PlatonicAgent."""

    def __init__(
        self,
        agent: PlatonicAgent | None = None,
        *,
        tier: str = "free",
        max_depth: int | None = None,
        max_fanout: int | None = None,
        max_concurrent_live: int | None = None,
    ) -> None:
        self.superpotential = (
            agent if agent is not None else candidate_platonic_agent()
        )
        self.tier = tier
        self.max_depth = (
            max_depth if max_depth is not None else _TIER_DEPTH.get(tier, _DEFAULT_DEPTH)
        )
        self.max_fanout = (
            max_fanout if max_fanout is not None else _DEFAULT_FANOUT
        )
        self.max_concurrent_live = (
            max_concurrent_live
            if max_concurrent_live is not None
            else _TIER_CONCURRENT_LIVE.get(tier, _DEFAULT_CONCURRENT_LIVE)
        )
        self._sub_agents: dict[str, SubAgent] = {}
        self._order: list[str] = []
        self._index = 0

    @property
    def caps(self) -> dict[str, int]:
        return {
            "tier": self.tier,
            "max_depth": self.max_depth,
            "max_fanout": self.max_fanout,
            "max_concurrent_live": self.max_concurrent_live,
        }

    def potential_sub_agents(self) -> tuple[PotentialSubAgent, ...]:
        """Every declared region of the superpotential is one option."""
        return tuple(
            PotentialSubAgent(
                region=region.name,
                description=region.description,
                dimensions=region.dimensions,
                surfaces=region.surfaces,
                status=region.status,
            )
            for region in self.superpotential.regions
        )

    def region_option(self, name: str) -> PotentialSubAgent:
        for option in self.potential_sub_agents():
            if option.region == name:
                return option
        raise ValueError(f"unknown region: {name}")

    def get(self, sub_agent_id: str) -> SubAgent:
        try:
            return self._sub_agents[sub_agent_id]
        except KeyError:
            raise KeyError(f"unknown sub_agent_id: {sub_agent_id}") from None

    def list_sub_agents(self, status: str | None = None) -> tuple[SubAgent, ...]:
        agents = tuple(
            self._sub_agents[sub_agent_id] for sub_agent_id in self._order
        )
        if status is None:
            return agents
        return tuple(agent for agent in agents if agent.status == status)

    def children_of(self, parent_run_id: str | None) -> tuple[SubAgent, ...]:
        return tuple(
            agent
            for agent in self.list_sub_agents()
            if agent.parent_run_id == parent_run_id
        )

    def live_count(self, parent_run_id: str | None) -> int:
        return sum(
            1
            for agent in self.children_of(parent_run_id)
            if agent.status == "spawned"
        )

    def create(
        self,
        region: str,
        bindings: Mapping[str, Any] | None = None,
        *,
        task: str = "",
        orchestration_mode: str = "single",
        cut_mode: str = "soft",
        providers: list[str] | tuple[str, ...] | None = None,
        parent: SubAgent | None = None,
    ) -> SubAgent:
        """Create any potential sub-agent by projecting a declared region.

        Unknown regions fail closed; cap violations raise SpawnCapExceeded.
        """
        if orchestration_mode not in SUPPORTED_ORCHESTRATION_MODES:
            raise ValueError(
                f"unsupported orchestration_mode: {orchestration_mode}"
            )
        if cut_mode not in SUPPORTED_CUT_MODES:
            raise ValueError(f"unsupported cut_mode: {cut_mode}")
        try:
            semantic_region = self.superpotential.region(region)
        except KeyError:
            known = ", ".join(self.superpotential.region_names)
            raise ValueError(
                f"unknown region: {region}; known regions: {known}"
            ) from None

        projection = self.superpotential.project_region(region, dict(bindings or {}))
        parent_run_id = parent.run_id if parent is not None else None
        new_depth = (parent.depth if parent is not None else 0) + 1

        if new_depth > self.max_depth:
            raise SpawnCapExceeded("depth", new_depth, self.max_depth)
        siblings = len(self.children_of(parent_run_id))
        if siblings + 1 > self.max_fanout:
            raise SpawnCapExceeded("fanout", siblings + 1, self.max_fanout)
        live = self.live_count(parent_run_id)
        if live + 1 > self.max_concurrent_live:
            raise SpawnCapExceeded("concurrent_live", live + 1, self.max_concurrent_live)

        run_id = str(uuid.uuid4())
        sub_agent_id = f"a0z-{run_id[:8]}"
        root_run_id = parent.root_run_id if parent is not None else run_id
        provider = providers[0] if providers else None
        name = sub_agent_name(self._index, provider=provider, name=region)
        self._index += 1

        sub_agent = SubAgent(
            sub_agent_id=sub_agent_id,
            name=name,
            run_id=run_id,
            parent_run_id=parent_run_id,
            root_run_id=root_run_id,
            depth=new_depth,
            region=semantic_region.name,
            selected=projection.selected,
            omitted=projection.omitted,
            unresolved=projection.unresolved,
            bindings=projection.bindings,
            orchestration_mode=orchestration_mode,
            cut_mode=cut_mode,
            providers=tuple(providers or ()),
            task=task,
        )
        self._sub_agents[sub_agent_id] = sub_agent
        self._order.append(sub_agent_id)
        return sub_agent

    def merge(self, sub_agent_id: str) -> SubAgent:
        """Mark a spawned sub-agent merged, releasing its concurrent-live slot."""
        current = self.get(sub_agent_id)
        if current.status != "spawned":
            return current
        merged = replace(current, status="merged")
        self._sub_agents[sub_agent_id] = merged
        return merged

    def superpotential_dict(self) -> dict[str, Any]:
        return {
            "agent_id": self.superpotential.agent_id,
            "dimensions": [
                {
                    "name": dimension.name,
                    "description": dimension.description,
                    "status": dimension.status,
                    "hmmm": list(dimension.hmmm),
                }
                for dimension in self.superpotential.dimensions
            ],
            "regions": [
                option.as_dict() for option in self.potential_sub_agents()
            ],
            "hmmm": list(self.superpotential.hmmm),
        }

    def save(self, path: str | os.PathLike[str]) -> None:
        """Persist created sub-agents as JSON so CLI invocations can share state."""
        payload = {
            "tier": self.tier,
            "index": self._index,
            "sub_agents": [self._sub_agents[i].as_dict() for i in self._order],
        }
        Path(path).write_text(json.dumps(payload, indent=2), encoding="utf-8")

    @classmethod
    def load(
        cls,
        path: str | os.PathLike[str],
        *,
        agent: PlatonicAgent | None = None,
        tier: str | None = None,
    ) -> "Harness":
        """Rebuild a harness from a state file written by save()."""
        payload = json.loads(Path(path).read_text(encoding="utf-8"))
        harness = cls(agent=agent, tier=tier or payload.get("tier", "free"))
        harness._index = int(payload.get("index", 0))
        for record in payload.get("sub_agents", []):
            sub_agent = SubAgent(
                sub_agent_id=record["sub_agent_id"],
                name=record["name"],
                run_id=record["run_id"],
                parent_run_id=record["parent_run_id"],
                root_run_id=record["root_run_id"],
                depth=record["depth"],
                region=record["region"],
                selected=tuple(record["selected"]),
                omitted=tuple(record["omitted"]),
                unresolved=tuple(record["unresolved"]),
                bindings=dict(record["bindings"]),
                orchestration_mode=record["orchestration_mode"],
                cut_mode=record["cut_mode"],
                providers=tuple(record["providers"]),
                task=record["task"],
                status=record["status"],
            )
            harness._sub_agents[sub_agent.sub_agent_id] = sub_agent
            harness._order.append(sub_agent.sub_agent_id)
        return harness
# ratios: loc_comments=297:24 imports_exports=10:4 calls_definitions=53:21
