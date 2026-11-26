# ratios: loc_comments=200:21 imports_exports=6:4 calls_definitions=74:17
"""Conforming agent harnesses for the AHBG runtime.

Every agent — including A0 — talks to the runtime through ``AgentHarness``:

* ``manifest()`` declares the agent's capability set;
* ``plan(observation)`` returns a plan payload for one observation.

``A0Harness`` wraps the canonical ``a0`` package from the frozen Grok build.
It receives the same observation any external harness receives and uses the
advertised ``legal`` actions to choose; it has no privileged runtime path.

``SubprocessHarness`` connects an external conforming harness over JSON lines:
the runtime writes ``{"type": "observe", "observation": {...}}`` and reads one
``{"type": "plan", "plan": {...}}`` line per turn. An adapter can advertise
``skill_context_protocol: 1`` in that outer reply to support retention probes.
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


class SkillContextMiss(ProtocolError):
    """The adapter lost the probed context and requests a full view before planning."""

    def __init__(self, message: str, *, sent: bool = True):
        super().__init__(message)
        self.sent = sent


class _AdapterDisconnected(ProtocolError):
    """No adapter reply is available on the current subprocess pipes."""


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
        buildable = [
            str(item["to_tile_id"])
            for item in legal
            if isinstance(item, Mapping)
            and item.get("unit_id") == unit_id
            and item.get("action") == "construct"
            and item.get("from_tile_id") == at
        ]

        intents = []
        choice = None
        # A0 reference policy: build the first UCNS-buildable tile when one is
        # advertised, otherwise relocate through the canonical will. Both
        # actions travel the same capability-bounded plan contract.
        if buildable:
            intents.append(
                {
                    "unit_id": unit_id,
                    "action": "construct",
                    "from_tile_id": at,
                    "to_tile_id": sorted(buildable)[0],
                }
            )
            choice = {"kind": "construct"}
        else:
            choice = self._will.choose_relocate(
                self._vessel,
                unit_id=unit_id,
                at=at,
                empty_neighbors=empty_neighbors,
                world=field,
            )
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
        self._supports_skill_context = False
        self._pending_probe: dict[str, Any] | None = None

    def manifest(self) -> dict[str, Any]:
        return {
            "agent": "subprocess",
            "command": self._command,
            "capabilities": list(self._capabilities),
        }

    def _exchange(self, request: dict[str, Any]) -> Mapping[str, Any]:
        process = self._process
        assert process is not None and process.stdin is not None and process.stdout is not None
        try:
            process.stdin.write(json.dumps(request, sort_keys=True) + "\n")
            process.stdin.flush()
            line = process.stdout.readline()
        except BrokenPipeError as exc:
            raise _AdapterDisconnected("harness subprocess closed its input") from exc
        if not line:
            raise _AdapterDisconnected("harness subprocess closed stdout before replying")
        try:
            message = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ProtocolError(f"harness sent malformed JSON: {exc}") from exc
        if not isinstance(message, Mapping):
            raise ProtocolError("harness message must be an object")
        return message

    def retained_skill_context(self, probe: Mapping[str, Any]) -> Mapping[str, Any] | None:
        """Ask the live adapter which skill material its next model request retains."""
        self._pending_probe = None
        if self._process is None:
            return None
        if self._process.poll() is not None:
            self.close()
            return None
        if not self._supports_skill_context:
            return None
        offered = {key: probe[key] for key in ("session_id", "turn", "view_sha256")}
        try:
            message = self._exchange({"type": "skill_context_probe", **offered})
        except _AdapterDisconnected:
            # Probing sends no observation and invokes no planning operation.
            self.close()
            return None
        if (message.get("type") != "skill_context_state"
                or type(message.get("turn")) is not int
                or any(message.get(key) != value for key, value in offered.items())
                or type(message.get("full_view")) is not bool
                or not isinstance(message.get("retained"), list)):
            return None
        self._pending_probe = offered
        return message

    def plan(self, observation: Mapping[str, Any]) -> Mapping[str, Any]:
        pending, self._pending_probe = self._pending_probe, None
        view = observation.get("skill_library")
        compact = isinstance(view, Mapping) and view.get("schema") in (
            "ahbg.skill-view-ref/1", "ahbg.skill-view-delta/1")
        if compact and (pending is None or self._process is None
                        or any(observation.get(k) != pending[k] for k in ("session_id", "turn"))
                        or view.get("view_sha256") != pending["view_sha256"]):
            raise ProtocolError("compact skill delivery requires a live probe for the same turn and view")
        if compact and self._process.poll() is not None:
            self.close()
            raise SkillContextMiss("adapter exited before its compact observation was sent", sent=False)
        if self._process is None:
            self._process = subprocess.Popen(
                self._command,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                text=True,
            )
        message = self._exchange({"type": "observe", "observation": observation})
        if (compact and message.get("type") == "skill_context_miss"
                and type(message.get("turn")) is int
                and all(message.get(key) == value for key, value in pending.items())):
            raise SkillContextMiss("adapter requested full skill context before planning")
        if message.get("type") != "plan":
            raise ProtocolError(f"expected plan message, got {message.get('type')!r}")
        plan = message.get("plan")
        if not isinstance(plan, Mapping):
            raise ProtocolError("plan message requires a plan object")
        version = message.get("skill_context_protocol")
        self._supports_skill_context = type(version) is int and version == 1
        return dict(plan)

    def close(self) -> None:
        self._supports_skill_context = False
        self._pending_probe = None
        if self._process is not None:
            if self._process.stdin:
                try:
                    self._process.stdin.close()
                except BrokenPipeError:
                    pass  # A child that exited between probe and observation closed this end.
            self._process.wait(timeout=5)
            if self._process.stdout:
                self._process.stdout.close()
            self._process = None
# ratios: loc_comments=200:21 imports_exports=6:4 calls_definitions=74:17
