"""Append-only hash-chained chronicle for the Grok AHBG field."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from typing import Any


SCHEMA = "interdependency.ahbg.grok.event/1"
KIND_PLANE_INIT = "plane.init"
KIND_TURN_BEGIN = "turn.begin"
KIND_MOVE = "move"
KIND_WAR = "war"
KIND_TURN_END = "turn.end"
KIND_FORK = "lineage.fork"


def _dump(obj: Any) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def _digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class Record:
    seq: int
    turn: int
    kind: str
    data: dict[str, Any]
    prev: str

    def payload(self) -> dict[str, Any]:
        return {
            "schema": SCHEMA,
            "seq": self.seq,
            "turn": self.turn,
            "kind": self.kind,
            "data": self.data,
            "prev": self.prev,
        }

    def digest(self) -> str:
        return _digest(_dump(self.payload()))


@dataclass
class Chain:
    records: list[Record] = field(default_factory=list)

    def append(self, kind: str, turn: int, data: dict[str, Any]) -> Record:
        prev = self.records[-1].digest() if self.records else "0" * 64
        record = Record(seq=len(self.records), turn=turn, kind=kind, data=dict(data), prev=prev)
        self.records.append(record)
        return record

    def verify(self) -> None:
        expect = "0" * 64
        for index, record in enumerate(self.records):
            if record.seq != index:
                raise ValueError("chronicle sequence broken")
            if record.prev != expect:
                raise ValueError("chronicle hash chain broken")
            expect = record.digest()

    def lines(self) -> list[str]:
        self.verify()
        return [_dump(record.payload()) for record in self.records]
