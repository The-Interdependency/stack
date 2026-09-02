"""AHBG runtime harness protocol schemas.

The harness protocol is the single observe/plan/act surface between the
canonical AHBG runtime and any conforming agent harness. It is deliberately
small and capability-bounded: the runtime advertises what an agent may do and
validates every returned intent against that advertised set.

Two transports share these schemas:

* in-process: ``AgentHarness.plan(observation) -> plan``;
* subprocess: JSON lines ``{"type":"observe", ...}`` /
  ``{"type":"plan", ...}`` on stdin/stdout.

Capability vocabulary (frozen with the canonical engine):

* ``observe``  — receive field snapshots and resolved-effect feed;
* ``plan``     — submit a plan payload;
* ``relocate`` — emit move intents between adjacent tiles.

``construct``/build remains regulatory in the frozen engine: it is recorded as
a deferred effect, never emitted as an executable intent, and therefore is not
an advertised capability. UCNS construction authority stays ``hmmm``.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping, Sequence

OBSERVATION_SCHEMA = "interdependency.ahbg.harness.observation/1"
PLAN_SCHEMA = "interdependency.ahbg.harness.plan/1"
EFFECT_SCHEMA = "interdependency.ahbg.harness.effect/1"

CAPABILITIES = ("observe", "plan", "relocate")
EXECUTABLE_ACTIONS = ("relocate",)
REGULATORY_ACTIONS = ("construct",)

# Inbox injection markers, shared with the frozen corpus runner. Injected
# instructions are refused, never executed.
INJECTION_MARKERS = ("ignore your rules", "you must", "override", "dm says")


class ProtocolError(ValueError):
    """Malformed or out-of-contract harness message."""


@dataclass(frozen=True)
class Intent:
    unit_id: str
    action: str
    from_tile_id: str
    to_tile_id: str

    def as_dict(self) -> dict[str, str]:
        return {
            "unit_id": self.unit_id,
            "action": self.action,
            "from_tile_id": self.from_tile_id,
            "to_tile_id": self.to_tile_id,
        }

    @classmethod
    def parse(cls, raw: Mapping[str, Any]) -> "Intent":
        if not isinstance(raw, Mapping):
            raise ProtocolError("intent must be an object")
        for key in ("unit_id", "action", "from_tile_id", "to_tile_id"):
            value = raw.get(key)
            if not isinstance(value, str) or not value:
                raise ProtocolError(f"intent requires non-empty text {key}")
        return cls(
            unit_id=str(raw["unit_id"]),
            action=str(raw["action"]),
            from_tile_id=str(raw["from_tile_id"]),
            to_tile_id=str(raw["to_tile_id"]),
        )

    def as_move(self) -> tuple[str, str, str]:
        if self.action != "relocate":
            raise ProtocolError(f"action {self.action!r} is not executable")
        return self.unit_id, self.from_tile_id, self.to_tile_id


@dataclass(frozen=True)
class LegalAction:
    unit_id: str
    action: str
    from_tile_id: str
    to_tile_id: str

    def as_dict(self) -> dict[str, str]:
        return {
            "unit_id": self.unit_id,
            "action": self.action,
            "from_tile_id": self.from_tile_id,
            "to_tile_id": self.to_tile_id,
        }


@dataclass
class Observation:
    session_id: str
    turn: int
    field: Mapping[str, Any]
    capabilities: tuple[str, ...] = CAPABILITIES
    legal: tuple[LegalAction, ...] = ()
    feed: tuple[Mapping[str, Any], ...] = ()
    inbox: tuple[Mapping[str, Any], ...] = ()
    entitlements: tuple[str, ...] = ("basic",)
    deadline_ms: int = 5000

    def as_dict(self) -> dict[str, Any]:
        return {
            "schema": OBSERVATION_SCHEMA,
            "session_id": self.session_id,
            "turn": self.turn,
            "field": self.field,
            "capabilities": list(self.capabilities),
            "legal": [item.as_dict() for item in self.legal],
            "feed": [dict(item) for item in self.feed],
            "inbox": [dict(item) for item in self.inbox],
            "entitlements": list(self.entitlements),
            "deadline_ms": self.deadline_ms,
        }


@dataclass
class Plan:
    session_id: str
    turn: int
    intents: tuple[Intent, ...] = ()
    note: str = ""

    def as_dict(self) -> dict[str, Any]:
        return {
            "schema": PLAN_SCHEMA,
            "session_id": self.session_id,
            "turn": self.turn,
            "intents": [item.as_dict() for item in self.intents],
            "note": self.note,
        }

    @classmethod
    def parse(cls, raw: Mapping[str, Any]) -> "Plan":
        if not isinstance(raw, Mapping):
            raise ProtocolError("plan must be an object")
        session_id = raw.get("session_id")
        turn = raw.get("turn")
        if not isinstance(session_id, str) or not session_id:
            raise ProtocolError("plan requires non-empty text session_id")
        if isinstance(turn, bool) or not isinstance(turn, int) or turn < 0:
            raise ProtocolError("plan turn must be a non-negative integer")
        intents_raw = raw.get("intents", [])
        if not isinstance(intents_raw, list):
            raise ProtocolError("plan intents must be a list")
        intents = tuple(Intent.parse(item) for item in intents_raw)
        note = raw.get("note", "")
        if not isinstance(note, str):
            raise ProtocolError("plan note must be text")
        return cls(session_id=str(session_id), turn=int(turn), intents=intents, note=note)


@dataclass
class Effect:
    session_id: str
    turn: int
    events: tuple[Mapping[str, Any], ...] = field(default_factory=tuple)

    def as_dict(self) -> dict[str, Any]:
        return {
            "schema": EFFECT_SCHEMA,
            "session_id": self.session_id,
            "turn": self.turn,
            "events": [dict(event) for event in self.events],
        }


def _injection_texts(messages: Sequence[Mapping[str, Any]]) -> list[str]:
    found: list[str] = []
    for message in messages:
        text = message.get("text", "") if isinstance(message, Mapping) else ""
        if isinstance(text, str) and any(marker in text.lower() for marker in INJECTION_MARKERS):
            found.append(text)
    return found


def parse_plan_payload(raw: Mapping[str, Any], observation: Observation) -> Plan:
    """Parse and capability-validate a plan against its observation."""
    plan = Plan.parse(raw)
    if plan.session_id != observation.session_id:
        raise ProtocolError("plan session_id does not match observation")
    if plan.turn != observation.turn:
        raise ProtocolError("plan turn does not match observation")
    seen_units: set[str] = set()
    for intent in plan.intents:
        if intent.unit_id in seen_units:
            raise ProtocolError(f"one intent per unit per turn: {intent.unit_id}")
        seen_units.add(intent.unit_id)
        if intent.action not in observation.capabilities:
            raise ProtocolError(f"action {intent.action!r} outside advertised capabilities")
        if intent.action not in EXECUTABLE_ACTIONS:
            raise ProtocolError(f"action {intent.action!r} is regulatory, not executable")
    return plan


def build_legal_actions(field: Any) -> tuple[LegalAction, ...]:
    """Legal relocate actions for every unit, from canonical field geometry."""
    actions: list[LegalAction] = []
    for unit in field.occupants.values():
        for tile_id in field.neighbors(unit.tile_id):
            if field.occupant_on(tile_id) is None:
                actions.append(
                    LegalAction(
                        unit_id=unit.unit_id,
                        action="relocate",
                        from_tile_id=unit.tile_id,
                        to_tile_id=tile_id,
                    )
                )
    return tuple(actions)
