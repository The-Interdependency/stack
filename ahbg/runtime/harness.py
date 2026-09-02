"""Conforming agent harnesses for the AHBG runtime.

Every agent — including A0 — talks to the runtime through ``AgentHarness``:

* ``manifest()`` declares the agent's capability set;
* ``plan(observation)`` returns a plan payload for one observation.

``A0Harness`` wraps the canonical ``a0`` package from the frozen Grok build.
It receives the same observation any external harness receives and uses the
advertised ``legal`` actions to choose; it has no privileged runtime path.

``SubprocessHarness`` connects an external conforming harness over JSON lines:
the runtime writes ``{"type": "observe", "observation": {...}}`` and reads one
``{"type": "plan", "plan": {...}}`` line per turn. That external harness can be
any language and does not modify AHBG.
"""

from __future__ import annotations

import json
import subprocess
from typing import Any, Mapping, Protocol, Sequence

from .engine import load_a0
from .protocol import CAPABILITIES, ProtocolError


class AgentHarness(Protocol):
    def manifest(self) -> Mapping[str, Any]: ...

    def plan(self, observation: Mapping[str, Any]) -> Mapping[str, Any]: ...


class A0Harness:
    """A0 as a conforming harness over the canonical ``a0`` package."""

    def __init__(self, *, salt: str = "ahbg-runtime-a0", role: str = "mover") -> None:
        self._selfhood, self._will = load_a0()
        self._vessel = self._selfhood.Vessel.instantiate(salt=salt, role=role)

    def manifest(self) -> dict[str, Any]:
        return {
            "agent": "a0",
            "capabilities": list(CAPABILITIES),
            "provider": self._vessel.provider,
            "scope": self._vessel.scope,
            "scale": self._vessel.scale,
        }

    def plan(self, observation: Mapping[str, Any]) -> dict[str, Any]:
        session_id = observation.get("session_id")
        turn = observation.get("turn")
        field = observation.get("field") or {}
        units = field.get("units") or []
        if not isinstance(units, list) or not units:
            return {
                "schema": "interdependency.ahbg.harness.plan/1",
                "session_id": session_id,
                "turn": turn,
                "intents": [],
                "note": "no-units-to-drive",
            }

        unit = units[0]
        unit_id = unit.get("unit_id")
        at = unit.get("tile_id")
        legal = observation.get("legal") or []
        empty_neighbors = [
            str(item["to_tile_id"])
            for item in legal
            if isinstance(item, Mapping)
            and item.get("unit_id") == unit_id
            and item.get("action") == "relocate"
            and item.get("from_tile_id") == at
        ]

        choice = self._will.choose_relocate(
            self._vessel,
            unit_id=unit_id,
            at=at,
            empty_neighbors=empty_neighbors,
            world=field,
        )
        intents = []
        if choice.get("kind") == "relocate":
            intents.append(
                {
                    "unit_id": choice["unit_id"],
                    "action": "relocate",
                    "from_tile_id": choice["from_tile_id"],
                    "to_tile_id": choice["to_tile_id"],
                }
            )
        return {
            "schema": "interdependency.ahbg.harness.plan/1",
            "session_id": session_id,
            "turn": turn,
            "intents": intents,
            "note": f"a0:{choice.get('kind')}:{choice.get('reason', '')}",
            "shadow": self._will.shadow_cost(self._vessel),
        }


class SubprocessHarness:
    """External conforming harness over JSON-lines stdin/stdout."""

    def __init__(self, command: Sequence[str], *, capabilities: Sequence[str] = CAPABILITIES) -> None:
        if not command:
            raise ProtocolError("subprocess harness needs a command")
        self._command = list(command)
        self._capabilities = tuple(capabilities)
        for name in self._capabilities:
            if name not in CAPABILITIES:
                raise ProtocolError(f"unknown capability {name!r}")
        self._process: subprocess.Popen[str] | None = None

    def manifest(self) -> dict[str, Any]:
        return {
            "agent": "subprocess",
            "command": self._command,
            "capabilities": list(self._capabilities),
        }

    def plan(self, observation: Mapping[str, Any]) -> Mapping[str, Any]:
        if self._process is None:
            self._process = subprocess.Popen(
                self._command,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                text=True,
            )
        assert self._process.stdin is not None and self._process.stdout is not None
        self._process.stdin.write(
            json.dumps({"type": "observe", "observation": observation}, sort_keys=True) + "\n"
        )
        self._process.stdin.flush()
        line = self._process.stdout.readline()
        if not line:
            raise ProtocolError("harness subprocess closed stdout before planning")
        try:
            message = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ProtocolError(f"harness sent malformed JSON: {exc}") from exc
        if not isinstance(message, Mapping):
            raise ProtocolError("harness message must be an object")
        if message.get("type") != "plan":
            raise ProtocolError(f"expected plan message, got {message.get('type')!r}")
        plan = message.get("plan")
        if not isinstance(plan, Mapping):
            raise ProtocolError("plan message requires a plan object")
        return dict(plan)

    def close(self) -> None:
        if self._process is not None:
            if self._process.stdin:
                self._process.stdin.close()
            self._process.wait(timeout=5)
            self._process = None
