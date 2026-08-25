"""Persistence and replay for the Grok field."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .chain import KIND_MOVE, KIND_PLANE_INIT, KIND_TURN_BEGIN, KIND_TURN_END, Chain, Record, SCHEMA
from .patch import ClosedUnknown, Field


def dump_field(opened: Field, chain: Chain, directory: Path) -> None:
    directory.mkdir(parents=True, exist_ok=True)
    replayed = replay(chain)
    if replayed.snapshot() != opened.snapshot():
        raise ValueError("refuse to write a field that does not replay")
    (directory / "field.json").write_text(json.dumps(opened.snapshot(), indent=2) + "\n", encoding="utf-8")
    (directory / "events.jsonl").write_text("\n".join(chain.lines()) + "\n", encoding="utf-8")


def load_field(directory: Path) -> tuple[Field, Chain]:
    chain = Chain()
    for line in (directory / "events.jsonl").read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        raw = json.loads(line)
        if raw.get("schema") != SCHEMA:
            raise ValueError("unknown event schema")
        chain.records.append(
            Record(seq=raw["seq"], turn=raw["turn"], kind=raw["kind"], data=raw["data"], prev=raw["prev"])
        )
    chain.verify()
    return replay(chain), chain


def replay(chain: Chain) -> Field:
    chain.verify()
    if not chain.records or chain.records[0].kind != KIND_PLANE_INIT:
        raise ValueError("replay needs plane.init first")
    body = chain.records[0].data["field"]
    opened = Field.open(seed=body["seed"], tiles=body["tiles"], units=body["units"])
    pending: list[tuple[str, str, str]] = []
    phase = "await_begin"
    for record in chain.records[1:]:
        if record.kind == KIND_TURN_BEGIN:
            if phase != "await_begin":
                raise ValueError("turn.begin out of order")
            phase = "open"
            pending = []
        elif record.kind == KIND_MOVE:
            if phase != "open":
                raise ValueError("move outside an open turn")
            data = record.data
            pending.append((data["unit_id"], data["from_tile_id"], data["to_tile_id"]))
        elif record.kind == KIND_TURN_END:
            if phase != "open":
                raise ValueError("turn.end out of order")
            try:
                opened.apply_moves(pending)
            except ClosedUnknown as exc:
                raise ValueError(f"replay hit closed unknown: {exc}") from exc
            digest = record.data.get("state_digest")
            from .chain import _digest, _dump

            if digest != _digest(_dump(opened.snapshot())):
                raise ValueError("replay digest mismatch")
            opened.turn += 1
            phase = "await_begin"
            pending = []
        elif record.kind == "lineage.fork":
            continue
        else:
            raise ValueError(f"unknown kind {record.kind}")
    return opened
