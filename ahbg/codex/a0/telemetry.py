"""Ordered telemetry for Codex A0 calibration runs."""

from __future__ import annotations

import json
import time
from typing import Any, Mapping


class Telemetry:
    """Append-only runtime event stream for one A0 scenario."""

    def __init__(self, instance_id: str, run_id: str, provider: str, scenario_id: str, seed: int) -> None:
        self._records: list[dict[str, Any]] = []
        self._seq = 0
        self.instance_id = instance_id
        self.run_id = run_id
        self.provider = provider
        self.scenario_id = scenario_id
        self.seed = seed

    def record(self, kind: str, turn: int, data: Mapping[str, Any]) -> dict[str, Any]:
        item = {
            "seq": self._seq,
            "kind": kind,
            "turn": turn,
            "ts_monotonic_ms": round(time.monotonic() * 1000.0, 3),
            "ts_wall": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "data": dict(data),
        }
        self._seq += 1
        self._records.append(item)
        return item

    def header(self) -> None:
        self.record(
            "instance.identity",
            0,
            {
                "instance_id": self.instance_id,
                "run_id": self.run_id,
                "provider_relation": self.provider,
                "scenario_id": self.scenario_id,
                "seed": self.seed,
            },
        )

    def records(self) -> list[dict[str, Any]]:
        return list(self._records)

    def to_jsonl(self) -> str:
        return "\n".join(
            json.dumps(record, sort_keys=True, separators=(",", ":"))
            for record in self._records
        ) + ("\n" if self._records else "")
