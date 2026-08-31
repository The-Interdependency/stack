"""Codex AHBG event log."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Any

from .world import canonical_json

EVENT_SCHEMA = "interdependency.ahbg.codex.event/1.0.0"
KIND_PLANE_INIT = "plane.init"
KIND_TURN_BEGIN = "turn.begin"
KIND_MOVE = "move"
KIND_WAR = "war"
KIND_TURN_END = "turn.end"


@dataclass(frozen=True)
class Event:
    seq: int
    turn: int
    kind: str
    data: dict[str, Any]
    prev_digest: str

    def __post_init__(self) -> None:
        if isinstance(self.seq, bool) or not isinstance(self.seq, int) or self.seq < 0:
            raise ValueError("event seq must be a non-negative integer")
        if isinstance(self.turn, bool) or not isinstance(self.turn, int) or self.turn < 0:
            raise ValueError("event turn must be a non-negative integer")
        if not isinstance(self.kind, str) or not self.kind:
            raise ValueError("event kind must be non-empty text")
        if not isinstance(self.data, dict):
            raise ValueError("event data must be an object")
        if not isinstance(self.prev_digest, str):
            raise ValueError("event prev_digest must be text")

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema": EVENT_SCHEMA,
            "seq": self.seq,
            "turn": self.turn,
            "kind": self.kind,
            "data": self.data,
            "prev_digest": self.prev_digest,
        }

    def canonical_json(self) -> str:
        return canonical_json(self.to_dict())

    def digest(self) -> str:
        return hashlib.sha256(self.canonical_json().encode("utf-8")).hexdigest()

    @classmethod
    def from_dict(cls, data: Any) -> "Event":
        if not isinstance(data, dict):
            raise ValueError("event must be an object")
        if data.get("schema") != EVENT_SCHEMA:
            raise ValueError(f"event schema must be {EVENT_SCHEMA}")
        allowed = {"schema", "seq", "turn", "kind", "data", "prev_digest"}
        unknown = sorted(set(data) - allowed)
        if unknown:
            raise ValueError(f"event has unknown fields: {unknown}")
        missing = sorted(allowed - set(data))
        if missing:
            raise ValueError(f"event is missing fields: {missing}")
        return cls(
            seq=data["seq"],
            turn=data["turn"],
            kind=data["kind"],
            data=data["data"],
            prev_digest=data["prev_digest"],
        )


class EventLog:
    """Append-only, hash-chained event sequence."""

    def __init__(self) -> None:
        self._events: list[Event] = []
        self._head = ""

    @property
    def events(self) -> tuple[Event, ...]:
        return tuple(self._events)

    @property
    def head(self) -> str:
        return self._head

    def __len__(self) -> int:
        return len(self._events)

    def append(self, kind: str, turn: int, data: dict[str, Any]) -> Event:
        if not self._events and kind != KIND_PLANE_INIT:
            raise ValueError("first event must be plane.init")
        if self._events and turn < self._events[-1].turn:
            raise ValueError("event turn moved backward")
        event = Event(
            seq=len(self._events),
            turn=turn,
            kind=kind,
            data=dict(data),
            prev_digest=self._head,
        )
        self._events.append(event)
        self._head = event.digest()
        return event

    def verify(self) -> None:
        expected = ""
        for index, event in enumerate(self._events):
            if event.seq != index:
                raise ValueError(f"event seq mismatch at index {index}")
            if event.prev_digest != expected:
                raise ValueError(f"event {event.seq} breaks hash chain")
            expected = event.digest()
        if expected != self._head:
            raise ValueError("event log head digest mismatch")

    def to_jsonl(self) -> str:
        self.verify()
        return "\n".join(event.canonical_json() for event in self._events) + ("\n" if self._events else "")

    @classmethod
    def from_jsonl(cls, text: str) -> "EventLog":
        log = cls()
        for line in text.splitlines():
            if not line.strip():
                continue
            event = Event.from_dict(json.loads(line))
            log._events.append(event)
            log._head = event.digest()
        log.verify()
        return log
