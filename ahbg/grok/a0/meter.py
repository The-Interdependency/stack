"""Raw calibration telemetry. Unknowns stay hmmm; nothing is synthesized."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class Meter:
    rows: list[dict[str, Any]] = field(default_factory=list)

    def note(self, **row: Any) -> None:
        payload = dict(row)
        for key in ("tokens", "latency", "retries", "tool_calls"):
            payload.setdefault(key, "hmmm")
        self.rows.append(payload)

    def lines(self) -> list[str]:
        import json

        return [json.dumps(row, sort_keys=True, separators=(",", ":")) for row in self.rows]
