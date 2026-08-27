# ratios: loc_comments=108:6 imports_exports=6:2 calls_definitions=42:15
"""DeepSeek AHBG realization — append-only event log with hash chain.

Independent implementation. The event-kind envelope is shared protocol:
``plane.init``, ``turn.begin``, ``move``, ``turn.end``. The serialization and
chain layout below are DeepSeek's own.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from typing import Any

from .world import canonical_json

EVENT_SCHEMA = "interdependency.ahbg.deepseek.event/1.0.0"

KIND_PLANE_INIT = "plane.init"
KIND_TURN_BEGIN = "turn.begin"
KIND_TURN_END = "turn.end"
KIND_MOVE = "move"
KIND_BUILD = "build"

_EVENT_KEYS = ("schema", "seq", "turn", "kind", "data", "prev")


@dataclass(frozen=True)
class Event:
    seq: int
    turn: int
    kind: str
    data: dict[str, Any]
    prev: str

    def __post_init__(self) -> None:
        if isinstance(self.seq, bool) or not isinstance(self.seq, int) or self.seq < 0:
            raise ValueError("event seq must be a non-negative integer")
        if isinstance(self.turn, bool) or not isinstance(self.turn, int) or self.turn < 0:
            raise ValueError("event turn must be a non-negative integer")
        if not isinstance(self.kind, str) or not self.kind:
            raise ValueError("event kind must be non-empty text")
        if not isinstance(self.data, dict):
            raise ValueError("event data must be an object")
        if not isinstance(self.prev, str):
            raise ValueError("event prev must be a string")

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema": EVENT_SCHEMA,
            "seq": self.seq,
            "turn": self.turn,
            "kind": self.kind,
            "data": self.data,
            "prev": self.prev,
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
            raise ValueError(f"event schema must be {EVENT_SCHEMA!r}")
        unknown = sorted(set(data) - set(_EVENT_KEYS))
        if unknown:
            raise ValueError(f"event has unknown fields: {unknown}")
        missing = sorted(set(_EVENT_KEYS) - set(data))
        if missing:
            raise ValueError(f"event is missing fields: {missing}")
        return cls(
            seq=data["seq"],
            turn=data["turn"],
            kind=data["kind"],
            data=data["data"],
            prev=data["prev"],
        )


class EventLog:
    """Append-only event sequence with a running head digest."""

    def __init__(self) -> None:
        self._events: list[Event] = []
        self._head: str = ""

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
            raise ValueError(f"first event must be {KIND_PLANE_INIT!r}")
        if self._events and turn < self._events[-1].turn:
            raise ValueError("event turns must be non-decreasing")
        event = Event(seq=len(self._events), turn=turn, kind=kind, data=dict(data), prev=self._head)
        self._events.append(event)
        self._head = event.digest()
        return event

    def verify(self) -> None:
        expected = ""
        for index, event in enumerate(self._events):
            if event.seq != index:
                raise ValueError(f"event seq {event.seq} out of order at index {index}")
            if event.prev != expected:
                raise ValueError(f"event seq {event.seq} breaks the hash chain")
            expected = event.digest()
        if expected != self._head:
            raise ValueError("event log head does not match its chain")

    def to_jsonl(self) -> str:
        self.verify()
        return "\n".join(event.canonical_json() for event in self._events) + ("\n" if self._events else "")

    @classmethod
    def from_jsonl(cls, text: str) -> "EventLog":
        log = cls()
        if not text:
            return log
        for line in text.splitlines():
            event = Event.from_dict(json.loads(line))
            log._events.append(event)
            log._head = event.digest()
        log.verify()
        return log
# ratios: loc_comments=108:6 imports_exports=6:2 calls_definitions=42:15
