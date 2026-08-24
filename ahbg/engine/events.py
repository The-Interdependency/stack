"""Append-only event log with a hash chain.

Events are the provenance spine of AHBG. Each event carries the SHA-256
digest of the previous event, so any tampering or truncation breaks
verification. The log is append-only by construction: once an event is
appended it is never mutated or removed.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from typing import Any

from .errors import ValidationError
from .plane import canonical_json

EVENT_SCHEMA = "ahbg.event/1"

KIND_PLANE_INIT = "plane.init"
KIND_TURN_BEGIN = "turn.begin"
KIND_TURN_END = "turn.end"

_EVENT_KEYS = ("schema", "seq", "turn", "kind", "data", "prev_hash")


@dataclass(frozen=True)
class Event:
    """One immutable, append-only engine event."""

    seq: int
    turn: int
    kind: str
    data: dict[str, Any]
    prev_hash: str

    def __post_init__(self) -> None:
        if not isinstance(self.seq, int) or isinstance(self.seq, bool) or self.seq < 0:
            raise ValidationError("event seq must be a non-negative integer")
        if not isinstance(self.turn, int) or isinstance(self.turn, bool) or self.turn < 0:
            raise ValidationError("event turn must be a non-negative integer")
        if not isinstance(self.kind, str) or not self.kind:
            raise ValidationError("event kind must be a non-empty string")
        if not isinstance(self.data, dict):
            raise ValidationError("event data must be an object")
        if not isinstance(self.prev_hash, str):
            raise ValidationError("event prev_hash must be a string")

    def canonical_dict(self) -> dict[str, Any]:
        return {
            "schema": EVENT_SCHEMA,
            "seq": self.seq,
            "turn": self.turn,
            "kind": self.kind,
            "data": self.data,
            "prev_hash": self.prev_hash,
        }

    def canonical_json(self) -> str:
        return canonical_json(self.canonical_dict())

    def digest(self) -> str:
        return hashlib.sha256(self.canonical_json().encode("utf-8")).hexdigest()

    @classmethod
    def from_dict(cls, data: Any) -> "Event":
        if not isinstance(data, dict):
            raise ValidationError("event must be an object")
        if data.get("schema") != EVENT_SCHEMA:
            raise ValidationError(
                f"event schema must be {EVENT_SCHEMA!r}, got {data.get('schema')!r}"
            )
        unknown = sorted(set(data) - set(_EVENT_KEYS))
        if unknown:
            raise ValidationError(f"event has unknown fields: {unknown}")
        missing = sorted(set(_EVENT_KEYS) - set(data))
        if missing:
            raise ValidationError(f"event is missing fields: {missing}")
        return cls(
            seq=data["seq"],
            turn=data["turn"],
            kind=data["kind"],
            data=data["data"],
            prev_hash=data["prev_hash"],
        )


@dataclass
class EventLog:
    """Append-only event sequence with a running head hash."""

    _events: list[Event] = field(default_factory=list)
    _head_hash: str = ""

    @property
    def events(self) -> tuple[Event, ...]:
        """Immutable view of the appended events."""
        return tuple(self._events)

    @property
    def head_hash(self) -> str:
        return self._head_hash

    def __len__(self) -> int:
        return len(self._events)

    def append(self, kind: str, turn: int, data: dict[str, Any]) -> Event:
        """Append one event and advance the head hash.

        The first event of a log must be ``plane.init`` so replay always has
        a bootstrap point. Turns must be non-decreasing across the log.
        """
        if not isinstance(data, dict):
            raise ValidationError("event data must be an object")
        if not isinstance(kind, str) or not kind:
            raise ValidationError("event kind must be a non-empty string")
        if not self._events and kind != KIND_PLANE_INIT:
            raise ValidationError(
                f"first event must be {KIND_PLANE_INIT!r}, got {kind!r}"
            )
        if self._events and turn < self._events[-1].turn:
            raise ValidationError("event turns must be non-decreasing")
        event = Event(
            seq=len(self._events),
            turn=turn,
            kind=kind,
            data=dict(data),
            prev_hash=self._head_hash,
        )
        self._events.append(event)
        self._head_hash = event.digest()
        return event

    def verify(self) -> None:
        """Recompute the hash chain and fail closed on any divergence."""
        expected_prev = ""
        for index, event in enumerate(self._events):
            if event.seq != index:
                raise ValidationError(
                    f"event seq {event.seq} out of order at index {index}"
                )
            if event.prev_hash != expected_prev:
                raise ValidationError(
                    f"event seq {event.seq} breaks the hash chain"
                )
            expected_prev = event.digest()
        if expected_prev != self._head_hash:
            raise ValidationError("event log head hash does not match its chain")

    def to_jsonl(self) -> str:
        self.verify()
        return "\n".join(event.canonical_json() for event in self._events) + (
            "\n" if self._events else ""
        )

    @classmethod
    def from_jsonl(cls, text: str) -> "EventLog":
        log = cls()
        if not text:
            return log
        for line in text.splitlines():
            event = Event.from_dict(json.loads(line))
            log._events.append(event)
            log._head_hash = event.digest()
        log.verify()
        return log
