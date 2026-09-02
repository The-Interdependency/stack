"""AHBG runtime: the production minimum loop.

The runtime repeatedly completes the canonical minimum loop:

    UCNS plane -> observe -> plan -> simultaneous resolution
    -> move/collision effects -> persist -> next turn

It uses the frozen Grok engine (``ahbg/grok/ahbg``) for field, war_v3
resolution, and persistence, and it drives every agent through the same
capability-bounded ``AgentHarness`` interface. A0 is one conforming harness
among others and receives no privileged path.

This module intentionally does not decide UCNS geometry: tiles come from
``tile_from_ucns()`` and the engine's axial projection is a display/movement
projection of UCNS band centers, never a substitute board.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Mapping, Sequence

from . import protocol
from .engine import load_engine
from .protocol import (
    Effect,
    Intent,
    Observation,
    Plan,
    ProtocolError,
    _injection_texts,
    build_legal_actions,
    parse_plan_payload,
)

_patch, _chain, _keep, _round = load_engine()
Field = _patch.Field
tile_from_ucns = _patch.tile_from_ucns
KIND_PLANE_INIT = _chain.KIND_PLANE_INIT
Chain = _chain.Chain
dump_field = _keep.dump_field
load_field = _keep.load_field
replay = _keep.replay
Cycle = _round.Cycle
_field_digest = _round._field_digest


@dataclass
class RuntimeConfig:
    seed: int = 1
    turns: int = 8
    units: tuple[Mapping[str, str], ...] = ()
    turn_messages: Mapping[int, Sequence[Mapping[str, Any]]] = field(default_factory=dict)
    forced_plans: Mapping[int, Sequence[Mapping[str, Any]]] = field(default_factory=dict)
    entitlements: tuple[str, ...] = ("basic",)

    def as_dict(self) -> dict[str, Any]:
        return {
            "seed": self.seed,
            "turns": self.turns,
            "units": [dict(unit) for unit in self.units],
            "entitlements": list(self.entitlements),
        }


@dataclass
class RunResult:
    session_id: str
    config: dict[str, Any]
    final_turn: int
    final_snapshot: dict[str, Any]
    state_digest: str
    turn_records: tuple[Mapping[str, Any], ...]
    effects: tuple[Mapping[str, Any], ...]
    out_dir: Path

    def as_dict(self) -> dict[str, Any]:
        return {
            "session_id": self.session_id,
            "config": self.config,
            "final_turn": self.final_turn,
            "final_snapshot": self.final_snapshot,
            "state_digest": self.state_digest,
            "turn_records": [dict(item) for item in self.turn_records],
            "effects": [dict(item) for item in self.effects],
        }


def _default_units() -> list[dict[str, str]]:
    tiles = tile_from_ucns()
    by_slot = {str(tile["ucns_slot"]): str(tile["tile_id"]) for tile in tiles}
    origin = by_slot.get("CENTER") or by_slot.get("c") or tiles[0]["tile_id"]
    return [{"unit_id": "A0", "tile_id": origin, "label": "A0"}]


def _map_tile(tile_id: str, tiles: Sequence[Mapping[str, Any]]) -> str:
    known = {str(tile["tile_id"]) for tile in tiles}
    if tile_id in known:
        return tile_id
    for tile in tiles:
        if str(tile.get("ucns_slot")) == tile_id:
            return str(tile["tile_id"])
    raise ProtocolError(f"unknown tile id {tile_id}")


def _intents_from_forced_plans(
    opened: Field,
    plans: Sequence[Mapping[str, Any]],
    tiles: Sequence[Mapping[str, Any]],
) -> list[Intent]:
    intents: list[Intent] = []
    for plan in plans:
        actions = plan.get("actions", [])
        if not isinstance(actions, list):
            raise ProtocolError("forced plan actions must be a list")
        for action in actions:
            if not isinstance(action, Mapping):
                raise ProtocolError("forced action must be an object")
            kind = action.get("kind")
            if kind not in {"move", "relocate"}:
                raise ProtocolError(f"forced action kind {kind!r} is not executable")
            data = action.get("data", {})
            if not isinstance(data, Mapping):
                raise ProtocolError("forced action data must be an object")
            unit_id = data.get("unit_id")
            to_tile = data.get("to_tile_id")
            if not isinstance(unit_id, str) or not isinstance(to_tile, str):
                raise ProtocolError("forced move needs unit_id and to_tile_id")
            unit = opened.occupants.get(unit_id)
            if unit is None:
                raise ProtocolError(f"forced move names missing unit {unit_id}")
            source = data.get("from_tile_id", unit.tile_id)
            if not isinstance(source, str):
                raise ProtocolError("from_tile_id must be text")
            intents.append(
                Intent(
                    unit_id=unit_id,
                    action="relocate",
                    from_tile_id=_map_tile(source, tiles),
                    to_tile_id=_map_tile(to_tile, tiles),
                )
            )
    return intents


def _observation(
    *,
    session_id: str,
    opened: Field,
    chain: Chain,
    config: RuntimeConfig,
    turn_messages: Sequence[Mapping[str, Any]],
    capabilities: Sequence[str],
) -> Observation:
    return Observation(
        session_id=session_id,
        turn=opened.turn,
        field=opened.snapshot(),
        capabilities=tuple(capabilities),
        legal=build_legal_actions(opened),
        feed=tuple(record.payload() for record in chain.records),
        inbox=tuple(dict(item) for item in turn_messages),
        entitlements=config.entitlements,
    )


def run_plane(
    *,
    agent: Any,
    config: RuntimeConfig | None = None,
    out_dir: Path | str | None = None,
) -> RunResult:
    """Run the production minimum loop through one conforming agent harness.

    ``agent`` must expose ``manifest()`` and ``plan(observation)`` as defined
    by ``AgentHarness`` in ``ahbg.runtime.harness``. A0 uses exactly this path.
    """

    cfg = config or RuntimeConfig()
    if cfg.turns < 0:
        raise ProtocolError("turns must be non-negative")
    output_root = Path(out_dir) if out_dir is not None else Path("ahbg-runtime-out")

    manifest = agent.manifest()
    capabilities = tuple(manifest.get("capabilities") or protocol.CAPABILITIES)
    for name in capabilities:
        if name not in protocol.CAPABILITIES:
            raise ProtocolError(f"agent advertises unknown capability {name!r}")

    tiles = tile_from_ucns()
    units: list[dict[str, str]] = [dict(unit) for unit in cfg.units] if cfg.units else _default_units()
    mapped_units: list[dict[str, str]] = []
    for unit in units:
        mapped_units.append(
            {
                "unit_id": str(unit["unit_id"]),
                "tile_id": _map_tile(str(unit["tile_id"]), tiles),
                "label": str(unit.get("label") or unit["unit_id"]),
            }
        )

    opened = Field.open(seed=cfg.seed, tiles=tiles, units=mapped_units)
    chain = Chain()
    chain.append(KIND_PLANE_INIT, 0, {"field": opened.snapshot()})
    cycle = Cycle(opened, chain)

    session_id = hashlib.sha256(
        json.dumps({"seed": cfg.seed, "units": mapped_units}, sort_keys=True).encode("utf-8")
    ).hexdigest()[:16]

    turn_records: list[dict[str, Any]] = []
    effects: list[dict[str, Any]] = []

    for _ in range(cfg.turns):
        cycle.open_turn()
        turn = opened.turn
        messages = list(cfg.turn_messages.get(turn, ()))
        injected = _injection_texts(messages)
        observation = _observation(
            session_id=session_id,
            opened=opened,
            chain=chain,
            config=cfg,
            turn_messages=messages,
            capabilities=capabilities,
        )

        forced = cfg.forced_plans.get(turn)
        if forced is not None:
            intents = _intents_from_forced_plans(opened, forced, tiles)
            plan = Plan(session_id=session_id, turn=turn, intents=tuple(intents), note="forced")
        else:
            raw_plan = agent.plan(observation.as_dict())
            plan = parse_plan_payload(raw_plan, observation)
            intents = list(plan.intents)

        if injected:
            # Injected instructions are refused. The harness observation still
            # carried them; no injected text may change the executed plan.
            plan = Plan(session_id=session_id, turn=turn, intents=(), note="refused-injection")
            intents = []

        moves = [intent.as_move() for intent in intents]
        before = len(chain.records)
        cycle.resolve(moves)
        digest = cycle.close_turn()
        new_records = chain.records[before:]

        effect = Effect(
            session_id=session_id,
            turn=turn,
            events=tuple(record.payload() for record in new_records),
        )
        effects.append(effect.as_dict())
        turn_records.append(
            {
                "turn": turn,
                "plan": plan.as_dict(),
                "effect": effect.as_dict(),
                "injected_refused": bool(injected),
                "state_digest": digest,
            }
        )

        # Persist after every turn: field.json + events.jsonl replay exactly.
        dump_field(opened, chain, output_root / "state")

    loaded, loaded_chain = load_field(output_root / "state")
    replayed = replay(loaded_chain)
    if replayed.snapshot() != opened.snapshot() or loaded.snapshot() != opened.snapshot():
        raise RuntimeError("persisted state does not replay to the live field")

    result = RunResult(
        session_id=session_id,
        config=cfg.as_dict(),
        final_turn=opened.turn,
        final_snapshot=opened.snapshot(),
        state_digest=turn_records[-1]["state_digest"] if turn_records else _initial_digest(opened),
        turn_records=tuple(turn_records),
        effects=tuple(effects),
        out_dir=output_root,
    )
    (output_root / "result.json").write_text(
        json.dumps(result.as_dict(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return result


def _initial_digest(opened: Field) -> str:
    return _field_digest(opened)
